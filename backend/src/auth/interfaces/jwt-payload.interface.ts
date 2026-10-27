import type { Rol } from '../../user/entities/user.entity.js';

// Interfaz que define la estructura del payload del JWT
export interface JwtPayload {
  sub: number; // ID de la credencial
  email: string; // Email de la cuenta
  role: Rol; // Rol: 'user' mientras no elige docente o estudiante
  // Nota R2 del docente: la sesión dice a qué docente o estudiante da acceso
  idDocente: number | null;
  idEstudiante: number | null;
}

// Token corto (15 min) que entrega la verificación del código de
// recuperación (E-09) y que solo sirve para fijar la contraseña nueva
// (E-10). No es una sesión: JwtStrategy lo rechaza por traer `proposito`.
export interface RecuperacionPayload {
  sub: number;
  proposito: 'nueva-contrasena';
}
