// Ventana 024 — Modal: Cargando (24-spec-modal-cargando.md).
// Marco chico de 412, Radio 24, Fill #FFFFFF, Stroke 1 #E7E7E7, Padding 32,
// Gap 24. Spinner `loader-circle` 32, stroke 2, #111111, girando. Título en
// gerundio, H3 Medium #111111; descripción opcional Body #555555. Sin botón
// cerrar: se cierra solo al llegar la respuesta (024 §2.1).
import { LoaderCircle } from 'lucide-react';
import { Modal } from './Modal';

export function ModalCargando({ titulo, descripcion }: { titulo: string; descripcion?: string }) {
  return (
    <Modal etiqueta={titulo}>
      <div className="flex w-412 flex-col items-center gap-24 rounded-24 borde-1 border-border bg-surface-0 p-32">
        <LoaderCircle size={32} strokeWidth={2} className="animate-spin text-primary-ink" aria-hidden />
        <div className="flex flex-col items-center gap-4 text-center">
          <p className="text-h3 font-medium text-primary-ink">{titulo}</p>
          {descripcion && <p className="text-body font-regular text-secondary">{descripcion}</p>}
        </div>
      </div>
    </Modal>
  );
}
