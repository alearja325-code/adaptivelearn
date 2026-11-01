import { ClassSerializerInterceptor, ValidationPipe } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import type { NestExpressApplication } from '@nestjs/platform-express';
import { resolve } from 'node:path';

/**
 * La configuración global de la guía (sección 5), en una función para que
 * main.ts y las pruebas de punta a punta usen exactamente la misma.
 */
export function configurarApp(app: NestExpressApplication): void {
  // Configurar ValidationPipe globalmente
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true, // Elimina propiedades no definidas en el DTO
      forbidNonWhitelisted: true, // Lanza error si hay propiedades no permitidas
      transform: true, // Transforma los datos al tipo definido en el DTO
    }),
  );

  // Aplicar @Exclude() de class-transformer en todas las respuestas
  app.useGlobalInterceptors(new ClassSerializerInterceptor(app.get(Reflector)));

  // Las fotos de perfil (RF-01-05) se sirven desde /uploads
  app.useStaticAssets(resolve(process.env.UPLOADS_DIR || 'uploads'), { prefix: '/uploads/' });

  // CORS: solo la dirección del frontend puede llamar al backend desde un
  // navegador. CORS_ORIGIN en .env (varias, separadas por comas); por defecto,
  // el frontend de desarrollo de Vite.
  app.enableCors({ origin: origenesPermitidos(process.env.CORS_ORIGIN) });
}

/** Direcciones que pueden llamar al backend desde un navegador (CORS). */
export function origenesPermitidos(valor: string | undefined): string[] {
  const lista = (valor ?? '')
    .split(',')
    .map((o) => o.trim().replace(/\/$/, ''))
    .filter((o) => o.length > 0);
  return lista.length > 0 ? lista : ['http://localhost:5173'];
}
