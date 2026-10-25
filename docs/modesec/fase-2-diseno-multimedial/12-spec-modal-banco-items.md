# Ventana 009 — Modal: Banco de preguntas y ejercicios

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Se abre desde:** `11-spec-vista-interna-materiales.md`, sección 2.4 —
botón "Ver banco de preguntas y ejercicios" (card Diagnóstico
seleccionada).

**Ampliación 2026-10-21 — `ADR-026`.** El banco pasa a ser del docente,
no solo algo que revisa. Cambios en esta ventana: contador de ítems
activos por evidencia (2.3), ícono "+" para agregar pregunta en el
separador de cada evidencia (2.3), botones Guardar/Cancelar y reglas de validación en el modo
edición (2.4b, antes no estaba escrito cómo se confirmaba un cambio), y
modo solo lectura cuando la experiencia está Publicada (2.5).

---

## 1. Nombre

`009 — Modal: Banco de preguntas y ejercicios`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Marco del modal

Reutiliza el marco del Modal de Crear Experiencia (`05-spec-crear-experiencia-paso1.md`,
sección 2.1) — mismo tamaño, incluso sin ser el mismo flujo, porque el
contenido es del mismo tipo (lista con scroll interno, encabezado y
zona fija arriba):
- Ancho **fijo `912px`**.
- Alto: ajustado al contenido (Hug) hasta un **máximo de `852px`**.
- Radio `24px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Padding `32px`
  (los 4 lados), Auto Layout Vertical, Gap `24px`.

**Fila de encabezado** — patrón de 3 zonas, título centrado (mismo
criterio que `05-spec-crear-experiencia-paso1.md`, sección 2.1 —
*Corrección 2026-08-29: reemplaza el Space Between título-izquierda de
la versión anterior*):
- Auto Layout Horizontal, ancho Fill, Alignment Center.
- Zona izquierda: caja invisible `32×32px`, sin relleno ni interacción
  — pesa lo mismo que el botón cerrar para que el título quede
  centrado en el ancho completo, no en el espacio libre.
- Título "Banco de preguntas y ejercicios": `24px / 32px` (H2), peso
  `700` Bold, color `#111111`, centrado.
- Zona derecha — Botón cerrar real: `32×32px`, Radio `8px`, Fill
  transparente, ícono X `16×16px` stroke `1.5px` color `#888888`. Hover:
  Fill `#FAFAF8`.

Sin subencabezado ni stepper — no es un flujo de pasos, la barra de
búsqueda y los chips (2.2) ya comunican de qué se trata.

### 2.2 Fila de búsqueda y chips — zona fija, no scrollea

**Búsqueda** — Auto Layout Vertical, Gap `12px` entre esta fila y la de
chips debajo:
- Search Input, ancho Fill: igual al de Dashboard / Paso 2 de Crear
  Experiencia — alto `44px`, Radio `12px`, Fill `#FFFFFF`, Stroke `1px`
  `#E7E7E7`, padding interno `16px` cada lado, gap ícono-texto `8px`,
  ícono lupa `16×16px` stroke `1.5px` color `#888888`.
  Placeholder: "Buscar por evidencia o enunciado...".
  - Filtra sobre dos campos a la vez: el enunciado de la Evidencia (el
    texto del separador, 2.3) y el enunciado del Ítem — no hace falta
    un selector aparte por evidencia, con el volumen esperado (unas
    pocas evidencias por DBA) un campo de texto alcanza.

**Chips de filtro por tipo de ítem** — Auto Layout Horizontal, Gap
`8px` (mismo componente Filter Chip del Dashboard,
`04-spec-dashboard.md`, Bloque 3):
- Filter Chip: alto `40px`, Radio `8px`, Padding izq/der `16px`.
  - Default: Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, texto `16px /
    22px` Medium, color `#555555`.
  - Selected: Fill `#F5F3EE`, Stroke `1px` `#111111`, texto peso `700`
    Bold, color `#111111`.
  - Chips: **"Todos" / "Selección única" / "Emparejar" / "Ordenar"** —
    corresponden 1 a 1 con `Ítem.formato` (`single_choice` /
    `matching` / `ordering`); "Todos" seleccionado por defecto.

### 2.3 Lista de ítems, con separadores de evidencia (área con scroll interno)

Auto Layout Vertical, Gap `12px` — **una sola lista plana**: separador
de evidencia, sus Cards de ítem, el siguiente separador, sus Cards, y
así sucesivamente. Separadores y cards son hermanos directos de este
mismo Auto Layout — no hay un contenedor de grupo aparte por evidencia,
ni padding propio del separador. Única zona que scrollea — encabezado
(2.1) y búsqueda/chips (2.2) quedan fijos.

**Separador de evidencia** — antes de los ítems de cada Evidencia,
siempre visible, sin estado de colapsar (no hay expandir/colapsar en
esta versión — con el volumen esperado de evidencias por DBA no
resuelve un problema real, solo agrega interacción de más a una
pantalla de solo revisar). Solo texto, sin caja, sin fondo, sin
padding, sin ícono ni divisor propios:
- Texto: enunciado de la Evidencia, **truncado a una sola línea con
  elipsis** (mismo tratamiento que "Enunciado truncado" en la fila
  colapsada de las cards) — `13px / 20px` (Caption), peso `700` Bold,
  color `#111111`. Caption por tamaño (no domina la lista al ir
  truncado a una línea, no hace falta más espacio); Bold y `#111111`
  (no `#888888` como las labels de los infoblocks) porque es contenido
  real —la evidencia oficial—, no una etiqueta secundaria, y a este
  tamaño Bold ya no pesa como pesaba en `16px`.
- **Contador de ítems activos** *(corrección 2026-10-21, ADR-026 —
  antes: "sin contador", con una nota que ya anticipaba que Descartar
  lo volvería necesario; con el mínimo para publicar, lo es)*. El
  separador pasa a Auto Layout Horizontal, Space Between: el enunciado
  truncado a la izquierda (Fill) y el contador a la derecha (Hug), en
  la misma línea:
  - Con 6 o más activos: "N activas" — `13px / 20px` (Caption), peso
    `400` Regular, color `#888888`.
  - Con menos de 6: "N activas · faltan X para publicar" — mismo
    tamaño, color `#991B1B` (Error). Es el único lugar donde el
    docente ve qué evidencia bloquea la publicación.
  - "Activas" = ítems no excluidos, sin importar su origen.
  - En modo solo lectura (2.5) se muestra siempre en `#888888`: ya no
    hay nada que corregir.
- **Botón "Agregar pregunta" — ícono "+" al final del separador**
  *(idea de Alejandro, 2026-10-21: reutiliza el separador que ya existe
  en vez de agregar un botón de ancho completo bajo cada evidencia)*.
  Tercer elemento de la misma fila, después del contador, Gap `8px`:
  - Mismo componente que el botón cerrar de los modales: `32×32px`,
    Radio `8px`, Fill transparente, ícono `+` `16×16px` stroke `1.5px`
    color `#555555`. Hover: Fill `#FAFAF8`.
  - **La zona clicable es el cuadro de `32px`, no solo el ícono de
    `16px`.** WCAG 2.2 pide un objetivo de al menos 24×24 px; un ícono
    suelto de 16 no lo cumple.
  - Nombre accesible y texto al pasar el cursor: "Agregar pregunta".
    El ícono solo no dice qué agrega; para un lector de pantalla, y
    para quien duda, el texto sí.
  - No aparece en modo solo lectura (2.5).
- Las Cards de ítem de esa evidencia (2.4) van justo debajo, como
  siguientes hermanas en la misma lista.

### 2.4 Card de ítem

Mismo patrón de dos capas que la Card de DBA
(`06-spec-crear-experiencia-paso2.md`, sección 2.4) — contenedor único:
Radio `16px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Padding `16px`
(los 4 lados), Auto Layout Vertical, Gap `16px`. Toda la card (fila
colapsada, separador, infoblocks) son hijos directos de este mismo
Auto Layout, sin subcontenedores nuevos.

**Capa 1 — fila colapsada** (siempre visible, con acciones accesibles
sin necesidad de expandir): Auto Layout Horizontal, Gap `12px`,
Alignment Center. Sin radio de selección — a diferencia de la Card de
DBA, aquí no se elige nada, solo se revisa:
1. **Badge de tipo de ítem** — mismo componente que el badge "DBA
   [grado]°": alto `22px`, Radio `4px`, Padding izq/der `8px`, Fill
   `#F5F3EE`, texto `12px / 16px` peso `700` Bold, color `#555555`.
   Texto: "Selección única" / "Emparejar" / "Ordenar", según
   `Ítem.formato`.
2. **Enunciado truncado** (Fill, una sola línea con elipsis): `16px /
   24px` peso `400` Regular, color `#111111`.
3. **Divisor vertical**: línea `1px`, color `#E7E7E7`, alto `20px`
   (más alta que los íconos de `16px`, para que se lea como separador
   y no como trazo de un ícono) — separa el contenido del grupo de
   acciones.
4. **Grupo de acciones** (Gap `8px` entre íconos — más cerca entre sí
   que del resto de la fila, para que se lean como un solo grupo). Solo
   dos acciones en esta versión — se descartó una tercera, "Regenerar"
   (sin fundamento en ningún ADR, costo real de API, y Editar ya cubre
   el caso de un ítem que salió mal, ver nota al final del documento):
   - **Editar**: ícono lápiz, `16×16px`, stroke `1.5px`, color
     `#888888`. Comportamiento completo en 2.4.
   - **Descartar**: ícono **ojo tachado**, `16×16px`, stroke `1.5px`,
     color `#888888` — no papelera: "descartar" no elimina el Ítem,
     solo lo excluye de lo que el estudiante ve, de forma reversible
     (campo nuevo `Ítem.excluido`, ver nota al final del documento). Al
     hacer clic, el ítem completo se atenúa (opacidad reducida), su
     texto pasa a Strikethrough, y **el ícono cambia a ojo abierto** —
     mismo par ojo tachado/ojo abierto, no un ícono sin relación. Un
     clic en el ojo abierto revierte al estado normal (vuelve a ojo
     tachado). Sin modal de confirmación — bajo riesgo (el banco
     todavía no está publicado) y el camino de vuelta es inmediato.
5. **Divisor vertical**: mismo tratamiento que el de arriba — separa el
   grupo de acciones del ícono de expandir.
6. **Ícono expandir**: `16×16px`, stroke `1.5px`, color `#888888` —
   chevron derecha colapsada, chevron abajo expandida.

**Capa 2 — separador** (solo si está expandida): línea `1px`, color
`#E7E7E7`, ancho completo.

**Infoblocks** (solo si está expandida) — hijos directos de la card
después del separador, heredan el Gap `16px` y Padding `16px` ya
definidos, sin contenedor propio. Mismo Gap `4px` Label→Value en los
dos:

**InfoBlock "Enunciado"**:
- Label: "Enunciado" — `13px / 20px` (Caption), peso `400` Regular,
  color `#888888`.
- Value: texto completo del enunciado del Ítem — `16px / 24px` peso
  `400` Regular, color `#111111`.

**Segundo InfoBlock — contextual según `Ítem.formato`**, mismo patrón
de "subgrupo dentro del Value" que el InfoBlock "Evidencias" de la Card
de DBA (Auto Layout Vertical, Gap `8px` exclusivo del subgrupo, aparte
del Gap `4px` Label→Value):

- **`single_choice` → Label "Opciones"**: una fila por Opción, Auto
  Layout Horizontal, Gap `8px`, Alignment Center:
  - Letra ("A", "B", "C"...— por `Opción.orden`): `16px / 24px` peso
    `700` Bold, color `#555555`.
  - Texto de la opción (`Opción.texto`): `16px / 24px` peso `400`
    Regular, color `#111111` — si `Opción.es_correcta` es verdadero,
    peso `700` Bold, color `#111111`, y al final de la fila (Space
    Between) un ícono **check dentro de un círculo** `16×16px` stroke
    `1.5px` color `#111111` — mismo ícono en modo lectura y en modo
    edición (2.4b), para no tener dos estilos distintos del mismo
    concepto. *(Deliberado: no se usa ninguno de los 3 colores de
    Resultado de evidencia ni el Informativo — marcar la opción
    correcta de un ítem es un concepto distinto, no se mezclan.)*

- **`matching` → Label "Pares correctos"**: una fila por par, Auto
  Layout Horizontal, Gap `8px`, Alignment Center — agrupa las Opciones
  por `Opción.orden` compartido entre `grupo` izquierda/derecha:
  - Término izquierdo: `16px / 24px` peso `700` Bold, color `#111111`.
  - Conector "→": `16px / 24px` peso `400` Regular, color `#888888`
    (Muted — es puntuación visual, no dato).
  - Término derecho: `16px / 24px` peso `400` Regular, color `#111111`.

- **`ordering` → Label "Orden correcto"**: una fila por Opción, en
  `Opción.orden` ascendente, Auto Layout Horizontal, Gap `8px`,
  Alignment Center:
  - Número (`Opción.orden`): `16px / 24px` peso `700` Bold, color
    `#888888`.
  - Texto de la opción (`Opción.texto`): `16px / 24px` peso `400`
    Regular, color `#111111`.

**Sin InfoBlocks adicionales al final de la card** — el diseño anterior
tenía dos InfoBlocks sin propósito identificable (placeholder sin
etiqueta real); no se reutilizan por no tener función clara en esta
versión. Si aparece una necesidad real más adelante, se agregan
entonces, no antes.

### 2.4b Modo edición (ícono lápiz, 2.3)

Clic en el ícono lápiz obliga a la card a estar expandida (si no lo
estaba) y convierte el contenido de los infoblocks en editable —
**editar el enunciado y su contenido**, término genérico: no se llama
"editar opciones" porque eso solo tiene sentido para `single_choice`
(las labels de cada infoblock — Opciones, Pares correctos, Orden
correcto — se quedan igual, cada una en su formato). Sin
drag-and-drop, sin reordenar arrastrando — mismo criterio de
simplicidad ya aplicado en todo el sistema:

- **InfoBlock "Enunciado"**: el Value pasa a ser un campo de texto
  editable (mismo tamaño/tipografía que en modo lectura, con un
  Stroke `1px` `#E7E7E7` para marcar que es un input, foco cambia el
  Stroke a `#111111` — mismo criterio que los demás campos de texto ya
  definidos, ej. Nombre del Paso 3).
- **`single_choice`**: el texto de cada Opción pasa a campo editable.
  El ícono círculo-check ahora es clickeable en **todas** las filas,
  no solo la correcta — la opción correcta muestra el círculo-check
  relleno; las demás muestran un **círculo con "−"** (mismo círculo,
  contenido distinto), indicando que se puede tocar para volverla la
  correcta. Clic en el círculo de otra opción → esa pasa a
  círculo-check relleno, la anterior pasa a círculo-"−" — solo una
  correcta a la vez.
- **`matching`**: término izquierdo y derecho de cada par pasan a
  campos editables. El número de `Opción.orden` (que define qué
  términos forman pareja) pasa a un **input numérico editable** — con
  eso el docente puede reasignar parejas escribiendo un número
  distinto, sin arrastrar nada.
- **`ordering`**: el texto de cada Opción pasa a campo editable, y su
  número de `Opción.orden` pasa a **input numérico editable** — mismo
  criterio que `matching`, reordenar es escribir un número nuevo.

**Agregar y quitar opciones** *(2026-10-21, ADR-026 — necesario para
que una pregunta creada desde cero no quede atada al mínimo)*:
- Debajo de la última opción/par/paso, un enlace de texto: "+ Agregar
  opción" (`single_choice`), "+ Agregar par" (`matching`, agrega una
  opción en cada grupo) o "+ Agregar paso" (`ordering`) — `16px / 22px`
  peso `500` Medium, color `#555555`, subrayado (mismo tratamiento de
  enlace que `17-spec-auth-login-registro.md`).
- Al final de cada fila editable, un botón "×" `16×16px` stroke `1.5px`
  color `#888888` que la quita. **Solo aparece mientras el ítem esté por
  encima del mínimo de su formato** (RI-4: 2 en `single_choice` y
  `ordering`, 4 opciones —2 pares— en `matching`); en el mínimo, no se
  dibuja, porque quitar sería imposible.

**Fila de confirmación** — último hijo de la card en modo edición,
Auto Layout Horizontal, Gap `12px`, alineada a la derecha (mismo
patrón Ghost + Primario de los footers de modal, en tamaño de card):
- **"Cancelar"** (Ghost, Hug, alto `44px`, Padding izq/der `16px`,
  texto `16px / 22px` Medium `#555555`) → descarta los cambios y vuelve
  a modo lectura. Si el ítem era nuevo (creado con "Agregar pregunta"),
  desaparece: no se guardó nunca.
- **"Guardar"** (Hug, alto `44px`, Radio `12px`, Padding izq/der
  `16px`, texto `16px / 22px` Medium `#FFFFFF`):
  - **Habilitado** (Fill `#111111`) solo si el ítem cumple las reglas
    de su formato: enunciado no vacío; ninguna opción vacía; mínimo de
    opciones de RI-4; en `single_choice`, exactamente una correcta; en
    `matching` y `ordering`, números de orden completos y sin repetir
    dentro de cada grupo.
  - **Deshabilitado** (Fill `#BDBDBD`) en cualquier otro caso. Mismo
    criterio que Nueva contraseña (`22-spec`): si la regla de
    habilitación es exacta, no hace falta un mensaje de error aparte.
  - Al guardar, `Ítem.origen` pasa de `ia` a `editado_docente`; un ítem
    creado con "Agregar pregunta" se guarda como `creado_docente`.

**Pregunta nueva (ícono "+" del separador)**: aparece como una card más al
final de su evidencia — la lista se desplaza hasta ella —, **ya expandida y en modo edición**, con el badge
del formato de esa evidencia (el de sus otros ítems — ADR-006 asigna
el formato por evidencia), enunciado vacío y el mínimo de filas de su
formato vacías. En `single_choice`, ninguna marcada como correcta:
Guardar sigue deshabilitado hasta que el docente elija una.

### 2.5 Modo solo lectura — experiencia Publicada

*(2026-10-21, ADR-026.)* Al publicar, el banco se congela: todos los
estudiantes responden sobre el mismo banco, y el Reporte compara cosas
iguales. Mismo modal, con 3 diferencias:
- **Sin acciones de ítem:** desaparecen el lápiz, el ojo y sus 2
  divisores verticales. Queda badge + enunciado + chevron. Los ítems
  excluidos antes de publicar siguen viéndose atenuados y tachados,
  para que el docente sepa que existieron y no se usan.
- **Sin el ícono "+"** en los separadores, y el contador de cada evidencia en
  `#888888`.
- **Aviso fijo** en la zona de búsqueda/chips (2.2), debajo de los
  chips: "Esta experiencia ya está publicada. El banco ya no se puede
  modificar." — `13px / 20px` (Caption), peso `400` Regular, color
  `#555555`.

## 3. Texto

- "Banco de preguntas y ejercicios" (título del modal).
- "Buscar por evidencia o enunciado..." (placeholder de búsqueda).
- "Todos", "Selección única", "Emparejar", "Ordenar" (chips de filtro).
- "Selección única", "Emparejar", "Ordenar" (badge de cada card de
  ítem — mismo texto que los chips, por diseño: son la misma
  categoría).
- "Enunciado", "Opciones", "Pares correctos", "Orden correcto" (labels
  de los infoblocks).
- "N activas" / "N activas · faltan X para publicar" (contador del
  separador de evidencia).
- "Agregar pregunta" (nombre accesible y texto al pasar el cursor del
  ícono "+" del separador).
- "+ Agregar opción" / "+ Agregar par" / "+ Agregar paso" (modo
  edición).
- "Cancelar", "Guardar" (fila de confirmación del modo edición).
- "Esta experiencia ya está publicada. El banco ya no se puede
  modificar." (aviso, modo solo lectura).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Expandir/colapsar una card de ítem: el chevron cambia de dirección,
  los infoblocks aparecen o desaparecen — sin animación compleja
  (mismo criterio que la Card de DBA). Los separadores de evidencia no
  tienen este comportamiento — son texto fijo, sin estado.
- Escribir en la búsqueda o tocar un chip: la lista se filtra al
  instante.
- Clic en Descartar (ojo tachado): la card baja de opacidad y su texto
  pasa a Strikethrough al instante; el ícono cambia a ojo abierto sin
  animación compleja. Revertir (clic en ojo abierto) es el mismo
  cambio, al revés.
- Clic en Editar (lápiz): los Values de los infoblocks cambian de texto
  fijo a campos editables al instante — sin animación compleja.
- "Guardar": Deshabilitado → Habilitado apenas el ítem cumple las
  reglas de su formato (2.4b), y al revés si deja de cumplirlas.
- El contador de una evidencia cambia de número, y de color
  (`#888888` ↔ `#991B1B`) al cruzar el umbral de 6, al instante.
- Hover en botón cerrar: Fill `#FAFAF8`.

## 7. Acciones

- Escribir en la búsqueda → filtra los ítems visibles por evidencia o
  enunciado; una evidencia sin ítems que coincidan se oculta por
  completo, junto con su separador.
- Tocar un chip → filtra por `Ítem.formato`; combina con la búsqueda si
  ambas están activas.
- Clic en el chevron de una card de ítem → expande/colapsa esa card,
  mostrando u ocultando los infoblocks.
- Clic en el botón cerrar (X) → cierra el modal, vuelve a la Vista
  Interna, tab Materiales.
- **"Publicar experiencia" no vive en este modal.** Se consideró
  agregarlo aquí, pero se descartó: revisar el banco no es un
  prerrequisito real para publicar (el docente puede no abrir este
  modal nunca y aun así publicar), y publicar cambia `Experiencia.estado`
  completo, no algo específico de este material. Va a vivir en la
  pantalla de la Vista Interna donde ya están el código de invitación y
  la gestión de estudiantes (`14-spec-vista-interna-estudiantes.md`) —
  junto con su modal de confirmación (`15-spec-modal-confirmar-publicar.md`).
  *(Corrección 2026-10-21: decía "pendiente, se especifica aparte".)*
- Clic en el ojo tachado de un ítem → lo descarta: se atenúa, texto
  Strikethrough, `Ítem.excluido` pasa a verdadero. El ícono cambia a
  ojo abierto. Sin modal de confirmación.
- Clic en el ojo abierto de un ítem descartado → lo vuelve a incluir,
  `Ítem.excluido` pasa a falso, el ícono regresa a ojo tachado.
- Clic en el lápiz de un ítem → activa el modo edición de esa card
  (2.4b): expande la card si no lo estaba, y los Values de los
  infoblocks pasan a campos editables.
- Clic en "Guardar" (solo si Habilitado) → guarda el ítem, vuelve a
  modo lectura, actualiza `Ítem.origen` (2.4b) y el contador de su
  evidencia.
- Clic en "Cancelar" → descarta los cambios; si el ítem era nuevo, lo
  quita.
- Clic en "+ Agregar opción/par/paso" → agrega una fila vacía; clic en
  "×" de una fila → la quita (solo por encima del mínimo, 2.4b).
- Clic en el "+" de un separador → agrega al final de esa evidencia una
  card nueva, expandida y en modo edición (2.4b).
- Descartar o reincluir un ítem → actualiza al instante el contador de
  su evidencia (2.3).
- **Con la experiencia Publicada (2.5):** ninguna de las acciones que
  modifican el banco está disponible; solo buscar, filtrar,
  expandir/colapsar y cerrar.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 12-spec-modal-banco-items.md
OK — 12-spec-modal-banco-items.md: todos los colores y valores en px están en tokens.json
```

Pasó limpio — no se agregó ningún valor nuevo a `tokens.json`. Todo lo
que usa esta ventana ya existía: el marco de Crear Experiencia
(`912`/`852`), el Search Input y el Filter Chip del Dashboard, y el
patrón de dos capas + infoblocks de la Card de DBA (incluido su
subgrupo "Value con Gap `8px` propio", reutilizado para Opciones/Pares
correctos/Orden correcto).

**Correcciones posteriores (sin valores nuevos):**
1. La lista de la sección 2.3 se había descrito con Gap `16px` entre
   grupos — inconsistente con la regla ya documentada en
   `03-tokens-diseno.md` ("12px vs 16px"): el espaciado entre hermanos
   de una lista vertical es `12px`, no `16px` (ese queda reservado para
   la pila interna de una sola card, como sí corresponde dentro de la
   Card de ítem, 2.4). Se corrigió a `12px`, igual que la lista de DBA
   del Paso 2 y la lista de experiencias del Dashboard.
2. El separador de evidencia se había descrito con Padding propio
   (`12px`) y un divisor `1px` debajo — de más: el separador es
   únicamente texto + ícono, sin caja ni fondo. Se corrigió la
   estructura de la sección 2.3 completa a una sola lista plana
   (separador, sus cards, el siguiente separador, sus cards...), sin
   contenedor de grupo aparte por evidencia.
3. El texto del separador pasó por dos ajustes: primero de `16px` Bold
   a `16px` Medium (seguía siendo demasiado grande), y en la corrección
   final se bajó a `13px / 20px` (Caption) Bold, truncado a una sola
   línea con elipsis — a ese tamaño, truncado, Bold ya no domina la
   lista. De paso se eliminó el estado expandir/colapsar del separador
   (quedó solo texto, sin ícono): con el volumen esperado de evidencias
   por DBA no resolvía un problema real.

**Hallazgo real de modelo de datos — formalizado en `ADR-015`
(`/diseno/decisiones.md`):** diseñar las acciones sobre el ítem expuso
que `Ítem` necesita un atributo nuevo, `excluido` (booleano) — para que
"Descartar" sea persistente (se recuerde aunque el docente cierre el
modal y vuelva otro día), no solo un estado visual temporal. La
decisión ya está registrada en `decisiones.md`; falta incorporarla a
`01-modelo-entidad-relacion.md`, que se reconstruye cuando se retome
Fase III — no antes, mismo criterio que se usó con Opción (ADR-014): un vacío
real detectado al diseñar la pantalla, no al revisar el modelo en
abstracto.

**Acciones consideradas y descartadas, con su razón, para que no se
reabra la discusión sin motivo nuevo:**
- **"Regenerar" un ítem con IA** — sin fundamento en ningún ADR, costo
  real de API, y Editar ya cubre el caso de un ítem que salió mal.
  *(Formalizado en `ADR-026`, que además retira la frase "pedir generar
  más" que ADR-009 dejaba viva aun después de que ADR-016 actualizara
  su número de banco: regenerar sin instrucciones daría algo parecido;
  lo que el docente necesita es corregir o agregar él mismo.)*
- **"Eliminar" en vez de "Descartar"** — borrar el Ítem para siempre no
  encaja con una pantalla de revisión (el docente decide qué se
  publica, no limpia la base de datos), y hubiera necesitado su propio
  modal de confirmación por ser irreversible.
- **Badge de tipo de ítem con ancho fijo** (para que los tres midan
  igual) — se descartó por romper la lógica de badges Hug-width que ya
  usa el resto del sistema; se acepta la diferencia de ancho.
- **Ícono de solo tipo de ítem** (sin texto) en vez del badge de texto
  — se descartó: no existe un vocabulario de íconos establecido para
  "selección única/emparejar/ordenar", y el riesgo de que el docente
  malinterprete el formato en una pantalla de revisión pesa más que la
  ganancia visual.
