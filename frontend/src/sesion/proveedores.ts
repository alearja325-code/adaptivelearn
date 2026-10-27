// Entrar con Google o Microsoft (ventana 014 §2.8 y §7; E-04 y E-05).
//
// Con el identificador de cliente configurado (VITE_GOOGLE_CLIENT_ID,
// VITE_MICROSOFT_CLIENT_ID), se abre una ventana emergente del proveedor que
// devuelve un "ID token" (OpenID Connect, flujo implícito). El backend lo
// verifica con las llaves públicas del proveedor. Para que funcione hay que
// registrar en Google Cloud y en Azure la dirección de retorno
// `<dirección del frontend>/oauth/retorno` y permitir el ID token.
//
// Sin identificador (el equipo todavía no lo tiene, encargo 04 §4.6), no hay
// cómo pedirle un token al proveedor: se envía al backend un marcador con
// forma de JWT y se muestra lo que el backend responda —503 "no
// configurado" si el backend tampoco lo está—. Así el botón dice lo mismo
// que el servidor, sin inventar un texto.
export type Proveedor = 'google' | 'microsoft';

const CLIENTES: Record<Proveedor, string | undefined> = {
  google: import.meta.env.VITE_GOOGLE_CLIENT_ID,
  microsoft: import.meta.env.VITE_MICROSOFT_CLIENT_ID,
};

const AUTORIZACION: Record<Proveedor, string> = {
  google: 'https://accounts.google.com/o/oauth2/v2/auth',
  microsoft: 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
};

/** Marcador con forma de JWT (tres partes base64url) para cuando no hay cliente */
export const MARCADOR_SIN_CONFIGURAR = 'eyJhbGciOiJub25lIn0.eyJzaW5fY29uZmlndXJhciI6dHJ1ZX0.c2luLWNvbmZpZ3VyYXI';

export function configurado(proveedor: Proveedor): boolean {
  return !!CLIENTES[proveedor];
}

export function urlAutorizacion(proveedor: Proveedor, clienteId: string, origen: string, nonce: string): string {
  const p = new URLSearchParams({
    client_id: clienteId,
    response_type: 'id_token',
    scope: 'openid email profile',
    redirect_uri: `${origen}/oauth/retorno`,
    nonce,
    state: `${proveedor}:${nonce}`,
    prompt: 'select_account',
  });
  if (proveedor === 'microsoft') p.set('response_mode', 'fragment');
  return `${AUTORIZACION[proveedor]}?${p.toString()}`;
}

/** Lee el ID token de la dirección de retorno (#id_token=…&state=…) */
export function leerRetorno(hash: string): { idToken: string | null; state: string | null; error: string | null } {
  const p = new URLSearchParams(hash.replace(/^#/, ''));
  return { idToken: p.get('id_token'), state: p.get('state'), error: p.get('error') };
}

/** Devuelve el token que se le enviará al backend */
export function obtenerToken(proveedor: Proveedor): Promise<string> {
  const cliente = CLIENTES[proveedor];
  if (!cliente) return Promise.resolve(MARCADOR_SIN_CONFIGURAR);

  const nonce = crypto.randomUUID();
  const ventana = window.open(urlAutorizacion(proveedor, cliente, window.location.origin, nonce), 'adaptivelearn-oauth', 'width=480,height=640');
  return new Promise((resolver, rechazar) => {
    const alMensaje = (e: MessageEvent) => {
      if (e.origin !== window.location.origin || e.data?.tipo !== 'oauth-retorno') return;
      window.removeEventListener('message', alMensaje);
      clearInterval(vigilante);
      if (e.data.state === `${proveedor}:${nonce}` && e.data.idToken) resolver(e.data.idToken);
      else rechazar(new Error('El proveedor no entregó el inicio de sesión.'));
    };
    window.addEventListener('message', alMensaje);
    // Si la persona cierra la ventana emergente sin terminar
    const vigilante = setInterval(() => {
      if (ventana?.closed) {
        clearInterval(vigilante);
        window.removeEventListener('message', alMensaje);
        rechazar(new Error('Se canceló el inicio de sesión.'));
      }
    }, 500);
  });
}
