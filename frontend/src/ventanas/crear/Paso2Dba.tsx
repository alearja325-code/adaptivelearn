// Ventana 003 — Crear Experiencia: Paso 2 (Elegir DBA)
// Spec: docs/modesec/fase-2-diseno-multimedial/06-spec-crear-experiencia-paso2.md
// Backend: E-17 GET /catalogo/grados, E-14 GET /catalogo/dbas (filtros
// codigo_area, numero_grado y q), E-15 GET /catalogo/dbas/:codigo (al expandir
// una card, no todos de una vez: encargo 04 §4.4).
import { ChevronRight, Search } from 'lucide-react';
import { useEffect, useRef, useState, type ReactNode } from 'react';
import { api, ErrorApi } from '../../api/cliente';
import type { Area, DbaDetalle, DbaResumen, Grado } from '../../api/tipos';
import { BotonGhost, BotonPrimario } from '../../componentes/Botones';
import { Mensaje } from '../../componentes/Formulario';
import { useSesion } from '../../sesion/SesionContexto';
import { Subencabezado } from './Subencabezado';

// Decisión del encargo 04, declarada: la búsqueda espera a que se deje de
// escribir 300 ms antes de pedir al backend (la spec dice "filtra" sin decir
// cuándo; así no sale una petición por cada letra).
export const ESPERA_BUSQUEDA_MS = 300;

// 06-spec §2.4: el ejemplo del PDF incluye una figura que esta versión no muestra
export const AVISO_IMAGEN = 'Este ejemplo incluye una imagen que no se muestra en esta versión.';

interface Props {
  area: Area;
  elegido: DbaResumen | null;
  onElegir: (d: DbaResumen) => void;
  onVolver: () => void;
  onContinuar: () => void;
}

export function Paso2Dba({ area, elegido, onElegir, onVolver, onContinuar }: Props) {
  const { token } = useSesion();
  const [texto, setTexto] = useState('');
  const [busqueda, setBusqueda] = useState('');
  const [grado, setGrado] = useState<number | null>(null);
  const [dbas, setDbas] = useState<DbaResumen[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const id = setTimeout(() => setBusqueda(texto), ESPERA_BUSQUEDA_MS);
    return () => clearTimeout(id);
  }, [texto]);

  useEffect(() => {
    let vigente = true;
    api
      .dbas(token!, area.codigo, grado, busqueda)
      .then((lista) => vigente && (setDbas(lista), setError(null)))
      .catch((e) => vigente && setError(e instanceof ErrorApi ? e.message : 'No se pudieron cargar los DBA.'));
    return () => {
      vigente = false;
    };
  }, [token, area.codigo, grado, busqueda]);

  return (
    <>
      <Subencabezado titulo="Aprendizaje" descripcion="La experiencia se ancla a un único DBA de esa área." />

      {/* §2.3 Fila de filtros */}
      <div className="flex gap-12">
        <label className="flex h-44 min-w-0 flex-1 items-center gap-8 rounded-12 borde-1 border-border bg-surface-0 px-16 focus-within:border-primary-ink">
          <Search size={16} strokeWidth={1.5} className="shrink-0 text-muted" aria-hidden />
          <input
            value={texto}
            onChange={(e) => setTexto(e.target.value)}
            placeholder="Buscar por enunciado..."
            aria-label="Buscar por enunciado"
            className="min-w-0 flex-1 bg-transparent text-boton font-regular text-primary-ink outline-none placeholder:text-muted"
          />
        </label>
        <SelectGrado valor={grado} onCambio={setGrado} />
      </div>

      {/* §2.4 Lista de DBA: la única zona que scrollea */}
      <ul className="flex min-h-0 flex-1 flex-col gap-12 overflow-y-auto" aria-label="DBA" data-testid="lista-dba">
        {(dbas ?? []).map((d) => (
          <CardDba key={d.codigo} dba={d} seleccionado={elegido?.codigo === d.codigo} onElegir={() => onElegir(d)} />
        ))}
      </ul>
      <Mensaje texto={error} />

      {/* §2.6 Footer fijo, con divisor encima */}
      <div className="flex flex-col">
        <div className="h-1 w-full bg-border" />
        <div className="mt-24 grid grid-cols-2 gap-12">
          <BotonGhost onClick={onVolver}>Volver</BotonGhost>
          <BotonPrimario disabled={!elegido} onClick={onContinuar}>
            Continuar
          </BotonPrimario>
        </div>
      </div>
    </>
  );
}

/**
 * §2.3 Select de Grado: ancho fijo 104, alto 44, Radio 12, Stroke 1 #E7E7E7,
 * texto Button/Input Medium centrado (#888888 sin elegir, #111111 elegido),
 * chevron 16 a la derecha (› cerrado, ⌄ abierto). Panel (confirmado el
 * 2026-10-21): debajo, mismo ancho, Fill #FFFFFF, Stroke 1, Radio 12, margen
 * 4; filas de 40, padding 16; hover #FAFAF8; el elegido Fill #F5F3EE Bold.
 * Decisión del encargo 04, declarada: la spec no dice cómo quitar el filtro;
 * elegir otra vez el grado ya elegido lo quita (vuelve a "Grado").
 */
function SelectGrado({ valor, onCambio }: { valor: number | null; onCambio: (g: number | null) => void }) {
  const { token } = useSesion();
  const [abierto, setAbierto] = useState(false);
  const [grados, setGrados] = useState<Grado[]>([]);
  const caja = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api.grados(token!).then(setGrados).catch(() => setGrados([]));
  }, [token]);

  useEffect(() => {
    if (!abierto) return;
    const fuera = (e: MouseEvent) => !caja.current?.contains(e.target as Node) && setAbierto(false);
    document.addEventListener('mousedown', fuera);
    return () => document.removeEventListener('mousedown', fuera);
  }, [abierto]);

  return (
    <div ref={caja} className="relative w-104 shrink-0">
      <button
        type="button"
        aria-haspopup="listbox"
        aria-expanded={abierto}
        aria-label="Grado"
        onClick={() => setAbierto((a) => !a)}
        className="flex h-44 w-104 cursor-pointer items-center justify-center gap-8 rounded-12 borde-1 border-border bg-surface-0 px-16"
      >
        <span className={`flex-1 text-center text-boton font-medium ${valor === null ? 'text-muted' : 'text-primary-ink'}`}>
          {valor === null ? 'Grado' : `${valor}°`}
        </span>
        {/* M13: el chevron gira de › a ⌄ */}
        <ChevronRight
          size={16}
          strokeWidth={1.5}
          className={`shrink-0 text-muted transition-transform duracion-media ${abierto ? 'rotate-90' : ''}`}
          aria-hidden
        />
      </button>
      {abierto && (
        <ul
          role="listbox"
          aria-label="Grados"
          className="absolute left-0 top-full z-10 mt-4 max-h-alto-modal w-104 animate-mensaje overflow-y-auto rounded-12 borde-1 border-border bg-surface-0"
        >
          {grados.map((g) => (
            <li key={g.numero} role="option" aria-selected={valor === g.numero}>
              <button
                type="button"
                onClick={() => {
                  onCambio(valor === g.numero ? null : g.numero);
                  setAbierto(false);
                }}
                className={`flex h-40 w-full cursor-pointer items-center px-16 text-boton text-primary-ink transition ${
                  valor === g.numero ? 'bg-surface-2 font-bold' : 'font-medium hover:bg-surface-1'
                }`}
              >
                {g.numero}°
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

/**
 * §2.4 Card de DBA — contenedor único: Radio 16, Stroke 1 #E7E7E7, Padding 16,
 * Gap 16. Fila colapsada: radio de selección 20 (Stroke 1.5 #E7E7E7; elegido:
 * Fill #111111 con punto blanco de 8), badge "DBA 8°", enunciado en una línea
 * con elipsis y chevron 16. Expandida: separador de 1 y los infoblocks
 * Enunciado, Evidencias y Ejemplo (Label Caption #888888, Value Body
 * #111111, Gap 4; las evidencias con Gap 8).
 */
function CardDba({ dba, seleccionado, onElegir }: { dba: DbaResumen; seleccionado: boolean; onElegir: () => void }) {
  const { token } = useSesion();
  const [abierta, setAbierta] = useState(false);
  const [detalle, setDetalle] = useState<DbaDetalle | null>(null);
  const [error, setError] = useState<string | null>(null);

  function alternar() {
    const abrir = !abierta;
    setAbierta(abrir);
    if (abrir && !detalle) {
      api
        .dba(token!, dba.codigo)
        .then(setDetalle)
        .catch((e) => setError(e instanceof ErrorApi ? e.message : 'No se pudo cargar el DBA.'));
    }
  }

  return (
    <li
      className={`flex shrink-0 flex-col gap-16 rounded-16 borde-1 border-border p-16 transition ${seleccionado ? 'bg-surface-0' : 'bg-surface-0 hover:bg-surface-1'}`}
      data-codigo={dba.codigo}
    >
      <div className="flex items-center gap-12">
        <button
          type="button"
          role="radio"
          aria-checked={seleccionado}
          aria-label={`Elegir ${dba.codigo}`}
          onClick={onElegir}
          className="flex min-w-0 flex-1 cursor-pointer items-center gap-12 text-left"
        >
          <span
            className={`flex size-20 shrink-0 items-center justify-center rounded-999 transition ${
              seleccionado ? 'bg-primary-ink' : 'borde-1_5 border-border'
            }`}
            aria-hidden
          >
            {seleccionado && <span className="size-8 rounded-999 bg-surface-0" />}
          </span>
          <span className="flex h-22 shrink-0 items-center rounded-4 bg-surface-2 px-8 text-badge font-bold text-secondary">
            DBA {dba.grado.numero}°
          </span>
          <span className="min-w-0 flex-1 truncate text-body font-regular text-primary-ink">{dba.enunciado}</span>
        </button>
        <button
          type="button"
          aria-expanded={abierta}
          aria-label={abierta ? `Ocultar ${dba.codigo}` : `Ver ${dba.codigo}`}
          onClick={alternar}
          className="shrink-0 cursor-pointer"
        >
          {/* M8: el chevron gira de › a ⌄ */}
          <ChevronRight
            size={16}
            strokeWidth={1.5}
            className={`text-muted transition-transform duracion-media ${abierta ? 'rotate-90' : ''}`}
            aria-hidden
          />
        </button>
      </div>

      {/* M8: al expandir, el cuerpo aparece; al colapsar, se va al instante */}
      {abierta && (
        <div className="flex animate-mensaje flex-col gap-16">
          <div className="h-1 w-full bg-border" />
          <InfoBlock etiqueta="Enunciado">
            <p className="text-body font-regular text-primary-ink">{dba.enunciado}</p>
          </InfoBlock>
          <InfoBlock etiqueta="Evidencias">
            <ul className="flex flex-col gap-8">
              {(detalle?.evidencias ?? []).map((e) => (
                <li key={e.numero} className="text-body font-regular text-primary-ink">
                  {/* Censo QA-014 (encargo 05); sin dictamen (null) se mostraría como "aplica" (encargo 04 §4.4) */}
                  {e.admiteFormatoCerrado === false ? (
                    <>
                      <span className="line-through">{e.enunciado}</span>
                      <span className="text-informativo"> — no aplica a formato cerrado</span>
                    </>
                  ) : (
                    e.enunciado
                  )}
                </li>
              ))}
            </ul>
            <Mensaje texto={error} />
          </InfoBlock>
          {/* §2.4: el texto del ejemplo (cada párrafo en su línea) y, si el del PDF trae una
              figura, el aviso informativo. Decisión del encargo 05: con texto y figura se
              muestran los dos; sin ejemplo en el PDF (null y sin figura), no hay infoblock */}
          {(detalle?.ejemplo || detalle?.ejemploTieneImagen) && (
            <InfoBlock etiqueta="Ejemplo">
              {detalle.ejemplo && (
                <p className="whitespace-pre-line text-body font-regular text-primary-ink">{detalle.ejemplo}</p>
              )}
              {detalle.ejemploTieneImagen && (
                <p className="text-body font-regular text-informativo">{AVISO_IMAGEN}</p>
              )}
            </InfoBlock>
          )}
        </div>
      )}
    </li>
  );
}

function InfoBlock({ etiqueta, children }: { etiqueta: string; children: ReactNode }) {
  return (
    <div className="flex flex-col gap-4">
      <p className="text-caption font-regular text-muted">{etiqueta}</p>
      {children}
    </div>
  );
}
