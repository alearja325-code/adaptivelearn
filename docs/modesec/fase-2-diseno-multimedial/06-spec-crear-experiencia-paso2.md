# Ventana 003 — Crear Experiencia: Paso 2 (Elegir DBA)

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Marco compartido:** hereda el modal de `05-spec-crear-experiencia-paso1.md`
(sección 2.1) — no se repite aquí. Ancho fijo `912px`, alto máximo
`852px` en este frame de Figma (`1440×900`); en producción, `852` es
"alto de pantalla menos `48px`" (regla relativa), no un número fijo.

---

## 1. Nombre

`003 — Crear Experiencia / Paso 2 (DBA)`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Encabezado y stepper

Igual que el Paso 1 (fila de encabezado + stepper) — círculo 2 activo,
círculo 1 en estado Completado.

### 2.2 Subencabezado del paso

Mismo componente que el Paso 1 (título + descripción apilados,
centrados, gap `4px`):
- Título: "Aprendizaje" — `16px / 24px` peso `700` Bold, color `#111111`.
- Descripción: "La experiencia se ancla a un único DBA de esa área." —
  `16px / 24px` peso `400` Regular, color `#555555`. *(Cambio
  deliberado frente a "Elige el DBA que vas a trabajar." — mismo
  criterio que el Paso 1: informa qué es este paso en el modelo, no
  solo instruye qué hacer, y ya no se confunde en forma con el
  subencabezado del Paso 1.)*

### 2.3 Fila de filtros

Auto Layout Horizontal, Gap `12px`:
- **Search Input** (ancho Fill): igual al de Dashboard — alto `44px`,
  Radio `12px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, padding interno
  `16px` cada lado, gap ícono-texto `8px`, ícono lupa `16×16px` stroke
  `1.5px` color `#888888`. Placeholder: "Buscar por enunciado...".
- **Select de Grado**: ancho **fijo `104px`** (agregado a
  `anchos_layout_px` en `tokens.json`) — sale de Padding `16px`
  (izquierda) + texto + Gap `8px` + ícono `16×16px` + Padding `16px`
  (derecha), medido con el texto "Grado". Alto `44px`, Radio `12px`,
  Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`. Auto Layout interno
  Horizontal, Alignment Center, **Gap `8px`** (mismo gap que usa el
  ícono de lupa del Search Input — ya no es Space Between; texto e
  ícono van pegados con este gap, el ícono después del texto).
  - **Texto** (placeholder "Grado" o el grado ya elegido, ej. "8°"):
    `16px / 22px` (Button/Input), peso `500` Medium, **Align Center**
    dentro de una caja de ancho fijo al del placeholder "Grado" (la
    opción más ancha) — así un grado corto como "10°" queda centrado en
    ese mismo espacio, sin que el select cambie de ancho ni el ícono se
    mueva al elegir una opción.
    - Sin elegir: color `#888888` (Muted) — mismo tratamiento que el
      placeholder del Search Input.
    - Con un grado elegido: color `#111111` (Primary Ink).
  - **Ícono**: `16×16px`, stroke `1.5px`, color `#888888` — después del
    texto, no antes. **Chevron derecha** (`›`) con el dropdown cerrado,
    **chevron abajo** (`⌄`) con el dropdown abierto — mismo lenguaje que
    el ícono de expandir de la Card de DBA (sección 2.4), deliberadamente
    unificado: ambos son "toca para revelar contenido debajo".
  - Opciones: `1°` a `11°` — **sin Transición** (verificado contra
    `curriculo_men_normalizado.json`: ninguna de las 4 áreas tiene DBA
    de Transición en los datos reales).

**Dropdown del Select de Grado — CONFIRMADO 2026-10-21** *(antes:
"propuesta, pendiente de confirmar". Alejandro lo aprobó tal cual: el
docente necesita poder filtrar los DBA por grado si lo desea)*:
- Panel: aparece debajo del trigger, alineado a la izquierda, mismo
  ancho que el trigger. Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Radio
  `12px`, margen superior `4px`. *Pendiente real: no existe todavía un
  token de elevación/sombra en `tokens.json` — si quieres sombra para
  el panel hay que definirla antes; de momento el spec no la incluye.*
- Opciones: Auto Layout Vertical, sin gap entre filas (se distinguen
  por el hover). Cada fila: alto `40px` (Small), Padding horizontal
  `16px`, Auto Layout Horizontal, Alignment Center.
  - Default: texto `16px / 22px` peso `500` Medium, color `#111111`.
  - Hover: Fill `#FAFAF8`.
  - Grado ya elegido (si se reabre el dropdown): Fill `#F5F3EE`, texto
    peso `700` Bold.
- Con 11 opciones de `40px` cada una (11 × 40 = 440 de alto total, cifra
  informativa, no un token nuevo) no debería necesitar scroll interno en
  este frame, pero si el espacio disponible es menor, el panel
  scrollea.

### 2.4 Lista de DBA (área con scroll interno si excede el alto disponible)

Auto Layout Vertical, Gap `12px`. Esta es la única zona que scrollea —
encabezado, stepper, subencabezado, filtros y el footer (2.6) quedan
fijos.

**Card de DBA — contenedor único.** Radio `16px`, Fill `#FFFFFF`,
Stroke `1px` `#E7E7E7`, Padding `16px` (los 4 lados), Auto Layout
Vertical, Gap `16px` — **un solo Auto Layout para toda la card**; todo
lo que sigue (fila colapsada, separador, infoblocks) son hijos directos
de este mismo contenedor, con el mismo gap y el mismo padding, sin
subgrupos ni contenedores nuevos.

**Capa 1 — fila colapsada** (siempre visible, colapsada o expandida):
Auto Layout Horizontal, Gap `12px`, Alignment Center:
1. **Radio de selección** (nuevo componente): `20×20px`, Radio `999px`
   (Full).
   - Default: Stroke `1.5px` `#E7E7E7`, Fill transparente.
   - Seleccionado: Fill `#111111`, con un punto blanco centrado `8×8px`.
   - Solo un DBA puede estar seleccionado a la vez — elegir otro
     desmarca el anterior.
2. **Badge** "DBA [grado]°" (ej. "DBA 8°"): alto `22px`, Radio `4px`,
   Padding izq/der `8px`, Fill `#F5F3EE`, texto `12px / 16px` peso `700`
   Bold, color `#555555`.
3. **Enunciado truncado** (Fill, una sola línea con elipsis): `16px /
   24px` peso `400` Regular, color `#111111`.
4. **Ícono expandir**: `16×16px`, stroke `1.5px`, color `#888888` —
   **chevron derecha** (`›`) colapsada, **chevron abajo** (`⌄`)
   expandida (mismo lenguaje que el ícono del Select de Grado, arriba).

**Capa 2 — separador** (solo si está expandida): línea de `1px`, color
`#E7E7E7`, ancho completo.

**Infoblocks** (solo si está expandida) — 3 hijos directos de la card,
después del separador, **no van agrupados en un contenedor propio**:
heredan el Gap `16px` y el Padding `16px` ya definidos arriba, nada
nuevo. Sin ícono de expandir individual (se descartó esa idea — ya
alcanza con el ícono de la Capa 1 para toda la card). Los 3 infoblocks
comparten la **misma** propiedad de gap entre Label y Value — Gap
`4px`, sin variar de uno a otro:

  **InfoBlock "Enunciado"**:
  - Label: "Enunciado" — `13px / 20px` (Caption), peso `400` Regular,
    color `#888888`.
  - Value: texto completo del enunciado del DBA — `16px / 24px` peso
    `400` Regular, color `#111111`.

  **InfoBlock "Evidencias"**: mismo Label. El Value es un **subgrupo
  propio** dentro del infoblock — Auto Layout Vertical, Gap `8px` (este
  gap es exclusivo de este subgrupo, para separar las evidencias entre
  sí; no reemplaza el Gap `4px` de Label→Value, es un gap adicional
  solo dentro del Value) — una fila por evidencia:
  - Evidencia que **aplica** a formato cerrado: `16px / 24px` Regular,
    color `#111111`.
  - Evidencia que **no aplica**: mismo tamaño, decoración
    **Strikethrough** (texto tachado), seguido en la misma fila de un
    texto corto " — no aplica a formato cerrado" en color `#6D28D9`
    (Informativo — ver `03-tokens-diseno.md`, deliberadamente distinto
    de los 3 colores de Resultado de evidencia, para no mezclar ambos
    conceptos). Sigue siendo una fila más dentro de la lista de
    Evidencias, no un elemento aparte. Depende del censo QA-014
    (pendiente) para saber cuáles evidencias son.

  **InfoBlock "Ejemplo"** — Auto Layout Vertical, Gap `4px` (mismo
  patrón de Label→Value que los otros dos infoblocks): solo texto, sin
  imagen — se descartó **mostrar** la imagen en esta versión (sin
  fuente verificada del MEN para usarla, y generarla con IA queda fuera
  de alcance por ahora; según ADR-011 es de todos modos la minoría de
  los casos — 2 a 8 de 21 a 115 según el área):
  - Value, caso normal (texto): texto completo del ejemplo del DBA —
    igual que el Value de Enunciado.
  - Value, caso raro (el ejemplo real incluye una imagen): mismo
    tratamiento informativo que la evidencia que no aplica — texto
    "Este ejemplo incluye una imagen que no se muestra en esta
    versión." en color `#6D28D9` (Informativo), en vez de texto vacío
    o el bloque desaparecido — para que no se vea como un error, sino
    como una limitación conocida.
  - *Pendiente de datos reales — el campo "ejemplo" no existe todavía
    en la base (QA-011), ni el dato de si un caso puntual trae imagen;
    este Value queda listo para cuando exista.*

### 2.5 Íconos sugeridos para el Select de Grado

Ninguno — es texto simple (el número de grado), no necesita ícono por
opción, solo el ícono de flecha del control.

### 2.6 Fila de acciones (footer, fijo — no scrollea)

Divisor `1px` `#E7E7E7`, ancho completo, encima del footer — señala el
límite entre la lista de DBA con scroll (2.4) y esta zona fija, mismo
criterio que se aplica en Materiales de la Vista Interna
(`11-spec-vista-interna-materiales.md`, sección 2.4).

Auto Layout Horizontal, Gap `12px`, margen superior `24px` desde el
divisor:
*(Corrección 2026-11-04, Alejandro: en todo el sistema, los dos botones
de acción de un modal se reparten la fila en **dos mitades iguales**,
como en el Figma. Antes: el secundario ancho Hug y el principal ocupaba
el resto.)*
- **Botón "Volver"** (Ghost — sin Fill, sin Stroke, **ancho Fill: la mitad de la fila**,
  texto centrado): alto
  `48px`, Padding izq/der `24px`, texto `16px / 22px` peso `500`
  Medium, color `#555555`. Sin fondo ni borde en la caja.
- **Botón "Continuar"** (**ancho Fill: la otra mitad**): igual especificación
  que el Paso 1 — Habilitado (hay un DBA seleccionado): Fill `#111111`,
  texto `#FFFFFF`. Deshabilitado: Fill `#BDBDBD`, texto `#FFFFFF`.

## 3. Texto

- "Aprendizaje · La experiencia se ancla a un único DBA de esa área."
  (subencabezado).
- "Buscar por enunciado..." (placeholder de búsqueda).
- "Grado" (placeholder del Select).
- "1°" a "11°" (opciones del Select — sin Transición).
- "DBA [grado]°" (badge de cada card).
- "Enunciado", "Evidencias", "Ejemplo" (labels de los infoblocks).
- "— no aplica a formato cerrado" (texto informativo, evidencia
  descartada, color `#6D28D9`).
- "Este ejemplo incluye una imagen que no se muestra en esta versión."
  (texto informativo, caso raro de Ejemplo con imagen, color `#6D28D9`).
- "Volver", "Continuar" (botones).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Hover en cards (sin seleccionar): Fill `#FAFAF8`.
- Selección de card: transición del radio (Default → Seleccionado),
  persiste.
- Expandir/colapsar card: el chevron cambia de derecha (`›`) a abajo
  (`⌄`), el cuerpo expandido aparece o desaparece — sin animación
  compleja, transición simple.
- Abrir/cerrar el Select de Grado: mismo cambio de chevron (derecha ↔
  abajo).
- Botón "Continuar": Deshabilitado → Habilitado apenas hay un DBA
  seleccionado.
- Hover en botones "Volver" y botón cerrar: Fill `#FAFAF8` (con padding
  propio del botón, no definido aquí — es un detalle menor de
  implementación, no de este spec).

## 7. Acciones

- Escribir en el Search Input → filtra la lista de DBA por texto del
  enunciado.
- Elegir un Grado en el Select → filtra la lista de DBA por grado.
- Clic en una card → selecciona ese DBA (desmarca cualquier otro).
- Clic en el ícono expandir → muestra/oculta el cuerpo con los
  infoblocks.
- Clic en "Volver" → regresa al Paso 1, conservando el área ya elegida.
- Clic en "Continuar" (solo si hay un DBA seleccionado) → avanza al
  Paso 3.
- Clic en el botón cerrar (X, en el encabezado) → cierra el modal sin
  crear nada.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 06-spec-crear-experiencia-paso2.md
OK — 06-spec-crear-experiencia-paso2.md: todos los colores y valores en px están en tokens.json
```

**Historial real de esta verificación, no ocultado:**
1. Primera corrida: limpia — todos los valores nuevos (radio de
   selección, badge, infoblocks, footer) se construyeron reutilizando
   tokens ya aprobados (`03-tokens-diseno.md`), sin necesitar agregar
   ninguno nuevo a `tokens.json`.
2. Corrección posterior (sin cambios de valores, solo de estructura):
   la Card de DBA — expandida tenía un padding de `24px` inventado para
   el "cuerpo expandido", sin explicar qué pasaba con el contenido de
   la fila colapsada al expandir. Se reestructuró como un único
   contenedor (Padding `16px`, el mismo de siempre) con 3 capas
   apiladas — fila colapsada (persiste siempre), separador y grupo de
   infoblocks (estas dos solo si está expandida) — sin ícono de
   expandir por infoblock. Se eliminó el `24px` inventado; no se agregó
   ningún token nuevo. Corrida limpia.
3. Segunda corrección (misma naturaleza, sin cambios de valores): los
   infoblocks quedaron mal descritos como un "grupo" con su propio Auto
   Layout — no son un contenedor aparte, son 3 hijos directos del mismo
   Auto Layout de la card, heredando su Gap `16px` y Padding `16px` sin
   nada nuevo. Se unificó el gap Label→Value de los 3 infoblocks en un
   solo valor (`4px`, sin variar entre ellos), dejando claro que el Gap
   `8px` de la lista de Evidencias es un subgrupo propio, exclusivo de
   ese infoblock, no un reemplazo del anterior. Se agregó la decoración
   Strikethrough al texto de evidencias que no aplican (no es un valor
   en px ni un color, no afecta la verificación de tokens). Corrida
   final, limpia.
4. Tercera corrección: el Select de Grado tenía un ancho fijo `96px`
   inventado y sin gap definido — se corrigió a Hug (Padding `16px` +
   texto + Gap `8px` + ícono + Padding `16px`, replicando el criterio
   del ícono de lupa del Search Input), con el texto en Align Center
   para que un grado corto no mueva el ancho del componente. Se agregó
   una propuesta (marcada como pendiente de confirmar) para el estado
   abierto del dropdown, que no existía. Se quitó el ícono info de la
   evidencia "no aplica" (queda pendiente de decisión cómo se comunica)
   y se permitió que el InfoBlock "Ejemplo" combine texto e imagen en
   vez de ser excluyente. El único número nuevo que aparece (`440`,
   alto total del panel de opciones) se escribió sin sufijo `px` porque
   es una cifra derivada/informativa, no un token — el script lo marcó
   una vez como fallo hasta corregir la redacción; ver línea de arriba,
   no se ocultó el fallo. Corrida final, limpia.
5. Cuarta corrección: se resolvieron las dos preguntas pendientes.
   "No aplica" usa un color nuevo — `#6D28D9` Informativo, agregado a
   `tokens.json` y documentado con su verificación de contraste en
   `03-tokens-diseno.md` (7.1:1 sobre blanco, pasa AAA) — en vez del
   ícono info retirado. Las imágenes de "Ejemplo" se descartan para
   esta versión (sin fuente MEN verificada, generarlas con IA queda
   fuera de alcance); el InfoBlock vuelve a Gap `4px` simple, sin
   subgrupo de imagen. Corrida final, limpia.
6. Quinta corrección: el Select de Grado en realidad debía ser ancho
   **fijo** `104px` (agregado a `anchos_layout_px`), no Hug — se había
   descrito mal. Se agregó el caso raro del InfoBlock "Ejemplo" con
   imagen real (mismo tratamiento informativo violeta que la evidencia
   descartada, en vez de dejarlo vacío o quitar el bloque). Se completó
   la sección "3. Texto" con las dos cadenas informativas que faltaban.
   Se reemplazó el subencabezado ("Elige el DBA que vas a trabajar.")
   por uno informativo ("La experiencia se ancla a un único DBA de esa
   área."), mismo criterio que el Paso 1, para dejar de parecer
   idéntico al subencabezado de ese paso. Corrida final, limpia.
7. Sexta corrección, a partir de la implementación real en Figma: ni el
   ícono del Select ("flecha abajo, rota 180°") ni el de expandir de la
   Card de DBA ("abajo → arriba") coincidían con lo que Alejandro
   terminó construyendo — chevron derecha (cerrado/colapsado) → chevron
   abajo (abierto/expandida), igual en ambos controles. Se corrigieron
   los dos para documentar el patrón real, ahora deliberadamente
   unificado entre Select y Card de DBA (mismo lenguaje visual: "toca
   para revelar contenido debajo"). Corrida final, limpia.
8. Séptima corrección, surgida al construir Materiales en la Vista
   Interna: el footer (2.6) tiene contenido con scroll inmediatamente
   encima (la lista de DBA, 2.4) pero no llevaba divisor que señalara
   el límite — inconsistente con el mismo patrón fijo-scroll-fijo
   aplicado en Materiales, donde sí se agregó un divisor por la misma
   razón. Se agregó acá también, mismo criterio en ambos lugares.
   Corrida final, limpia.
