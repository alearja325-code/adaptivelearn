// Lo que las pantallas piden y todavía no existe (encargo 04 §4): el
// Dashboard vacío, "Unirse con código", "Crear experiencia" del Paso 3, el
// Paso 2 sin dictamen ni ejemplo, y Google/Microsoft sin configurar.
import { screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { backendFalso, montar, ruta, usuario } from '../pruebas/utilidades';

const docente = ruta('GET', '/auth/profile', { estado: 200, cuerpo: { user: usuario() } });
const estudiante = ruta('GET', '/auth/profile', {
  estado: 200,
  cuerpo: { user: usuario({ idDocente: null, idEstudiante: 3, role: 'estudiante' }) },
});
const catalogo = [
  ruta('GET', '/catalogo/areas', {
    estado: 200,
    cuerpo: [
      { codigo: 'CN', nombre: 'Ciencias Naturales' },
      { codigo: 'CS', nombre: 'Ciencias Sociales' },
      { codigo: 'LEN', nombre: 'Lenguaje' },
      { codigo: 'MAT', nombre: 'Matemáticas' },
    ],
  }),
  ruta('GET', '/catalogo/grados', {
    estado: 200,
    cuerpo: Array.from({ length: 11 }, (_, i) => ({ numero: i + 1, nombre: `G${i + 1}`, nivel: 'media' })),
  }),
  ruta('GET', /^\/catalogo\/dbas\?/, {
    estado: 200,
    cuerpo: [{ codigo: 'CS-08-08', enunciado: 'Comprende la importancia de las asociaciones.', area: { codigo: 'CS', nombre: 'Ciencias Sociales' }, grado: { numero: 8, nombre: 'Octavo' } }],
  }),
  ruta('GET', '/catalogo/dbas/CS-08-08', {
    estado: 200,
    cuerpo: {
      codigo: 'CS-08-08',
      enunciado: 'Comprende la importancia de las asociaciones.',
      area: { codigo: 'CS', nombre: 'Ciencias Sociales' },
      grado: { numero: 8, nombre: 'Octavo' },
      ejemplo: null,
      documento: { titulo: 'DBA', version: 'V.1', anio: 2016, paginas: 52, urlOficial: 'https://x' },
      evidencias: [
        { numero: 1, enunciado: 'Primera evidencia.', admiteFormatoCerrado: null, formato: null },
        { numero: 2, enunciado: 'Segunda evidencia.', admiteFormatoCerrado: null, formato: null },
      ],
    },
  }),
];

describe('Dashboard (001) sin experiencias — §4.1', () => {
  it('docente: estado vacío, sin pedir una lista que no existe', async () => {
    const llamadas = backendFalso(docente);
    montar('/', { token: 'tok' });
    expect(await screen.findByText('Aún no has creado ninguna experiencia.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Borradores' })).toBeInTheDocument();
    expect(llamadas.map((l) => l.url)).toEqual(['/auth/profile']);
  });

  it('estudiante: estado vacío y "Unirse con código" muestra el aviso informativo (§4.2)', async () => {
    backendFalso(estudiante);
    montar('/', { token: 'tok' });
    expect(await screen.findByText('Aún no te has unido a ninguna experiencia.')).toBeInTheDocument();
    expect(screen.queryByText('Unirse a una experiencia llega en la siguiente etapa.')).not.toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: '→ Unirse con código' }));
    const aviso = screen.getByText('Unirse a una experiencia llega en la siguiente etapa.');
    expect(aviso).toHaveClass('text-informativo', 'text-caption');
  });

  it('"Cerrar sesión" borra la sesión del navegador y lleva a 014 (§4.5)', async () => {
    backendFalso(docente);
    montar('/', { token: 'tok' });
    await userEvent.click(await screen.findByRole('button', { name: 'Cerrar sesión' }));
    expect(await screen.findByText('Bienvenido de vuelta')).toBeInTheDocument();
    expect(sessionStorage.getItem('adaptivelearn.token')).toBeNull();
  });
});

describe('Crear experiencia (002 → 003 → 004)', () => {
  async function irAlPaso2() {
    const llamadas = backendFalso(docente, ...catalogo);
    montar('/', { token: 'tok' });
    await userEvent.click(await screen.findByRole('button', { name: '+ Crear experiencia' }));
    const dialogo = await screen.findByRole('dialog', { name: 'Crear experiencia' });
    const continuar = within(dialogo).getByRole('button', { name: 'Continuar' });
    expect(continuar).toBeDisabled();
    await userEvent.click(await within(dialogo).findByRole('radio', { name: 'Ciencias Sociales' }));
    await userEvent.click(continuar);
    return { dialogo, llamadas };
  }

  it('Paso 1: las áreas en el orden de la spec (Matemáticas, Lenguaje, Naturales, Sociales)', async () => {
    backendFalso(docente, ...catalogo);
    montar('/', { token: 'tok' });
    await userEvent.click(await screen.findByRole('button', { name: '+ Crear experiencia' }));
    const radios = await screen.findAllByRole('radio');
    expect(radios.map((r) => r.textContent)).toEqual(['Matemáticas', 'Lenguaje', 'Ciencias Naturales', 'Ciencias Sociales']);
  });

  it('Paso 2: el grado filtra la lista, y las evidencias se piden al expandir; sin dictamen, todas "aplican" y sin ejemplo (§4.4)', async () => {
    const { dialogo, llamadas } = await irAlPaso2();
    await within(dialogo).findByText('Comprende la importancia de las asociaciones.');
    expect(llamadas.some((l) => l.url.startsWith('/catalogo/dbas/'))).toBe(false);

    await userEvent.click(within(dialogo).getByRole('button', { name: 'Grado' }));
    await userEvent.click(within(dialogo).getByRole('button', { name: '8°' }));
    expect(llamadas.some((l) => l.url === '/catalogo/dbas?codigo_area=CS&numero_grado=8')).toBe(true);

    await userEvent.click(within(dialogo).getByRole('button', { name: 'Ver CS-08-08' }));
    expect(await within(dialogo).findByText('Segunda evidencia.')).toBeInTheDocument();
    expect(llamadas.filter((l) => l.url === '/catalogo/dbas/CS-08-08')).toHaveLength(1);
    expect(within(dialogo).queryByText('— no aplica a formato cerrado')).not.toBeInTheDocument();
    expect(within(dialogo).queryByText('Ejemplo')).not.toBeInTheDocument();
  });

  it('Paso 3: "Crear experiencia" no llama a nada y muestra el aviso informativo (§4.3)', async () => {
    const { dialogo, llamadas } = await irAlPaso2();
    await userEvent.click(await within(dialogo).findByRole('radio', { name: 'Elegir CS-08-08' }));
    await userEvent.click(within(dialogo).getByRole('button', { name: 'Continuar' }));
    const nombre = await within(dialogo).findByDisplayValue('Comprende la importancia de las asociaciones.');
    expect(nombre).toHaveClass('text-muted');
    const antes = llamadas.length;

    const crear = within(dialogo).getByRole('button', { name: 'Crear experiencia' });
    await userEvent.click(crear);
    const aviso = within(dialogo).getByText('Crear la experiencia llega en la siguiente etapa.');
    expect(aviso).toHaveClass('text-informativo');
    expect(llamadas).toHaveLength(antes);
    expect(screen.queryByText('Generando las preguntas...')).not.toBeInTheDocument();

    await userEvent.clear(nombre);
    expect(crear).toBeDisabled();
  });
});

describe('Google y Microsoft sin configurar (§4.6)', () => {
  it('el botón muestra el mensaje "no configurado" que responde el backend', async () => {
    const llamadas = backendFalso(
      ruta('POST', '/auth/google', {
        estado: 503,
        cuerpo: { message: 'El acceso con Google no está configurado en este servidor.' },
      }),
    );
    montar('/iniciar-sesion');
    await userEvent.click(screen.getByRole('button', { name: 'Continuar con Google' }));
    expect(await screen.findByText('El acceso con Google no está configurado en este servidor.')).toBeInTheDocument();
    expect(llamadas[0].url).toBe('/auth/google');
  });
});
