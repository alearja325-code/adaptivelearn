import { Column, Entity, PrimaryColumn } from 'typeorm';

// Tabla `respuesta_opcion` (ADR-019): qué eligió, no solo si acertó.
// `id_item` está en las dos llaves foráneas: el motor rechaza una opción de
// otro ítem (RI-6, ciclo C4, `17` §5.2).
@Entity('respuesta_opcion')
export class RespuestaOpcion {
  @PrimaryColumn({ name: 'id_respuesta', type: 'int', unsigned: true })
  idRespuesta: number;

  @PrimaryColumn({ name: 'id_opcion', type: 'int', unsigned: true })
  idOpcion: number;

  @Column({ name: 'id_item', type: 'int', unsigned: true })
  idItem: number;

  @Column({
    name: 'valor_dado',
    type: 'tinyint',
    unsigned: true,
    nullable: true,
  })
  valorDado: number | null;
}
