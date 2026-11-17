import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import {
  borrarCuentas,
  crearApp,
  crearCuenta,
  type AppPruebas,
} from './app-pruebas.js';
import {
  borrarExperiencias,
  crearExperiencia,
  HIPOTESIS,
  idDeRol,
  renombrarEstudiante,
  seleccion,
  tomar,
  type ExperienciaPrueba,
  type Formato,
  type Plan,
} from './experiencias-prueba.js';

// Encargo 07, parte D: I3 (diagnóstico, E-29 a E-34) e I4 (reporte, E-35 a
// E-37) de punta a punta, contra MySQL. Las experiencias las arma el
// ayudante directo en la base (sin los endpoints de I2, encargo 06).

const auth = (token: string) => ({ Authorization: `Bearer ${token}` });

// Planes de respuesta (qué hace el estudiante con la k-ésima pregunta de cada evidencia).
const todoBienSeguro: Plan = () => ({ correcta: true, certeza: 5 });
const todoAdivinado: Plan = (_ev, k) => ({
  correcta: k % 2 === 0,
  certeza: k % 3,
}); // certeza 0 a 2: débil

/**
 * Lo que el estudiante NUNCA recibe (RF-04-08, ADR-028 punto 4, ADR-020):
 * se revisa la respuesta JSON completa, a cualquier profundidad.
 */
const CLAVES_PROHIBIDAS = [
  'es_correcta',
  'hipotesis_error',
  'correcta',
  'orden',
  'orden_presentacion',
  'numero_evidencia',
  'estado',
  'resultado',
  'resultados',
  'faltan',
  'total',
];
const VALORES_PROHIBIDOS = [
  'muestra',
  'no_muestra',
  'no_concluyente',
  'sin_concluir',
  HIPOTESIS,
];

function revisarQueNadaSeFiltre(cuerpo: unknown, donde = '$'): void {
  if (Array.isArray(cuerpo)) {
    cuerpo.forEach((x, i) => revisarQueNadaSeFiltre(x, `${donde}[${i}]`));
  } else if (cuerpo && typeof cuerpo === 'object') {
    for (const [k, v] of Object.entries(cuerpo)) {
      expect(CLAVES_PROHIBIDAS, `clave ${k} en ${donde}`).not.toContain(k);
      revisarQueNadaSeFiltre(v, `${donde}.${k}`);
    }
  } else if (typeof cuerpo === 'string') {
    expect(VALORES_PROHIBIDOS, `valor ${cuerpo} en ${donde}`).not.toContain(
      cuerpo,
    );
  }
}

describe('I3 e I4 — diagnóstico y reporte (encargo 07)', () => {
  let t: AppPruebas;
  let docente: { token: string; email: string; idDocente: number };
  let otroDocente: { token: string; idDocente: number };
  let n = 0;

  /** Un estudiante nuevo, con sesión. */
  async function estudiante(
    nombres?: string,
    apellidos?: string,
  ): Promise<{ token: string; email: string }> {
    const email = `est${++n}@prueba.co`;
    const { token } = await crearCuenta(t, email, 'estudiante');
    if (nombres) await renombrarEstudiante(t.db, email, nombres, apellidos!);
    return { token, email };
  }

  async function unirse(token: string, codigo: string): Promise<number> {
    const r = await t.http
      .post('/inscripciones')
      .set(auth(token))
      .send({ codigo });
    expect([200, 201]).toContain(r.status);
    return r.body.id_inscripcion;
  }

  beforeAll(async () => {
    t = await crearApp();
    await borrarExperiencias(t.db);
    await borrarCuentas(t.db);
    const d = await crearCuenta(t, 'docente@prueba.co', 'docente');
    docente = {
      token: d.token,
      email: 'docente@prueba.co',
      idDocente: (await idDeRol(t.db, 'docente@prueba.co')).idDocente!,
    };
    const o = await crearCuenta(t, 'otro.docente@prueba.co', 'docente');
    otroDocente = {
      token: o.token,
      idDocente: (await idDeRol(t.db, 'otro.docente@prueba.co')).idDocente!,
    };
  });
  afterAll(async () => {
    await borrarExperiencias(t.db);
    await t.app.close();
  });

  // ------------------------------------------------------------ D.1
  describe.each<Formato>(['single_choice', 'matching', 'ordering'])(
    'D.1 El camino del estudiante — %s',
    (formato) => {
      let exp: ExperienciaPrueba;
      let est: { token: string };
      let id: number;

      beforeAll(async () => {
        exp = await crearExperiencia(t.db, docente.idDocente, {
          formato,
          excluidos: 2,
        });
        est = await estudiante();
      });

      it('se une con el código, en minúsculas, y entra "No iniciada" (CU-22)', async () => {
        const r = await t.http
          .post('/inscripciones')
          .set(auth(est.token))
          .send({ codigo: ` ${exp.codigo.toLowerCase()} ` })
          .expect(201);
        id = r.body.id_inscripcion;
        expect(r.body.progreso).toBe('no_iniciada');
        expect(r.body.experiencia).toMatchObject({
          id_experiencia: exp.id,
          docente: { nombres: 'Ana', apellidos: 'Pérez' },
        });
        expect(typeof r.body.experiencia.area).toBe('string');
        const c = await t.http
          .get(`/inscripciones/${id}`)
          .set(auth(est.token))
          .expect(200);
        expect(c.body).toMatchObject({
          progreso: 'no_iniciada',
          respuestas: 0,
        });
      });

      it('responde hasta concluir todas las evidencias, en el orden oficial, y recibe el cierre sin pregunta', async () => {
        const toma = await tomar(t, est.token, id, exp, todoBienSeguro);
        expect(toma.terminada).toBe(true);
        // ADR-031 p.4: todo correcto y seguro concluye en la 4.ª respuesta de cada evidencia.
        expect(toma.secuencia).toEqual(
          exp.evidencias.flatMap((e) => [e, e, e, e]),
        );
        // ADR-024: el orden oficial, aunque el ayudante las insertó al revés.
        expect([...exp.evidencias].sort((a, b) => a - b)).toEqual(
          exp.evidencias,
        );
        // Nada de lo que recibió dice si acertó ni cómo va.
        revisarQueNadaSeFiltre(toma.cuerpos);

        const resultados = await t.db.query(
          'SELECT numero_evidencia, estado, fecha_calculo FROM resultado WHERE id_inscripcion = ? ORDER BY numero_evidencia',
          [id],
        );
        expect(resultados.map((r: { estado: string }) => r.estado)).toEqual([
          'muestra',
          'muestra',
          'muestra',
        ]);
        expect(
          resultados.every(
            (r: { fecha_calculo: Date | null }) => r.fecha_calculo !== null,
          ),
        ).toBe(true);
        // ADR-021: `correcta` se guarda como fotografía.
        const [{ bien }] = await t.db.query(
          'SELECT SUM(correcta) AS bien FROM respuesta WHERE id_inscripcion = ?',
          [id],
        );
        expect(Number(bien)).toBe(12);
        // ADR-015: los ítems excluidos nunca se presentan.
        const [{ excluidos }] = await t.db.query(
          'SELECT COUNT(*) AS excluidos FROM presentacion p JOIN item i ON i.id_item = p.id_item WHERE p.id_inscripcion = ? AND i.excluido',
          [id],
        );
        expect(Number(excluidos)).toBe(0);
      });

      it('al volver, el cierre se repite (200 sin pregunta) y la experiencia figura Completada', async () => {
        const r = await t.http
          .post(`/inscripciones/${id}/presentaciones`)
          .set(auth(est.token))
          .expect(200);
        expect(r.body).toEqual({ pregunta: null });
        const lista = await t.http
          .get('/inscripciones')
          .set(auth(est.token))
          .expect(200);
        expect(lista.body.map((x: { progreso: string }) => x.progreso)).toEqual(
          ['completada'],
        );
        revisarQueNadaSeFiltre(lista.body);
        const c = await t.http
          .get(`/inscripciones/${id}`)
          .set(auth(est.token))
          .expect(200);
        expect(c.body).toMatchObject({
          progreso: 'completada',
          respuestas: 12,
        });
        revisarQueNadaSeFiltre(c.body);
      });

      it('una respuesta incorrecta del formato se guarda como incorrecta (ADR-031 p.3, CU-24)', async () => {
        const otro = await estudiante();
        const idOtro = await unirse(otro.token, exp.codigo);
        const toma = await tomar(t, otro.token, idOtro, exp, (ev, k) =>
          ev === exp.evidencias[0] && k < 4
            ? { correcta: false, certeza: 4 }
            : null,
        );
        expect(toma.terminada).toBe(false);
        const [r] = await t.db.query(
          'SELECT estado FROM resultado WHERE id_inscripcion = ?',
          [idOtro],
        );
        expect(r.estado).toBe('no_muestra');
        const [{ bien }] = await t.db.query(
          'SELECT SUM(correcta) AS bien FROM respuesta WHERE id_inscripcion = ?',
          [idOtro],
        );
        expect(Number(bien)).toBe(0);
      });
    },
  );

  // ------------------------------------------------------------ D.2 y D.3
  describe('D.2 Retomar y D.3 salir y volver', () => {
    let exp: ExperienciaPrueba;
    let est: { token: string };
    let id: number;

    beforeAll(async () => {
      exp = await crearExperiencia(t.db, docente.idDocente, {
        formato: 'matching',
      });
      est = await estudiante();
      id = await unirse(est.token, exp.codigo);
    });

    it('ADR-031 p.6: una pregunta sin responder se repite, con sus opciones en el mismo orden, sin crear otra presentación', async () => {
      const a = await t.http
        .post(`/inscripciones/${id}/presentaciones`)
        .set(auth(est.token))
        .expect(201);
      const b = await t.http
        .post(`/inscripciones/${id}/presentaciones`)
        .set(auth(est.token))
        .expect(200);
      expect(b.body).toEqual(a.body);
      revisarQueNadaSeFiltre([a.body, b.body]);
      const [{ cuantas }] = await t.db.query(
        'SELECT COUNT(*) AS cuantas FROM presentacion WHERE id_inscripcion = ?',
        [id],
      );
      expect(Number(cuantas)).toBe(1);
      // Ya está "En curso" (CU-21, prueba de aceptación: desde la primera pregunta).
      const c = await t.http
        .get(`/inscripciones/${id}`)
        .set(auth(est.token))
        .expect(200);
      expect(c.body.progreso).toBe('en_curso');
    });

    it('al emparejar, el estudiante recibe el lado de cada opción pero no la pareja correcta', async () => {
      const r = await t.http
        .post(`/inscripciones/${id}/presentaciones`)
        .set(auth(est.token))
        .expect(200);
      expect(r.body.pregunta.formato).toBe('matching');
      expect(
        r.body.pregunta.opciones.every((o: { grupo: string }) =>
          ['izquierda', 'derecha'].includes(o.grupo),
        ),
      ).toBe(true);
      expect(Object.keys(r.body.pregunta.opciones[0]).sort()).toEqual([
        'grupo',
        'id_opcion',
        'texto',
      ]);
    });

    it('CU-26: salir borra la inscripción y lo respondido; al volver con el código aparece "No iniciada"', async () => {
      const r = await t.http
        .post(`/inscripciones/${id}/presentaciones`)
        .set(auth(est.token))
        .expect(200);
      const item = exp.items.get(r.body.pregunta.id_item)!;
      await t.http
        .post(`/inscripciones/${id}/respuestas`)
        .set(auth(est.token))
        .send({ id_item: item.id, opciones: seleccion(item, true), certeza: 3 })
        .expect(201);
      const c = await t.http
        .get(`/inscripciones/${id}`)
        .set(auth(est.token))
        .expect(200);
      expect(c.body.respuestas).toBe(1); // lo que se perdería al salir (CU-26 paso 2)

      await t.http
        .delete(`/inscripciones/${id}`)
        .set(auth(est.token))
        .expect(204);
      await t.http
        .get('/inscripciones')
        .set(auth(est.token))
        .expect(200)
        .expect([]);
      for (const tabla of ['presentacion', 'respuesta', 'resultado']) {
        const [{ cuantas }] = await t.db.query(
          `SELECT COUNT(*) AS cuantas FROM ${tabla} WHERE id_inscripcion = ?`,
          [id],
        );
        expect(Number(cuantas)).toBe(0);
      }
      // El banco no cambia (CU-26, postcondición).
      const [{ items }] = await t.db.query(
        'SELECT COUNT(*) AS items FROM item WHERE id_experiencia = ?',
        [exp.id],
      );
      expect(Number(items)).toBe(18);

      const v = await t.http
        .post('/inscripciones')
        .set(auth(est.token))
        .send({ codigo: exp.codigo })
        .expect(201);
      expect(v.body.progreso).toBe('no_iniciada');
      expect(v.body.id_inscripcion).not.toBe(id);
    });
  });

  // ------------------------------------------------------------ integridad
  describe('B.4 Reglas de integridad', () => {
    let exp: ExperienciaPrueba;
    let est: { token: string };
    let id: number;

    beforeAll(async () => {
      exp = await crearExperiencia(t.db, docente.idDocente);
      est = await estudiante();
    });

    it('RI-1: unirse dos veces no duplica (201 la primera, 200 la segunda, la misma inscripción)', async () => {
      const a = await t.http
        .post('/inscripciones')
        .set(auth(est.token))
        .send({ codigo: exp.codigo })
        .expect(201);
      const b = await t.http
        .post('/inscripciones')
        .set(auth(est.token))
        .send({ codigo: exp.codigo.toLowerCase() })
        .expect(200);
      expect(b.body.id_inscripcion).toBe(a.body.id_inscripcion);
      id = a.body.id_inscripcion;
      const lista = await t.http
        .get('/inscripciones')
        .set(auth(est.token))
        .expect(200);
      expect(lista.body).toHaveLength(1);
    });

    it('RI-7: un código en Borrador da el mismo 404 que uno que no existe', async () => {
      const borrador = await crearExperiencia(t.db, docente.idDocente, {
        estado: 'Borrador',
      });
      const a = await t.http
        .post('/inscripciones')
        .set(auth(est.token))
        .send({ codigo: borrador.codigo })
        .expect(404);
      const b = await t.http
        .post('/inscripciones')
        .set(auth(est.token))
        .send({ codigo: 'ZZZZZZ' })
        .expect(404);
      expect(a.body.message).toBe(b.body.message);
      const [{ cuantas }] = await t.db.query(
        'SELECT COUNT(*) AS cuantas FROM inscripcion WHERE id_experiencia = ?',
        [borrador.id],
      );
      expect(Number(cuantas)).toBe(0);
    });

    it('RNF-10: una respuesta no se cambia (409), y solo se responde la pregunta pendiente (409)', async () => {
      const p = await t.http
        .post(`/inscripciones/${id}/presentaciones`)
        .set(auth(est.token))
        .expect(201);
      const item = exp.items.get(p.body.pregunta.id_item)!;
      const otroItem = [...exp.items.values()].find((i) => i.id !== item.id)!;
      // Una pregunta que no se le presentó
      await t.http
        .post(`/inscripciones/${id}/respuestas`)
        .set(auth(est.token))
        .send({
          id_item: otroItem.id,
          opciones: seleccion(otroItem, true),
          certeza: 3,
        })
        .expect(409);
      await t.http
        .post(`/inscripciones/${id}/respuestas`)
        .set(auth(est.token))
        .send({
          id_item: item.id,
          opciones: seleccion(item, false),
          certeza: 5,
        })
        .expect(201);
      const otra = await t.http
        .post(`/inscripciones/${id}/respuestas`)
        .set(auth(est.token))
        .send({ id_item: item.id, opciones: seleccion(item, true), certeza: 5 })
        .expect(409);
      expect(otra.body.message).toMatch(/no se cambia/);
      const [r] = await t.db.query(
        'SELECT correcta, certeza FROM respuesta WHERE id_inscripcion = ? AND id_item = ?',
        [id, item.id],
      );
      expect({ correcta: Number(r.correcta), certeza: r.certeza }).toEqual({
        correcta: 0,
        certeza: 5,
      });
    });

    it('RI-6: una opción de otro ítem se rechaza (400), y nada se guarda', async () => {
      const p = await t.http
        .post(`/inscripciones/${id}/presentaciones`)
        .set(auth(est.token))
        .expect(201);
      const item = exp.items.get(p.body.pregunta.id_item)!;
      const ajena = [...exp.items.values()].find((i) => i.id !== item.id)!
        .opciones[1];
      await t.http
        .post(`/inscripciones/${id}/respuestas`)
        .set(auth(est.token))
        .send({
          id_item: item.id,
          opciones: [{ id_opcion: ajena.id }],
          certeza: 3,
        })
        .expect(400);
      const [{ cuantas }] = await t.db.query(
        'SELECT COUNT(*) AS cuantas FROM respuesta WHERE id_inscripcion = ? AND id_item = ?',
        [id, item.id],
      );
      expect(Number(cuantas)).toBe(0);
    });

    it('RI-6 en el motor: la base misma rechaza una opción de otro ítem (ciclo C4)', async () => {
      const [r] = await t.db.query(
        'SELECT id_respuesta, id_item FROM respuesta WHERE id_inscripcion = ? LIMIT 1',
        [id],
      );
      const ajena = [...exp.items.values()].find((i) => i.id !== r.id_item)!
        .opciones[0];
      await expect(
        t.db.query(
          'INSERT INTO respuesta_opcion (id_respuesta, id_opcion, id_item) VALUES (?, ?, ?)',
          [r.id_respuesta, ajena.id, r.id_item],
        ),
      ).rejects.toThrow(/foreign key/i);
    });

    it('400: certeza fuera de 0 a 5, ninguna opción, dos en selección única, campos de más', async () => {
      const p = await t.http
        .post(`/inscripciones/${id}/presentaciones`)
        .set(auth(est.token))
        .expect(200);
      const item = exp.items.get(p.body.pregunta.id_item)!;
      const base = {
        id_item: item.id,
        opciones: seleccion(item, true),
        certeza: 3,
      };
      for (const malo of [
        { ...base, certeza: 6 },
        { ...base, certeza: -1 },
        { ...base, certeza: 2.5 },
        { ...base, opciones: [] },
        {
          ...base,
          opciones: [
            { id_opcion: item.opciones[0].id },
            { id_opcion: item.opciones[1].id },
          ],
        },
        { ...base, es_correcta: true },
        { id_item: item.id, opciones: base.opciones },
      ]) {
        await t.http
          .post(`/inscripciones/${id}/respuestas`)
          .set(auth(est.token))
          .send(malo)
          .expect(400);
      }
    });
  });

  // ------------------------------------------------------------ errores por endpoint
  describe('D.5 Errores: 400, 401, 403, 404 y 409 de cada endpoint', () => {
    let exp: ExperienciaPrueba;
    let duena: { token: string };
    let intrusa: { token: string };
    let id: number;

    beforeAll(async () => {
      exp = await crearExperiencia(t.db, docente.idDocente, {
        formato: 'ordering',
      });
      duena = await estudiante();
      intrusa = await estudiante();
      id = await unirse(duena.token, exp.codigo);
    });

    it('401 sin sesión en los 9 endpoints', async () => {
      await t.http.get('/inscripciones').expect(401);
      await t.http
        .post('/inscripciones')
        .send({ codigo: exp.codigo })
        .expect(401);
      await t.http.get(`/inscripciones/${id}`).expect(401);
      await t.http.post(`/inscripciones/${id}/presentaciones`).expect(401);
      await t.http.post(`/inscripciones/${id}/respuestas`).send({}).expect(401);
      await t.http.delete(`/inscripciones/${id}`).expect(401);
      await t.http.get(`/experiencias/${exp.id}/reporte`).expect(401);
      await t.http.get(`/experiencias/${exp.id}/estudiantes`).expect(401);
      await t.http.get(`/inscripciones/${id}/historial`).expect(401);
    });

    it('403: el docente no usa los endpoints del estudiante (E-29 a E-34)', async () => {
      const tk = auth(docente.token);
      await t.http.get('/inscripciones').set(tk).expect(403);
      await t.http
        .post('/inscripciones')
        .set(tk)
        .send({ codigo: exp.codigo })
        .expect(403);
      await t.http.get(`/inscripciones/${id}`).set(tk).expect(403);
      await t.http
        .post(`/inscripciones/${id}/presentaciones`)
        .set(tk)
        .expect(403);
      await t.http
        .post(`/inscripciones/${id}/respuestas`)
        .set(tk)
        .send({ id_item: 1, opciones: [{ id_opcion: 1 }], certeza: 1 })
        .expect(403);
      await t.http.delete(`/inscripciones/${id}`).set(tk).expect(403);
    });

    it('403: otro estudiante no toca una inscripción ajena (E-31 a E-34)', async () => {
      const tk = auth(intrusa.token);
      await t.http.get(`/inscripciones/${id}`).set(tk).expect(403);
      await t.http
        .post(`/inscripciones/${id}/presentaciones`)
        .set(tk)
        .expect(403);
      await t.http
        .post(`/inscripciones/${id}/respuestas`)
        .set(tk)
        .send({ id_item: 1, opciones: [{ id_opcion: 1 }], certeza: 1 })
        .expect(403);
      await t.http.delete(`/inscripciones/${id}`).set(tk).expect(403);
      await t.http
        .get(`/inscripciones/${id}`)
        .set(auth(duena.token))
        .expect(200); // sigue ahí
    });

    it('403: el estudiante nunca ve el reporte, el grupo ni el historial (ADR-028), ni siquiera el suyo', async () => {
      const tk = auth(duena.token);
      await t.http.get(`/experiencias/${exp.id}/reporte`).set(tk).expect(403);
      await t.http
        .get(`/experiencias/${exp.id}/estudiantes`)
        .set(tk)
        .expect(403);
      await t.http.get(`/inscripciones/${id}/historial`).set(tk).expect(403);
    });

    it('403: otro docente no ve el reporte, el grupo ni el historial de una experiencia ajena (E-35 a E-37)', async () => {
      const tk = auth(otroDocente.token);
      await t.http.get(`/experiencias/${exp.id}/reporte`).set(tk).expect(403);
      await t.http
        .get(`/experiencias/${exp.id}/estudiantes`)
        .set(tk)
        .expect(403);
      await t.http.get(`/inscripciones/${id}/historial`).set(tk).expect(403);
    });

    it('404: lo que no existe', async () => {
      const est = auth(duena.token);
      const doc = auth(docente.token);
      await t.http
        .post('/inscripciones')
        .set(est)
        .send({ codigo: 'QQQQQQ' })
        .expect(404);
      await t.http.get('/inscripciones/999999').set(est).expect(404);
      await t.http
        .post('/inscripciones/999999/presentaciones')
        .set(est)
        .expect(404);
      await t.http
        .post('/inscripciones/999999/respuestas')
        .set(est)
        .send({ id_item: 1, opciones: [{ id_opcion: 1 }], certeza: 1 })
        .expect(404);
      await t.http.delete('/inscripciones/999999').set(est).expect(404);
      await t.http.get('/experiencias/999999/reporte').set(doc).expect(404);
      await t.http.get('/experiencias/999999/estudiantes').set(doc).expect(404);
      await t.http.get('/inscripciones/999999/historial').set(doc).expect(404);
    });

    it('400: datos que no cumplen una regla', async () => {
      const est = auth(duena.token);
      const doc = auth(docente.token);
      await t.http
        .get('/inscripciones?progreso=terminada')
        .set(est)
        .expect(400);
      await t.http.post('/inscripciones').set(est).send({}).expect(400);
      await t.http
        .post('/inscripciones')
        .set(est)
        .send({ codigo: '' })
        .expect(400);
      await t.http.get('/inscripciones/abc').set(est).expect(400);
      await t.http
        .post('/inscripciones/abc/presentaciones')
        .set(est)
        .expect(400);
      await t.http
        .post(`/inscripciones/${id}/respuestas`)
        .set(est)
        .send({ id_item: 'x', opciones: 'y', certeza: 'z' })
        .expect(400);
      await t.http.delete('/inscripciones/abc').set(est).expect(400);
      await t.http.get('/experiencias/abc/reporte').set(doc).expect(400);
      await t.http
        .get(`/experiencias/${exp.id}/estudiantes?estado=aprobado`)
        .set(doc)
        .expect(400);
      await t.http.get('/inscripciones/abc/historial').set(doc).expect(400);
    });

    it('409: responder sin una pregunta pendiente', async () => {
      const item = [...exp.items.values()][0];
      await t.http
        .post(`/inscripciones/${id}/respuestas`)
        .set(auth(duena.token))
        .send({ id_item: item.id, opciones: seleccion(item, true), certeza: 3 })
        .expect(409);
    });

    it('ordenar: el estudiante no recibe las posiciones, y las opciones no le llegan en el orden correcto guardado', async () => {
      const r = await t.http
        .post(`/inscripciones/${id}/presentaciones`)
        .set(auth(duena.token))
        .expect(201);
      expect(Object.keys(r.body.pregunta.opciones[0]).sort()).toEqual([
        'id_opcion',
        'texto',
      ]);
      revisarQueNadaSeFiltre(r.body);
    });
  });

  // ------------------------------------------------------------ D.4 reporte
  describe('D.4 Varios estudiantes: reporte, estudiantes por estado e historial', () => {
    let exp: ExperienciaPrueba;
    const ins: Record<string, number> = {};
    const emails: string[] = [];
    let e1: number, e2: number, e3: number;

    beforeAll(async () => {
      exp = await crearExperiencia(t.db, docente.idDocente, { evidencias: 3 });
      [e1, e2, e3] = exp.evidencias;
      // Cada estudiante y lo que hace. Lo que la regla predice, calculado a mano:
      const planes: Record<string, [string, string, Plan]> = {
        // A: todo bien y seguro → M, M, M → Muestra
        A: ['Zoe', 'Arias', todoBienSeguro],
        // B: e1 mal y seguro (4 respuestas → No muestra), el resto bien → NM, M, M → No muestra
        B: ['Carlos', 'Díaz', (ev) => ({ correcta: ev !== e1, certeza: 5 })],
        // C: todo con certeza 0 a 2 → 6 respuestas por evidencia → NC, NC, NC → No concluyente
        C: ['Diana', 'Ortiz', todoAdivinado],
        // D: e1 bien (M); en e2 responde 2 y sale con la 3.ª pendiente → M, SC, SC → Sin concluir
        D: [
          'Ana',
          'Ruiz',
          (ev, k) =>
            ev === e1 || k < 2 ? { correcta: true, certeza: 5 } : null,
        ],
        // E: solo se une → SC, SC, SC → Sin concluir
        E: ['Álvaro', 'Mena', () => null],
        // F: e1 mal y seguro (NM), sale con la 1.ª de e2 pendiente → NM, SC, SC → No muestra (precedencia ADR-022)
        F: [
          'Beatriz',
          'Gómez',
          (ev) => (ev === e1 ? { correcta: false, certeza: 4 } : null),
        ],
      };
      for (const [clave, [nombres, apellidos, plan]] of Object.entries(
        planes,
      )) {
        const est = await estudiante(nombres, apellidos);
        emails.push(est.email);
        ins[clave] = await unirse(est.token, exp.codigo);
        if (clave !== 'E') await tomar(t, est.token, ins[clave], exp, plan);
      }
    });

    it('la regla dejó en la base exactamente los resultados predichos', async () => {
      const filas: {
        id_inscripcion: number;
        numero_evidencia: number;
        estado: string;
      }[] = await t.db.query(
        'SELECT id_inscripcion, numero_evidencia, estado FROM resultado WHERE id_experiencia = ?',
        [exp.id],
      );
      const de = (k: string) =>
        [e1, e2, e3].map(
          (e) =>
            filas.find(
              (f) => f.id_inscripcion === ins[k] && f.numero_evidencia === e,
            )?.estado ?? 'sin_concluir',
        );
      expect(de('A')).toEqual(['muestra', 'muestra', 'muestra']);
      expect(de('B')).toEqual(['no_muestra', 'muestra', 'muestra']);
      expect(de('C')).toEqual([
        'no_concluyente',
        'no_concluyente',
        'no_concluyente',
      ]);
      expect(de('D')).toEqual(['muestra', 'sin_concluir', 'sin_concluir']);
      expect(de('E')).toEqual(['sin_concluir', 'sin_concluir', 'sin_concluir']);
      expect(de('F')).toEqual(['no_muestra', 'sin_concluir', 'sin_concluir']);
      // C respondió 6 por evidencia (tope de ADR-016); A, 4 por evidencia.
      const [{ c }] = await t.db.query(
        'SELECT COUNT(*) AS c FROM respuesta WHERE id_inscripcion = ?',
        [ins.C],
      );
      const [{ a }] = await t.db.query(
        'SELECT COUNT(*) AS a FROM respuesta WHERE id_inscripcion = ?',
        [ins.A],
      );
      expect([Number(c), Number(a)]).toEqual([18, 12]);
    });

    it('E-35: el reporte, con los números calculados a mano (ADR-022, ADR-032)', async () => {
      const r = await t.http
        .get(`/experiencias/${exp.id}/reporte`)
        .set(auth(docente.token))
        .expect(200);
      expect(r.body.inscritos).toBe(6);
      // Estado general: A muestra; B y F no muestra; C no concluyente; D y E sin concluir.
      expect(r.body.estado_general).toEqual({
        muestra: 1,
        no_muestra: 2,
        no_concluyente: 1,
        sin_concluir: 2,
      });
      expect(
        r.body.evidencias.map(
          (e: { numero_evidencia: number }) => e.numero_evidencia,
        ),
      ).toEqual([e1, e2, e3]);
      const [r1, r2, r3] = r.body.evidencias;
      // e1: A M, B NM, C NC, D M, E SC, F NM → NC+SC = 2 de 6 (33 % < 40 %) y hay "no muestra" → Brecha aparente
      expect(r1.distribucion).toEqual({
        muestra: 2,
        no_muestra: 2,
        no_concluyente: 1,
        sin_concluir: 1,
      });
      expect(r1.clasificacion).toBe('brecha_aparente');
      // e2 y e3: A M, B M, C NC, D SC, E SC, F SC → NC+SC = 4 de 6 (67 % ≥ 40 %) → Datos insuficientes
      for (const e of [r2, r3]) {
        expect(e.distribucion).toEqual({
          muestra: 2,
          no_muestra: 0,
          no_concluyente: 1,
          sin_concluir: 3,
        });
        expect(e.clasificacion).toBe('datos_insuficientes');
      }
      expect(typeof r1.enunciado).toBe('string');
    });

    it('E-35: Sin brecha aparente cuando todos muestran; y con N = 0 no hay clasificación', async () => {
      const otra = await crearExperiencia(t.db, docente.idDocente, {
        evidencias: 2,
      });
      for (let i = 0; i < 2; i++) {
        const est = await estudiante();
        await tomar(
          t,
          est.token,
          await unirse(est.token, otra.codigo),
          otra,
          todoBienSeguro,
        );
      }
      const r = await t.http
        .get(`/experiencias/${otra.id}/reporte`)
        .set(auth(docente.token))
        .expect(200);
      expect(r.body.estado_general).toEqual({
        muestra: 2,
        no_muestra: 0,
        no_concluyente: 0,
        sin_concluir: 0,
      });
      expect(
        r.body.evidencias.map(
          (e: { clasificacion: string }) => e.clasificacion,
        ),
      ).toEqual(['sin_brecha_aparente', 'sin_brecha_aparente']);

      const vacia = await crearExperiencia(t.db, docente.idDocente, {
        evidencias: 2,
      });
      const v = await t.http
        .get(`/experiencias/${vacia.id}/reporte`)
        .set(auth(docente.token))
        .expect(200);
      expect(v.body.inscritos).toBe(0);
      expect(
        v.body.evidencias.map((e: { clasificacion: null }) => e.clasificacion),
      ).toEqual([null, null]);
      const g = await t.http
        .get(`/experiencias/${vacia.id}/estudiantes`)
        .set(auth(docente.token))
        .expect(200);
      expect(g.body).toMatchObject({
        estado_experiencia: 'Publicada',
        inscritos: 0,
        grupos: [],
      });
    });

    it('E-36: grupos en el orden No muestra, No concluyente, Sin concluir, Muestra; alfabético dentro; con su estado por evidencia', async () => {
      const r = await t.http
        .get(`/experiencias/${exp.id}/estudiantes`)
        .set(auth(docente.token))
        .expect(200);
      const grupos = r.body.grupos.map(
        (g: { estado: string; estudiantes: { nombres: string }[] }) => [
          g.estado,
          g.estudiantes.map((e) => e.nombres),
        ],
      );
      expect(grupos).toEqual([
        ['no_muestra', ['Beatriz', 'Carlos']],
        ['no_concluyente', ['Diana']],
        ['sin_concluir', ['Álvaro', 'Ana']],
        ['muestra', ['Zoe']],
      ]);
      const beatriz = r.body.grupos[0].estudiantes[0];
      expect(
        beatriz.evidencias.map((e: { estado: string }) => e.estado),
      ).toEqual(['no_muestra', 'sin_concluir', 'sin_concluir']);
      // ADR-022, sub-distinción: Álvaro no ha respondido nada; Ana ya empezó.
      const [alvaro, ana] = r.body.grupos[2].estudiantes;
      expect([alvaro.ha_respondido, ana.ha_respondido]).toEqual([false, true]);
    });

    it('E-36: filtro por estado y búsqueda por nombre sin tildes ni mayúsculas', async () => {
      const m = await t.http
        .get(`/experiencias/${exp.id}/estudiantes?estado=muestra`)
        .set(auth(docente.token))
        .expect(200);
      expect(m.body.grupos).toHaveLength(1);
      expect(
        m.body.grupos[0].estudiantes.map((e: { nombres: string }) => e.nombres),
      ).toEqual(['Zoe']);
      const q = await t.http
        .get(`/experiencias/${exp.id}/estudiantes?q=ALVARO`)
        .set(auth(docente.token))
        .expect(200);
      expect(q.body.grupos).toEqual([
        expect.objectContaining({ estado: 'sin_concluir' }),
      ]);
      expect(q.body.grupos[0].estudiantes[0].apellidos).toBe('Mena');
    });

    it('ADR-029: ninguna respuesta del docente trae el correo del estudiante', async () => {
      const cuerpos = [
        (
          await t.http
            .get(`/experiencias/${exp.id}/reporte`)
            .set(auth(docente.token))
        ).text,
        (
          await t.http
            .get(`/experiencias/${exp.id}/estudiantes`)
            .set(auth(docente.token))
        ).text,
        ...(await Promise.all(
          Object.values(ins).map(
            async (i) =>
              (
                await t.http
                  .get(`/inscripciones/${i}/historial`)
                  .set(auth(docente.token))
              ).text,
          ),
        )),
      ];
      for (const texto of cuerpos) {
        for (const email of emails) expect(texto).not.toContain(email);
        expect(texto).not.toMatch(/"(correo|email)"/);
        expect(texto).not.toContain('@');
        // ADR-008 p.1 y ADR-020: la hipótesis de error nunca se reporta, tampoco al docente.
        expect(texto).not.toContain(HIPOTESIS);
        expect(texto).not.toContain('hipotesis_error');
      }
    });

    it('E-37: el historial de F, por evidencia en orden oficial, con la pregunta abandonada como no respondida (CU-29)', async () => {
      const r = await t.http
        .get(`/inscripciones/${ins.F}/historial`)
        .set(auth(docente.token))
        .expect(200);
      expect(r.body.estudiante).toEqual({
        nombres: 'Beatriz',
        apellidos: 'Gómez',
        avatar_url: null,
      });
      const [h1, h2, h3] = r.body.evidencias;
      expect([
        h1.numero_evidencia,
        h2.numero_evidencia,
        h3.numero_evidencia,
      ]).toEqual([e1, e2, e3]);
      expect([h1.estado, h2.estado, h3.estado]).toEqual([
        'no_muestra',
        'sin_concluir',
        'sin_concluir',
      ]);
      expect(
        h1.preguntas.map(
          (p: { orden_presentacion: number }) => p.orden_presentacion,
        ),
      ).toEqual([1, 2, 3, 4]);
      for (const p of h1.preguntas) {
        expect(p.respuesta).toMatchObject({ correcta: false, certeza: 4 });
        expect(p.respuesta.seleccion).toHaveLength(1);
        // El docente sí ve cuál era la correcta (27-spec §2.2).
        expect(
          p.opciones.filter((o: { es_correcta: boolean }) => o.es_correcta),
        ).toHaveLength(1);
      }
      expect(h2.preguntas).toHaveLength(1);
      expect(h2.preguntas[0]).toMatchObject({
        orden_presentacion: 5,
        respuesta: null,
      });
      expect(h3.preguntas).toEqual([]);
    });

    it('E-37: un estudiante que solo se unió no tiene preguntas en su historial', async () => {
      const r = await t.http
        .get(`/inscripciones/${ins.E}/historial`)
        .set(auth(docente.token))
        .expect(200);
      expect(
        r.body.evidencias.every(
          (e: { preguntas: unknown[]; estado: string }) =>
            e.preguntas.length === 0 && e.estado === 'sin_concluir',
        ),
      ).toBe(true);
    });

    it('RNF-04: el reporte no trae texto redactado que afirme certeza (solo códigos de estado)', async () => {
      const r = await t.http
        .get(`/experiencias/${exp.id}/reporte`)
        .set(auth(docente.token))
        .expect(200);
      const sinEnunciados = JSON.stringify({
        ...r.body,
        evidencias: r.body.evidencias.map((e: object) => ({
          ...e,
          enunciado: '',
        })),
      });
      expect(sinEnunciados).not.toMatch(
        /domina|aprob|reprob|nota|seguro|certeza|detectad|confirmad/i,
      );
    });
  });
});
