import { Matches } from 'class-validator';
import { PASSWORD_REGEX, PASSWORD_MENSAJE } from './password.constants.js';

// Spec 22, sección 2.2 — un solo campo, sin "confirmar contraseña" (ya
// decidido en spec 17: el ícono de mostrar/ocultar hace innecesario
// pedirla 2 veces).
export class NuevaContrasenaDto {
  @Matches(PASSWORD_REGEX, { message: PASSWORD_MENSAJE })
  password: string;
}
