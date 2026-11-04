// Botones del sistema de diseño.
//  - Primario: 014 §2.6 (CTA); Deshabilitado/Habilitado de 015 §2.3, 016 §2.5,
//    017 §2.3, 018 §2.3, 019 §2.3; hover opacidad 85% (014 §6).
//  - Ghost "Volver": 006 §2.6 y 017 §2.3; hover Fill #FAFAF8 (006 §6).
//  - En el pie de un modal, Ghost y Primario van en una rejilla de 2 columnas
//    iguales (corrección 2026-11-04: mitad y mitad en todo el sistema).
import { X } from 'lucide-react';
import type { ButtonHTMLAttributes, ReactNode } from 'react';

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
}

export function BotonPrimario({ children, disabled, className = '', ...resto }: Props) {
  const estado = disabled ? 'bg-disabled cursor-not-allowed' : 'bg-primary-ink hover:opacity-85 cursor-pointer';
  return (
    <button
      type="button"
      disabled={disabled}
      className={`h-48 w-full rounded-12 text-boton font-medium text-surface-0 ${estado} ${className}`}
      {...resto}
    >
      {children}
    </button>
  );
}

export function BotonGhost({ children, className = '', ...resto }: Props) {
  return (
    <button
      type="button"
      className={`h-48 shrink-0 rounded-12 px-24 text-boton font-medium text-secondary hover:bg-surface-1 cursor-pointer ${className}`}
      {...resto}
    >
      {children}
    </button>
  );
}

/** Botón cerrar de los modales: 32×32, Radio 8, X 16 (002 §2.1, 026 §2.1) */
export function BotonCerrar({ onClick, etiqueta = 'Cerrar' }: { onClick: () => void; etiqueta?: string }) {
  return (
    <button
      type="button"
      aria-label={etiqueta}
      onClick={onClick}
      className="flex size-32 items-center justify-center rounded-8 hover:bg-surface-1 cursor-pointer"
    >
      <X size={16} strokeWidth={1.5} className="text-muted" aria-hidden />
    </button>
  );
}

/** Enlace de texto: Caption, Bold, #111111, subrayado (014 §2.5 y §2.9) */
export function Enlace({ children, className = '', ...resto }: Props) {
  return (
    <button
      type="button"
      className={`text-caption font-bold text-primary-ink underline cursor-pointer ${className}`}
      {...resto}
    >
      {children}
    </button>
  );
}
