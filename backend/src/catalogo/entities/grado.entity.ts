import { Column, Entity, PrimaryColumn } from 'typeorm';

export type NivelEducativo = 'basica_primaria' | 'basica_secundaria' | 'media';

// Tabla `grado` (ADR-036): 1 a 11, con su nivel de la Ley 115 de 1994.
@Entity('grado')
export class Grado {
  @PrimaryColumn({ type: 'tinyint', unsigned: true })
  numero: number;

  @Column({ type: 'varchar', length: 20 })
  nombre: string;

  @Column({ type: 'enum', enum: ['basica_primaria', 'basica_secundaria', 'media'] })
  nivel: NivelEducativo;
}
