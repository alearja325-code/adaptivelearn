// Verificador de estilos del frontend (encargo 04 §2, ADR-038): es en el
// código lo que verificar_tokens.py hace en las specs de la Fase II.
// Falla (código de salida 1) si en src/ aparece:
//   1. un color escrito a mano (#rrggbb, rgb(), hsl());
//   2. una medida escrita a mano (16px, 1.5rem, 2em) o un style={...} en línea;
//   3. un valor arbitrario de Tailwind (w-[13px], bg-[#123456], [color:red]);
//   4. una clase de Tailwind cuyo valor no existe en el tema generado desde
//      tokens.json (p-5, bg-red-500, rounded-full, text-sm, border-3…);
//   5. un ícono de Lucide con un tamaño o un grosor que tokens.json no tiene;
//   6. una opacidad que ninguna spec usa (solo 60% y 85%: 016 §2.2 y 014 §6);
//   7. una duración, curva o animación que no sale de tokens.json "movimiento"
//      (duration-300, ease-in-out, animate-bounce…; 31-guia-de-movimiento.md).
// No revisa src/marcas/ (logos de terceros con sus colores de marca, 014 §2.8)
// ni el tema generado. Uso: npm run verificar:estilos
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const AQUI = dirname(fileURLToPath(import.meta.url));
const SRC = join(AQUI, '..', 'src');
const tema = JSON.parse(readFileSync(join(SRC, 'estilos', 'tema.generado.json'), 'utf8'));
const tokens = JSON.parse(
  readFileSync(join(AQUI, '..', '..', 'docs', 'modesec', 'fase-2-diseno-multimedial', 'tokens.json'), 'utf8'),
);

// 0 y 100: mostrar y ocultar con transición (M1, 31-guia-de-movimiento.md)
const OPACIDADES = new Set(['0', '60', '85', '100']);
const ICONOS = new Set(tokens.iconos_px.map(String));
const GROSORES = new Set(tokens.grosores_borde_px.map(String));

const COLORES = new Set(tema.colores);
const ESPACIOS = new Set(tema.espaciados);
const RADIOS = new Set(tema.radios);
const TEXTOS = new Set(tema.textos);
const PESOS = new Set(tema.pesos);
const BORDES = new Set(tema.grosores);
const COLOR_CLAVE = new Set(['transparent', 'current', 'inherit']);
const CURVAS = new Set(tema.curvas);
const DURACIONES = new Set(tema.duraciones);
const ANIMACIONES = new Set(tema.animaciones);

// Prefijo de utilidad → qué valores admite (palabras clave + valores del tema)
const ESPACIO_CLAVE = ['auto', 'full', 'screen', 'fit', 'min', 'max'];
const REGLAS = [
  // tamaños y espacios
  [/^-?(p|px|py|pt|pr|pb|pl|ps|pe|m|mx|my|mt|mr|mb|ml|ms|me|gap|gap-x|gap-y|space-x|space-y|w|h|size|min-w|min-h|max-w|max-h|top|right|bottom|left|inset|inset-x|inset-y|translate-x|translate-y|basis)$/,
    (v) => ESPACIOS.has(v) || ESPACIO_CLAVE.includes(v)],
  [/^rounded(-(t|r|b|l|tl|tr|br|bl|s|e))?$/, (v) => RADIOS.has(v) || v === 'none'],
  [/^text$/, (v) => COLORES.has(v) || TEXTOS.has(v) || ['left', 'center', 'right', 'justify', 'start', 'end'].includes(v)],
  [/^(bg|fill|stroke|caret|accent|decoration|from|via|to|divide)$/, (v) => COLORES.has(v) || COLOR_CLAVE.has(v)],
  [/^border(-(t|r|b|l|x|y|s|e))?$/, (v) => COLORES.has(v) || COLOR_CLAVE.has(v) || ['solid', 'dashed', 'none'].includes(v)],
  [/^borde$/, (v) => BORDES.has(v)],
  [/^font$/, (v) => PESOS.has(v) || v === 'sans'],
  [/^opacity$/, (v) => OPACIDADES.has(v)],
  [/^(leading|tracking|shadow|ring|outline|blur|drop-shadow|inset-shadow)$/, (v) => v === 'none'],
  // movimiento: solo los nombres de tokens.json (duration-300 o delay-100 no)
  [/^(duration|delay)$/, () => false],
  [/^duracion$/, (v) => DURACIONES.has(v)],
  [/^ease$/, (v) => CURVAS.has(v)],
  [/^animate$/, (v) => ANIMACIONES.has(v) || v === 'none'],
];

const errores = [];
const error = (archivo, linea, texto) => errores.push(`${relative(join(AQUI, '..'), archivo)}:${linea}  ${texto}`);

function archivos(dir) {
  return readdirSync(dir).flatMap((n) => {
    const r = join(dir, n);
    if (statSync(r).isDirectory()) return n === 'marcas' ? [] : archivos(r);
    return /\.(tsx?|css)$/.test(n) && !n.startsWith('tema.generado') && !/\.test\.tsx?$/.test(n) ? [r] : [];
  });
}

/** Revisa una clase de Tailwind (sin variantes como hover: o focus-within:) */
function revisarClase(clase) {
  const base = clase.split(':').pop();
  if (/\[/.test(base)) return 'valor arbitrario: no se permite (usa un valor del tema)';
  const conOpacidad = base.match(/^(.*)\/(\d+)$/);
  const sinMod = conOpacidad ? conOpacidad[1] : base;
  if (conOpacidad && !OPACIDADES.has(conOpacidad[2])) return `opacidad /${conOpacidad[2]}: ninguna spec la usa`;
  // el prefijo más largo que tenga una regla (gap-x antes que gap)
  const partes = sinMod.split('-');
  for (let i = partes.length - 1; i >= 1; i--) {
    const prefijo = partes.slice(0, i).join('-');
    const valor = partes.slice(i).join('-');
    const regla = REGLAS.find(([re]) => re.test(prefijo));
    if (regla) return regla[1](valor) ? null : `"${valor}" no existe en el tema para ${prefijo}-* (tokens.json)`;
  }
  if (/^border-\d/.test(sinMod)) return 'grosor de borde de Tailwind: usa borde-1, borde-1_5, borde-2 o borde-2_5';
  return null;
}

/**
 * El código de una línea, sin comentarios: los comentarios citan los valores
 * de la spec (#111111, Radio 24…) para que el grupo B pueda explicarla, y eso
 * no es usarlos. Quita bloques /* … *\/, {/* … *\/}, // … y las líneas de un
 * bloque de comentario que empiezan con *.
 */
function sinComentarios(linea) {
  if (/^\s*(\*|\/\*)/.test(linea)) return '';
  return linea
    .replace(/\{?\/\*.*?\*\/\}?/g, '')
    .replace(/(^|[^:])\/\/.*$/, '$1');
}

for (const archivo of archivos(SRC)) {
  const lineas = readFileSync(archivo, 'utf8').split('\n');
  lineas.forEach((original, i) => {
    const n = i + 1;
    const linea = sinComentarios(original);
    if (/#[0-9a-fA-F]{3,8}\b/.test(linea.replace(/https?:\/\/\S+/g, ''))) error(archivo, n, `color escrito a mano: ${linea.trim()}`);
    if (/\b(rgba?|hsla?)\(/.test(linea)) error(archivo, n, `color escrito a mano: ${linea.trim()}`);
    if (/\b\d+(\.\d+)?(px|rem|em)\b/.test(linea)) error(archivo, n, `medida escrita a mano: ${linea.trim()}`);
    if (/\bstyle=\{/.test(linea)) error(archivo, n, 'estilo en línea (style={...}): usa clases del tema');
    for (const m of linea.matchAll(/\bsize=\{(\d+(?:\.\d+)?)\}/g)) {
      if (!ICONOS.has(m[1])) error(archivo, n, `ícono de ${m[1]}: tokens.json no tiene ese tamaño (iconos_px)`);
    }
    for (const m of linea.matchAll(/\bstrokeWidth=\{(\d+(?:\.\d+)?)\}/g)) {
      if (!GROSORES.has(m[1])) error(archivo, n, `grosor de ícono ${m[1]}: no está en grosores_borde_px`);
    }
    // Las clases: cada texto entre comillas o acentos graves, palabra por palabra
    for (const m of linea.matchAll(/(['"`])((?:(?!\1).)*)\1/g)) {
      for (const pedazo of m[2].split(/\$\{[^}]*\}/)) {
        for (const clase of pedazo.split(/\s+/)) {
          if (!/^[a-z0-9:/_.\-[\]#()%,]+$/.test(clase) || !clase.includes('-') && !clase.includes('[')) continue;
          const problema = revisarClase(clase);
          if (problema) error(archivo, n, `${clase} — ${problema}`);
        }
      }
    }
  });
}

if (errores.length) {
  console.error(`verificar-estilos: ${errores.length} problemas\n`);
  for (const e of errores) console.error(`  ${e}`);
  process.exit(1);
}
console.log(`OK — verificar-estilos: ${archivos(SRC).length} archivos, todos los colores, medidas y clases salen de tokens.json`);
