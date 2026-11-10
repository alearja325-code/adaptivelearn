// Selector de avatar: 016 §2.2 (reutilizado en 026 §2.2).
// Círculo 96×96, Radio 999. Sin foto: Fill #E7E7E7 con `image-up` 32,
// stroke 1.5, #888888. Con foto: la imagen llena el círculo, recorte
// centrado. Hover: capa #111111 al 60% con `camera` 24, stroke 1.5, #FFFFFF.
// Archivo inválido: "Solo imágenes JPG o PNG, máximo 5 MB." (Caption,
// #991B1B, centrado) y el avatar no cambia.
import { Camera, ImageUp } from 'lucide-react';
import { useEffect, useMemo, useRef, useState } from 'react';
import { fotoValida } from '../sesion/reglas';
import { Mensaje } from './Formulario';

export const ERROR_FOTO = 'Solo imágenes JPG o PNG, máximo 5 MB.';

interface Props {
  /** Foto recién elegida (aún no guardada) */
  archivo: File | null;
  /** Foto ya guardada en la cuenta (026) */
  urlActual?: string | null;
  onElegir: (archivo: File) => void;
}

export function SelectorAvatar({ archivo, urlActual = null, onElegir }: Props) {
  const entrada = useRef<HTMLInputElement>(null);
  const [error, setError] = useState(false);
  const vistaPrevia = useMemo(() => (archivo ? URL.createObjectURL(archivo) : null), [archivo]);
  useEffect(() => () => {
    if (vistaPrevia) URL.revokeObjectURL(vistaPrevia);
  }, [vistaPrevia]);
  const imagen = vistaPrevia ?? urlActual;

  function alElegir(lista: FileList | null) {
    const f = lista?.[0];
    if (!f) return;
    if (!fotoValida(f)) {
      setError(true);
      return;
    }
    setError(false);
    onElegir(f);
  }

  return (
    <div className="flex flex-col items-center gap-8">
      <button
        type="button"
        onClick={() => entrada.current?.click()}
        aria-label="Elegir foto de perfil"
        className="group relative flex size-96 cursor-pointer items-center justify-center overflow-hidden rounded-999 bg-border"
      >
        {imagen ? (
          <img src={imagen} alt="Foto de perfil" className="size-96 object-cover object-center" />
        ) : (
          <ImageUp size={32} strokeWidth={1.5} className="text-muted" aria-hidden />
        )}
        <span className="absolute inset-0 flex items-center justify-center rounded-999 bg-primary-ink/60 opacity-0 transition group-hover:opacity-100">
          <Camera size={24} strokeWidth={1.5} className="text-surface-0" aria-hidden />
        </span>
      </button>
      <input
        ref={entrada}
        type="file"
        accept="image/jpeg,image/png"
        className="hidden"
        data-testid="entrada-foto"
        onChange={(e) => {
          alElegir(e.target.files);
          e.target.value = '';
        }}
      />
      <Mensaje texto={error ? ERROR_FOTO : null} />
    </div>
  );
}
