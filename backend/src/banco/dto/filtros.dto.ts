import { IsIn, IsOptional, IsString, MaxLength } from 'class-validator';

/** E-18 — GET /experiencias?estado=borrador&q=texto (RF-02-01). */
export class FiltroExperienciasDto {
  @IsOptional()
  @IsIn(['borrador', 'publicada'], {
    message: 'estado debe ser borrador o publicada',
  })
  estado?: 'borrador' | 'publicada';

  @IsOptional()
  @IsString()
  @MaxLength(160)
  q?: string;
}

/** E-24 — GET /experiencias/:id/banco?formato=matching&q=texto (RF-03-04). */
export class FiltroBancoDto {
  @IsOptional()
  @IsIn(['single_choice', 'matching', 'ordering'], {
    message: 'formato debe ser single_choice, matching u ordering',
  })
  formato?: 'single_choice' | 'matching' | 'ordering';

  @IsOptional()
  @IsString()
  @MaxLength(200)
  q?: string;
}
