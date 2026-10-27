import { existsSync } from 'node:fs';
import { join } from 'node:path';

const ENV = join(import.meta.dirname, '..', '.env');

/**
 * Nombre de la base de las pruebas e2e. Se BORRA y se recrea en cada
 * corrida, así que nunca es la de desarrollo: DB_DATABASE_PRUEBAS, o el
 * nombre de DB_DATABASE seguido de _pruebas.
 */
export function nombreBasePruebas(): string {
  if (existsSync(ENV)) process.loadEnvFile(ENV);
  const nombre = process.env.DB_DATABASE_PRUEBAS || `${process.env.DB_DATABASE ?? 'adaptivelearn'}_pruebas`;
  if (nombre === process.env.DB_DATABASE) {
    throw new Error('DB_DATABASE_PRUEBAS no puede ser la misma base de DB_DATABASE: se borra.');
  }
  return nombre;
}
