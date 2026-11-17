import { Transform } from 'class-transformer';
import { IsNotEmpty, IsString, Matches, MaxLength } from 'class-validator';

/** E-19 — POST /experiencias (CU-11). Los campos, con los nombres del MR. */
export class CrearExperienciaDto {
  // Código ÁREA-GG-NN del DBA (RI-21)
  @Matches(/^(MAT|LEN|CN|CS)-\d{2}-\d{2}$/, {
    message: 'codigo_dba debe tener la forma ÁREA-GG-NN, por ejemplo MAT-08-01',
  })
  codigo_dba: string;

  // Prellenado con el enunciado del DBA en el Paso 3; obligatorio (RF-02-02)
  @Transform(({ value }: { value: unknown }) =>
    typeof value === 'string' ? value.trim() : value,
  )
  @IsString()
  @IsNotEmpty({ message: 'El nombre de la experiencia no puede estar vacío' })
  @MaxLength(160, { message: 'El nombre puede tener hasta 160 caracteres' })
  nombre: string;
}
