// Las reglas del Reporte, sin base de datos ni HTTP (CU-27, CU-28, CU-30).
// El reporte se calcula al abrirlo y no se guarda (ADR-022).
//
//   estadoGeneral       ADR-018 modificada por ADR-022 (4.º estado y
//                       precedencia); `Reporte.estadoGeneral()` de `13`.
//   distribucion        cuántos inscritos en cada estado de UNA evidencia;
//                       `Reporte.distribucion()`.
//   clasificarEvidencia ADR-032, que precisa ADR-013, ADR-017 y ADR-023;
//                       `Reporte.clasificar()`.

import type { EstadoResultado } from '../../diagnostico/reglas/regla-adaptativa.js';

/** El resultado de UNA evidencia para UN estudiante: el guardado, o sin fila. */
export type EstadoEvidencia = EstadoResultado | 'sin_concluir';

/** El estado general de un estudiante frente al DBA (ADR-022). */
export type EstadoGeneral =
  'no_muestra' | 'muestra' | 'no_concluyente' | 'sin_concluir';

/** El orden en que se muestran los grupos de estudiantes (CU-28 paso 2). */
export const ORDEN_GRUPOS: readonly EstadoGeneral[] = [
  'no_muestra',
  'no_concluyente',
  'sin_concluir',
  'muestra',
];

export type Clasificacion =
  'datos_insuficientes' | 'brecha_aparente' | 'sin_brecha_aparente';

/** ADR-013 (vigente en el número, ampliado por ADR-023): 40 % de N. */
export const UMBRAL_DATOS_INSUFICIENTES_PORCIENTO = 40;

/**
 * ADR-022: el estado general de un estudiante, con precedencia explícita.
 * `estados` tiene un valor por CADA evidencia de la experiencia
 * ('sin_concluir' si no hay fila en `resultado`).
 */
export function estadoGeneral(
  estados: readonly EstadoEvidencia[],
): EstadoGeneral {
  if (estados.length === 0)
    throw new Error('Una experiencia sin evidencias no tiene estado general.');
  // 1. No muestra: al menos una evidencia concluida en "no muestra", sin
  //    importar las demás. Tiene precedencia sobre todo lo demás.
  if (estados.includes('no_muestra')) return 'no_muestra';
  // 4. Sin concluir: (no aplica 1) y al menos una sin Resultado.
  if (estados.includes('sin_concluir')) return 'sin_concluir';
  // 2. Muestra: todas concluidas y todas "muestra".
  if (estados.every((e) => e === 'muestra')) return 'muestra';
  // 3. No concluyente: todas concluidas y al menos una "no concluyente".
  return 'no_concluyente';
}

export interface Distribucion {
  muestra: number;
  no_muestra: number;
  no_concluyente: number;
  sin_concluir: number;
}

/** Cuántos estudiantes hay en cada estado, en UNA evidencia o en el estado general. */
export function distribucion(
  estados: readonly EstadoEvidencia[],
): Distribucion {
  const d: Distribucion = {
    muestra: 0,
    no_muestra: 0,
    no_concluyente: 0,
    sin_concluir: 0,
  };
  for (const e of estados) d[e]++;
  return d;
}

/**
 * ADR-032: la clasificación de UNA evidencia sobre N = estudiantes inscritos
 * (la suma de la distribución). Con N = 0 no hay reporte: devuelve null.
 */
export function clasificarEvidencia(d: Distribucion): Clasificacion | null {
  const n = d.muestra + d.no_muestra + d.no_concluyente + d.sin_concluir;
  if (n === 0) return null;
  // 1. "no concluyente" + "sin concluir" ≥ 40 % de N (ADR-013 + ADR-023).
  //    Se compara en enteros (100·k ≥ 40·N) para no depender de decimales.
  if (
    (d.no_concluyente + d.sin_concluir) * 100 >=
    n * UMBRAL_DATOS_INSUFICIENTES_PORCIENTO
  ) {
    return 'datos_insuficientes';
  }
  // 2. Al menos 1 estudiante con "no muestra".
  if (d.no_muestra >= 1) return 'brecha_aparente';
  // 3. Si no.
  return 'sin_brecha_aparente';
}
