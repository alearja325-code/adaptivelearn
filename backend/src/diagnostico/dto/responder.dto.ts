import { Type } from 'class-transformer';
import {
  ArrayMaxSize,
  ArrayMinSize,
  IsArray,
  IsInt,
  IsOptional,
  Max,
  Min,
  ValidateNested,
} from 'class-validator';

/** Una fila de `respuesta_opcion` (ADR-019). */
export class OpcionElegidaDto {
  @IsInt({ message: 'id_opcion debe ser un número entero' })
  @Min(1)
  id_opcion: number;

  /** Posición (ordenar) o número de pareja (emparejar); sin valor en selección única. */
  @IsOptional()
  @IsInt({ message: 'valor_dado debe ser un número entero' })
  @Min(1)
  @Max(255)
  valor_dado?: number | null;
}

/** E-33: la respuesta a la pregunta pendiente (CU-24). */
export class ResponderDto {
  @IsInt({ message: 'id_item debe ser un número entero' })
  @Min(1)
  id_item: number;

  @IsArray({ message: 'opciones debe ser una lista' })
  @ArrayMinSize(1, { message: 'Elige una respuesta' })
  @ArrayMaxSize(50)
  @ValidateNested({ each: true })
  @Type(() => OpcionElegidaDto)
  opciones: OpcionElegidaDto[];

  // ADR-028 punto 3 y ADR-008 punto 2: escala CRI de 0 a 5
  @IsInt({ message: 'La certeza va de 0 a 5' })
  @Min(0, { message: 'La certeza va de 0 a 5' })
  @Max(5, { message: 'La certeza va de 0 a 5' })
  certeza: number;
}
