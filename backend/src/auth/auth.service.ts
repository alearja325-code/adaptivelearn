import {
  BadRequestException,
  ConflictException,
  ForbiddenException,
  HttpException,
  HttpStatus,
  Inject,
  Injectable,
  Logger,
  ServiceUnavailableException,
  UnauthorizedException,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { JwtService } from '@nestjs/jwt';
import { InjectDataSource } from '@nestjs/typeorm';
import { DataSource, IsNull } from 'typeorm';
import * as bcrypt from 'bcrypt';
import { UserService, mensajeCorreoRegistrado } from '../user/user.service.js';
import { User } from '../user/entities/user.entity.js';
import { Docente } from '../user/entities/docente.entity.js';
import { Estudiante } from '../user/entities/estudiante.entity.js';
import { CorreoService } from '../correo/correo.service.js';
import { CodigoService, type ResultadoCodigo } from './codigo.service.js';
import { LoginDto } from './dto/login.dto.js';
import { RegisterDto } from './dto/register.dto.js';
import { VerificarCorreoDto } from './dto/verificar-correo.dto.js';
import { ReenviarCodigoDto } from './dto/reenviar-codigo.dto.js';
import { ElegirRolDto } from './dto/elegir-rol.dto.js';
import { EditarPerfilDto } from './dto/editar-perfil.dto.js';
import { SolicitarRecuperacionDto } from './dto/solicitar-recuperacion.dto.js';
import { VerificarRecuperacionDto } from './dto/verificar-recuperacion.dto.js';
import { NuevaContrasenaDto } from './dto/nueva-contrasena.dto.js';
import { JwtPayload, RecuperacionPayload } from './interfaces/jwt-payload.interface.js';
import { AuthResponse } from './interfaces/auth-response.interface.js';
import {
  NOMBRE_PROVEEDOR,
  VERIFICADORES,
  type ProveedorExterno,
  type Verificadores,
} from './proveedores/proveedor-identidad.js';
import { borrarFoto, guardarFoto, type ArchivoSubido } from './foto.js';

// Guía: «Credenciales inválidas». Ventana 014: el mismo mensaje genérico,
// sin decir qué dato falló (RF-01-07).
const CREDENCIALES_INVALIDAS = 'Credenciales inválidas';
const MAX_INTENTOS_LOGIN = 5;
const MINUTOS_BLOQUEO_LOGIN = 15;
const SEGUNDOS_TOKEN_RECUPERACION = 15 * 60;

// Ventana 015: qué responder a cada resultado de un código
const MENSAJE_CODIGO: Record<Exclude<ResultadoCodigo, 'ok'>, string> = {
  incorrecto: 'Código incorrecto. Revisa que esté bien escrito.',
  vencido: 'El código venció. Pide uno nuevo.',
  inexistente: 'El código venció. Pide uno nuevo.',
  agotado: 'Demasiados intentos con este código. Pide uno nuevo.',
};

function errorDeCodigo(resultado: Exclude<ResultadoCodigo, 'ok'>): HttpException {
  return resultado === 'agotado'
    ? new HttpException(MENSAJE_CODIGO.agotado, HttpStatus.TOO_MANY_REQUESTS)
    : new BadRequestException(MENSAJE_CODIGO[resultado]);
}

@Injectable()
export class AuthService {
  private readonly logger = new Logger(AuthService.name);
  private readonly carpetaFotos: string;

  constructor(
    private readonly userService: UserService,
    private readonly jwtService: JwtService,
    private readonly codigoService: CodigoService,
    private readonly correoService: CorreoService,
    @Inject(VERIFICADORES) private readonly verificadores: Verificadores,
    @InjectDataSource() private readonly dataSource: DataSource,
    configService: ConfigService,
  ) {
    this.carpetaFotos = configService.get<string>('UPLOADS_DIR') || 'uploads';
  }

  /**
   * Registrar un nuevo usuario
   * Crea el usuario y retorna un token JWT (guía). Además envía el código
   * para verificar el correo (RF-01-03, nota R5).
   */
  async register(registerDto: RegisterDto): Promise<AuthResponse> {
    // Crear el usuario usando el servicio de usuarios
    const user: User = await this.userService.create(registerDto);
    await this.enviarCodigo(user, 'verificar_correo');
    return await this.buildAuthResponse(user);
  }

  /**
   * Login de usuario
   * Valida credenciales y retorna un token JWT. Si la cuenta no eligió rol,
   * el token es de rol 'user' y la pantalla retoma el registro (ADR-035).
   */
  async login(loginDto: LoginDto): Promise<AuthResponse> {
    const { email, password } = loginDto;

    // Buscar usuario por email (incluye password); puede ser null
    const user: User | null = await this.userService.findOneByEmail(email);

    // Verificar si el usuario existe
    if (!user) {
      throw new UnauthorizedException(CREDENCIALES_INVALIDAS);
    }

    // Cuenta de Google o Microsoft: no tiene contraseña (RF-01-04)
    if (user.proveedor !== 'correo') {
      throw new ConflictException(
        `Esta cuenta entra con ${NOMBRE_PROVEEDOR[user.proveedor]}. Continúa con ese botón.`,
      );
    }

    // Bloqueo de 15 minutos tras 5 intentos fallidos. Mismo mensaje
    // genérico: uno distinto confirmaría que la cuenta existe.
    if (user.bloqueadoHasta && user.bloqueadoHasta.getTime() > Date.now()) {
      throw new UnauthorizedException(CREDENCIALES_INVALIDAS);
    }

    // Comparar contraseñas
    const isPasswordValid: boolean =
      user.password !== null && (await bcrypt.compare(password, user.password));

    if (!isPasswordValid) {
      await this.registrarLoginFallido(user);
      throw new UnauthorizedException(CREDENCIALES_INVALIDAS);
    }

    if (user.intentosLogin > 0 || user.bloqueadoHasta) {
      await this.userService.actualizarIntentosLogin(user.id, 0, null);
    }

    return await this.buildAuthResponse(user);
  }

  /**
   * Generar token JWT con el payload del usuario
   */
  private async generateToken(user: User): Promise<string> {
    const payload: JwtPayload = {
      sub: user.id,
      email: user.email,
      role: user.role,
      idDocente: user.idDocente,
      idEstudiante: user.idEstudiante,
    };
    // Firmar y retornar el token
    return await this.jwtService.signAsync(payload);
  }

  /**
   * Construir la respuesta de register/login (sin la contraseña)
   */
  private async buildAuthResponse(user: User): Promise<AuthResponse> {
    const token: string = await this.generateToken(user);
    return {
      user: {
        id: user.id,
        email: user.email,
        fullName: user.fullName,
        role: user.role,
      },
      token,
    };
  }

  // ------------------------------------------------------------------
  // El resto del acceso de AdaptiveLearn (`20` §3, E-02 a E-12)
  // ------------------------------------------------------------------

  /** E-02 — verificar el correo con el código (CU-03, ventana 015). */
  async verificarCorreo(sesion: User, dto: VerificarCorreoDto): Promise<{ user: User }> {
    if (sesion.estadoVerificacion === 'verificado') {
      throw new ConflictException('El correo ya está verificado.');
    }
    const resultado = await this.codigoService.verificar(sesion.id, 'verificar_correo', dto.codigo);
    if (resultado !== 'ok') {
      throw errorDeCodigo(resultado);
    }
    await this.userService.marcarVerificado(sesion.id);
    return { user: await this.userService.findOne(sesion.id) };
  }

  /**
   * E-03 — reenviar el código (CU-03 1a). La espera de 30 s de la pantalla
   * se vuelve a exigir acá, porque la ruta se puede llamar directo. Responde
   * igual exista o no la cuenta (RNF-07).
   */
  async reenviarCodigo(dto: ReenviarCodigoDto): Promise<{ ok: true }> {
    const user: User | null = await this.userService.findOneByEmail(dto.email);
    if (user && user.proveedor === 'correo' && user.estadoVerificacion === 'procesando') {
      await this.enviarCodigo(user, 'verificar_correo', true);
    }
    return { ok: true };
  }

  /** E-04 y E-05 — entrar con Google o Microsoft (CU-02). */
  async entrarConProveedor(proveedor: ProveedorExterno, token: string): Promise<AuthResponse> {
    const verificador = this.verificadores[proveedor];
    if (!verificador.configurado) {
      throw new ServiceUnavailableException(
        `El acceso con ${NOMBRE_PROVEEDOR[proveedor]} no está configurado en este servidor.`,
      );
    }

    let identidad;
    try {
      identidad = await verificador.verificar(token);
    } catch {
      throw new UnauthorizedException(`${NOMBRE_PROVEEDOR[proveedor]} no aceptó el inicio de sesión.`);
    }

    // Cuenta ya creada con este proveedor: entra (o retoma su registro)
    const existente = await this.userService.findByProveedor(proveedor, identidad.proveedorId);
    if (existente) {
      return await this.buildAuthResponse(existente);
    }

    // El correo ya tiene cuenta con otro método: se avisa, no se vincula (RF-01-04)
    const mismoCorreo = await this.userService.findOneByEmail(identidad.correo);
    if (mismoCorreo) {
      throw new ConflictException(mensajeCorreoRegistrado(mismoCorreo.proveedor));
    }

    const nueva = await this.userService.createExterna(
      proveedor,
      identidad.proveedorId,
      identidad.correo,
      identidad.nombre,
    );
    return await this.buildAuthResponse(nueva);
  }

  /**
   * E-06 — completar el perfil y elegir el rol (CU-04, CU-05). Crea el
   * docente o el estudiante con su perfil y lo asocia a la credencial, en
   * una transacción. El UPDATE es condicional (solo si aún no hay rol): dos
   * peticiones simultáneas no pueden asignar dos roles (RI-12).
   */
  async elegirRol(sesion: User, dto: ElegirRolDto, foto?: ArchivoSubido): Promise<AuthResponse> {
    if (sesion.tieneRol()) {
      throw new ConflictException('Esta cuenta ya tiene un rol: el rol no se cambia.');
    }
    if (sesion.estadoVerificacion !== 'verificado') {
      throw new ForbiddenException('Primero verifica tu correo.');
    }

    const avatarUrl = foto ? await guardarFoto(foto, this.carpetaFotos) : null;
    const perfil = { nombres: dto.nombres, apellidos: dto.apellidos, avatarUrl };

    try {
      await this.dataSource.transaction(async (manager) => {
        const enlace =
          dto.role === 'docente'
            ? { idDocente: (await manager.save(manager.create(Docente, perfil))).id }
            : { idEstudiante: (await manager.save(manager.create(Estudiante, perfil))).id };

        const result = await manager.update(
          User,
          { id: sesion.id, idDocente: IsNull(), idEstudiante: IsNull() },
          enlace,
        );
        if (!result.affected) {
          throw new ConflictException('Esta cuenta ya tiene un rol: el rol no se cambia.');
        }
      });
    } catch (error) {
      await borrarFoto(avatarUrl, this.carpetaFotos);
      throw error;
    }

    return await this.buildAuthResponse(await this.userService.findOne(sesion.id));
  }

  /**
   * E-08 — pedir el código de recuperación (CU-07). Responde EXACTAMENTE
   * igual si la cuenta no existe, si es de Google o Microsoft o si existe
   * con contraseña: ninguno de esos casos se distingue desde afuera (RNF-07).
   */
  async solicitarRecuperacion(dto: SolicitarRecuperacionDto): Promise<{ ok: true }> {
    const user: User | null = await this.userService.findOneByEmail(dto.email);
    if (user && user.proveedor === 'correo') {
      await this.enviarCodigo(user, 'recuperar_contrasena', true);
    }
    return { ok: true };
  }

  /**
   * E-09 — verificar el código de recuperación. Devuelve un token corto que
   * solo sirve para POST /auth/nueva-contrasena. Si el correo no existe, el
   * mensaje es el mismo que con un código incorrecto.
   */
  async verificarRecuperacion(dto: VerificarRecuperacionDto): Promise<{ token: string }> {
    const user: User | null = await this.userService.findOneByEmail(dto.email);
    if (!user || user.proveedor !== 'correo') {
      throw new BadRequestException(MENSAJE_CODIGO.incorrecto);
    }
    const resultado = await this.codigoService.verificar(user.id, 'recuperar_contrasena', dto.codigo);
    if (resultado !== 'ok') {
      throw errorDeCodigo(resultado);
    }

    // Recibir el código prueba que el correo es suyo
    await this.userService.marcarVerificado(user.id);

    const payload: RecuperacionPayload = { sub: user.id, proposito: 'nueva-contrasena' };
    const token = await this.jwtService.signAsync(payload, {
      expiresIn: SEGUNDOS_TOKEN_RECUPERACION,
    });
    return { token };
  }

  /**
   * E-10 — guardar la contraseña nueva. No abre sesión: la persona vuelve a
   * iniciar sesión (CU-07 paso 5).
   */
  async nuevaContrasena(idCredencial: number, dto: NuevaContrasenaDto): Promise<void> {
    const user: User | null = await this.userService.findById(idCredencial);
    if (!user) {
      throw new UnauthorizedException('Token de recuperación inválido o vencido.');
    }
    await this.userService.actualizarPassword(user.id, dto.password);
  }

  /**
   * E-12 — editar el propio perfil (CU-09). Sin :id en la ruta: solo se
   * edita el perfil de quien tiene la sesión. Si la foto nueva no es válida,
   * responde 400 y la anterior no cambia.
   */
  async editarPerfil(sesion: User, dto: EditarPerfilDto, foto?: ArchivoSubido): Promise<{ user: User }> {
    const fila = sesion.docente ?? sesion.estudiante;
    if (!fila) {
      throw new ForbiddenException('Todavía no tienes un perfil: termina tu registro.');
    }

    const avatarUrl = foto ? await guardarFoto(foto, this.carpetaFotos) : undefined;
    const cambios = {
      ...(dto.nombres !== undefined && { nombres: dto.nombres }),
      ...(dto.apellidos !== undefined && { apellidos: dto.apellidos }),
      ...(avatarUrl && { avatarUrl }),
    };

    if (Object.keys(cambios).length > 0) {
      const entidad = sesion.docente ? Docente : Estudiante;
      await this.dataSource.getRepository(entidad).update({ id: fila.id }, cambios);
      // La foto se reemplaza, no se acumula (ventana 026)
      if (avatarUrl) await borrarFoto(fila.avatarUrl, this.carpetaFotos);
    }
    return { user: await this.userService.findOne(sesion.id) };
  }

  private async registrarLoginFallido(user: User): Promise<void> {
    const intentos: number = user.intentosLogin + 1;
    if (intentos >= MAX_INTENTOS_LOGIN) {
      const hasta = new Date(Date.now() + MINUTOS_BLOQUEO_LOGIN * 60_000);
      await this.userService.actualizarIntentosLogin(user.id, 0, hasta);
    } else {
      await this.userService.actualizarIntentosLogin(user.id, intentos, null);
    }
  }

  private async enviarCodigo(
    user: User,
    proposito: 'verificar_correo' | 'recuperar_contrasena',
    respetarEspera = false,
  ): Promise<void> {
    const codigo = await this.codigoService.emitir(user.id, proposito, { respetarEspera });
    if (!codigo) return;
    // Si el servidor de correo falla, la cuenta ya existe y el código
    // también: la persona puede pedir otro con «Reenviar» (ventana 015).
    try {
      await this.correoService.enviarCodigo(user.email, codigo, proposito);
    } catch (error) {
      this.logger.error(`No se pudo enviar el código a ${user.email}: ${String(error)}`);
    }
  }
}
