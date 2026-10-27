import {
  Controller,
  Post,
  Body,
  Get,
  Patch,
  UseGuards,
  UseInterceptors,
  UploadedFile,
  HttpCode,
  HttpStatus,
  Req,
} from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { AuthService } from './auth.service.js';
import { LoginDto } from './dto/login.dto.js';
import { RegisterDto } from './dto/register.dto.js';
import { VerificarCorreoDto } from './dto/verificar-correo.dto.js';
import { ReenviarCodigoDto } from './dto/reenviar-codigo.dto.js';
import { ProveedorTokenDto } from './dto/proveedor-token.dto.js';
import { ElegirRolDto } from './dto/elegir-rol.dto.js';
import { EditarPerfilDto } from './dto/editar-perfil.dto.js';
import { SolicitarRecuperacionDto } from './dto/solicitar-recuperacion.dto.js';
import { VerificarRecuperacionDto } from './dto/verificar-recuperacion.dto.js';
import { NuevaContrasenaDto } from './dto/nueva-contrasena.dto.js';
import { JwtAuthGuard } from './guards/jwt-auth.guard.js';
import { RecuperacionGuard } from './guards/recuperacion.guard.js';
import { GetUser } from './decorators/get-user.decorator.js';
import { AuthResponse } from './interfaces/auth-response.interface.js';
import { User } from '../user/entities/user.entity.js';
import { OPCIONES_FOTO, type ArchivoSubido } from './foto.js';

// Rutas de la guía (register, login, profile) y las del acceso de
// AdaptiveLearn (`20` §3). El número E-xx es el del catálogo de endpoints.
@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  /**
   * POST /auth/register — E-01
   * Registrar un nuevo usuario (responde 201 Created)
   */
  @Post('register')
  register(@Body() registerDto: RegisterDto): Promise<AuthResponse> {
    return this.authService.register(registerDto);
  }

  /**
   * POST /auth/login — E-07
   * Iniciar sesión (responde 200 OK, no se crea ningún recurso)
   */
  @Post('login')
  @HttpCode(HttpStatus.OK)
  login(@Body() loginDto: LoginDto): Promise<AuthResponse> {
    return this.authService.login(loginDto);
  }

  /**
   * GET /auth/profile — E-11
   * Obtener perfil del usuario autenticado. Ruta protegida con JWT; acepta
   * también el token de una cuenta sin rol (prueba 3 de la guía).
   */
  @UseGuards(JwtAuthGuard)
  @Get('profile')
  getProfile(@GetUser() user: User): { user: User } {
    return { user };
  }

  /**
   * PATCH /auth/profile — E-12
   * Editar el propio perfil (CU-09): nombres, apellidos y foto, en
   * multipart/form-data. No es PATCH /users/:id, que en la guía es de admin.
   */
  @UseGuards(JwtAuthGuard)
  @UseInterceptors(FileInterceptor('foto', OPCIONES_FOTO))
  @Patch('profile')
  editarPerfil(
    @GetUser() user: User,
    @Body() dto: EditarPerfilDto,
    @UploadedFile() foto?: ArchivoSubido,
  ): Promise<{ user: User }> {
    return this.authService.editarPerfil(user, dto, foto);
  }

  /** POST /auth/verificar-correo — E-02 (ventana 015) */
  @UseGuards(JwtAuthGuard)
  @Post('verificar-correo')
  @HttpCode(HttpStatus.OK)
  verificarCorreo(@GetUser() user: User, @Body() dto: VerificarCorreoDto): Promise<{ user: User }> {
    return this.authService.verificarCorreo(user, dto);
  }

  /** POST /auth/reenviar-codigo — E-03 (ventana 015, «Reenviar») */
  @Post('reenviar-codigo')
  reenviarCodigo(@Body() dto: ReenviarCodigoDto): Promise<{ ok: true }> {
    return this.authService.reenviarCodigo(dto);
  }

  /** POST /auth/google — E-04 */
  @Post('google')
  @HttpCode(HttpStatus.OK)
  google(@Body() dto: ProveedorTokenDto): Promise<AuthResponse> {
    return this.authService.entrarConProveedor('google', dto.token);
  }

  /** POST /auth/microsoft — E-05 */
  @Post('microsoft')
  @HttpCode(HttpStatus.OK)
  microsoft(@Body() dto: ProveedorTokenDto): Promise<AuthResponse> {
    return this.authService.entrarConProveedor('microsoft', dto.token);
  }

  /**
   * POST /auth/elegir-rol — E-06 (ventanas 016 y 017)
   * Rol, nombres, apellidos y foto opcional, en multipart/form-data.
   */
  @UseGuards(JwtAuthGuard)
  @UseInterceptors(FileInterceptor('foto', OPCIONES_FOTO))
  @Post('elegir-rol')
  elegirRol(
    @GetUser() user: User,
    @Body() dto: ElegirRolDto,
    @UploadedFile() foto?: ArchivoSubido,
  ): Promise<AuthResponse> {
    return this.authService.elegirRol(user, dto, foto);
  }

  /** POST /auth/recuperar-contrasena — E-08 (ventana 018) */
  @Post('recuperar-contrasena')
  @HttpCode(HttpStatus.ACCEPTED)
  solicitarRecuperacion(@Body() dto: SolicitarRecuperacionDto): Promise<{ ok: true }> {
    return this.authService.solicitarRecuperacion(dto);
  }

  /** POST /auth/recuperar-contrasena/verificar — E-09 (ventana 015) */
  @Post('recuperar-contrasena/verificar')
  @HttpCode(HttpStatus.OK)
  verificarRecuperacion(@Body() dto: VerificarRecuperacionDto): Promise<{ token: string }> {
    return this.authService.verificarRecuperacion(dto);
  }

  /** POST /auth/nueva-contrasena — E-10 (con el token de recuperación) */
  @UseGuards(RecuperacionGuard)
  @Post('nueva-contrasena')
  @HttpCode(HttpStatus.NO_CONTENT)
  nuevaContrasena(
    @Req() req: { idRecuperacion: number },
    @Body() dto: NuevaContrasenaDto,
  ): Promise<void> {
    return this.authService.nuevaContrasena(req.idRecuperacion, dto);
  }
}
