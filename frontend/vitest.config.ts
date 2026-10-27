import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

// Pruebas unitarias: componentes en un DOM simulado (jsdom), sin backend
export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/pruebas/preparar.ts'],
    include: ['src/**/*.test.{ts,tsx}'],
    css: false,
  },
});
