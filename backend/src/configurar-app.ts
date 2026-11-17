import { ClassSerializerInterceptor, ValidationPipe } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import type { NestExpressApplication } from '@nestjs/platform-express';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
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

  // Documentación interactiva (20-catalogo-endpoints.md §8): /docs para
  // probar cada endpoint desde el navegador, y /docs-json con la
  // especificación OpenAPI. Para las rutas con sesión: «Authorize» y pegar
  // el token que devuelven login o register.
  configurarDocumentacion(app);
}

/** Swagger en /docs (y el JSON en /docs-json). */
export function configurarDocumentacion(app: NestExpressApplication): void {
  const config = new DocumentBuilder()
    .setTitle('AdaptiveLearn API')
    .setDescription(
      'Backend de AdaptiveLearn: diagnóstico adaptativo por evidencia sobre los DBA del MEN. ' +
        'I1 acceso, I2 experiencias y banco de preguntas, I3 diagnóstico, I4 reporte. ' +
        'Catálogo completo de endpoints, con sus reglas: ' +
        'docs/modesec/fase-3-diseno-computacional/20-catalogo-endpoints.md. ' +
        'Para las rutas con sesión, use «Authorize» con el token de /auth/login.',
    )
    .setVersion('1.0')
    .addBearerAuth()
    .addSecurityRequirements('bearer')
    .build();
  const documento = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('docs', app, documento, {
    jsonDocumentUrl: 'docs-json',
    swaggerOptions: { persistAuthorization: true, tagsSorter: 'alpha' },
  });
}

/** Direcciones que pueden llamar al backend desde un navegador (CORS). */
export function origenesPermitidos(valor: string | undefined): string[] {
  const lista = (valor ?? '')
    .split(',')
    .map((o) => o.trim().replace(/\/$/, ''))
    .filter((o) => o.length > 0);
  return lista.length > 0 ? lista : ['http://localhost:5173'];
}
