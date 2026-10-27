import { describe, expect, it } from 'vitest';
import { ForbiddenException, UnauthorizedException, type ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { RolesGuard } from './roles.guard.js';

function contexto(user: unknown): ExecutionContext {
  return {
    getHandler: () => () => undefined,
    getClass: () => class {},
    switchToHttp: () => ({ getRequest: () => ({ user }) }),
  } as unknown as ExecutionContext;
}

function guard(roles: string[] | undefined): RolesGuard {
  const reflector = { getAllAndOverride: () => roles } as unknown as Reflector;
  return new RolesGuard(reflector);
}

// Guía v2, sección 6: sin usuario 401, rol no permitido 403
describe('RolesGuard', () => {
  it('deja pasar si la ruta no exige roles', () => {
    expect(guard(undefined).canActivate(contexto(undefined))).toBe(true);
    expect(guard([]).canActivate(contexto(undefined))).toBe(true);
  });
  it('sin usuario responde 401', () => {
    expect(() => guard(['admin']).canActivate(contexto(undefined))).toThrow(UnauthorizedException);
  });
  it('con un rol que no está en la lista responde 403', () => {
    expect(() => guard(['admin']).canActivate(contexto({ role: 'user' }))).toThrow(ForbiddenException);
    expect(() => guard(['docente']).canActivate(contexto({ role: 'estudiante' }))).toThrow(ForbiddenException);
  });
  it('con el rol pedido deja pasar', () => {
    expect(guard(['docente']).canActivate(contexto({ role: 'docente' }))).toBe(true);
  });
});
