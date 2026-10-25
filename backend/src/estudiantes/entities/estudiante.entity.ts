import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

// Refleja estudiante(id_estudiante, nombre, correo, avatar_url) tal cual
// está aprobado en fase-3-diseno-computacional/04-modelo-relacional.md —
// sin columnas nuevas.
@Entity('estudiante')
export class Estudiante {
  @PrimaryGeneratedColumn({ name: 'id_estudiante' })
  id: number;

  @Column()
  nombre: string;

  @Column({ unique: true })
  correo: string;

  @Column({ name: 'avatar_url', type: 'varchar', nullable: true })
  avatarUrl: string | null;
}
