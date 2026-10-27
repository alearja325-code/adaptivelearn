// Prepara la base de datos del backend desde cero (encargo 03):
//   1. crea la base, si no existe (utf8mb4);
//   2. crea las tablas con sql/001_esquema.sql (generado del modelo relacional);
//   3. carga los datos de referencia con sql/002_datos_referencia.sql;
//   4. carga los 343 DBA y sus evidencias desde
//      data/curriculo-men/catalogo/catalogo_dba.json (encargo 02).
// Lee la conexión de .env (DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD,
// DB_DATABASE). No inventa ni corrige datos: si el catálogo no coincide con
// los documentos de 002 (área o versión), se detiene.
//
// Uso:
//   node scripts/preparar-base.mjs                 base de DB_DATABASE
//   node scripts/preparar-base.mjs --base otra     otra base (las pruebas e2e)
//   node scripts/preparar-base.mjs --borrar        la borra antes (¡todo!)
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import mysql from 'mysql2/promise';

const AQUI = dirname(fileURLToPath(import.meta.url));
const BACKEND = join(AQUI, '..');
const CATALOGO = join(BACKEND, '..', 'data', 'curriculo-men', 'catalogo', 'catalogo_dba.json');

if (existsSync(join(BACKEND, '.env'))) process.loadEnvFile(join(BACKEND, '.env'));

const args = process.argv.slice(2);
const borrar = args.includes('--borrar');
const iBase = args.indexOf('--base');
const base = iBase >= 0 ? args[iBase + 1] : process.env.DB_DATABASE;
if (!base || !/^\w+$/.test(base)) {
  console.error('Falta el nombre de la base (DB_DATABASE en .env, o --base nombre).');
  process.exit(1);
}

const conexion = await mysql.createConnection({
  host: process.env.DB_HOST ?? 'localhost',
  port: Number(process.env.DB_PORT ?? 3306),
  user: process.env.DB_USERNAME,
  password: process.env.DB_PASSWORD ?? '',
  multipleStatements: true,
  charset: 'utf8mb4',
});

try {
  if (borrar) {
    await conexion.query(`DROP DATABASE IF EXISTS \`${base}\``);
    console.log(`base ${base} borrada`);
  }
  await conexion.query(
    `CREATE DATABASE IF NOT EXISTS \`${base}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`,
  );
  await conexion.query(`USE \`${base}\``);

  const [tablas] = await conexion.query("SHOW TABLES LIKE 'credencial'");
  if (tablas.length > 0) {
    console.error(`La base ${base} ya tiene tablas. Para empezar de cero: --borrar.`);
    process.exit(1);
  }

  for (const archivo of ['001_esquema.sql', '002_datos_referencia.sql']) {
    await conexion.query(await readFile(join(BACKEND, 'sql', archivo), 'utf8'));
    console.log(`${archivo}: ejecutado`);
  }

  // ---------------------------------------------------- el catálogo (A12)
  const { dba: dbas } = JSON.parse(await readFile(CATALOGO, 'utf8'));
  const [docs] = await conexion.query('SELECT id_documento, codigo_area, version FROM documento_oficial');
  const documentoDe = new Map(docs.map((d) => [d.codigo_area, d]));

  await conexion.beginTransaction();
  let evidencias = 0;
  for (const d of dbas) {
    const doc = documentoDe.get(d.codigo_area);
    if (!doc || doc.version !== d.documento.version) {
      throw new Error(
        `${d.codigo_dba}: el catálogo dice ${d.codigo_area} ${d.documento.version}, ` +
          `y documento_oficial no tiene ese documento`,
      );
    }
    await conexion.query(
      'INSERT INTO dba (codigo_dba, codigo_area, numero_grado, id_documento, enunciado, ejemplo) ' +
        'VALUES (?, ?, ?, ?, ?, NULL)',
      [d.codigo_dba, d.codigo_area, d.grado, doc.id_documento, d.enunciado],
    );
    // numero_evidencia = la posición en la lista oficial del DBA (ADR-024)
    for (const [i, texto] of d.evidencias.entries()) {
      await conexion.query(
        'INSERT INTO evidencia (codigo_dba, numero_evidencia, enunciado) VALUES (?, ?, ?)',
        [d.codigo_dba, i + 1, texto],
      );
      evidencias += 1;
    }
  }
  await conexion.commit();
  console.log(`catálogo: ${dbas.length} DBA y ${evidencias} evidencias cargados`);

  const dudosos = dbas.filter((d) => d.dudoso.length > 0);
  if (dudosos.length > 0) {
    console.log('DBA marcados como dudosos en el catálogo (encargo 02), cargados tal cual:');
    for (const d of dudosos) console.log(`  ${d.codigo_dba} (página ${d.pagina}): ${d.dudoso.join('; ')}`);
  }
  console.log(`listo: base ${base}`);
} catch (error) {
  await conexion.rollback().catch(() => undefined);
  console.error(`Error: ${error.message}`);
  process.exitCode = 1;
} finally {
  await conexion.end();
}
