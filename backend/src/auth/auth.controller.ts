import { Controller, Post, Body, Get, UseGuards, Request } from '@nestjs/common';
import { AuthService } from './auth.service.js';
import { LoginDto } from './dto/login.dto.js';
import { RegisterDto } from './dto/register.dto.js';
import { VerificarCorreoDto } from './dto/verificar-correo.dto.js';
import { ReenviarCodigoDto } from './dto/reenviar-codigo.dto.js';
import { ElegirRolDto } from './dto/elegir-rol.dto.js';
import { SolicitarRecuperacionDto } from './dto/solicitar-recuperacion.dto.js';
import { VerificarRecuperacionDto } from './dto/verificar-recuperacion.dto.js';
import { NuevaContrasenaDto } from './dto/nueva-contrasena.dto.js';
import { JwtAuthGuard } from './guards/jwt-auth.guard.js';
import { RecuperacionGuard } from './guards/recuperacion.guard.js';
import { GetUser } from './decorators/get-user.decorator.js';
import { User } from '../user/entities/user.entity.js';

@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  /**
   * POST /auth/register
   * Registrar un nuevo usuario
   */
  @Post('register')
  async register(@Body() registerDto: RegisterDto) {
    return await this.authService.register(registerDto);
  }

  /**
   * POST /auth/login
   * Iniciar sesión
   */
  @Post('login')
  async login(@Body() loginDto: LoginDto) {
    return await this.authService.login(loginDto);
  }

  /**
   * GET /auth/profile
   * Obtener perfil del usuario autenticado
   * Ruta protegida con JWT
   */
  @UseGuards(JwtAuthGuard)
  @Get('profile')
  getProfile(@Request() req: { user: User }) {
    // req.user contiene la información del usuario autenticado
    return {
      user: req.user,
    };
  }

  // ------------------------------------------------------------------
  // Agregado por las specs de MODESEC 18 a 22 (fuera de la guía)
  // ------------------------------------------------------------------

  // Spec 18, flujo 1 — verificar el correo (con sesión iniciada).
  @UseGuards(JwtAuthGuard)
  @Post('verificar-correo')
  verificarCorreo(@GetUser() user: User, @Body() dto: VerificarCorreoDto) {
    return this.authService.verificarCorreo(user, dto);
  }

  // Spec 18, sección 2.5 — reenviar el código (sirve para los 2 flujos).
  @Post('reenviar-codigo')
  reenviarCodigo(@Body() dto: ReenviarCodigoDto) {
    return this.authService.reenviarCodigo(dto);
  }

  // Spec 20 — elegir rol (con sesión iniciada). El perfil de la spec 19 se
  // completa con PATCH /users/:id.
  @UseGuards(JwtAuthGuard)
  @Post('elegir-rol')
  elegirRol(@GetUser() user: User, @Body() dto: ElegirRolDto) {
    return this.authService.elegirRol(user, dto);
  }

  // Spec 21 — pedir código de recuperación (sin sesión).
  @Post('recuperar-contrasena')
  solicitarRecuperacion(@Body() dto: SolicitarRecuperacionDto) {
    return this.authService.solicitarRecuperacion(dto);
  }

  // Spec 18, flujo 2 — verificar el código de recuperación.
  @Post('recuperar-contrasena/verificar')
  verificarRecuperacion(@Body() dto: VerificarRecuperacionDto) {
    return this.authService.verificarRecuperacion(dto);
  }

  // Spec 22 — guardar la contraseña nueva (con el token de recuperación).
  @UseGuards(RecuperacionGuard)
  @Post('nueva-contrasena')
  nuevaContrasena(@Request() req: { idRecuperacion: number }, @Body() dto: NuevaContrasenaDto) {
    return this.authService.nuevaContrasena(req.idRecuperacion, dto);
  }
}
