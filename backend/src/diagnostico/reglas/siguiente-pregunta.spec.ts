import { describe, expect, it } from 'vitest';
import {
  BancoAgotado,
  barajarEstable,
  decidirSiguiente,
  type EvidenciaEnPlan,
} from './siguiente-pregunta.js';

const primero = () => 0;
const ev = (
  numeroEvidencia: number,
  itemsActivos: number[],
  concluida = false,
): EvidenciaEnPlan => ({
  numeroEvidencia,
  concluida,
  itemsActivos,
});

describe('Qué pregunta sigue (ADR-031 p.5 y p.6, ADR-024)', () => {
  it('ADR-031 p.6: si quedó una pregunta mostrada y sin responder, se repite esa', () => {
    const d = decidirSiguiente(
      { evidencias: [ev(1, [10, 11])], presentados: [10], pendiente: 10 },
      primero,
    );
    expect(d).toEqual({ tipo: 'repetir', idItem: 10 });
  });

  it('ADR-024: las evidencias van en el orden oficial (numero_evidencia), no en el orden en que llegan', () => {
    const d = decidirSiguiente(
      {
        evidencias: [ev(3, [30]), ev(1, [10]), ev(2, [20])],
        presentados: [],
        pendiente: null,
      },
      primero,
    );
    expect(d).toEqual({ tipo: 'presentar', idItem: 10, numeroEvidencia: 1 });
  });

  it('ADR-031 p.5: no se pasa a la siguiente evidencia sin concluir la actual', () => {
    const evidencias = [ev(1, [10, 11, 12, 13, 14, 15]), ev(2, [20, 21])];
    const d = decidirSiguiente(
      { evidencias, presentados: [10, 11, 12, 13], pendiente: null },
      primero,
    );
    expect(d).toMatchObject({
      tipo: 'presentar',
      numeroEvidencia: 1,
      idItem: 14,
    });
  });

  it('ADR-031 p.5: concluida la primera, sigue la segunda', () => {
    const evidencias = [ev(1, [10, 11, 12, 13], true), ev(2, [20, 21])];
    const d = decidirSiguiente(
      { evidencias, presentados: [10, 11, 12, 13], pendiente: null },
      primero,
    );
    expect(d).toMatchObject({ tipo: 'presentar', numeroEvidencia: 2 });
  });

  it('ADR-031 p.5: al azar, solo entre los activos que todavía no vio', () => {
    const elegidos = new Set<number>();
    for (let k = 0; k < 3; k++) {
      const d = decidirSiguiente(
        {
          evidencias: [ev(1, [10, 11, 12, 13])],
          presentados: [11],
          pendiente: null,
        },
        () => k,
      );
      if (d.tipo === 'presentar') elegidos.add(d.idItem);
    }
    expect([...elegidos].sort()).toEqual([10, 12, 13]);
  });

  it('ADR-015: un ítem excluido no se presenta (no está entre los activos)', () => {
    // El servicio solo pasa los activos; aquí el 11 no está.
    const d = decidirSiguiente(
      { evidencias: [ev(1, [10, 12])], presentados: [10], pendiente: null },
      primero,
    );
    expect(d).toMatchObject({ idItem: 12 });
  });

  it('CU-23 p.7: con todas las evidencias concluidas, no hay pregunta', () => {
    const d = decidirSiguiente(
      {
        evidencias: [ev(1, [10], true), ev(2, [20], true)],
        presentados: [10, 20],
        pendiente: null,
      },
      primero,
    );
    expect(d).toEqual({ tipo: 'completada' });
  });

  it('RI-9: nunca más de 6 presentaciones en una evidencia; ni más que sus ítems activos', () => {
    const seis = [10, 11, 12, 13, 14, 15];
    expect(() =>
      decidirSiguiente(
        {
          evidencias: [ev(1, [...seis, 16])],
          presentados: seis,
          pendiente: null,
        },
        primero,
      ),
    ).toThrow(BancoAgotado);
    expect(() =>
      decidirSiguiente(
        { evidencias: [ev(1, [10])], presentados: [10], pendiente: null },
        primero,
      ),
    ).toThrow(BancoAgotado);
  });

  it('el barajado es estable para una misma presentación y no deja el orden guardado', () => {
    const lista = [1, 2, 3, 4, 5, 6];
    expect(barajarEstable(lista, 42)).toEqual(barajarEstable(lista, 42));
    expect(barajarEstable(lista, 42).sort()).toEqual(lista);
    // Entre muchas semillas, alguna cambia el orden (no es la identidad).
    expect(
      [1, 2, 3, 4, 5].some(
        (s) => barajarEstable(lista, s).join() !== lista.join(),
      ),
    ).toBe(true);
  });
});
