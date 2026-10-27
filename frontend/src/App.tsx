// Las rutas de esta etapa (encargo 04 §3) y el camino de una cuenta según el
// backend (§5): sin sesión → 014; sin verificar → 015; verificada sin rol →
// 016; con rol → 001. Vale al iniciar sesión y al recargar la página.
import type { ReactNode } from 'react';
import { Navigate, Route, Routes } from 'react-router';
import { ModalCargando } from './componentes/ModalCargando';
import { destinoDe } from './sesion/reglas';
import { useSesion } from './sesion/SesionContexto';
import { RetornoOAuth } from './ventanas/RetornoOAuth';
import { V001Dashboard } from './ventanas/V001Dashboard';
import { V014Acceso } from './ventanas/V014Acceso';
import { V015Verificar } from './ventanas/V015Verificar';
import { V016Perfil } from './ventanas/V016Perfil';
import { V017Rol } from './ventanas/V017Rol';
import { V018Recuperar } from './ventanas/V018Recuperar';
import { V019NuevaContrasena } from './ventanas/V019NuevaContrasena';

type Paso = '/verificar-correo' | '/completar-perfil' | '/';

/**
 * Deja pasar solo si la cuenta está en el paso `paso`; si no, la lleva a
 * donde le corresponde. Sin sesión, a Iniciar sesión.
 */
function EnPaso({ paso, children }: { paso: Paso | Paso[]; children: ReactNode }) {
  const { token, usuario, cargando } = useSesion();
  // Decisión del encargo 04, declarada: mientras se consulta la cuenta al
  // recargar, se muestra el Modal: Cargando (024) — nunca una pantalla en blanco.
  if (cargando) return <ModalCargando titulo="Abriendo tu sesión..." />;
  if (!token || !usuario) return <Navigate to="/iniciar-sesion" replace />;
  const destino = destinoDe(usuario);
  const permitidos = Array.isArray(paso) ? paso : [paso];
  return permitidos.includes(destino) ? <>{children}</> : <Navigate to={destino} replace />;
}

/** Las pantallas sin sesión: con una sesión ya abierta, se va a su paso. */
function SinSesion({ children }: { children: ReactNode }) {
  const { token, usuario, cargando } = useSesion();
  if (cargando) return <ModalCargando titulo="Abriendo tu sesión..." />;
  if (token && usuario) return <Navigate to={destinoDe(usuario)} replace />;
  return <>{children}</>;
}

export function App() {
  return (
    <Routes>
      <Route path="/iniciar-sesion" element={<SinSesion><V014Acceso variante="iniciar" /></SinSesion>} />
      <Route path="/crear-cuenta" element={<SinSesion><V014Acceso variante="crear" /></SinSesion>} />
      <Route path="/recuperar" element={<SinSesion><V018Recuperar /></SinSesion>} />
      <Route path="/recuperar/verificar" element={<SinSesion><V015Verificar flujo="recuperacion" /></SinSesion>} />
      <Route path="/nueva-contrasena" element={<SinSesion><V019NuevaContrasena /></SinSesion>} />
      <Route path="/verificar-correo" element={<EnPaso paso="/verificar-correo"><V015Verificar flujo="registro" /></EnPaso>} />
      <Route path="/completar-perfil" element={<EnPaso paso="/completar-perfil"><V016Perfil /></EnPaso>} />
      <Route path="/elegir-rol" element={<EnPaso paso="/completar-perfil"><V017Rol /></EnPaso>} />
      <Route path="/" element={<EnPaso paso="/"><V001Dashboard /></EnPaso>} />
      <Route path="/oauth/retorno" element={<RetornoOAuth />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
