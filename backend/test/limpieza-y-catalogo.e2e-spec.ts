import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { LimpiezaService } from '../src/limpieza/limpieza.service.js';
import { CLAVE, borrarCuentas, crearApp, crearCuenta, type AppPruebas } from './app-pruebas.js';

describe('Tarea nocturna (ADR-039)', () => {
  let t: AppPruebas;
  beforeAll(async () => {
    t = await crearApp();
    await borrarCuentas(t.db);
  });
  afterAll(async () => t.app.close());

  it('borra códigos vencidos y credenciales de más de 7 días en procesando sin rol; nada más', async () => {
    const registrar = (email: string) => t.http.post('/auth/register').send({ email, password: CLAVE }).expect(201);
    await registrar('vieja@x.co'); // 8 días, procesando, sin rol → se borra
    await registrar('reciente@x.co'); // procesando, de hoy → queda
    await registrar('verificada@x.co'); // 8 días, verificada pero sin rol → queda
    await registrar('admin@x.co'); // 8 días, procesando, admin → queda
    await crearCuenta(t, 'docente@x.co'); // con rol → queda

    const hace = (dias: number) => `DATE_SUB(NOW(), INTERVAL ${dias} DAY)`;
    await t.db.query(
      `UPDATE credencial SET creado_en = ${hace(8)} WHERE correo IN ('vieja@x.co','verificada@x.co','admin@x.co')`,
    );
    await t.db.query("UPDATE credencial SET estado_verificacion = 'verificado' WHERE correo = 'verificada@x.co'");
    await t.db.query("UPDATE credencial SET es_admin = 1 WHERE correo = 'admin@x.co'");
    // El código de reciente@ venció; el de admin@ sigue vigente
    await t.db.query(
      "UPDATE codigo_verificacion c JOIN credencial u USING (id_credencial) " +
        "SET c.creado_en = DATE_SUB(NOW(), INTERVAL 11 MINUTE) WHERE u.correo = 'reciente@x.co'",
    );

    const resultado = await t.app.get(LimpiezaService).limpiar();
    // vieja@ cuenta como credencial; su código se va en cascada (no se cuenta)
    expect(resultado).toEqual({ codigosVencidos: 1, credencialesSinTerminar: 1 });

    const quedan = await t.db.query('SELECT correo FROM credencial ORDER BY correo');
    expect(quedan.map((f: { correo: string }) => f.correo)).toEqual([
      'admin@x.co',
      'docente@x.co',
      'reciente@x.co',
      'verificada@x.co',
    ]);
    const codigos = await t.db.query(
      'SELECT u.correo FROM codigo_verificacion c JOIN credencial u USING (id_credencial) ORDER BY u.correo',
    );
    expect(codigos.map((f: { correo: string }) => f.correo)).toEqual(['admin@x.co', 'verificada@x.co']);
  });

  it('está programada con la hora de .env (por defecto 3:00 a. m.)', async () => {
    const { SchedulerRegistry } = await import('@nestjs/schedule');
    const tarea = t.app.get(SchedulerRegistry).getCronJob('limpieza-nocturna');
    expect(tarea.cronTime.source).toBe('0 3 * * *');
  });
});

describe('Catálogo curricular (E-14 a E-17): solo lectura, solo docente', () => {
  let t: AppPruebas;
  let docente: string;
  let estudiante: string;
  let sinRol: string;
  const bearer = (token: string) => ({ Authorization: `Bearer ${token}` });

  beforeAll(async () => {
    t = await crearApp();
    await borrarCuentas(t.db);
    docente = (await crearCuenta(t, 'doc@x.co', 'docente')).token;
    estudiante = (await crearCuenta(t, 'est@x.co', 'estudiante')).token;
    sinRol = (await t.http.post('/auth/register').send({ email: 'nuevo@x.co', password: CLAVE })).body.token;
  });
  afterAll(async () => t.app.close());

  it('solo la sesión de un docente: sin token 401, estudiante o sin rol 403', async () => {
    for (const ruta of ['/catalogo/areas', '/catalogo/grados', '/catalogo/dbas?codigo_area=MAT', '/catalogo/dbas/MAT-08-01']) {
      await t.http.get(ruta).expect(401);
      await t.http.get(ruta).set(bearer(estudiante)).expect(403);
      await t.http.get(ruta).set(bearer(sinRol)).expect(403);
      await t.http.get(ruta).set(bearer(docente)).expect(200);
    }
  });

  it('GET /catalogo/areas — las 4 áreas de ADR-033', async () => {
    const res = await t.http.get('/catalogo/areas').set(bearer(docente)).expect(200);
    expect(res.body).toEqual([
      { codigo: 'CN', nombre: 'Ciencias Naturales' },
      { codigo: 'CS', nombre: 'Ciencias Sociales' },
      { codigo: 'LEN', nombre: 'Lenguaje' },
      { codigo: 'MAT', nombre: 'Matemáticas' },
    ]);
  });

  it('GET /catalogo/grados — 1 a 11 con su nivel de la Ley 115', async () => {
    const res = await t.http.get('/catalogo/grados').set(bearer(docente)).expect(200);
    expect(res.body).toHaveLength(11);
    expect(res.body[0]).toEqual({ numero: 1, nombre: 'Primero', nivel: 'basica_primaria' });
    expect(res.body[8]).toEqual({ numero: 9, nombre: 'Noveno', nivel: 'basica_secundaria' });
    expect(res.body[10]).toEqual({ numero: 11, nombre: 'Undécimo', nivel: 'media' });
  });

  it('GET /catalogo/dbas — filtra por área, por grado y por texto', async () => {
    const mat = await t.http.get('/catalogo/dbas?codigo_area=MAT').set(bearer(docente)).expect(200);
    expect(mat.body).toHaveLength(119);
    expect(mat.body.every((d: { area: { codigo: string } }) => d.area.codigo === 'MAT')).toBe(true);

    const mat8 = await t.http.get('/catalogo/dbas?codigo_area=MAT&numero_grado=8').set(bearer(docente)).expect(200);
    expect(mat8.body.length).toBeGreaterThan(0);
    expect(mat8.body.every((d: { codigo: string; grado: { numero: number } }) =>
      d.grado.numero === 8 && d.codigo.startsWith('MAT-08-'))).toBe(true);

    const cs = await t.http.get('/catalogo/dbas?codigo_area=CS').set(bearer(docente)).expect(200);
    expect(cs.body).toHaveLength(82);

    const texto = await t.http
      .get('/catalogo/dbas?codigo_area=MAT&q=irracionales')
      .set(bearer(docente))
      .expect(200);
    expect(texto.body.length).toBeGreaterThan(0);
    expect(texto.body.every((d: { enunciado: string }) => /irracionales/i.test(d.enunciado))).toBe(true);
  });

  it('GET /catalogo/dbas — sin área, con un área que no existe o un grado fuera de 1 a 11 → 400', async () => {
    await t.http.get('/catalogo/dbas').set(bearer(docente)).expect(400);
    await t.http.get('/catalogo/dbas?codigo_area=ART').set(bearer(docente)).expect(400);
    await t.http.get('/catalogo/dbas?codigo_area=mat').set(bearer(docente)).expect(400);
    await t.http.get('/catalogo/dbas?codigo_area=MAT&numero_grado=12').set(bearer(docente)).expect(400);
    await t.http.get('/catalogo/dbas?codigo_area=MAT&otro=1').set(bearer(docente)).expect(400);
  });

  it('GET /catalogo/dbas/:codigo — documento oficial y evidencias en orden; 404 si no existe', async () => {
    const res = await t.http.get('/catalogo/dbas/CS-05-01').set(bearer(docente)).expect(200);
    expect(res.body).toMatchObject({
      codigo: 'CS-05-01',
      area: { codigo: 'CS', nombre: 'Ciencias Sociales' },
      grado: { numero: 5, nombre: 'Quinto' },
      // ADR-033: Ciencias Sociales es V.1, aunque el archivo diga "v2"
      documento: { version: 'V.1', anio: 2016, paginas: 52 },
    });
    const numeros = res.body.evidencias.map((e: { numero: number }) => e.numero);
    expect(numeros).toEqual([...numeros].sort((a, b) => a - b));
    expect(numeros[0]).toBe(1);
    // Sin dictamen todavía (censo QA-014): ni sí ni no
    expect(res.body.evidencias[0]).toMatchObject({ admiteFormatoCerrado: null, formato: null });

    await t.http.get('/catalogo/dbas/MAT-99-99').set(bearer(docente)).expect(404);
  });
});
