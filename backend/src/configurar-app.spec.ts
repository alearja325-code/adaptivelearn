import { describe, expect, it } from 'vitest';
import { origenesPermitidos } from './configurar-app.js';

describe('origenesPermitidos (CORS)', () => {
  it('sin CORS_ORIGIN, solo el frontend de desarrollo', () => {
    expect(origenesPermitidos(undefined)).toEqual(['http://localhost:5173']);
    expect(origenesPermitidos('  ')).toEqual(['http://localhost:5173']);
  });
  it('varias direcciones separadas por comas, sin la barra final', () => {
    expect(origenesPermitidos('https://a.co/, http://localhost:5174')).toEqual(['https://a.co', 'http://localhost:5174']);
  });
});
