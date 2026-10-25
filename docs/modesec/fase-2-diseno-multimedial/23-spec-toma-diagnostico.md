# Ventana 020-023 — Toma del diagnóstico (estudiante)

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Motivo (A5, `diseno/pendientes.md`):** la razón original por la que se
abrió el flujo del estudiante — resuelve H-2/H-3 de la revisión del
docente. Pausada el 2026-09-04 a favor de A9 (Auth), retomada el
2026-09-26.
**Origen:** se entra aquí desde una card de experiencia del Dashboard
del estudiante (`04-spec-dashboard.md`, Bloque 4), sea porque acaba de
unirse con un código (`08-spec-unirse-codigo.md`) o porque vuelve a una
experiencia en la que ya tiene una Inscripción.

Cuatro ventanas, dos marcos distintos:
- **020 — Pantalla de inicio.** Hereda el marco de Vista Interna
  (`09-spec-vista-interna-marco.md`) — es la única de las cuatro que lo
  usa, porque es la única que necesita identificar de qué experiencia se
  trata antes de empezar.
- **021, 022, 023 — Ítem, Certeza, Cierre.** Heredan el marco de Auth
  (`17-spec-auth-login-registro.md`, sección 2.1) — card centrada
  `480px`, sin sidebar. Una vez que el estudiante presiona "Comenzar" o
  "Continuar" en 020, sale por completo del marco del Dashboard — no
  hay forma de volver a él salvo cerrando la pestaña (ver 3.4).

---

## 1. Nombre

`020 — Toma del diagnóstico / Pantalla de inicio`
`021 — Toma del diagnóstico / Ítem`
`022 — Toma del diagnóstico / Certeza`
`023 — Toma del diagnóstico / Cierre`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Ventana 020 — Pantalla de inicio

**Marco:** reutiliza `09-spec-vista-interna-marco.md` completo (Frame
`1440×900`, Sidebar `280px` sin cambios, Panel de contenido Fill, Radio
`24px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Padding `32px`, Auto
Layout Vertical, Alignment Center) — con 2 diferencias:

1. **Sin nav de tabs, sin su divisor.** Esta pantalla no tiene 3
   secciones que navegar — es un único momento. El contenido va
   directo después de la fila de metadata.
2. **El botón "..." del encabezado ahora sí tiene contenido** — quedaba
   pendiente desde el `09-spec-vista-interna-marco.md` original
   ("Contenido del menú: pendiente, fuera de esta ventana"). Se
   resuelve acá y se corrige por referencia en ese documento (ver nota
   al final de esta sección).

**Fila de encabezado** — mismos 3 zonas de `09-spec-vista-interna-marco.md`:
- Zona izquierda: botón "←". **Vuelve directo al Dashboard, sin
  advertencia** — a diferencia de 021/022, acá todavía no hay ninguna
  respuesta registrada que perder (RI: no puede existir `Presentación`
  antes de que el estudiante presione "Comenzar").
- Título (centro): nombre real de la experiencia.
- Zona derecha: botón "...". **Contenido, una sola acción — sin
  desplegable de varios ítems, porque solo hay una acción real para
  este rol:** clic → abre directo el modal "Salir de esta experiencia"
  (`25-spec-modal-confirmar-eliminar-salir.md`, variante Estudiante).
  *(Se decidió no envolverlo en un menú desplegable: un desplegable con
  un solo ítem agrega un paso sin agregar ninguna opción real — mismo
  criterio que ya evitó un mensaje de error sin causa real en
  `20-spec-auth-elige-rol.md`.)*

**Fila de metadata** — mismo componente (Label+Value, Caption `#888888`
+ Button/Input Bold `#111111`), pero con los campos ya definidos para
el rol Estudiante en `04-spec-dashboard.md` (12 de septiembre): **Área
· Nombre del docente** — 2 pares, no los 5 del docente (Estado, Creada,
Estudiantes y Grado no distinguen nada útil para el estudiante acá,
mismo argumento ya usado para la metadata de su card en el Dashboard).

**Contenido central — reutiliza el patrón de Estado por defecto de
`14-spec-vista-interna-estudiantes.md`, sección 2.3** (ícono `32×32px`
+ título + descripción + botón, todo centrado vertical y
horizontalmente en el panel, sin fila de acciones aparte). **3 estados,
derivados de `04-spec-dashboard.md` (Badge del estudiante), sin agregar
ninguna variable nueva:**

**Corrección 2026-09-27 — título y descripción, en los 3 estados:**
la primera versión usaba `24/32` (H2) y una descripción de hasta 3
oraciones explicando por adelantado reglas del sistema (secuencia
opaca, sin resultados visibles). Alejandro la rechazó, con razón: ni el
tamaño ni la extensión coinciden con el propio patrón que este bloque
dice reutilizar — el Estado 1 real de `14-spec-vista-interna-estudiantes.md`
usa `16px / 24px` Bold para el título y una descripción de una sola
frase corta (ej. "Publícala para empezar a invitarlos.", 5 palabras).
Corregido a ese tamaño y a esa extensión en los 3 estados; las 2 reglas
que la descripción larga intentaba adelantar no se pierden — ya viven
donde de verdad corresponden: la ausencia de contador no necesita
explicarse (simplemente no está, en 021/022), y "solo el docente ve
resultados" ya lo dice, con una frase corta, el Estado C de acá mismo y
el Cierre (2.4).

**Corrección 2026-09-27 (2) — un ícono por estado, no el mismo
repetido.** La primera versión reutilizaba `Play` para A y B, y solo
cambiaba su grosor/color en C — mismo patrón que `14-spec-vista-interna-estudiantes.md`
usa para sus 2 estados (`Users`, sin cambiar de forma). Alejandro lo
rechazó acá: con 3 estados en vez de 2, y con B representando un verbo
distinto a A ("continuar" no es "empezar"), repetir la forma pesa más
de lo que ahorra. Los 3 íconos quedan ligados al verbo real de cada
botón/estado, no solo al criterio de "hay acción vs. no hay acción"
(que se conserva en el grosor/color, sin cambios).

**Estado A — No iniciada** (ninguna `Presentación` todavía para esta
Inscripción):
- Ícono `Play`, `32×32px`, stroke `2.5px`, color `#111111` (empezar —
  mismo tratamiento de énfasis que "Borrador" en la pestaña
  Estudiantes: hay una acción real que tomar).
- Título: "Aún no empezaste esta experiencia." — `16px / 24px`, peso
  `700` Bold, color `#111111`.
- Descripción: "Empecemos cuando quieras." — `16px / 24px`, peso `400`
  Regular, color `#555555`.
- Botón "Comenzar diagnóstico" — ancho Hug, alto `48px`, Radio `12px`,
  Fill `#111111`, texto `#FFFFFF`, `16px / 22px` (Button/Input) peso
  `500` Medium.

**Estado B — En curso** (existe al menos una `Presentación` para esta
Inscripción, pero no todas las evidencias del DBA tienen ya su
`Resultado` — misma condición exacta que ya deriva el Badge "En curso"
del Dashboard):
- Ícono `ArrowRight`, `32×32px`, stroke `2.5px`, color `#111111`
  (continuar, no empezar — mismo grosor/color que A: sigue habiendo una
  acción real, pero es otro verbo).
- Título: "Aún no terminaste esta experiencia." — mismo tratamiento
  tipográfico que el Estado A (mismo eco de cadencia que "Aún no hay
  estudiantes en esta experiencia." del Estado 1 de Tab Estudiantes).
- Descripción: "Sigamos donde quedaste." — mismo tratamiento.
- Botón: mismo componente, texto "Continuar diagnóstico". **Al
  presionarlo, la Ventana 021 se abre así (ADR-031, punto 6):**
  - Si el estudiante salió con una pregunta **mostrada y sin
    responder**, ve **esa misma pregunta**: no pierde uno de sus 6 cupos
    por haber cerrado la pestaña.
  - Si no, sigue como en cualquier otro momento: la evidencia en curso
    (o la siguiente, en el orden oficial), con una pregunta al azar
    entre las que todavía no se le mostraron.
  *(Corrección 2026-10-21: el texto anterior decía a la vez "el
  siguiente ítem pendiente de presentar" y "no un ítem nuevo"; con eso,
  una pregunta abandonada ocupaba un cupo sin respuesta.)*

**Estado C — Completada** (todas las evidencias del DBA ya tienen
`Resultado` — misma condición del Badge "Completada"):
- Ícono `Check`, `32×32px`, stroke `1.5px`, color `#888888` — más
  suave, sin urgencia (mismo criterio que "Publicada, 0 estudiantes" en
  la pestaña Estudiantes: no hay ninguna acción pendiente). **Mismo
  ícono que el de 023 (Cierre)** — es el mismo hecho (terminó) contado
  en 2 momentos distintos, así que comparten forma a propósito, a
  diferencia de A/B/C entre sí.
- Título: "Ya completaste esta experiencia." — mismo tratamiento.
- Descripción: "Tu docente puede ver los resultados." — mismo
  tratamiento. *(Corta a propósito: solo dice el hecho, no argumenta el
  alcance de la versión — esa reflexión pertenece a este documento, no
  al texto que lee el estudiante. La idea a futuro de mostrarle algo al
  estudiante queda anotada en `diseno/pendientes.md`, sección A5, no
  acá.)*
- **Sin botón** — no hay ninguna acción que tomar (mismo patrón que el
  estado sin botón de Estudiantes).

**Corrección retroactiva a `09-spec-vista-interna-marco.md`:** su nota
"Contenido del menú: pendiente, fuera de esta ventana" queda resuelta
en 2 lugares — la variante Docente ("Eliminar experiencia") se
documenta en `25-spec-modal-confirmar-eliminar-salir.md` y se referencia
desde ahí; la variante Estudiante, en esta sección.

### 2.2 Ventana 021 — Ítem

**Marco:** hereda `17-spec-auth-login-registro.md`, sección 2.1 — card
centrada, ancho fijo `480px`, Radio `24px`, Fill `#FFFFFF`, Stroke
`1px` `#E7E7E7`, Padding `32px`, Auto Layout Vertical, Gap `24px`. **Sin
sidebar, sin encabezado, sin botón "←".**

**Sin indicador de progreso, a propósito.** Se consideró agregar una
barra o puntos de avance y se descartó: con una cantidad de ítems que
varía según la certeza reportada (ADR-016, mínimo 4 / tope 6), cualquier
indicador que sugiera un total sería falso una parte de las veces —
mismo principio que ya evita que el proyecto invente un dato que no
tiene (ej. "sin mensaje de error sin causa real" en `20-spec-auth-elige-rol.md`).
**No se le avisa al estudiante por adelantado en 020** (Corrección
2026-09-27) — no es un dato que valga la pena adelantar con texto: la
ausencia de contador simplemente no está, igual que ninguna otra
pantalla del proyecto explica por adelantado algo que no va a
aparecer.

**Enunciado del ítem** — Auto Layout Vertical, Alignment **Left** (no
centrado: un enunciado puede ser largo o tener varias líneas, y texto
largo centrado es más difícil de leer — mismo criterio ya aplicado a
los enunciados de evidencia en `14-spec-vista-interna-estudiantes.md`,
"completo, sin truncar"):
- Texto del enunciado (variable, provisto por el ítem generado): `20px
  / 28px` (H3), peso `500` Medium, color `#111111`.
- Debajo, una línea de instrucción fija: "Elige la opción que mejor
  responda." — `16px / 24px` (Body), peso `400` Regular, color
  `#555555`.

**Opciones de respuesta** — Auto Layout Vertical, Gap `12px` (hermanos
en una lista, regla de `03-tokens-diseno.md`), ancho Fill. Reutiliza el
mismo lenguaje de selección que la Card de rol de
`20-spec-auth-elige-rol.md` (Fill/Stroke/peso cambian al elegir, sin
ícono de radio aparte — no se agrega un componente nuevo para lo mismo
que el sistema ya resuelve con Fill/Stroke), adaptado a fila completa
en vez de card fija, porque el texto de una opción varía en longitud:
- Cada opción: ancho Fill, alto Hug, Radio `12px`, Padding `16px`, Auto
  Layout Horizontal, Alignment Center Left.
  - **Default:** Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`. Texto `16px /
    24px` (Body), peso `400` Regular, color `#111111`.
  - **Hover:** Fill `#FAFAF8`.
  - **Seleccionada** (una sola, exclusiva — es opción múltiple de una
    sola respuesta): Fill `#F5F3EE`, Stroke `2px` `#111111`. Texto
    peso `700` Bold, color `#111111`.
- Cantidad de opciones: variable según el ítem (generado con
  distractores, ADR-008 punto 1) — el layout no fija un número.

**Botón "Siguiente"** — ancho Fill, alto `48px`, Radio `12px`, texto
centrado `16px / 22px` (Button/Input) peso `500` Medium.
- **Deshabilitado** (ninguna opción elegida): Fill `#BDBDBD`, texto
  `#FFFFFF`.
- **Habilitado** (una opción elegida): Fill `#111111`, texto `#FFFFFF`.

**Sin botón "Atrás".** Regla ya confirmada: la secuencia del diagnóstico
es de un solo sentido. Cambiar una respuesta ya enviada rompería la
inmutabilidad que el resto del modelo protege (V-2, RI-10).

### 2.3 Ventana 022 — Certeza

**Marco:** idéntico a 021 — misma card `480px`, mismo Gap `24px`.

**Recordatorio de lo respondido** — Auto Layout Vertical, Gap `4px`,
mismo patrón de "descripción partida en 2 líneas fijas" ya usado en
`18-spec-auth-verifica-correo.md` (texto fijo + dato real en su propia
línea, Bold), para que el estudiante no pierda de vista qué acaba de
elegir mientras piensa su certeza:
- "Elegiste:" — `13px / 20px` (Caption), peso `400` Regular, color
  `#888888`.
- Texto de la opción elegida (tal cual la escribió en 021) — `16px /
  24px` (Body), peso `700` Bold, color `#111111`.

**Título y descripción** — mismo componente de siempre, centrado:
- Título: "¿Qué tan seguro/a estás?" — `24px / 32px` (H2), peso `700`
  Bold, color `#111111`.
- Descripción: "No existe una respuesta correcta o incorrecta en esta
  pregunta — cuéntanos qué tan segura o seguro te sentiste al elegir la
  tuya." — `16px / 24px` (Body), peso `400` Regular, color `#555555`,
  centrado. *(Redactado para que la certeza no se sienta como una
  segunda oportunidad de "acertar" — es una medición honesta, CRI,
  Hasan et al. 1999, ADR-008 punto 2, no una trampa.)*

**Selector de certeza (CRI, escala 0-5) — componente nuevo, primera vez
en el proyecto.** Auto Layout Horizontal, Gap `8px`, Alignment Center,
ancho Hug (centrado por el marco). 6 segmentos, uno por valor (0 a 5):
- Cada segmento: `32×32px` (reutiliza la altura "Tiny" de
  `alturas_control_px`, cuadrado). Radio `8px` (S — control
  seleccionable). Número centrado, `12px / 16px` (Badge Label), peso
  `700` Bold.
  - **Default:** Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, texto
    `#888888` (Muted).
  - **Hover:** Fill `#FAFAF8`.
  - **Seleccionado** (uno solo, exclusivo): Fill `#111111`, texto
    `#FFFFFF` — mismo tratamiento de énfasis que un botón primario, es
    la elección que se va a registrar.
- **Anclas de texto**, una fila debajo del selector, Space Between,
  ancho igual al del selector: "Adiviné" (izquierda) / "Segurísimo/a"
  (derecha) — `13px / 20px` (Caption), peso `400` Regular, color
  `#888888`. Traduce los extremos académicos de la escala CRI (0 =
  adivinó totalmente, 5 = completamente seguro) a lenguaje llano para
  la banda de edad del producto (11 a 17 años) — no se muestran los 4
  valores intermedios en texto, serían ruido sobre un número que ya es
  autoexplicativo en una escala corta.

**Botón "Confirmar"** — mismo componente que "Siguiente" de 021
(Deshabilitado hasta elegir un segmento, Habilitado con uno elegido).
Al confirmar: guarda `Respuesta` (opción elegida en 021 + esta certeza +
`fecha_respuesta`) — pasa primero por la Ventana 024 (Modal: Cargando).

### 2.4 Ventana 023 — Cierre

**Marco:** idéntico a 021/022.

- Ícono `Check` o similar, `32×32px`, stroke `2.5px`, color `#111111`.
- Título: "Terminaste" — `24px / 32px` (H2), peso `700` Bold, color
  `#111111`.
- Descripción: "Tu docente puede ver los resultados." — `16px / 24px`
  (Body), peso `400` Regular, color `#555555`, centrado. *(Corrección
  2026-09-27: misma frase corta del Estado C de 020, en vez de la
  versión anterior con la aclaración de alcance incluida en el texto —
  esa reflexión no le corresponde al estudiante, vive en este
  documento.)*
- Botón "Volver al inicio" — mismo componente de botón primario, Fill
  `#111111`. Lleva al Dashboard del estudiante. La card de esa
  experiencia ya se ve con el Badge "Completada" (04-spec-dashboard.md).

---

## 3. Texto

- "Aún no empezaste esta experiencia." / "Aún no terminaste esta
  experiencia." / "Ya completaste esta experiencia." (títulos de 020,
  por estado).
- "Empecemos cuando quieras." (descripción, Estado A).
- "Sigamos donde quedaste." (descripción, Estado B).
- "Tu docente puede ver los resultados." (descripción, Estado C de 020 —
  misma frase reutilizada como descripción de 023, Cierre).
- "Comenzar diagnóstico" / "Continuar diagnóstico" (botones de 020).
- "Elige la opción que mejor responda." (021).
- "Siguiente" (botón de 021).
- "Elegiste:" (022).
- "¿Qué tan seguro/a estás?" (título de 022).
- "No existe una respuesta correcta o incorrecta en esta pregunta —
  cuéntanos qué tan segura o seguro te sentiste al elegir la tuya."
- "Adiviné" / "Segurísimo/a" (anclas del selector de certeza).
- "Confirmar" (botón de 022).
- "Terminaste" (título de 023).
- "Respondiste todo lo necesario. Tu docente ya puede ver cómo te fue —
  por ahora, esta versión no te muestra el resultado a ti."
- "Volver al inicio" (botón de 023).

## 4. Audio

No aplica. Ninguna tarea del producto depende de audio — decisión ya
declarada (E0, Bloque H) desde antes de diseñar esta pantalla.

## 5. Video

No aplica, mismo motivo.

## 6. Animación

- Clic en una opción de 021 → cambia su Fill/Stroke/peso a Seleccionada;
  si había otra elegida antes, vuelve a Default (selección exclusiva).
  Botón "Siguiente": Deshabilitado → Habilitado.
- Clic en un segmento de 022 → mismo comportamiento exclusivo. Botón
  "Confirmar": Deshabilitado → Habilitado.
- Transición de 021 a 022, y de 022 al siguiente 021 (o a 023 si ya no
  quedan ítems): pasa por la Ventana 024 (Modal: Cargando) mientras se
  registra la `Respuesta` y el sistema decide si sigue o concluye
  (ADR-016).
- Hover en botón "←" de 020: Fill `#FAFAF8` (mismo tratamiento que el
  resto de botones ghost del proyecto).

## 7. Acciones

- 020, botón "←" → vuelve al Dashboard, sin advertencia.
- 020, botón "..." → abre `25-spec-modal-confirmar-eliminar-salir.md`
  (variante Estudiante).
- 020, botón "Comenzar"/"Continuar" → abre 021: la pregunta que quedó
  sin responder, si la hay; si no, una al azar entre las no mostradas
  de la evidencia en curso (ADR-031).
- 021, clic en opción → selecciona (exclusivo).
- 021, "Siguiente" (solo si hay opción elegida) → abre 022, llevando la
  opción elegida.
- 022, clic en segmento → selecciona certeza (exclusivo).
- 022, "Confirmar" (solo si hay certeza elegida) → registra `Respuesta`
  (024, Cargando) → si el sistema decide continuar (ADR-016), vuelve a
  021 con el siguiente ítem; si decide concluir, avanza a 023.
- 023, "Volver al inicio" → Dashboard.
- **Cerrar la pestaña o navegar fuera del navegador, en 021 o en 022**
  (no hay botón "←" visible en estas 2 pantallas — la única forma de
  salir a mitad de camino es esta): dispara la advertencia nativa del
  navegador (`beforeunload`) antes de permitirlo — regla ya confirmada
  ("advertir antes de salir"). Si el estudiante sale de todas formas, no
  se pierde nada a nivel de datos: lo ya respondido queda guardado (cada
  `Respuesta` se registra al confirmar, no al final), y la Inscripción
  vuelve a verse como "En curso" la próxima vez.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 23-spec-toma-diagnostico.md
OK — 23-spec-toma-diagnostico.md: todos los colores y valores en px están en tokens.json
```

Ningún valor nuevo — reutiliza `32px` (Tiny, ya en `alturas_control_px`
e `iconos_px`), `8px`/`12px` (radios y espaciado ya aprobados), y los
colores existentes. El único elemento genuinamente nuevo (el selector
de certeza) se construyó combinando tokens ya aprobados, sin necesitar
agregar ninguno.
