// Ventana 014 — Auth: Iniciar sesión / Crear cuenta
// Spec: docs/modesec/fase-2-diseno-multimedial/17-spec-auth-login-registro.md
// Backend: E-07 POST /auth/login, E-01 POST /auth/register, E-04/E-05 Google y Microsoft.
import { Lock, Mail } from 'lucide-react';
import { useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router';
import { api, ErrorApi } from '../api/cliente';
import { BotonPrimario, Enlace } from '../componentes/Botones';
import { Ayuda, Campo, Mensaje, type TipoMensaje } from '../componentes/Formulario';
import { Descripcion, MarcoAuth, TituloAuth } from '../componentes/MarcoAuth';
import googleLogo from '../marcas/google.svg';
import microsoftLogo from '../marcas/microsoft.svg';
import { useFlujo } from '../sesion/FlujoContexto';
import { obtenerToken, type Proveedor } from '../sesion/proveedores';
import { destinoDe, esCorreo, REGLA_CONTRASENA, TEXTO_REGLA_CONTRASENA } from '../sesion/reglas';
import { useSesion } from '../sesion/SesionContexto';

export type Variante = 'iniciar' | 'crear';

// Textos de la spec, §3
const TEXTOS = {
  iniciar: { titulo: 'Bienvenido de vuelta', descripcion: 'Usa el correo con el que te registraste.', boton: 'Iniciar sesión', pregunta: '¿No tienes cuenta?', enlace: 'Regístrate gratis' },
  crear: { titulo: 'Crea tu cuenta', descripcion: 'Para unirte o crear experiencias.', boton: 'Crear cuenta', pregunta: '¿Ya tienes cuenta?', enlace: 'Inicia sesión' },
} as const;
export const ERROR_CREDENCIALES = 'Correo o contraseña incorrectos.';
export const ERROR_YA_EXISTE = 'Ya existe una cuenta con este correo. Inicia sesión.';
// Decisión del encargo 04, declarada: §2.3 pide un "mensaje general" para el
// correo con formato inválido, pero §2.6 no trae su texto. Se usa el de la
// ventana 018 (§2.4), la misma validación en el mismo sistema.
export const ERROR_CORREO = 'Escribe un correo válido.';

/** "Esta cuenta usa Google (o Microsoft) para entrar…" (§2.6), si el backend nombra al proveedor */
function mensajeOtroMetodo(mensaje: string): string | null {
  const proveedor = /Google/.test(mensaje) ? 'Google' : /Microsoft/.test(mensaje) ? 'Microsoft' : null;
  return proveedor ? `Esta cuenta usa ${proveedor} para entrar. Continúa con ese botón.` : null;
}

export function V014Acceso({ variante }: { variante: Variante }) {
  const t = TEXTOS[variante];
  const navegar = useNavigate();
  const { entrar, aviso, ponerAviso } = useSesion();
  const { credenciales, setCredenciales } = useFlujo();
  const [email, setEmail] = useState(credenciales.email);
  const [password, setPassword] = useState(credenciales.password);
  const [errorCorreo, setErrorCorreo] = useState(false);
  const [errorClave, setErrorClave] = useState(false);
  const [mensaje, setMensaje] = useState<{ texto: string; tipo: TipoMensaje } | null>(
    variante === 'iniciar' && aviso ? { texto: aviso.texto, tipo: aviso.tipo } : null,
  );
  const [enviando, setEnviando] = useState(false);

  // §7: el formato se valida al perder el foco, no mientras se escribe
  const alSalirCorreo = () => setErrorCorreo(email.trim() !== '' && !esCorreo(email));

  function cambiarVariante() {
    // §7: cambiar de variante no pierde lo escrito en Correo
    setCredenciales({ email, password });
    ponerAviso(null);
    navegar(variante === 'iniciar' ? '/crear-cuenta' : '/iniciar-sesion');
  }

  async function terminar(token: string) {
    ponerAviso(null);
    const usuario = await entrar(token);
    navegar(destinoDe(usuario));
  }

  async function enviar(e: FormEvent) {
    e.preventDefault();
    const correoMalo = !esCorreo(email);
    const claveMala = variante === 'crear' ? !REGLA_CONTRASENA.test(password) : password === '';
    setErrorCorreo(correoMalo);
    setErrorClave(claveMala);
    if (correoMalo) return setMensaje({ texto: ERROR_CORREO, tipo: 'error' });
    if (claveMala) {
      return setMensaje({ texto: variante === 'crear' ? TEXTO_REGLA_CONTRASENA : ERROR_CREDENCIALES, tipo: 'error' });
    }

    setEnviando(true);
    setMensaje(null);
    try {
      if (variante === 'iniciar') {
        const r = await api.iniciarSesion(email.trim(), password);
        await terminar(r.token);
      } else {
        const r = await api.registrar(email.trim(), password);
        setCredenciales({ email: email.trim(), password });
        await terminar(r.token);
      }
    } catch (error) {
      setMensaje({ texto: textoDeError(error, variante), tipo: 'error' });
    } finally {
      setEnviando(false);
    }
  }

  async function conProveedor(proveedor: Proveedor) {
    setMensaje(null);
    try {
      const tokenProveedor = await obtenerToken(proveedor);
      const r = await api.entrarConProveedor(proveedor, tokenProveedor);
      await terminar(r.token);
    } catch (error) {
      setMensaje({ texto: textoDeError(error, variante), tipo: 'error' });
    }
  }

  return (
    <MarcoAuth>
      <TituloAuth titulo={t.titulo}>
        <Descripcion>{t.descripcion}</Descripcion>
      </TituloAuth>

      <form onSubmit={enviar} noValidate className="flex w-full flex-col gap-24">
        <div className="flex w-full flex-col gap-12">
          <Campo
            icono={Mail}
            type="email"
            name="email"
            autoComplete="email"
            placeholder="Correo electrónico"
            aria-label="Correo electrónico"
            value={email}
            error={errorCorreo}
            onChange={(e) => setEmail(e.target.value)}
            onBlur={alSalirCorreo}
          />
          <div className="flex w-full flex-col gap-8">
            <Campo
              icono={Lock}
              contrasena
              name="password"
              autoComplete={variante === 'crear' ? 'new-password' : 'current-password'}
              placeholder="Contraseña"
              aria-label="Contraseña"
              value={password}
              error={errorClave}
              onChange={(e) => {
                setPassword(e.target.value);
                setErrorClave(false);
              }}
            />
            {variante === 'crear' && <Ayuda>{TEXTO_REGLA_CONTRASENA}</Ayuda>}
          </div>
          {variante === 'iniciar' && (
            <div className="flex justify-end">
              <Enlace onClick={() => navegar('/recuperar')}>¿Olvidaste tu contraseña?</Enlace>
            </div>
          )}
        </div>

        <div className="flex w-full flex-col gap-8">
          <Mensaje texto={mensaje?.texto ?? null} tipo={mensaje?.tipo} alineacion="izquierda" />
          <BotonPrimario type="submit" disabled={enviando}>
            {t.boton}
          </BotonPrimario>
        </div>
      </form>

      {/* §2.7 Divisor "o" */}
      <div className="flex w-full items-center gap-12" aria-hidden>
        <span className="h-1 flex-1 bg-border" />
        <span className="text-caption font-regular text-muted">o</span>
        <span className="h-1 flex-1 bg-border" />
      </div>

      {/* §2.8 Botones de login social: solo el logo, 20×20 */}
      <div className="flex w-full gap-12">
        <BotonSocial logo={googleLogo} nombre="Google" onClick={() => conProveedor('google')} />
        <BotonSocial logo={microsoftLogo} nombre="Microsoft" onClick={() => conProveedor('microsoft')} />
      </div>

      {/* §2.9 Enlace de cambio de variante */}
      <div className="flex items-center gap-8">
        <span className="text-caption font-regular text-secondary">{t.pregunta}</span>
        <Enlace onClick={cambiarVariante}>{t.enlace}</Enlace>
      </div>
    </MarcoAuth>
  );
}

function BotonSocial({ logo, nombre, onClick }: { logo: string; nombre: string; onClick: () => void }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={`Continuar con ${nombre}`}
      className="flex h-48 flex-1 cursor-pointer items-center justify-center rounded-12 borde-1 border-border bg-surface-0 hover:bg-surface-1"
    >
      <img src={logo} alt="" className="size-20" />
    </button>
  );
}

/** El texto de la spec para cada error del backend; si no hay, el `message` del backend */
export function textoDeError(error: unknown, variante: Variante): string {
  if (!(error instanceof ErrorApi)) {
    return error instanceof Error ? error.message : 'Algo falló. Intenta de nuevo.';
  }
  if (error.estado === 409) {
    return mensajeOtroMetodo(error.message) ?? (variante === 'crear' ? ERROR_YA_EXISTE : error.message);
  }
  if (error.estado === 401 && variante === 'iniciar' && error.message === 'Credenciales inválidas') {
    return ERROR_CREDENCIALES;
  }
  return error.message;
}
