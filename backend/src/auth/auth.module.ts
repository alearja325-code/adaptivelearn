import { Module } from '@nestjs/common';
import { JwtModule, JwtModuleOptions } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { AuthService } from './auth.service.js';
import { AuthController } from './auth.controller.js';
import { UserModule } from '../user/user.module.js';
import { JwtStrategy } from './strategies/jwt.strategy.js';
import { RecuperacionGuard } from './guards/recuperacion.guard.js';
import { CodigoService } from './codigo.service.js';
import { CodigoVerificacion } from './entities/codigo-verificacion.entity.js';
import { VERIFICADORES, type Verificadores } from './proveedores/proveedor-identidad.js';
import { VerificadorGoogle, VerificadorMicrosoft } from './proveedores/verificadores-jwks.js';

@Module({
  imports: [
    // Importar UserModule para acceder a UserService
    UserModule,
    // El repositorio de los códigos de verificación (ADR-039)
    TypeOrmModule.forFeature([CodigoVerificacion]),
    // Configurar Passport con 'jwt' como estrategia por defecto
    PassportModule.register({ defaultStrategy: 'jwt' }),
    // Configurar JWT leyendo el secreto y la expiración del .env
    JwtModule.registerAsync({
      inject: [ConfigService],
      useFactory: (configService: ConfigService): JwtModuleOptions => ({
        secret: configService.getOrThrow<string>('JWT_SECRET'),
        signOptions: {
          // Segundos; las variables de entorno siempre llegan como string
          expiresIn: Number(configService.getOrThrow<string>('JWT_EXPIRATION')),
        },
      }),
    }),
  ],
  controllers: [AuthController],
  providers: [
    AuthService,
    JwtStrategy,
    RecuperacionGuard,
    CodigoService,
    // Google y Microsoft (E-04, E-05): sin su identificador en .env quedan
    // "no configurados" y la ruta responde 503. Las pruebas los reemplazan.
    {
      provide: VERIFICADORES,
      inject: [ConfigService],
      useFactory: (configService: ConfigService): Verificadores => ({
        google: new VerificadorGoogle(configService.get<string>('GOOGLE_CLIENT_ID')),
        microsoft: new VerificadorMicrosoft(configService.get<string>('MICROSOFT_CLIENT_ID')),
      }),
    },
  ],
  exports: [AuthService, CodigoService],
})
export class AuthModule {}
