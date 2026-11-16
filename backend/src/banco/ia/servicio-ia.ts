import type { ServicioIaNombre } from '../entities/experiencia.entity.js';
import type { ContextoEvidencia, Instrucciones } from '../instrucciones-ia.js';

/**
 * El servicio de IA que genera las preguntas de una evidencia (ADR-043
 * punto 3): la generación no sabe cuál es. Hoy hay dos implementaciones:
 * DeepSeek, la real, e IaFalsa, la de las pruebas (ADR-045 punto 5). Agregar
 * Gemini como respaldo sería agregar otra.
 */
export interface ServicioIa {
  /** Se guarda en la experiencia (RI-17): 'gemini' | 'deepseek'. */
  readonly servicio: ServicioIaNombre;
  /** El modelo que responde; también se guarda en la experiencia. */
  readonly modelo: string;
  /**
   * Pide las preguntas de una evidencia y devuelve el JSON que respondió la
   * IA, sin validar. `senal` se aborta cuando se cumple el tiempo límite.
   */
  generar(
    ctx: ContextoEvidencia,
    instrucciones: Instrucciones,
    senal: AbortSignal,
  ): Promise<unknown>;
}

/** Token de inyección del servicio elegido con IA_SERVICIO. */
export const SERVICIO_IA = Symbol('SERVICIO_IA');

/** Una falla del servicio de IA. El mensaje nunca lleva la clave. */
export class ErrorIa extends Error {}
