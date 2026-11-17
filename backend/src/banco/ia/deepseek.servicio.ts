import type { ContextoEvidencia, Instrucciones } from '../instrucciones-ia.js';
import { ErrorIa, type ServicioIa } from './servicio-ia.js';

/** La API de DeepSeek es compatible con la de OpenAI (chat completions). */
export const DEEPSEEK_URL = 'https://api.deepseek.com/chat/completions';
export const DEEPSEEK_MODELO_POR_DEFECTO = 'deepseek-chat';

/**
 * DeepSeek (ADR-043): el único servicio de esta versión. La clave sale de
 * DEEPSEEK_API_KEY y el modelo de DEEPSEEK_MODEL. La clave solo viaja en la
 * cabecera de la petición: nunca se escribe en un log, en una respuesta ni en
 * el mensaje de un error.
 */
export class DeepSeekServicio implements ServicioIa {
  readonly servicio = 'deepseek' as const;
  readonly modelo: string;

  constructor(
    private readonly clave: string | undefined,
    modelo: string | undefined,
    private readonly url: string = DEEPSEEK_URL,
  ) {
    this.modelo = modelo?.trim() || DEEPSEEK_MODELO_POR_DEFECTO;
  }

  async generar(
    _ctx: ContextoEvidencia,
    instrucciones: Instrucciones,
    senal: AbortSignal,
  ): Promise<unknown> {
    if (!this.clave?.trim()) {
      throw new ErrorIa('DEEPSEEK_API_KEY no está configurada');
    }
    let respuesta: Response;
    try {
      respuesta = await fetch(this.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${this.clave}`,
        },
        body: JSON.stringify({
          model: this.modelo,
          messages: [
            { role: 'system', content: instrucciones.sistema },
            { role: 'user', content: instrucciones.usuario },
          ],
          // Respuesta en JSON: la API garantiza un objeto JSON válido
          response_format: { type: 'json_object' },
          stream: false,
        }),
        signal: senal,
      });
    } catch (error) {
      // Solo el nombre del error: el de fetch no lleva la clave, pero así no
      // se arrastra nada de la petición
      throw new ErrorIa(
        senal.aborted
          ? 'tiempo límite agotado'
          : `no se pudo conectar (${(error as Error).name})`,
      );
    }
    if (!respuesta.ok) {
      // El código HTTP basta para saber qué pasó (401 clave, 402 saldo, 429
      // límite, 5xx caída); el cuerpo no se copia
      throw new ErrorIa(`DeepSeek respondió ${respuesta.status}`);
    }
    const cuerpo = (await respuesta.json().catch(() => null)) as {
      choices?: { message?: { content?: string } }[];
    } | null;
    const contenido = cuerpo?.choices?.[0]?.message?.content;
    if (typeof contenido !== 'string')
      throw new ErrorIa('la respuesta no trae contenido');
    try {
      return JSON.parse(contenido) as unknown;
    } catch {
      throw new ErrorIa('la respuesta no es JSON');
    }
  }
}
