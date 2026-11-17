import { IsIn, IsOptional, IsString, MaxLength } from 'class-validator';
import { ORDEN_GRUPOS, type EstadoGeneral } from '../reglas/clasificacion.js';

/** E-36: un grupo y búsqueda por nombre (RF-05-03). */
export class FiltroEstudiantesDto {
  @IsOptional()
  @IsIn(ORDEN_GRUPOS, {
    message:
      'estado debe ser no_muestra, no_concluyente, sin_concluir o muestra',
  })
  estado?: EstadoGeneral;

  @IsOptional()
  @IsString()
  @MaxLength(240)
  q?: string;
}
