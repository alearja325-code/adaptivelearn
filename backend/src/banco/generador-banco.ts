import { Logger } from '@nestjs/common';
import type { Formato } from './entities/item.entity.js';
import {
  armarInstrucciones,
  ITEMS_POR_EVIDENCIA,
  type ContextoEvidencia,
} from './instrucciones-ia.js';
import type { ServicioIa } from './ia/servicio-ia.js';
import {
  normalizarOpciones,
  validarItem,
  type ItemPropuesto,
  type OpcionPropuesta,
} from './validar-item.js';

/** Un ítem que ya pasó la validación, listo para guardarse. */
export interface ItemGenerado {
  enunciado: string;
  opciones: Required<OpcionPropuesta>[];
}

export interface OpcionesGenerador {
  /** Límite de cada llamada a la IA (IA_TIEMPO_LIMITE_MS; por defecto 180000). */
  tiempoLimiteMs: number;
  /** Cuántas evidencias se piden a la vez (ADR-045 punto 2: hasta 3). */
  concurrencia: number;
  /** Intentos por evidencia: el primero y un reintento (ADR-045 punto 3). */
  intentos: number;
}

export const OPCIONES_POR_DEFECTO: OpcionesGenerador = {
  tiempoLimiteMs: 180_000,
  concurrencia: 3,
  intentos: 2,
};

/** La generación falló: una evidencia no salió bien después del reintento. */
export class ErrorGeneracion extends Error {}

/** La respuesta de la IA no sirve; el mensaje dice por qué (sin datos del docente). */
class RespuestaInvalida extends Error {}

const OPCION_COMODIN = /\b(todas las|ninguna de las) anteriores\b/i;

/**
 * Lee lo que respondió la IA para una evidencia: un objeto con exactamente
 * 12 ítems, cada uno válido para su formato (RI-4, `validarItem`, la misma
 * regla de editar y agregar). Además, solo para lo generado: en selección
 * única cada distractor trae su hipótesis de error (ADR-020), y ninguna
 * opción es «todas/ninguna de las anteriores» (ADR-045 punto 4).
 */
export function leerRespuesta(
  formato: Formato,
  respuesta: unknown,
): ItemGenerado[] {
  const items = (respuesta as { items?: unknown } | null)?.items;
  if (!Array.isArray(items))
    throw new RespuestaInvalida('la respuesta no trae "items"');
  if (items.length !== ITEMS_POR_EVIDENCIA) {
    throw new RespuestaInvalida(
      `trae ${items.length} ítems y deben ser ${ITEMS_POR_EVIDENCIA}`,
    );
  }
  return items.map((crudo, i) => {
    const item = crudo as ItemPropuesto;
    const errores = validarItem(formato, item);
    if (errores.length === 0 && formato === 'single_choice') {
      if (
        item.opciones.some(
          (o) => o.es_correcta !== true && !o.hipotesis_error?.trim(),
        )
      ) {
        errores.push('un distractor no trae su hipótesis de error');
      }
    }
    if (
      errores.length === 0 &&
      item.opciones.some((o) => OPCION_COMODIN.test(o.texto))
    ) {
      errores.push('una opción es «todas/ninguna de las anteriores»');
    }
    if (errores.length > 0)
      throw new RespuestaInvalida(`ítem ${i + 1}: ${errores.join(' ')}`);
    return {
      enunciado: item.enunciado.trim(),
      opciones: normalizarOpciones(formato, item.opciones),
    };
  });
}

const segundos = (desde: number): string =>
  `${((Date.now() - desde) / 1000).toFixed(1)} s`;

/**
 * Genera el banco de una experiencia (CU-16, ADR-045): una llamada por
 * evidencia, hasta `concurrencia` a la vez; si una respuesta no llega a
 * tiempo o algún ítem no es válido, esa evidencia se pide una vez más; si
 * vuelve a fallar, falla todo (ADR-027). No guarda nada: eso lo hace quien lo
 * llama, en una sola transacción. Registra en la consola cuánto tardó cada
 * evidencia y el total, para medir RNF-13; sin datos del docente.
 */
export class GeneradorBanco {
  private readonly logger = new Logger('GeneradorBanco');

  constructor(
    readonly ia: ServicioIa,
    private readonly opciones: OpcionesGenerador = OPCIONES_POR_DEFECTO,
  ) {}

  async generar(
    idGeneracion: string,
    contextos: ContextoEvidencia[],
  ): Promise<Map<number, ItemGenerado[]>> {
    const inicio = Date.now();
    const resultado = new Map<number, ItemGenerado[]>();
    const pendientes = [...contextos];
    let falla: ErrorGeneracion | null = null;

    const trabajador = async (): Promise<void> => {
      for (
        let ctx = pendientes.shift();
        ctx && !falla;
        ctx = pendientes.shift()
      ) {
        try {
          resultado.set(
            ctx.evidencia.numero,
            await this.evidencia(idGeneracion, ctx),
          );
        } catch (error) {
          falla ??= error as ErrorGeneracion;
        }
      }
    };
    const cuantos = Math.max(
      1,
      Math.min(this.opciones.concurrencia, contextos.length),
    );
    await Promise.all(Array.from({ length: cuantos }, trabajador));

    if (falla) {
      this.logger.warn(
        `generación ${idGeneracion}: falló en ${segundos(inicio)} (${(falla as Error).message})`,
      );
      throw falla;
    }
    this.logger.log(
      `generación ${idGeneracion}: ${contextos.length} evidencias, ` +
        `${contextos.length * ITEMS_POR_EVIDENCIA} ítems, total ${segundos(inicio)} ` +
        `(${this.ia.servicio}, ${this.ia.modelo})`,
    );
    return resultado;
  }

  /** Una evidencia, con su reintento. */
  private async evidencia(
    idGeneracion: string,
    ctx: ContextoEvidencia,
  ): Promise<ItemGenerado[]> {
    const instrucciones = armarInstrucciones(ctx);
    const quien = `${ctx.dba.codigo} #${ctx.evidencia.numero} (${ctx.formato})`;
    let motivo = '';
    for (let intento = 1; intento <= this.opciones.intentos; intento++) {
      const inicio = Date.now();
      const control = new AbortController();
      const reloj = setTimeout(
        () => control.abort(),
        this.opciones.tiempoLimiteMs,
      );
      try {
        const respuesta = await Promise.race([
          this.ia.generar(ctx, instrucciones, control.signal),
          new Promise<never>((_, rechazar) =>
            control.signal.addEventListener(
              'abort',
              () => rechazar(new Error('tiempo límite agotado')),
              {
                once: true,
              },
            ),
          ),
        ]);
        const items = leerRespuesta(ctx.formato, respuesta);
        this.logger.log(
          `generación ${idGeneracion}: ${quien} lista en ${segundos(inicio)} (intento ${intento})`,
        );
        return items;
      } catch (error) {
        motivo = (error as Error).message;
        this.logger.warn(
          `generación ${idGeneracion}: ${quien} falló en ${segundos(inicio)} (intento ${intento}): ${motivo}`,
        );
      } finally {
        clearTimeout(reloj);
      }
    }
    throw new ErrorGeneracion(`${quien}: ${motivo}`);
  }
}
