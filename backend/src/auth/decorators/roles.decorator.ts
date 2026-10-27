import { CustomDecorator, SetMetadata } from '@nestjs/common';
import type { Rol } from '../../user/entities/user.entity.js';

// Clave compartida entre el decorador y el guard (evita errores de escritura)
export const ROLES_KEY = 'roles';

/**
 * Decorador para especificar roles requeridos
 * Uso: @Roles('admin') o @Roles('docente')
 */
export const Roles = (...roles: Rol[]): CustomDecorator<string> => SetMetadata(ROLES_KEY, roles);
