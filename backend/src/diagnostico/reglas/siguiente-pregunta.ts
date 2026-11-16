// Qué pregunta sigue (ADR-031 puntos 5 y 6, ADR-024, RI-9), sin base de
// datos ni HTTP: recibe una fotografía del estado de la inscripción y
// decide. `Inscripcion.presentacionPendiente()`, `evidenciaEnCurso()` y
// `presentarSiguiente()` del diagrama de clases (`13`, secuencia 6 de `15`).

import { TOPE_RESPUESTAS } from './regla-adaptativa.js';

/** Una evidencia de la experiencia, con lo que el estudiante lleva en ella. */
export interface EvidenciaEnPlan {
  numeroEvidencia: number;
  /** ¿Ya tiene fila en `resultado`? */
  concluida: boolean;
  /** Ítems activos (no excluidos) de la evidencia. */
  itemsActivos: readonly number[];
}

export interface EstadoInscripcion {
  /** Las evidencias de la experiencia, en cualquier orden. */
  evidencias: readonly EvidenciaEnPlan[];
  /** Ítems ya presentados a este estudiante (con o sin respuesta). */
  presentados: readonly number[];
  /** El ítem presentado y sin responder, si lo hay. */
  pendiente: number | null;
}

export type Decision =
  | { tipo: 'repetir'; idItem: number }
  | { tipo: 'presentar'; idItem: number; numeroEvidencia: number }
  | { tipo: 'completada' };

/** La evidencia no tiene ítems sin ver: no debería pasar si se publicó bien (RI-14). */
export class BancoAgotado extends Error {}

/**
 * `azar(n)` devuelve un entero de 0 a n-1. Se inyecta para que las pruebas
 * puedan fijarlo; en el servicio es `Math.random`.
 */
export function decidirSiguiente(
  estado: EstadoInscripcion,
  azar: (n: number) => number,
): Decision {
  // ADR-031 punto 6: si quedó una pregunta mostrada y sin responder, al
  // volver ve esa misma: no pierde uno de sus 6 cupos.
  if (estado.pendiente !== null)
    return { tipo: 'repetir', idItem: estado.pendiente };

  // ADR-024: orden oficial del DBA (numero_evidencia); ADR-031 punto 5: no
  // se pasa a la siguiente sin concluir la actual.
  const enOrden = [...estado.evidencias].sort(
    (a, b) => a.numeroEvidencia - b.numeroEvidencia,
  );
  const actual = enOrden.find((e) => !e.concluida);
  if (!actual) return { tipo: 'completada' };

  const vistos = new Set(estado.presentados);
  const yaPresentadas = actual.itemsActivos.filter((id) =>
    vistos.has(id),
  ).length;
  // RI-9: no más de 6 presentaciones por evidencia. La regla concluye a más
  // tardar en la 6.ª respuesta, así que llegar aquí sería un error de datos.
  if (yaPresentadas >= TOPE_RESPUESTAS) {
    throw new BancoAgotado(
      `La evidencia ${actual.numeroEvidencia} ya tiene ${yaPresentadas} presentaciones sin concluir.`,
    );
  }
  // ADR-031 punto 5: al azar entre los activos que todavía no vio.
  const candidatos = actual.itemsActivos.filter((id) => !vistos.has(id));
  if (candidatos.length === 0) {
    throw new BancoAgotado(
      `La evidencia ${actual.numeroEvidencia} no tiene preguntas sin ver.`,
    );
  }
  const i = azar(candidatos.length);
  if (!Number.isInteger(i) || i < 0 || i >= candidatos.length)
    throw new Error('azar fuera de rango');
  return {
    tipo: 'presentar',
    idItem: candidatos[i],
    numeroEvidencia: actual.numeroEvidencia,
  };
}

/** El azar del servicio: un entero de 0 a n-1. */
export const azarReal = (n: number): number => Math.floor(Math.random() * n);

/**
 * Baraja las opciones de forma ESTABLE para una presentación: el mismo
 * estudiante ve el mismo orden si retoma la misma pregunta (ADR-031 punto
 * 6), y el orden guardado en la base (que puede seguir el orden correcto,
 * sobre todo al ordenar) no se filtra al estudiante (RF-04-08).
 * Semilla: la presentación (inscripción e ítem). Fisher-Yates con mulberry32.
 */
export function barajarEstable<T>(lista: readonly T[], semilla: number): T[] {
  let s = semilla >>> 0;
  const siguiente = (): number => {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const copia = [...lista];
  for (let i = copia.length - 1; i > 0; i--) {
    const j = Math.floor(siguiente() * (i + 1));
    [copia[i], copia[j]] = [copia[j], copia[i]];
  }
  return copia;
}
