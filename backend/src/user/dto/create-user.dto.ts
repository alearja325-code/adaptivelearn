import { IsEmail, IsNotEmpty, IsOptional, IsString, Matches, MaxLength } from 'class-validator';
import { PASSWORD_REGEX, PASSWORD_MENSAJE } from '../../auth/dto/password.constants.js';

export class CreateUserDto {
  // Validación de email con formato correcto
  @IsEmail({}, { message: 'El email debe ser válido' })
  @MaxLength(254, { message: 'El email es demasiado largo' })
  @IsNotEmpty({ message: 'El email es obligatorio' })
  email: string;

  // Guía: MinLength(6). AdaptiveLearn (RF-01-01, ventana 014): mínimo 8
  // caracteres, una mayúscula y un número.
  @IsString({ message: 'La contraseña debe ser una cadena de texto' })
  @Matches(PASSWORD_REGEX, { message: PASSWORD_MENSAJE })
  @IsNotEmpty({ message: 'La contraseña es obligatoria' })
  password: string;

  // Guía: obligatorio. Acá opcional: la ventana 014 (Crear cuenta) no pide
  // nombre; nombres y apellidos se piden en la 016 (Completa tu perfil).
  @IsString({ message: 'El nombre completo debe ser una cadena de texto' })
  @MaxLength(240, { message: 'El nombre completo es demasiado largo' })
  @IsOptional()
  fullName?: string;
}
