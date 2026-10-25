import { IsEmail, IsNotEmpty, IsOptional, IsString, Matches } from 'class-validator';
import { PASSWORD_REGEX, PASSWORD_MENSAJE } from './password.constants.js';

export class RegisterDto {
  @IsEmail({}, { message: 'El email debe ser válido' })
  @IsNotEmpty({ message: 'El email es obligatorio' })
  email: string;

  // Guía: MinLength(6). Spec 17: mínimo 8, una mayúscula y un número.
  @IsString({ message: 'La contraseña debe ser una cadena de texto' })
  @Matches(PASSWORD_REGEX, { message: PASSWORD_MENSAJE })
  @IsNotEmpty({ message: 'La contraseña es obligatoria' })
  password: string;

  // Guía: obligatorio. Acá opcional: la pantalla de registro (spec 17) no
  // pide nombre — se pide después, en "Completa tu perfil" (spec 19).
  @IsString({ message: 'El nombre completo debe ser una cadena de texto' })
  @IsOptional()
  fullName?: string;
}
