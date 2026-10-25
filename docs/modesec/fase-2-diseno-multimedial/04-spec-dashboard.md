# Ventana 001 — Dashboard (Mis experiencias)

**Metodología:** MODESEC — Fase II, punto 3 (ventana estándar aplicada) y
punto 6 (descripción de la ventana por categorías).
**Tokens:** ver `03-tokens-diseno.md` para la tabla completa y el porqué
de cada valor — aquí van los valores mismos, sin necesidad de cruzar
documentos mientras construyes en Figma.

Esta ventana tiene **2 variantes de contenido** sobre la misma
plantilla — docente y estudiante (QA-016: el estudiante no crea, solo se
une).

---

## 1. Nombre

- Frame A: `001 — Dashboard / Mis experiencias (Docente)`
- Frame B: `001 — Dashboard / Mis experiencias (Estudiante)`

## 2. Imagen — construcción paso a paso, con valores exactos

### 2.1 Frame base

- Tamaño: `1440 × 900`.
- Fill: `#F7F6F3`.
- Auto Layout: Horizontal, Padding `24px` (los 4 lados), Gap `24px`.

### 2.2 Sidebar (izquierda, ambas variantes)

- Tamaño: `280px` de ancho fijo × alto Fill.
- Auto Layout: Vertical, Padding `24px` (los 4 lados).
- Radio: `24px`. Fill: `#FFFFFF`. Stroke: `1px`, color `#E7E7E7`, Inside.

*(Nota de fuente: toda la tipografía de esta ventana usa **Inter** en
Figma — instalada por defecto, sin descargar nada. Ver `03-tokens-diseno.md`
para el porqué. No se repite en cada línea de aquí en adelante.)*

**Bloque de perfil** — Auto Layout Vertical, Gap `8px`, Alignment Center:
1. Avatar: `56 × 56px`, Radio `999px` (Full).
2. Nombre: Inter, tamaño `16px`, interlineado `24px`, peso `700` (Bold),
   color `#111111`.
3. Correo: Inter, tamaño `13px`, interlineado `20px`, peso `400`
   (Regular), color `#888888`.

**El bloque completo es un botón** *(2026-10-21, idea de Alejandro)*:
clic en cualquier parte del bloque —avatar, nombre o correo— abre
`26-spec-modal-mi-perfil.md`. Reemplaza al ítem "Mi perfil" (antes
"Configuración") de la navegación secundaria, que se retira: 2 caminos
a la misma pantalla sobran. Mismo patrón que Notion o Slack.
- Ancho Fill (todo el ancho del Sidebar menos su padding), Padding
  `12px`, Radio `12px`, para que la zona clicable y el hover tengan una
  forma clara y no solo el contorno del texto.
- **Hover:** Fill `#FAFAF8`, cursor de mano. Es la única señal de que
  el bloque es clicable — sin ella, un bloque de perfil se lee como
  información fija. Mismo Fill de hover de los ítems de navegación.
- Nombre accesible: "Editar mi perfil".

**Divisor:** línea, alto `1px`, ancho Fill, color `#E7E7E7`. Margen
`24px` arriba y abajo.

**Navegación principal** — Auto Layout Vertical, Gap `4px`:
- Un solo ítem, ambas variantes: **"Mis experiencias"**.
  *(Nota deliberada: "Mis clases" y "Biblioteca" del diseño anterior
  quedan fuera — sus pantallas nunca se diseñaron; mejor omitirlas que
  enlazar a algo inexistente, mismo criterio que con el panel derecho.)*
- Cada ítem: alto `44px`, Radio `8px`, Auto Layout Horizontal, Gap
  `12px`, Padding izquierdo/derecho `12px`.
  - Ícono: `20 × 20px`, stroke `1.5px`, color `#555555` (inactivo).
  - Label: `16px / 22px`, peso `500` (Medium), color `#555555` (inactivo).
  - **Estado activo:** Fill `#F5F3EE`, label peso `700` (Bold), color
    `#111111`, ícono color `#111111` stroke `2px`. *(Sin color nuevo —
    ver `03-tokens-diseno.md`.)*

Espaciador flexible (Fill, empuja lo siguiente al fondo del sidebar).

**Divisor** igual al anterior.

**Navegación secundaria** — mismo tamaño/spacing que la principal, en
estado inactivo siempre: "Cerrar sesión" (un solo ítem).
*(Corrección 2026-10-21: aquí estaba "Configuración", que llevaba a
una pantalla que nunca se diseñó. Primero se renombró a "Mi perfil";
después se retiró, porque el bloque de perfil de arriba ya abre esa
pantalla (`26-spec-modal-mi-perfil.md`). "Cerrar sesión" lleva directo
a Iniciar sesión (`17-spec-auth-login-registro.md`), sin confirmación:
no se pierde nada al salir.)*

### 2.3 Área de contenido (derecha, Fill el ancho restante)

- Radio: `24px`. Fill: `#FFFFFF`. Stroke: `1px` `#E7E7E7`, Inside.
- Auto Layout: Vertical, Padding `32px` (los 4 lados), Gap `32px`.

**Bloque 1 — Encabezado** — Auto Layout Vertical, Gap `4px`:
- Título "Mis experiencias": `32px / 40px`, peso `700` (Bold), color
  `#111111`.
- Subtítulo: `16px / 24px`, peso `400` (Regular), color `#555555`.
  - Docente: *"Crea una experiencia para tu grupo."*
  - Estudiante: *"Únete a una experiencia con el código de tu docente."*

**Bloque 2 — Acciones** — Auto Layout Horizontal, Gap `12px`, Alignment
Center:
- Search Input: Fill (ancho restante), alto `44px`, Radio `12px`, Fill
  `#FFFFFF`, Stroke `1px` `#E7E7E7`. **Padding interno: izquierda `16px`,
  derecha `16px`** (no `14px` — no es múltiplo de 4, no válido en
  nuestra escala; se redondea a `16px`, no `12px`, para que el campo de
  44px de alto no se vea apretado). Auto Layout interno horizontal,
  Alignment Center, gap ícono-texto `8px`. Ícono lupa `16×16px` stroke
  `1.5px` color `#888888`, primero en el layout. Placeholder `16px / 22px`
  Regular, color `#888888`: "Buscar experiencias".
- Botón primario, alto `48px`, Radio `12px`, Fill `#111111`, Padding
  izq/der `24px`, texto `16px / 22px` peso `500` (Medium) color `#FFFFFF`,
  gap ícono-texto `12px`:
  - Docente: "+ Crear experiencia".
  - Estudiante: "→ Unirse con código".
  - *(Cada rol ve solo su botón — no ambos.)*

**Bloque 3 — Filtros (ambas variantes, ejes distintos)**  — Auto Layout
Horizontal, Gap `8px`:
- Filter Chip: alto `40px`, Radio `8px`, Padding izq/der `16px`.
  - Default: Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, texto `16px / 22px`
    Medium, color `#555555`.
  - Selected: Fill `#F5F3EE`, Stroke `1px` `#111111`, texto peso `700`
    Bold, color `#111111`.
- **Docente — chips: "Todas" / "Borradores" / "Publicadas"**.
  *(Corrección 2026-09-12: el chip decía "Borrador", singular, al lado
  de "Publicadas", plural — el chip filtra un subconjunto de la LISTA
  ["mostrar solo las ___"], distinto al Badge de 2.4, que describe UNA
  card puntual ["esta experiencia está en ___"] y sí va en singular, sin
  cambios. "Borradores" concuerda con "Todas"/"Publicadas", mismo
  término que usa Gmail para su carpeta de borradores.)* Estados de
  Experiencia (confirmados): **Borrador** = banco generado, pendiente
  de revisión docente (ADR-005). **Publicada** = docente ya revisó,
  disponible para estudiantes.
- **Estudiante — chips: "Todas" / "No iniciadas" / "En curso" /
  "Completadas"** *(agregado 2026-09-12, corregido en el mismo día —
  ver nota de género en el Badge, 2.4, que aplica igual acá)*. Eje
  distinto al de Docente: el progreso del propio estudiante en cada
  experiencia, no el estado de publicación — un estudiante nunca ve una
  Borrador, así que ese eje seguía sin aplicar, pero este es un dato
  real que sí varía de una experiencia a otra. Mismo componente Filter
  Chip, sin ningún ajuste. Ver Status Badge (Bloque 4) para el origen
  exacto del dato y sus 3 estados.

**Bloque 4 — Lista de experiencias** — Auto Layout Vertical, Gap `12px`:
- Row Card: Radio `16px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Padding
  `16px` (los 4 lados), Auto Layout Horizontal, Gap `12px`, Alignment
  Center Left.
  - **Status Badge — ambas variantes, ejes distintos.** *(Corrección
    2026-09-04: se había retirado para el Estudiante porque el único
    eje que existía entonces —Borrador/Publicada— es del docente, y un
    estudiante nunca ve una Borrador: todas sus cards dirían siempre
    "Publicada", un badge de un solo valor no distingue nada. Esa
    corrección sigue siendo válida para ESE eje. Agregado 2026-09-12,
    sin contradecirla: un eje distinto, el progreso del propio
    estudiante, que sí varía card por card.)* Alto `22px`, Radio `4px`,
    Padding izq/der `8px`, texto `12px / 16px` peso `700` Bold.
    - **Docente** — Borrador: Fill `#F5F3EE`, texto color `#555555`.
      Publicada: Fill `#111111`, texto color `#FFFFFF`.
    - **Estudiante** — 3 estados, derivados sin tocar el MER
      (`Presentación` y `Resultado` ya alcanzan). *(Corrección
      2026-09-12: "No iniciado"/"Completado" en masculino rompía la
      concordancia con "experiencia" que el propio Badge ya usaba en
      "Publicada" — mismo componente, misma card, dos reglas de género
      distintas sin razón. Corregido a femenino, consistente con
      "Publicada".)* **No iniciada** (ninguna Presentación todavía para
      esa Inscripción) — Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, texto
      color `#888888` (Muted). **En curso** (hay Presentación, pero no
      todas las evidencias del DBA tienen ya su Resultado) — Fill
      `#F5F3EE`, texto color `#555555` (mismo combo que "Borrador",
      mismo nivel de énfasis). **Completada** (todas las evidencias del
      DBA ya tienen Resultado) — Fill `#111111`, texto color `#FFFFFF`
      (mismo combo que "Publicada"). Escala deliberada de menos a más
      énfasis según avanza el progreso — ningún color nuevo agregado a
      `tokens.json`.
  - Título: `16px / 24px` peso `700` Bold, color `#111111`.
  - Metadata (junto al título, mismo renglón): `16px / 24px` Regular,
    color `#555555`. *(Corrección 2026-09-12: hasta ahora un solo
    formato para las 2 variantes; se separan porque cada rol necesita
    distinguir cosas distintas entre sus propias cards.)*
    - **Docente:** `"Área · Grado · N estudiantes"` — sin cambios, las
      3 partes distinguen algo real entre las experiencias que un
      mismo docente crea.
    - **Estudiante:** `"Área · Nombre del docente"` — Grado se retira
      (es siempre el propio del estudiante, constante en todas sus
      cards, no distingue nada) y N estudiantes se retira (señal débil
      para el estudiante, a diferencia del docente que la necesita para
      gestionar participación). Se agrega el nombre del docente que
      creó la experiencia — dato que hoy no existe en ningún lado de la
      vista del estudiante, y es lo que de verdad distingue una
      experiencia de otra si llega a tener varias (de distintas
      materias o distintos docentes). Área se conserva — sí puede
      variar entre las experiencias de un mismo estudiante.
  - Ícono ChevronRight: `16 × 16px`, stroke `1.5px`, color `#888888`,
    alineado a la derecha (empujado por Fill en el bloque de texto).
- **Empty state:** Auto Layout Vertical, Alignment Center, Gap `8px`,
  Padding `48px` vertical. Ícono `32×32px` color `#BDBDBD`. Texto
  `16px / 24px` Regular, color `#888888`:
  - Docente: *"Aún no has creado ninguna experiencia."*
  - Estudiante: *"Aún no te has unido a ninguna experiencia."*

## 3. Texto

Ya está completo en el punto 2, en el lugar exacto donde aparece — no se
duplica aquí para que no haya dos versiones del mismo texto.

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Hover en botón primario: opacidad `85%`.
- Hover en Row Card: Fill cambia de `#FFFFFF` a `#FAFAF8`.
- Sin transiciones de página ni animación compleja en esta versión.

## 7. Acciones

- **Docente:** buscar, filtrar por estado, crear experiencia (abre el
  flujo de creación), clic en una card → entra al detalle de esa
  experiencia.
- **Estudiante:** buscar, filtrar por su progreso (No iniciada/En
  curso/Completada), unirse con código (abre modal), clic en una card →
  entra a su vista de esa experiencia.
- **Ambos** *(2026-10-21)*: clic en el bloque de perfil del Sidebar
  (avatar, nombre o correo) → abre `26-spec-modal-mi-perfil.md`; clic
  en "Cerrar sesión" → termina la sesión y lleva a Iniciar sesión, sin
  confirmación.

---

**Fuera de esta spec, ya especificado aparte** *(corrección 2026-10-21 —
decía "se especifican aparte", ya existen)*: el modal "Unirse con
código" (`08-spec-unirse-codigo.md`) y el detalle de una experiencia —
para el docente, la Vista Interna (`09-spec-vista-interna-marco.md` y
sus 3 pestañas); para el estudiante, la pantalla de inicio de la Toma
del diagnóstico (`23-spec-toma-diagnostico.md`, Ventana 020).
