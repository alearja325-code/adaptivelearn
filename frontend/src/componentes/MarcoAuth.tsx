// Marco de las pantallas de acceso: 014 §2.1 (heredado por 015 a 019).
// Fondo Canvas #F7F6F3 a pantalla completa, card centrada de 480 de ancho,
// Radio 24, Fill #FFFFFF, Stroke 1 #E7E7E7, Padding 32, Gap 24.
// Título + descripción: 014 §2.2 (H2 Bold #111111 / Body #555555, Gap 4).
import type { ReactNode } from 'react';

export function MarcoAuth({ children }: { children: ReactNode }) {
  return (
    <main className="flex min-h-screen items-center justify-center bg-canvas p-24 font-sans">
      <section className="flex w-480 flex-col items-center gap-24 rounded-24 borde-1 border-border bg-surface-0 p-32">
        {children}
      </section>
    </main>
  );
}

export function TituloAuth({ titulo, children }: { titulo: string; children?: ReactNode }) {
  return (
    <header className="flex w-full flex-col items-center gap-4 text-center">
      <h1 className="text-h2 font-bold text-primary-ink">{titulo}</h1>
      {children}
    </header>
  );
}

export function Descripcion({ children }: { children: ReactNode }) {
  return <p className="text-body font-regular text-secondary">{children}</p>;
}
