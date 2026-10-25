import type { Rol } from '../../user/entities/user.entity.js';

// Interfaz que define la estructura del payload del JWT
export interface JwtPayload {
  sub: number;      // ID del usuario
  email: string;    // Email del usuario
  role: Rol | null; // Rol del usuario — null hasta "Elige tu rol" (spec 20)
}
