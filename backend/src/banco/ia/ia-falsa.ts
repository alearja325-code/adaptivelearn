import type { Formato } from '../entities/item.entity.js';
import {
  ITEMS_POR_EVIDENCIA,
  type ContextoEvidencia,
  type Instrucciones,
} from '../instrucciones-ia.js';
import { ErrorIa, type ServicioIa } from './servicio-ia.js';

/**
 * Qué hace la IA falsa en un intento:
 * - valida: 12 ítems válidos del formato pedido;
 * - invalida: 12 ítems, uno con dos opciones correctas (no pasa RI-4);
 * - incompleta: solo 11 ítems;
 * - lenta: no responde hasta que se agota el tiempo límite;
 * - error: falla (como un 500 del servicio);
 * - no-cabe: 12 ítems válidos, pero el último tiene un enunciado más largo
 *   que la columna TEXT: la generación sale bien y falla al guardar (para
 *   probar que la transacción no deja nada a medias, ADR-027).
 */
export type Comportamiento =
  'valida' | 'invalida' | 'incompleta' | 'lenta' | 'error' | 'no-cabe';

/**
 * La IA de las pruebas (ADR-045 punto 5): nunca llama a DeepSeek. Devuelve
 * ítems fijos y, para cada evidencia, se le puede programar qué hace en cada
 * intento. Lo que no se programa responde válido.
 */
export class IaFalsa implements ServicioIa {
  readonly servicio = 'deepseek' as const; // la columna solo admite gemini | deepseek
  readonly modelo = 'ia-falsa (pruebas)';
  private readonly programa = new Map<string, Comportamiento[]>();
  /** Cada llamada recibida: evidencia, formato y el texto enviado. */
  readonly llamadas: {
    clave: string;
    formato: Formato;
    instrucciones: Instrucciones;
  }[] = [];

  /** Ej.: programar('MAT-01-04', 2, ['invalida', 'invalida']). */
  programar(
    codigoDba: string,
    numero: number,
    intentos: Comportamiento[],
  ): void {
    this.programa.set(`${codigoDba}#${numero}`, [...intentos]);
  }

  reiniciar(): void {
    this.programa.clear();
    this.llamadas.length = 0;
  }

  async generar(
    ctx: ContextoEvidencia,
    instrucciones: Instrucciones,
    senal: AbortSignal,
  ): Promise<unknown> {
    const clave = `${ctx.dba.codigo}#${ctx.evidencia.numero}`;
    this.llamadas.push({ clave, formato: ctx.formato, instrucciones });
    const que = this.programa.get(clave)?.shift() ?? 'valida';
    if (que === 'error') throw new ErrorIa('falla simulada');
    if (que === 'lenta') {
      await new Promise<void>((resolver) =>
        senal.addEventListener('abort', () => resolver(), { once: true }),
      );
      throw new ErrorIa('tiempo límite agotado');
    }
    const items = Array.from({ length: ITEMS_POR_EVIDENCIA }, (_, i) =>
      itemFalso(ctx, i + 1),
    );
    if (que === 'incompleta') items.pop();
    if (que === 'no-cabe')
      items[ITEMS_POR_EVIDENCIA - 1].enunciado += ' x'.repeat(40_000);
    if (que === 'invalida' && ctx.formato === 'single_choice') {
      (items[0].opciones as { es_correcta: boolean }[])[1].es_correcta = true;
    } else if (que === 'invalida') {
      items[0].enunciado = '';
    }
    return { items };
  }
}

function itemFalso(
  ctx: ContextoEvidencia,
  i: number,
): { enunciado: string; opciones: object[] } {
  const base = `Pregunta ${i} de ${ctx.dba.codigo}, evidencia ${ctx.evidencia.numero}`;
  if (ctx.formato === 'ordering') {
    return {
      enunciado: `${base}: ordena los pasos.`,
      opciones: [3, 1, 4, 2].map((orden) => ({
        texto: `Paso ${orden}`,
        orden,
      })),
    };
  }
  if (ctx.formato === 'matching') {
    return {
      enunciado: `${base}: une cada término con su pareja.`,
      opciones: [
        ...[1, 2, 3].map((orden) => ({
          texto: `Término ${orden}`,
          grupo: 'izquierda',
          orden,
        })),
        ...[2, 3, 1].map((orden) => ({
          texto: `Pareja ${orden}`,
          grupo: 'derecha',
          orden,
        })),
      ],
    };
  }
  return {
    enunciado: `${base}: ¿cuál es la respuesta correcta?`,
    opciones: [
      {
        texto: 'La respuesta correcta',
        es_correcta: true,
        hipotesis_error: null,
      },
      {
        texto: 'Un distractor',
        es_correcta: false,
        hipotesis_error: 'Confunde un concepto con otro.',
      },
      {
        texto: 'Otro distractor',
        es_correcta: false,
        hipotesis_error: 'Hace el cálculo al revés.',
      },
      {
        texto: 'Un tercer distractor',
        es_correcta: false,
        hipotesis_error: 'Generaliza un caso particular.',
      },
    ],
  };
}
