import type { Formato } from './entities/item.entity.js';
import type { Grupo } from './entities/opcion.entity.js';

/**
 * Un ítem como llega de la IA o del docente, antes de guardarse.
 * Los nombres son los de la tabla `opcion` (`18` §15).
 */
export interface OpcionPropuesta {
  texto: string;
  es_correcta?: boolean | null;
  orden?: number | null;
  grupo?: Grupo | null;
  hipotesis_error?: string | null;
}

export interface ItemPropuesto {
  enunciado: string;
  opciones: OpcionPropuesta[];
}

/** Mínimo de opciones por formato (RI-4, hallazgo H-9 del MER). */
export const MINIMO_OPCIONES: Record<Formato, number> = {
  single_choice: 2,
  ordering: 2,
  matching: 4,
};

/** En emparejamiento, al menos 2 opciones por grupo (H-9). */
export const MINIMO_POR_GRUPO = 2;

/** Tope de opciones de un ítem: ninguna regla lo pide; evita ítems absurdos. */
export const MAXIMO_OPCIONES = 20;

const vacio = (t: unknown): boolean => typeof t !== 'string' || t.trim() === '';

/** ¿Los números son exactamente 1, 2, …, n, sin huecos ni repetidos? */
function completos(numeros: (number | null | undefined)[]): boolean {
  if (numeros.some((n) => typeof n !== 'number' || !Number.isInteger(n)))
    return false;
  const ordenados = [...(numeros as number[])].sort((a, b) => a - b);
  return ordenados.every((n, i) => n === i + 1);
}

/**
 * Las reglas de un ítem según su formato: RI-4 con los mínimos de H-9, tal
 * como las escribe RF-03-05 y la ventana 009 (`12-spec` §2.4b, «Guardar»).
 * Es la única validación: la usan la generación del banco (CU-16), editar
 * (CU-18) y agregar (CU-20). Devuelve los problemas, en español; vacía si
 * el ítem es válido.
 */
export function validarItem(formato: Formato, item: ItemPropuesto): string[] {
  const errores: string[] = [];
  if (vacio(item?.enunciado))
    errores.push('El enunciado no puede estar vacío.');
  const opciones = Array.isArray(item?.opciones) ? item.opciones : [];
  if (!Array.isArray(item?.opciones)) errores.push('Faltan las opciones.');

  if (opciones.length < MINIMO_OPCIONES[formato]) {
    errores.push(
      `Este formato necesita al menos ${MINIMO_OPCIONES[formato]} opciones.`,
    );
  }
  if (opciones.length > MAXIMO_OPCIONES) {
    errores.push(`Un ítem no puede tener más de ${MAXIMO_OPCIONES} opciones.`);
  }
  if (opciones.some((o) => vacio(o?.texto)))
    errores.push('Ninguna opción puede estar vacía.');

  if (formato === 'single_choice') {
    const correctas = opciones.filter((o) => o?.es_correcta === true).length;
    if (correctas !== 1)
      errores.push(
        'En selección única debe haber exactamente una opción correcta.',
      );
    if (opciones.some((o) => o?.grupo))
      errores.push('En selección única las opciones no tienen grupo.');
  }

  if (formato === 'ordering') {
    if (!completos(opciones.map((o) => o?.orden))) {
      errores.push(
        'En ordenamiento los números de orden deben ir de 1 al total, sin repetirse.',
      );
    }
    if (opciones.some((o) => o?.grupo))
      errores.push('En ordenamiento las opciones no tienen grupo.');
    if (opciones.some((o) => o?.es_correcta === true)) {
      errores.push(
        'En ordenamiento ninguna opción se marca como correcta: lo correcto es el orden.',
      );
    }
  }

  if (formato === 'matching') {
    if (
      opciones.some((o) => o?.grupo !== 'izquierda' && o?.grupo !== 'derecha')
    ) {
      errores.push(
        'En emparejamiento cada opción es de la izquierda o de la derecha.',
      );
    }
    const izquierda = opciones.filter((o) => o?.grupo === 'izquierda');
    const derecha = opciones.filter((o) => o?.grupo === 'derecha');
    if (
      izquierda.length < MINIMO_POR_GRUPO ||
      derecha.length < MINIMO_POR_GRUPO
    ) {
      errores.push(
        `En emparejamiento cada lado necesita al menos ${MINIMO_POR_GRUPO} opciones.`,
      );
    }
    // El número de pareja va de 1 al total en cada lado, sin repetirse: así
    // cada término de la izquierda tiene exactamente un par a la derecha.
    if (
      izquierda.length !== derecha.length ||
      !completos(izquierda.map((o) => o.orden)) ||
      !completos(derecha.map((o) => o.orden))
    ) {
      errores.push(
        'En emparejamiento cada pareja tiene un número, de 1 al total, uno a cada lado y sin repetirse.',
      );
    }
    if (opciones.some((o) => o?.es_correcta === true)) {
      errores.push(
        'En emparejamiento ninguna opción se marca como correcta: lo correcto son las parejas.',
      );
    }
  }
  return errores;
}

/**
 * Deja las columnas de cada opción como las pide su formato (RI-4, `18`
 * §15): en selección única, `orden` es nulo y `es_correcta` es sí o no (las
 * opciones se guardan en el orden en que llegan, y en ese orden se
 * muestran); en los otros dos formatos, `es_correcta` es nulo. Supone un
 * ítem ya validado.
 */
export function normalizarOpciones(
  formato: Formato,
  opciones: OpcionPropuesta[],
): Required<OpcionPropuesta>[] {
  return opciones.map((o) => ({
    texto: o.texto.trim(),
    es_correcta: formato === 'single_choice' ? o.es_correcta === true : null,
    orden: formato === 'single_choice' ? null : (o.orden as number),
    grupo: formato === 'matching' ? (o.grupo as Grupo) : null,
    // La hipótesis de error es de una opción incorrecta (ADR-020): en
    // ordenamiento y emparejamiento ninguna opción es «la incorrecta»
    hipotesis_error:
      formato === 'single_choice' && o.es_correcta !== true
        ? o.hipotesis_error?.trim() || null
        : null,
  }));
}
