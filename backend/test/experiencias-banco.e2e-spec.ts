import { afterAll, beforeAll, beforeEach, describe, expect, it } from 'vitest';
import { IaFalsa } from '../src/banco/ia/ia-falsa.js';
import { SERVICIO_IA } from '../src/banco/ia/servicio-ia.js';
import {
  borrarCuentas,
  crearApp,
  crearCuenta,
  type AppPruebas,
} from './app-pruebas.js';

// I2 — experiencias y banco de preguntas (encargo 06), con la IA falsa:
// nunca se llama a DeepSeek (ADR-045 punto 5). DBA de prueba, por el censo:
// MAT-01-04 tiene 4 evidencias diagnosticables (1 selección única,
// 2 emparejamiento, 3 y 4 ordenamiento); MAT-04-06 no tiene ninguna.
const DBA = 'MAT-01-04';
const SIN_EVIDENCIAS = 'MAT-04-06';

describe('Experiencias y banco (E-18 a E-28)', () => {
  let t: AppPruebas;
  let ia: IaFalsa;
  let docente: string;
  let otro: string;
  let estudiante: string;

  const como = (token: string) => ({ Authorization: `Bearer ${token}` });
  const cuantas = async (tabla: string): Promise<number> =>
    Number(
      (
        (await t.db.query(`SELECT COUNT(*) AS n FROM ${tabla}`)) as {
          n: number;
        }[]
      )[0].n,
    );

  /** Pide la experiencia y espera a que la generación termine. */
  async function crear(nombre = 'Diagnóstico de prueba', token = docente) {
    const res = await t.http
      .post('/experiencias')
      .set(como(token))
      .send({ codigo_dba: DBA, nombre })
      .expect(202);
    expect(res.body.estado).toBe('generando');
    for (let i = 0; i < 200; i++) {
      const g = await t.http
        .get(`/experiencias/generaciones/${res.body.id}`)
        .set(como(token))
        .expect(200);
      if (g.body.estado !== 'generando')
        return g.body as {
          id: string;
          estado: string;
          idExperiencia: number | null;
          mensaje: string | null;
        };
      await new Promise((r) => setTimeout(r, 25));
    }
    throw new Error('la generación no terminó');
  }

  async function crearLista(nombre?: string): Promise<number> {
    const g = await crear(nombre);
    expect(g.estado).toBe('lista');
    return g.idExperiencia!;
  }

  beforeAll(async () => {
    t = await crearApp();
    ia = t.app.get<IaFalsa>(SERVICIO_IA);
    expect(ia).toBeInstanceOf(IaFalsa);
    await borrarCuentas(t.db);
    await t.db.query('DELETE FROM experiencia');
    docente = (await crearCuenta(t, 'doc-i2@x.co', 'docente')).token;
    otro = (await crearCuenta(t, 'otro-i2@x.co', 'docente')).token;
    estudiante = (await crearCuenta(t, 'est-i2@x.co', 'estudiante')).token;
  });
  beforeEach(() => ia.reiniciar());
  afterAll(async () => t.app.close());

  describe('E-19 crear y la generación (ADR-045)', () => {
    it('202 → lista: 12 ítems por evidencia diagnosticable, con su formato, código y servicio', async () => {
      const id = await crearLista();
      // una llamada por evidencia, con el formato de su dictamen (RI-5, RI-19)
      expect(ia.llamadas.map((l) => [l.clave, l.formato]).sort()).toEqual([
        [`${DBA}#1`, 'single_choice'],
        [`${DBA}#2`, 'matching'],
        [`${DBA}#3`, 'ordering'],
        [`${DBA}#4`, 'ordering'],
      ]);
      const [exp] = (await t.db.query(
        'SELECT * FROM experiencia WHERE id_experiencia = ?',
        [id],
      )) as Record<string, unknown>[];
      expect(exp).toMatchObject({
        estado: 'Borrador',
        fecha_publicacion: null,
        servicio_ia: 'deepseek',
        modelo_ia: ia.modelo,
      });
      expect(exp.codigo_invitacion).toMatch(
        /^[ABCDEFGHJKMNPQRSTUVWXYZ23456789]{6}$/,
      ); // RI-3
      const porEvidencia = (await t.db.query(
        'SELECT numero_evidencia AS n, formato, origen, COUNT(*) AS c FROM item WHERE id_experiencia = ? GROUP BY 1, 2, 3 ORDER BY 1',
        [id],
      )) as { n: number; formato: string; origen: string; c: number }[];
      expect(
        porEvidencia.map((f) => [f.n, f.formato, f.origen, Number(f.c)]),
      ).toEqual([
        [1, 'single_choice', 'ia', 12],
        [2, 'matching', 'ia', 12],
        [3, 'ordering', 'ia', 12],
        [4, 'ordering', 'ia', 12],
      ]);
    });

    it('todo o nada: una evidencia inválida dos veces → fallida y nada en la base', async () => {
      const antes = {
        exp: await cuantas('experiencia'),
        item: await cuantas('item'),
        op: await cuantas('opcion'),
      };
      ia.programar(DBA, 3, ['invalida', 'invalida']);
      const g = await crear('No se debe guardar');
      expect(g).toMatchObject({
        estado: 'fallida',
        idExperiencia: null,
        mensaje: 'No se pudieron generar las preguntas. Intenta de nuevo.',
      });
      expect({
        exp: await cuantas('experiencia'),
        item: await cuantas('item'),
        op: await cuantas('opcion'),
      }).toEqual(antes);
      const nombres = (await t.db.query(
        "SELECT 1 FROM experiencia WHERE nombre = 'No se debe guardar'",
      )) as unknown[];
      expect(nombres).toHaveLength(0);
    });

    it('todo o nada al guardar: si la base rechaza un ítem de la última evidencia, no queda nada', async () => {
      const antes = {
        exp: await cuantas('experiencia'),
        ee: await cuantas('experiencia_evidencia'),
        item: await cuantas('item'),
        op: await cuantas('opcion'),
      };
      // las evidencias 1 a 3 se guardan antes; la 4 trae un enunciado que no cabe en TEXT
      ia.programar(DBA, 4, ['no-cabe']);
      const g = await crear('Tampoco se debe guardar');
      expect(g).toMatchObject({ estado: 'fallida', idExperiencia: null });
      expect({
        exp: await cuantas('experiencia'),
        ee: await cuantas('experiencia_evidencia'),
        item: await cuantas('item'),
        op: await cuantas('opcion'),
      }).toEqual(antes);
    });

    it('reintento: una evidencia inválida una vez → se pide de nuevo y queda lista', async () => {
      ia.programar(DBA, 2, ['invalida']);
      const g = await crear();
      expect(g.estado).toBe('lista');
      expect(ia.llamadas.filter((l) => l.clave === `${DBA}#2`)).toHaveLength(2);
    });

    it('un error del servicio, también con un reintento; dos errores → fallida', async () => {
      ia.programar(DBA, 1, ['error']);
      expect((await crear()).estado).toBe('lista');
      ia.programar(DBA, 1, ['error', 'incompleta']);
      expect((await crear()).estado).toBe('fallida');
    });

    it('409 con el texto de V-12 si el DBA no tiene evidencias diagnosticables; 404 si no existe', async () => {
      const res = await t.http
        .post('/experiencias')
        .set(como(docente))
        .send({ codigo_dba: SIN_EVIDENCIAS, nombre: 'x' })
        .expect(409);
      expect(res.body.message).toBe(
        'Este DBA no tiene evidencias que se puedan diagnosticar con preguntas cerradas en esta versión.',
      );
      await t.http
        .post('/experiencias')
        .set(como(docente))
        .send({ codigo_dba: 'MAT-99-99', nombre: 'x' })
        .expect(404);
      expect(ia.llamadas).toHaveLength(0);
    });

    it('400 con un nombre vacío o un código mal escrito', async () => {
      await t.http
        .post('/experiencias')
        .set(como(docente))
        .send({ codigo_dba: DBA, nombre: '   ' })
        .expect(400);
      await t.http
        .post('/experiencias')
        .set(como(docente))
        .send({ codigo_dba: 'mat-1-4', nombre: 'x' })
        .expect(400);
    });

    it('la generación solo la ve quien la pidió', async () => {
      const res = await t.http
        .post('/experiencias')
        .set(como(docente))
        .send({ codigo_dba: DBA, nombre: 'x' })
        .expect(202);
      await t.http
        .get(`/experiencias/generaciones/${res.body.id}`)
        .set(como(otro))
        .expect(403);
      await t.http
        .get('/experiencias/generaciones/no-existe')
        .set(como(docente))
        .expect(404);
    });

    it('solo docentes: un estudiante recibe 403, sin token 401', async () => {
      await t.http
        .post('/experiencias')
        .set(como(estudiante))
        .send({ codigo_dba: DBA, nombre: 'x' })
        .expect(403);
      await t.http.get('/experiencias').expect(401);
    });
  });

  describe('E-18, E-20, E-22: listar, consultar, código', () => {
    it('lista solo las del docente, con filtros por estado y texto', async () => {
      const id = await crearLista('Sumas con decenas');
      const mias = await t.http
        .get('/experiencias')
        .set(como(docente))
        .expect(200);
      expect(mias.body.length).toBeGreaterThan(0);
      expect(mias.body[0]).toMatchObject({
        id,
        nombre: 'Sumas con decenas',
        estado: 'Borrador',
        dba: { codigo: DBA },
        area: { codigo: 'MAT' },
        grado: { numero: 1 },
        estudiantes: 0,
      });
      const filtradas = await t.http
        .get('/experiencias?q=decenas&estado=borrador')
        .set(como(docente))
        .expect(200);
      expect(filtradas.body.map((e: { id: number }) => e.id)).toEqual([id]);
      expect(
        (
          await t.http
            .get('/experiencias?estado=publicada')
            .set(como(docente))
            .expect(200)
        ).body,
      ).toEqual([]);
      expect(
        (await t.http.get('/experiencias').set(como(otro)).expect(200)).body,
      ).toEqual([]);
    });

    it('consulta con lo que falta por evidencia; 403 de otro docente, 404 si no existe', async () => {
      const id = await crearLista();
      const res = await t.http
        .get(`/experiencias/${id}`)
        .set(como(docente))
        .expect(200);
      expect(res.body.evidencias).toHaveLength(4);
      expect(res.body.evidencias[0]).toMatchObject({
        numero: 1,
        formato: 'single_choice',
        activos: 12,
        total: 12,
        faltanParaPublicar: 0,
      });
      expect(res.body).toMatchObject({
        puedePublicar: true,
        respuestas: 0,
        servicioIa: 'deepseek',
      });
      expect(res.body.codigoInvitacion).toBeUndefined();
      await t.http.get(`/experiencias/${id}`).set(como(otro)).expect(403);
      await t.http.get('/experiencias/999999').set(como(docente)).expect(404);
    });

    it('el código: 409 en Borrador; después de publicar, el guardado al crear', async () => {
      const id = await crearLista();
      await t.http
        .get(`/experiencias/${id}/codigo`)
        .set(como(docente))
        .expect(409);
      await t.http
        .post(`/experiencias/${id}/publicar`)
        .set(como(docente))
        .expect(200);
      const res = await t.http
        .get(`/experiencias/${id}/codigo`)
        .set(como(docente))
        .expect(200);
      const [{ codigo }] = (await t.db.query(
        'SELECT codigo_invitacion AS codigo FROM experiencia WHERE id_experiencia = ?',
        [id],
      )) as { codigo: string }[];
      expect(res.body).toEqual({ codigo });
      await t.http
        .get(`/experiencias/${id}/codigo`)
        .set(como(otro))
        .expect(403);
    });
  });

  describe('E-24 a E-28: el banco', () => {
    let id: number;
    beforeAll(async () => {
      id = await crearLista('Banco para editar');
    });

    const banco = async (consulta = '') =>
      (
        await t.http
          .get(`/experiencias/${id}/banco${consulta}`)
          .set(como(docente))
          .expect(200)
      ).body;
    const unItem = async (numero: number) =>
      (await banco()).evidencias.find(
        (e: { numero: number }) => e.numero === numero,
      ).items[0];

    it('trae evidencias en orden, ítems con respuesta correcta y nunca la hipótesis de error', async () => {
      const b = await banco();
      expect(b).toMatchObject({ soloLectura: false, estado: 'Borrador' });
      expect(b.evidencias.map((e: { numero: number }) => e.numero)).toEqual([
        1, 2, 3, 4,
      ]);
      const opciones = b.evidencias[0].items[0].opciones;
      expect(
        opciones.filter((o: { esCorrecta: boolean }) => o.esCorrecta),
      ).toHaveLength(1);
      expect(JSON.stringify(b)).not.toMatch(/hipotesis/i); // ADR-008, ADR-020
      const soloMatching = await banco('?formato=matching');
      expect(
        soloMatching.evidencias.map((e: { numero: number }) => e.numero),
      ).toEqual([2]);
    });

    it('editar: guarda, pasa a editado_docente y valida con RI-4 (400)', async () => {
      const item = await unItem(1);
      const opciones = [
        { texto: 'Doce', es_correcta: true },
        { texto: 'Diez', es_correcta: false },
        { texto: 'Once', es_correcta: false },
      ];
      const res = await t.http
        .patch(`/items/${item.id}`)
        .set(como(docente))
        .send({ enunciado: '¿Cuánto es 7 + 5?', opciones })
        .expect(200);
      expect(res.body).toMatchObject({
        id: item.id,
        enunciado: '¿Cuánto es 7 + 5?',
        origen: 'editado_docente',
        formato: 'single_choice',
      });
      expect(res.body.opciones.map((o: { texto: string }) => o.texto)).toEqual([
        'Doce',
        'Diez',
        'Once',
      ]);
      // dos correctas: la misma regla de la generación
      const mala = await t.http
        .patch(`/items/${item.id}`)
        .set(como(docente))
        .send({
          enunciado: 'x',
          opciones: opciones.map((o) => ({ ...o, es_correcta: true })),
        })
        .expect(400);
      expect(mala.body.message).toContain(
        'En selección única debe haber exactamente una opción correcta.',
      );
      // la hipótesis de error no se recibe del docente
      await t.http
        .patch(`/items/${item.id}`)
        .set(como(docente))
        .send({
          enunciado: 'x',
          opciones: [
            { ...opciones[0] },
            { ...opciones[1], hipotesis_error: 'y' },
          ],
        })
        .expect(400);
      await t.http
        .patch(`/items/${item.id}`)
        .set(como(otro))
        .send({ enunciado: 'x', opciones })
        .expect(403);
      await t.http
        .patch('/items/999999')
        .set(como(docente))
        .send({ enunciado: 'x', opciones })
        .expect(404);
    });

    it('editar un ordenamiento con el orden incompleto → 400', async () => {
      const item = await unItem(3);
      const res = await t.http
        .patch(`/items/${item.id}`)
        .set(como(docente))
        .send({
          enunciado: 'Ordena',
          opciones: [
            { texto: 'a', orden: 1 },
            { texto: 'b', orden: 3 },
          ],
        })
        .expect(400);
      expect(res.body.message).toContain(
        'En ordenamiento los números de orden deben ir de 1 al total, sin repetirse.',
      );
    });

    it('descartar y reincluir: el ítem no se borra y cuenta en los activos', async () => {
      const item = await unItem(2);
      await t.http
        .post(`/items/${item.id}/descartar`)
        .set(como(docente))
        .expect(204);
      let b = await banco();
      expect(b.evidencias[1]).toMatchObject({ activos: 11, total: 12 });
      expect(
        b.evidencias[1].items.find((i: { id: number }) => i.id === item.id)
          .excluido,
      ).toBe(true);
      await t.http
        .post(`/items/${item.id}/reincluir`)
        .set(como(docente))
        .expect(204);
      b = await banco();
      expect(b.evidencias[1]).toMatchObject({ activos: 12, total: 12 });
      await t.http
        .post(`/items/${item.id}/descartar`)
        .set(como(otro))
        .expect(403);
    });

    it('agregar: creado_docente, con el formato del dictamen; 404 si la evidencia no está', async () => {
      const res = await t.http
        .post(`/experiencias/${id}/evidencias/2/items`)
        .set(como(docente))
        .send({
          enunciado: 'Une cada número con su nombre',
          opciones: [
            { texto: '1', grupo: 'izquierda', orden: 1 },
            { texto: '2', grupo: 'izquierda', orden: 2 },
            { texto: 'dos', grupo: 'derecha', orden: 2 },
            { texto: 'uno', grupo: 'derecha', orden: 1 },
          ],
        })
        .expect(201);
      expect(res.body).toMatchObject({
        origen: 'creado_docente',
        formato: 'matching',
        excluido: false,
        numeroEvidencia: 2,
      });
      expect((await banco()).evidencias[1].total).toBe(13);
      const valido = {
        enunciado: 'x',
        opciones: [
          { texto: 'a', orden: 1 },
          { texto: 'b', orden: 2 },
        ],
      };
      await t.http
        .post(`/experiencias/${id}/evidencias/9/items`)
        .set(como(docente))
        .send(valido)
        .expect(404);
      await t.http
        .post(`/experiencias/${id}/evidencias/3/items`)
        .set(como(otro))
        .send(valido)
        .expect(403);
      // un emparejamiento con un solo lado no pasa RI-4
      await t.http
        .post(`/experiencias/${id}/evidencias/2/items`)
        .set(como(docente))
        .send({
          enunciado: 'x',
          opciones: [1, 2, 3, 4].map((n) => ({
            texto: `${n}`,
            grupo: 'izquierda',
            orden: n,
          })),
        })
        .expect(400);
    });
  });

  describe('E-21 publicar y E-23 eliminar', () => {
    it('409 si una evidencia tiene menos de 6 activos; dice cuántos faltan', async () => {
      const id = await crearLista();
      const items = (await t.db.query(
        'SELECT id_item AS id FROM item WHERE id_experiencia = ? AND numero_evidencia = 4 LIMIT 7',
        [id],
      )) as { id: number }[];
      for (const { id: idItem } of items)
        await t.http
          .post(`/items/${idItem}/descartar`)
          .set(como(docente))
          .expect(204);
      const res = await t.http
        .post(`/experiencias/${id}/publicar`)
        .set(como(docente))
        .expect(409);
      expect(res.body.evidencias).toEqual([
        { numero: 4, activos: 5, faltanParaPublicar: 1 },
      ]);
      expect(res.body.message).toContain(
        'a la evidencia 4 le falta 1 ítem activo',
      );
      await t.http
        .post(`/items/${items[0].id}/reincluir`)
        .set(como(docente))
        .expect(204);
      await t.http
        .post(`/experiencias/${id}/publicar`)
        .set(como(otro))
        .expect(403);
      const ok = await t.http
        .post(`/experiencias/${id}/publicar`)
        .set(como(docente))
        .expect(200);
      expect(ok.body.estado).toBe('Publicada');
      expect(ok.body.fechaPublicacion).toBeTruthy();
    });

    it('publicada: no se publica otra vez y el banco queda congelado (409)', async () => {
      const id = await crearLista();
      await t.http
        .post(`/experiencias/${id}/publicar`)
        .set(como(docente))
        .expect(200);
      await t.http
        .post(`/experiencias/${id}/publicar`)
        .set(como(docente))
        .expect(409);
      const [{ id: idItem }] = (await t.db.query(
        'SELECT id_item AS id FROM item WHERE id_experiencia = ? LIMIT 1',
        [id],
      )) as { id: number }[];
      await t.http
        .post(`/items/${idItem}/descartar`)
        .set(como(docente))
        .expect(409);
      await t.http
        .post(`/items/${idItem}/reincluir`)
        .set(como(docente))
        .expect(409);
      const valido = {
        enunciado: 'x',
        opciones: [
          { texto: 'a', orden: 1 },
          { texto: 'b', orden: 2 },
        ],
      };
      await t.http
        .post(`/experiencias/${id}/evidencias/3/items`)
        .set(como(docente))
        .send(valido)
        .expect(409);
      const b = await t.http
        .get(`/experiencias/${id}/banco`)
        .set(como(docente))
        .expect(200);
      expect(b.body.soloLectura).toBe(true);
    });

    it('eliminar borra en cascada evidencias, ítems, opciones, inscripciones y respuestas', async () => {
      const id = await crearLista('Para borrar');
      // Un estudiante inscrito con una respuesta, escrito directo (I3 no es de este encargo)
      const { insertId: idEst } = (await t.db.query(
        "INSERT INTO estudiante (nombres, apellidos) VALUES ('Eva', 'Ruiz')",
      )) as { insertId: number };
      const { insertId: idIns } = (await t.db.query(
        'INSERT INTO inscripcion (id_estudiante, id_experiencia, fecha_union) VALUES (?, ?, NOW())',
        [idEst, id],
      )) as { insertId: number };
      const [{ id: idItem }] = (await t.db.query(
        'SELECT id_item AS id FROM item WHERE id_experiencia = ? LIMIT 1',
        [id],
      )) as { id: number }[];
      await t.db.query(
        'INSERT INTO presentacion (id_inscripcion, id_item, id_experiencia, orden_presentacion, fecha_presentacion) VALUES (?, ?, ?, 1, NOW())',
        [idIns, idItem, id],
      );
      await t.db.query(
        'INSERT INTO respuesta (id_inscripcion, id_item, certeza, fecha_respuesta, correcta) VALUES (?, ?, 3, NOW(), TRUE)',
        [idIns, idItem],
      );
      const detalle = await t.http
        .get(`/experiencias/${id}`)
        .set(como(docente))
        .expect(200);
      expect(detalle.body).toMatchObject({ estudiantes: 1, respuestas: 1 });

      await t.http.delete(`/experiencias/${id}`).set(como(otro)).expect(403);
      await t.http.delete(`/experiencias/${id}`).set(como(docente)).expect(204);
      for (const tabla of [
        'experiencia',
        'experiencia_evidencia',
        'item',
        'inscripcion',
      ]) {
        const filas = (await t.db.query(
          `SELECT 1 FROM ${tabla} WHERE id_experiencia = ?`,
          [id],
        )) as unknown[];
        expect(filas, tabla).toHaveLength(0);
      }
      expect(
        (await t.db.query('SELECT 1 FROM opcion WHERE id_item = ?', [
          idItem,
        ])) as unknown[],
      ).toHaveLength(0);
      expect(
        (await t.db.query('SELECT 1 FROM respuesta WHERE id_inscripcion = ?', [
          idIns,
        ])) as unknown[],
      ).toHaveLength(0);
      // la cuenta del estudiante sigue (CU-15)
      expect(
        (await t.db.query('SELECT 1 FROM estudiante WHERE id_estudiante = ?', [
          idEst,
        ])) as unknown[],
      ).toHaveLength(1);
      await t.http.get(`/experiencias/${id}`).set(como(docente)).expect(404);
    });
  });
});
