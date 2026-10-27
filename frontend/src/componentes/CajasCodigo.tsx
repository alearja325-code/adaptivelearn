// Fila de 6 casillas de código: 015 §2.2 (reutiliza 008 §2.3).
// 48×48, Radio 12, Stroke 1 #E7E7E7, H4 Bold #111111, Gap 12; foco #111111;
// error #991B1B en las 6. Solo dígitos; el foco avanza solo, Backspace en una
// caja vacía retrocede, y pegar un código de 6 dígitos llena todas (015 §6).
import { useRef, type ClipboardEvent, type KeyboardEvent } from 'react';

interface Props {
  valor: string[];
  onCambio: (valor: string[]) => void;
  error: boolean;
}

export function CajasCodigo({ valor, onCambio, error }: Props) {
  const refs = useRef<(HTMLInputElement | null)[]>([]);

  function escribir(i: number, texto: string) {
    const digito = texto.replace(/\D/g, '').slice(-1);
    if (!digito && texto) return; // cualquier tecla que no sea un dígito se ignora
    const nuevo = [...valor];
    nuevo[i] = digito;
    onCambio(nuevo);
    if (digito && i < 5) refs.current[i + 1]?.focus();
  }

  function tecla(i: number, e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Backspace' && !valor[i] && i > 0) refs.current[i - 1]?.focus();
  }

  function pegar(e: ClipboardEvent<HTMLInputElement>) {
    const digitos = e.clipboardData.getData('text').replace(/\D/g, '');
    if (digitos.length !== 6) return;
    e.preventDefault();
    onCambio(digitos.split(''));
    refs.current[5]?.focus();
  }

  const borde = error ? 'border-error' : 'border-border focus:border-primary-ink';
  return (
    <div className="flex gap-12" role="group" aria-label="Código de 6 dígitos">
      {valor.map((d, i) => (
        <input
          key={i}
          ref={(el) => {
            refs.current[i] = el;
          }}
          value={d}
          inputMode="numeric"
          autoComplete={i === 0 ? 'one-time-code' : 'off'}
          maxLength={2}
          aria-label={`Dígito ${i + 1}`}
          onChange={(e) => escribir(i, e.target.value)}
          onKeyDown={(e) => tecla(i, e)}
          onPaste={pegar}
          className={`size-48 rounded-12 borde-1 bg-surface-0 text-center text-h4 font-bold text-primary-ink outline-none ${borde}`}
        />
      ))}
    </div>
  );
}
