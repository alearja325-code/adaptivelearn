import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';

// Tabla `documento_oficial` (ADR-036): el PDF del MEN del que se copió cada
// DBA, con la versión que dice el documento (ADR-033).
@Entity('documento_oficial')
export class DocumentoOficial {
  @PrimaryGeneratedColumn({ name: 'id_documento', unsigned: true })
  id: number;

  @Column({ name: 'codigo_area', type: 'varchar', length: 3 })
  codigoArea: string;

  @Column({ type: 'varchar', length: 200 })
  titulo: string;

  @Column({ type: 'varchar', length: 10 })
  version: string;

  @Column({ type: 'smallint', unsigned: true })
  anio: number;

  @Column({ type: 'smallint', unsigned: true })
  paginas: number;

  @Column({ name: 'url_oficial', type: 'varchar', length: 500 })
  urlOficial: string;
}
