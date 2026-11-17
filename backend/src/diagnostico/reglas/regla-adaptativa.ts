// La regla adaptativa del diagnóstico (CU-25, RF-04-07), escrita UNA sola vez
// y sin base de datos ni HTTP, para poder probar cada caso de ADR-031.
//
// Fuente: ADR-031 (regla exacta), que precisa a ADR-016 (mínimo 4, tope 6)
// y usa el corte de certeza de ADR-008 punto 2 (Hasan, Bagayoko y Kelley,
// 1999). La misma regla está en
// docs/modesec/fase-3-diseno-computacional/uml/regla.py, que usa el
// verificador del diseño; las dos deben decir lo mismo.

/** Estado con que concluye una evidencia (columna `resultado.estado`). */
export type EstadoResultado = 'muestra' | 'no_muestra' | 'no_concluyente';

/** Lo único que la regla necesita de cada respuesta. */
export interface RespuestaEvaluada {
  /** Certeza de 0 a 5 que dio el estudiante (ADR-028 punto 3). */
  certeza: number;
  /** Si fue correcta (ADR-031 punto 3; se calcula con `evaluarSeleccion`). */
  correcta: boolean;
}

/** ADR-031 punto 2: cada respuesta es una de tres señales. */
export type Senal = 'fuerte_muestra' | 'fuerte_no_muestra' | 'debil';

/** ADR-016: ninguna conclusión con menos de 4 respuestas. */
export const MINIMO_RESPUESTAS = 4;
/** ADR-016: a lo sumo 6 respuestas por evidencia. */
export const TOPE_RESPUESTAS = 6;
/** ADR-031 punto 1: certeza alta = 3, 4 o 5. */
export const CERTEZA_ALTA = 3;

/** ADR-031 punto 2. */
export function senal(r: RespuestaEvaluada): Senal {
  if (r.certeza < CERTEZA_ALTA) return 'debil';
  return r.correcta ? 'fuerte_muestra' : 'fuerte_no_muestra';
}

/**
 * ADR-031 punto 4. Recibe TODAS las respuestas de UNA evidencia de un
 * estudiante (en el orden en que respondió) y dice si la evidencia concluye
 * y cómo. `null` = todavía no concluye: hay que presentar otra pregunta de
 * la misma evidencia.
 *
 * Se aplica después de cada respuesta. Si se le pasan más de 6 respuestas
 * es un error del llamador (la regla ya habría concluido en la 6.ª): se
 * rechaza en vez de inventar un resultado.
 */
export function concluir(
  respuestas: readonly RespuestaEvaluada[],
): EstadoResultado | null {
  const n = respuestas.length;
  if (n > TOPE_RESPUESTAS) {
    throw new Error(
      `La regla adaptativa recibió ${n} respuestas; el tope es ${TOPE_RESPUESTAS} (ADR-016).`,
    );
  }
  for (const r of respuestas) {
    if (!Number.isInteger(r.certeza) || r.certeza < 0 || r.certeza > 5) {
      throw new Error(
        `Certeza fuera de la escala 0 a 5: ${r.certeza} (ADR-028).`,
      );
    }
  }
  // Con n menor que 4, nunca se detiene.
  if (n < MINIMO_RESPUESTAS) return null;

  const senales = respuestas.map(senal);
  const muestra = senales.filter((s) => s === 'fuerte_muestra').length;
  const noMuestra = senales.filter((s) => s === 'fuerte_no_muestra').length;

  // "Más de la mitad de las n respuestas": 2·k > n. Las dos no pueden pasar
  // a la vez, porque sumarían más de n.
  if (muestra * 2 > n) return 'muestra';
  if (noMuestra * 2 > n) return 'no_muestra';
  // Al llegar a 6 sin mayoría: No concluyente.
  if (n === TOPE_RESPUESTAS) return 'no_concluyente';
  return null;
}
