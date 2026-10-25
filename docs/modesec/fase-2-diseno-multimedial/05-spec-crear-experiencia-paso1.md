# Ventana 002 — Crear Experiencia: Marco compartido + Paso 1 (Elegir área)

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` antes de darse por cerrado — ver resultado al
final de este documento.

El marco de esta sección (1) se comparte con los pasos 2 y 3, que
tendrán su propia spec — no se repite ahí, se referencia.

---

## 1. Nombre

`002 — Crear Experiencia / Marco + Paso 1 (Área)`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Modal — marco compartido (pasos 1, 2 y 3)

- Ancho: **fijo `912px`**, compartido por los 3 pasos — salió de sumar
  el contenido real de este Paso 1 (4 cards de `200px` + gaps +
  padding), y se reutiliza en los pasos 2 y 3 para que el modal no
  cambie de tamaño entre pasos.
- Alto: ajustado al contenido (Hug) hasta un **máximo de `852px`** —
  misma regla de margen que usan las columnas del Dashboard (`24px`
  arriba y abajo del frame de `900px`). *En producción esto es una
  regla relativa al alto real de la pantalla, no un número fijo — `852`
  es el valor concreto para trabajar en este frame de Figma
  (`1440×900`).* Este Paso 1 no lo alcanza a necesitar; el Paso 2 sí
  (ver su spec).
- Radio `24px`. Fill `#FFFFFF`. Stroke `1px` `#E7E7E7`. Padding `32px`
  (los 4 lados). Auto Layout Vertical, Gap `24px`.

**Fila de encabezado** — patrón de 3 zonas para que el título quede
centrado en el ancho completo del modal, no en el espacio libre que
deja un solo ícono a un lado (*Corrección 2026-08-29: reemplaza el
Space Between título-izquierda/cerrar-derecha de la versión anterior —
unifica con el único modal que ya centraba, `08-spec-unirse-codigo.md`,
en vez de dejar la inconsistencia entre los dos estilos*):
- Auto Layout Horizontal, ancho Fill, Alignment Center. 3 hijos: zona
  izquierda, título, zona derecha.
- **Zona izquierda**: caja invisible `32×32px` — mismo tamaño exacto que
  el botón cerrar, sin relleno, sin ícono, sin interacción. Su único
  propósito es pesar lo mismo que la zona derecha para que el título
  quede matemáticamente centrado, no solo centrado en el espacio que
  sobra. *(Nota de implementación: esto es necesario en Figma porque
  Auto Layout no tiene un equivalente nativo a columnas simétricas; en
  código real esto se resuelve con una rejilla de 3 columnas `1fr auto
  1fr` — la columna central queda centrada sola, sin necesitar ningún
  elemento invisible.)*
- **Título** "Crear experiencia": Inter, `24px / 32px` (H2), peso `700`
  Bold, color `#111111`, centrado.
- **Zona derecha** — Botón cerrar real: `32×32px` (altura Tiny), Radio
  `8px`, Fill transparente. Ícono X `16×16px`, stroke `1.5px`, color
  `#888888`.
  - Hover: Fill `#FAFAF8`.

**Stepper** — Auto Layout Horizontal, Alignment Center. Solo círculos
numerados, **sin label de texto debajo** — el encabezado de cada paso
(ej. "Área · Elige el área...") ya dice en cuál estás; el label repetía
esa misma información y rompía la simetría del stepper sin aportar
nada. 3 pasos en total (Área / Aprendizaje / Detalles — nombres
internos, no se muestran).
- Círculo: `32×32px`, Radio `999px` (Full), número centrado.
  - **Activo:** Fill `#111111`, texto `#FFFFFF` peso `700` Bold, `12/16`.
  - **Completado:** Fill `#555555`, texto `#FFFFFF` peso `700` Bold, `12/16`.
  - **Pendiente:** Fill transparente, Stroke `1px` `#E7E7E7`, texto
    `#888888` peso `400` Regular, `12/16`.
- Línea conectora: Auto Layout Fill (se estira entre círculos), alto
  `1px`. Color `#E7E7E7` (pendiente) o `#555555` (ya recorrido).

### 2.2 Contenido — Paso 1 (Elegir área)

**Subencabezado del paso** — no es un separador tipo "Materiales ·
Selecciona...", es un título + descripción propios de este paso
(distinto del título del modal "Crear experiencia", que es el
encabezado principal). Auto Layout Vertical, Alignment Center, Gap
`4px`, texto centrado:
- Título del paso: "Área" — `16px / 24px` peso `700` Bold, color
  `#111111`.
- Descripción del paso: "Cada experiencia pertenece a una de las 4
  áreas del currículo MEN." — `16px / 24px` peso `400` Regular, color
  `#555555`. Línea propia, debajo del título, no en la misma línea.
  *(Cambio deliberado frente a una versión anterior — "Elige el área
  que vas a trabajar." — que era indistinguible en forma del
  subencabezado del Paso 2; ahora cada paso informa qué es, no solo
  instruye qué hacer, y el contenido real ya los diferencia.)*

**Fila de cards de área** — Auto Layout Horizontal, Gap `16px`:
- 4 cards, una por área: Matemáticas, Lenguaje, Ciencias Naturales,
  Ciencias Sociales — nombres oficiales del MEN, sin acortar (verificado
  contra `curriculo_men_normalizado.json`).
- Cada card: ancho fijo `200px`, alto fijo `112px` (no Fill, no Hug —
  fijo a propósito, para que las 4 se vean iguales sin importar si el
  nombre del área es corto o largo). Radio `16px`, Fill `#FFFFFF`,
  Stroke `1px` `#E7E7E7`. Auto Layout Vertical, Alignment Center,
  Padding `16px`, Gap `8px`.
  - **Default:** Ícono `24×24px`, stroke `2px`, color `#555555`.
    Label `16px / 24px`, peso `500` Medium, color `#555555`.
  - **Hover (sin seleccionar):** Fill `#FAFAF8`.
  - **Seleccionada (persistente — se elige una card, se puede cambiar de
    elección libremente, "Continuar" avanza):** Fill `#F5F3EE`, Stroke
    `2px` `#111111`. Ícono stroke sube de `2px` a **`2.5px`**, color
    `#111111` — mismo peso visual que el texto en negrita, para que no
    se sientan descompensados entre sí. Label peso `700` Bold, color
    `#111111`.

**Íconos sugeridos** (Lucide, ajustables):
- Matemáticas → `calculator`
- Lenguaje → `book-open`
- Ciencias Naturales → `leaf`
- Ciencias Sociales → `globe`

**Fila de acciones** — Auto Layout Horizontal, margen superior `24px`:
- Botón "Continuar": ancho Fill (ocupa todo el ancho del contenido, no
  solo a la derecha), alto `48px` (CTA), Radio `12px`, texto centrado
  `16px / 22px` peso `500` Medium.
  - **Habilitado** (ya hay un área seleccionada): Fill `#111111`, texto
    `#FFFFFF`.
  - **Deshabilitado** (ninguna área seleccionada todavía): Fill
    `#BDBDBD`, texto `#FFFFFF`. No clickeable.

## 3. Texto

- "Crear experiencia" (título del modal).
- "Área · Cada experiencia pertenece a una de las 4 áreas del currículo
  MEN." (encabezado del paso).
- "Matemáticas", "Lenguaje", "Ciencias Naturales", "Ciencias Sociales"
  (labels de las 4 cards).
- "Continuar" (botón).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Hover en cards de área (sin seleccionar): Fill `#FAFAF8`.
- Selección de card: transición del estado Default al Seleccionado
  (color, stroke, peso de texto e ícono) — persiste hasta que se elija
  otra o se cierre el modal.
- Hover en botón cerrar: Fill `#FAFAF8`.
- Botón "Continuar": pasa de Deshabilitado a Habilitado apenas hay una
  card seleccionada.

## 7. Acciones

- Clic en una card de área → la selecciona (estado persistente); un
  clic en otra card cambia la selección, no se pueden elegir dos a la
  vez.
- Clic en "Continuar" (solo si hay un área seleccionada) → avanza al
  Paso 2, con esa área ya aplicada como filtro.
- Clic en el botón cerrar (X) → cierra el modal sin crear nada.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 05-spec-crear-experiencia-paso1.md
OK — 05-spec-crear-experiencia-paso1.md: todos los colores y valores en px están en tokens.json
```

**Historial real de esta verificación, no ocultado:**
1. Primera corrida: encontró un alto de card heredado del spec viejo
   sin revisar, fuera de la escala. Se cambió a alto ajustado al
   contenido (Hug).
2. Al agregar el botón "Continuar", se decidió fijar el tamaño de la
   card en vez de dejarla Hug o Fill — `200×112px`, agregados a
   `tokens.json` de forma deliberada (ver nota en el archivo). También
   se agregó `2.5px` a grosores de borde, para el ícono en estado
   seleccionado. Corrida final, limpia.
3. Corrección de contenido (sin valores nuevos): la descripción del
   subencabezado ("Elige el área que vas a trabajar.") era
   indistinguible en forma de la del Paso 2 — mismo patrón "Elige X que
   vas a trabajar", solo cambiaba el sustantivo. Se reemplazó por un
   texto informativo ("Cada experiencia pertenece a una de las 4 áreas
   del currículo MEN.") que dice qué es el paso, no solo qué hacer.
   Corrida final, limpia.
