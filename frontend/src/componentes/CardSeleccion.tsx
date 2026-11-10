// Card de selección: 002 §2.2 (Card de área), reutilizada tal cual en 017 §2.2.
// 200×112 fijo, Radio 16, Fill #FFFFFF, Stroke 1 #E7E7E7, Padding 16, Gap 8.
// Default: ícono 24 stroke 2 #555555, label Body Medium #555555.
// Hover sin seleccionar: Fill #FAFAF8.
// Seleccionada: Fill #F5F3EE, Stroke 2 #111111, ícono stroke 2.5 #111111,
// label Bold #111111.
import type { LucideIcon } from 'lucide-react';

interface Props {
  icono: LucideIcon;
  etiqueta: string;
  seleccionada: boolean;
  onElegir: () => void;
}

export function CardSeleccion({ icono: Icono, etiqueta, seleccionada, onElegir }: Props) {
  const caja = seleccionada
    ? 'borde-2 border-primary-ink bg-surface-2'
    : 'borde-1 border-border bg-surface-0 hover:bg-surface-1';
  return (
    <button
      type="button"
      role="radio"
      aria-checked={seleccionada}
      onClick={onElegir}
      className={`flex h-112 w-200 shrink-0 cursor-pointer flex-col items-center justify-center gap-8 rounded-16 p-16 transition ${caja}`}
    >
      <Icono
        size={24}
        strokeWidth={seleccionada ? 2.5 : 2}
        className={seleccionada ? 'text-primary-ink' : 'text-secondary'}
        aria-hidden
      />
      <span className={`text-body ${seleccionada ? 'font-bold text-primary-ink' : 'font-medium text-secondary'}`}>
        {etiqueta}
      </span>
    </button>
  );
}
