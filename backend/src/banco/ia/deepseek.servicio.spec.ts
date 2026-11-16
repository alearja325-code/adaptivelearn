import { afterEach, describe, expect, it, vi } from 'vitest';
import {
  DeepSeekServicio,
  DEEPSEEK_MODELO_POR_DEFECTO,
  DEEPSEEK_URL,
} from './deepseek.servicio.js';
import type { ContextoEvidencia } from '../instrucciones-ia.js';

// Nunca llama a DeepSeek (ADR-045 punto 5): fetch es simulado.
const CLAVE = 'clave-de-prueba-que-no-debe-salir';
const ctx = {} as ContextoEvidencia;
const instrucciones = { sistema: 'S', usuario: 'U' };
const senal = () => new AbortController().signal;

describe('DeepSeekServicio', () => {
  afterEach(() => vi.unstubAllGlobals());

  it('pide chat completions en JSON, con el modelo de DEEPSEEK_MODEL y la clave solo en la cabecera', async () => {
    const fetch = vi.fn().mockResolvedValue(
      new Response(
        JSON.stringify({
          choices: [{ message: { content: '{"items": []}' } }],
        }),
        { status: 200 },
      ),
    );
    vi.stubGlobal('fetch', fetch);
    const respuesta = await new DeepSeekServicio(
      CLAVE,
      'deepseek-reasoner',
    ).generar(ctx, instrucciones, senal());
    expect(respuesta).toEqual({ items: [] });
    const [url, init] = fetch.mock.calls[0];
    expect(url).toBe(DEEPSEEK_URL);
    expect(init.headers.Authorization).toBe(`Bearer ${CLAVE}`);
    const cuerpo = JSON.parse(init.body);
    expect(cuerpo).toMatchObject({
      model: 'deepseek-reasoner',
      response_format: { type: 'json_object' },
    });
    expect(cuerpo.messages).toEqual([
      { role: 'system', content: 'S' },
      { role: 'user', content: 'U' },
    ]);
    expect(init.body).not.toContain(CLAVE);
  });

  it('sin DEEPSEEK_MODEL usa el modelo por defecto', () => {
    expect(new DeepSeekServicio(CLAVE, undefined).modelo).toBe(
      DEEPSEEK_MODELO_POR_DEFECTO,
    );
  });

  it('ningún error lleva la clave: sin clave, error HTTP, sin conexión, contenido que no es JSON', async () => {
    const casos: [string | undefined, () => Promise<Response>][] = [
      [undefined, async () => new Response('{}')],
      [
        CLAVE,
        async () => new Response(`clave inválida: ${CLAVE}`, { status: 401 }),
      ],
      [CLAVE, async () => Promise.reject(new TypeError(`falló con ${CLAVE}`))],
      [
        CLAVE,
        async () =>
          new Response(
            JSON.stringify({
              choices: [{ message: { content: 'no es json' } }],
            }),
          ),
      ],
    ];
    for (const [clave, respuesta] of casos) {
      vi.stubGlobal('fetch', vi.fn(respuesta));
      const error = (await new DeepSeekServicio(clave, undefined)
        .generar(ctx, instrucciones, senal())
        .catch((e: unknown) => e)) as Error;
      expect(error).toBeInstanceOf(Error);
      expect(String(error.message)).not.toContain(CLAVE);
      expect(JSON.stringify(error)).not.toContain(CLAVE);
    }
  });
});
