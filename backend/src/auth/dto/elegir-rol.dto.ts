import { IsIn } from 'class-validator';
import { PerfilDto } from './perfil.dto.js';

// Ventanas 016 y 017 en una sola petición (E-06): el perfil se guarda al
// elegir el rol (RF-01-05, RF-01-06). La foto llega aparte, como archivo
// del multipart/form-data (campo `foto`).
export class ElegirRolDto extends PerfilDto {
  @IsIn(['docente', 'estudiante'], { message: 'El rol debe ser "docente" o "estudiante"' })
  role: 'docente' | 'estudiante';
}
