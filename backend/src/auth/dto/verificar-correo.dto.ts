import { Matches } from 'class-validator';

// Ventana 015 (después de crear cuenta): solo dígitos, exactamente 6.
export class VerificarCorreoDto {
  @Matches(/^\d{6}$/, { message: 'El código debe tener 6 dígitos.' })
  codigo: string;
}
