import {
  BadRequestException,
  ConflictException,
  ForbiddenException,
  Injectable,
  InternalServerErrorException,
  NotFoundException,
} from '@nestjs/common';
import { InjectDataSource } from '@nestjs/typeorm';
import { DataSource, EntityManager } from 'typeorm';
import type { User } from '../user/entities/user.entity.js';
import { Inscripcion } from './entities/inscripcion.entity.js';
import { Presentacion } from './entities/presentacion.entity.js';
import { Respuesta } from './entities/respuesta.entity.js';
import { RespuestaOpcion } from './entities/respuesta-opcion.entity.js';
import { Resultado } from './entities/resultado.entity.js';
import { FiltroInscripcionesDto } from './dto/filtro-inscripciones.dto.js';
import { ResponderDto } from './dto/responder.dto.js';
import { concluir } from './reglas/regla-adaptativa.js';
import {
  evaluarSeleccion,
  SeleccionInvalida,
  type Formato,
  type OpcionDelItem,
} from './reglas/evaluar-seleccion.js';
import {
  azarReal,
  BancoAgotado,
  barajarEstable,
  decidirSiguiente,
} from './reglas/siguiente-pregunta.js';
import { progreso, type Progreso } from './reglas/progreso.js';
import { normalizar } from './reglas/texto.js';

// ---------------------------------------------------------------------------
// Lo que recibe el ESTUDIANTE. Cada forma está escrita aquí, campo por campo:
// nada sale de una fila de la base sin pasar por estas funciones, y ninguna
// tiene `es_correcta`, `hipotesis_error`, `orden`, `correcta`, el número de
// pregunta, cuántas faltan ni un resultado (RF-04-08, ADR-028 punto 4).
// ---------------------------------------------------------------------------

/** Una experiencia en la lista del estudiante (E-29, E-30). */
export interface InscripcionResumen {
  id_inscripcion: number;
  fecha_union: Date;
  progreso: Progreso;
  experiencia: {
    id_experiencia: number;
    nombre: string;
    area: string;
    docente: { nombres: string; apellidos: string };
  };
}

/** E-31: además, cuántas respuestas se perderían al salir (CU-26 paso 2). */
export interface InscripcionDetalle extends InscripcionResumen {
  respuestas: number;
}

/** Una opción como la ve el estudiante: sin `es_correcta`, `orden` ni `hipotesis_error`. */
export interface OpcionParaEstudiante {
  id_opcion: number;
  texto: string;
  /** Solo al emparejar: de qué lado está. */
  grupo?: 'izquierda' | 'derecha';
}

export interface PreguntaParaEstudiante {
  id_item: number;
  enunciado: string;
  formato: Formato;
  opciones: OpcionParaEstudiante[];
}

/** E-32: la pregunta, o `null` si ya concluyeron todas las evidencias (cierre, RF-04-11). */
export interface SiguientePregunta {
  /** 201 si se creó la presentación ahora; 200 si es la misma de antes o el cierre. */
  creada: boolean;
  pregunta: PreguntaParaEstudiante | null;
}

interface FilaResumen {
  id_inscripcion: number;
  id_estudiante: number;
  fecha_union: Date;
  id_experiencia: number;
  nombre: string;
  area: string;
  nombres: string;
  apellidos: string;
  presentaciones: string | number;
  resultados: string | number;
  evidencias: string | number;
  respuestas: string | number;
}

const SQL_RESUMEN = `
  SELECT i.id_inscripcion, i.id_estudiante, i.fecha_union, e.id_experiencia, e.nombre,
         a.nombre AS area, d.nombres, d.apellidos,
         (SELECT COUNT(*) FROM presentacion p WHERE p.id_inscripcion = i.id_inscripcion) AS presentaciones,
         (SELECT COUNT(*) FROM resultado r WHERE r.id_inscripcion = i.id_inscripcion) AS resultados,
         (SELECT COUNT(*) FROM experiencia_evidencia ee WHERE ee.id_experiencia = e.id_experiencia) AS evidencias,
         (SELECT COUNT(*) FROM respuesta rs WHERE rs.id_inscripcion = i.id_inscripcion) AS respuestas
    FROM inscripcion i
    JOIN experiencia e ON e.id_experiencia = i.id_experiencia
    JOIN dba ON dba.codigo_dba = e.codigo_dba
    JOIN area a ON a.codigo_area = dba.codigo_area
    JOIN docente d ON d.id_docente = e.id_docente`;

function aResumen(f: FilaResumen): InscripcionResumen {
  return {
    id_inscripcion: f.id_inscripcion,
    fecha_union: f.fecha_union,
    progreso: progreso(
      Number(f.presentaciones),
      Number(f.resultados),
      Number(f.evidencias),
    ),
    experiencia: {
      id_experiencia: f.id_experiencia,
      nombre: f.nombre,
      area: f.area,
      docente: { nombres: f.nombres, apellidos: f.apellidos },
    },
  };
}

const NO_ENCONTRADA = 'No encontramos esa experiencia.';

/**
 * SUB-04, Diagnóstico (I3): `ServicioDiagnostico` del diagrama de clases
 * (`13`), endpoints E-29 a E-34 (`20` §5), secuencias 5 y 6 (`15`).
 *
 * Lee las tablas de la experiencia y el banco (`experiencia`, `item`,
 * `opcion`, ...) con SQL directo, sin entidades propias: esas tablas son del
 * módulo de experiencias (encargo 06, en paralelo), y así los dos módulos no
 * declaran dos entidades para la misma tabla.
 */
@Injectable()
export class DiagnosticoService {
  /** El azar de ADR-031 punto 5. Las pruebas pueden reemplazarlo. */
  azar: (n: number) => number = azarReal;

  constructor(@InjectDataSource() private readonly dataSource: DataSource) {}

  /** E-29 · CU-21: las experiencias del estudiante, con su progreso. */
  async misInscripciones(
    user: User,
    filtro: FiltroInscripcionesDto,
  ): Promise<InscripcionResumen[]> {
    const filas: FilaResumen[] = await this.dataSource.query(
      `${SQL_RESUMEN} WHERE i.id_estudiante = ? ORDER BY i.fecha_union DESC, i.id_inscripcion DESC`,
      [user.idEstudiante],
    );
    const q = filtro.q ? normalizar(filtro.q) : '';
    return filas
      .map(aResumen)
      .filter((r) => !filtro.progreso || r.progreso === filtro.progreso)
      .filter((r) => !q || normalizar(r.experiencia.nombre).includes(q));
  }

  /**
   * E-30 · CU-22: unirse con el código. `creada` = false si ya estaba
   * inscrito (RI-1): se devuelve la misma inscripción, sin duplicarla.
   */
  async unirse(
    user: User,
    codigo: string,
  ): Promise<{ creada: boolean; inscripcion: InscripcionResumen }> {
    const limpio = codigo.trim().toUpperCase();
    // RI-7: solo una experiencia Publicada admite inscripciones. Un código
    // en Borrador da el MISMO 404 que uno inexistente (CU-22 2a).
    const [exp]: { id_experiencia: number }[] = await this.dataSource.query(
      "SELECT id_experiencia FROM experiencia WHERE codigo_invitacion = ? AND estado = 'Publicada'",
      [limpio],
    );
    if (!exp)
      throw new NotFoundException(
        'No encontramos una experiencia con ese código.',
      );

    const idEstudiante = user.idEstudiante!;
    let creada = false;
    const existente = await this.dataSource.manager.findOneBy(Inscripcion, {
      idEstudiante,
      idExperiencia: exp.id_experiencia,
    });
    let id = existente?.id;
    if (!existente) {
      try {
        const r = await this.dataSource.manager.insert(Inscripcion, {
          idEstudiante,
          idExperiencia: exp.id_experiencia,
          fechaUnion: new Date(),
        });
        id = r.identifiers[0].id as number;
        creada = true;
      } catch (e) {
        // Dos clics a la vez: el UNIQUE de RI-1 frena la segunda; se
        // devuelve la que ganó.
        if ((e as { code?: string }).code !== 'ER_DUP_ENTRY') throw e;
        const otra = await this.dataSource.manager.findOneByOrFail(
          Inscripcion,
          {
            idEstudiante,
            idExperiencia: exp.id_experiencia,
          },
        );
        id = otra.id;
      }
    }
    return { creada, inscripcion: aResumen(await this.filaResumen(id!)) };
  }

  /** E-31 · CU-23 paso 1, CU-26 paso 2: progreso y cuántas respuestas se perderían. */
  async consultar(
    user: User,
    idInscripcion: number,
  ): Promise<InscripcionDetalle> {
    await this.inscripcionDelEstudiante(
      this.dataSource.manager,
      user,
      idInscripcion,
    );
    const fila = await this.filaResumen(idInscripcion);
    return { ...aResumen(fila), respuestas: Number(fila.respuestas) };
  }

  /**
   * E-32 · CU-23: la pregunta pendiente (ADR-031 punto 6), una nueva
   * (ADR-031 punto 5, ADR-024) o ninguna si ya concluyeron todas.
   */
  async siguientePregunta(
    user: User,
    idInscripcion: number,
  ): Promise<SiguientePregunta> {
    return await this.dataSource.transaction(async (m) => {
      // Bloquea la inscripción: dos peticiones a la vez (doble clic, dos
      // pestañas) no crean dos presentaciones.
      const ins = await this.inscripcionDelEstudiante(
        m,
        user,
        idInscripcion,
        true,
      );

      const evidencias: {
        numero_evidencia: number;
        concluida: string | number;
      }[] = await m.query(
        `SELECT ee.numero_evidencia,
                EXISTS (SELECT 1 FROM resultado r WHERE r.id_inscripcion = ? AND r.codigo_dba = ee.codigo_dba
                          AND r.numero_evidencia = ee.numero_evidencia) AS concluida
           FROM experiencia_evidencia ee WHERE ee.id_experiencia = ?`,
        [ins.id, ins.idExperiencia],
      );
      const activos: { id_item: number; numero_evidencia: number }[] =
        await m.query(
          'SELECT id_item, numero_evidencia FROM item WHERE id_experiencia = ? AND excluido = FALSE',
          [ins.idExperiencia],
        );
      const presentados: {
        id_item: number;
        orden_presentacion: number;
        respondida: string | number;
      }[] = await m.query(
        `SELECT p.id_item, p.orden_presentacion,
                  EXISTS (SELECT 1 FROM respuesta r WHERE r.id_inscripcion = p.id_inscripcion AND r.id_item = p.id_item) AS respondida
             FROM presentacion p WHERE p.id_inscripcion = ?`,
        [ins.id],
      );

      let decision;
      try {
        decision = decidirSiguiente(
          {
            evidencias: evidencias.map((e) => ({
              numeroEvidencia: e.numero_evidencia,
              concluida: Number(e.concluida) === 1,
              itemsActivos: activos
                .filter((a) => a.numero_evidencia === e.numero_evidencia)
                .map((a) => a.id_item),
            })),
            presentados: presentados.map((p) => p.id_item),
            pendiente:
              presentados.find((p) => Number(p.respondida) === 0)?.id_item ??
              null,
          },
          this.azar,
        );
      } catch (e) {
        // RI-14 garantiza 6 activos por evidencia al publicar: si faltan, es
        // un error de datos, no del estudiante.
        if (e instanceof BancoAgotado)
          throw new InternalServerErrorException(e.message);
        throw e;
      }

      if (decision.tipo === 'completada')
        return { creada: false, pregunta: null };
      if (decision.tipo === 'presentar') {
        // RI-8: el orden sigue al último, en todo el diagnóstico.
        const orden =
          Math.max(0, ...presentados.map((p) => p.orden_presentacion)) + 1;
        await m.insert(Presentacion, {
          idInscripcion: ins.id,
          idItem: decision.idItem,
          idExperiencia: ins.idExperiencia,
          ordenPresentacion: orden,
          fechaPresentacion: new Date(),
        });
      }
      return {
        creada: decision.tipo === 'presentar',
        pregunta: await this.preguntaParaEstudiante(m, ins.id, decision.idItem),
      };
    });
  }

  /**
   * E-33 · CU-24 y CU-25: guarda la respuesta a la pregunta pendiente y
   * aplica la regla adaptativa. No devuelve nada que diga si acertó ni cómo
   * va (RF-04-08).
   */
  async responder(
    user: User,
    idInscripcion: number,
    dto: ResponderDto,
  ): Promise<void> {
    await this.dataSource.transaction(async (m) => {
      const ins = await this.inscripcionDelEstudiante(
        m,
        user,
        idInscripcion,
        true,
      );

      // RNF-10: una respuesta no se cambia; y solo se responde la pendiente.
      const [presentada]: { respondida: string | number }[] = await m.query(
        `SELECT EXISTS (SELECT 1 FROM respuesta r WHERE r.id_inscripcion = p.id_inscripcion AND r.id_item = p.id_item) AS respondida
           FROM presentacion p WHERE p.id_inscripcion = ? AND p.id_item = ?`,
        [ins.id, dto.id_item],
      );
      if (!presentada)
        throw new ConflictException(
          'Esa no es la pregunta que tienes pendiente.',
        );
      if (Number(presentada.respondida) === 1) {
        throw new ConflictException(
          'Esa pregunta ya la respondiste: una respuesta no se cambia.',
        );
      }

      const [item]: {
        formato: Formato;
        codigo_dba: string;
        numero_evidencia: number;
      }[] = await m.query(
        'SELECT formato, codigo_dba, numero_evidencia FROM item WHERE id_item = ?',
        [dto.id_item],
      );
      const opciones: {
        id_opcion: number;
        es_correcta: number | null;
        orden: number | null;
        grupo: OpcionDelItem['grupo'];
      }[] = await m.query(
        'SELECT id_opcion, es_correcta, orden, grupo FROM opcion WHERE id_item = ?',
        [dto.id_item],
      );

      const seleccion = dto.opciones.map((o) => ({
        idOpcion: o.id_opcion,
        valorDado: o.valor_dado ?? null,
      }));
      let correcta: boolean;
      try {
        correcta = evaluarSeleccion(
          item.formato,
          opciones.map((o) => ({
            idOpcion: o.id_opcion,
            esCorrecta:
              o.es_correcta === null ? null : Number(o.es_correcta) === 1,
            orden: o.orden,
            grupo: o.grupo,
          })),
          seleccion,
        );
      } catch (e) {
        if (e instanceof SeleccionInvalida)
          throw new BadRequestException(e.message);
        throw e;
      }

      // RF-04-06: opciones elegidas, certeza, fecha y si fue correcta
      // (`correcta` como fotografía, ADR-021).
      const r = await m.insert(Respuesta, {
        idInscripcion: ins.id,
        idItem: dto.id_item,
        certeza: dto.certeza,
        fechaRespuesta: new Date(),
        correcta,
      });
      const idRespuesta = r.identifiers[0].id as number;
      await m.insert(
        RespuestaOpcion,
        seleccion.map((s) => ({
          idRespuesta,
          idOpcion: s.idOpcion,
          idItem: dto.id_item,
          valorDado: s.valorDado,
        })),
      );

      // CU-25: la regla, con las respuestas de ESTA evidencia, en orden.
      const deLaEvidencia: { certeza: number; correcta: number }[] =
        await m.query(
          `SELECT r.certeza, r.correcta
           FROM respuesta r
           JOIN presentacion p ON p.id_inscripcion = r.id_inscripcion AND p.id_item = r.id_item
           JOIN item it ON it.id_item = r.id_item
          WHERE r.id_inscripcion = ? AND it.codigo_dba = ? AND it.numero_evidencia = ?
          ORDER BY p.orden_presentacion`,
          [ins.id, item.codigo_dba, item.numero_evidencia],
        );
      const estado = concluir(
        deLaEvidencia.map((x) => ({
          certeza: x.certeza,
          correcta: Number(x.correcta) === 1,
        })),
      );
      if (estado) {
        // RNF-11, ADR-021: el resultado se guarda una vez, con su fecha.
        await m.insert(Resultado, {
          idInscripcion: ins.id,
          idExperiencia: ins.idExperiencia,
          codigoDba: item.codigo_dba,
          numeroEvidencia: item.numero_evidencia,
          estado,
          fechaCalculo: new Date(),
        });
      }
    });
  }

  /** E-34 · CU-26: salir; la base borra en cascada lo respondido (V-11). */
  async salir(user: User, idInscripcion: number): Promise<void> {
    await this.dataSource.transaction(async (m) => {
      const ins = await this.inscripcionDelEstudiante(
        m,
        user,
        idInscripcion,
        true,
      );
      await m.delete(Inscripcion, { id: ins.id });
    });
  }

  // ------------------------------------------------------------- ayudantes

  /** 404 si no existe; 403 si es de otro estudiante (`20` §2.2). */
  private async inscripcionDelEstudiante(
    m: EntityManager,
    user: User,
    idInscripcion: number,
    bloquear = false,
  ): Promise<Inscripcion> {
    const consulta = m
      .createQueryBuilder(Inscripcion, 'i')
      .where('i.id = :id', { id: idInscripcion });
    if (bloquear) consulta.setLock('pessimistic_write');
    const ins = await consulta.getOne();
    if (!ins) throw new NotFoundException(NO_ENCONTRADA);
    if (ins.idEstudiante !== user.idEstudiante) {
      throw new ForbiddenException('Esta inscripción no es tuya.');
    }
    return ins;
  }

  private async filaResumen(idInscripcion: number): Promise<FilaResumen> {
    const [fila]: FilaResumen[] = await this.dataSource.query(
      `${SQL_RESUMEN} WHERE i.id_inscripcion = ?`,
      [idInscripcion],
    );
    if (!fila) throw new NotFoundException(NO_ENCONTRADA);
    return fila;
  }

  /**
   * La pregunta como la ve el estudiante. Las opciones se barajan de forma
   * estable por presentación: el orden guardado (que al ordenar puede ser el
   * correcto) no se filtra, y al retomar ve el mismo orden.
   */
  private async preguntaParaEstudiante(
    m: EntityManager,
    idInscripcion: number,
    idItem: number,
  ): Promise<PreguntaParaEstudiante> {
    const [item]: { id_item: number; enunciado: string; formato: Formato }[] =
      await m.query(
        'SELECT id_item, enunciado, formato FROM item WHERE id_item = ?',
        [idItem],
      );
    const opciones: {
      id_opcion: number;
      texto: string;
      grupo: 'izquierda' | 'derecha' | null;
    }[] = await m.query(
      'SELECT id_opcion, texto, grupo FROM opcion WHERE id_item = ? ORDER BY id_opcion',
      [idItem],
    );
    return {
      id_item: item.id_item,
      enunciado: item.enunciado,
      formato: item.formato,
      opciones: barajarEstable(opciones, idInscripcion * 100_003 + idItem).map(
        (o) =>
          item.formato === 'matching'
            ? { id_opcion: o.id_opcion, texto: o.texto, grupo: o.grupo! }
            : { id_opcion: o.id_opcion, texto: o.texto },
      ),
    };
  }
}
