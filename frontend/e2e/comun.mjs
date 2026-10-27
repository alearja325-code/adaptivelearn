// Lo que comparten la preparación y el arranque del backend de las pruebas e2e.
import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

export const FRONTEND = join(dirname(fileURLToPath(import.meta.url)), '..');
export const BACKEND = join(FRONTEND, '..', 'backend');
export const SALIDA = join(FRONTEND, 'e2e', '.salida');
export const LOG_BACKEND = join(SALIDA, 'backend.log');

/** La base de las pruebas del frontend: se BORRA en cada corrida. */
export function basePruebas() {
  if (existsSync(join(BACKEND, '.env'))) process.loadEnvFile(join(BACKEND, '.env'));
  const nombre = process.env.DB_DATABASE_E2E_FRONTEND || `${process.env.DB_DATABASE ?? 'adaptivelearn'}_e2e_frontend`;
  if (nombre === process.env.DB_DATABASE) throw new Error('La base de las pruebas no puede ser la de desarrollo: se borra.');
  return nombre;
}
