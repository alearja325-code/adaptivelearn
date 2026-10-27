import { defineConfig } from '@playwright/test';

// Pruebas de punta a punta en un navegador real (encargo 04 §6.2), contra el
// backend real y MySQL. Levantan su propio backend (puerto 3100, base de
// datos de pruebas que se borra y se recrea, sin MAIL_HOST: los códigos salen
// en su consola, que se guarda en e2e/.salida/backend.log) y su propio
// frontend (puerto 5174). La conexión a MySQL sale de backend/.env.
export const PUERTO_BACKEND = 3100;
export const PUERTO_FRONTEND = 5174;

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  workers: 1,
  timeout: 90_000,
  expect: { timeout: 10_000 },
  reporter: [['list']],
  use: {
    baseURL: `http://localhost:${PUERTO_FRONTEND}`,
    viewport: { width: 1440, height: 900 },
    trace: 'retain-on-failure',
  },
  webServer: [
    {
      command: 'node e2e/arrancar-backend.mjs',
      url: `http://localhost:${PUERTO_BACKEND}/auth/profile`,
      reuseExistingServer: false,
      timeout: 60_000,
    },
    {
      command: `npx vite --port ${PUERTO_FRONTEND} --strictPort`,
      url: `http://localhost:${PUERTO_FRONTEND}`,
      reuseExistingServer: false,
      env: { VITE_API_URL: `http://localhost:${PUERTO_BACKEND}`, VITE_GOOGLE_CLIENT_ID: '', VITE_MICROSOFT_CLIENT_ID: '' },
      timeout: 60_000,
    },
  ],
});
