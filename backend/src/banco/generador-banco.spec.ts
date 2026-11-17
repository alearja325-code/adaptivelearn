import { Logger } from '@nestjs/common';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
  ErrorGeneracion,
  GeneradorBanco,
  leerRespuesta,
} from './generador-banco.js';
import { IaFalsa } from './ia/ia-falsa.js';
import type { ContextoEvidencia } from './instrucciones-ia.js';
import type { Formato } from './entities/item.entity.js';

const ctx = (
  numero: number,
  formato: Formato = 'single_choice',
): ContextoEvidencia => ({
  area: 'Matemáticas',
  grado: { numero: 1, nombre: 'Primero' },
  dba: {
    codigo: 'MAT-01-04',
    enunciado: 'Reconoce y compara atributos.',
    ejemplo: null,
    ejemploTieneImagen: false,
  },
  evidencia: { numero, enunciado: `Evidencia ${numero}` },
  formato,
});
const rapido = { tiempoLimiteMs: 200, concurrencia: 3, intentos: 2 };

describe('GeneradorBanco (ADR-045)', () => {
  let ia: IaFalsa;
  let avisos: string[];
  beforeEach(() => {
    ia = new IaFalsa();
    avisos = [];
    vi.spyOn(Logger.prototype, 'log').mockImplementation(
      (m: unknown) => void avisos.push(String(m)),
    );
    vi.spyOn(Logger.prototype, 'warn').mockImplementation(
      (m: unknown) => void avisos.push(String(m)),
    );
  });
  afterEach(() => vi.restoreAllMocks());

  it('una llamada por evidencia, 12 ítems cada una, con el formato de su dictamen', async () => {
    const banco = await new GeneradorBanco(ia, rapido).generar('g1', [
      ctx(1),
      ctx(2, 'matching'),
      ctx(3, 'ordering'),
    ]);
    expect([...banco.keys()].sort()).toEqual([1, 2, 3]);
    expect([...banco.values()].every((items) => items.length === 12)).toBe(
      true,
    );
    expect(ia.llamadas.map((l) => l.formato).sort()).toEqual([
      'matching',
      'ordering',
      'single_choice',
    ]);
  });

  it('reintenta una vez: inválida y después válida → lista', async () => {
    ia.programar('MAT-01-04', 2, ['invalida']);
    const banco = await new GeneradorBanco(ia, rapido).generar('g2', [
      ctx(1),
      ctx(2),
    ]);
    expect(banco.get(2)).toHaveLength(12);
    expect(ia.llamadas.filter((l) => l.clave === 'MAT-01-04#2')).toHaveLength(
      2,
    );
  });

  it('dos veces inválida → falla toda la generación', async () => {
    ia.programar('MAT-01-04', 2, ['invalida', 'incompleta']);
    await expect(
      new GeneradorBanco(ia, rapido).generar('g3', [ctx(1), ctx(2)]),
    ).rejects.toBeInstanceOf(ErrorGeneracion);
    expect(ia.llamadas.filter((l) => l.clave === 'MAT-01-04#2')).toHaveLength(
      2,
    );
  });

  it('el tiempo límite cuenta como falla, y el reintento puede salvarla', async () => {
    ia.programar('MAT-01-04', 1, ['lenta']);
    const banco = await new GeneradorBanco(ia, rapido).generar('g4', [ctx(1)]);
    expect(banco.get(1)).toHaveLength(12);
    ia.programar('MAT-01-04', 1, ['lenta', 'error']);
    await expect(
      new GeneradorBanco(ia, rapido).generar('g5', [ctx(1)]),
    ).rejects.toThrow('MAT-01-04 #1');
  });

  it('pide hasta 3 evidencias a la vez, no más', async () => {
    let enCurso = 0;
    let maximo = 0;
    const lenta = new IaFalsa();
    const original = lenta.generar.bind(lenta);
    lenta.generar = async (...args) => {
      enCurso++;
      maximo = Math.max(maximo, enCurso);
      await new Promise((r) => setTimeout(r, 20));
      enCurso--;
      return original(...args);
    };
    await new GeneradorBanco(lenta, rapido).generar(
      'g6',
      [1, 2, 3, 4, 5, 6].map((n) => ctx(n)),
    );
    expect(maximo).toBe(3);
  });

  it('registra cuánto tardó cada evidencia y el total', async () => {
    await new GeneradorBanco(ia, rapido).generar('g7', [ctx(1), ctx(2)]);
    expect(
      avisos.some((a) =>
        /g7: MAT-01-04 #1 \(single_choice\) lista en \d+\.\d s \(intento 1\)/.test(
          a,
        ),
      ),
    ).toBe(true);
    expect(
      avisos.some((a) => /g7: 2 evidencias, 24 ítems, total \d+\.\d s/.test(a)),
    ).toBe(true);
  });
});

describe('leerRespuesta', () => {
  const doce = (formato: Formato) => ({
    items: Array.from({ length: 12 }, () => ({ ...formatoValido[formato] })),
  });
  const formatoValido: Record<Formato, object> = {
    single_choice: {
      enunciado: 'P',
      opciones: [
        { texto: 'a', es_correcta: true, hipotesis_error: null },
        { texto: 'b', es_correcta: false, hipotesis_error: 'h' },
      ],
    },
    ordering: {
      enunciado: 'P',
      opciones: [
        { texto: 'a', orden: 1 },
        { texto: 'b', orden: 2 },
      ],
    },
    matching: {
      enunciado: 'P',
      opciones: [
        { texto: 'a', grupo: 'izquierda', orden: 1 },
        { texto: 'b', grupo: 'izquierda', orden: 2 },
        { texto: 'c', grupo: 'derecha', orden: 1 },
        { texto: 'd', grupo: 'derecha', orden: 2 },
      ],
    },
  };

  it('acepta 12 ítems válidos de cada formato', () => {
    for (const f of ['single_choice', 'ordering', 'matching'] as Formato[]) {
      expect(leerRespuesta(f, doce(f))).toHaveLength(12);
    }
  });

  it('rechaza: sin "items", otra cantidad, un ítem inválido, un distractor sin hipótesis y «todas las anteriores»', () => {
    expect(() => leerRespuesta('single_choice', { preguntas: [] })).toThrow(
      'no trae "items"',
    );
    expect(() =>
      leerRespuesta('single_choice', {
        items: doce('single_choice').items.slice(1),
      }),
    ).toThrow('trae 11 ítems');
    const malo = doce('ordering');
    malo.items[4] = {
      enunciado: 'P',
      opciones: [
        { texto: 'a', orden: 1 },
        { texto: 'b', orden: 1 },
      ],
    };
    expect(() => leerRespuesta('ordering', malo)).toThrow('ítem 5');
    const sinHipotesis = doce('single_choice');
    sinHipotesis.items[0] = {
      enunciado: 'P',
      opciones: [
        { texto: 'a', es_correcta: true },
        { texto: 'b', es_correcta: false },
      ],
    };
    expect(() => leerRespuesta('single_choice', sinHipotesis)).toThrow(
      'hipótesis de error',
    );
    const comodin = doce('single_choice');
    comodin.items[0] = {
      enunciado: 'P',
      opciones: [
        { texto: 'a', es_correcta: true },
        {
          texto: 'Todas las anteriores',
          es_correcta: false,
          hipotesis_error: 'h',
        },
      ],
    };
    expect(() => leerRespuesta('single_choice', comodin)).toThrow('anteriores');
  });
});
