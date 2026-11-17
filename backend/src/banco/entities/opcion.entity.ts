import {
  Column,
  Entity,
  JoinColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
  type Relation,
} from 'typeorm';
import { Item } from './item.entity.js';

export type Grupo = 'izquierda' | 'derecha';

// Tabla `opcion` (`18` §15). Qué columnas aplican depende del formato (RI-4):
// single_choice usa es_correcta (orden nulo, `18` §15); ordering,
// orden como posición correcta; matching, grupo y orden como número de pareja.
@Entity('opcion')
export class Opcion {
  @PrimaryGeneratedColumn({ name: 'id_opcion', unsigned: true })
  id: number;

  @Column({ name: 'id_item', type: 'int', unsigned: true })
  idItem: number;

  @Column({ type: 'text' })
  texto: string;

  @Column({ type: 'tinyint', unsigned: true, nullable: true })
  orden: number | null;

  @Column({ name: 'es_correcta', type: 'boolean', nullable: true })
  esCorrecta: boolean | null;

  @Column({ type: 'enum', enum: ['izquierda', 'derecha'], nullable: true })
  grupo: Grupo | null;

  // Por qué un estudiante podría elegir esta opción incorrecta (ADR-020).
  // Nunca se muestra ni se reporta (ADR-008): ninguna respuesta la incluye.
  @Column({ name: 'hipotesis_error', type: 'text', nullable: true })
  hipotesisError: string | null;

  @ManyToOne(() => Item, (item) => item.opciones, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'id_item' })
  item: Relation<Item>;
}
