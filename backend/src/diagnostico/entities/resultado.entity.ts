import { Column, Entity, PrimaryColumn } from 'typeorm';
import type { EstadoResultado } from '../reglas/regla-adaptativa.js';

// Tabla `resultado` (`17`): entidad débil, una fila cuando la regla
// adaptativa concluye la evidencia. Fotografía con su fecha (ADR-021,
// RNF-11): no se vuelve a escribir. Sin fila = "sin concluir" (ADR-022).
@Entity('resultado')
export class Resultado {
  @PrimaryColumn({ name: 'id_inscripcion', type: 'int', unsigned: true })
  idInscripcion: number;

  @PrimaryColumn({ name: 'codigo_dba', type: 'varchar', length: 9 })
  codigoDba: string;

  @PrimaryColumn({ name: 'numero_evidencia', type: 'tinyint', unsigned: true })
  numeroEvidencia: number;

  @Column({ name: 'id_experiencia', type: 'int', unsigned: true })
  idExperiencia: number;

  @Column({ type: 'enum', enum: ['muestra', 'no_muestra', 'no_concluyente'] })
  estado: EstadoResultado;

  @Column({ name: 'fecha_calculo', type: 'datetime' })
  fechaCalculo: Date;
}
