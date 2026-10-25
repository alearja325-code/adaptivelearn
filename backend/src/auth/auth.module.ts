import { Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { AuthService } from './auth.service.js';
import { AuthController } from './auth.controller.js';
import { UserModule } from '../user/user.module.js';
import { JwtStrategy } from './strategies/jwt.strategy.js';
import { RecuperacionGuard } from './guards/recuperacion.guard.js';
import { DocentesModule } from '../docentes/docentes.module.js';
import { EstudiantesModule } from '../estudiantes/estudiantes.module.js';

@Module({
  imports: [
    // Importar UserModule para acceder a UserService
    UserModule,

    // Configurar Passport
    PassportModule,

    // Configurar JWT
    JwtModule.registerAsync({
      imports: [ConfigModule],
      useFactory: async (configService: ConfigService) => ({
        secret: configService.get('JWT_SECRET'),
        signOptions: {
          expiresIn: configService.get('JWT_EXPIRATION'),
        },
      }),
      inject: [ConfigService],
    }),

    // Agregado (spec 20): "Elige tu rol" crea la fila en docente o estudiante
    DocentesModule,
    EstudiantesModule,
  ],
  controllers: [AuthController],
  providers: [AuthService, JwtStrategy, RecuperacionGuard],
  exports: [AuthService],
})
export class AuthModule {}
