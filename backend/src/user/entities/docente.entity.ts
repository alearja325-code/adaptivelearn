import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';

// Tabla `docente` del modelo relacional (`17`). Nace al elegir el rol
// Docente, con su perfil (RF-01-05, RF-01-06); el correo está en la credencial.
@Entity('docente')
export class Docente {
  @PrimaryGeneratedColumn({ name: 'id_docente', unsigned: true })
  id: number;

  @Column({ type: 'varchar', length: 120 })
  nombres: string;

  @Column({ type: 'varchar', length: 120 })
  apellidos: string;

  @Column({ name: 'avatar_url', type: 'varchar', length: 500, nullable: true })
  avatarUrl: string | null;
}
