import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';

// Tabla `inscripcion` del modelo relacional (`17`): un estudiante en una
// experiencia. UNIQUE(id_estudiante, id_experiencia) es RI-1.
@Entity('inscripcion')
export class Inscripcion {
  @PrimaryGeneratedColumn({ name: 'id_inscripcion', unsigned: true })
  id: number;

  @Column({ name: 'id_estudiante', type: 'int', unsigned: true })
  idEstudiante: number;

  @Column({ name: 'id_experiencia', type: 'int', unsigned: true })
  idExperiencia: number;

  @Column({ name: 'fecha_union', type: 'datetime' })
  fechaUnion: Date;
}
