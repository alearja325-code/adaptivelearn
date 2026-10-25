# Ventana 006 — Vista Interna de la Experiencia: Marco compartido

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Origen:** se entra aquí desde una card de experiencia en el Dashboard
(`04-spec-dashboard.md`, Bloque 4) — docente o estudiante.

Este marco (sidebar + encabezado + metadata + nav de tabs) se comparte
entre las 3 pestañas — Resumen, Materiales, Estudiantes — que tendrán su
propia spec, referenciando esta sección en vez de repetirla. Solo 2
columnas (sidebar + contenido) — sin una tercera columna a la derecha,
mismo criterio ya aplicado en el Dashboard.

---

## 1. Nombre

`006 — Vista Interna de la Experiencia / Marco compartido`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Frame base

Igual que el Dashboard: `1440 × 900`, Fill `#F7F6F3`, Auto Layout
Horizontal, Padding `24px` (los 4 lados), Gap `24px`.

### 2.2 Sidebar

Se reutiliza **sin cambios** del Dashboard (`04-spec-dashboard.md`,
sección 2.2) — mismo bloque de perfil, mismo divisor, misma navegación.
"Mis experiencias" se mantiene en estado **activo** — seguimos dentro de
esa sección, esto es un drill-down de una de sus cards, no una sección
nueva.

### 2.3 Panel de contenido

Alto **Fill** (igual que el Sidebar — ambos ocupan los `852px`
disponibles del frame de forma fija, para que el Sidebar nunca
desaparezca al hacer scroll). Radio `24px`, Fill `#FFFFFF`, Stroke
`1px` `#E7E7E7`, Inside. Auto Layout Vertical, Padding `32px` (los 4
lados), Gap `32px`, **Alignment Center** (*Corrección 2026-08-29: antes
sin especificar, quedaban alineados a la izquierda por defecto*). Este
único ajuste centra como bloque la fila de metadata y el nav de tabs
(2.3 y más abajo) — ambos son Hug-width, se acomodan al centro solos.
No afecta al área de contenido de cada pestaña: esa siempre es
Fill-width (son cards que ocupan el ancho completo), así que "centrado"
no le cambia nada — ya ocupa todo el espacio disponible.

**Zona fija vs. zona con scroll:** encabezado, metadata y nav de tabs
quedan siempre fijos (no scrollean). El contenido de la pestaña activa,
debajo del nav, es lo único que scrollea internamente si excede el alto
disponible — cada pestaña define si además necesita algo fijo propio
(ej. un botón de acción) en su propio spec.

**Fila de encabezado** — patrón de 3 zonas, título centrado (mismo
criterio unificado en `05-spec-crear-experiencia-paso1.md`, sección
2.1 — *Corrección 2026-08-29: reemplaza el Space Between de la versión
anterior, donde "←" y el título vivían juntos a la izquierda*). A
diferencia de los modales grandes (que solo tienen un ícono real y
necesitan una caja invisible del otro lado para que el título quede
centrado), acá ya hay 2 íconos reales, uno en cada zona — no hace falta
ningún elemento invisible:
- Auto Layout Horizontal, ancho Fill, Alignment Center.
- Zona izquierda: Botón "←" volver — ícono `20×20px`, stroke `1.5px`,
  color `#555555` — mismo tratamiento que los íconos de nav del
  sidebar. Ya no comparte fila interna con el título — es su propia
  zona, sola.
- Título (zona central): nombre real de la experiencia (el que el
  docente definió en el Paso 3 de creación) — `32px / 40px` (H1), peso
  `700` Bold, color `#111111`, centrado. Mismo nivel que "Mis
  experiencias" en el Dashboard — esta pantalla funciona como su propia
  página.
- Zona derecha: botón "..." — `32×32px`, Radio `8px`, Fill transparente,
  ícono `16×16px` stroke `1.5px` color `#888888`. Hover: Fill
  `#FAFAF8`. *(Corrección 2026-09-26 — contenido resuelto: abre directo
  el modal de confirmación de `25-spec-modal-confirmar-eliminar-salir.md`
  (variante Docente, "Eliminar experiencia") — sin desplegable
  intermedio, es la única acción real disponible acá. Este mismo botón
  se reutiliza para el estudiante en `23-spec-toma-diagnostico.md`,
  Ventana 020, con la variante Estudiante del mismo modal.)*

**Fila de metadata** — Auto Layout Horizontal, ancho **Hug**, Gap
`24px`, Alignment Center. Ancho Hug a propósito (no Fill): así queda
centrada como bloque por el `Alignment Center` del Panel de contenido
(2.3), en vez de estirarse de borde a borde. **Estado**, **Creada**,
**Estudiantes**, **Área**, **Grado**:
los 5 son pares Label+Value en línea, **mismo tratamiento sin
excepción** — Auto Layout Horizontal Gap `4px` cada par:
- Label: `13px / 20px` (Caption), peso `400` Regular, color `#888888`.
- Value: `16px / 22px` (Button/Input), peso `700` Bold, color `#111111`
  — para **Estado** el valor es el texto plano "Borrador"/"Publicada",
  sin badge.

*(Corrección — el Estado usaba el Status Badge del Dashboard, con
fondo relleno. Se retira aquí: en una lista (Dashboard) el color de
fondo ayuda a escanear muchas filas de un vistazo, que es el trabajo
real de ese componente ahí. Acá no hay nada que escanear — es un solo
objeto leído como una frase, y el badge se veía más pesado que sus 4
vecinos de la misma fila sin aportar nada que el texto plano no diera
igual. El Status Badge del Dashboard no cambia, sigue siendo el
correcto ahí.)*

**Regla compartida entre las 3 pestañas — el subencabezado de sección
no lleva título en bold.** Cada pestaña puede tener una descripción de
sección (16/24 Regular `#555555`, mismo criterio de siempre: dice qué
es esto en el modelo, no solo instruye), pero **sin** el título Bold
`#111111` que el mismo componente sí usa en Crear Experiencia. Ahí
tiene sentido — el Stepper no compite con él. Acá el nav de tabs activo
ya usa `16/22 Bold #111111` con subrayado, y la fila de metadata ya usa
`16/22 Bold #111111` para sus values — un tercer texto con la misma
tipografía, peso y color, apilado a centímetros de los otros dos, no
suma jerarquía, la borra. El nav ya dice en cuál pestaña se está; el
título repetía esa misma respuesta con otras palabras. Aplica
retroactivo a Resumen y Materiales (ver sus specs).

**Nav de tabs** — Auto Layout Horizontal, ancho **Hug**, Gap `24px` —
mismo motivo que la fila de metadata: Hug para que el `Alignment
Center` del Panel de contenido lo centre como bloque:
- "Resumen", "Materiales", "Estudiantes" — sin "Tecnico" (nunca se
  llegó a elaborar en el sistema anterior, se deja fuera).
- **Activo** (Resumen por defecto, al entrar): texto `16px / 22px`
  peso `700` Bold, color `#111111`, con un subrayado propio (`2px`
  `#111111`) debajo de esa etiqueta.
- **Inactivo**: texto `16px / 22px` peso `500` Medium, color `#888888`,
  sin subrayado.

**Divisor** — elemento propio, **fuera** de la fila de tabs (que ahora
es Hug): `1px` `#E7E7E7`, ancho **Fill**, debajo de toda la fila de
tabs. Tiene que ser Fill para cruzar el panel completo — si viviera
dentro de la fila Hug, solo taparía el ancho de las 3 etiquetas, no el
panel entero (*Corrección 2026-08-29: antes vivía como bullet dentro de
la fila de tabs, sin problema porque esa fila era Fill; ahora que es
Hug, tiene que separarse*).

**Contenido de la pestaña activa** — va debajo del nav, dentro del
mismo panel; cada pestaña se especifica en su propio archivo.

## 3. Texto

- "Mis experiencias" (sidebar, se mantiene activo).
- Nombre de la experiencia (título — dato real, no fijo).
- "Estado", "Creada", "Estudiantes", "Área", "Grado" (labels de
  metadata).
- "Resumen", "Materiales", "Estudiantes" (tabs).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Hover en botón "←" y botón "...": Fill `#FAFAF8`.
- Cambio de tab: el subrayado se mueve a la etiqueta activa, el
  contenido debajo cambia — sin animación compleja.

## 7. Acciones

- Clic en "←" → vuelve al Dashboard.
- Clic en "..." → abre directo el modal "¿Eliminar esta experiencia?"
  (`25-spec-modal-confirmar-eliminar-salir.md`, variante Docente).
  *(Corrección 2026-10-21: esta línea seguía diciendo "contenido
  pendiente" aunque la sección 2.3 ya se había corregido el 2026-09-26
  — la corrección se hizo a medias.)*
- Clic en un tab → cambia la pestaña activa, cambia el contenido debajo.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 09-spec-vista-interna-marco.md
OK — 09-spec-vista-interna-marco.md: todos los colores y valores en px están en tokens.json
```

Pasó limpio en la primera corrida — todo se construyó reutilizando
tokens y componentes ya aprobados (Sidebar y Status Badge del Dashboard,
tipografía y botones-ícono de los pasos de Crear Experiencia), sin
necesitar agregar ninguno nuevo a `tokens.json`.

**Corrección posterior (2026-08-26, sin valores nuevos):** dos cambios,
a partir de una observación real de Alejandro sobre esta pantalla —
(1) el Estado dejó de usar el Status Badge, pasa a texto plano como sus
4 vecinos de fila (ver 2.3, razón completa ahí); (2) se documentó la
regla de que el subencabezado de sección, dentro de las 3 pestañas, no
lleva título Bold — competía en tipografía con el nav activo y con los
values de la metadata, los 3 iguales en tamaño/peso/color. Ningún valor
de `tokens.json` cambia — ambas correcciones usan tokens que ya
existían, solo se corrige dónde se aplican.
