import { ConflictException, Injectable, NotFoundException } from '@nestjs/common';
import { InjectDataSource, InjectRepository } from '@nestjs/typeorm';
import { DataSource, QueryFailedError, Repository } from 'typeorm';
import * as bcrypt from 'bcrypt';
import { User, type ProveedorAuth } from './entities/user.entity.js';
import { Docente } from './entities/docente.entity.js';
import { Estudiante } from './entities/estudiante.entity.js';
import { CreateUserDto } from './dto/create-user.dto.js';
import { UpdateUserDto } from './dto/update-user.dto.js';
import { NOMBRE_PROVEEDOR } from '../auth/proveedores/proveedor-identidad.js';

// Mensajes de la ventana 014 (RF-01-04): si el correo ya tiene cuenta, se
// avisa con qué método entrar; nunca se vinculan métodos.
export function mensajeCorreoRegistrado(proveedor: ProveedorAuth): string {
  return proveedor === 'correo'
    ? 'El email ya está registrado. Inicia sesión.'
    : `El email ya está registrado con ${NOMBRE_PROVEEDOR[proveedor]}. Continúa con ese botón.`;
}

// Las relaciones que hacen falta para el nombre y el perfil (fullName)
const RELACIONES = { docente: true, estudiante: true } as const;

@Injectable()
export class UserService {
  // Número de rondas de encriptación de bcrypt
  private readonly saltRounds = 10;

  constructor(
    // Inyección del repositorio de User
    @InjectRepository(User)
    private readonly userRepository: Repository<User>,
    @InjectDataSource() private readonly dataSource: DataSource,
  ) {}

  /**
   * Crear un nuevo usuario
   * Encripta la contraseña antes de guardarla. La cuenta nace de correo y
   * contraseña, `procesando` y sin rol (ADR-037, ADR-035).
   */
  async create(createUserDto: CreateUserDto): Promise<User> {
    // Verificar si el email ya existe
    const existente: User | null = await this.userRepository.findOneBy({
      email: createUserDto.email,
    });
    if (existente) {
      throw new ConflictException(mensajeCorreoRegistrado(existente.proveedor));
    }

    // Encriptar la contraseña
    const hashedPassword: string = await bcrypt.hash(createUserDto.password, this.saltRounds);

    // Crear nueva instancia de usuario
    const user: User = this.userRepository.create({
      email: createUserDto.email,
      password: hashedPassword,
      nombreCompleto: createUserDto.fullName?.trim() || null,
      proveedor: 'correo',
    });

    // Guardar en la base de datos. El UNIQUE de `correo` es la última
    // palabra si dos registros con el mismo correo llegan a la vez.
    try {
      await this.userRepository.save(user);
    } catch (error) {
      if (esDuplicado(error)) {
        throw new ConflictException(mensajeCorreoRegistrado('correo'));
      }
      throw error;
    }
    return await this.findOne(user.id);
  }

  /** Cuenta nueva de Google o Microsoft: nace con el correo verificado (RI-15). */
  async createExterna(
    proveedor: Exclude<ProveedorAuth, 'correo'>,
    proveedorId: string,
    email: string,
    nombre: string | null,
  ): Promise<User> {
    const user: User = this.userRepository.create({
      email,
      proveedor,
      proveedorId,
      password: null,
      nombreCompleto: nombre,
      estadoVerificacion: 'verificado',
    });
    await this.userRepository.save(user);
    return await this.findOne(user.id);
  }

  /**
   * Obtener todos los usuarios
   * No incluye las contraseñas (select: false en la entidad)
   */
  async findAll(): Promise<User[]> {
    return await this.userRepository.find({ relations: RELACIONES, order: { id: 'ASC' } });
  }

  /**
   * Obtener un usuario por ID
   * Lanza 404 si no existe (para uso en controladores)
   */
  async findOne(id: number): Promise<User> {
    const user: User | null = await this.findById(id);
    if (!user) {
      throw new NotFoundException(`Usuario con ID ${id} no encontrado`);
    }
    return user;
  }

  /**
   * Buscar un usuario por ID sin lanzar excepción
   * Devuelve null si no existe (lo usa la estrategia JWT)
   */
  async findById(id: number): Promise<User | null> {
    return await this.userRepository.findOne({ where: { id }, relations: RELACIONES });
  }

  /**
   * Buscar usuario por email
   * Incluye la contraseña y el bloqueo (solo para autenticación)
   * Devuelve null si el email no está registrado
   */
  async findOneByEmail(email: string): Promise<User | null> {
    return await this.userRepository
      .createQueryBuilder('user')
      .addSelect(['user.password', 'user.intentosLogin', 'user.bloqueadoHasta'])
      .leftJoinAndSelect('user.docente', 'docente')
      .leftJoinAndSelect('user.estudiante', 'estudiante')
      .where('user.email = :email', { email })
      .getOne();
  }

  /** Buscar la credencial de una persona en Google o Microsoft. */
  async findByProveedor(proveedor: ProveedorAuth, proveedorId: string): Promise<User | null> {
    return await this.userRepository.findOne({
      where: { proveedor, proveedorId },
      relations: RELACIONES,
    });
  }

  /**
   * Actualizar un usuario (solo administrador: PATCH /users/:id)
   * Guía: email, contraseña, nombre, isActive y role. Acá email, contraseña
   * y nombre; un correo nuevo vuelve a `procesando`, porque nadie lo verificó.
   */
  async update(id: number, updateUserDto: UpdateUserDto): Promise<User> {
    const user: User = await this.findOne(id);

    if ((updateUserDto.email || updateUserDto.password) && user.proveedor !== 'correo') {
      throw new ConflictException(
        `Esta cuenta entra con ${NOMBRE_PROVEEDOR[user.proveedor]}: no tiene correo ni contraseña propios.`,
      );
    }

    const cambios: Partial<User> = {};

    // Si se cambia el email, verificar que no pertenezca a otro usuario
    if (updateUserDto.email && updateUserDto.email !== user.email) {
      const otro: User | null = await this.userRepository.findOneBy({
        email: updateUserDto.email,
      });
      if (otro && otro.id !== id) {
        throw new ConflictException(mensajeCorreoRegistrado(otro.proveedor));
      }
      cambios.email = updateUserDto.email;
      cambios.estadoVerificacion = 'procesando';
    }

    // Si se actualiza la contraseña, encriptarla
    if (updateUserDto.password) {
      cambios.password = await bcrypt.hash(updateUserDto.password, this.saltRounds);
    }

    if (updateUserDto.fullName !== undefined) {
      cambios.nombreCompleto = updateUserDto.fullName.trim() || null;
    }

    if (Object.keys(cambios).length > 0) {
      await this.userRepository.update({ id }, cambios);
    }
    return await this.findOne(id);
  }

  /**
   * Eliminar un usuario (borrado físico del registro)
   * Borra la credencial (sus códigos se van en cascada) y su docente o
   * estudiante, en una transacción. Si el docente ya tiene experiencias,
   * la base lo impide (RESTRICT) y se responde 409.
   */
  async remove(id: number): Promise<void> {
    const user: User = await this.findOne(id);
    try {
      await this.dataSource.transaction(async (manager) => {
        await manager.delete(User, { id: user.id });
        if (user.idDocente) await manager.delete(Docente, { id: user.idDocente });
        if (user.idEstudiante) await manager.delete(Estudiante, { id: user.idEstudiante });
      });
    } catch (error) {
      if (error instanceof QueryFailedError && /foreign key/i.test(error.message)) {
        throw new ConflictException('El usuario tiene datos asociados y no se puede borrar.');
      }
      throw error;
    }
  }

  // ------------------------------------------------------------------
  // Agregado para el acceso de AdaptiveLearn (fuera de la guía)
  // ------------------------------------------------------------------

  async marcarVerificado(id: number): Promise<void> {
    await this.userRepository.update({ id }, { estadoVerificacion: 'verificado' });
  }

  async actualizarPassword(id: number, password: string): Promise<void> {
    const hash: string = await bcrypt.hash(password, this.saltRounds);
    // Contraseña nueva: también se levanta el bloqueo de inicio de sesión
    await this.userRepository.update(
      { id },
      { password: hash, intentosLogin: 0, bloqueadoHasta: null },
    );
  }

  async actualizarIntentosLogin(id: number, intentos: number, hasta: Date | null): Promise<void> {
    await this.userRepository.update({ id }, { intentosLogin: intentos, bloqueadoHasta: hasta });
  }
}

function esDuplicado(error: unknown): boolean {
  return (
    error instanceof QueryFailedError &&
    (error.driverError as { code?: string } | undefined)?.code === 'ER_DUP_ENTRY'
  );
}
