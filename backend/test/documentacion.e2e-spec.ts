import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { crearApp, type AppPruebas } from './app-pruebas.js';

// Swagger (20-catalogo-endpoints.md §8): el docente prueba la API desde el
// navegador en /docs, y /docs-json tiene la especificación OpenAPI.
describe('Documentación interactiva (/docs)', () => {
  let t: AppPruebas;
  beforeAll(async () => {
    t = await crearApp();
  });
  afterAll(async () => t.app.close());

  it('/docs responde con la página de Swagger', async () => {
    const r = await t.http.get('/docs/').expect(200);
    expect(r.text).toContain('swagger');
  });

  it('/docs-json trae las rutas de los cuatro incrementos y el token Bearer', async () => {
    const r = await t.http.get('/docs-json').expect(200);
    const rutas = Object.keys(r.body.paths);
    for (const ruta of [
      '/auth/login', // I1
      '/catalogo/dbas/{codigo}', // I2
      '/experiencias', // I2
      '/experiencias/generaciones/{id}', // I2, E-38
      '/inscripciones/{id}/respuestas', // I3
      '/experiencias/{id}/reporte', // I4
    ]) {
      expect(rutas).toContain(ruta);
    }
    expect(r.body.components.securitySchemes.bearer.scheme).toBe('bearer');
  });
});
