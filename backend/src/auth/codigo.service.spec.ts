import { describe, expect, it } from 'vitest';
import type { ConfigService } from '@nestjs/config';
import type { Repository } from 'typeorm';
import {
  CodigoService,
  MAX_INTENTOS_CODIGO,
  codigoVencido,
  puedeReenviar,
} from './codigo.service.js';
import type { CodigoVerificacion } from './entities/codigo-verificacion.entity.js';

const T0 = new Date('2026-10-27T10:00:00Z');
const mas = (segundos: number) => new Date(T0.getTime() + segundos * 1000);

// ADR-039: vencimiento y espera se calculan desde creado_en
describe('Tiempos del código (RF-01-03, ADR-039)', () => {
  it('vence a los 10 minutos, no antes', () => {
    expect(codigoVencido(T0, mas(10 * 60))).toBe(false);
    expect(codigoVencido(T0, mas(10 * 60 + 1))).toBe(true);
  });
  it('se puede reenviar a los 30 segundos, no antes', () => {
    expect(puedeReenviar(T0, mas(29))).toBe(false);
    expect(puedeReenviar(T0, mas(30))).toBe(true);
  });
  it('el máximo de intentos es 5, como el CHECK del modelo relacional', () => {
    expect(MAX_INTENTOS_CODIGO).toBe(5);
  });
});

describe('CodigoService.hash', () => {
  const config = { getOrThrow: () => 'secreto-de-prueba' } as unknown as ConfigService;
  const servicio = new CodigoService({} as Repository<CodigoVerificacion>, config);

  it('es hexadecimal de 64 caracteres y no contiene el código', () => {
    const h = servicio.hash(1, 'verificar_correo', '123456');
    expect(h).toMatch(/^[0-9a-f]{64}$/);
    expect(h).not.toContain('123456');
  });
  it('el mismo código de otra credencial o de otro propósito da otro hash', () => {
    const h = servicio.hash(1, 'verificar_correo', '123456');
    expect(servicio.hash(2, 'verificar_correo', '123456')).not.toBe(h);
    expect(servicio.hash(1, 'recuperar_contrasena', '123456')).not.toBe(h);
    expect(servicio.hash(1, 'verificar_correo', '123456')).toBe(h);
  });
});
