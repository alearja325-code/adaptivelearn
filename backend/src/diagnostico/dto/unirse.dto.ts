import { IsNotEmpty, IsString, MaxLength } from 'class-validator';

/** E-30: el código de invitación, sin distinguir mayúsculas (CU-22). */
export class UnirseDto {
  @IsString({ message: 'Escribe el código de la experiencia' })
  @IsNotEmpty({ message: 'Escribe el código de la experiencia' })
  @MaxLength(20, { message: 'El código tiene 6 caracteres' })
  codigo: string;
}
