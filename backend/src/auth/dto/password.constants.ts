// Misma regla en 2 lugares (spec 17, Crear cuenta, y spec 22, Nueva
// contraseña) — se comparte para que no se desincronicen si cambia.
export const PASSWORD_REGEX = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$/;
export const PASSWORD_MENSAJE = 'Mínimo 8 caracteres, con una mayúscula, una minúscula y un número.';
