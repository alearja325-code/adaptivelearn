// Ayudas de las pruebas unitarias: el backend simulado y la app montada.
import { render } from '@testing-library/react';
import { MemoryRouter } from 'react-router';
import { vi } from 'vitest';
import { App } from '../App';
import type { Usuario } from '../api/tipos';
import { FlujoProveedor } from '../sesion/FlujoContexto';
import { SesionProveedor } from '../sesion/SesionContexto';

type Respuesta = { estado: number; cuerpo?: unknown };
type Manejador = (url: string, init: RequestInit) => Respuesta | undefined;

/** Reemplaza fetch: cada petición se resuelve con el primer manejador que responda */
export function backendFalso(...manejadores: Manejador[]) {
  const llamadas: { metodo: string; url: string; cuerpo: unknown }[] = [];
  const fetchFalso = vi.fn(async (entrada: string | URL | Request, init: RequestInit = {}) => {
    const url = String(entrada).replace('http://localhost:3000', '');
    const cuerpo = typeof init.body === 'string' ? JSON.parse(init.body) : init.body;
    llamadas.push({ metodo: init.method ?? 'GET', url, cuerpo });
    for (const m of manejadores) {
      const r = m(url, init);
      if (r) {
        return new Response(r.cuerpo === undefined ? null : JSON.stringify(r.cuerpo), {
          status: r.estado,
          headers: { 'Content-Type': 'application/json' },
        });
      }
    }
    return new Response(JSON.stringify({ message: `sin respuesta simulada: ${url}` }), { status: 500 });
  });
  vi.stubGlobal('fetch', fetchFalso);
  return llamadas;
}

export const ruta =
  (metodo: string, patron: string | RegExp, respuesta: Respuesta | ((init: RequestInit) => Respuesta)): Manejador =>
  (url, init) => {
    const coincide = typeof patron === 'string' ? url === patron : patron.test(url);
    if (!coincide || (init.method ?? 'GET') !== metodo) return undefined;
    return typeof respuesta === 'function' ? respuesta(init) : respuesta;
  };

export function usuario(datos: Partial<Usuario> = {}): Usuario {
  return {
    id: 1,
    email: 'ana@colegio.co',
    proveedor: 'correo',
    estadoVerificacion: 'verificado',
    idDocente: 7,
    idEstudiante: null,
    role: 'docente',
    fullName: 'Ana Pérez',
    perfil: { nombres: 'Ana', apellidos: 'Pérez', avatarUrl: null },
    ...datos,
  };
}

/** Monta la aplicación completa en una dirección, con o sin sesión guardada */
export function montar(direccion: string, { token }: { token?: string } = {}) {
  if (token) sessionStorage.setItem('adaptivelearn.token', token);
  return render(
    <MemoryRouter initialEntries={[direccion]}>
      <SesionProveedor>
        <FlujoProveedor>
          <App />
        </FlujoProveedor>
      </SesionProveedor>
    </MemoryRouter>,
  );
}
