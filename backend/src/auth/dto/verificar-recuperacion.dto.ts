import { IsEmail, IsNotEmpty, Matches } from 'class-validator';

// Spec 18, flujo 2 (recuperar contraseña) — sin sesión, por eso lleva el email.
export class VerificarRecuperacionDto {
  @IsEmail({}, { message: 'El email debe ser válido' })
  @IsNotEmpty({ message: 'El email es obligatorio' })
  email: string;

  @Matches(/^\d{6}$/, { message: 'El código debe tener 6 dígitos.' })
  codigo: string;
}
