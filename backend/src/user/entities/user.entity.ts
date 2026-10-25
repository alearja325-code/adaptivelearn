import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';

export type ProveedorAuth = 'correo' | 'google' | 'microsoft';
export type Rol = 'docente' | 'estudiante';

// El User de la guía, sobre la tabla `credencial` (sql/001 y 002). No hay
// columna `role`: la spec 20 exige que Docente y Estudiante sean 2 tablas
// separadas, así que el rol se deduce de cuál de las 2 FK tiene valor.
// Propiedades de la guía con su nombre original; las agregadas por las
// specs de MODESEC, en español.
@Entity('credencial')
export class User {
  @PrimaryGeneratedColumn({ name: 'id_credencial' })
  id: number;

  @Column({ name: 'correo', unique: true, nullable: false })
  email: string;

  @Column({ name: 'password_hash', type: 'varchar', nullable: true, select: false })
  password: string | null;

  @Column({ name: 'nombre_completo', type: 'varchar', nullable: true })
  fullName: string | null;

  @Column({ type: 'enum', enum: ['correo', 'google', 'microsoft'] })
  proveedor: ProveedorAuth;

  @Column({ name: 'proveedor_id', type: 'varchar', nullable: true })
  proveedorId: string | null;

  @Column({ name: 'email_verificado', default: false })
  emailVerificado: boolean;

  @Column({ name: 'codigo_verificacion', type: 'char', length: 6, nullable: true, select: false })
  codigoVerificacion: string | null;

  @Column({ name: 'codigo_expira_en', type: 'datetime', nullable: true })
  codigoExpiraEn: Date | null;

  @Column({ name: 'codigo_ultimo_envio', type: 'datetime', nullable: true })
  codigoUltimoEnvio: Date | null;

  @Column({ name: 'intentos_codigo', default: 0 })
  intentosCodigo: number;

  @Column({ name: 'intentos_login', default: 0 })
  intentosLogin: number;

  @Column({ name: 'bloqueado_hasta', type: 'datetime', nullable: true })
  bloqueadoHasta: Date | null;

  @Column({ type: 'varchar', nullable: true })
  nombres: string | null;

  @Column({ type: 'varchar', nullable: true })
  apellidos: string | null;

  @Column({ name: 'avatar_url', type: 'varchar', nullable: true })
  avatarUrl: string | null;

  @Column({ name: 'id_docente', type: 'int', nullable: true })
  idDocente: number | null;

  @Column({ name: 'id_estudiante', type: 'int', nullable: true })
  idEstudiante: number | null;

  @CreateDateColumn({ name: 'creado_en' })
  createdAt: Date;

  @UpdateDateColumn({ name: 'actualizado_en' })
  updatedAt: Date;

  get role(): Rol | null {
    if (this.idDocente) return 'docente';
    if (this.idEstudiante) return 'estudiante';
    return null;
  }

  // Única forma en que un User sale en una respuesta HTTP: nunca password,
  // códigos, contadores de intentos ni ids internos.
  toJSON() {
    return {
      id: this.id,
      email: this.email,
      fullName: this.fullName,
      role: this.role,
      emailVerificado: this.emailVerificado,
    };
  }
}
