import { describe, expect, it } from 'vitest';
import { concluir, senal, type RespuestaEvaluada } from './regla-adaptativa.js';

// Una respuesta: (certeza, correcta).
const r = (certeza: number, correcta: boolean): RespuestaEvaluada => ({
  certeza,
  correcta,
});
const bien = (certeza: number) => r(certeza, true);
const mal = (certeza: number) => r(certeza, false);

/** Aplica la regla después de cada respuesta, como el servicio: ¿en cuál concluye? */
function primeraConclusion(
  respuestas: RespuestaEvaluada[],
): [number, string | null] {
  for (let i = 1; i <= respuestas.length; i++) {
    const e = concluir(respuestas.slice(0, i));
    if (e) return [i, e];
  }
  return [respuestas.length, null];
}

describe('ReglaAdaptativa (ADR-031, ADR-016)', () => {
  describe('ADR-031 p.1: certeza alta = 3, 4 o 5', () => {
    it('ADR-031 p.1: certeza 3 ya es alta; 2 no', () => {
      expect(senal(bien(3))).toBe('fuerte_muestra');
      expect(senal(bien(2))).toBe('debil');
    });
    it('ADR-031 p.1: 4 respuestas correctas con certeza 2 no concluyen (no son señales fuertes)', () => {
      expect(concluir([bien(2), bien(2), bien(2), bien(2)])).toBeNull();
    });
    it('ADR-031 p.1: 4 respuestas correctas con certeza 3 concluyen Muestra', () => {
      expect(concluir([bien(3), bien(3), bien(3), bien(3)])).toBe('muestra');
    });
  });

  describe('ADR-031 p.2: cada respuesta es una de tres señales', () => {
    it('ADR-031 p.2: correcta con certeza 3 a 5 = fuerte de "muestra"', () => {
      for (const c of [3, 4, 5]) expect(senal(bien(c))).toBe('fuerte_muestra');
    });
    it('ADR-031 p.2: incorrecta con certeza 3 a 5 = fuerte de "no muestra"', () => {
      for (const c of [3, 4, 5])
        expect(senal(mal(c))).toBe('fuerte_no_muestra');
    });
    it('ADR-031 p.2: certeza 0 a 2 = débil, correcta o no (ADR-008 p.2)', () => {
      for (const c of [0, 1, 2]) {
        expect(senal(bien(c))).toBe('debil');
        expect(senal(mal(c))).toBe('debil');
      }
    });
  });

  describe('ADR-031 p.4: cuándo se detiene', () => {
    it('ADR-031 p.4: con n < 4 nunca se detiene, aunque todo sea fuerte', () => {
      expect(concluir([])).toBeNull();
      expect(concluir([bien(5)])).toBeNull();
      expect(concluir([bien(5), bien(5)])).toBeNull();
      expect(concluir([bien(5), bien(5), bien(5)])).toBeNull();
      expect(concluir([mal(5), mal(5), mal(5)])).toBeNull();
    });
    it('ADR-031 p.4 (prueba de aceptación de CU-25): correctas con certeza 4, 5, 1 y 3 concluyen Muestra en la 4.ª', () => {
      expect(primeraConclusion([bien(4), bien(5), bien(1), bien(3)])).toEqual([
        4,
        'muestra',
      ]);
    });
    it('ADR-031 p.4: con n = 4, 3 fuertes de "no muestra" concluyen No muestra', () => {
      expect(concluir([mal(4), bien(1), mal(3), mal(5)])).toBe('no_muestra');
    });
    it('ADR-031 p.4: con n = 4, 2 fuertes no son más de la mitad (2·2 = 4): sigue', () => {
      expect(concluir([bien(5), bien(5), mal(5), mal(5)])).toBeNull();
      expect(concluir([bien(5), bien(5), bien(0), bien(0)])).toBeNull();
    });
    it('ADR-031 p.4: con n = 5 hacen falta 3 fuertes iguales', () => {
      expect(concluir([bien(5), bien(5), mal(5), mal(5), bien(4)])).toBe(
        'muestra',
      );
      expect(concluir([bien(5), bien(5), mal(5), mal(5), mal(4)])).toBe(
        'no_muestra',
      );
      expect(concluir([bien(5), bien(5), mal(5), mal(5), bien(2)])).toBeNull();
    });
    it('ADR-031 p.4: con n = 6 hacen falta 4 fuertes iguales (3 de 6 no es más de la mitad)', () => {
      expect(
        concluir([bien(5), bien(5), bien(5), mal(5), mal(5), mal(5)]),
      ).toBe('no_concluyente');
      expect(
        concluir([bien(5), bien(5), bien(5), mal(5), mal(5), bien(5)]),
      ).toBe('muestra');
      expect(concluir([mal(5), mal(5), mal(5), bien(5), bien(5), mal(3)])).toBe(
        'no_muestra',
      );
    });
    it('ADR-031 p.4 (prueba de aceptación de CU-25): seis respuestas con certeza 0 a 2 concluyen No concluyente', () => {
      const seis = [bien(0), mal(1), bien(2), mal(2), bien(1), mal(0)];
      expect(primeraConclusion(seis)).toEqual([6, 'no_concluyente']);
    });
    it('ADR-031 p.4: las respuestas débiles cuentan en n (el denominador), no en la mayoría', () => {
      // 3 fuertes de 6 no son mayoría, aunque las otras 3 sean débiles.
      expect(
        concluir([bien(5), bien(5), bien(5), bien(0), bien(0), bien(0)]),
      ).toBe('no_concluyente');
    });
    it('ADR-031 p.4: "muestra" y "no muestra" nunca pueden cumplirse a la vez (se prueban todas las combinaciones de n = 4 a 6)', () => {
      const tipos = [bien(5), mal(5), bien(0)];
      for (let n = 4; n <= 6; n++) {
        for (let k = 0; k < 3 ** n; k++) {
          const resp = Array.from(
            { length: n },
            (_, i) => tipos[Math.floor(k / 3 ** i) % 3],
          );
          const si = resp.filter((x) => senal(x) === 'fuerte_muestra').length;
          const no = resp.filter(
            (x) => senal(x) === 'fuerte_no_muestra',
          ).length;
          expect(si * 2 > n && no * 2 > n).toBe(false);
          // y la regla coincide con la definición escrita
          const esperado =
            si * 2 > n
              ? 'muestra'
              : no * 2 > n
                ? 'no_muestra'
                : n === 6
                  ? 'no_concluyente'
                  : null;
          expect(concluir(resp)).toBe(esperado);
        }
      }
    });
  });

  describe('ADR-016: mínimo 4, tope 6', () => {
    it('ADR-016: con 6 respuestas siempre concluye (nunca devuelve null)', () => {
      expect(
        concluir([bien(0), bien(0), bien(0), bien(0), bien(0), bien(0)]),
      ).not.toBeNull();
    });
    it('ADR-016: con 5 respuestas sin mayoría todavía no concluye (el tope es 6, no 5)', () => {
      expect(
        concluir([bien(0), bien(0), bien(0), bien(0), bien(0)]),
      ).toBeNull();
    });
    it('ADR-016: más de 6 respuestas es un error del llamador, no un resultado', () => {
      expect(() => concluir(Array.from({ length: 7 }, () => bien(0)))).toThrow(
        /tope/,
      );
    });
    it('ADR-028 p.3: una certeza fuera de 0 a 5 se rechaza', () => {
      expect(() => concluir([bien(6), bien(5), bien(5), bien(5)])).toThrow(
        /Certeza/,
      );
      expect(() => concluir([bien(-1), bien(5), bien(5), bien(5)])).toThrow(
        /Certeza/,
      );
    });
  });
});
