// Ventana 001 — Dashboard (Mis experiencias), variantes Docente y Estudiante
// Spec: docs/modesec/fase-2-diseno-multimedial/04-spec-dashboard.md
// Backend: E-11 GET /auth/profile (el bloque de perfil del Sidebar).
//
// Encargo 04 §4.1: todavía no existe la ruta para listar experiencias; se
// muestra el estado vacío (§2.3, "Empty state") en las dos variantes, sin
// llamar a una ruta que no existe. Buscar y los filtros se ven, pero no
// tienen sobre qué actuar.
import { Inbox, LayoutGrid, LogOut, Search, User } from 'lucide-react';
import { useState } from 'react';
import { useNavigate } from 'react-router';
import { urlFoto } from '../api/cliente';
import { BotonPrimario } from '../componentes/Botones';
import { Mensaje } from '../componentes/Formulario';
import { varianteDe } from '../sesion/reglas';
import { useSesion } from '../sesion/SesionContexto';
import { V002CrearExperiencia } from './V002CrearExperiencia';
import { V026MiPerfil } from './V026MiPerfil';

const TEXTOS = {
  docente: {
    subtitulo: 'Crea una experiencia para tu grupo.',
    boton: '+ Crear experiencia',
    chips: ['Todas', 'Borradores', 'Publicadas'],
    vacio: 'Aún no has creado ninguna experiencia.',
  },
  estudiante: {
    subtitulo: 'Únete a una experiencia con el código de tu docente.',
    boton: '→ Unirse con código',
    chips: ['Todas', 'No iniciadas', 'En curso', 'Completadas'],
    vacio: 'Aún no te has unido a ninguna experiencia.',
  },
} as const;

// Encargo 04 §4.2
export const AVISO_UNIRSE = 'Unirse a una experiencia llega en la siguiente etapa.';

export function V001Dashboard() {
  const navegar = useNavigate();
  const { usuario, cerrar } = useSesion();
  const [chip, setChip] = useState('Todas');
  const [busqueda, setBusqueda] = useState('');
  const [modal, setModal] = useState<'perfil' | 'crear' | null>(null);
  const [avisoUnirse, setAvisoUnirse] = useState(false);
  if (!usuario?.perfil) return null;

  const variante = varianteDe(usuario);
  const t = TEXTOS[variante];
  const { nombres, apellidos, avatarUrl } = usuario.perfil;

  function accionPrincipal() {
    if (variante === 'docente') setModal('crear');
    else setAvisoUnirse(true);
  }

  function salir() {
    // §2.2: "Cerrar sesión" lleva directo a Iniciar sesión, sin confirmación.
    // No hay ruta en el backend (E-13 es opcional): se borra la sesión del navegador.
    cerrar();
    navegar('/iniciar-sesion');
  }

  return (
    <main className="flex h-screen gap-24 bg-canvas p-24 font-sans">
      {/* §2.2 Sidebar */}
      <aside className="flex w-280 shrink-0 flex-col rounded-24 borde-1 border-border bg-surface-0 p-24">
        <button
          type="button"
          aria-label="Editar mi perfil"
          onClick={() => setModal('perfil')}
          className="flex w-full cursor-pointer flex-col items-center gap-8 rounded-12 p-12 hover:bg-surface-1"
        >
          <Avatar url={urlFoto(avatarUrl)} />
          <span className="w-full truncate text-body font-bold text-primary-ink" data-testid="nombre-sidebar">
            {nombres} {apellidos}
          </span>
          <span className="w-full truncate text-caption font-regular text-muted">{usuario.email}</span>
        </button>

        <div className="my-24 h-1 w-full bg-border" />

        <nav className="flex flex-col gap-4" aria-label="Navegación principal">
          <a
            href="/"
            aria-current="page"
            className="flex h-44 items-center gap-12 rounded-8 bg-surface-2 px-12 text-boton font-bold text-primary-ink"
          >
            <LayoutGrid size={20} strokeWidth={2} className="text-primary-ink" aria-hidden />
            Mis experiencias
          </a>
        </nav>

        <div className="flex-1" />
        <div className="my-24 h-1 w-full bg-border" />

        <nav className="flex flex-col gap-4" aria-label="Navegación secundaria">
          <button
            type="button"
            onClick={salir}
            className="flex h-44 cursor-pointer items-center gap-12 rounded-8 px-12 text-boton font-medium text-secondary hover:bg-surface-1"
          >
            <LogOut size={20} strokeWidth={1.5} className="text-secondary" aria-hidden />
            Cerrar sesión
          </button>
        </nav>
      </aside>

      {/* §2.3 Área de contenido */}
      <section className="flex min-w-0 flex-1 flex-col gap-32 overflow-y-auto rounded-24 borde-1 border-border bg-surface-0 p-32">
        <header className="flex flex-col gap-4">
          <h1 className="text-h1 font-bold text-primary-ink">Mis experiencias</h1>
          <p className="text-body font-regular text-secondary">{t.subtitulo}</p>
        </header>

        <div className="flex flex-col gap-8">
          <div className="flex items-center gap-12">
            <label className="flex h-44 min-w-0 flex-1 items-center gap-8 rounded-12 borde-1 border-border bg-surface-0 px-16 focus-within:border-primary-ink">
              <Search size={16} strokeWidth={1.5} className="shrink-0 text-muted" aria-hidden />
              <input
                value={busqueda}
                onChange={(e) => setBusqueda(e.target.value)}
                placeholder="Buscar experiencias"
                aria-label="Buscar experiencias"
                className="min-w-0 flex-1 bg-transparent text-boton font-regular text-primary-ink outline-none placeholder:text-muted"
              />
            </label>
            <div className="shrink-0">
              <BotonPrimario className="px-24" onClick={accionPrincipal}>
                {t.boton}
              </BotonPrimario>
            </div>
          </div>
          {/* Encargo 04 §4.2: aviso informativo, Caption, #6D28D9 */}
          {avisoUnirse && <Mensaje texto={AVISO_UNIRSE} tipo="informativo" />}
        </div>

        <div className="flex gap-8" role="group" aria-label="Filtros">
          {t.chips.map((c) => (
            <button
              key={c}
              type="button"
              aria-pressed={chip === c}
              onClick={() => setChip(c)}
              className={`h-40 cursor-pointer rounded-8 px-16 text-boton ${
                chip === c ? 'borde-1 border-primary-ink bg-surface-2 font-bold text-primary-ink' : 'borde-1 border-border bg-surface-0 font-medium text-secondary'
              }`}
            >
              {c}
            </button>
          ))}
        </div>

        {/* §2.3 Bloque 4 — Empty state (encargo 04 §4.1) */}
        <div className="flex flex-col items-center gap-8 py-48">
          <Inbox size={32} strokeWidth={1.5} className="text-disabled" aria-hidden />
          <p className="text-body font-regular text-muted">{t.vacio}</p>
        </div>
      </section>

      {modal === 'perfil' && <V026MiPerfil onCerrar={() => setModal(null)} />}
      {modal === 'crear' && <V002CrearExperiencia onCerrar={() => setModal(null)} />}
    </main>
  );
}

/** Avatar del Sidebar: 56×56, Radio 999 (§2.2). Sin foto: el ícono por defecto
 *  de 016 §2.2 (persona sobre #E7E7E7) — decisión declarada del encargo 04. */
function Avatar({ url }: { url: string | null }) {
  return url ? (
    <img src={url} alt="" className="size-56 rounded-999 object-cover object-center" />
  ) : (
    <span className="flex size-56 items-center justify-center rounded-999 bg-border">
      <User size={24} strokeWidth={1.5} className="text-muted" aria-hidden />
    </span>
  );
}
