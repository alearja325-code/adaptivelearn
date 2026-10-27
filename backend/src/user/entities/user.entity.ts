import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  CreateDateColumn,
  UpdateDateColumn,
  OneToOne,
  JoinColumn,
} from 'typeorm';
import { Exclude, Expose } from 'class-transformer';
import { Docente } from './docente.entity.js';
import { Estudiante } from './estudiante.entity.js';

export type ProveedorAuth = 'correo' | 'google' | 'microsoft';
export type EstadoVerificacion = 'procesando' | 'verificado';

// Los roles de la sesión (ADR-040). 'docente' y 'estudiante' son los del
// producto; 'admin' es la marca de la guía para /users; 'user' es el rol
// por defecto de la guía, que aquí significa "registro a medias: todavía
// sin docente ni estudiante" (ADR-035).
export type Rol = 'user' | 'docente' | 'estudiante' | 'admin';

export interface Perfil {
  nombres: string;
  apellidos: string;
  avatarUrl: string | null;
}

// Decorador @Entity define que esta clase es una entidad de base de datos.
// Guía: @Entity('users'). Acá el User de la guía vive sobre la tabla
// `credencial` del modelo relacional (`17`, ADR-034): las columnas se llaman
// como en el MR y las propiedades, como en la guía (email, password,
// fullName, role). La tabla la crea sql/001_esquema.sql, generado del MR.
@Entity('credencial')
export class User {
  // Clave primaria auto-incremental
  @PrimaryGeneratedColumn({ name: 'id_credencial', unsigned: true })
  id: number;

  // Columna de email única y no nula
  @Column({ name: 'correo', type: 'varchar', length: 254, unique: true, nullable: false })
  email: string;

  // Contraseña encriptada. select: false evita que se lea por defecto;
  // @Exclude() evita que se envíe en las respuestas HTTP (guía, sección 5).
  // NULL si la cuenta entra con Google o Microsoft (RI-15).
  @Exclude()
  @Column({ name: 'password_hash', type: 'varchar', nullable: true, select: false })
  password: string | null;

  // Guía: fullName es una columna. Acá es el nombre escrito al registrarse;
  // cuando hay rol, el nombre es el de docente o estudiante (getter fullName).
  @Exclude()
  @Column({ name: 'nombre_completo', type: 'varchar', length: 240, nullable: true })
  nombreCompleto: string | null;

  // Método con el que se creó la cuenta (RF-01-04)
  @Column({ type: 'enum', enum: ['correo', 'google', 'microsoft'] })
  proveedor: ProveedorAuth;

  @Exclude()
  @Column({ name: 'proveedor_id', type: 'varchar', nullable: true, select: false })
  proveedorId: string | null;

  // R3 / ADR-037: procesando hasta que se confirma el código
  @Column({
    name: 'estado_verificacion',
    type: 'enum',
    enum: ['procesando', 'verificado'],
    default: 'procesando',
  })
  estadoVerificacion: EstadoVerificacion;

  // ADR-040: marca de administrador. Solo se pone por SQL; se ve en `role`.
  @Exclude()
  @Column({ name: 'es_admin', type: 'boolean', default: false })
  esAdmin: boolean;

  // Bloqueo tras 5 intentos fallidos de inicio de sesión (RF-01-07)
  @Exclude()
  @Column({ name: 'intentos_login', type: 'tinyint', unsigned: true, default: 0, select: false })
  intentosLogin: number;

  @Exclude()
  @Column({ name: 'bloqueado_hasta', type: 'datetime', nullable: true, select: false })
  bloqueadoHasta: Date | null;

  // Nota R2 del docente: la cuenta apunta al docente o al estudiante, nunca
  // a los dos (RI-12). Se envían en las respuestas.
  @Column({ name: 'id_docente', type: 'int', unsigned: true, nullable: true })
  idDocente: number | null;

  @Column({ name: 'id_estudiante', type: 'int', unsigned: true, nullable: true })
  idEstudiante: number | null;

  @Exclude()
  @OneToOne(() => Docente, { nullable: true })
  @JoinColumn({ name: 'id_docente' })
  docente?: Docente | null;

  @Exclude()
  @OneToOne(() => Estudiante, { nullable: true })
  @JoinColumn({ name: 'id_estudiante' })
  estudiante?: Estudiante | null;

  // Fecha de creación automática
  @CreateDateColumn({ name: 'creado_en' })
  createdAt: Date;

  // Fecha de actualización automática
  @UpdateDateColumn({ name: 'actualizado_en' })
  updatedAt: Date;

  /**
   * Guía: columna `role` con 'user' por defecto. Acá se deduce: la marca de
   * administrador primero; si no, de cuál de las dos FK tiene valor.
   */
  @Expose()
  get role(): Rol {
    if (this.esAdmin) return 'admin';
    if (this.idDocente) return 'docente';
    if (this.idEstudiante) return 'estudiante';
    return 'user';
  }

  /** ¿Ya eligió docente o estudiante? (ADR-035: si no, retoma el registro) */
  tieneRol(): boolean {
    return this.idDocente !== null || this.idEstudiante !== null;
  }

  /** Nombres, apellidos y foto, si ya eligió rol (ventanas 016 y 026). */
  @Expose()
  get perfil(): Perfil | null {
    const fila = this.docente ?? this.estudiante;
    if (!fila) return null;
    return { nombres: fila.nombres, apellidos: fila.apellidos, avatarUrl: fila.avatarUrl };
  }

  /** El fullName de la guía: el del perfil si existe; si no, el del registro. */
  @Expose()
  get fullName(): string | null {
    const perfil = this.perfil;
    return perfil ? `${perfil.nombres} ${perfil.apellidos}` : this.nombreCompleto;
  }
}
