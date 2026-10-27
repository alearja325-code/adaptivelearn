import { execFileSync } from 'node:child_process';
import { join } from 'node:path';
import { nombreBasePruebas } from './base-pruebas.js';

// globalSetup de vitest: una vez por corrida, la base de pruebas desde cero,
// con el mismo script que usa el equipo (esquema del MR + catálogo).
export default function setup(): void {
  execFileSync(
    'node',
    [join(import.meta.dirname, '..', 'scripts', 'preparar-base.mjs'), '--borrar', '--base', nombreBasePruebas()],
    { stdio: 'inherit' },
  );
}
