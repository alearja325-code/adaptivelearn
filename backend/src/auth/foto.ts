import { BadRequestException } from '@nestjs/common';
import { randomUUID } from 'node:crypto';
import { mkdir, unlink, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

// RF-01-05: foto JPG o PNG, máximo 5 MB.
export const MAX_BYTES_FOTO = 5 * 1024 * 1024;

export interface ArchivoSubido {
  buffer: Buffer;
  size: number;
}

/** Opciones de multer: la foto llega en memoria, con el límite de 5 MB. */
export const OPCIONES_FOTO = { limits: { fileSize: MAX_BYTES_FOTO, files: 1 } };

/**
 * El tipo se decide por los primeros bytes del archivo, no por su nombre ni
 * por el tipo que declara el navegador: los dos se pueden falsificar.
 */
export function extensionFoto(buffer: Buffer): 'jpg' | 'png' | null {
  if (buffer.length >= 3 && buffer[0] === 0xff && buffer[1] === 0xd8 && buffer[2] === 0xff) {
    return 'jpg';
  }
  const png = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  if (buffer.length >= 8 && png.every((b, i) => buffer[i] === b)) {
    return 'png';
  }
  return null;
}

/**
 * Guarda la foto en la carpeta de subidas con un nombre al azar y devuelve
 * su dirección pública (/uploads/...). Si el archivo no es JPG ni PNG,
 * responde 400 y no guarda nada (CU-04 2a, CU-09 3a: la foto no cambia).
 * El recorte cuadrado (RF-01-05) lo hace la pantalla al mostrarla.
 */
export async function guardarFoto(archivo: ArchivoSubido, carpeta: string): Promise<string> {
  const ext = extensionFoto(archivo.buffer);
  if (!ext) {
    throw new BadRequestException('La foto debe ser JPG o PNG.');
  }
  await mkdir(carpeta, { recursive: true });
  const nombre = `${randomUUID()}.${ext}`;
  await writeFile(join(carpeta, nombre), archivo.buffer);
  return `/uploads/${nombre}`;
}

/** Borra una foto guardada (si la operación que la usaba falló). */
export async function borrarFoto(url: string | null, carpeta: string): Promise<void> {
  if (!url?.startsWith('/uploads/')) return;
  await unlink(join(carpeta, url.slice('/uploads/'.length))).catch(() => undefined);
}
