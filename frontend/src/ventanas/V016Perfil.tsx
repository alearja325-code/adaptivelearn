// Ventana 016 — Auth: Completa tu perfil
// Spec: docs/modesec/fase-2-diseno-multimedial/19-spec-auth-completa-perfil.md
// No llama al backend: el perfil se envía junto con el rol en la 017 (E-06).
import { User } from 'lucide-react';
import { useState } from 'react';
import { useNavigate } from 'react-router';
import { BotonPrimario } from '../componentes/Botones';
import { Campo } from '../componentes/Formulario';
import { Descripcion, MarcoAuth, TituloAuth } from '../componentes/MarcoAuth';
import { SelectorAvatar } from '../componentes/SelectorAvatar';
import { useFlujo } from '../sesion/FlujoContexto';
import { partirNombre } from '../sesion/reglas';
import { useSesion } from '../sesion/SesionContexto';

export function V016Perfil() {
  const navegar = useNavigate();
  const { usuario } = useSesion();
  const { perfil, setPerfil } = useFlujo();
  // Lo ya escrito (al volver de 017) o, si no, el nombre que dio Google,
  // Microsoft o el registro (§2.3, §2.4)
  const inicial = perfil ?? { ...partirNombre(usuario?.fullName ?? null), foto: null };
  const [nombres, setNombres] = useState(inicial.nombres);
  const [apellidos, setApellidos] = useState(inicial.apellidos);
  const [foto, setFoto] = useState<File | null>(inicial.foto);

  const listo = nombres.trim() !== '' && apellidos.trim() !== '';

  function continuar() {
    if (!listo) return;
    setPerfil({ nombres: nombres.trim(), apellidos: apellidos.trim(), foto });
    navegar('/elegir-rol');
  }

  return (
    <MarcoAuth>
      <TituloAuth titulo="Completa tu perfil">
        <Descripcion>Así te reconocen tu docente o tus estudiantes.</Descripcion>
      </TituloAuth>
      <SelectorAvatar archivo={foto} onElegir={setFoto} />
      <div className="flex w-full flex-col gap-12">
        <Campo icono={User} placeholder="Nombres" aria-label="Nombres" value={nombres} maxLength={120} onChange={(e) => setNombres(e.target.value)} />
        <Campo icono={User} placeholder="Apellidos" aria-label="Apellidos" value={apellidos} maxLength={120} onChange={(e) => setApellidos(e.target.value)} />
      </div>
      <BotonPrimario disabled={!listo} onClick={continuar}>
        Continuar
      </BotonPrimario>
    </MarcoAuth>
  );
}
