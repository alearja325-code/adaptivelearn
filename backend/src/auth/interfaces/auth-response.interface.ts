import type { Rol } from '../../user/entities/user.entity.js';

// Datos públicos del usuario que se devuelven al autenticarse (guía, sección 4)
export interface AuthUser {
  id: number;
  email: string;
  fullName: string | null;
  role: Rol;
}

// Respuesta de los endpoints /auth/register y /auth/login (y de los otros
// que abren o cambian la sesión: elegir rol, Google, Microsoft)
export interface AuthResponse {
  user: AuthUser;
  token: string;
}
