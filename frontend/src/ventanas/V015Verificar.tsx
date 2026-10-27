// Ventana 015 — Auth: Verifica tu correo
// Spec: docs/modesec/fase-2-diseno-multimedial/18-spec-auth-verifica-correo.md
// Dos flujos (spec, "Se abre desde"):
//  - registro: E-02 POST /auth/verificar-correo, E-03 POST /auth/reenviar-codigo
//  - recuperación: E-09 POST /auth/recuperar-contrasena/verificar; reenviar
//    es pedir otra vez E-08 POST /auth/recuperar-contrasena
import { useEffect, useState } from 'react';
import { flushSync } from 'react-dom';
import { Navigate, useNavigate } from 'react-router';
import { api, ErrorApi } from '../api/cliente';
import { BotonPrimario, Enlace } from '../componentes/Botones';
import { CajasCodigo } from '../componentes/CajasCodigo';
import { Mensaje } from '../componentes/Formulario';
import { Descripcion, MarcoAuth, TituloAuth } from '../componentes/MarcoAuth';
import { useFlujo } from '../sesion/FlujoContexto';
import { useSesion } from '../sesion/SesionContexto';

export const ERROR_CODIGO = 'Código incorrecto. Revisa que esté bien escrito.';
const SEGUNDOS_ESPERA = 30; // RF-01-03

/** "00:29" */
function reloj(segundos: number): string {
  return `00:${String(segundos).padStart(2, '0')}`;
}

export function V015Verificar({ flujo }: { flujo: 'registro' | 'recuperacion' }) {
  const navegar = useNavigate();
  const { token, usuario, recargar, cerrar } = useSesion();
  const { recuperacion, setRecuperacion } = useFlujo();
  const [codigo, setCodigo] = useState<string[]>(['', '', '', '', '', '']);
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const [espera, setEspera] = useState(SEGUNDOS_ESPERA);

  // §2.5: cuenta regresiva de 30 s antes de poder reenviar
  useEffect(() => {
    if (espera <= 0) return;
    const id = setTimeout(() => setEspera((s) => s - 1), 1000);
    return () => clearTimeout(id);
  }, [espera]);

  const email = flujo === 'registro' ? usuario?.email : recuperacion.email;
  if (!email) return <Navigate to={flujo === 'registro' ? '/iniciar-sesion' : '/recuperar'} replace />;

  const completo = codigo.every((d) => d !== '');

  async function verificar() {
    if (!completo || enviando) return;
    setEnviando(true);
    try {
      if (flujo === 'registro') {
        await api.verificarCorreo(token!, codigo.join(''));
        await recargar();
        navegar('/completar-perfil');
      } else {
        const r = await api.verificarRecuperacion(recuperacion.email, codigo.join(''));
        setRecuperacion({ email: recuperacion.email, token: r.token });
        navegar('/nueva-contrasena');
      }
    } catch (e) {
      // §2.4: el texto de la spec para el código incorrecto; para los casos que la
      // spec no tiene (código vencido, 5 intentos), el mensaje del backend
      const msg = e instanceof ErrorApi ? e.message : 'Algo falló. Intenta de nuevo.';
      setError(msg.startsWith('Código incorrecto') ? ERROR_CODIGO : msg);
    } finally {
      setEnviando(false);
    }
  }

  async function reenviar() {
    setEspera(SEGUNDOS_ESPERA);
    try {
      if (flujo === 'registro') await api.reenviarCodigo(email!);
      else await api.solicitarRecuperacion(email!);
    } catch (e) {
      setError(e instanceof ErrorApi ? e.message : 'Algo falló. Intenta de nuevo.');
    }
  }

  function volver() {
    if (flujo === 'registro') {
      // §7: vuelve a Crear cuenta con el correo y la contraseña ya escritos
      // (siguen en memoria, en FlujoContexto). La sesión del registro se cierra
      // primero, del todo (flushSync), y se navega al final: si no, la regla de
      // rutas de esta ventana, que exige sesión, mandaría a Iniciar sesión.
      flushSync(() => cerrar());
      navegar('/crear-cuenta', { replace: true });
    } else {
      navegar('/recuperar');
    }
  }

  return (
    <MarcoAuth>
      <TituloAuth titulo="Verifica tu correo">
        <Descripcion>Enviamos un código de 6 dígitos a</Descripcion>
        <p className="w-full truncate text-body font-bold text-primary-ink" data-testid="correo-verificar">
          {email}
        </p>
      </TituloAuth>

      <CajasCodigo valor={codigo} onCambio={setCodigo} error={error !== null} />

      <div className="flex w-full flex-col gap-8">
        <Mensaje texto={error} />
        <BotonPrimario disabled={!completo || enviando} onClick={verificar}>
          Verificar
        </BotonPrimario>
      </div>

      <div className="flex items-center gap-8">
        <span className="text-caption font-regular text-secondary">¿No recibiste el código?</span>
        {espera > 0 ? (
          <span className="text-caption font-regular text-muted" aria-disabled="true">
            Reenviar ({reloj(espera)})
          </span>
        ) : (
          <Enlace onClick={reenviar}>Reenviar</Enlace>
        )}
      </div>

      <Enlace onClick={volver}>Volver</Enlace>
    </MarcoAuth>
  );
}
