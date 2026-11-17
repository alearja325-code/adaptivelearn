// El progreso de una inscripción (CU-21, CU-23 paso 1, `04-spec` Badge del
// estudiante, `23-spec` §2.1). Es un atributo CALCULADO del MER: no se
// guarda (`20` E-29).
//   no_iniciada  ninguna Presentación todavía (`23-spec`, Estado A)
//   completada   todas las evidencias tienen Resultado (Estado C)
//   en_curso     lo demás: hay al menos una Presentación (Estado B)

export type Progreso = 'no_iniciada' | 'en_curso' | 'completada';
export const PROGRESOS: readonly Progreso[] = [
  'no_iniciada',
  'en_curso',
  'completada',
];

export function progreso(
  presentaciones: number,
  resultados: number,
  evidencias: number,
): Progreso {
  if (evidencias > 0 && resultados >= evidencias) return 'completada';
  if (presentaciones === 0) return 'no_iniciada';
  return 'en_curso';
}
