// Cuándo una respuesta es correcta (ADR-031 punto 3) y cuándo una selección
// es válida (RI-6), por formato. Sin base de datos ni HTTP: `Item.evaluar()`
// del diagrama de clases (`13`), que la secuencia 6 (`15` §6) llama desde
// `Presentacion.responder()`.
//
// Cómo se guarda cada formato (ADR-014, ADR-019; `18-diccionario-datos`):
//   single_choice  opcion.es_correcta marca la correcta; la selección es una
//                  sola fila, sin valor_dado.
//   ordering       opcion.orden es la posición correcta; valor_dado es la
//                  posición que le dio el estudiante.
//   matching       opcion.grupo dice el lado (izquierda o derecha) y
//                  opcion.orden el número de pareja; valor_dado es el número
//                  de pareja que el estudiante le asignó, compartido por las
//                  2 opciones que emparejó.

export type Formato = 'single_choice' | 'matching' | 'ordering';

/** Una opción del ítem, como está en la tabla `opcion`. */
export interface OpcionDelItem {
  idOpcion: number;
  esCorrecta: boolean | null;
  orden: number | null;
  grupo: 'izquierda' | 'derecha' | null;
}

/** Lo que mandó el estudiante: una fila de `respuesta_opcion`. */
export interface OpcionElegida {
  idOpcion: number;
  valorDado: number | null;
}

/** La selección no cumple RI-6 o la forma de su formato: es un `400`. */
export class SeleccionInvalida extends Error {}

/**
 * Valida la selección contra las opciones del ítem y dice si es correcta.
 * Lanza `SeleccionInvalida` si la selección no se puede guardar.
 *
 * ADR-031 punto 3: en selección única, correcta si eligió la opción
 * correcta; en emparejar y ordenar, solo si TODOS los pares o TODAS las
 * posiciones están bien. Un acierto parcial cuenta como incorrecta.
 */
export function evaluarSeleccion(
  formato: Formato,
  opciones: readonly OpcionDelItem[],
  seleccion: readonly OpcionElegida[],
): boolean {
  // RI-6: al menos una opción, y solo del ítem presentado.
  if (seleccion.length === 0)
    throw new SeleccionInvalida('Elige una respuesta.');
  const porId = new Map(opciones.map((o) => [o.idOpcion, o]));
  const vistas = new Set<number>();
  for (const s of seleccion) {
    if (!porId.has(s.idOpcion)) {
      throw new SeleccionInvalida(
        'Una de las opciones no es de esta pregunta.',
      );
    }
    if (vistas.has(s.idOpcion))
      throw new SeleccionInvalida('Una opción aparece dos veces.');
    vistas.add(s.idOpcion);
  }

  switch (formato) {
    case 'single_choice':
      return evaluarSeleccionUnica(porId, seleccion);
    case 'ordering':
      return evaluarOrden(opciones, porId, seleccion);
    case 'matching':
      return evaluarEmparejamiento(porId, seleccion);
  }
}

function evaluarSeleccionUnica(
  porId: Map<number, OpcionDelItem>,
  seleccion: readonly OpcionElegida[],
): boolean {
  // RI-6: en selección única, exactamente una.
  if (seleccion.length !== 1)
    throw new SeleccionInvalida('En selección única se elige una sola opción.');
  if (seleccion[0].valorDado !== null) {
    throw new SeleccionInvalida(
      'En selección única la opción no lleva valor_dado.',
    );
  }
  return porId.get(seleccion[0].idOpcion)!.esCorrecta === true;
}

function evaluarOrden(
  opciones: readonly OpcionDelItem[],
  porId: Map<number, OpcionDelItem>,
  seleccion: readonly OpcionElegida[],
): boolean {
  // Ordenar es poner TODAS las opciones en posiciones 1..n, sin repetir.
  const n = opciones.length;
  if (seleccion.length !== n)
    throw new SeleccionInvalida('Ordena todas las opciones.');
  const posiciones = new Set<number>();
  for (const s of seleccion) {
    const p = s.valorDado;
    if (p === null || !Number.isInteger(p) || p < 1 || p > n) {
      throw new SeleccionInvalida(
        `Cada opción lleva una posición de 1 a ${n}.`,
      );
    }
    if (posiciones.has(p))
      throw new SeleccionInvalida(
        'Dos opciones no pueden ir en la misma posición.',
      );
    posiciones.add(p);
  }
  return seleccion.every((s) => porId.get(s.idOpcion)!.orden === s.valorDado);
}

function evaluarEmparejamiento(
  porId: Map<number, OpcionDelItem>,
  seleccion: readonly OpcionElegida[],
): boolean {
  // Emparejar: cada opción de la izquierda va en exactamente un par, y cada
  // par es una opción de cada lado. Una de la derecha puede quedar sin par
  // si el ítem tiene más a la derecha (RI-4 pide al menos 2 por lado, no
  // que sean iguales).
  const izquierdas = [...porId.values()].filter((o) => o.grupo === 'izquierda');
  const pares = new Map<number, OpcionDelItem[]>();
  for (const s of seleccion) {
    const p = s.valorDado;
    if (p === null || !Number.isInteger(p) || p < 1) {
      throw new SeleccionInvalida(
        'Cada opción emparejada lleva su número de pareja.',
      );
    }
    const lista = pares.get(p) ?? [];
    lista.push(porId.get(s.idOpcion)!);
    pares.set(p, lista);
  }
  for (const par of pares.values()) {
    const lados = par.map((o) => o.grupo).sort();
    if (
      par.length !== 2 ||
      lados[0] !== 'derecha' ||
      lados[1] !== 'izquierda'
    ) {
      throw new SeleccionInvalida('Cada pareja une una opción de cada lado.');
    }
  }
  const izquierdasElegidas = seleccion.filter(
    (s) => porId.get(s.idOpcion)!.grupo === 'izquierda',
  ).length;
  if (izquierdasElegidas !== izquierdas.length) {
    throw new SeleccionInvalida('Empareja todas las opciones de la izquierda.');
  }
  // Correcta solo si las dos opciones de CADA par son la misma pareja real.
  return [...pares.values()].every(
    ([a, b]) => a.orden !== null && a.orden === b.orden,
  );
}
