import { describe, expect, it } from 'vitest';
import { leerRetorno, urlAutorizacion } from './proveedores';

// Lo que se puede probar sin credenciales reales (encargo 04 §4.6)
describe('Google y Microsoft', () => {
  it('pide un ID token con la dirección de retorno del frontend', () => {
    const url = new URL(urlAutorizacion('google', 'cliente-123', 'http://localhost:5173', 'n1'));
    expect(url.origin + url.pathname).toBe('https://accounts.google.com/o/oauth2/v2/auth');
    expect(url.searchParams.get('response_type')).toBe('id_token');
    expect(url.searchParams.get('redirect_uri')).toBe('http://localhost:5173/oauth/retorno');
    expect(url.searchParams.get('state')).toBe('google:n1');
    const ms = new URL(urlAutorizacion('microsoft', 'c', 'http://x', 'n2'));
    expect(ms.searchParams.get('response_mode')).toBe('fragment');
  });
  it('lee el ID token de la dirección de retorno', () => {
    expect(leerRetorno('#id_token=abc&state=google%3An1')).toEqual({ idToken: 'abc', state: 'google:n1', error: null });
  });
});
