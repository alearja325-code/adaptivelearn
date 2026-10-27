// Ventana 002 — Crear Experiencia: Paso 1 (Elegir área)
// Spec: docs/modesec/fase-2-diseno-multimedial/05-spec-crear-experiencia-paso1.md, §2.2
// Backend: E-16 GET /catalogo/areas
import { BookOpen, Calculator, Globe, Leaf, type LucideIcon } from 'lucide-react';
import { useEffect, useState } from 'react';
import { api, ErrorApi } from '../../api/cliente';
import type { Area } from '../../api/tipos';
import { BotonPrimario } from '../../componentes/Botones';
import { CardSeleccion } from '../../componentes/CardSeleccion';
import { Mensaje } from '../../componentes/Formulario';
import { useSesion } from '../../sesion/SesionContexto';
import { Subencabezado } from './Subencabezado';

// §2.2 "Íconos sugeridos", en el orden de la spec
export const ICONO_AREA: Record<string, LucideIcon> = {
  MAT: Calculator,
  LEN: BookOpen,
  CN: Leaf,
  CS: Globe,
};
const ORDEN = Object.keys(ICONO_AREA);

interface Props {
  elegida: Area | null;
  onElegir: (a: Area) => void;
  onContinuar: () => void;
}

export function Paso1Area({ elegida, onElegir, onContinuar }: Props) {
  const { token } = useSesion();
  const [areas, setAreas] = useState<Area[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .areas(token!)
      .then((lista) => setAreas([...lista].sort((a, b) => ORDEN.indexOf(a.codigo) - ORDEN.indexOf(b.codigo))))
      .catch((e) => setError(e instanceof ErrorApi ? e.message : 'No se pudieron cargar las áreas.'));
  }, [token]);

  return (
    <>
      <Subencabezado titulo="Área" descripcion="Cada experiencia pertenece a una de las 4 áreas del currículo MEN." />
      <Mensaje texto={error} />
      <div className="flex gap-16" role="radiogroup" aria-label="Área">
        {(areas ?? []).map((a) => (
          <CardSeleccion
            key={a.codigo}
            icono={ICONO_AREA[a.codigo] ?? BookOpen}
            etiqueta={a.nombre}
            seleccionada={elegida?.codigo === a.codigo}
            onElegir={() => onElegir(a)}
          />
        ))}
      </div>
      <div className="mt-24 flex">
        <BotonPrimario disabled={!elegida} onClick={onContinuar}>
          Continuar
        </BotonPrimario>
      </div>
    </>
  );
}
