import { createRemoteJWKSet, jwtVerify, type JWTPayload } from 'jose';
import type { IdentidadExterna, VerificadorProveedor } from './proveedor-identidad.js';

/**
 * Google (E-04). El ID token se verifica con las llaves públicas de Google
 * (JWKS): firma, emisor, audiencia (nuestro GOOGLE_CLIENT_ID) y
 * vencimiento. Solo se acepta un correo que Google marca como verificado.
 */
export class VerificadorGoogle implements VerificadorProveedor {
  private readonly jwks = createRemoteJWKSet(new URL('https://www.googleapis.com/oauth2/v3/certs'));

  constructor(private readonly clientId: string | undefined) {}

  get configurado(): boolean {
    return !!this.clientId;
  }

  async verificar(token: string): Promise<IdentidadExterna> {
    const { payload } = await jwtVerify(token, this.jwks, {
      issuer: ['https://accounts.google.com', 'accounts.google.com'],
      audience: this.clientId,
    });
    if (payload.email_verified !== true) {
      throw new Error('Google no verificó este correo');
    }
    return identidad(payload, payload.email);
  }
}

/**
 * Microsoft (E-05), cuentas personales y de organización (endpoint
 * `common`). El emisor depende del inquilino (`tid`), así que se comprueba
 * contra el `tid` del propio token, ya verificado con las llaves de Microsoft.
 */
export class VerificadorMicrosoft implements VerificadorProveedor {
  private readonly jwks = createRemoteJWKSet(
    new URL('https://login.microsoftonline.com/common/discovery/v2.0/keys'),
  );

  constructor(private readonly clientId: string | undefined) {}

  get configurado(): boolean {
    return !!this.clientId;
  }

  async verificar(token: string): Promise<IdentidadExterna> {
    const { payload } = await jwtVerify(token, this.jwks, { audience: this.clientId });
    const tid = typeof payload.tid === 'string' ? payload.tid : '';
    if (payload.iss !== `https://login.microsoftonline.com/${tid}/v2.0`) {
      throw new Error('Emisor de Microsoft inválido');
    }
    return identidad(payload, payload.email ?? payload.preferred_username);
  }
}

function identidad(payload: JWTPayload, correo: unknown): IdentidadExterna {
  if (typeof payload.sub !== 'string' || typeof correo !== 'string' || !correo.includes('@')) {
    throw new Error('El token no trae identificador o correo');
  }
  return {
    proveedorId: payload.sub,
    correo: correo.toLowerCase(),
    nombre: typeof payload.name === 'string' ? payload.name : null,
  };
}
