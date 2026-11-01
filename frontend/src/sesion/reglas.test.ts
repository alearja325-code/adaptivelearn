import { describe, expect, it } from 'vitest';
import { usuario } from '../pruebas/utilidades';
import { destinoDe, esCorreo, nombreSugerido, partirNombre, REGLA_CONTRASENA, varianteDe } from './reglas';

describe('el camino de una cuenta (encargo 04 §5, ADR-035)', () => {
  it('sin verificar → 015; verificada sin rol → 016; con rol → 001', () => {
    expect(destinoDe(usuario({ estadoVerificacion: 'procesando', perfil: null }))).toBe('/verificar-correo');
    expect(destinoDe(usuario({ perfil: null, role: 'user', idDocente: null }))).toBe('/completar-perfil');
    expect(destinoDe(usuario())).toBe('/');
  });
  it('la variante del Dashboard sale de la fila de docente o estudiante', () => {
    expect(varianteDe(usuario())).toBe('docente');
    expect(varianteDe(usuario({ idDocente: null, idEstudiante: 3, role: 'estudiante' }))).toBe('estudiante');
  });
});

describe('validaciones de los formularios', () => {
  it('contraseña: 8 caracteres, una mayúscula, una minúscula y un número (RF-01-01)', () => {
    expect(REGLA_CONTRASENA.test('Password123')).toBe(true);
    expect(REGLA_CONTRASENA.test('password123')).toBe(false);
    expect(REGLA_CONTRASENA.test('Password')).toBe(false);
    expect(REGLA_CONTRASENA.test('Pass12')).toBe(false);
    expect(REGLA_CONTRASENA.test('PASSWORD123')).toBe(false);
  });
  it('correo: solo el formato (018 §7)', () => {
    expect(esCorreo('ana@colegio.co')).toBe(true);
    expect(esCorreo('ana@colegio')).toBe(false);
    expect(esCorreo('ana colegio.co')).toBe(false);
  });
});

describe('prellenados', () => {
  it('nombres y apellidos desde un nombre completo', () => {
    expect(partirNombre('Ana María Pérez Gómez')).toEqual({ nombres: 'Ana María', apellidos: 'Pérez Gómez' });
    expect(partirNombre('Luis Pérez Gómez')).toEqual({ nombres: 'Luis', apellidos: 'Pérez Gómez' });
    expect(partirNombre('Juan Pérez')).toEqual({ nombres: 'Juan', apellidos: 'Pérez' });
    expect(partirNombre(null)).toEqual({ nombres: '', apellidos: '' });
  });
  it('el nombre de la experiencia: el enunciado, hasta 160 caracteres (004 §2.3)', () => {
    expect(nombreSugerido('Reconoce los números.')).toBe('Reconoce los números.');
    const largo = 'palabra '.repeat(40);
    const s = nombreSugerido(largo);
    expect(s.length).toBeLessThanOrEqual(160);
    expect(s.endsWith('…')).toBe(true);
  });
});
