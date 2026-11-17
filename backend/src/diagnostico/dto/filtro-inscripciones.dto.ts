import { IsIn, IsOptional, IsString, MaxLength } from 'class-validator';
import { PROGRESOS, type Progreso } from '../reglas/progreso.js';

/** E-29: búsqueda y filtro por progreso (RF-04-01). */
export class FiltroInscripcionesDto {
  @IsOptional()
  @IsIn(PROGRESOS, {
    message: 'progreso debe ser no_iniciada, en_curso o completada',
  })
  progreso?: Progreso;

  @IsOptional()
  @IsString()
  @MaxLength(160)
  q?: string;
}
