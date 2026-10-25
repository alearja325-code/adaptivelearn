import { IsEmail, IsNotEmpty } from 'class-validator';

// Spec 18, sección 2.5 — "Reenviar".
export class ReenviarCodigoDto {
  @IsEmail({}, { message: 'El email debe ser válido' })
  @IsNotEmpty({ message: 'El email es obligatorio' })
  email: string;
}
