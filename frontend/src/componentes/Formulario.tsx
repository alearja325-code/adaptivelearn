// Piezas de los formularios de acceso.
//  - Campo de texto: 014 §2.3 (alto 44, Radio 12, Stroke 1 #E7E7E7, padding
//    16, gap 8, ícono 16 stroke 1.5 #888888; foco #111111; error #991B1B).
//  - Mensaje: 014 §2.6 (Caption, centrado; error #991B1B, confirmación
//    #555555 según 019 §2.4; informativo #6D28D9 según el encargo 04 §4).
import { Eye, EyeOff, type LucideIcon } from 'lucide-react';
import { useState, type InputHTMLAttributes, type ReactNode } from 'react';

interface CampoProps extends InputHTMLAttributes<HTMLInputElement> {
  icono?: LucideIcon;
  error?: boolean;
  /** Muestra el ícono de ojo para ver u ocultar (014 §2.4) */
  contrasena?: boolean;
}

export function Campo({ icono: Icono, error = false, contrasena = false, className = '', ...resto }: CampoProps) {
  const [visible, setVisible] = useState(false);
  const borde = error ? 'border-error' : 'border-border focus-within:border-primary-ink';
  return (
    <label className={`flex h-44 w-full items-center gap-8 rounded-12 borde-1 bg-surface-0 px-16 transition ${borde} ${className}`}>
      {Icono && <Icono size={16} strokeWidth={1.5} className="shrink-0 text-muted" aria-hidden />}
      <input
        {...resto}
        type={contrasena ? (visible ? 'text' : 'password') : resto.type}
        aria-invalid={error || undefined}
        className="min-w-0 flex-1 bg-transparent text-boton font-regular text-primary-ink outline-none placeholder:text-muted"
      />
      {contrasena && (
        <button
          type="button"
          onClick={() => setVisible((v) => !v)}
          aria-label={visible ? 'Ocultar contraseña' : 'Mostrar contraseña'}
          className="shrink-0 cursor-pointer"
        >
          {visible ? (
            <EyeOff size={16} strokeWidth={1.5} className="text-muted" aria-hidden />
          ) : (
            <Eye size={16} strokeWidth={1.5} className="text-muted" aria-hidden />
          )}
        </button>
      )}
    </label>
  );
}

/** Texto de ayuda bajo un campo: Caption, Regular, #888888 (014 §2.4) */
export function Ayuda({ children }: { children: ReactNode }) {
  return <p className="w-full text-caption font-regular text-muted">{children}</p>;
}

export type TipoMensaje = 'error' | 'confirmacion' | 'informativo';
const COLOR: Record<TipoMensaje, string> = {
  error: 'text-error',
  confirmacion: 'text-secondary',
  informativo: 'text-informativo',
};

/** alineacion 'izquierda': 014 §2.6 (corrección 2026-11-04); el resto, centrado */
export function Mensaje({
  texto,
  tipo = 'error',
  alineacion = 'centro',
}: {
  texto: string | null;
  tipo?: TipoMensaje;
  alineacion?: 'centro' | 'izquierda';
}) {
  if (!texto) return null;
  const alinear = alineacion === 'izquierda' ? 'text-left' : 'text-center';
  return (
    // M9: aparece bajando 4px, sin temblar (31-guia-de-movimiento.md, principio 5)
    <p key={texto} role={tipo === 'error' ? 'alert' : 'status'} className={`w-full animate-mensaje ${alinear} text-caption font-regular ${COLOR[tipo]}`}>
      {texto}
    </p>
  );
}
