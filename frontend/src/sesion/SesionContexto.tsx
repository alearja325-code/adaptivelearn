// La sesión: el token, la cuenta (GET /auth/profile) y el aviso que muestra
// la ventana 014 al llegar (sesión vencida o contraseña actualizada).
import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import { api, registrarAlVencerSesion } from '../api/cliente';
import type { Usuario } from '../api/tipos';
import { guardarToken, leerToken } from './almacen';

export interface Aviso {
  texto: string;
  /** confirmacion: #555555 (ventana 019 §2.4); error: #991B1B */
  tipo: 'confirmacion' | 'error';
}

// Decisión del encargo 04, declarada: el texto de "sesión vencida" no está
// en ninguna spec. Va en el lugar del mensaje de la ventana 014 (§2.6), en
// Secondary como la confirmación de 019: no es un error de la persona.
export const AVISO_SESION_VENCIDA: Aviso = { texto: 'Tu sesión terminó. Inicia sesión de nuevo.', tipo: 'confirmacion' };

interface Sesion {
  token: string | null;
  usuario: Usuario | null;
  /** true mientras se consulta la cuenta al abrir o recargar la página */
  cargando: boolean;
  aviso: Aviso | null;
  /** Guarda el token y trae la cuenta; devuelve la cuenta */
  entrar: (token: string) => Promise<Usuario>;
  recargar: () => Promise<Usuario | null>;
  cerrar: (aviso?: Aviso | null) => void;
  ponerAviso: (aviso: Aviso | null) => void;
}

const Contexto = createContext<Sesion | null>(null);

export function SesionProveedor({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => leerToken());
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [cargando, setCargando] = useState<boolean>(() => leerToken() !== null);
  const [aviso, setAviso] = useState<Aviso | null>(null);

  const cerrar = useCallback((nuevoAviso: Aviso | null = null) => {
    guardarToken(null);
    setToken(null);
    setUsuario(null);
    setCargando(false);
    setAviso(nuevoAviso);
  }, []);

  // Encargo 04 §5: una sesión vencida (401) lleva a 014 sin perder el aviso
  useEffect(() => {
    registrarAlVencerSesion(() => cerrar(AVISO_SESION_VENCIDA));
    return () => registrarAlVencerSesion(null);
  }, [cerrar]);

  const entrar = useCallback(async (nuevo: string) => {
    guardarToken(nuevo);
    setToken(nuevo);
    const { user } = await api.perfil(nuevo);
    setUsuario(user);
    setAviso(null);
    return user;
  }, []);

  const recargar = useCallback(async () => {
    if (!token) return null;
    const { user } = await api.perfil(token);
    setUsuario(user);
    return user;
  }, [token]);

  // Al abrir o recargar la página con un token guardado: traer la cuenta
  useEffect(() => {
    const guardado = leerToken();
    if (!guardado) return;
    api
      .perfil(guardado)
      .then(({ user }) => setUsuario(user))
      .catch(() => cerrar(AVISO_SESION_VENCIDA))
      .finally(() => setCargando(false));
  }, [cerrar]);

  const valor = useMemo(
    () => ({ token, usuario, cargando, aviso, entrar, recargar, cerrar, ponerAviso: setAviso }),
    [token, usuario, cargando, aviso, entrar, recargar, cerrar],
  );
  return <Contexto.Provider value={valor}>{children}</Contexto.Provider>;
}

export function useSesion(): Sesion {
  const s = useContext(Contexto);
  if (!s) throw new Error('useSesion fuera de SesionProveedor');
  return s;
}
