import { Column, Entity, JoinColumn, ManyToOne, OneToMany, PrimaryColumn, type Relation } from 'typeorm';
import { Area } from './area.entity.js';
import { Grado } from './grado.entity.js';
import { DocumentoOficial } from './documento-oficial.entity.js';
import { Evidencia } from './evidencia.entity.js';

// Relation<...>: en ESM, dos entidades que se importan entre sí fallan al
// cargar si TypeScript emite su tipo; Relation lo evita (TypeORM).
// Tabla `dba`: dato del MEN, de solo lectura (SUB-06). Código ÁREA-GG-NN (RI-21).
@Entity('dba')
export class Dba {
  @PrimaryColumn({ name: 'codigo_dba', type: 'varchar', length: 9 })
  codigo: string;

  @Column({ name: 'codigo_area', type: 'varchar', length: 3 })
  codigoArea: string;

  @Column({ name: 'numero_grado', type: 'tinyint', unsigned: true })
  numeroGrado: number;

  @Column({ name: 'id_documento', type: 'int', unsigned: true })
  idDocumento: number;

  @Column({ type: 'text' })
  enunciado: string;

  @Column({ type: 'text', nullable: true })
  ejemplo: string | null;

  @ManyToOne(() => Area)
  @JoinColumn({ name: 'codigo_area' })
  area: Relation<Area>;

  @ManyToOne(() => Grado)
  @JoinColumn({ name: 'numero_grado' })
  grado: Relation<Grado>;

  @ManyToOne(() => DocumentoOficial)
  @JoinColumn({ name: 'id_documento' })
  documento: Relation<DocumentoOficial>;

  @OneToMany(() => Evidencia, (evidencia) => evidencia.dba)
  evidencias: Relation<Evidencia[]>;
}
