import { Column, Entity, JoinColumn, OneToOne, PrimaryColumn, type Relation } from 'typeorm';
import { Evidencia } from './evidencia.entity.js';

// Tabla `evidencia_dictamen`: el único juicio nuestro sobre el material del
// MEN (RF-06-02). Vacía hasta que termine el censo QA-014 (V-6).
@Entity('evidencia_dictamen')
export class EvidenciaDictamen {
  @PrimaryColumn({ name: 'codigo_dba', type: 'varchar', length: 9 })
  codigoDba: string;

  @PrimaryColumn({ name: 'numero_evidencia', type: 'tinyint', unsigned: true })
  numeroEvidencia: number;

  @Column({ name: 'aplica_formato_cerrado', type: 'boolean' })
  aplicaFormatoCerrado: boolean;

  @Column({ type: 'enum', enum: ['single_choice', 'matching', 'ordering'], nullable: true })
  formato: string | null;

  @OneToOne(() => Evidencia, (evidencia) => evidencia.dictamen)
  @JoinColumn([
    { name: 'codigo_dba', referencedColumnName: 'codigoDba' },
    { name: 'numero_evidencia', referencedColumnName: 'numero' },
  ])
  evidencia: Relation<Evidencia>;
}
