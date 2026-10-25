import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UserModule } from './user/user.module.js';
import { AuthModule } from './auth/auth.module.js';
import { ExampleController } from './example.controller.js';

@Module({
  imports: [
    // Configuración de variables de entorno
    // isGlobal: true hace que ConfigModule esté disponible en toda la app
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
    }),

    // Configuración de TypeORM con MySQL (MariaDB es compatible)
    // useFactory permite inyectar ConfigService para leer variables de entorno
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: (configService: ConfigService) => ({
        type: 'mysql',
        host: configService.get('DB_HOST'),
        port: +configService.get('DB_PORT'),
        username: configService.get('DB_USERNAME'),
        password: configService.get('DB_PASSWORD'),
        database: configService.get('DB_DATABASE'),
        // Guía: __dirname. Este proyecto es ESM (NestJS 12), donde __dirname
        // no existe; import.meta.dirname es su equivalente.
        entities: [import.meta.dirname + '/**/*.entity{.ts,.js}'],
        // Guía: true. Acá false: las tablas siguen el modelo relacional ya
        // aprobado y se crean con sql/001 y sql/002; synchronize podría
        // alterarlas por su cuenta. La propia guía lo advierte.
        synchronize: false,
      }),
      inject: [ConfigService],
    }),

    // Módulos de la aplicación
    UserModule,
    AuthModule,
  ],
  // Ejemplo de uso de Guards y Decoradores (sección 6 de la guía)
  controllers: [ExampleController],
})
export class AppModule {}
