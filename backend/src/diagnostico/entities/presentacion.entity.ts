import { Column, Entity, PrimaryColumn } from 'typeorm';

// Tabla `presentacion` (`17`): qué ítem se le mostró y en qué orden (RI-8).
// `id_experiencia` repite la de la inscripción a propósito (RI-13, `17` §5.1).
@Entity('presentacion')
export class Presentacion {
  @PrimaryColumn({ name: 'id_inscripcion', type: 'int', unsigned: true })
  idInscripcion: number;

  @PrimaryColumn({ name: 'id_item', type: 'int', unsigned: true })
  idItem: number;

  @Column({ name: 'id_experiencia', type: 'int', unsigned: true })
  idExperiencia: number;

  @Column({ name: 'orden_presentacion', type: 'tinyint', unsigned: true })
  ordenPresentacion: number;

  @Column({ name: 'fecha_presentacion', type: 'datetime' })
  fechaPresentacion: Date;
}
