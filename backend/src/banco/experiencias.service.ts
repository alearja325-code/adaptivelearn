import {
  ConflictException,
  ForbiddenException,
  Injectable,
  Logger,
  NotFoundException,
} from '@nestjs/common';
import { InjectDataSource } from '@nestjs/typeorm';
import { DataSource, type EntityManager } from 'typeorm';
import { Dba } from '../catalogo/entities/dba.entity.js';
import { nuevoCodigo } from './codigo-invitacion.js';
import type { CrearExperienciaDto } from './dto/crear-experiencia.dto.js';
import type { FiltroExperienciasDto } from './dto/filtros.dto.js';
import type { EstadoExperiencia } from './entities/experiencia.entity.js';
import type { Formato } from './entities/item.entity.js';
import { GeneradorBanco, type ItemGenerado } from './generador-banco.js';
import { Generaciones, type EstadoGeneracion } from './generaciones.js';
import type { ContextoEvidencia } from './instrucciones-ia.js';
import { experienciaPropia, MINIMO_ACTIVOS, patronLike } from './propiedad.js';

/** El texto de la tarjeta de la ventana 007 (V-12, ADR-045 punto 6). */
export const MENSAJE_SIN_EVIDENCIAS =
  'Este DBA no tiene evidencias que se puedan diagnosticar con preguntas cerradas en esta versión.';

export interface GeneracionVista {
  id: string;
  estado: EstadoGeneracion;
  idExperiencia: number | null;
  mensaje: string | null;
}

export interface ExperienciaResumen {
  id: number;
  nombre: string;
  estado: EstadoExperiencia;
  fechaCreacion: Date;
  fechaPublicacion: Date | null;
  dba: { codigo: string };
  area: { codigo: string; nombre: string };
  grado: { numero: number; nombre: string };
  estudiantes: number;
}

export interface EvidenciaConteo {
  numero: number;
  enunciado: string;
  formato: Formato;
  activos: number;
  total: number;
  // cuántos ítems activos faltan para llegar a 6 (CU-13 1a); 0 si ya alcanza
  faltanParaPublicar: number;
}

export interface ExperienciaDetalle extends ExperienciaResumen {
  dba: { codigo: string; enunciado: string };
  servicioIa: string;
  modeloIa: string;
  // lo que se perdería al eliminarla (CU-15 paso 2)
  respuestas: number;
  evidencias: EvidenciaConteo[];
  puedePublicar: boolean;
}

/**
 * SUB-02, experiencias (`20` §4.2): ServicioExperiencias de `13`. Todo lo que
 * modifica es solo del docente dueño (RF-01-04).
 */
@Injectable()
export class ExperienciasService {
  private readonly logger = new Logger('ExperienciasService');

  constructor(
    @InjectDataSource() private readonly dataSource: DataSource,
    private readonly generador: GeneradorBanco,
    private readonly generaciones: Generaciones,
  ) {}

  /**
   * E-19 — crea la experiencia (CU-11) y genera su banco (CU-16). Responde
   * enseguida con el id de la generación (ADR-045 punto 1); la experiencia se
   * guarda solo si el banco salió completo, en una sola transacción (ADR-027).
   */
  async crear(
    idDocente: number,
    dto: CrearExperienciaDto,
  ): Promise<GeneracionVista> {
    const contextos = await this.contextos(dto.codigo_dba);
    const generacion = this.generaciones.crear(idDocente);
    void this.generarYGuardar(generacion.id, idDocente, dto, contextos);
    return this.vistaGeneracion(generacion.id);
  }

  /** GET /experiencias/generaciones/:id — solo la ve quien la pidió. */
  generacion(idDocente: number, id: string): GeneracionVista {
    const generacion = this.generaciones.buscar(id);
    if (!generacion)
      throw new NotFoundException(
        'No existe esa generación, o ya terminó hace más de una hora.',
      );
    if (generacion.idDocente !== idDocente)
      throw new ForbiddenException('Esa generación no es tuya.');
    return this.vistaGeneracion(id);
  }

  /** E-18 — las experiencias del docente (CU-10), las más nuevas primero. */
  async listar(
    idDocente: number,
    filtro: FiltroExperienciasDto,
  ): Promise<ExperienciaResumen[]> {
    const condiciones = ['e.id_docente = ?'];
    const valores: unknown[] = [idDocente];
    if (filtro.estado) {
      condiciones.push('e.estado = ?');
      valores.push(filtro.estado === 'publicada' ? 'Publicada' : 'Borrador');
    }
    if (filtro.q?.trim()) {
      // q busca en el nombre de la experiencia (RF-02-01)
      condiciones.push('e.nombre LIKE ?');
      valores.push(patronLike(filtro.q));
    }
    const filas = (await this.dataSource.query(
      `${SELECT_RESUMEN} WHERE ${condiciones.join(' AND ')} ORDER BY e.fecha_creacion DESC, e.id_experiencia DESC`,
      valores,
    )) as FilaResumen[];
    return filas.map(resumen);
  }

  /** E-20 — el detalle de una experiencia (CU-12, CU-13, CU-15). */
  async consultar(idDocente: number, id: number): Promise<ExperienciaDetalle> {
    await experienciaPropia(this.dataSource.manager, id, idDocente);
    const [fila] = (await this.dataSource.query(
      `${SELECT_RESUMEN} WHERE e.id_experiencia = ?`,
      [id],
    )) as FilaResumen[];
    const [{ respuestas }] = (await this.dataSource.query(
      `SELECT COUNT(*) AS respuestas FROM respuesta r
         JOIN inscripcion i ON i.id_inscripcion = r.id_inscripcion
        WHERE i.id_experiencia = ?`,
      [id],
    )) as { respuestas: number | string }[];
    const evidencias = await conteoEvidencias(this.dataSource.manager, id);
    return {
      ...resumen(fila),
      dba: { codigo: fila.codigoDba, enunciado: fila.dbaEnunciado },
      servicioIa: fila.servicioIa,
      modeloIa: fila.modeloIa,
      respuestas: Number(respuestas),
      evidencias,
      puedePublicar:
        fila.estado === 'Borrador' &&
        evidencias.every((e) => e.faltanParaPublicar === 0),
    };
  }

  /** E-21 — publica (CU-13): no se deshace y congela el banco (ADR-026). */
  async publicar(idDocente: number, id: number): Promise<ExperienciaDetalle> {
    await this.dataSource.transaction(async (m) => {
      // FOR UPDATE: dos «Publicar» seguidos no publican dos veces
      await m.query(
        'SELECT id_experiencia FROM experiencia WHERE id_experiencia = ? FOR UPDATE',
        [id],
      );
      const experiencia = await experienciaPropia(m, id, idDocente);
      if (experiencia.estado === 'Publicada') {
        throw new ConflictException(
          'La experiencia ya está publicada; publicar no se deshace.',
        );
      }
      const faltan = (await conteoEvidencias(m, id)).filter(
        (e) => e.faltanParaPublicar > 0,
      );
      if (faltan.length > 0) {
        const detalle = faltan
          .map(
            (e) =>
              `a la evidencia ${e.numero} le ${e.faltanParaPublicar === 1 ? 'falta 1 ítem activo' : `faltan ${e.faltanParaPublicar} ítems activos`}`,
          )
          .join('; ');
        throw new ConflictException({
          message: `Cada evidencia necesita al menos ${MINIMO_ACTIVOS} ítems activos para publicar: ${detalle}.`,
          evidencias: faltan.map(({ numero, activos, faltanParaPublicar }) => ({
            numero,
            activos,
            faltanParaPublicar,
          })),
        });
      }
      await m.query(
        "UPDATE experiencia SET estado = 'Publicada', fecha_publicacion = ? WHERE id_experiencia = ?",
        [new Date(), id],
      );
    });
    return await this.consultar(idDocente, id);
  }

  /** E-22 — el código de invitación (CU-14); en Borrador no se muestra (RF-02-06). */
  async codigo(idDocente: number, id: number): Promise<{ codigo: string }> {
    const experiencia = await experienciaPropia(
      this.dataSource.manager,
      id,
      idDocente,
    );
    if (experiencia.estado === 'Borrador') {
      throw new ConflictException(
        'El código se muestra cuando la experiencia está publicada.',
      );
    }
    const [{ codigo }] = (await this.dataSource.query(
      'SELECT codigo_invitacion AS codigo FROM experiencia WHERE id_experiencia = ?',
      [id],
    )) as { codigo: string }[];
    return { codigo };
  }

  /**
   * E-23 — elimina la experiencia (CU-15). Lo que cuelga de ella (evidencias
   * incluidas, ítems, opciones, inscripciones, respuestas, resultados) lo
   * borran las llaves foráneas en cascada del esquema (`17`).
   */
  async eliminar(idDocente: number, id: number): Promise<void> {
    await experienciaPropia(this.dataSource.manager, id, idDocente);
    await this.dataSource.query(
      'DELETE FROM experiencia WHERE id_experiencia = ?',
      [id],
    );
  }

  /**
   * Qué se le pide a la IA: una entrada por evidencia cuyo dictamen admite
   * formato cerrado (RI-5), con el formato de ese dictamen (RI-19).
   */
  private async contextos(codigoDba: string): Promise<ContextoEvidencia[]> {
    const dba = await this.dataSource
      .getRepository(Dba)
      .createQueryBuilder('dba')
      .innerJoinAndSelect('dba.area', 'area')
      .innerJoinAndSelect('dba.grado', 'grado')
      .leftJoinAndSelect('dba.evidencias', 'evidencia')
      .leftJoinAndSelect('evidencia.dictamen', 'dictamen')
      .where('dba.codigo_dba = :codigoDba', { codigoDba })
      .orderBy('evidencia.numero_evidencia', 'ASC')
      .getOne();
    if (!dba) throw new NotFoundException(`No existe el DBA ${codigoDba}`);

    const contextos = dba.evidencias
      .filter(
        (e) => e.dictamen?.aplicaFormatoCerrado === true && e.dictamen.formato,
      )
      .map((e): ContextoEvidencia => ({
        area: dba.area.nombre,
        grado: { numero: dba.grado.numero, nombre: dba.grado.nombre },
        dba: {
          codigo: dba.codigo,
          enunciado: dba.enunciado,
          ejemplo: dba.ejemplo,
          ejemploTieneImagen: dba.ejemploTieneImagen,
        },
        evidencia: { numero: e.numero, enunciado: e.enunciado },
        formato: e.dictamen!.formato as Formato,
      }));
    if (contextos.length === 0)
      throw new ConflictException(MENSAJE_SIN_EVIDENCIAS);
    return contextos;
  }

  /** En segundo plano: generar y, si todo salió, guardar todo junto. */
  private async generarYGuardar(
    idGeneracion: string,
    idDocente: number,
    dto: CrearExperienciaDto,
    contextos: ContextoEvidencia[],
  ): Promise<void> {
    try {
      const bancos = await this.generador.generar(idGeneracion, contextos);
      const idExperiencia = await this.dataSource.transaction((m) =>
        this.guardar(m, idDocente, dto, contextos, bancos),
      );
      this.generaciones.lista(idGeneracion, idExperiencia);
    } catch (error) {
      // El detalle va a la consola, sin datos del docente; la pantalla
      // recibe el mensaje de 07-spec (MENSAJE_FALLIDA)
      this.logger.warn(
        `generación ${idGeneracion}: no se guardó nada (${(error as Error).message})`,
      );
      this.generaciones.fallida(idGeneracion);
    }
  }

  /** La experiencia, sus evidencias, sus ítems y sus opciones: todo o nada (ADR-027). */
  private async guardar(
    m: EntityManager,
    idDocente: number,
    dto: CrearExperienciaDto,
    contextos: ContextoEvidencia[],
    bancos: Map<number, ItemGenerado[]>,
  ): Promise<number> {
    const { servicio, modelo } = this.generador.ia;
    const codigo = await codigoLibre(m);
    const { insertId: idExperiencia } = (await m.query(
      `INSERT INTO experiencia (id_docente, codigo_dba, nombre, estado, fecha_creacion, codigo_invitacion, servicio_ia, modelo_ia)
       VALUES (?, ?, ?, 'Borrador', ?, ?, ?, ?)`,
      [
        idDocente,
        dto.codigo_dba,
        dto.nombre,
        new Date(),
        codigo,
        servicio,
        modelo,
      ],
    )) as { insertId: number };

    for (const ctx of contextos) {
      const numero = ctx.evidencia.numero;
      await m.query(
        'INSERT INTO experiencia_evidencia (id_experiencia, codigo_dba, numero_evidencia) VALUES (?, ?, ?)',
        [idExperiencia, dto.codigo_dba, numero],
      );
      const items = bancos.get(numero);
      if (!items) throw new Error(`falta el banco de la evidencia ${numero}`);
      for (const item of items) {
        await insertarItem(
          m,
          idExperiencia,
          dto.codigo_dba,
          numero,
          ctx.formato,
          'ia',
          item,
        );
      }
    }
    return idExperiencia;
  }

  private vistaGeneracion(id: string): GeneracionVista {
    const { estado, idExperiencia, mensaje } = this.generaciones.buscar(id)!;
    return { id, estado, idExperiencia, mensaje };
  }
}

/** Un ítem con sus opciones, ya validado. Lo usan crear (E-19) y agregar (E-28). */
export async function insertarItem(
  m: EntityManager,
  idExperiencia: number,
  codigoDba: string,
  numeroEvidencia: number,
  formato: Formato,
  origen: 'ia' | 'creado_docente',
  item: ItemGenerado,
): Promise<number> {
  const { insertId: idItem } = (await m.query(
    `INSERT INTO item (id_experiencia, codigo_dba, numero_evidencia, enunciado, formato, origen, excluido)
     VALUES (?, ?, ?, ?, ?, ?, FALSE)`,
    [
      idExperiencia,
      codigoDba,
      numeroEvidencia,
      item.enunciado,
      formato,
      origen,
    ],
  )) as { insertId: number };
  await insertarOpciones(m, idItem, item);
  return idItem;
}

export async function insertarOpciones(
  m: EntityManager,
  idItem: number,
  item: ItemGenerado,
): Promise<void> {
  for (const o of item.opciones) {
    await m.query(
      'INSERT INTO opcion (id_item, texto, orden, es_correcta, grupo, hipotesis_error) VALUES (?, ?, ?, ?, ?, ?)',
      [idItem, o.texto, o.orden, o.es_correcta, o.grupo, o.hipotesis_error],
    );
  }
}

/** Un código que no use otra experiencia (RI-3: es único). */
async function codigoLibre(m: EntityManager): Promise<string> {
  for (let intento = 0; intento < 10; intento++) {
    const codigo = nuevoCodigo();
    const usado = (await m.query(
      'SELECT 1 FROM experiencia WHERE codigo_invitacion = ?',
      [codigo],
    )) as unknown[];
    if (usado.length === 0) return codigo;
  }
  // 31^6 ≈ 887 millones de códigos: diez choques seguidos no deberían pasar
  throw new Error('no se encontró un código de invitación libre');
}

/** Cuántos ítems activos y en total tiene cada evidencia incluida, en orden oficial. */
export async function conteoEvidencias(
  m: EntityManager,
  idExperiencia: number,
): Promise<EvidenciaConteo[]> {
  const filas = (await m.query(
    `SELECT ee.numero_evidencia AS numero, ev.enunciado, d.formato,
            COUNT(it.id_item) AS total,
            COALESCE(SUM(it.excluido = FALSE), 0) AS activos
       FROM experiencia_evidencia ee
       JOIN evidencia ev ON ev.codigo_dba = ee.codigo_dba AND ev.numero_evidencia = ee.numero_evidencia
       LEFT JOIN evidencia_dictamen d ON d.codigo_dba = ee.codigo_dba AND d.numero_evidencia = ee.numero_evidencia
       LEFT JOIN item it ON it.id_experiencia = ee.id_experiencia AND it.numero_evidencia = ee.numero_evidencia
      WHERE ee.id_experiencia = ?
      GROUP BY ee.numero_evidencia, ev.enunciado, d.formato
      ORDER BY ee.numero_evidencia`,
    [idExperiencia],
  )) as {
    numero: number;
    enunciado: string;
    formato: Formato;
    total: number | string;
    activos: number | string;
  }[];
  return filas.map((f) => {
    const activos = Number(f.activos);
    return {
      numero: f.numero,
      enunciado: f.enunciado,
      formato: f.formato,
      activos,
      total: Number(f.total),
      faltanParaPublicar: Math.max(0, MINIMO_ACTIVOS - activos),
    };
  });
}

const SELECT_RESUMEN = `
  SELECT e.id_experiencia AS id, e.nombre, e.estado, e.fecha_creacion AS fechaCreacion,
         e.fecha_publicacion AS fechaPublicacion, e.codigo_dba AS codigoDba,
         e.servicio_ia AS servicioIa, e.modelo_ia AS modeloIa, d.enunciado AS dbaEnunciado,
         a.codigo_area AS areaCodigo, a.nombre AS areaNombre, g.numero AS gradoNumero, g.nombre AS gradoNombre,
         (SELECT COUNT(*) FROM inscripcion i WHERE i.id_experiencia = e.id_experiencia) AS estudiantes
    FROM experiencia e
    JOIN dba d ON d.codigo_dba = e.codigo_dba
    JOIN area a ON a.codigo_area = d.codigo_area
    JOIN grado g ON g.numero = d.numero_grado`;

interface FilaResumen {
  id: number;
  nombre: string;
  estado: EstadoExperiencia;
  fechaCreacion: Date;
  fechaPublicacion: Date | null;
  codigoDba: string;
  servicioIa: string;
  modeloIa: string;
  dbaEnunciado: string;
  areaCodigo: string;
  areaNombre: string;
  gradoNumero: number;
  gradoNombre: string;
  estudiantes: number | string;
}

function resumen(f: FilaResumen): ExperienciaResumen {
  return {
    id: f.id,
    nombre: f.nombre,
    estado: f.estado,
    fechaCreacion: f.fechaCreacion,
    fechaPublicacion: f.fechaPublicacion,
    dba: { codigo: f.codigoDba },
    area: { codigo: f.areaCodigo, nombre: f.areaNombre },
    grado: { numero: f.gradoNumero, nombre: f.gradoNombre },
    estudiantes: Number(f.estudiantes),
  };
}
