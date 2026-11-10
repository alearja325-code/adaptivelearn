// Genera el tema de Tailwind desde el sistema de diseño de la Fase II
// (ADR-038, encargo 04 §2): docs/modesec/fase-2-diseno-multimedial/tokens.json
// y la pila de fuentes web de 03-tokens-diseno.md. Escribe
// src/estilos/tema.generado.css — NO se edita a mano: se cambia tokens.json
// (y su .md) y se vuelve a correr `npm run tema`.
//
// El tema BORRA los valores por defecto de Tailwind (colores, espaciados,
// radios, tamaños de letra, sombras): así una clase como `bg-red-500` o
// `p-5` no produce nada, y verificar-estilos.mjs la marca como error.
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const AQUI = dirname(fileURLToPath(import.meta.url));
const FASE2 = join(AQUI, '..', '..', 'docs', 'modesec', 'fase-2-diseno-multimedial');
const SALIDA = join(AQUI, '..', 'src', 'estilos', 'tema.generado.css');

const tokens = JSON.parse(readFileSync(join(FASE2, 'tokens.json'), 'utf8'));
const doc = readFileSync(join(FASE2, '03-tokens-diseno.md'), 'utf8');

/** "Estado: No muestra — revisado…" → "estado-no-muestra" */
export function nombreColor(descripcion) {
  return descripcion
    .split(/ — | \(/)[0]
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

/** "Button/Input" → "boton"; "Badge Label" → "badge" */
const NOMBRE_TEXTO = { H1: 'h1', H2: 'h2', H3: 'h3', H4: 'h4', Body: 'body', 'Button/Input': 'boton', Caption: 'caption', 'Badge Label': 'badge' };
const NOMBRE_PESO = { 400: 'regular', 500: 'medium', 700: 'bold' };

export function construirTema() {
  const colores = Object.entries(tokens.colores).map(([hex, desc]) => [nombreColor(desc), hex]);

  // Medidas de caja: espaciados, alturas de control, íconos, anchos de
  // layout y los interlineados (el Badge mide 22 de alto: el interlineado
  // de Button/Input, ya aprobado en tokens.json)
  const medidas = new Set([0]);
  for (const v of tokens.espaciado_px) medidas.add(v);
  for (const v of tokens.alturas_control_px) medidas.add(v);
  for (const v of tokens.iconos_px) medidas.add(v);
  for (const k of Object.keys(tokens.anchos_layout_px)) if (/^\d+$/.test(k)) medidas.add(Number(k));
  for (const t of tokens.tipografia) medidas.add(t.lh);
  // y las líneas divisoras de 1 (grosores_borde_px: "línea de 1px")
  for (const g of tokens.grosores_borde_px) if (Number.isInteger(g) && g < 4) medidas.add(g);
  const espaciados = [...medidas].sort((a, b) => a - b);

  const pila = doc.match(/pila CSS `([^`]+)`/);
  if (!pila) throw new Error('No encontré la pila de fuentes web en 03-tokens-diseno.md');

  return { colores, espaciados, radios: tokens.radios_px, grosores: tokens.grosores_borde_px, tipografia: tokens.tipografia, fuente: pila[1], movimiento: tokens.movimiento };
}

function css({ colores, espaciados, radios, grosores, tipografia, fuente, movimiento }) {
  const L = [];
  const w = (s) => L.push(s);
  w('/* GENERADO por scripts/generar-tema.mjs desde');
  w(' * docs/modesec/fase-2-diseno-multimedial/tokens.json y 03-tokens-diseno.md.');
  w(' * No editar a mano: cambiar tokens.json y correr `npm run tema`. */');
  w('');
  w('@theme {');
  w('  /* Sin los valores por defecto de Tailwind: solo los del sistema de diseño */');
  for (const ns of ['color', 'spacing', 'radius', 'text', 'font-weight', 'leading', 'tracking', 'shadow', 'inset-shadow', 'drop-shadow', 'blur', 'breakpoint', 'container', 'font', 'ease', 'animate', 'perspective', 'aspect']) {
    w(`  --${ns}-*: initial;`);
  }
  w('  --spacing: initial;');
  w('');
  w('  /* Colores (tokens.json, "colores") */');
  for (const [nombre, hex] of colores) w(`  --color-${nombre}: ${hex};`);
  w('');
  w('  /* Medidas en px: espaciado, alturas de control, íconos, anchos de layout e interlineados */');
  for (const v of espaciados) w(`  --spacing-${v}: ${v}px;`);
  w('  /* Alto máximo del modal de Crear experiencia: en Figma 852, en producción');
  w('     "alto de pantalla menos 48" (tokens.json, anchos_layout_px.852) */');
  w('  --spacing-alto-modal: calc(100vh - 48px);');
  w('');
  w('  /* Radios (tokens.json, "radios_px") */');
  for (const v of radios) w(`  --radius-${v}: ${v}px;`);
  w('');
  w('  /* Tipografía (tokens.json, "tipografia"); fuente web de 03-tokens-diseno.md */');
  w(`  --font-sans: ${fuente};`);
  for (const t of tipografia) {
    const n = NOMBRE_TEXTO[t.nivel];
    if (!n) throw new Error(`Nivel tipográfico sin nombre: ${t.nivel}`);
    w(`  --text-${n}: ${t.size}px;`);
    w(`  --text-${n}--line-height: ${t.lh}px;`);
    w(`  --text-${n}--font-weight: ${t.peso};`);
  }
  for (const p of [...new Set(tipografia.map((t) => t.peso))].sort()) w(`  --font-weight-${NOMBRE_PESO[p]}: ${p};`);
  w('');
  movimientoTema(movimiento, w);
  w('}');
  w('');
  w('/* Grosores de borde (tokens.json, "grosores_borde_px"): borde-1, borde-1_5, … */');
  for (const g of grosores) {
    w(`@utility borde-${String(g).replace('.', '_')} {`);
    w(`  border-style: solid;`);
    w(`  border-width: ${g}px;`);
    w('}');
  }
  w('');
  movimientoFuera(movimiento, w);
  return L.join('\n') + '\n';
}

/**
 * Movimiento (31-guia-de-movimiento.md, ADR-041; tokens.json "movimiento").
 * Cada animación es un patrón de la guía. Solo se anima lo que llega; lo que
 * se va, se va al instante (principio 3), así que no hay animaciones de salida.
 */
const ANIMACIONES = {
  // nombre: [patrón, duración, curva, desde (transform), repetir]
  aparecer: ['M6 llegar a una pantalla', 'lenta', 'entrada', (d) => `translateY(${d.corta}px)`],
  modal: ['M4 abrir un modal (panel)', 'lenta', 'entrada', (d, e) => `translateY(${d.corta}px) scale(${e})`],
  fondo: ['M4 abrir un modal (fondo)', 'media', 'estandar', () => null],
  mensaje: ['M9, M8 y M13: un mensaje, un cuerpo o una lista que aparece', 'media', 'entrada', (d) => `translateY(-${d.minima}px)`],
  'paso-adelante': ['M7 avanzar de paso', 'media', 'entrada', (d) => `translateX(${d.paso}px)`],
  'paso-atras': ['M7 volver de paso', 'media', 'entrada', (d) => `translateX(-${d.paso}px)`],
};

function movimientoTema(m, w) {
  const ms = m.duraciones_ms;
  w('  /* Movimiento (tokens.json, "movimiento"; 31-guia-de-movimiento.md) */');
  for (const [n, v] of Object.entries(m.curvas)) w(`  --ease-${n}: ${v};`);
  w(`  --default-transition-duration: ${ms.rapida}ms;`);
  w('  --default-transition-timing-function: var(--ease-estandar);');
  for (const [n, [patron, dur, curva]] of Object.entries(ANIMACIONES)) {
    w(`  --animate-${n}: ${n} ${ms[dur]}ms var(--ease-${curva}) both; /* ${patron} */`);
  }
  w(`  --animate-girar: girar ${ms.giro}ms linear infinite; /* M12 cargando */`);
  for (const [n, [, , , desde]] of Object.entries(ANIMACIONES)) {
    const t = desde(m.distancias_px, m.escala_modal);
    w(`  @keyframes ${n} { from { opacity: 0;${t ? ` transform: ${t};` : ''} } to { opacity: 1;${t ? ' transform: none;' : ''} } }`);
  }
  w('  @keyframes girar { to { transform: rotate(360deg); } }');
}

function movimientoFuera(m, w) {
  const ms = m.duraciones_ms;
  w('/* Duraciones con nombre para las transiciones: duracion-rapida, -media, -lenta */');
  for (const n of ['rapida', 'media', 'lenta']) {
    w(`@utility duracion-${n} {`);
    w(`  transition-duration: ${ms[n]}ms;`);
    w('}');
  }
  w('');
  w('/* Reducir movimiento (31-guia-de-movimiento.md): sin desplazamientos ni escalas;');
  w('   quedan cambios de opacidad en "rapida". El spinner (M12) sigue girando. */');
  w('@media (prefers-reduced-motion: reduce) {');
  for (const n of Object.keys(ANIMACIONES)) {
    w(`  @keyframes ${n} { from { opacity: 0; } to { opacity: 1; } }`);
    w(`  .animate-${n} { animation-duration: ${ms.rapida}ms; }`);
  }
  w('  .transition-transform { transition-duration: 0ms; }');
  w('}');
}

const tema = construirTema();
writeFileSync(SALIDA, css(tema));
writeFileSync(
  join(AQUI, '..', 'src', 'estilos', 'tema.generado.json'),
  JSON.stringify(
    {
      _nota: 'GENERADO por scripts/generar-tema.mjs — lo usa verificar-estilos.mjs',
      colores: tema.colores.map(([n]) => n),
      espaciados: tema.espaciados.map(String).concat('alto-modal'),
      radios: tema.radios.map(String),
      grosores: tema.grosores.map((g) => String(g).replace('.', '_')),
      textos: tema.tipografia.map((t) => NOMBRE_TEXTO[t.nivel]),
      pesos: [...new Set(tema.tipografia.map((t) => NOMBRE_PESO[t.peso]))],
      curvas: Object.keys(tema.movimiento.curvas),
      duraciones: ['rapida', 'media', 'lenta'],
      animaciones: [...Object.keys(ANIMACIONES), 'girar'],
    },
    null,
    2,
  ) + '\n',
);
console.log(`tema generado: ${tema.colores.length} colores, ${tema.espaciados.length} medidas, ${tema.radios.length} radios, ${tema.tipografia.length} tamaños de letra`);
