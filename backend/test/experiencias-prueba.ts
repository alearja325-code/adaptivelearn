import type { DataSource } from 'typeorm';
import type { AppPruebas } from './app-pruebas.js';

// Ayudante de las pruebas de I3 e I4 (encargo 07): arma experiencias con su
// banco insertándolas DIRECTO en la base de pruebas, sin los endpoints de I2
// (encargo 06, en paralelo). Respeta el esquema del MR: RI-4 (mínimos por
// formato), RI-14 (6 activos por evidencia), RI-16 (fecha de publicación).

export type Formato = 'single_choice' | 'matching' | 'ordering';

export interface OpcionPrueba {
  id: number;
  esCorrecta: boolean | null;
  orden: number | null;
  grupo: 'izquierda' | 'derecha' | null;
}

export interface ItemPrueba {
  id: number;
  numeroEvidencia: number;
  formato: Formato;
  excluido: boolean;
  opciones: OpcionPrueba[];
}

export interface ExperienciaPrueba {
  id: number;
  codigo: string;
  codigoDba: string;
  evidencias: number[];
  items: Map<number, ItemPrueba>;
}

/** Texto que solo existe en `opcion.hipotesis_error`: si aparece en una respuesta HTTP, se filtró. */
export const HIPOTESIS = 'HIPOTESIS-SECRETA-NO-DEBE-SALIR';

const ALFABETO = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'; // RI-3: sin 0 O 1 I L

function codigoAlAzar(): string {
  return Array.from(
    { length: 6 },
    () => ALFABETO[Math.floor(Math.random() * ALFABETO.length)],
  ).join('');
}

/** El id de docente o estudiante de una cuenta (la sesión trae el de la credencial). */
export async function idDeRol(
  db: DataSource,
  email: string,
): Promise<{ idDocente: number | null; idEstudiante: number | null }> {
  const [c] = await db.query(
    'SELECT id_docente, id_estudiante FROM credencial WHERE correo = ?',
    [email],
  );
  return { idDocente: c.id_docente, idEstudiante: c.id_estudiante };
}

export async function renombrarEstudiante(
  db: DataSource,
  email: string,
  nombres: string,
  apellidos: string,
): Promise<void> {
  const { idEstudiante } = await idDeRol(db, email);
  await db.query(
    'UPDATE estudiante SET nombres = ?, apellidos = ? WHERE id_estudiante = ?',
    [nombres, apellidos, idEstudiante],
  );
}

/** Vacía las tablas de experiencias y diagnóstico (el catálogo no se toca). */
export async function borrarExperiencias(db: DataSource): Promise<void> {
  await db.query('SET FOREIGN_KEY_CHECKS = 0');
  for (const t of [
    'respuesta_opcion',
    'respuesta',
    'resultado',
    'presentacion',
    'inscripcion',
    'opcion',
    'item',
    'experiencia_evidencia',
    'experiencia',
  ]) {
    await db.query(`TRUNCATE TABLE ${t}`);
  }
  await db.query('SET FOREIGN_KEY_CHECKS = 1');
}

/**
 * Una experiencia con `evidencias` evidencias de un DBA real del catálogo y
 * `porEvidencia` ítems de un formato (6 por defecto, el mínimo de RI-14).
 * Con `excluidos`, además, ese número de ítems descartados por evidencia.
 */
export async function crearExperiencia(
  db: DataSource,
  idDocente: number,
  o: {
    formato?: Formato;
    evidencias?: number;
    porEvidencia?: number;
    excluidos?: number;
    estado?: 'Publicada' | 'Borrador';
  } = {},
): Promise<ExperienciaPrueba> {
  const formato = o.formato ?? 'single_choice';
  const cuantas = o.evidencias ?? 3;
  const estado = o.estado ?? 'Publicada';
  const [dba] = await db.query(
    'SELECT codigo_dba FROM evidencia GROUP BY codigo_dba HAVING COUNT(*) >= ? ORDER BY codigo_dba LIMIT 1',
    [cuantas],
  );
  const numeros: number[] = (
    await db.query(
      'SELECT numero_evidencia FROM evidencia WHERE codigo_dba = ? ORDER BY numero_evidencia LIMIT ?',
      [dba.codigo_dba, cuantas],
    )
  ).map((f: { numero_evidencia: number }) => f.numero_evidencia);

  const codigo = codigoAlAzar();
  const r = await db.query(
    `INSERT INTO experiencia (id_docente, codigo_dba, nombre, estado, fecha_creacion, fecha_publicacion, codigo_invitacion, servicio_ia, modelo_ia)
     VALUES (?, ?, ?, ?, NOW(), ?, ?, 'deepseek', 'modelo-de-prueba')`,
    [
      idDocente,
      dba.codigo_dba,
      `Experiencia ${formato} ${codigo}`,
      estado,
      estado === 'Publicada' ? new Date() : null,
      codigo,
    ],
  );
  const id: number = r.insertId;
  const items = new Map<number, ItemPrueba>();
  // Se insertan en orden inverso: el orden oficial lo debe poner el backend (ADR-024).
  for (const n of [...numeros].reverse()) {
    await db.query(
      'INSERT INTO experiencia_evidencia (id_experiencia, codigo_dba, numero_evidencia) VALUES (?, ?, ?)',
      [id, dba.codigo_dba, n],
    );
    const total = (o.porEvidencia ?? 6) + (o.excluidos ?? 0);
    for (let k = 0; k < total; k++) {
      const excluido = k >= (o.porEvidencia ?? 6);
      const it = await db.query(
        'INSERT INTO item (id_experiencia, codigo_dba, numero_evidencia, enunciado, formato, origen, excluido) VALUES (?, ?, ?, ?, ?, ?, ?)',
        [
          id,
          dba.codigo_dba,
          n,
          `Pregunta ${k + 1} de la evidencia ${n}`,
          formato,
          'ia',
          excluido,
        ],
      );
      const item: ItemPrueba = {
        id: it.insertId,
        numeroEvidencia: n,
        formato,
        excluido,
        opciones: [],
      };
      for (const op of opcionesDe(formato)) {
        const ro = await db.query(
          'INSERT INTO opcion (id_item, texto, orden, es_correcta, grupo, hipotesis_error) VALUES (?, ?, ?, ?, ?, ?)',
          [
            item.id,
            op.texto,
            op.orden,
            op.esCorrecta,
            op.grupo,
            op.esCorrecta === false || (op.grupo !== null && op.orden === null)
              ? HIPOTESIS
              : null,
          ],
        );
        item.opciones.push({
          id: ro.insertId,
          esCorrecta: op.esCorrecta,
          orden: op.orden,
          grupo: op.grupo,
        });
      }
      items.set(item.id, item);
    }
  }
  return { id, codigo, codigoDba: dba.codigo_dba, evidencias: numeros, items };
}

function opcionesDe(
  formato: Formato,
): (Omit<OpcionPrueba, 'id'> & { texto: string })[] {
  switch (formato) {
    case 'single_choice': // RI-4: al menos 2; la 2.ª es la correcta
      return [false, true, false, false].map((c, i) => ({
        texto: `Opción ${i + 1}`,
        esCorrecta: c,
        orden: null,
        grupo: null,
      }));
    case 'ordering': // orden = posición correcta, guardadas en orden correcto
      return [1, 2, 3, 4].map((p) => ({
        texto: `Paso ${p}`,
        esCorrecta: null,
        orden: p,
        grupo: null,
      }));
    case 'matching': // 3 parejas y una derecha sin pareja (RI-4: al menos 2 por lado)
      return [
        ...[1, 2, 3].flatMap((p) => [
          {
            texto: `Término ${p}`,
            esCorrecta: null,
            orden: p,
            grupo: 'izquierda' as const,
          },
          {
            texto: `Definición ${p}`,
            esCorrecta: null,
            orden: p,
            grupo: 'derecha' as const,
          },
        ]),
        {
          texto: 'Definición sobrante',
          esCorrecta: null,
          orden: null,
          grupo: 'derecha' as const,
        },
      ];
  }
}

/** La selección que manda el estudiante, correcta o no, según el formato. */
export function seleccion(
  item: ItemPrueba,
  correcta: boolean,
): { id_opcion: number; valor_dado?: number }[] {
  const ops = item.opciones;
  switch (item.formato) {
    case 'single_choice': {
      const op = ops.find((o) => (o.esCorrecta === true) === correcta)!;
      return [{ id_opcion: op.id }];
    }
    case 'ordering': {
      const posiciones = ops.map((o) => o.orden!);
      if (!correcta)
        [posiciones[0], posiciones[1]] = [posiciones[1], posiciones[0]]; // dos posiciones cambiadas
      return ops.map((o, i) => ({
        id_opcion: o.id,
        valor_dado: posiciones[i],
      }));
    }
    case 'matching': {
      const izq = ops.filter((o) => o.grupo === 'izquierda');
      const der = izq.map((l) =>
        ops.find((o) => o.grupo === 'derecha' && o.orden === l.orden)!,
      );
      if (!correcta) [der[0], der[1]] = [der[1], der[0]]; // un par cruzado: todo o nada
      return izq.flatMap((l, i) => [
        { id_opcion: l.id, valor_dado: i + 1 },
        { id_opcion: der[i].id, valor_dado: i + 1 },
      ]);
    }
  }
}

/** Qué hace el estudiante con la k-ésima pregunta (desde 0) de la evidencia `ev`; null = sale sin responderla. */
export type Plan = (
  ev: number,
  k: number,
) => { correcta: boolean; certeza: number } | null;

export interface Toma {
  /** Todas las respuestas HTTP que recibió el estudiante (para revisar que nada se filtre). */
  cuerpos: unknown[];
  /** Las evidencias de cada pregunta presentada, en orden. */
  secuencia: number[];
  terminada: boolean;
}

/** Toma el diagnóstico por HTTP, como lo haría el frontend, siguiendo un plan. */
export async function tomar(
  t: AppPruebas,
  token: string,
  idInscripcion: number,
  exp: ExperienciaPrueba,
  plan: Plan,
): Promise<Toma> {
  const toma: Toma = { cuerpos: [], secuencia: [], terminada: false };
  const respondidas = new Map<number, number>();
  for (let vuelta = 0; vuelta < 200; vuelta++) {
    const sig = await t.http
      .post(`/inscripciones/${idInscripcion}/presentaciones`)
      .set('Authorization', `Bearer ${token}`);
    if (![200, 201].includes(sig.status))
      throw new Error(
        `E-32 respondió ${sig.status}: ${JSON.stringify(sig.body)}`,
      );
    toma.cuerpos.push(sig.body);
    if (sig.body.pregunta === null) {
      toma.terminada = true;
      return toma;
    }
    const item = exp.items.get(sig.body.pregunta.id_item)!;
    toma.secuencia.push(item.numeroEvidencia);
    const k = respondidas.get(item.numeroEvidencia) ?? 0;
    const paso = plan(item.numeroEvidencia, k);
    if (!paso) return toma;
    const res = await t.http
      .post(`/inscripciones/${idInscripcion}/respuestas`)
      .set('Authorization', `Bearer ${token}`)
      .send({
        id_item: item.id,
        opciones: seleccion(item, paso.correcta),
        certeza: paso.certeza,
      });
    if (res.status !== 201)
      throw new Error(
        `E-33 respondió ${res.status}: ${JSON.stringify(res.body)}`,
      );
    toma.cuerpos.push(res.body);
    respondidas.set(item.numeroEvidencia, k + 1);
  }
  throw new Error('El diagnóstico no terminó en 200 vueltas');
}
