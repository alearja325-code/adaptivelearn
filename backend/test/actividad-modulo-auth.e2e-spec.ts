import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { borrarCuentas, crearApp, type AppPruebas } from './app-pruebas.js';

// Lo que la actividad "Módulo de autenticación" (DSE-2) pide además de la
// guía: contraseña con minúscula (punto 3), validateUser() (punto 4) y CORS
// configurado para el frontend (punto 8).
describe('Actividad: módulo de autenticación', () => {
  let t: AppPruebas;

  beforeAll(async () => {
    t = await crearApp();
    await borrarCuentas(t.db);
  });
  afterAll(async () => t.app.close());

  it('punto 3: una contraseña sin minúscula se rechaza (400)', async () => {
    const res = await t.http
      .post('/auth/register')
      .send({ email: 'sin.minuscula@example.com', password: 'PASSWORD123' })
      .expect(400);
    expect(JSON.stringify(res.body)).toContain('una minúscula');
  });

  it('punto 4: validateUser() devuelve la cuenta solo con la contraseña correcta', async () => {
    await t.http
      .post('/auth/register')
      .send({ email: 'validar@example.com', password: 'Password123' })
      .expect(201);
    const auth = t.app.get((await import('../src/auth/auth.service.js')).AuthService);
    const user = await auth.validateUser('validar@example.com', 'Password123');
    expect(user.email).toBe('validar@example.com');
    await expect(auth.validateUser('validar@example.com', 'Otra12345')).rejects.toThrow('Credenciales inválidas');
    await expect(auth.validateUser('nadie@example.com', 'Password123')).rejects.toThrow('Credenciales inválidas');
  });

  it('punto 8: CORS responde solo a la dirección del frontend', async () => {
    const permitido = await t.http.get('/auth/profile').set('Origin', 'http://localhost:5173');
    expect(permitido.headers['access-control-allow-origin']).toBe('http://localhost:5173');
    const otro = await t.http.get('/auth/profile').set('Origin', 'https://sitio-ajeno.example');
    expect(otro.headers['access-control-allow-origin']).toBeUndefined();
  });
});
