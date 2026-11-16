import { describe, expect, it } from 'vitest';
import {
  evaluarSeleccion,
  SeleccionInvalida,
  type OpcionDelItem,
} from './evaluar-seleccion.js';

const op = (
  idOpcion: number,
  o: Partial<OpcionDelItem> = {},
): OpcionDelItem => ({
  idOpcion,
  esCorrecta: null,
  orden: null,
  grupo: null,
  ...o,
});
const elige = (idOpcion: number, valorDado: number | null = null) => ({
  idOpcion,
  valorDado,
});

// Selección única: la 2 es la correcta.
const unica = [
  op(1, { esCorrecta: false }),
  op(2, { esCorrecta: true }),
  op(3, { esCorrecta: false }),
];
// Ordenar: 11 va primero, 12 segundo, 13 tercero, 14 cuarto.
const orden = [
  op(11, { orden: 1 }),
  op(12, { orden: 2 }),
  op(13, { orden: 3 }),
  op(14, { orden: 4 }),
];
// Emparejar: (21,22) pareja 1, (23,24) pareja 2; 25 es una derecha sin pareja.
const pares = [
  op(21, { grupo: 'izquierda', orden: 1 }),
  op(22, { grupo: 'derecha', orden: 1 }),
  op(23, { grupo: 'izquierda', orden: 2 }),
  op(24, { grupo: 'derecha', orden: 2 }),
  op(25, { grupo: 'derecha', orden: null }),
];

describe('Item.evaluar (ADR-031 p.3, RI-6)', () => {
  describe('ADR-031 p.3: selección única', () => {
    it('ADR-031 p.3: correcta si eligió la opción correcta', () => {
      expect(evaluarSeleccion('single_choice', unica, [elige(2)])).toBe(true);
      expect(evaluarSeleccion('single_choice', unica, [elige(1)])).toBe(false);
    });
    it('RI-6: exactamente una opción en selección única', () => {
      expect(() =>
        evaluarSeleccion('single_choice', unica, [elige(1), elige(2)]),
      ).toThrow(SeleccionInvalida);
      expect(() => evaluarSeleccion('single_choice', unica, [])).toThrow(
        SeleccionInvalida,
      );
    });
    it('RI-6: una opción de otro ítem se rechaza', () => {
      expect(() =>
        evaluarSeleccion('single_choice', unica, [elige(99)]),
      ).toThrow(SeleccionInvalida);
    });
    it('ADR-019: en selección única la fila no lleva valor_dado', () => {
      expect(() =>
        evaluarSeleccion('single_choice', unica, [elige(2, 1)]),
      ).toThrow(SeleccionInvalida);
    });
  });

  describe('ADR-031 p.3: ordenar, todo o nada', () => {
    it('ADR-031 p.3: correcta solo si todas las posiciones están bien', () => {
      expect(
        evaluarSeleccion('ordering', orden, [
          elige(11, 1),
          elige(12, 2),
          elige(13, 3),
          elige(14, 4),
        ]),
      ).toBe(true);
    });
    it('ADR-031 p.3 (prueba de aceptación de CU-24): con dos posiciones cambiadas es incorrecta', () => {
      expect(
        evaluarSeleccion('ordering', orden, [
          elige(11, 1),
          elige(12, 2),
          elige(13, 4),
          elige(14, 3),
        ]),
      ).toBe(false);
    });
    it('ordenar exige todas las opciones, en posiciones 1..n sin repetir', () => {
      expect(() =>
        evaluarSeleccion('ordering', orden, [
          elige(11, 1),
          elige(12, 2),
          elige(13, 3),
        ]),
      ).toThrow(SeleccionInvalida);
      expect(() =>
        evaluarSeleccion('ordering', orden, [
          elige(11, 1),
          elige(12, 1),
          elige(13, 3),
          elige(14, 4),
        ]),
      ).toThrow(SeleccionInvalida);
      expect(() =>
        evaluarSeleccion('ordering', orden, [
          elige(11, 1),
          elige(12, 2),
          elige(13, 3),
          elige(14, 5),
        ]),
      ).toThrow(SeleccionInvalida);
      expect(() =>
        evaluarSeleccion('ordering', orden, [
          elige(11),
          elige(12, 2),
          elige(13, 3),
          elige(14, 4),
        ]),
      ).toThrow(SeleccionInvalida);
    });
  });

  describe('ADR-031 p.3: emparejar, todo o nada', () => {
    it('ADR-031 p.3: correcta si todos los pares están bien (el número de pareja lo pone el estudiante)', () => {
      expect(
        evaluarSeleccion('matching', pares, [
          elige(21, 1),
          elige(22, 1),
          elige(23, 2),
          elige(24, 2),
        ]),
      ).toBe(true);
      // Los números de pareja del estudiante no tienen que coincidir con los guardados.
      expect(
        evaluarSeleccion('matching', pares, [
          elige(21, 7),
          elige(22, 7),
          elige(23, 3),
          elige(24, 3),
        ]),
      ).toBe(true);
    });
    it('ADR-031 p.3: un par equivocado hace incorrecta toda la respuesta', () => {
      expect(
        evaluarSeleccion('matching', pares, [
          elige(21, 1),
          elige(22, 1),
          elige(23, 2),
          elige(25, 2),
        ]),
      ).toBe(false);
      expect(
        evaluarSeleccion('matching', pares, [
          elige(21, 1),
          elige(24, 1),
          elige(23, 2),
          elige(22, 2),
        ]),
      ).toBe(false);
    });
    it('emparejar exige cada izquierda en un par, y cada par con una opción de cada lado', () => {
      expect(() =>
        evaluarSeleccion('matching', pares, [elige(21, 1), elige(22, 1)]),
      ).toThrow(SeleccionInvalida);
      expect(() =>
        evaluarSeleccion('matching', pares, [
          elige(21, 1),
          elige(23, 1),
          elige(22, 2),
          elige(24, 2),
        ]),
      ).toThrow(SeleccionInvalida);
      expect(() =>
        evaluarSeleccion('matching', pares, [
          elige(21, 1),
          elige(22, 1),
          elige(24, 1),
          elige(23, 2),
        ]),
      ).toThrow(SeleccionInvalida);
      expect(() =>
        evaluarSeleccion('matching', pares, [
          elige(21),
          elige(22),
          elige(23, 2),
          elige(24, 2),
        ]),
      ).toThrow(SeleccionInvalida);
    });
  });

  it('RI-6: la misma opción dos veces se rechaza', () => {
    expect(() =>
      evaluarSeleccion('ordering', orden, [
        elige(11, 1),
        elige(11, 2),
        elige(13, 3),
        elige(14, 4),
      ]),
    ).toThrow(SeleccionInvalida);
  });
});
