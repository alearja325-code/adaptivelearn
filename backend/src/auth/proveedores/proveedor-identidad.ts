import type { ProveedorAuth } from '../../user/entities/user.entity.js';

export type ProveedorExterno = Exclude<ProveedorAuth, 'correo'>;

/** Lo que el backend toma del ID token de Google o Microsoft (CU-02). */
export interface IdentidadExterna {
  proveedorId: string; // `sub` del token: la persona en ese proveedor
  correo: string;
  nombre: string | null;
}

/**
 * Verifica un ID token de un proveedor. Dos implementaciones reales
 * (Google y Microsoft) y, en las pruebas, una simulada.
 */
export interface VerificadorProveedor {
  /** false si falta su identificador de cliente en .env */
  readonly configurado: boolean;
  /** Lanza un error si el token no es válido para esta aplicación. */
  verificar(token: string): Promise<IdentidadExterna>;
}

export const VERIFICADORES = Symbol('VERIFICADORES');
export type Verificadores = Record<ProveedorExterno, VerificadorProveedor>;

export const NOMBRE_PROVEEDOR: Record<ProveedorAuth, string> = {
  correo: 'correo y contraseña',
  google: 'Google',
  microsoft: 'Microsoft',
};
