import { Type } from 'class-transformer';
import {
  ArrayMaxSize,
  IsArray,
  IsBoolean,
  IsIn,
  IsInt,
  IsOptional,
  IsString,
  Max,
  Min,
  ValidateNested,
} from 'class-validator';
import { MAXIMO_OPCIONES } from '../validar-item.js';

/**
 * Una opción, como la escribe el docente (E-25, E-28). Los campos son los de
 * la tabla `opcion`; qué campos usa cada formato lo revisa validarItem (RI-4).
 * hipotesis_error no se recibe: el docente no la ve (ADR-008, ADR-020).
 */
export class OpcionDto {
  @IsString()
  texto: string;

  @IsOptional()
  @IsBoolean()
  es_correcta?: boolean | null;

  @IsOptional()
  @IsInt()
  @Min(1)
  @Max(255)
  orden?: number | null;

  @IsOptional()
  @IsIn(['izquierda', 'derecha'])
  grupo?: 'izquierda' | 'derecha' | null;
}

/** E-25 PATCH /items/:id y E-28 POST /experiencias/:id/evidencias/:n/items. */
export class ItemDto {
  @IsString()
  enunciado: string;

  @IsArray()
  @ArrayMaxSize(MAXIMO_OPCIONES)
  @ValidateNested({ each: true })
  @Type(() => OpcionDto)
  opciones: OpcionDto[];
}
