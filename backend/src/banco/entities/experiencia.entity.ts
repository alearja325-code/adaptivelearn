import {
  Column,
  Entity,
  JoinColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
  type Relation,
} from 'typeorm';
import { Dba } from '../../catalogo/entities/dba.entity.js';

export type EstadoExperiencia = 'Borrador' | 'Publicada';
export type ServicioIaNombre = 'gemini' | 'deepseek';

// Tabla `experiencia` (`17`, `18` §5): un diagnóstico anclado a un solo DBA.
// Se guarda solo si su banco se generó completo (ADR-027). El servicio y el
// modelo de IA que generaron el banco se guardan aquí, una vez (RI-17, ADR-035).
@Entity('experiencia')
export class Experiencia {
  @PrimaryGeneratedColumn({ name: 'id_experiencia', unsigned: true })
  id: number;

  @Column({ name: 'id_docente', type: 'int', unsigned: true })
  idDocente: number;

  @Column({ name: 'codigo_dba', type: 'varchar', length: 9 })
  codigoDba: string;

  @Column({ type: 'varchar', length: 160 })
  nombre: string;

  @Column({
    type: 'enum',
    enum: ['Borrador', 'Publicada'],
    default: 'Borrador',
  })
  estado: EstadoExperiencia;

  @Column({ name: 'fecha_creacion', type: 'datetime' })
  fechaCreacion: Date;

  // NULL si y solo si está en Borrador (RI-16)
  @Column({ name: 'fecha_publicacion', type: 'datetime', nullable: true })
  fechaPublicacion: Date | null;

  // 6 caracteres sin 0 O 1 I L (RI-3); se crea al guardar la experiencia
  @Column({ name: 'codigo_invitacion', type: 'char', length: 6 })
  codigoInvitacion: string;

  @Column({ name: 'servicio_ia', type: 'enum', enum: ['gemini', 'deepseek'] })
  servicioIa: ServicioIaNombre;

  @Column({ name: 'modelo_ia', type: 'varchar', length: 80 })
  modeloIa: string;

  @ManyToOne(() => Dba)
  @JoinColumn({ name: 'codigo_dba' })
  dba: Relation<Dba>;
}
