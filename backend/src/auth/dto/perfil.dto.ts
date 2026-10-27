import { Transform } from 'class-transformer';
import { IsNotEmpty, IsString, MaxLength } from 'class-validator';

const recortar = ({ value }: { value: unknown }) =>
  typeof value === 'string' ? value.trim() : value;

// Nombres y apellidos, obligatorios (RF-01-05, ventana 016).
export class PerfilDto {
  @Transform(recortar)
  @IsString({ message: 'Los nombres deben ser texto' })
  @MaxLength(120, { message: 'Los nombres son demasiado largos' })
  @IsNotEmpty({ message: 'Los nombres son obligatorios' })
  nombres: string;

  @Transform(recortar)
  @IsString({ message: 'Los apellidos deben ser texto' })
  @MaxLength(120, { message: 'Los apellidos son demasiado largos' })
  @IsNotEmpty({ message: 'Los apellidos son obligatorios' })
  apellidos: string;
}
