import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';

// Tabla `estudiante` del modelo relacional (`17`). Solo los datos mínimos
// (ADR-029): nombres, apellidos y foto opcional.
@Entity('estudiante')
export class Estudiante {
  @PrimaryGeneratedColumn({ name: 'id_estudiante', unsigned: true })
  id: number;

  @Column({ type: 'varchar', length: 120 })
  nombres: string;

  @Column({ type: 'varchar', length: 120 })
  apellidos: string;

  @Column({ name: 'avatar_url', type: 'varchar', length: 500, nullable: true })
  avatarUrl: string | null;
}
