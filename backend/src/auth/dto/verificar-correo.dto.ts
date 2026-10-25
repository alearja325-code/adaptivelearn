import { Matches } from 'class-validator';

// Spec 18, flujo 1 (después de crear cuenta) — solo dígitos, exactamente 6.
export class VerificarCorreoDto {
  @Matches(/^\d{6}$/, { message: 'El código debe tener 6 dígitos.' })
  codigo: string;
}
