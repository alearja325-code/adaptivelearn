import { IsEmail, IsNotEmpty } from 'class-validator';

// Spec 21, sección 2.4 — solo se valida formato, nunca existencia.
export class SolicitarRecuperacionDto {
  @IsEmail({}, { message: 'Escribe un correo válido.' })
  @IsNotEmpty({ message: 'Escribe un correo válido.' })
  email: string;
}
