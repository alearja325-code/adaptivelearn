// Contenedor de los modales (002 §2.1, 024 §2.1, 026 §2.1): centrado sobre la
// pantalla donde está la persona.
// Decisión del encargo 04, declarada: ninguna spec define el fondo detrás de
// un modal. Se usa #111111 al 60% de opacidad, la misma capa ya aprobada para
// el hover del avatar (016 §2.2): no agrega ningún color ni opacidad nuevos.
import { useEffect, type ReactNode } from 'react';

interface Props {
  etiqueta: string;
  children: ReactNode;
  /** Escape cierra (si el modal se puede cerrar; 024 no se puede) */
  onCerrar?: () => void;
}

export function Modal({ etiqueta, children, onCerrar }: Props) {
  useEffect(() => {
    if (!onCerrar) return;
    const alTeclear = (e: KeyboardEvent) => e.key === 'Escape' && onCerrar();
    window.addEventListener('keydown', alTeclear);
    return () => window.removeEventListener('keydown', alTeclear);
  }, [onCerrar]);

  return (
    // M4 (31-guia-de-movimiento.md): el fondo aparece por opacidad y el panel sube
    // y crece al entrar. M5: al cerrar, desaparece al instante (sin animación).
    <div className="fixed inset-0 z-10 flex animate-fondo items-center justify-center bg-primary-ink/60 p-24">
      <div role="dialog" aria-modal="true" aria-label={etiqueta} className="flex max-h-full animate-modal">
        {children}
      </div>
    </div>
  );
}

/**
 * Encabezado de 3 zonas (002 §2.1): el título queda centrado en el ancho
 * completo. La spec sugiere una rejilla `1fr auto 1fr`; aquí son dos zonas
 * laterales que crecen igual (flex-1), que da el mismo centrado sin un
 * valor arbitrario.
 */
export function EncabezadoModal({ titulo, cerrar }: { titulo: string; cerrar: ReactNode }) {
  return (
    <div className="flex w-full items-center">
      <span className="flex-1" aria-hidden />
      <h2 className="text-h2 font-bold text-primary-ink">{titulo}</h2>
      <div className="flex flex-1 justify-end">{cerrar}</div>
    </div>
  );
}
