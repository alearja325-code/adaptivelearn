// Ayudas de las pruebas e2e: correos únicos, leer el código de la consola del
// backend, capturas y los pasos que se repiten.
import { expect, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { crc32, deflateSync } from 'node:zlib';
import { FRONTEND, LOG_BACKEND } from './comun.mjs';

export const CLAVE = 'Password123';

let contador = 0;
export function correoNuevo(nombre: string): string {
  contador += 1;
  return `${nombre}.${Date.now()}.${contador}@prueba.co`;
}

/** Los códigos que el backend escribió en su consola para un correo, en orden */
function codigosDe(correo: string): string[] {
  const log = readFileSync(LOG_BACKEND, 'utf8');
  const escapado = correo.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return [...log.matchAll(new RegExp(`\\(${escapado}\\): (\\d{6})`, 'g'))].map((m) => m[1]);
}

/** Espera a que aparezca el código número `n` (1 = el primero) de ese correo */
export async function leerCodigo(correo: string, n = 1): Promise<string> {
  await expect.poll(() => codigosDe(correo).length, { timeout: 10_000 }).toBeGreaterThanOrEqual(n);
  return codigosDe(correo)[n - 1];
}

export async function escribirCodigo(page: Page, codigo: string): Promise<void> {
  await page.getByLabel('Dígito 1').click();
  await page.keyboard.type(codigo);
}

/** Capturas para que Alejandro las revise contra las specs (encargo 04 §6.3) */
export async function captura(page: Page, nombre: string): Promise<void> {
  await page.waitForTimeout(150);
  await page.screenshot({ path: join(FRONTEND, 'capturas', `${nombre}.png`) });
}

/** Una foto PNG de prueba: un cuadro de 64×64 de un solo color, armado aquí */
export function fotoPng(): { name: string; mimeType: string; buffer: Buffer } {
  const lado = 64;
  const fila = Buffer.concat([Buffer.from([0]), Buffer.alloc(lado * 3, 0x80)]);
  const datos = deflateSync(Buffer.concat(Array.from({ length: lado }, () => fila)));
  const bloque = (tipo: string, cuerpo: Buffer) => {
    const largo = Buffer.alloc(4);
    largo.writeUInt32BE(cuerpo.length);
    const tc = Buffer.concat([Buffer.from(tipo), cuerpo]);
    const crc = Buffer.alloc(4);
    crc.writeUInt32BE(crc32(tc));
    return Buffer.concat([largo, tc, crc]);
  };
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(lado, 0);
  ihdr.writeUInt32BE(lado, 4);
  ihdr.set([8, 2, 0, 0, 0], 8);
  const png = Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    bloque('IHDR', ihdr),
    bloque('IDAT', datos),
    bloque('IEND', Buffer.alloc(0)),
  ]);
  return { name: 'foto.png', mimeType: 'image/png', buffer: png };
}

/** Crear cuenta → verificar → completar perfil → elegir rol: una cuenta lista */
export async function crearCuentaCompleta(page: Page, correo: string, rol: 'Docente' | 'Estudiante'): Promise<void> {
  await page.goto('/crear-cuenta');
  await page.getByLabel('Correo electrónico').fill(correo);
  await page.getByLabel('Contraseña', { exact: true }).fill(CLAVE);
  await page.getByRole('button', { name: 'Crear cuenta' }).click();
  await expect(page.getByRole('heading', { name: 'Verifica tu correo' })).toBeVisible();
  await escribirCodigo(page, await leerCodigo(correo));
  await page.getByRole('button', { name: 'Verificar' }).click();
  await expect(page.getByRole('heading', { name: 'Completa tu perfil' })).toBeVisible();
  await page.getByLabel('Nombres').fill('Ana María');
  await page.getByLabel('Apellidos').fill('Pérez Gómez');
  await page.getByRole('button', { name: 'Continuar' }).click();
  await page.getByRole('radio', { name: `Soy ${rol}` }).click();
  await page.getByRole('button', { name: 'Continuar' }).click();
  await expect(page.getByRole('heading', { name: 'Mis experiencias' })).toBeVisible();
}
