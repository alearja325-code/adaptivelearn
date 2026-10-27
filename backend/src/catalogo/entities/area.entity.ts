import { Column, Entity, PrimaryColumn } from 'typeorm';

// Tabla `area` (ADR-036): las 4 áreas de ADR-033.
@Entity('area')
export class Area {
  @PrimaryColumn({ name: 'codigo_area', type: 'varchar', length: 3 })
  codigo: string;

  @Column({ type: 'varchar', length: 40 })
  nombre: string;
}
