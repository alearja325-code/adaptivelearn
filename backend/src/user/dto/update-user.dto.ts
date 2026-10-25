import { IsNotEmpty, IsOptional, IsString, IsUrl } from 'class-validator';

// Guía: PartialType(CreateUserDto) + isActive + role. Acá solo los datos de
// "Completa tu perfil" (spec 19). Sin `role`: el rol no se cambia nunca
// (spec 20). Sin `isActive`: ninguna spec define desactivar cuentas. Sin
// email/password: la contraseña tiene su propio flujo (specs 21-22).
export class UpdateUserDto {
  @IsString()
  @IsNotEmpty({ message: 'Nombres no puede estar vacío' })
  @IsOptional()
  nombres?: string;

  @IsString()
  @IsNotEmpty({ message: 'Apellidos no puede estar vacío' })
  @IsOptional()
  apellidos?: string;

  // Por ahora una URL; la subida real de archivo (JPG/PNG ≤5MB) queda pendiente.
  @IsUrl({}, { message: 'El avatar debe ser una URL válida' })
  @IsOptional()
  avatarUrl?: string;
}
