import { defineConfig } from 'vitest/config';
import tsconfigPaths from 'vite-tsconfig-paths';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { nombreBasePruebas } from './test/base-pruebas.js';

// Pruebas de punta a punta contra un MySQL real (encargo 03): la conexión
// sale de .env, pero la base es otra, que se borra y se recrea en cada corrida.
export default defineConfig({
  plugins: [tsconfigPaths()],
  test: {
    globals: true,
    root: './',
    include: ['**/*.e2e-spec.ts'],
    globalSetup: ['./test/preparar-base-e2e.ts'],
    // Todos los archivos comparten la base: uno a la vez
    fileParallelism: false,
    testTimeout: 20_000,
    hookTimeout: 60_000,
    env: {
      DB_DATABASE: nombreBasePruebas(),
      UPLOADS_DIR: join(tmpdir(), 'adaptivelearn-pruebas-uploads'),
      // Sin correo real ni proveedores reales: las pruebas los simulan
      MAIL_HOST: '',
      GOOGLE_CLIENT_ID: '',
      MICROSOFT_CLIENT_ID: '',
    },
  },
});
