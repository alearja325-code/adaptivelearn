import { NestFactory } from '@nestjs/core';
import type { NestExpressApplication } from '@nestjs/platform-express';
import { AppModule } from './app.module.js';
import { configurarApp } from './configurar-app.js';

async function bootstrap(): Promise<void> {
  const app = await NestFactory.create<NestExpressApplication>(AppModule);

  // ValidationPipe y ClassSerializerInterceptor globales, CORS y /uploads
  configurarApp(app);

  // Guía: process.env.PORT ?? 3000. Con || también un PORT vacío (el de
  // .env.example) usa el 3000.
  const port: number = Number(process.env.PORT || 3000);
  await app.listen(port);
  console.log(`🚀 Servidor corriendo en http://localhost:${port}`);
}
void bootstrap();
