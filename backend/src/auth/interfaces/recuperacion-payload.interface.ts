// Token corto (15 min) que emite la verificación del código de
// recuperación (specs 18 flujo 2 y 21) y que solo sirve para guardar la
// contraseña nueva (spec 22). No es un token de sesión: JwtStrategy lo
// rechaza por traer `proposito`.
export interface RecuperacionPayload {
  sub: number; // ID del usuario
  proposito: 'nueva-contrasena';
}
