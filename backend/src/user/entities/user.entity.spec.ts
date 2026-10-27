import { describe, expect, it } from 'vitest';
import { instanceToPlain } from 'class-transformer';
import { User } from './user.entity.js';
import { Docente } from './docente.entity.js';

function credencial(datos: Partial<User>): User {
  return Object.assign(new User(), {
    id: 1,
    email: 'ana@colegio.co',
    password: '$2b$10$hash',
    nombreCompleto: null,
    proveedor: 'correo',
    proveedorId: null,
    estadoVerificacion: 'procesando',
    esAdmin: false,
    intentosLogin: 2,
    bloqueadoHasta: null,
    idDocente: null,
    idEstudiante: null,
    ...datos,
  });
}

describe('User (credencial)', () => {
  describe('role: se deduce, no se guarda (ADR-040)', () => {
    it("sin docente ni estudiante es 'user': registro a medias (ADR-035)", () => {
      expect(credencial({}).role).toBe('user');
      expect(credencial({}).tieneRol()).toBe(false);
    });
    it('con id_docente es docente; con id_estudiante, estudiante', () => {
      expect(credencial({ idDocente: 3 }).role).toBe('docente');
      expect(credencial({ idEstudiante: 4 }).role).toBe('estudiante');
      expect(credencial({ idEstudiante: 4 }).tieneRol()).toBe(true);
    });
    it('la marca de administrador va primero', () => {
      expect(credencial({ esAdmin: true }).role).toBe('admin');
      expect(credencial({ esAdmin: true, idDocente: 3 }).role).toBe('admin');
    });
  });

  describe('fullName', () => {
    it('sin perfil, el nombre escrito al registrarse (o null)', () => {
      expect(credencial({}).fullName).toBeNull();
      expect(credencial({ nombreCompleto: 'Juan Pérez' }).fullName).toBe('Juan Pérez');
    });
    it('con perfil, nombres y apellidos de docente o estudiante', () => {
      const docente = Object.assign(new Docente(), {
        id: 3,
        nombres: 'Ana María',
        apellidos: 'Pérez',
        avatarUrl: null,
      });
      const user = credencial({ idDocente: 3, docente, nombreCompleto: 'otro' });
      expect(user.fullName).toBe('Ana María Pérez');
      expect(user.perfil).toEqual({ nombres: 'Ana María', apellidos: 'Pérez', avatarUrl: null });
    });
  });

  describe('serialización (guía, sección 5: @Exclude)', () => {
    const json = instanceToPlain(credencial({ nombreCompleto: 'Juan' }));

    it('nunca envía la contraseña ni los datos de seguridad', () => {
      for (const campo of ['password', 'intentosLogin', 'bloqueadoHasta', 'proveedorId', 'esAdmin']) {
        expect(json).not.toHaveProperty(campo);
      }
    });
    it('envía el rol, el nombre, el estado y los ids de rol (nota R2)', () => {
      expect(json).toMatchObject({
        id: 1,
        email: 'ana@colegio.co',
        role: 'user',
        fullName: 'Juan',
        estadoVerificacion: 'procesando',
        idDocente: null,
        idEstudiante: null,
        perfil: null,
      });
    });
  });
});
