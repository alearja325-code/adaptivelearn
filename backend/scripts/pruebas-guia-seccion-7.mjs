// Corre las 6 pruebas de la sección 7 de la guía del docente v2 (y su tabla
// de respuestas esperadas) contra el servidor ENCENDIDO (npm run start:dev),
// e imprime cada petición con su respuesta, para el informe de comparación
// (docs/cursos/dse-2-203453/backend-auth-informe-guia.md).
//
// Antes borra todas las cuentas (sql/borrar-cuentas.sql), para que los ids
// empiecen en 1 como en la guía. SOLO para desarrollo.
//
// Uso:  node scripts/pruebas-guia-seccion-7.mjs [http://localhost:3000]
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import mysql from 'mysql2/promise';

const BACKEND = join(dirname(fileURLToPath(import.meta.url)), '..');
if (existsSync(join(BACKEND, '.env'))) process.loadEnvFile(join(BACKEND, '.env'));
const URL_BASE = process.argv[2] ?? `http://localhost:${process.env.PORT || 3000}`;

const db = await mysql.createConnection({
  host: process.env.DB_HOST,
  port: Number(process.env.DB_PORT),
  user: process.env.DB_USERNAME,
  password: process.env.DB_PASSWORD ?? '',
  database: process.env.DB_DATABASE,
  multipleStatements: true,
});
await db.query(await readFile(join(BACKEND, 'sql', 'borrar-cuentas.sql'), 'utf8'));

const corto = (token) => (token ? `${token.slice(0, 36)}…` : token);
let fallas = 0;

async function pedir(titulo, metodo, ruta, { token, cuerpo, espera } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(URL_BASE + ruta, {
    method: metodo,
    headers,
    ...(cuerpo && { body: JSON.stringify(cuerpo) }),
  });
  const texto = await res.text();
  const json = texto ? JSON.parse(texto) : null;
  const mostrado = json && json.token ? { ...json, token: corto(json.token) } : json;
  const ok = res.status === espera;
  if (!ok) fallas += 1;
  console.log(`\n### ${titulo}`);
  console.log(`${metodo} ${ruta}${token ? `\nAuthorization: Bearer ${corto(token)}` : ''}`);
  if (cuerpo) console.log(JSON.stringify(cuerpo, null, 2));
  console.log(`→ ${res.status} ${res.statusText}   (esperado: ${espera}) ${ok ? 'OK' : 'DISTINTO'}`);
  if (mostrado !== null) console.log(JSON.stringify(mostrado, null, 2));
  return json;
}

console.log(`Servidor: ${URL_BASE} · ${new Date().toISOString()}`);

const r1 = await pedir('1. Registrar un nuevo usuario', 'POST', '/auth/register', {
  cuerpo: { email: 'usuario@example.com', password: 'Password123', fullName: 'Juan Pérez' },
  espera: 201,
});
const r2 = await pedir('2. Iniciar sesión', 'POST', '/auth/login', {
  cuerpo: { email: 'usuario@example.com', password: 'Password123' },
  espera: 200,
});
await pedir('3. Obtener perfil (ruta protegida)', 'GET', '/auth/profile', { token: r2.token, espera: 200 });

const sql = "UPDATE credencial SET es_admin = 1 WHERE correo = 'usuario@example.com';";
const [res4] = await db.query(sql);
console.log(`\n### 4. Convertir un usuario en administrador\n${sql}\n→ ${res4.affectedRows} fila`);
const r4 = await pedir('4. (después) Iniciar sesión otra vez', 'POST', '/auth/login', {
  cuerpo: { email: 'usuario@example.com', password: 'Password123' },
  espera: 200,
});
await pedir('5. Crear usuario (requiere admin)', 'POST', '/users', {
  token: r4.token,
  cuerpo: { email: 'otro@example.com', password: 'Password456', fullName: 'María García' },
  espera: 201,
});
await pedir('6. Listar todos los usuarios (requiere admin)', 'GET', '/users', { token: r4.token, espera: 200 });

console.log('\n## Tabla de respuestas esperadas');
await pedir('Sin token', 'GET', '/users', { espera: 401 });
await pedir('Token vencido o inválido', 'GET', '/auth/profile', { token: 'eyJ.no.valido', espera: 401 });
const otro = await pedir('(login del usuario normal)', 'POST', '/auth/login', {
  cuerpo: { email: 'otro@example.com', password: 'Password456' },
  espera: 200,
});
await pedir('Token válido pero rol user en /users', 'GET', '/users', { token: otro.token, espera: 403 });
await pedir('Email ya registrado', 'POST', '/auth/register', {
  cuerpo: { email: 'otro@example.com', password: 'Password456', fullName: 'Otra' },
  espera: 409,
});
await pedir('Datos inválidos en el body', 'POST', '/auth/register', {
  cuerpo: { email: 'no-es-un-correo', password: 'password123' },
  espera: 400,
});
await pedir('Usuario con ese ID no existe (admin)', 'GET', '/users/999', { token: r4.token, espera: 404 });
await pedir('Borrar un usuario (admin)', 'DELETE', '/users/2', { token: r4.token, espera: 204 });

void r1;
await db.end();
console.log(`\nResultado: ${fallas === 0 ? 'todas las respuestas son las esperadas' : `${fallas} DISTINTAS`}`);
process.exitCode = fallas === 0 ? 0 : 1;
