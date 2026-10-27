// Lo que las pantallas de acceso se pasan entre sí y no se guarda en el
// navegador: solo vive en memoria mientras la pestaña está abierta.
//  - lo escrito en Crear cuenta, para que "Volver" de 015 lo devuelva
//    (ventana 015 §7). La contraseña está aquí solo en memoria: nunca en
//    el almacenamiento del navegador (encargo 04 §5);
//  - el perfil de 016, para que "Volver" de 017 lo devuelva (017 §7);
//  - el correo y el token de la recuperación (018 → 015 → 019).
import { createContext, useContext, useMemo, useState, type ReactNode } from 'react';

export interface BorradorPerfil {
  nombres: string;
  apellidos: string;
  foto: File | null;
}

interface Flujo {
  credenciales: { email: string; password: string };
  setCredenciales: (c: { email: string; password: string }) => void;
  perfil: BorradorPerfil | null;
  setPerfil: (p: BorradorPerfil | null) => void;
  recuperacion: { email: string; token: string | null };
  setRecuperacion: (r: { email: string; token: string | null }) => void;
}

const Contexto = createContext<Flujo | null>(null);

export function FlujoProveedor({ children }: { children: ReactNode }) {
  const [credenciales, setCredenciales] = useState({ email: '', password: '' });
  const [perfil, setPerfil] = useState<BorradorPerfil | null>(null);
  const [recuperacion, setRecuperacion] = useState<{ email: string; token: string | null }>({ email: '', token: null });
  const valor = useMemo(
    () => ({ credenciales, setCredenciales, perfil, setPerfil, recuperacion, setRecuperacion }),
    [credenciales, perfil, recuperacion],
  );
  return <Contexto.Provider value={valor}>{children}</Contexto.Provider>;
}

export function useFlujo(): Flujo {
  const f = useContext(Contexto);
  if (!f) throw new Error('useFlujo fuera de FlujoProveedor');
  return f;
}
