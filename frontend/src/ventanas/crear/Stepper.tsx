// Stepper de Crear experiencia (002 §2.1): 3 círculos de 32, Radio 999, sin
// texto debajo. Activo: Fill #111111, número #FFFFFF Bold 12/16. Completado:
// Fill #555555, número #FFFFFF Bold. Pendiente: Stroke 1 #E7E7E7, número
// #888888 Regular. Línea de 1 que se estira: #555555 si ya se recorrió,
// #E7E7E7 si no.
export function Stepper({ paso }: { paso: 1 | 2 | 3 }) {
  return (
    <ol className="flex w-full items-center" aria-label={`Paso ${paso} de 3`}>
      {[1, 2, 3].map((n) => {
        const estado = n === paso ? 'activo' : n < paso ? 'completado' : 'pendiente';
        const circulo = {
          activo: 'bg-primary-ink text-surface-0 font-bold',
          completado: 'bg-secondary text-surface-0 font-bold',
          pendiente: 'borde-1 border-border text-muted font-regular',
        }[estado];
        return (
          <li key={n} className={`flex items-center ${n < 3 ? 'flex-1' : ''}`} aria-current={n === paso ? 'step' : undefined}>
            <span className={`flex size-32 shrink-0 items-center justify-center rounded-999 text-badge transition duracion-media ${circulo}`} data-estado={estado}>
              {n}
            </span>
            {n < 3 && <span className={`h-1 flex-1 transition duracion-media ${n < paso ? 'bg-secondary' : 'bg-border'}`} />}
          </li>
        );
      })}
    </ol>
  );
}
