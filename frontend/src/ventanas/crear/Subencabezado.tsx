// Subencabezado de cada paso de Crear experiencia (002 §2.2, 003 §2.2, 004 §2.2):
// título Body Bold #111111 + descripción Body Regular #555555, centrados, Gap 4.
export function Subencabezado({ titulo, descripcion }: { titulo: string; descripcion: string }) {
  return (
    <div className="flex flex-col items-center gap-4 text-center">
      <h3 className="text-body font-bold text-primary-ink">{titulo}</h3>
      <p className="text-body font-regular text-secondary">{descripcion}</p>
    </div>
  );
}
