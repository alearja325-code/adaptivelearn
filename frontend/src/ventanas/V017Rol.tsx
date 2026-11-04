// Ventana 017 — Auth: Elige tu rol
// Spec: docs/modesec/fase-2-diseno-multimedial/20-spec-auth-elige-rol.md
// Backend: E-06 POST /auth/elegir-rol (multipart: role, nombres, apellidos, foto)
import { Book, Presentation } from 'lucide-react';
import { useState } from 'react';
import { Navigate, useNavigate } from 'react-router';
import { api, ErrorApi } from '../api/cliente';
import { BotonGhost, BotonPrimario } from '../componentes/Botones';
import { CardSeleccion } from '../componentes/CardSeleccion';
import { Mensaje } from '../componentes/Formulario';
import { Descripcion, MarcoAuth, TituloAuth } from '../componentes/MarcoAuth';
import { useFlujo } from '../sesion/FlujoContexto';
import { useSesion } from '../sesion/SesionContexto';

export function V017Rol() {
  const navegar = useNavigate();
  const { token, entrar } = useSesion();
  const { perfil, setPerfil } = useFlujo();
  const [rol, setRol] = useState<'docente' | 'estudiante' | null>(null);
  const [enviando, setEnviando] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [terminado, setTerminado] = useState(false);

  // Sin el perfil de 016 (por ejemplo, al recargar aquí) no hay qué enviar
  if (!perfil && !terminado) return <Navigate to="/completar-perfil" replace />;

  async function continuar() {
    if (!rol || !perfil || enviando) return;
    const datos = new FormData();
    datos.set('role', rol);
    datos.set('nombres', perfil.nombres);
    datos.set('apellidos', perfil.apellidos);
    if (perfil.foto) datos.set('foto', perfil.foto);
    setEnviando(true);
    setError(null);
    try {
      const r = await api.elegirRol(token!, datos);
      setTerminado(true);
      await entrar(r.token);
      setPerfil(null);
      navegar('/');
    } catch (e) {
      // La spec no define un error aquí (§2.3: solo falla la red o el
      // servidor). Encargo 04 §5: nunca una pantalla en blanco; se muestra el
      // mensaje del backend en el lugar de los errores de Auth (014 §2.6).
      setError(e instanceof ErrorApi ? e.message : 'Algo falló. Intenta de nuevo.');
    } finally {
      setEnviando(false);
    }
  }

  return (
    <MarcoAuth>
      <TituloAuth titulo="Elige tu rol">
        <Descripcion>No podrás cambiarlo después.</Descripcion>
      </TituloAuth>
      <div className="flex gap-16" role="radiogroup" aria-label="Rol">
        <CardSeleccion icono={Presentation} etiqueta="Soy Docente" seleccionada={rol === 'docente'} onElegir={() => setRol('docente')} />
        <CardSeleccion icono={Book} etiqueta="Soy Estudiante" seleccionada={rol === 'estudiante'} onElegir={() => setRol('estudiante')} />
      </div>
      <div className="flex w-full flex-col gap-8">
        <Mensaje texto={error} />
        <div className="grid w-full grid-cols-2 gap-12">
          <BotonGhost onClick={() => navegar('/completar-perfil')}>Volver</BotonGhost>
          <BotonPrimario disabled={!rol || enviando} onClick={continuar}>
            Continuar
          </BotonPrimario>
        </div>
      </div>
    </MarcoAuth>
  );
}
