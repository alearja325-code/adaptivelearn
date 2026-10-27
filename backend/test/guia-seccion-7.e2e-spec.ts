import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { borrarCuentas, crearApp, type AppPruebas } from './app-pruebas.js';

// Las 6 pruebas de la sección 7 de la guía del docente v2, y su tabla de
// respuestas esperadas. Única diferencia: las contraseñas llevan mayúscula
// (Password123, Password456), por la regla de RF-01-01 (informe, D-04).
describe('Guía v2, sección 7', () => {
  let t: AppPruebas;
  let tokenUsuario: string;
  let tokenAdmin: string;

  beforeAll(async () => {
    t = await crearApp();
    await borrarCuentas(t.db);
  });
  afterAll(async () => t.app.close());

  it('1. registrar un nuevo usuario → 201 { user, token }', async () => {
    const res = await t.http
      .post('/auth/register')
      .send({ email: 'usuario@example.com', password: 'Password123', fullName: 'Juan Pérez' })
      .expect(201);
    expect(res.body.user).toEqual({
      id: 1,
      email: 'usuario@example.com',
      fullName: 'Juan Pérez',
      role: 'user',
    });
    expect(res.body.token).toMatch(/^eyJ/);
    expect(JSON.stringify(res.body)).not.toContain('password');
  });

  it('2. iniciar sesión → 200', async () => {
    const res = await t.http
      .post('/auth/login')
      .send({ email: 'usuario@example.com', password: 'Password123' })
      .expect(200);
    expect(res.body.user.role).toBe('user');
    tokenUsuario = res.body.token;
  });

  it('3. obtener perfil (ruta protegida) → 200 { user }', async () => {
    const res = await t.http.get('/auth/profile').set('Authorization', `Bearer ${tokenUsuario}`).expect(200);
    expect(res.body.user).toMatchObject({ id: 1, email: 'usuario@example.com', role: 'user' });
    expect(res.body.user).not.toHaveProperty('password');
  });

  it('4. convertir en administrador por SQL y volver a iniciar sesión', async () => {
    await t.db.query("UPDATE credencial SET es_admin = 1 WHERE correo = 'usuario@example.com'");
    const res = await t.http
      .post('/auth/login')
      .send({ email: 'usuario@example.com', password: 'Password123' })
      .expect(200);
    expect(res.body.user.role).toBe('admin');
    tokenAdmin = res.body.token;
  });

  it('5. crear usuario desde /users (requiere admin) → 201', async () => {
    const res = await t.http
      .post('/users')
      .set('Authorization', `Bearer ${tokenAdmin}`)
      .send({ email: 'otro@example.com', password: 'Password456', fullName: 'María García' })
      .expect(201);
    expect(res.body).toMatchObject({ id: 2, email: 'otro@example.com', fullName: 'María García', role: 'user' });
    expect(res.body).not.toHaveProperty('password');
  });

  it('6. listar todos los usuarios (requiere admin) → 200', async () => {
    const res = await t.http.get('/users').set('Authorization', `Bearer ${tokenAdmin}`).expect(200);
    expect(res.body.map((u: { email: string }) => u.email)).toEqual([
      'usuario@example.com',
      'otro@example.com',
    ]);
    expect(JSON.stringify(res.body)).not.toContain('password');
  });

  describe('tabla de respuestas esperadas', () => {
    it('sin token o token vencido → 401', async () => {
      await t.http.get('/users').expect(401);
      await t.http.get('/auth/profile').set('Authorization', 'Bearer x.y.z').expect(401);
    });

    it('token válido pero rol user en /users → 403', async () => {
      const login = await t.http
        .post('/auth/login')
        .send({ email: 'otro@example.com', password: 'Password456' })
        .expect(200);
      await t.http.get('/users').set('Authorization', `Bearer ${login.body.token}`).expect(403);
    });

    it('email ya registrado → 409', async () => {
      await t.http
        .post('/auth/register')
        .send({ email: 'otro@example.com', password: 'Password456', fullName: 'Otra' })
        .expect(409);
    });

    it('datos inválidos en el body → 400', async () => {
      await t.http.post('/auth/register').send({ email: 'no-es-correo', password: 'x' }).expect(400);
      await t.http.post('/auth/login').send({ email: 'otro@example.com' }).expect(400);
    });

    it('usuario con ese ID no existe (admin) → 404', async () => {
      await t.http.get('/users/999').set('Authorization', `Bearer ${tokenAdmin}`).expect(404);
    });

    it('borrar un usuario (admin) → 204', async () => {
      await t.http.delete('/users/2').set('Authorization', `Bearer ${tokenAdmin}`).expect(204);
      await t.http.get('/users/2').set('Authorization', `Bearer ${tokenAdmin}`).expect(404);
    });

    it('/example/protected con cualquier sesión, /example/admin solo admin', async () => {
      const otra = await t.http
        .post('/auth/register')
        .send({ email: 'tercera@example.com', password: 'Password789' })
        .expect(201);
      await t.http.get('/example/protected').set('Authorization', `Bearer ${otra.body.token}`).expect(200);
      await t.http.get('/example/admin').set('Authorization', `Bearer ${otra.body.token}`).expect(403);
      await t.http.get('/example/admin').set('Authorization', `Bearer ${tokenAdmin}`).expect(200);
    });

    it('el rol se lee de la base en cada petición, como en la guía: el token viejo ya es de admin', async () => {
      // JwtStrategy.validate() busca al usuario: la marca puesta por SQL vale
      // desde la petición siguiente, aunque el token se haya firmado antes
      await t.http.get('/example/admin').set('Authorization', `Bearer ${tokenUsuario}`).expect(200);
    });
  });
});
