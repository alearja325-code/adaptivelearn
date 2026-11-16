import {
  Column,
  Entity,
  OneToMany,
  PrimaryGeneratedColumn,
  type Relation,
} from 'typeorm';
import { Opcion } from './opcion.entity.js';

export type Formato = 'single_choice' | 'matching' | 'ordering';
export type OrigenItem = 'ia' | 'editado_docente' | 'creado_docente';
export const FORMATOS: readonly Formato[] = [
  'single_choice',
  'matching',
  'ordering',
];

// Tabla `item` (`18` §14): una pregunta del banco. Cuelga de una evidencia
// incluida en su experiencia (FK compuesta a experiencia_evidencia, H-4).
@Entity('item')
export class Item {
  @PrimaryGeneratedColumn({ name: 'id_item', unsigned: true })
  id: number;

  @Column({ name: 'id_experiencia', type: 'int', unsigned: true })
  idExperiencia: number;

  @Column({ name: 'codigo_dba', type: 'varchar', length: 9 })
  codigoDba: string;

  @Column({ name: 'numero_evidencia', type: 'tinyint', unsigned: true })
  numeroEvidencia: number;

  @Column({ type: 'text' })
  enunciado: string;

  @Column({
    type: 'enum',
    enum: ['single_choice', 'matching', 'ordering'],
    default: 'single_choice',
  })
  formato: Formato;

  @Column({
    type: 'enum',
    enum: ['ia', 'editado_docente', 'creado_docente'],
    default: 'ia',
  })
  origen: OrigenItem;

  // «Descartar»: no se muestra a los estudiantes, pero sigue en el banco (ADR-015)
  @Column({ type: 'boolean', default: false })
  excluido: boolean;

  @OneToMany(() => Opcion, (opcion) => opcion.item)
  opciones: Relation<Opcion[]>;
}
