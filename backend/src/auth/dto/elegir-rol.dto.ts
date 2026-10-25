import { IsIn } from 'class-validator';
import type { Rol } from '../../user/entities/user.entity.js';

// Spec 20 — "Elige tu rol".
export class ElegirRolDto {
  @IsIn(['docente', 'estudiante'], { message: 'El rol debe ser "docente" o "estudiante"' })
  role: Rol;
}
