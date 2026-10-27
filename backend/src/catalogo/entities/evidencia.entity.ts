import { Column, Entity, JoinColumn, ManyToOne, OneToOne, PrimaryColumn, type Relation } from 'typeorm';
import { Dba } from './dba.entity.js';
import { EvidenciaDictamen } from './evidencia-dictamen.entity.js';

// Tabla `evidencia`: entidad débil del DBA; `numero` es su posición oficial.
@Entity('evidencia')
export class Evidencia {
  @PrimaryColumn({ name: 'codigo_dba', type: 'varchar', length: 9 })
  codigoDba: string;

  @PrimaryColumn({ name: 'numero_evidencia', type: 'tinyint', unsigned: true })
  numero: number;

  @Column({ type: 'text' })
  enunciado: string;

  @ManyToOne(() => Dba, (dba) => dba.evidencias)
  @JoinColumn({ name: 'codigo_dba' })
  dba: Relation<Dba>;

  @OneToOne(() => EvidenciaDictamen, (dictamen) => dictamen.evidencia)
  dictamen: Relation<EvidenciaDictamen> | null;
}
