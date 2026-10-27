// Ventana 019 — Auth: Nueva contraseña
// Spec: docs/modesec/fase-2-diseno-multimedial/22-spec-auth-nueva-contrasena.md
// Backend: E-10 POST /auth/nueva-contrasena, con el token de recuperación
// (que solo vive en memoria: si se recarga la página, se vuelve a 018).
import { Lock } from 'lucide-react';
import { useState } from 'react';
import { Navigate, useNavigate } from 'react-router';
import { api, ErrorApi } from '../api/cliente';
import { BotonPrimario } from '../componentes/Botones';
import { Ayuda, Campo, Mensaje } from '../componentes/Formulario';
import { Descripcion, MarcoAuth, TituloAuth } from '../componentes/MarcoAuth';
import { useFlujo } from '../sesion/FlujoContexto';
import { REGLA_CONTRASENA, TEXTO_REGLA_CONTRASENA } from '../sesion/reglas';
import { useSesion } from '../sesion/SesionContexto';

export const CONFIRMACION_CONTRASENA = 'Contraseña actualizada. Inicia sesión.';

export function V019NuevaContrasena() {
  const navegar = useNavigate();
  const { ponerAviso } = useSesion();
  const { recuperacion, setRecuperacion, setCredenciales } = useFlujo();
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  // Al terminar se borra el token de recuperación; esto evita que, en ese
  // mismo instante, la regla de abajo mande a 018 en vez de a 014
  const [terminado, setTerminado] = useState(false);

  if (!recuperacion.token && !terminado) return <Navigate to="/recuperar" replace />;
  const cumple = REGLA_CONTRASENA.test(password);

  async function guardar() {
    if (!cumple || enviando) return;
    setEnviando(true);
    try {
      await api.nuevaContrasena(recuperacion.token!, password);
      setTerminado(true);
      setRecuperacion({ email: '', token: null });
      setCredenciales({ email: recuperacion.email, password: '' });
      // §2.4: confirmación en Iniciar sesión, en #555555
      ponerAviso({ texto: CONFIRMACION_CONTRASENA, tipo: 'confirmacion' });
      navegar('/iniciar-sesion');
    } catch (e) {
      // §2.3: solo puede fallar la red, el servidor o un token vencido
      setError(e instanceof ErrorApi ? e.message : 'Algo falló. Intenta de nuevo.');
    } finally {
      setEnviando(false);
    }
  }

  return (
    <MarcoAuth>
      <TituloAuth titulo="Crea una nueva contraseña">
        <Descripcion>Se usará la próxima vez que inicies sesión.</Descripcion>
      </TituloAuth>
      <div className="flex w-full flex-col gap-8">
        <Campo
          icono={Lock}
          contrasena
          autoComplete="new-password"
          placeholder="Nueva contraseña"
          aria-label="Nueva contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Ayuda>{TEXTO_REGLA_CONTRASENA}</Ayuda>
      </div>
      <div className="flex w-full flex-col gap-8">
        <Mensaje texto={error} />
        <BotonPrimario disabled={!cumple || enviando} onClick={guardar}>
          Guardar
        </BotonPrimario>
      </div>
    </MarcoAuth>
  );
}
