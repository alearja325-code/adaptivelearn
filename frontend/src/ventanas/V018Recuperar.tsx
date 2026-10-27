// Ventana 018 — Auth: Recupera tu contraseña
// Spec: docs/modesec/fase-2-diseno-multimedial/21-spec-auth-recupera-contrasena.md
// Backend: E-08 POST /auth/recuperar-contrasena (responde igual exista o no
// la cuenta: la pantalla siempre avanza, RNF-07)
import { Mail } from 'lucide-react';
import { useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router';
import { api, ErrorApi } from '../api/cliente';
import { BotonPrimario, Enlace } from '../componentes/Botones';
import { Campo, Mensaje } from '../componentes/Formulario';
import { Descripcion, MarcoAuth, TituloAuth } from '../componentes/MarcoAuth';
import { useFlujo } from '../sesion/FlujoContexto';
import { esCorreo } from '../sesion/reglas';

export function V018Recuperar() {
  const navegar = useNavigate();
  const { recuperacion, setRecuperacion } = useFlujo();
  const [email, setEmail] = useState(recuperacion.email);
  const [errorCorreo, setErrorCorreo] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  // §6: el botón se habilita con validación continua; el borde rojo espera
  // a que el campo pierda el foco (§7: son dos comprobaciones distintas)
  const valido = esCorreo(email);

  async function enviar(e: FormEvent) {
    e.preventDefault();
    if (!valido) {
      setErrorCorreo(true);
      setError('Escribe un correo válido.');
      return;
    }
    setEnviando(true);
    try {
      await api.solicitarRecuperacion(email.trim());
      setRecuperacion({ email: email.trim(), token: null });
      navegar('/recuperar/verificar');
    } catch (e) {
      setError(e instanceof ErrorApi ? e.message : 'Algo falló. Intenta de nuevo.');
    } finally {
      setEnviando(false);
    }
  }

  return (
    <MarcoAuth>
      <TituloAuth titulo="¿Olvidaste tu contraseña?">
        <Descripcion>Te enviaremos un código a tu correo.</Descripcion>
      </TituloAuth>
      <form onSubmit={enviar} noValidate className="flex w-full flex-col gap-24">
        <Campo
          icono={Mail}
          type="email"
          autoComplete="email"
          placeholder="Correo electrónico"
          aria-label="Correo electrónico"
          value={email}
          error={errorCorreo}
          onChange={(e) => {
            setEmail(e.target.value);
            setError(null);
          }}
          onBlur={() => {
            const malo = email.trim() !== '' && !esCorreo(email);
            setErrorCorreo(malo);
            setError(malo ? 'Escribe un correo válido.' : null);
          }}
        />
        <div className="flex w-full flex-col gap-8">
          <Mensaje texto={error} />
          <BotonPrimario type="submit" disabled={!valido || enviando}>
            Enviar código
          </BotonPrimario>
        </div>
      </form>
      <Enlace onClick={() => navegar('/iniciar-sesion')}>Volver a inicio de sesión</Enlace>
    </MarcoAuth>
  );
}
