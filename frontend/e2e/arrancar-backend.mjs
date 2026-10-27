// Arranca el backend real para las pruebas e2e (Playwright lo llama antes de
// las pruebas, desde playwright.config.ts):
//  1. compila el backend si todavía no está compilado;
//  2. crea la base de pruebas desde cero con el mismo script del equipo
//     (esquema del MR + catálogo) — se BORRA en cada corrida;
//  3. lo arranca en el puerto 3100, con esa base, sin correo (los códigos
//     salen en su consola) y sin Google ni Microsoft;
//  4. copia su consola a e2e/.salida/backend.log, de donde las pruebas leen
//     los códigos de 6 dígitos.
import { execFileSync, execSync, spawn } from 'node:child_process';
import { createWriteStream, existsSync, mkdirSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { BACKEND, LOG_BACKEND, SALIDA, basePruebas } from './comun.mjs';

rmSync(SALIDA, { recursive: true, force: true });
mkdirSync(SALIDA, { recursive: true });
if (!existsSync(join(BACKEND, 'dist', 'main.js'))) {
  execSync('npm run build', { cwd: BACKEND, stdio: 'inherit' });
}
execFileSync(process.execPath, [join(BACKEND, 'scripts', 'preparar-base.mjs'), '--borrar', '--base', basePruebas()], {
  stdio: 'inherit',
});
const log = createWriteStream(LOG_BACKEND, { flags: 'a' });
const hijo = spawn(process.execPath, [join(BACKEND, 'dist', 'main.js')], {
  cwd: BACKEND,
  env: {
    ...process.env,
    PORT: '3100',
    DB_DATABASE: basePruebas(),
    MAIL_HOST: '',
    GOOGLE_CLIENT_ID: '',
    MICROSOFT_CLIENT_ID: '',
    UPLOADS_DIR: join(SALIDA, 'uploads'),
    NO_COLOR: '1',
  },
});
hijo.stdout.pipe(log);
hijo.stderr.pipe(log);
hijo.stdout.pipe(process.stdout);
hijo.stderr.pipe(process.stderr);
hijo.on('exit', (codigo) => process.exit(codigo ?? 0));
for (const senal of ['SIGINT', 'SIGTERM']) process.on(senal, () => hijo.kill(senal));
