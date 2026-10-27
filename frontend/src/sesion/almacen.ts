// Dónde vive el token de sesión en el navegador. Decisión del encargo 04,
// declarada: sessionStorage. Sobrevive a recargar la página, pero se borra
// al cerrar la pestaña, así una sesión olvidada en un computador compartido
// (una sala de informática) no queda abierta. El token vence de todos modos
// a la hora (JWT_EXPIRATION). La contraseña NUNCA se guarda en el navegador.
const CLAVE = 'adaptivelearn.token';

export function leerToken(): string | null {
  try {
    return sessionStorage.getItem(CLAVE);
  } catch {
    return null;
  }
}

export function guardarToken(token: string | null): void {
  try {
    if (token) sessionStorage.setItem(CLAVE, token);
    else sessionStorage.removeItem(CLAVE);
  } catch {
    // sin almacenamiento (modo privado estricto): la sesión vive en memoria
  }
}
