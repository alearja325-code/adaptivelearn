// Las peticiones al backend (backend/README.md; endpoints en
// docs/modesec/fase-3-diseno-computacional/20-catalogo-endpoints.md).
import type { Area, DbaDetalle, DbaResumen, Grado, RespuestaSesion, Usuario } from './tipos';

export const URL_API: string = import.meta.env.VITE_API_URL || 'http://localhost:3000';

/** Un error del backend: su código HTTP y su `message` (texto o lista de textos). */
export class ErrorApi extends Error {
  constructor(
    readonly estado: number,
    mensaje: string,
  ) {
    super(mensaje);
  }
}

/** Se llama cuando una petición con sesión responde 401: la sesión venció. */
let alVencerSesion: (() => void) | null = null;
export function registrarAlVencerSesion(fn: (() => void) | null): void {
  alVencerSesion = fn;
}

interface Opciones {
  metodo?: 'GET' | 'POST' | 'PATCH';
  token?: string | null;
  /** false: el token no es de sesión (el de recuperación); un 401 no la vence */
  deSesion?: boolean;
  cuerpo?: unknown;
  formulario?: FormData;
}

export async function pedir<T>(
  ruta: string,
  { metodo = 'GET', token, cuerpo, formulario, deSesion = true }: Opciones = {},
): Promise<T> {
  const headers: Record<string, string> = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  let body: BodyInit | undefined;
  if (formulario) body = formulario;
  else if (cuerpo !== undefined) {
    headers['Content-Type'] = 'application/json';
    body = JSON.stringify(cuerpo);
  }

  let res: Response;
  try {
    res = await fetch(URL_API + ruta, { method: metodo, headers, body });
  } catch {
    throw new ErrorApi(0, 'No se pudo conectar con el servidor. Revisa tu conexión e intenta de nuevo.');
  }

  if (res.status === 204) return undefined as T;
  const datos: unknown = await res.json().catch(() => null);
  if (!res.ok) {
    const crudo = (datos as { message?: string | string[] } | null)?.message;
    const mensaje = Array.isArray(crudo) ? crudo.join(' ') : crudo || 'Algo falló en el servidor. Intenta de nuevo.';
    if (res.status === 401 && token && deSesion && alVencerSesion) alVencerSesion();
    throw new ErrorApi(res.status, mensaje);
  }
  return datos as T;
}

/** La dirección completa de una foto de perfil guardada en el backend (/uploads/...) */
export function urlFoto(avatarUrl: string | null | undefined): string | null {
  if (!avatarUrl) return null;
  return avatarUrl.startsWith('http') ? avatarUrl : URL_API + avatarUrl;
}

// ------------------------------------------------------------- acceso (§3)
export const api = {
  registrar: (email: string, password: string) =>
    pedir<RespuestaSesion>('/auth/register', { metodo: 'POST', cuerpo: { email, password } }),
  iniciarSesion: (email: string, password: string) =>
    pedir<RespuestaSesion>('/auth/login', { metodo: 'POST', cuerpo: { email, password } }),
  perfil: (token: string) => pedir<{ user: Usuario }>('/auth/profile', { token }),
  verificarCorreo: (token: string, codigo: string) =>
    pedir<{ user: Usuario }>('/auth/verificar-correo', { metodo: 'POST', token, cuerpo: { codigo } }),
  reenviarCodigo: (email: string) =>
    pedir<{ ok: true }>('/auth/reenviar-codigo', { metodo: 'POST', cuerpo: { email } }),
  entrarConProveedor: (proveedor: 'google' | 'microsoft', tokenProveedor: string) =>
    pedir<RespuestaSesion>(`/auth/${proveedor}`, { metodo: 'POST', cuerpo: { token: tokenProveedor } }),
  elegirRol: (token: string, formulario: FormData) =>
    pedir<RespuestaSesion>('/auth/elegir-rol', { metodo: 'POST', token, formulario }),
  solicitarRecuperacion: (email: string) =>
    pedir<{ ok: true }>('/auth/recuperar-contrasena', { metodo: 'POST', cuerpo: { email } }),
  verificarRecuperacion: (email: string, codigo: string) =>
    pedir<{ token: string }>('/auth/recuperar-contrasena/verificar', { metodo: 'POST', cuerpo: { email, codigo } }),
  // El token de recuperación no es de sesión: un 401 aquí no "vence" la sesión
  nuevaContrasena: (tokenRecuperacion: string, password: string) =>
    pedir<void>('/auth/nueva-contrasena', {
      metodo: 'POST',
      cuerpo: { password },
      token: tokenRecuperacion,
      deSesion: false,
    }),
  editarPerfil: (token: string, formulario: FormData) =>
    pedir<{ user: Usuario }>('/auth/profile', { metodo: 'PATCH', token, formulario }),

  // --------------------------------------------------------- catálogo (§4.1)
  areas: (token: string) => pedir<Area[]>('/catalogo/areas', { token }),
  grados: (token: string) => pedir<Grado[]>('/catalogo/grados', { token }),
  dbas: (token: string, codigoArea: string, numeroGrado: number | null, q: string) => {
    const p = new URLSearchParams({ codigo_area: codigoArea });
    if (numeroGrado !== null) p.set('numero_grado', String(numeroGrado));
    if (q.trim()) p.set('q', q.trim());
    return pedir<DbaResumen[]>(`/catalogo/dbas?${p.toString()}`, { token });
  },
  dba: (token: string, codigo: string) => pedir<DbaDetalle>(`/catalogo/dbas/${encodeURIComponent(codigo)}`, { token }),
};
