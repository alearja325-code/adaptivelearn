import type { Formato } from './entities/item.entity.js';

// El texto que se le envía a la IA para generar las preguntas de UNA
// evidencia (ADR-045 punto 4). Todo lo que la IA recibe está en este archivo,
// para que el equipo lo revise como cualquier otro código. Por qué dice lo
// que dice: docs/diseno/instrucciones-ia-banco.md.

/** Cuántas preguntas por evidencia (RF-03-01, ADR-016). */
export const ITEMS_POR_EVIDENCIA = 12;

export interface ContextoEvidencia {
  area: string; // nombre del área, como lo escribe el MEN
  grado: { numero: number; nombre: string };
  dba: {
    codigo: string;
    enunciado: string;
    ejemplo: string | null;
    ejemploTieneImagen: boolean;
  };
  evidencia: { numero: number; enunciado: string };
  formato: Formato;
}

export interface Instrucciones {
  sistema: string;
  usuario: string;
}

const NOMBRE_FORMATO: Record<Formato, string> = {
  single_choice: 'selección única',
  matching: 'emparejamiento',
  ordering: 'ordenamiento',
};

const SISTEMA = `Eres un experto en evaluación educativa que escribe preguntas de diagnóstico para estudiantes de colegios de Colombia, de 1.° a 11.° grado. Escribes en español de Colombia, claro y correcto.

Cada pregunta sirve para saber si un estudiante muestra una evidencia de aprendizaje de los Derechos Básicos de Aprendizaje (DBA) del Ministerio de Educación Nacional. La evidencia es un texto oficial: no la cambias, no la amplías y no preguntas por otra cosa.

Respondes solo con un objeto JSON válido, sin texto antes ni después.`;

/** Lo que se pide del formato y la forma exacta de cada pregunta en el JSON. */
const FORMA: Record<Formato, string> = {
  single_choice: `Formato: selección única. Cada pregunta tiene exactamente 4 opciones y solo una es correcta.
- Las 3 opciones incorrectas (distractores) son plausibles: cada una corresponde a un error que un estudiante de este grado podría cometer de verdad.
- En "hipotesis_error" de cada opción incorrecta escribe, en una frase, qué error o confusión llevaría a elegirla. Ese texto lo lee solo el sistema: no se le muestra al estudiante, así que no lo pongas en el enunciado ni en las opciones. En la opción correcta, "hipotesis_error" es null.
- Ninguna opción dice que es la correcta o la incorrecta, ni lleva marcas como "(correcta)".
- Varía la posición de la opción correcta entre las preguntas.

Forma de cada pregunta:
{"enunciado": "…", "opciones": [
  {"texto": "…", "es_correcta": true, "hipotesis_error": null},
  {"texto": "…", "es_correcta": false, "hipotesis_error": "…"},
  {"texto": "…", "es_correcta": false, "hipotesis_error": "…"},
  {"texto": "…", "es_correcta": false, "hipotesis_error": "…"}
]}`,
  ordering: `Formato: ordenamiento. El estudiante ordena entre 3 y 6 elementos (pasos, etapas, hechos o cantidades).
- "orden" es la posición correcta de cada elemento: 1, 2, 3… sin saltos ni repetidos.
- El orden correcto es uno solo y no depende de opiniones.
- Escribe las opciones en un orden distinto del correcto.

Forma de cada pregunta:
{"enunciado": "…", "opciones": [
  {"texto": "…", "orden": 2},
  {"texto": "…", "orden": 1},
  {"texto": "…", "orden": 3}
]}`,
  matching: `Formato: emparejamiento. El estudiante une cada elemento de la izquierda con uno de la derecha. Entre 3 y 5 parejas.
- Cada opción tiene "grupo": "izquierda" o "derecha", y "orden": el número de su pareja. La opción de la izquierda con "orden": 1 va con la de la derecha con "orden": 1, y así.
- Los dos lados tienen la misma cantidad de opciones, y los números de pareja van de 1 al total en cada lado, sin repetirse.
- Cada elemento de la izquierda tiene una sola pareja correcta.

Forma de cada pregunta:
{"enunciado": "…", "opciones": [
  {"texto": "…", "grupo": "izquierda", "orden": 1},
  {"texto": "…", "grupo": "izquierda", "orden": 2},
  {"texto": "…", "grupo": "izquierda", "orden": 3},
  {"texto": "…", "grupo": "derecha", "orden": 2},
  {"texto": "…", "grupo": "derecha", "orden": 1},
  {"texto": "…", "grupo": "derecha", "orden": 3}
]}`,
};

/** El escenario de las preguntas: el ejemplo del DBA (ADR-011), o uno cercano. */
function escenario(ctx: ContextoEvidencia): string {
  const { ejemplo, ejemploTieneImagen } = ctx.dba;
  if (!ejemplo) {
    return `Este DBA no tiene un ejemplo oficial. Propón situaciones cercanas a la vida de un estudiante colombiano de ${ctx.grado.nombre.toLowerCase()} grado (su casa, su colegio, su barrio, el campo o la ciudad), sin suponer cuál es su familia, su escuela o su municipio.`;
  }
  const figura = ejemploTieneImagen
    ? '\n\nEn el documento oficial, este ejemplo trae una figura (una imagen, una tabla o un dibujo) que tú no recibes. No te refieras a ella ni supongas qué muestra: usa solo lo que dice el texto.'
    : '';
  return `Usa como escenario el ejemplo oficial del DBA. No lo copies como pregunta: tómalo como el tipo de situación que el estudiante debe poder resolver, y crea situaciones parecidas y variadas.

Ejemplo oficial del DBA:
"""
${ejemplo}
"""${figura}`;
}

const REGLAS = `Reglas para todas las preguntas:
1. Solo texto. Ninguna pregunta puede pedir mirar una imagen, un mapa, una gráfica, un dibujo o escuchar un audio, porque el estudiante no los verá. Si hace falta una tabla, escríbela en el enunciado con palabras o con líneas de texto; si hace falta una figura, descríbela con sus medidas ("un triángulo de lados 3, 4 y 5 cm").
2. Cada pregunta tiene una sola respuesta correcta, que no depende de opiniones ni de la vida del estudiante.
3. Cada pregunta mide la evidencia indicada, no otra cosa.
4. Nunca uses opciones como "todas las anteriores", "ninguna de las anteriores", "A y B" o "no sé".
5. Usa un lenguaje y unos números adecuados para la edad del grado, y oraciones cortas.
6. No uses nombres de personas reales, de marcas ni de instituciones reales. Usa nombres comunes inventados (por ejemplo, Camila, Andrés, Valentina, Juan).
7. Las preguntas no se repiten: cambia la situación, los datos o lo que se pregunta.
8. No escribas la respuesta dentro del enunciado.`;

/**
 * Arma el texto de una evidencia. La IA debe devolver
 * {"items": [ …12 preguntas con la forma de su formato… ]}.
 */
export function armarInstrucciones(ctx: ContextoEvidencia): Instrucciones {
  const usuario = `Escribe ${ITEMS_POR_EVIDENCIA} preguntas de diagnóstico de ${NOMBRE_FORMATO[ctx.formato]}.

Área: ${ctx.area}
Grado: ${ctx.grado.numero}.° (${ctx.grado.nombre})
DBA ${ctx.dba.codigo}: ${ctx.dba.enunciado}

Evidencia de aprendizaje que miden las preguntas (número ${ctx.evidencia.numero} del DBA):
"""
${ctx.evidencia.enunciado}
"""

${escenario(ctx)}

${REGLAS}

${FORMA[ctx.formato]}

Responde solo con este objeto JSON, con exactamente ${ITEMS_POR_EVIDENCIA} preguntas:
{"items": [ …las ${ITEMS_POR_EVIDENCIA} preguntas… ]}`;
  return { sistema: SISTEMA, usuario };
}
