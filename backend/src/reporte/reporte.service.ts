import {
  ForbiddenException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { InjectDataSource } from '@nestjs/typeorm';
import { DataSource } from 'typeorm';
import type { User } from '../user/entities/user.entity.js';
import type { EstadoResultado } from '../diagnostico/reglas/regla-adaptativa.js';
import type { Formato } from '../diagnostico/reglas/evaluar-seleccion.js';
import { normalizar } from '../diagnostico/reglas/texto.js';
import {
  clasificarEvidencia,
  distribucion,
  estadoGeneral,
  ORDEN_GRUPOS,
  type Clasificacion,
  type Distribucion,
  type EstadoEvidencia,
  type EstadoGeneral,
} from './reglas/clasificacion.js';
import { FiltroEstudiantesDto } from './dto/filtro-estudiantes.dto.js';

// ---------------------------------------------------------------------------
// Lo que recibe el DOCENTE. Ninguna forma lleva el correo del estudiante
// (ADR-029 punto 3, RNF-05) ni la hipótesis de error de una opción (ADR-008
// punto 1, ADR-020). Los estados van como códigos, sin texto: los textos los
// pone la pantalla (`13-spec`, `14-spec`, `27-spec`), y ninguno afirma
// certeza (RNF-04).
// ---------------------------------------------------------------------------

export interface EvidenciaDelReporte {
  numero_evidencia: number;
  enunciado: string;
  distribucion: Distribucion;
  /** ADR-032. `null` con N = 0: no hay reporte. */
  clasificacion: Clasificacion | null;
}

/** E-35 · CU-27: se calcula al abrirlo, no se guarda (ADR-022). */
export interface Reporte {
  id_experiencia: number;
  /** N = estudiantes inscritos (ADR-032). */
  inscritos: number;
  /** Cuántos estudiantes hay en cada estado general (CU-27 paso 3, `13-spec` §2.2). */
  estado_general: Distribucion;
  /** En el orden oficial del DBA; la pantalla las agrupa por clasificación (`13-spec` §2.3). */
  evidencias: EvidenciaDelReporte[];
}

export interface EstudianteDelGrupo {
  id_inscripcion: number;
  nombres: string;
  apellidos: string;
  avatar_url: string | null;
  estado_general: EstadoGeneral;
  /** ADR-022, sub-distinción para la interfaz: ¿respondió algo ya? */
  ha_respondido: boolean;
  evidencias: {
    numero_evidencia: number;
    enunciado: string;
    estado: EstadoEvidencia;
  }[];
}

/** E-36 · CU-28: agrupados No muestra, No concluyente, Sin concluir, Muestra; sin grupos vacíos. */
export interface EstudiantesPorEstado {
  id_experiencia: number;
  estado_experiencia: 'Borrador' | 'Publicada';
  inscritos: number;
  grupos: { estado: EstadoGeneral; estudiantes: EstudianteDelGrupo[] }[];
}

export interface PreguntaDelHistorial {
  orden_presentacion: number;
  id_item: number;
  enunciado: string;
  formato: Formato;
  opciones: {
    id_opcion: number;
    texto: string;
    es_correcta: boolean | null;
    orden: number | null;
    grupo: 'izquierda' | 'derecha' | null;
  }[];
  /** null = se le mostró y no la respondió (`27-spec`, "Sin responder"). */
  respuesta: null | {
    correcta: boolean;
    certeza: number;
    fecha_respuesta: Date;
    seleccion: { id_opcion: number; valor_dado: number | null }[];
  };
}

/** E-37 · CU-29: lo que pasó, por evidencia en orden oficial y por pregunta en orden de presentación. */
export interface Historial {
  id_inscripcion: number;
  estudiante: { nombres: string; apellidos: string; avatar_url: string | null };
  evidencias: {
    numero_evidencia: number;
    enunciado: string;
    estado: EstadoEvidencia;
    preguntas: PreguntaDelHistorial[];
  }[];
}

interface Fotografia {
  experiencia: {
    id_experiencia: number;
    estado: 'Borrador' | 'Publicada';
    codigo_dba: string;
  };
  evidencias: { numero_evidencia: number; enunciado: string }[];
  inscritos: {
    id_inscripcion: number;
    nombres: string;
    apellidos: string;
    avatar_url: string | null;
    respuestas: number;
    estados: EstadoEvidencia[];
  }[];
}

/**
 * SUB-05, Reporte y seguimiento (I4): `ServicioReporte` y `Reporte` del
 * diagrama de clases (`13`), endpoints E-35 a E-37 (`20` §6), secuencia 7
 * (`15`). Solo lee. Las reglas viven en `reglas/clasificacion.ts`.
 */
@Injectable()
export class ReporteService {
  constructor(@InjectDataSource() private readonly dataSource: DataSource) {}

  /** E-35 · CU-27 + CU-30. */
  async reporte(user: User, idExperiencia: number): Promise<Reporte> {
    const f = await this.fotografia(user, idExperiencia);
    return {
      id_experiencia: idExperiencia,
      inscritos: f.inscritos.length,
      estado_general: distribucionGeneral(
        f.inscritos.map((i) => estadoGeneral(i.estados)),
      ),
      evidencias: f.evidencias.map((e, k) => {
        const d = distribucion(f.inscritos.map((i) => i.estados[k]));
        return {
          numero_evidencia: e.numero_evidencia,
          enunciado: e.enunciado,
          distribucion: d,
          clasificacion: clasificarEvidencia(d),
        };
      }),
    };
  }

  /** E-36 · CU-28 + CU-30. */
  async estudiantesPorEstado(
    user: User,
    idExperiencia: number,
    filtro: FiltroEstudiantesDto,
  ): Promise<EstudiantesPorEstado> {
    const f = await this.fotografia(user, idExperiencia);
    const q = filtro.q ? normalizar(filtro.q) : '';
    const estudiantes: EstudianteDelGrupo[] = f.inscritos
      .filter(
        (i) => !q || normalizar(`${i.nombres} ${i.apellidos}`).includes(q),
      )
      .map((i) => ({
        id_inscripcion: i.id_inscripcion,
        nombres: i.nombres,
        apellidos: i.apellidos,
        avatar_url: i.avatar_url,
        estado_general: estadoGeneral(i.estados),
        ha_respondido: i.respuestas > 0,
        evidencias: f.evidencias.map((e, k) => ({
          numero_evidencia: e.numero_evidencia,
          enunciado: e.enunciado,
          estado: i.estados[k],
        })),
      }))
      // Alfabético por el nombre que muestra la card: nombres y apellidos (`14-spec` §2.3).
      .sort((a, b) =>
        `${a.nombres} ${a.apellidos}`.localeCompare(
          `${b.nombres} ${b.apellidos}`,
          'es',
          { sensitivity: 'base' },
        ),
      );
    const grupos = ORDEN_GRUPOS.filter(
      (g) => !filtro.estado || g === filtro.estado,
    )
      .map((estado) => ({
        estado,
        estudiantes: estudiantes.filter((e) => e.estado_general === estado),
      }))
      .filter((g) => g.estudiantes.length > 0);
    return {
      id_experiencia: idExperiencia,
      estado_experiencia: f.experiencia.estado,
      inscritos: f.inscritos.length,
      grupos,
    };
  }

  /** E-37 · CU-29: solo el docente dueño; el estudiante nunca (ADR-028). */
  async historial(user: User, idInscripcion: number): Promise<Historial> {
    const [ins]: {
      id_inscripcion: number;
      id_experiencia: number;
      nombres: string;
      apellidos: string;
      avatar_url: string | null;
    }[] = await this.dataSource.query(
      `SELECT i.id_inscripcion, i.id_experiencia, s.nombres, s.apellidos, s.avatar_url
           FROM inscripcion i JOIN estudiante s ON s.id_estudiante = i.id_estudiante
          WHERE i.id_inscripcion = ?`,
      [idInscripcion],
    );
    if (!ins)
      throw new NotFoundException(
        'No encontramos ese estudiante en la experiencia.',
      );
    await this.experienciaDelDocente(user, ins.id_experiencia);

    const evidencias = await this.evidencias(ins.id_experiencia);
    const resultados: { numero_evidencia: number; estado: EstadoResultado }[] =
      await this.dataSource.query(
        'SELECT numero_evidencia, estado FROM resultado WHERE id_inscripcion = ?',
        [idInscripcion],
      );
    const presentadas: {
      orden_presentacion: number;
      id_item: number;
      enunciado: string;
      formato: Formato;
      numero_evidencia: number;
      id_respuesta: number | null;
      correcta: number | null;
      certeza: number | null;
      fecha_respuesta: Date | null;
    }[] = await this.dataSource.query(
      `SELECT p.orden_presentacion, it.id_item, it.enunciado, it.formato, it.numero_evidencia,
              r.id_respuesta, r.correcta, r.certeza, r.fecha_respuesta
         FROM presentacion p
         JOIN item it ON it.id_item = p.id_item
         LEFT JOIN respuesta r ON r.id_inscripcion = p.id_inscripcion AND r.id_item = p.id_item
        WHERE p.id_inscripcion = ?
        ORDER BY p.orden_presentacion`,
      [idInscripcion],
    );
    const ids = presentadas.map((p) => p.id_item);
    // Sin `hipotesis_error`: nunca se nombra ni se reporta (ADR-008 p.1, ADR-020).
    const opciones: {
      id_item: number;
      id_opcion: number;
      texto: string;
      es_correcta: number | null;
      orden: number | null;
      grupo: 'izquierda' | 'derecha' | null;
    }[] =
      ids.length === 0
        ? []
        : await this.dataSource.query(
            'SELECT id_item, id_opcion, texto, es_correcta, orden, grupo FROM opcion WHERE id_item IN (?) ORDER BY id_opcion',
            [ids],
          );
    const idsRespuesta = presentadas
      .filter((p) => p.id_respuesta !== null)
      .map((p) => p.id_respuesta);
    const elegidas: {
      id_respuesta: number;
      id_opcion: number;
      valor_dado: number | null;
    }[] =
      idsRespuesta.length === 0
        ? []
        : await this.dataSource.query(
            'SELECT id_respuesta, id_opcion, valor_dado FROM respuesta_opcion WHERE id_respuesta IN (?) ORDER BY id_opcion',
            [idsRespuesta],
          );

    return {
      id_inscripcion: idInscripcion,
      estudiante: {
        nombres: ins.nombres,
        apellidos: ins.apellidos,
        avatar_url: ins.avatar_url,
      },
      evidencias: evidencias.map((e) => ({
        numero_evidencia: e.numero_evidencia,
        enunciado: e.enunciado,
        estado:
          resultados.find((r) => r.numero_evidencia === e.numero_evidencia)
            ?.estado ?? 'sin_concluir',
        preguntas: presentadas
          .filter((p) => p.numero_evidencia === e.numero_evidencia)
          .map((p) => ({
            orden_presentacion: p.orden_presentacion,
            id_item: p.id_item,
            enunciado: p.enunciado,
            formato: p.formato,
            opciones: opciones
              .filter((o) => o.id_item === p.id_item)
              .map((o) => ({
                id_opcion: o.id_opcion,
                texto: o.texto,
                es_correcta:
                  o.es_correcta === null ? null : Number(o.es_correcta) === 1,
                orden: o.orden,
                grupo: o.grupo,
              })),
            respuesta:
              p.id_respuesta === null
                ? null
                : {
                    correcta: Number(p.correcta) === 1,
                    certeza: p.certeza!,
                    fecha_respuesta: p.fecha_respuesta!,
                    seleccion: elegidas
                      .filter((s) => s.id_respuesta === p.id_respuesta)
                      .map((s) => ({
                        id_opcion: s.id_opcion,
                        valor_dado: s.valor_dado,
                      })),
                  },
          })),
      })),
    };
  }

  // ------------------------------------------------------------- ayudantes

  /** 404 si no existe; 403 si es de otro docente (`20` §2.2). */
  private async experienciaDelDocente(
    user: User,
    idExperiencia: number,
  ): Promise<Fotografia['experiencia']> {
    const [exp]: (Fotografia['experiencia'] & { id_docente: number })[] =
      await this.dataSource.query(
        'SELECT id_experiencia, id_docente, estado, codigo_dba FROM experiencia WHERE id_experiencia = ?',
        [idExperiencia],
      );
    if (!exp) throw new NotFoundException('No encontramos esa experiencia.');
    if (exp.id_docente !== user.idDocente)
      throw new ForbiddenException('Esta experiencia no es tuya.');
    return {
      id_experiencia: exp.id_experiencia,
      estado: exp.estado,
      codigo_dba: exp.codigo_dba,
    };
  }

  private async evidencias(
    idExperiencia: number,
  ): Promise<Fotografia['evidencias']> {
    // ADR-024: el orden oficial del DBA.
    return await this.dataSource.query(
      `SELECT ee.numero_evidencia, ev.enunciado
         FROM experiencia_evidencia ee
         JOIN evidencia ev ON ev.codigo_dba = ee.codigo_dba AND ev.numero_evidencia = ee.numero_evidencia
        WHERE ee.id_experiencia = ?
        ORDER BY ee.numero_evidencia`,
      [idExperiencia],
    );
  }

  /** Todo lo que el reporte necesita, leído una vez: evidencias × inscritos. */
  private async fotografia(
    user: User,
    idExperiencia: number,
  ): Promise<Fotografia> {
    const experiencia = await this.experienciaDelDocente(user, idExperiencia);
    const evidencias = await this.evidencias(idExperiencia);
    const inscritos: {
      id_inscripcion: number;
      nombres: string;
      apellidos: string;
      avatar_url: string | null;
      respuestas: string | number;
    }[] = await this.dataSource.query(
      `SELECT i.id_inscripcion, s.nombres, s.apellidos, s.avatar_url,
                (SELECT COUNT(*) FROM respuesta r WHERE r.id_inscripcion = i.id_inscripcion) AS respuestas
           FROM inscripcion i JOIN estudiante s ON s.id_estudiante = i.id_estudiante
          WHERE i.id_experiencia = ?`,
      [idExperiencia],
    );
    const resultados: {
      id_inscripcion: number;
      numero_evidencia: number;
      estado: EstadoResultado;
    }[] = await this.dataSource.query(
      'SELECT id_inscripcion, numero_evidencia, estado FROM resultado WHERE id_experiencia = ?',
      [idExperiencia],
    );
    const porClave = new Map(
      resultados.map((r) => [
        `${r.id_inscripcion}:${r.numero_evidencia}`,
        r.estado,
      ]),
    );
    return {
      experiencia,
      evidencias,
      inscritos: inscritos.map((i) => ({
        id_inscripcion: i.id_inscripcion,
        nombres: i.nombres,
        apellidos: i.apellidos,
        avatar_url: i.avatar_url,
        respuestas: Number(i.respuestas),
        // ADR-022: sin fila en `resultado` = "sin concluir".
        estados: evidencias.map(
          (e) =>
            porClave.get(`${i.id_inscripcion}:${e.numero_evidencia}`) ??
            'sin_concluir',
        ),
      })),
    };
  }
}

function distribucionGeneral(estados: EstadoGeneral[]): Distribucion {
  return distribucion(estados);
}
