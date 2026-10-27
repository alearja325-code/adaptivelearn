import { PartialType } from '@nestjs/mapped-types';
import { CreateUserDto } from './create-user.dto.js';

// PartialType hace que todas las propiedades de CreateUserDto sean opcionales.
// Guía: además isActive y role. Acá ninguno de los dos: no hay cuentas
// desactivadas en el modelo, y ni el rol ni la marca de administrador se
// asignan por la API (RF-01-06, ADR-040: la marca solo se pone por SQL).
export class UpdateUserDto extends PartialType(CreateUserDto) {}
