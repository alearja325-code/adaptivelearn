import { ConflictException, Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { QueryFailedError, Repository } from 'typeorm';
import * as bcrypt from 'bcrypt';
import { User, type ProveedorAuth } from './entities/user.entity.js';
import { CreateUserDto } from './dto/create-user.dto.js';
import { UpdateUserDto } from './dto/update-user.dto.js';

const NOMBRE_PROVEEDOR: Record<ProveedorAuth, string> = {
  correo: 'correo',
  google: 'Google',
  microsoft: 'Microsoft',
};

// Spec 17, sección 2.6.
export function mensajeOtroProveedor(proveedor: ProveedorAuth): string {
  return `Esta cuenta usa ${NOMBRE_PROVEEDOR[proveedor]} para entrar. Continúa con ese botón.`;
}

function conflictoPorCorreo(proveedor: ProveedorAuth): ConflictException {
  return new ConflictException(
    proveedor === 'correo'
      ? 'Ya existe una cuenta con este correo. Inicia sesión.'
      : mensajeOtroProveedor(proveedor),
  );
}

@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User)
    private readonly userRepository: Repository<User>,
  ) {}

  /**
   * Crear un nuevo usuario
   * Encripta la contraseña antes de guardarla
   */
  async create(createUserDto: CreateUserDto): Promise<User> {
    const existingUser = await this.userRepository.findOne({
      where: { email: createUserDto.email },
    });

    if (existingUser) {
      throw conflictoPorCorreo(existingUser.proveedor);
    }

    const hashedPassword = await bcrypt.hash(createUserDto.password, 10);

    const user = this.userRepository.create({
      email: createUserDto.email,
      password: hashedPassword,
      fullName: createUserDto.fullName ?? null,
      proveedor: 'correo',
      emailVerificado: false,
      idDocente: null,
      idEstudiante: null,
    });

    try {
      return await this.userRepository.save(user);
    } catch (error) {
      // Dos registros simultáneos con el mismo correo pasan ambos el
      // findOne de arriba; el UNIQUE de la base detiene al segundo.
      if (
        error instanceof QueryFailedError &&
        (error.driverError as { code?: string }).code === 'ER_DUP_ENTRY'
      ) {
        throw conflictoPorCorreo('correo');
      }
      throw error;
    }
  }

  /**
   * Obtener todos los usuarios
   * No incluye las contraseñas
   */
  async findAll(): Promise<User[]> {
    return await this.userRepository.find();
  }

  /**
   * Obtener un usuario por ID
   */
  async findOne(id: number): Promise<User> {
    const user = await this.userRepository.findOne({ where: { id } });

    if (!user) {
      throw new NotFoundException(`Usuario con ID ${id} no encontrado`);
    }

    return user;
  }

  /**
   * Buscar usuario por email
   * Incluye la contraseña y el código de verificación (para autenticación)
   */
  async findOneByEmail(email: string): Promise<User | null> {
    return await this.userRepository
      .createQueryBuilder('user')
      .addSelect('user.password')
      .addSelect('user.codigoVerificacion')
      .where('user.email = :email', { email })
      .getOne();
  }

  /**
   * Actualizar el perfil de un usuario (spec 19)
   */
  async update(id: number, updateUserDto: UpdateUserDto): Promise<User> {
    const user = await this.findOne(id);

    Object.assign(user, updateUserDto);

    if (user.nombres && user.apellidos) {
      user.fullName = `${user.nombres} ${user.apellidos}`;
    }

    return await this.userRepository.save(user);
  }

  async guardarCodigoVerificacion(id: number, codigo: string, expiraEn: Date): Promise<void> {
    await this.userRepository.update(id, {
      codigoVerificacion: codigo,
      codigoExpiraEn: expiraEn,
      codigoUltimoEnvio: new Date(),
      intentosCodigo: 0,
    });
  }

  async registrarIntentoCodigoFallido(id: number): Promise<void> {
    await this.userRepository.increment({ id }, 'intentosCodigo', 1);
  }

  async marcarCorreoVerificado(id: number): Promise<void> {
    await this.userRepository.update(id, {
      emailVerificado: true,
      codigoVerificacion: null,
      codigoExpiraEn: null,
      intentosCodigo: 0,
    });
  }

  async actualizarIntentosLogin(id: number, intentos: number, bloqueadoHasta: Date | null): Promise<void> {
    await this.userRepository.update(id, { intentosLogin: intentos, bloqueadoHasta });
  }

  async actualizarPassword(id: number, passwordHash: string): Promise<void> {
    await this.userRepository.update(id, {
      password: passwordHash,
      intentosLogin: 0,
      bloqueadoHasta: null,
    });
  }
}
