import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule, TypeOrmModuleOptions } from '@nestjs/typeorm';
import { ScheduleModule } from '@nestjs/schedule';
import { UserModule } from './user/user.module.js';
import { AuthModule } from './auth/auth.module.js';
import { CorreoModule } from './correo/correo.module.js';
import { CatalogoModule } from './catalogo/catalogo.module.js';
import { LimpiezaModule } from './limpieza/limpieza.module.js';
import { ExampleController } from './example/example.controller.js';

@Module({
  imports: [
    // Configuración de variables de entorno
    // isGlobal: true hace que ConfigService esté disponible en toda la app
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
    }),

    // Configuración de TypeORM con MySQL
    // useFactory permite inyectar ConfigService para leer variables de entorno
    TypeOrmModule.forRootAsync({
      inject: [ConfigService],
      useFactory: (configService: ConfigService): TypeOrmModuleOptions => ({
        type: 'mysql',
        // getOrThrow lanza un error claro si la variable no existe en .env
        host: configService.getOrThrow<string>('DB_HOST'),
        port: Number(configService.getOrThrow<string>('DB_PORT')),
        username: configService.getOrThrow<string>('DB_USERNAME'),
        password: configService.get<string>('DB_PASSWORD', ''),
        database: configService.getOrThrow<string>('DB_DATABASE'),
        // Carga automáticamente las entidades registradas con forFeature()
        autoLoadEntities: true,
        // Guía: true. Acá false: las tablas son las del modelo relacional
        // (sql/001_esquema.sql, generado del MR) y synchronize podría
        // alterarlas por su cuenta. La propia guía dice "solo en desarrollo".
        synchronize: false,
      }),
    }),

    // Tareas programadas: la limpieza nocturna de ADR-039
    ScheduleModule.forRoot(),

    // Módulos de la aplicación
    CorreoModule,
    UserModule,
    AuthModule,
    CatalogoModule,
    LimpiezaModule,
  ],
  // Ejemplo de uso de Guards y Decoradores (sección 6 de la guía)
  controllers: [ExampleController],
})
export class AppModule {}
