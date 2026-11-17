import { describe, expect, it } from 'vitest';
import {
  clasificarEvidencia,
  distribucion,
  estadoGeneral,
  type EstadoEvidencia,
} from './clasificacion.js';

const M = 'muestra',
  NM = 'no_muestra',
  NC = 'no_concluyente',
  SC = 'sin_concluir';

describe('Reporte.estadoGeneral (CU-30, ADR-022 que modifica ADR-018)', () => {
  it('ADR-022 regla 1: una evidencia "no muestra" da No muestra, aunque las demás sean "muestra"', () => {
    expect(estadoGeneral([M, NM, M])).toBe('no_muestra');
  });
  it('ADR-022 regla 1 (prueba de aceptación de CU-30): "no muestra" + una sin concluir = No muestra; la precedencia gana', () => {
    expect(estadoGeneral([NM, SC])).toBe('no_muestra');
    expect(estadoGeneral([SC, SC, NM])).toBe('no_muestra');
  });
  it('ADR-022 regla 1: "no muestra" gana también sobre "no concluyente"', () => {
    expect(estadoGeneral([NC, NM, NC])).toBe('no_muestra');
  });
  it('ADR-022 regla 2: todas concluidas y todas "muestra" = Muestra', () => {
    expect(estadoGeneral([M, M, M])).toBe('muestra');
  });
  it('ADR-022 regla 3: todas concluidas, alguna "no concluyente", ninguna "no muestra" = No concluyente', () => {
    expect(estadoGeneral([M, NC, M])).toBe('no_concluyente');
    expect(estadoGeneral([NC, NC])).toBe('no_concluyente');
  });
  it('ADR-022 regla 4: alguna sin concluir y ninguna "no muestra" = Sin concluir (aunque las demás sean "muestra")', () => {
    expect(estadoGeneral([M, M, SC])).toBe('sin_concluir');
    expect(estadoGeneral([NC, SC])).toBe('sin_concluir');
    expect(estadoGeneral([SC, SC, SC])).toBe('sin_concluir');
  });
  it('ADR-022: las 4 reglas son exhaustivas y no se superponen (todas las combinaciones de 1 a 4 evidencias)', () => {
    const valores: EstadoEvidencia[] = [M, NM, NC, SC];
    for (let n = 1; n <= 4; n++) {
      for (let k = 0; k < 4 ** n; k++) {
        const e = Array.from(
          { length: n },
          (_, i) => valores[Math.floor(k / 4 ** i) % 4],
        );
        // La regla escrita en ADR-022, condición por condición.
        const r1 = e.includes(NM);
        const r2 = !r1 && e.every((x) => x === M);
        const r3 = !r1 && e.every((x) => x !== SC) && e.includes(NC);
        const r4 = !r1 && e.includes(SC);
        expect([r1, r2, r3, r4].filter(Boolean)).toHaveLength(1);
        const esperado = r1
          ? 'no_muestra'
          : r2
            ? 'muestra'
            : r3
              ? 'no_concluyente'
              : 'sin_concluir';
        expect(estadoGeneral(e)).toBe(esperado);
      }
    }
  });
});

describe('Reporte.clasificar (CU-27, ADR-032 que precisa ADR-013, ADR-017 y ADR-023)', () => {
  const d = (m: number, nm: number, nc: number, sc: number) => ({
    muestra: m,
    no_muestra: nm,
    no_concluyente: nc,
    sin_concluir: sc,
  });

  it('ADR-032 regla 1 (prueba de aceptación de CU-27): 10 inscritos, 3 no concluyente + 1 sin concluir = Datos insuficientes', () => {
    expect(clasificarEvidencia(d(5, 1, 3, 1))).toBe('datos_insuficientes');
  });
  it('ADR-032 regla 1: el 40 % exacto ya cuenta (≥, no >)', () => {
    expect(clasificarEvidencia(d(3, 0, 2, 0))).toBe('datos_insuficientes'); // 2/5 = 40 %
  });
  it('ADR-032 regla 1: justo debajo del 40 % no cuenta', () => {
    expect(clasificarEvidencia(d(6, 0, 3, 1))).toBe('datos_insuficientes'); // 4/10 = 40 %
    expect(clasificarEvidencia(d(7, 0, 2, 1))).toBe('sin_brecha_aparente'); // 3/10 = 30 %
    expect(clasificarEvidencia(d(18, 0, 6, 1))).toBe('sin_brecha_aparente'); // 7/25 = 28 %
    expect(clasificarEvidencia(d(14, 1, 9, 1))).toBe('datos_insuficientes'); // 10/25 = 40 %
    expect(clasificarEvidencia(d(15, 1, 8, 1))).toBe('brecha_aparente'); // 9/25 = 36 %
  });
  it('ADR-023: "sin concluir" cuenta hacia Datos insuficientes; una evidencia que nadie empezó lo es', () => {
    expect(clasificarEvidencia(d(0, 0, 0, 7))).toBe('datos_insuficientes');
    expect(clasificarEvidencia(d(3, 0, 0, 2))).toBe('datos_insuficientes');
  });
  it('ADR-032 regla 1 tiene precedencia sobre la 2: con muchos sin concluir, aunque haya "no muestra"', () => {
    expect(clasificarEvidencia(d(1, 2, 0, 2))).toBe('datos_insuficientes');
  });
  it('ADR-032 regla 2: un solo estudiante con "no muestra" basta para Brecha aparente (1/35)', () => {
    expect(clasificarEvidencia(d(34, 1, 0, 0))).toBe('brecha_aparente');
  });
  it('ADR-032 regla 3: nadie con "no muestra" y datos suficientes = Sin brecha aparente', () => {
    expect(clasificarEvidencia(d(10, 0, 0, 0))).toBe('sin_brecha_aparente');
    expect(clasificarEvidencia(d(7, 0, 1, 1))).toBe('sin_brecha_aparente'); // 2/9 = 22 %
  });
  it('ADR-032: con N = 0 no hay reporte (no hay clasificación)', () => {
    expect(clasificarEvidencia(d(0, 0, 0, 0))).toBeNull();
  });
  it('distribución: cuenta cada estado', () => {
    expect(distribucion([M, M, NM, SC, NC, SC])).toEqual(d(2, 1, 1, 2));
  });
});
