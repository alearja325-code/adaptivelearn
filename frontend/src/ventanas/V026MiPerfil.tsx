// Ventana 026 — Modal: Mi perfil
// Spec: docs/modesec/fase-2-diseno-multimedial/26-spec-modal-mi-perfil.md
// Backend: E-12 PATCH /auth/profile (multipart: nombres, apellidos, foto)
import { User } from 'lucide-react';
import { useState } from 'react';
import { api, ErrorApi, urlFoto } from '../api/cliente';
import { BotonCerrar, BotonPrimario } from '../componentes/Botones';
import { Campo, Mensaje } from '../componentes/Formulario';
import { EncabezadoModal, Modal } from '../componentes/Modal';
import { ModalCargando } from '../componentes/ModalCargando';
import { SelectorAvatar } from '../componentes/SelectorAvatar';
import { useSesion } from '../sesion/SesionContexto';

export function V026MiPerfil({ onCerrar }: { onCerrar: () => void }) {
  const { token, usuario, recargar } = useSesion();
  const actual = usuario!.perfil!;
  const [nombres, setNombres] = useState(actual.nombres);
  const [apellidos, setApellidos] = useState(actual.apellidos);
  const [foto, setFoto] = useState<File | null>(null);
  const [guardando, setGuardando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // §2.4: habilitado solo si hay al menos un cambio y los 2 campos tienen contenido
  const hayCambios = nombres.trim() !== actual.nombres || apellidos.trim() !== actual.apellidos || foto !== null;
  const habilitado = hayCambios && nombres.trim() !== '' && apellidos.trim() !== '';

  async function guardar() {
    if (!habilitado) return;
    const datos = new FormData();
    if (nombres.trim() !== actual.nombres) datos.set('nombres', nombres.trim());
    if (apellidos.trim() !== actual.apellidos) datos.set('apellidos', apellidos.trim());
    if (foto) datos.set('foto', foto);
    setGuardando(true);
    setError(null);
    try {
      await api.editarPerfil(token!, datos);
      await recargar(); // §7: el Sidebar se actualiza con los datos nuevos
      onCerrar();
    } catch (e) {
      // La spec no define un error de guardado; se muestra el del backend
      // en el lugar de los mensajes de Auth (decisión declarada, encargo 04)
      setError(e instanceof ErrorApi ? e.message : 'Algo falló. Intenta de nuevo.');
    } finally {
      setGuardando(false);
    }
  }

  // §7: mientras guarda, el Modal: Cargando (024) con "Guardando tu perfil..."
  if (guardando) return <ModalCargando titulo="Guardando tu perfil..." />;

  return (
    <Modal etiqueta="Mi perfil" onCerrar={onCerrar}>
      <div className="flex w-480 flex-col items-center gap-24 overflow-y-auto rounded-24 borde-1 border-border bg-surface-0 p-32">
        <div className="flex w-full flex-col items-center gap-4 text-center">
          <EncabezadoModal titulo="Mi perfil" cerrar={<BotonCerrar onClick={onCerrar} />} />
          <p className="text-body font-regular text-secondary">Así te reconocen tu docente o tus estudiantes.</p>
        </div>
        <div className="flex flex-col items-center gap-8">
          <SelectorAvatar archivo={foto} urlActual={urlFoto(actual.avatarUrl)} onElegir={setFoto} />
          <p className="text-caption font-regular text-muted">{usuario!.email}</p>
        </div>
        <div className="flex w-full flex-col gap-12">
          <Campo icono={User} placeholder="Nombres" aria-label="Nombres" value={nombres} maxLength={120} onChange={(e) => setNombres(e.target.value)} />
          <Campo icono={User} placeholder="Apellidos" aria-label="Apellidos" value={apellidos} maxLength={120} onChange={(e) => setApellidos(e.target.value)} />
        </div>
        <div className="flex w-full flex-col gap-8">
          <Mensaje texto={error} />
          <BotonPrimario disabled={!habilitado} onClick={guardar}>
            Guardar cambios
          </BotonPrimario>
        </div>
      </div>
    </Modal>
  );
}
