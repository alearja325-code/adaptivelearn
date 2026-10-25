# Ventana 008 — Vista Interna de la Experiencia: Tab Materiales

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Marco compartido:** hereda `09-spec-vista-interna-marco.md` — sidebar,
encabezado, metadata y nav de tabs no se repiten aquí.

---

## 1. Nombre

`008 — Vista Interna de la Experiencia / Tab Materiales`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Encabezado de sección — zona fija, no scrollea

**Descripción de sección** — mismo criterio ya aplicado en Resumen
(`10-spec-vista-interna-resumen.md`, sección 2.1): solo la línea de
descripción, sin el título Bold del componente "Subencabezado del
paso" (regla compartida documentada en
`09-spec-vista-interna-marco.md`), ancho **Hug**, centrado — se acomoda
solo al centro por el `Alignment Center` del Panel de contenido:
- "Las herramientas de esta experiencia para medir el alcance de las
  evidencias del DBA." — `16px / 24px` peso `400` Regular, color
  `#555555`. Dice qué es esto en el modelo (mismo criterio que
  `06-spec-crear-experiencia-paso2.md`) — sin repetir los nombres de
  las 2 cards de 2.2, la relación real que conecta a Diagnóstico y
  Reportes: las evidencias del DBA que ancla la experiencia (mismo
  hecho que usa Resumen).

*(Corrección 2026-08-26: se retira el título "Recursos". Mismo texto
de descripción, sin cambios. Corrección 2026-08-29: revierte a
centrado, ver la nota equivalente en `10-spec-vista-interna-resumen.md`.)*

### 2.2 Fila de cards de material — zona con scroll

Auto Layout Horizontal, Gap `16px`. Reutiliza la Card de área del Paso
1 (`05-spec-crear-experiencia-paso1.md`, sección 2.2), con **un
ajuste**: ancho **Fill** en vez de fijo `200px` — en el Paso 1 ese
ancho fijo salió de no tener ningún contenedor con tamaño ya definido
(de hecho el modal completo salió de sumar esas 4 cards); acá el Panel
de contenido ya tiene un ancho real heredado del frame, así que las
cards se reparten el espacio disponible en vez de imponer el suyo.
Alto se mantiene fijo en `112px` — el resto sin cambios: Radio `16px`,
Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Auto Layout Vertical, Alignment
Center, Padding `16px`, Gap `8px`.

Solo 2 cards — Diagnóstico y Reportes (ADR-007: Práctica y Verificación
quedan fuera del alcance de esta versión, no se muestran):
- **Diagnóstico**: ícono lupa `24×24px`.
- **Reportes**: ícono gráfico de barras `24×24px`.

Estados, sin cambios respecto al Paso 1:
- **Default**: ícono stroke `2px` `#555555`, label `16/24` peso `500`
  `#555555`.
- **Hover** (sin seleccionar): Fill `#FAFAF8`.
- **Seleccionada** (persistente — Diagnóstico por defecto al entrar):
  Fill `#F5F3EE`, Stroke `2px` `#111111`, ícono stroke `2.5px`
  `#111111`, label peso `700` Bold `#111111`.

### 2.3 Card informativa — zona con scroll

Mismo componente que la card informativa del Paso 3
(`07-spec-crear-experiencia-paso3.md`, sección 2.4) — Radio `16px`,
Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Padding `16px`, Auto Layout
Vertical, Gap `16px`, siempre expandida, 3 InfoBlocks (Label `13/20`
`#888888`, Value `16/24` `#111111`, Gap `4px`). A diferencia del Paso
3, aquí **sí** encaja tal cual la estructura Qué es/Para qué
sirve/Cómo funciona — no es prospectivo (algo que va a pasar), es
retrospectivo (algo que ya existe y se está describiendo).

Contenido, según la card de material seleccionada en 2.2:

**Diagnóstico:**
- **¿Qué es?** — "Es el banco de preguntas y ejercicios generado por
  IA para las evidencias del DBA de esta experiencia, usando como
  referencia el enunciado oficial del MEN."
- **¿Para qué sirve?** — "Te permite obtener una estimación
  aproximada del punto de partida de tus estudiantes frente a cada
  evidencia, antes de intervenir."
- **¿Cómo funciona?** — "Cada evidencia tiene un banco de 12
  preguntas; el sistema decide cuántas responde cada estudiante
  (mínimo 4, hasta 6) según qué tan clara sea su respuesta. El
  resultado nunca es una certeza — muestra, no muestra, o no
  concluyente — y puedes revisar, editar o descartar cualquier
  pregunta antes de que tus estudiantes la vean."

**Reportes:**
- **¿Qué es?** — "Es la vista con los resultados del diagnóstico: el
  estado general por estudiante para todo el DBA, y el detalle
  evidencia por evidencia — construida sobre lo que Diagnóstico
  produce."
- **¿Para qué sirve?** — "Te muestra patrones a nivel de grupo que no
  podrías armar a mano con 30-40 estudiantes — qué evidencias tienen
  brecha aparente, cuáles no, y en cuáles los datos todavía son
  insuficientes."
- **¿Cómo funciona?** — "El estado general de cada estudiante se
  calcula evidencia por evidencia: no muestra si basta una que no
  muestre, sin esperar a que termine el resto. Si ya concluyó todas,
  muestra si todas muestran, o no concluyente si alguna quedó
  ambigua; mientras le falte terminar alguna, cuenta como sin
  concluir. Cada evidencia, además, se etiqueta según la proporción de
  tu grupo en cada estado, calculada, nunca redactada por IA."

*(Corrección 2026-08-26: "veredicto general" → "estado general", para
coincidir con el título real de la sección del modal de Reporte
("Estado general") — eran dos palabras distintas para el mismo concepto,
ambas visibles al docente. Y, mismo día, ADR-022: la versión anterior decía "no
concluyente en los demás casos" — ya no es correcto, "los demás casos"
ahora se divide en "no concluyente" y "sin concluir", dos cosas
distintas.)*

### 2.4 Botón de acción — zona fija, no scrollea

Divisor `1px` `#E7E7E7`, ancho completo, encima del botón — separa
visualmente la zona fija de la zona con scroll que queda detrás.
Margen superior `24px` desde el divisor.

Botón, ancho Fill, alto `48px`, Radio `12px`, Fill `#111111`, texto
centrado `16px / 22px` peso `500` Medium, color `#FFFFFF` — mismo
estilo CTA que "Continuar" / "Crear experiencia". **Contextual** a la
card de material seleccionada:
- Diagnóstico seleccionado: "Ver banco de preguntas y ejercicios" → abre
  el modal del banco (`12-spec-modal-banco-items.md`).
- Reportes seleccionado: "Ver reporte" → abre la vista de Reporte
  (`13-spec-modal-reporte.md`).

## 3. Texto

- "Las herramientas de esta experiencia para medir el alcance de las
  evidencias del DBA." (descripción de sección — sin título, ver 2.1).
- "Diagnóstico", "Reportes" (labels de las cards de material).
- "¿Qué es?", "¿Para qué sirve?", "¿Cómo funciona?" (labels de los
  InfoBlocks — textos completos en 2.3, dos versiones según selección).
- "Ver banco de preguntas y ejercicios", "Ver reporte" (botón, contextual).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Hover en card de material (sin seleccionar): Fill `#FAFAF8`.
- Selección de card de material: cambia la card informativa (2.3) y el
  texto/acción del botón (2.4) al instante — sin animación compleja.
- Hover en botón de acción: opacidad `85%` (mismo criterio que el
  botón primario del Dashboard).

## 7. Acciones

- Clic en una card de material → la selecciona (persistente), actualiza
  la card informativa y el botón de abajo.
- Clic en el botón de acción → abre el modal del banco (Diagnóstico,
  `12-spec-modal-banco-items.md`) o la vista de Reporte (Reportes,
  `13-spec-modal-reporte.md`).

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 11-spec-vista-interna-materiales.md
OK — 11-spec-vista-interna-materiales.md: todos los colores y valores en px están en tokens.json
```

Pasó limpio en la primera corrida — todo reutiliza componentes y
tokens ya aprobados (Card de área del Paso 1, Card informativa del
Paso 3, botón CTA, patrón fijo-scroll-fijo), sin necesitar agregar
ninguno nuevo a `tokens.json`.

**Corrección posterior (sin valores nuevos):** la Card de material se
había descrito con ancho fijo `200px`, copiado sin pensar de la Card de
área del Paso 1 — ese fijo tenía sentido ahí porque no existía ningún
contenedor con ancho propio (de hecho el modal salió de sumar esas
cards). Acá el Panel de contenido ya tiene ancho real, así que se
corrigió a ancho Fill, alto se mantiene fijo en `112px`. De paso se
identificó que el divisor antes del botón (2.4) debía existir también
en el footer del Paso 2 de Crear Experiencia, por la misma razón
(scroll inmediatamente encima) — se corrigió ahí también. Corrida
final, limpia.

**Corrección posterior 2 (2026-08-25) — actualización tras cerrar
`12-spec-modal-banco-items.md` y `13-spec-modal-reporte.md`:** este
spec se escribió antes de formalizar los mecanismos reales de
Diagnóstico y Reporte, así que había quedado desactualizado en 2
puntos concretos:
- La descripción del encabezado (2.1) solo enumeraba los nombres de
  las 2 cards de abajo ("Diagnóstico y Reportes de esta experiencia"),
  sin decir qué son en el modelo — no cumplía la regla ya documentada
  en `06-spec-crear-experiencia-paso2.md`. Se reescribió citando el
  mismo hecho que ya usa `10-spec-vista-interna-resumen.md` (las
  evidencias del DBA que ancla la experiencia).
- La card informativa de Diagnóstico (¿Cómo funciona?) describía un
  mecanismo viejo (preguntas de formato cerrado sin número definido,
  "revisarlo y editarlo antes de publicarlo" — ese último punto ya no
  aplica, "Publicar" vive en Tab Estudiantes, no depende de revisar el
  banco). Se actualizó al mecanismo real (ADR-016: banco de 12,
  mínimo 4/tope 6 adaptativo; ADR-015: Editar/Descartar).
- La card informativa de Reportes tenía un error concreto —
  "brecha extendida" ya no existe (ADR-017 la fusionó en "Brecha
  aparente") — y sus 3 textos solo describían la vista por evidencia
  (2.3 de `13-spec-modal-reporte.md`), sin mencionar "Resultados
  generales" (2.2, ADR-018). Se reescribieron los 3 para cubrir ambas
  secciones y las 3 categorías/estados reales, no solo uno.
