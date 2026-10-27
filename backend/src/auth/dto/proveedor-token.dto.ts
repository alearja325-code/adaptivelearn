import { IsJWT, IsNotEmpty } from 'class-validator';

// E-04 y E-05: el ID token (un JWT) que Google o Microsoft entregó al
// frontend. El backend lo verifica con las llaves públicas del proveedor.
export class ProveedorTokenDto {
  @IsJWT({ message: 'El token del proveedor no tiene formato de JWT' })
  @IsNotEmpty({ message: 'El token es obligatorio' })
  token: string;
}
