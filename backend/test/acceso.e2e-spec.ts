import { afterAll, beforeAll, beforeEach, describe, expect, it } from 'vitest';
import {
  CLAVE,
  borrarCuentas,
  crearApp,
  crearCuenta,
  envejecerCodigo,
  tokenConFormaDeJwt,
  type AppPruebas,
} from './app-pruebas.js';

// El acceso de AdaptiveLearn (`20` §3, E-01 a E-12) contra MySQL real.
// Cada bloque empieza sin cuentas.
describe('Acceso', () => {
  let t: AppPruebas;
  const bearer = (token: string) => ({ Authorization: `Bearer ${token}` });

  beforeAll(async () => {
    t = await crearApp();
  });
  beforeEach(async () => {
    await borrarCuentas(t.db);
    t.correo.enviados = [];
  });
  afterAll(async () => t.app.close());

  describe('registro → verificar → completar perfil → elegir rol (CU-01, 03, 04, 05)', () => {
    it('recorre el flujo completo, con foto, y la sesión lleva el rol y el id (R2)', async () => {
      const reg = await t.http
        .post('/auth/register')
        .send({ email: 'ana@colegio.co', password: CLAVE, fullName: 'Ana Pérez' })
        .expect(201);
      expect(reg.body.user.role).toBe('user');

      // El código no se guarda legible: solo su HMAC (ADR-039)
      const codigo = t.correo.ultimo('ana@colegio.co');
      const [fila] = await t.db.query('SELECT codigo_hash, intentos FROM codigo_verificacion');
      expect(fila.codigo_hash).toMatch(/^[0-9a-f]{64}$/);
      expect(fila.codigo_hash).not.toContain(codigo);

      // Antes de verificar, no se puede elegir rol
      await t.http
        .post('/auth/elegir-rol')
        .set(bearer(reg.body.token))
        .send({ role: 'docente', nombres: 'Ana', apellidos: 'Pérez' })
        .expect(403);

      const ver = await t.http
        .post('/auth/verificar-correo')
        .set(bearer(reg.body.token))
        .send({ codigo })
        .expect(200);
      expect(ver.body.user.estadoVerificacion).toBe('verificado');
      // El código usado se borra
      expect(await t.db.query('SELECT * FROM codigo_verificacion')).toHaveLength(0);

      // Nombres vacíos → 400
      await t.http
        .post('/auth/elegir-rol')
        .set(bearer(reg.body.token))
        .field('role', 'docente')
        .field('nombres', '   ')
        .field('apellidos', 'Pérez')
        .expect(400);

      // Una foto que no es JPG ni PNG → 400 y no se crea nada
      await t.http
        .post('/auth/elegir-rol')
        .set(bearer(reg.body.token))
        .field('role', 'docente')
        .field('nombres', 'Ana')
        .field('apellidos', 'Pérez')
        .attach('foto', Buffer.from('GIF89a no soy una foto'), 'foto.png')
        .expect(400);
      expect(await t.db.query('SELECT * FROM docente')).toHaveLength(0);

      const png = Buffer.from(
        'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
        'base64',
      );
      const rol = await t.http
        .post('/auth/elegir-rol')
        .set(bearer(reg.body.token))
        .field('role', 'docente')
        .field('nombres', 'Ana María')
        .field('apellidos', 'Pérez')
        .attach('foto', png, 'yo.png')
        .expect(201);
      expect(rol.body.user).toMatchObject({ role: 'docente', fullName: 'Ana María Pérez' });

      const sesion = JSON.parse(Buffer.from(rol.body.token.split('.')[1], 'base64url').toString());
      expect(sesion).toMatchObject({ role: 'docente', idEstudiante: null });
      expect(sesion.idDocente).toBeGreaterThan(0);

      const perfil = await t.http.get('/auth/profile').set(bearer(rol.body.token)).expect(200);
      expect(perfil.body.user.perfil.avatarUrl).toMatch(/^\/uploads\/.+\.png$/);
      const foto = await t.http.get(perfil.body.user.perfil.avatarUrl).expect(200);
      expect(foto.headers['content-type']).toBe('image/png');

      // El rol no se cambia (RF-01-06)
      await t.http
        .post('/auth/elegir-rol')
        .set(bearer(rol.body.token))
        .send({ role: 'estudiante', nombres: 'Ana', apellidos: 'Pérez' })
        .expect(409);
    });

    it('registro a medias: al iniciar sesión sin rol, retoma (ADR-035)', async () => {
      await t.http.post('/auth/register').send({ email: 'luis@x.co', password: CLAVE }).expect(201);
      const login = await t.http.post('/auth/login').send({ email: 'luis@x.co', password: CLAVE }).expect(200);
      expect(login.body.user.role).toBe('user');
      const perfil = await t.http.get('/auth/profile').set(bearer(login.body.token)).expect(200);
      expect(perfil.body.user).toMatchObject({ estadoVerificacion: 'procesando', perfil: null });
    });

    it('correo ya registrado → 409 con el método que se debe usar (RF-01-04)', async () => {
      await t.http.post('/auth/register').send({ email: 'ana@colegio.co', password: CLAVE }).expect(201);
      const res = await t.http
        .post('/auth/register')
        .send({ email: 'ANA@colegio.co', password: CLAVE })
        .expect(409);
      expect(res.body.message).toContain('ya está registrado');
    });
  });

  describe('códigos (ADR-039, nota R4)', () => {
    let token: string;
    beforeEach(async () => {
      const reg = await t.http.post('/auth/register').send({ email: 'ana@colegio.co', password: CLAVE });
      token = reg.body.token;
    });

    it('un código vencido (más de 10 minutos desde creado_en) no sirve', async () => {
      const codigo = t.correo.ultimo('ana@colegio.co');
      await envejecerCodigo(t.db, 'ana@colegio.co', 10 * 60 + 1);
      const res = await t.http.post('/auth/verificar-correo').set(bearer(token)).send({ codigo }).expect(400);
      expect(res.body.message).toContain('venció');
    });

    it('reenviar antes de 30 s no envía otro código; después, sí, y el viejo deja de servir', async () => {
      await t.http.post('/auth/reenviar-codigo').send({ email: 'ana@colegio.co' }).expect(201, { ok: true });
      expect(t.correo.cuantos('ana@colegio.co')).toBe(1);

      const viejo = t.correo.ultimo('ana@colegio.co');
      await envejecerCodigo(t.db, 'ana@colegio.co', 31);
      await t.http.post('/auth/reenviar-codigo').send({ email: 'ana@colegio.co' }).expect(201, { ok: true });
      expect(t.correo.cuantos('ana@colegio.co')).toBe(2);
      const nuevo = t.correo.ultimo('ana@colegio.co');

      // Sigue habiendo un solo código por credencial y propósito
      expect(await t.db.query('SELECT * FROM codigo_verificacion')).toHaveLength(1);
      if (viejo !== nuevo) {
        await t.http.post('/auth/verificar-correo').set(bearer(token)).send({ codigo: viejo }).expect(400);
      }
      await t.http.post('/auth/verificar-correo').set(bearer(token)).send({ codigo: nuevo }).expect(200);
    });

    it('reenviar a un correo que no existe responde igual (RNF-07)', async () => {
      await t.http.post('/auth/reenviar-codigo').send({ email: 'nadie@x.co' }).expect(201, { ok: true });
    });

    it('5 intentos por código: el quinto fallo lo agota, y ni el correcto sirve después', async () => {
      const codigo = t.correo.ultimo('ana@colegio.co');
      const malo = codigo === '000000' ? '111111' : '000000';
      for (let i = 1; i <= 4; i++) {
        const res = await t.http.post('/auth/verificar-correo').set(bearer(token)).send({ codigo: malo }).expect(400);
        expect(res.body.message).toContain('incorrecto');
      }
      await t.http.post('/auth/verificar-correo').set(bearer(token)).send({ codigo: malo }).expect(429);
      await t.http.post('/auth/verificar-correo').set(bearer(token)).send({ codigo }).expect(429);
      const [fila] = await t.db.query('SELECT intentos FROM codigo_verificacion');
      expect(fila.intentos).toBe(5);

      // Con un código nuevo, vuelve a funcionar
      await envejecerCodigo(t.db, 'ana@colegio.co', 31);
      await t.http.post('/auth/reenviar-codigo').send({ email: 'ana@colegio.co' }).expect(201);
      await t.http
        .post('/auth/verificar-correo')
        .set(bearer(token))
        .send({ codigo: t.correo.ultimo('ana@colegio.co') })
        .expect(200);
    });
  });

  describe('inicio de sesión (RF-01-07)', () => {
    it('5 contraseñas incorrectas bloquean 15 minutos, con el mismo mensaje genérico', async () => {
      await crearCuenta(t, 'ana@colegio.co');
      for (let i = 1; i <= 5; i++) {
        const res = await t.http.post('/auth/login').send({ email: 'ana@colegio.co', password: 'Malamala1' }).expect(401);
        expect(res.body.message).toBe('Credenciales inválidas');
      }
      // Bloqueada: ni la contraseña correcta entra, y el mensaje no cambia
      const bloqueada = await t.http.post('/auth/login').send({ email: 'ana@colegio.co', password: CLAVE }).expect(401);
      expect(bloqueada.body.message).toBe('Credenciales inválidas');
      const [fila] = await t.db.query(
        'SELECT TIMESTAMPDIFF(MINUTE, NOW(), bloqueado_hasta) AS min FROM credencial',
      );
      expect(Number(fila.min)).toBeGreaterThanOrEqual(14);

      // Pasados los 15 minutos, entra
      await t.db.query('UPDATE credencial SET bloqueado_hasta = DATE_SUB(NOW(), INTERVAL 1 MINUTE)');
      await t.http.post('/auth/login').send({ email: 'ana@colegio.co', password: CLAVE }).expect(200);
    });

    it('un correo que no existe da el mismo 401 que una contraseña incorrecta', async () => {
      const res = await t.http.post('/auth/login').send({ email: 'nadie@x.co', password: CLAVE }).expect(401);
      expect(res.body.message).toBe('Credenciales inválidas');
    });
  });

  describe('recuperar la contraseña (CU-07) sin revelar si el correo existe (RNF-07)', () => {
    it('responde igual exista o no la cuenta, y el flujo completo cambia la contraseña', async () => {
      await crearCuenta(t, 'ana@colegio.co');
      const existe = await t.http.post('/auth/recuperar-contrasena').send({ email: 'ana@colegio.co' }).expect(202);
      const noExiste = await t.http.post('/auth/recuperar-contrasena').send({ email: 'nadie@x.co' }).expect(202);
      expect(existe.body).toEqual(noExiste.body);
      expect(t.correo.cuantos('nadie@x.co', 'recuperar_contrasena')).toBe(0);

      // Verificar con un correo que no existe: el mismo mensaje que un código malo
      const codigo = t.correo.ultimo('ana@colegio.co', 'recuperar_contrasena');
      const malo = codigo === '000000' ? '111111' : '000000';
      const r1 = await t.http.post('/auth/recuperar-contrasena/verificar').send({ email: 'nadie@x.co', codigo }).expect(400);
      const r2 = await t.http.post('/auth/recuperar-contrasena/verificar').send({ email: 'ana@colegio.co', codigo: malo }).expect(400);
      expect(r1.body.message).toBe(r2.body.message);

      const ver = await t.http
        .post('/auth/recuperar-contrasena/verificar')
        .send({ email: 'ana@colegio.co', codigo })
        .expect(200);

      // El token de recuperación no abre sesión
      await t.http.get('/auth/profile').set(bearer(ver.body.token)).expect(401);
      // Y un token de sesión no sirve para fijar la contraseña
      const sesion = await t.http.post('/auth/login').send({ email: 'ana@colegio.co', password: CLAVE }).expect(200);
      await t.http.post('/auth/nueva-contrasena').set(bearer(sesion.body.token)).send({ password: 'NuevaClave9' }).expect(401);

      await t.http.post('/auth/nueva-contrasena').set(bearer(ver.body.token)).send({ password: 'debil' }).expect(400);
      await t.http.post('/auth/nueva-contrasena').set(bearer(ver.body.token)).send({ password: 'NuevaClave9' }).expect(204);
      await t.http.post('/auth/login').send({ email: 'ana@colegio.co', password: CLAVE }).expect(401);
      await t.http.post('/auth/login').send({ email: 'ana@colegio.co', password: 'NuevaClave9' }).expect(200);
    });
  });

  describe('editar el propio perfil (CU-09, E-12)', () => {
    it('PATCH /auth/profile cambia solo el perfil de quien tiene la sesión', async () => {
      const ana = await crearCuenta(t, 'ana@colegio.co', 'docente');
      const luis = await crearCuenta(t, 'luis@colegio.co', 'estudiante');

      const res = await t.http
        .patch('/auth/profile')
        .set(bearer(luis.token))
        .send({ apellidos: 'Gómez Ruiz' })
        .expect(200);
      expect(res.body.user.perfil).toMatchObject({ nombres: 'Ana', apellidos: 'Gómez Ruiz' });

      const deAna = await t.http.get('/auth/profile').set(bearer(ana.token)).expect(200);
      expect(deAna.body.user.perfil.apellidos).toBe('Pérez');

      // Una foto de más de 5 MB → 413, y la foto no cambia (RF-01-05)
      const grande = Buffer.concat([
        Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
        Buffer.alloc(5 * 1024 * 1024),
      ]);
      await t.http.patch('/auth/profile').set(bearer(luis.token)).attach('foto', grande, 'g.png').expect(413);
      const sinFoto = await t.http.get('/auth/profile').set(bearer(luis.token)).expect(200);
      expect(sinFoto.body.user.perfil.avatarUrl).toBeNull();

      // El correo y el rol no se editan; los nombres no quedan vacíos
      await t.http.patch('/auth/profile').set(bearer(luis.token)).send({ email: 'x@x.co' }).expect(400);
      await t.http.patch('/auth/profile').set(bearer(luis.token)).send({ role: 'docente' }).expect(400);
      await t.http.patch('/auth/profile').set(bearer(luis.token)).send({ nombres: '' }).expect(400);

      // Y el perfil ajeno, por la ruta de la guía, es solo de administrador
      await t.http.patch(`/users/${ana.id}`).set(bearer(luis.token)).send({ fullName: 'X' }).expect(403);
    });

    it('sin rol todavía no hay perfil que editar → 403', async () => {
      const reg = await t.http.post('/auth/register').send({ email: 'ana@colegio.co', password: CLAVE });
      await t.http.patch('/auth/profile').set(bearer(reg.body.token)).send({ nombres: 'Ana' }).expect(403);
    });
  });

  describe('/users es solo del administrador (guía, ADR-040)', () => {
    it('con un usuario normal → 403; sin token → 401; ninguna ruta pone la marca', async () => {
      const ana = await crearCuenta(t, 'ana@colegio.co');
      await t.http.get('/users').set(bearer(ana.token)).expect(403);
      await t.http.post('/users').set(bearer(ana.token)).send({ email: 'b@x.co', password: CLAVE }).expect(403);
      await t.http.get('/users').expect(401);

      await t.db.query("UPDATE credencial SET es_admin = 1 WHERE correo = 'ana@colegio.co'");
      // La API no acepta asignar rol ni marca: forbidNonWhitelisted → 400
      await t.http.patch(`/users/${ana.id}`).set(bearer(ana.token)).send({ role: 'admin' }).expect(400);
      await t.http.patch(`/users/${ana.id}`).set(bearer(ana.token)).send({ esAdmin: true }).expect(400);
    });

    it('borrar un usuario con rol borra también su docente (204)', async () => {
      const admin = await crearCuenta(t, 'admin@x.co');
      await t.db.query("UPDATE credencial SET es_admin = 1 WHERE correo = 'admin@x.co'");
      const ana = await crearCuenta(t, 'ana@colegio.co');
      await t.http.delete(`/users/${ana.id}`).set(bearer(admin.token)).expect(204);
      const [{ n }] = await t.db.query('SELECT COUNT(*) AS n FROM docente');
      expect(Number(n)).toBe(1);
    });
  });

  describe('Google y Microsoft (E-04, E-05), con un proveedor simulado', () => {
    it('cuenta nueva: nace verificada y sin rol; la segunda vez, entra a la misma', async () => {
      const token = tokenConFormaDeJwt('ana-google');
      t.google.registrar(token, { proveedorId: 'g-1', correo: 'ana@gmail.com', nombre: 'Ana Pérez' });

      const r1 = await t.http.post('/auth/google').send({ token }).expect(200);
      expect(r1.body.user).toMatchObject({ email: 'ana@gmail.com', fullName: 'Ana Pérez', role: 'user' });
      const perfil = await t.http.get('/auth/profile').set(bearer(r1.body.token)).expect(200);
      expect(perfil.body.user).toMatchObject({ proveedor: 'google', estadoVerificacion: 'verificado' });

      // Con el correo verificado por Google, elige rol directamente
      await t.http
        .post('/auth/elegir-rol')
        .set(bearer(r1.body.token))
        .send({ role: 'estudiante', nombres: 'Ana', apellidos: 'Pérez' })
        .expect(201);

      const r2 = await t.http.post('/auth/google').send({ token }).expect(200);
      expect(r2.body.user).toMatchObject({ id: r1.body.user.id, role: 'estudiante' });

      // No tiene contraseña: el login con contraseña dice qué método usar
      const login = await t.http.post('/auth/login').send({ email: 'ana@gmail.com', password: CLAVE }).expect(409);
      expect(login.body.message).toContain('Google');
    });

    it('un correo ya registrado con otro método → 409 y no se vincula (RF-01-04)', async () => {
      await t.http.post('/auth/register').send({ email: 'ana@colegio.co', password: CLAVE }).expect(201);
      const token = tokenConFormaDeJwt('ana-ms');
      t.microsoft.registrar(token, { proveedorId: 'm-1', correo: 'ana@colegio.co', nombre: null });
      await t.http.post('/auth/microsoft').send({ token }).expect(409);
      const [{ n }] = await t.db.query('SELECT COUNT(*) AS n FROM credencial');
      expect(Number(n)).toBe(1);
    });

    it('un token que el proveedor rechaza → 401; uno sin forma de JWT → 400', async () => {
      await t.http.post('/auth/google').send({ token: tokenConFormaDeJwt('desconocido') }).expect(401);
      await t.http.post('/auth/google').send({ token: 'no-es-un-jwt' }).expect(400);
    });

    it('sin configuración → 503 «no configurado»', async () => {
      t.microsoft.configurado = false;
      try {
        const res = await t.http.post('/auth/microsoft').send({ token: tokenConFormaDeJwt('x') }).expect(503);
        expect(res.body.message).toContain('no está configurado');
      } finally {
        t.microsoft.configurado = true;
      }
    });
  });
});
