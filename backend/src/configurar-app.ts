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

  // Habilitar CORS (opcional, para desarrollo con frontend)
  app.enableCors();
}
