import { Type } from 'class-transformer';
import { IsInt, IsNotEmpty, IsOptional, IsString, Matches, Max, MaxLength, Min } from 'class-validator';

// E-14 — filtros de GET /catalogo/dbas (CU-31, ventana 003). Los nombres son
// los del MR (`codigo_area`, `numero_grado`).
export class FiltroDbasDto {
  @Matches(/^[A-Z]{2,3}$/, { message: 'codigo_area debe ser MAT, LEN, CN o CS' })
  @IsNotEmpty({ message: 'Falta el área: codigo_area' })
  codigo_area: string;

  @Type(() => Number)
  @IsInt({ message: 'numero_grado debe ser un número de 1 a 11' })
  @Min(1, { message: 'numero_grado debe ser un número de 1 a 11' })
  @Max(11, { message: 'numero_grado debe ser un número de 1 a 11' })
  @IsOptional()
  numero_grado?: number;

  // Búsqueda por texto en el enunciado (CU-31 paso 2)
  @IsString()
  @MaxLength(100, { message: 'La búsqueda es demasiado larga' })
  @IsOptional()
  q?: string;
}
