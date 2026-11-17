import {
  BadRequestException,
  ConflictException,
  ForbiddenException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { InjectDataSource } from '@nestjs/typeorm';
import { DataSource, type EntityManager } from 'typeorm';
import type { FiltroBancoDto } from './dto/filtros.dto.js';
import type { ItemDto } from './dto/item.dto.js';
import type { EstadoExperiencia } from './entities/experiencia.entity.js';
import type { Formato, OrigenItem } from './entities/item.entity.js';
import type { Grupo } from './entities/opcion.entity.js';
import {
  conteoEvidencias,
  insertarItem,
  insertarOpciones,
  type EvidenciaConteo,
} from './experiencias.service.js';
import { experienciaPropia } from './propiedad.js';
import { normalizarOpciones, validarItem } from './validar-item.js';

/** Una opción como la ve el docente: sin hipotesis_error (ADR-008, ADR-020). */
export interface OpcionVista {
  id: number;
  texto: string;
  orden: number | null;
  esCorrecta: boolean | null;
  grupo: Grupo | null;
}

export interface ItemVista {
  id: number;
  numeroEvidencia: number;
  enunciado: string;
  formato: Formato;
  origen: OrigenItem;
  excluido: boolean;
  opciones: OpcionVista[];
}

export interface BancoVista {
  idExperiencia: number;
  estado: EstadoExperiencia;
  // Publicada: el banco está congelado (CU-17 4a, ADR-026)
  soloLectura: boolean;
  evidencias: (EvidenciaConteo & { items: ItemVista[] })[];
}

const MENSAJE_CONGELADO =
  'La experiencia está publicada: su banco ya no se puede cambiar.';

interface ItemDueno {
  id: number;
  idExperiencia: number;
  formato: Formato;
  origen: OrigenItem;
}

/** SUB-03, el banco de preguntas (`20` §4.3): ServicioBanco de `13`. */
@Injectable()
export class BancoService {
  constructor(@InjectDataSource() private readonly dataSource: DataSource) {}

  /**
   * E-24 — el banco (CU-17): las evidencias en orden oficial, cada una con
   * sus ítems y cuántos activos le faltan para publicar. `formato` y `q`
   * filtran los ítems; los conteos son siempre los de la evidencia entera, y
   * una evidencia sin ítems que cumplan el filtro no se muestra.
   */
  async banco(
    idDocente: number,
    idExperiencia: number,
    filtro: FiltroBancoDto,
  ): Promise<BancoVista> {
    const experiencia = await experienciaPropia(
      this.dataSource.manager,
      idExperiencia,
      idDocente,
    );
    const conteos = await conteoEvidencias(
      this.dataSource.manager,
      idExperiencia,
    );
    const items = await itemsDe(
      this.dataSource.manager,
      'i.id_experiencia = ?',
      [idExperiencia],
    );
    const q = filtro.q?.trim().toLocaleLowerCase('es');
    const cumple = (item: ItemVista): boolean =>
      (!filtro.formato || item.formato === filtro.formato) &&
      (!q ||
        item.enunciado.toLocaleLowerCase('es').includes(q) ||
        item.opciones.some((o) => o.texto.toLocaleLowerCase('es').includes(q)));
    const hayFiltro = Boolean(filtro.formato || q);

    return {
      idExperiencia,
      estado: experiencia.estado,
      soloLectura: experiencia.estado === 'Publicada',
      evidencias: conteos
        .map((e) => ({
          ...e,
          items: items.filter(
            (i) => i.numeroEvidencia === e.numero && cumple(i),
          ),
        }))
        .filter((e) => !hayFiltro || e.items.length > 0),
    };
  }

  /**
   * E-25 — edita un ítem (CU-18). Se reemplazan todas sus opciones; un ítem
   * de la IA pasa a `editado_docente` (RF-03-03). La hipótesis de error de una
   * opción incorrecta se conserva si su texto no cambió: el docente no la ve
   * (ADR-008) y por eso no puede reescribirla.
   */
  async editarItem(
    idDocente: number,
    idItem: number,
    dto: ItemDto,
  ): Promise<ItemVista> {
    await this.dataSource.transaction(async (m) => {
      const item = await this.itemModificable(m, idDocente, idItem);
      const opciones = validar(item.formato, dto);
      const anteriores = (await m.query(
        'SELECT texto, hipotesis_error AS hipotesis FROM opcion WHERE id_item = ? AND hipotesis_error IS NOT NULL',
        [idItem],
      )) as { texto: string; hipotesis: string }[];
      const hipotesis = new Map(
        anteriores.map((a) => [a.texto.trim(), a.hipotesis]),
      );
      for (const o of opciones) {
        if (item.formato === 'single_choice' && o.es_correcta === false)
          o.hipotesis_error = hipotesis.get(o.texto) ?? null;
      }
      const origen: OrigenItem =
        item.origen === 'ia' ? 'editado_docente' : item.origen;
      await m.query(
        'UPDATE item SET enunciado = ?, origen = ? WHERE id_item = ?',
        [dto.enunciado.trim(), origen, idItem],
      );
      await m.query('DELETE FROM opcion WHERE id_item = ?', [idItem]);
      await insertarOpciones(m, idItem, {
        enunciado: dto.enunciado.trim(),
        opciones,
      });
    });
    return await this.item(idItem);
  }

  /** E-26 — descarta un ítem (CU-19): no se borra, deja de estar activo (ADR-015). */
  async descartar(idDocente: number, idItem: number): Promise<void> {
    await this.marcarExcluido(idDocente, idItem, true);
  }

  /** E-27 — lo vuelve a incluir, con el mismo contenido (CU-19). */
  async reincluir(idDocente: number, idItem: number): Promise<void> {
    await this.marcarExcluido(idDocente, idItem, false);
  }

  /**
   * E-28 — agrega una pregunta propia (CU-20): activa, de origen
   * `creado_docente`, con el formato del dictamen de su evidencia (RI-19).
   */
  async agregarItem(
    idDocente: number,
    idExperiencia: number,
    numero: number,
    dto: ItemDto,
  ): Promise<ItemVista> {
    const idItem = await this.dataSource.transaction(async (m) => {
      const experiencia = await experienciaPropia(m, idExperiencia, idDocente);
      const [incluida] = (await m.query(
        `SELECT d.formato FROM experiencia_evidencia ee
           JOIN evidencia_dictamen d ON d.codigo_dba = ee.codigo_dba AND d.numero_evidencia = ee.numero_evidencia
          WHERE ee.id_experiencia = ? AND ee.numero_evidencia = ?`,
        [idExperiencia, numero],
      )) as { formato: Formato }[];
      if (!incluida)
        throw new NotFoundException(
          `La evidencia ${numero} no está incluida en esta experiencia.`,
        );
      if (experiencia.estado === 'Publicada')
        throw new ConflictException(MENSAJE_CONGELADO);
      const opciones = validar(incluida.formato, dto);
      return await insertarItem(
        m,
        idExperiencia,
        experiencia.codigoDba,
        numero,
        incluida.formato,
        'creado_docente',
        {
          enunciado: dto.enunciado.trim(),
          opciones,
        },
      );
    });
    return await this.item(idItem);
  }

  private async marcarExcluido(
    idDocente: number,
    idItem: number,
    excluido: boolean,
  ): Promise<void> {
    await this.dataSource.transaction(async (m) => {
      await this.itemModificable(m, idDocente, idItem);
      await m.query('UPDATE item SET excluido = ? WHERE id_item = ?', [
        excluido,
        idItem,
      ]);
    });
  }

  /** El ítem existe (404), su experiencia es del docente (403) y está en Borrador (409). */
  private async itemModificable(
    m: EntityManager,
    idDocente: number,
    idItem: number,
  ): Promise<ItemDueno> {
    const [item] = (await m.query(
      'SELECT id_item AS id, id_experiencia AS idExperiencia, formato, origen FROM item WHERE id_item = ? FOR UPDATE',
      [idItem],
    )) as ItemDueno[];
    if (!item) throw new NotFoundException('No existe ese ítem.');
    const experiencia = await experienciaPropia(
      m,
      item.idExperiencia,
      idDocente,
    ).catch((error: unknown) => {
      throw error instanceof ForbiddenException
        ? new ForbiddenException('Ese ítem no es tuyo.')
        : error;
    });
    if (experiencia.estado === 'Publicada')
      throw new ConflictException(MENSAJE_CONGELADO);
    return item;
  }

  private async item(idItem: number): Promise<ItemVista> {
    const [item] = await itemsDe(this.dataSource.manager, 'i.id_item = ?', [
      idItem,
    ]);
    return item;
  }
}

/** RI-4 con la misma función de la generación (`validarItem`); 400 si no pasa. */
function validar(formato: Formato, dto: ItemDto) {
  const errores = validarItem(formato, dto);
  if (errores.length > 0) throw new BadRequestException(errores);
  return normalizarOpciones(formato, dto.opciones);
}

/** Ítems con sus opciones, en el orden en que se guardaron. */
async function itemsDe(
  m: EntityManager,
  condicion: string,
  valores: unknown[],
): Promise<ItemVista[]> {
  const filas = (await m.query(
    `SELECT i.id_item AS id, i.numero_evidencia AS numeroEvidencia, i.enunciado, i.formato, i.origen, i.excluido,
            o.id_opcion AS idOpcion, o.texto, o.orden, o.es_correcta AS esCorrecta, o.grupo
       FROM item i LEFT JOIN opcion o ON o.id_item = i.id_item
      WHERE ${condicion}
      ORDER BY i.id_item, o.id_opcion`,
    valores,
  )) as {
    id: number;
    numeroEvidencia: number;
    enunciado: string;
    formato: Formato;
    origen: OrigenItem;
    excluido: number | boolean;
    idOpcion: number | null;
    texto: string;
    orden: number | null;
    esCorrecta: number | boolean | null;
    grupo: Grupo | null;
  }[];
  const items = new Map<number, ItemVista>();
  for (const f of filas) {
    let item = items.get(f.id);
    if (!item) {
      item = {
        id: f.id,
        numeroEvidencia: f.numeroEvidencia,
        enunciado: f.enunciado,
        formato: f.formato,
        origen: f.origen,
        excluido: Boolean(f.excluido),
        opciones: [],
      };
      items.set(f.id, item);
    }
    if (f.idOpcion !== null) {
      item.opciones.push({
        id: f.idOpcion,
        texto: f.texto,
        orden: f.orden,
        esCorrecta: f.esCorrecta === null ? null : Boolean(f.esCorrecta),
        grupo: f.grupo,
      });
    }
  }
  return [...items.values()];
}
