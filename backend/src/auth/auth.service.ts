import {
  BadRequestException,
  ConflictException,
  ForbiddenException,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { InjectDataSource } from '@nestjs/typeorm';
import { DataSource, IsNull } from 'typeorm';
import { randomInt } from 'node:crypto';
import * as bcrypt from 'bcrypt';
import { UserService, mensajeOtroProveedor } from '../user/user.service.js';
import { User, type Rol } from '../user/entities/user.entity.js';
import { DocentesService } from '../docentes/docentes.service.js';
import { EstudiantesService } from '../estudiantes/estudiantes.service.js';
import { LoginDto } from './dto/login.dto.js';
import { RegisterDto } from './dto/register.dto.js';
import { VerificarCorreoDto } from './dto/verificar-correo.dto.js';
import { ReenviarCodigoDto } from './dto/reenviar-codigo.dto.js';
import { ElegirRolDto } from './dto/elegir-rol.dto.js';
import { SolicitarRecuperacionDto } from './dto/solicitar-recuperacion.dto.js';
import { VerificarRecuperacionDto } from './dto/verificar-recuperacion.dto.js';
import { NuevaContrasenaDto } from './dto/nueva-contrasena.dto.js';
import { JwtPayload } from './interfaces/jwt-payload.interface.js';
import { RecuperacionPayload } from './interfaces/recuperacion-payload.interface.js';

const CREDENCIALES_INCORRECTAS = 'Correo o contraseña incorrectos.'; // spec 17, 2.6
const CODIGO_INCORRECTO = 'Código incorrecto. Revisa que esté bien escrito.'; // spec 18, 2.4

const MINUTOS_VALIDEZ_CODIGO = 10;
const SEGUNDOS_COOLDOWN_REENVIO = 30; // spec 18, 2.5
const MAX_INTENTOS_CODIGO = 5;
const MAX_INTENTOS_LOGIN = 5;
const MINUTOS_BLOQUEO_LOGIN = 15;
const SEGUNDOS_VALIDEZ_TOKEN_RECUPERACION = 15 * 60;

// crypto y no Math.random: Math.random no es impredecible, y este código
// es lo único que protege la recuperación de contraseña.
function generarCodigoVerificacion(): string {
  return randomInt(0, 1_000_000).toString().padStart(6, '0');
}

function puedeReenviar(user: User): boolean {
  return (
    !user.codigoUltimoEnvio ||
    Date.now() - user.codigoUltimoEnvio.getTime() >= SEGUNDOS_COOLDOWN_REENVIO * 1000
  );
}

@Injectable()
export class AuthService {
  constructor(
    private readonly userService: UserService,
    private readonly jwtService: JwtService,
    private readonly docentesService: DocentesService,
    private readonly estudiantesService: EstudiantesService,
    @InjectDataSource() private readonly dataSource: DataSource,
  ) {}

  /**
   * Registrar un nuevo usuario
   * Crea el usuario y retorna un token JWT (igual que la guía).
   * Además envía el código de verificación de correo (spec 18).
   */
  async register(registerDto: RegisterDto) {
    const user = await this.userService.create(registerDto);

    await this.enviarNuevoCodigo(user);

    const token = await this.generateToken(user.id, user.email, user.role);

    return { user, token };
  }

  /**
   * Login de usuario
   * Valida credenciales y retorna un token JWT
   */
  async login(loginDto: LoginDto) {
    const { email, password } = loginDto;

    // Buscar usuario por email (incluye password)
    const user = await this.userService.findOneByEmail(email);

    if (!user) {
      throw new UnauthorizedException(CREDENCIALES_INCORRECTAS);
    }

    // Cuenta creada con Google/Microsoft: no tiene contraseña (spec 17, 2.6)
    if (user.proveedor !== 'correo') {
      throw new UnauthorizedException(mensajeOtroProveedor(user.proveedor));
    }

    // Bloqueo temporal tras varios intentos fallidos. Mismo mensaje
    // genérico: uno distinto confirmaría que la cuenta existe.
    if (user.bloqueadoHasta && user.bloqueadoHasta.getTime() > Date.now()) {
      throw new UnauthorizedException(CREDENCIALES_INCORRECTAS);
    }

    // Comparar contraseñas
    const isPasswordValid =
      user.password !== null && (await bcrypt.compare(password, user.password));

    if (!isPasswordValid) {
      await this.registrarLoginFallido(user);
      throw new UnauthorizedException(CREDENCIALES_INCORRECTAS);
    }

    if (user.intentosLogin > 0) {
      await this.userService.actualizarIntentosLogin(user.id, 0, null);
    }

    // Generar el token JWT
    const token = await this.generateToken(user.id, user.email, user.role);

    return { user, token };
  }

  /**
   * Generar token JWT
   * Crea un token con el payload especificado
   */
  private async generateToken(userId: number, email: string, role: Rol | null): Promise<string> {
    const payload: JwtPayload = {
      sub: userId,
      email,
      role,
    };

    // Firmar y retornar el token
    return await this.jwtService.signAsync(payload);
  }

  // ------------------------------------------------------------------
  // Agregado por las specs de MODESEC (fuera de la guía)
  // ------------------------------------------------------------------

  /**
   * Spec 18, flujo 1 — verificar el correo con la sesión ya iniciada.
   */
  async verificarCorreo(sesion: User, dto: VerificarCorreoDto) {
    const user = await this.userService.findOneByEmail(sesion.email);

    // 400 y no 401: la sesión es válida, lo incorrecto es el código escrito.
    if (!user || !(await this.validarCodigo(user, dto.codigo))) {
      throw new BadRequestException(CODIGO_INCORRECTO);
    }

    await this.userService.marcarCorreoVerificado(user.id);

    return { user: await this.userService.findOne(user.id) };
  }

  /**
   * Spec 18, sección 2.5 — "Reenviar". La cuenta regresiva de 30 s de la
   * pantalla se vuelve a exigir acá, porque este endpoint se puede llamar
   * directo. Responde igual exista o no la cuenta (anti-enumeración).
   */
  async reenviarCodigo(dto: ReenviarCodigoDto) {
    const user = await this.userService.findOneByEmail(dto.email);

    if (user && user.proveedor === 'correo' && puedeReenviar(user)) {
      await this.enviarNuevoCodigo(user);
    }

    return { ok: true };
  }

  /**
   * Spec 20 — "Elige tu rol". Crea la fila en docente o estudiante (nunca
   * las 2) y devuelve un token nuevo con el rol ya incluido. Exige correo
   * verificado (spec 18) y perfil completo (spec 19).
   */
  async elegirRol(sesion: User, dto: ElegirRolDto) {
    if (sesion.role !== null) {
      throw new ConflictException('Esta cuenta ya tiene un rol asignado.');
    }
    if (!sesion.emailVerificado) {
      throw new ForbiddenException('Primero verifica tu correo.');
    }
    if (!sesion.nombres || !sesion.apellidos) {
      throw new BadRequestException('Falta completar el perfil antes de elegir un rol.');
    }

    const datos = {
      nombre: `${sesion.nombres} ${sesion.apellidos}`,
      correo: sesion.email,
      avatarUrl: sesion.avatarUrl,
    };

    // Transacción: crear la fila y enlazarla a la credencial pasan juntas o
    // ninguna. El UPDATE es condicional (solo si aún no hay rol), así 2
    // peticiones simultáneas no pueden asignar 2 roles.
    await this.dataSource.transaction(async (manager) => {
      const enlace =
        dto.role === 'docente'
          ? { idDocente: (await this.docentesService.crear(manager, datos)).id }
          : { idEstudiante: (await this.estudiantesService.crear(manager, datos)).id };

      const result = await manager.update(
        User,
        { id: sesion.id, idDocente: IsNull(), idEstudiante: IsNull() },
        enlace,
      );

      if (!result.affected) {
        throw new ConflictException('Esta cuenta ya tiene un rol asignado.');
      }
    });

    const user = await this.userService.findOne(sesion.id);
    const token = await this.generateToken(user.id, user.email, user.role);

    return { user, token };
  }

  /**
   * Spec 21 — pedir el código de recuperación. Responde EXACTAMENTE igual
   * si la cuenta no existe, si es solo de Google/Microsoft o si existe con
   * contraseña: ninguno de esos casos debe poder distinguirse desde afuera.
   */
  async solicitarRecuperacion(dto: SolicitarRecuperacionDto) {
    const user = await this.userService.findOneByEmail(dto.email);

    if (user && user.proveedor === 'correo' && puedeReenviar(user)) {
      await this.enviarNuevoCodigo(user);
    }

    return { ok: true };
  }

  /**
   * Spec 18, flujo 2 — verificar el código de recuperación. Devuelve un
   * token corto que solo sirve para POST /auth/nueva-contrasena.
   */
  async verificarRecuperacion(dto: VerificarRecuperacionDto) {
    const user = await this.userService.findOneByEmail(dto.email);

    if (!user || user.proveedor !== 'correo' || !(await this.validarCodigo(user, dto.codigo))) {
      throw new UnauthorizedException(CODIGO_INCORRECTO);
    }

    await this.userService.marcarCorreoVerificado(user.id);

    const payload: RecuperacionPayload = { sub: user.id, proposito: 'nueva-contrasena' };
    const token = await this.jwtService.signAsync(payload, {
      expiresIn: SEGUNDOS_VALIDEZ_TOKEN_RECUPERACION,
    });

    return { token };
  }

  /**
   * Spec 22 — guardar la contraseña nueva. No abre sesión: la persona vuelve
   * a "Iniciar sesión" (spec 17, 2.6, mensaje de confirmación).
   */
  async nuevaContrasena(userId: number, dto: NuevaContrasenaDto) {
    const user = await this.userService.findOne(userId).catch(() => null);

    if (!user) {
      throw new UnauthorizedException('Token de recuperación inválido o vencido.');
    }

    const passwordHash = await bcrypt.hash(dto.password, 10);
    await this.userService.actualizarPassword(user.id, passwordHash);

    return { ok: true };
  }

  /**
   * Un código es válido si existe, no venció y no se agotaron los intentos.
   * Cada intento equivocado cuenta: con 5 como máximo, adivinar 1 código
   * entre 1.000.000 deja de ser viable.
   */
  private async validarCodigo(user: User, codigo: string): Promise<boolean> {
    const vigente =
      user.codigoVerificacion !== null &&
      user.codigoExpiraEn !== null &&
      user.codigoExpiraEn.getTime() > Date.now() &&
      user.intentosCodigo < MAX_INTENTOS_CODIGO;

    if (!vigente) {
      return false;
    }

    if (user.codigoVerificacion === codigo) {
      return true;
    }

    await this.userService.registrarIntentoCodigoFallido(user.id);
    return false;
  }

  private async registrarLoginFallido(user: User): Promise<void> {
    const intentos = user.intentosLogin + 1;

    if (intentos >= MAX_INTENTOS_LOGIN) {
      const hasta = new Date(Date.now() + MINUTOS_BLOQUEO_LOGIN * 60_000);
      await this.userService.actualizarIntentosLogin(user.id, 0, hasta);
    } else {
      await this.userService.actualizarIntentosLogin(user.id, intentos, null);
    }
  }

  private async enviarNuevoCodigo(user: User): Promise<void> {
    const codigo = generarCodigoVerificacion();
    const expiraEn = new Date(Date.now() + MINUTOS_VALIDEZ_CODIGO * 60_000);

    await this.userService.guardarCodigoVerificacion(user.id, codigo, expiraEn);

    // Modo desarrollo (decidido el 2026-09-17): sin envío real de correo;
    // el código se imprime en la terminal del servidor.
    console.log(`[DEV] Código de verificación para ${user.email}: ${codigo}`);
  }
}
