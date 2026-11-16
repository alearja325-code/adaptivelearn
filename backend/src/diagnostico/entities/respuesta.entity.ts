import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';

// Tabla `respuesta` (`17`). `correcta` es derivada y se guarda como
// fotografía (ADR-021); una respuesta no se cambia (RNF-10).
@Entity('respuesta')
export class Respuesta {
  @PrimaryGeneratedColumn({ name: 'id_respuesta', unsigned: true })
  id: number;

  @Column({ name: 'id_inscripcion', type: 'int', unsigned: true })
  idInscripcion: number;

  @Column({ name: 'id_item', type: 'int', unsigned: true })
  idItem: number;

  @Column({ type: 'tinyint', unsigned: true })
  certeza: number;

  @Column({ name: 'fecha_respuesta', type: 'datetime' })
  fechaRespuesta: Date;

  @Column({ type: 'boolean' })
  correcta: boolean;
}
