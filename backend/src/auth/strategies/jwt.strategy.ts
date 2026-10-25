import { Injectable, UnauthorizedException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { UserService } from '../../user/user.service.js';
import { JwtPayload } from '../interfaces/jwt-payload.interface.js';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(
    private readonly userService: UserService,
    private readonly configService: ConfigService,
  ) {
    super({
      // Extraer el token del header Authorization como Bearer token
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      // No ignorar la expiración del token
      ignoreExpiration: false,
      // Secreto para verificar el token. Guía: get(). Con los tipos actuales
      // de passport-jwt, get() no compila (puede ser undefined); getOrThrow
      // además impide arrancar el servidor si falta JWT_SECRET en el .env.
      secretOrKey: configService.getOrThrow('JWT_SECRET'),
    });
  }

  /**
   * Método que se ejecuta automáticamente después de validar el token
   * El payload ya viene decodificado por Passport
   */
  async validate(payload: JwtPayload & { proposito?: string }) {
    // El token de recuperación (spec 22) está firmado con el mismo secreto,
    // pero no es una sesión: no debe abrir rutas protegidas.
    if (payload.proposito) {
      throw new UnauthorizedException();
    }

    const { sub: id } = payload;

    // Buscar el usuario en la base de datos. Guía: findOne lanza 404 si no
    // existe; para un token inválido la respuesta correcta es 401.
    const user = await this.userService.findOne(id).catch(() => null);

    if (!user) {
      throw new UnauthorizedException();
    }

    // Guía: acá revisa isActive. Ninguna spec define desactivar cuentas,
    // así que ese campo no existe en este modelo.

    // Retornar el usuario (se agregará a request.user)
    return user;
  }
}
