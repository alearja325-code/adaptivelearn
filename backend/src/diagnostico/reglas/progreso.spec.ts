import { describe, expect, it } from 'vitest';
import { progreso } from './progreso.js';

describe('progreso de una inscripción (CU-21, 23-spec §2.1)', () => {
  it('sin presentaciones: No iniciada (Estado A)', () => {
    expect(progreso(0, 0, 3)).toBe('no_iniciada');
  });
  it('CU-21 (prueba de aceptación): con una pregunta mostrada ya está En curso (Estado B)', () => {
    expect(progreso(1, 0, 3)).toBe('en_curso');
    expect(progreso(9, 2, 3)).toBe('en_curso');
  });
  it('todas las evidencias con resultado: Completada (Estado C)', () => {
    expect(progreso(14, 3, 3)).toBe('completada');
  });
});
