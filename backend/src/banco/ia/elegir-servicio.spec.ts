import type { ConfigService } from '@nestjs/config';
import { describe, expect, it } from 'vitest';
import { DeepSeekServicio } from './deepseek.servicio.js';
import { elegirServicioIa, tiempoLimite } from './elegir-servicio.js';
import { IaFalsa } from './ia-falsa.js';

const config = (vars: Record<string, string>) =>
  ({ get: (k: string) => vars[k] }) as unknown as ConfigService;

describe('elegirServicioIa (IA_SERVICIO, ADR-045 punto 5)', () => {
  it('por defecto, DeepSeek con su modelo por defecto', () => {
    const ia = elegirServicioIa(config({}));
    expect(ia).toBeInstanceOf(DeepSeekServicio);
    expect(ia.modelo).toBe('deepseek-chat');
  });
  it('DEEPSEEK_MODEL cambia el modelo que se guarda en la experiencia', () => {
    expect(
      elegirServicioIa(
        config({ IA_SERVICIO: 'deepseek', DEEPSEEK_MODEL: 'otro' }),
      ).modelo,
    ).toBe('otro');
  });
  it('falsa → la IA de las pruebas', () => {
    expect(elegirServicioIa(config({ IA_SERVICIO: 'falsa' }))).toBeInstanceOf(
      IaFalsa,
    );
  });
  it('otro valor no arranca, y el error no lleva la clave', () => {
    expect(() =>
      elegirServicioIa(
        config({ IA_SERVICIO: 'gemini', DEEPSEEK_API_KEY: 'sk-x' }),
      ),
    ).toThrow(/deepseek o falsa/);
    try {
      elegirServicioIa(
        config({ IA_SERVICIO: 'gemini', DEEPSEEK_API_KEY: 'sk-x' }),
      );
    } catch (e) {
      expect(String(e)).not.toContain('sk-x');
    }
  });
});

describe('tiempoLimite (IA_TIEMPO_LIMITE_MS)', () => {
  it('120000 por defecto; el valor si es un entero positivo; si no, error', () => {
    expect(tiempoLimite(config({}))).toBe(120_000);
    expect(tiempoLimite(config({ IA_TIEMPO_LIMITE_MS: '90000' }))).toBe(90_000);
    expect(() =>
      tiempoLimite(config({ IA_TIEMPO_LIMITE_MS: 'dos minutos' })),
    ).toThrow();
    expect(() => tiempoLimite(config({ IA_TIEMPO_LIMITE_MS: '0' }))).toThrow();
  });
});
