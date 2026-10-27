import { CanActivate, ExecutionContext, Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import type { RecuperacionPayload } from '../interfaces/jwt-payload.interface.js';

/**
 * Guard para "Nueva contraseña" (E-10, ventana 018): exige el token corto que
 * entrega POST /auth/recuperar-contrasena/verificar. Quien recupera su
 * contraseña no tiene sesión, por eso no sirve JwtAuthGuard. Deja el id de
 * la credencial en request.idRecuperacion.
 */
@Injectable()
export class RecuperacionGuard implements CanActivate {
  constructor(private readonly jwtService: JwtService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context
      .switchToHttp()
      .getRequest<{ headers: { authorization?: string }; idRecuperacion?: number }>();
    const authHeader = request.headers.authorization;
    const token = authHeader?.startsWith('Bearer ') ? authHeader.slice(7) : undefined;

    if (!token) {
      throw new UnauthorizedException('Falta el token de recuperación.');
    }

    let payload: RecuperacionPayload;
    try {
      payload = await this.jwtService.verifyAsync<RecuperacionPayload>(token);
    } catch {
      throw new UnauthorizedException('Token de recuperación inválido o vencido.');
    }

    // Un token de sesión normal no sirve acá, aunque tenga firma válida.
    if (payload.proposito !== 'nueva-contrasena') {
      throw new UnauthorizedException('Token de recuperación inválido o vencido.');
    }

    request.idRecuperacion = payload.sub;
    return true;
  }
}
