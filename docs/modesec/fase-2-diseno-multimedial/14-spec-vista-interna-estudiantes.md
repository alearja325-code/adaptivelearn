# Ventana 011 — Vista Interna de la Experiencia: Tab Estudiantes

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Marco compartido:** hereda `09-spec-vista-interna-marco.md` — sidebar,
encabezado, metadata y nav de tabs no se repiten aquí.

**Mecanismo:** esta pestaña es la "vista de estudiantes/aula" que define
`ADR-010` punto 4 — listado del grupo con detalle por estudiante,
historial, no agregado (a diferencia de Reporte, que sí agrega). Cumple
dos funciones: invitar estudiantes (código) y ver el roster.

---

## 1. Nombre

`011 — Vista Interna de la Experiencia / Tab Estudiantes`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Encabezado de sección — zona fija, no scrollea

**Descripción de sección** — mismo criterio que Resumen y Materiales
(regla compartida documentada en `09-spec-vista-interna-marco.md`: solo
la línea de descripción, sin el título Bold del componente
"Subencabezado del paso"), ancho **Hug**, centrado — se acomoda sola al
centro por el `Alignment Center` del Panel de contenido (*Corrección
2026-08-29: revierte a centrado, ver la nota equivalente en
`10-spec-vista-interna-resumen.md`*):
- "El grupo inscrito en esta experiencia, estudiante por estudiante." —
  `16px / 24px` peso `400` Regular, color `#555555`. A diferencia de
  Reporte (que agrega, "Cuántos estudiantes, por estado..."), acá el
  contenido real es per-estudiante — la frase debe sonar a lista, no a
  conteo, mismo cuidado por el que "Cuántos" se usó en
  `13-spec-modal-reporte.md`.

### 2.2 Fila de acciones — zona fija, no scrollea, **solo si `estado = Publicada`**

**No se renderiza en absoluto mientras `estado = Borrador`** — en ese
estado no tiene ninguna función real (buscar sin nada que buscar,
invitar bloqueado), así que en vez de mostrarla inerte se retira
completa; todo el foco del panel queda en el bloque de 2.3 (Estado 1).
Aparece recién al publicar (Estados 2 y 3):

Auto Layout Horizontal, Gap `12px`, Alignment Center — mismo patrón que
el Bloque 2 del Dashboard (`04-spec-dashboard.md`, líneas 80-94) y la
fila de búsqueda del banco de ítems (`12-spec-modal-banco-items.md`,
sección 2.2):

- **Search Input** — igual al de Dashboard: ancho Fill, alto `44px`,
  Radio `12px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Padding interno
  izq/der `16px`, ícono lupa `16×16px` stroke `1.5px` color `#888888`,
  gap ícono-texto `8px`. Placeholder `16px / 22px` Regular `#888888`:
  "Buscar por nombre". Filtra la lista de 2.3 por nombre de estudiante.
- **Botón "Código de invitación"** — mismo estilo que el botón primario
  del Dashboard ("+ Crear experiencia"): alto `48px`, Radio `12px`,
  Padding izq/der `24px`, texto `16px / 22px` peso `500` Medium, Fill
  `#111111`, texto `#FFFFFF`. **Sin estado Disabled** — al no
  renderizarse esta fila durante Borrador (ver arriba), no existe el
  caso que ese estado tendría que cubrir.

  *Nota de mecanismo — generación vs. visibilidad:* `codigo_invitacion`
  es `NOT NULL UNIQUE` en `Experiencia` (`04-modelo-relacional.md`,
  línea 151) — se genera al crear la experiencia (Paso 3 de creación),
  no al publicar; no hay ninguna razón para volver esa columna nullable
  ni para regenerarla después. Lo que cambia con `estado` es solo si el
  docente puede **ver/copiar** el código desde esta pantalla, no si el
  dato existe. Como consecuencia, el docente nunca tiene forma de
  compartir el código antes de publicar, así que el mensaje de error de
  `08-spec-unirse-codigo.md` (código válido, experiencia en Borrador) no
  ocurre en el flujo normal — pero se mantiene tal cual, sin tocarlo: es
  validación del lado del servidor y no debe depender de que el gate de
  la interfaz sea la única protección.

### 2.3 Área de contenido — zona con scroll

Esta pantalla se comporta según 3 escenarios posibles, mutuamente
excluyentes (no confundir con los 4 estados del veredicto por DBA de
`ADR-022` — son dos escalas distintas: esta es de la pantalla completa,
esa es por estudiante):

**Estado 1 — Borrador (0 estudiantes, no puede haberlos; sin fila de
acciones, ver 2.2):** en este estado la pantalla tiene exactamente 2
elementos propios — el encabezado de sección (2.1) y este bloque, sin
nada entre ambos.

Área de contenido: alto **Fill** (crece para ocupar todo el espacio
restante del panel, ya que no hay fila de acciones empujando desde
arriba), Auto Layout Vertical, Alignment Center, **Justify Center** — a
diferencia del Empty State del Dashboard (que convive con más contenido
y no es la pantalla completa), acá sí lo es, así que el grupo interno
queda centrado tanto horizontal como verticalmente en el espacio real
disponible, no pegado arriba con padding fijo.

Grupo interno (un solo layer, Auto Layout Vertical, Alignment Center):
- Ícono `Users` (grupo de personas), `32×32px`, stroke `2.5px`, color
  `#111111` — mismo color y grosor que el título de abajo, para que
  ícono y texto armonicen como un solo bloque en vez de tres tonos
  distintos compitiendo (ícono, título, descripción). Se descarta el
  tratamiento Disabled del ícono vacío del Dashboard (`#BDBDBD`/`1.5px`)
  — acá no hay nada deshabilitado, es el mensaje central de la pantalla.
- Gap `8px` (ícono → bloque de texto — mismo valor que usa el Empty
  State del Dashboard entre ícono y texto).
- Bloque de texto — reutiliza el componente "Subencabezado del paso"
  (título + descripción, Gap `4px`, centrado —
  `06-spec-crear-experiencia-paso2.md`, sección 2.2), no el texto único
  Muted del Empty State del Dashboard:
  - Título: "Aún no hay estudiantes en esta experiencia." — `16px /
    24px` peso `700` Bold, color `#111111`.
  - Descripción: "Publícala para empezar a invitarlos." — `16px / 24px`
    peso `400` Regular, color `#555555`.
- Gap `24px` (bloque de texto → botón — deliberadamente mayor que los 2
  gaps de arriba: esos agrupan un solo mensaje leído de corrido; este
  separa *leer* de *actuar*, un salto de registro distinto que merece
  más aire, no el mismo gap tratando todo por igual).
- Botón "Publicar experiencia" — mismo estilo CTA (Fill `#111111`,
  texto `16/22` Medium `#FFFFFF`, Radio `12px`, alto `48px`), pero
  ancho **Hug** (no Fill) — es un bloque centrado y flotante, no una
  barra de panel completo como el botón de acción de Materiales (2.4).
  - **Deshabilitado** *(2026-10-21, ADR-026)* mientras alguna evidencia
    incluida tenga menos de 6 ítems activos en el banco: Fill
    `#BDBDBD`, texto `#FFFFFF`. Debajo del botón, Gap `8px`, una línea
    que dice por qué: "Faltan preguntas en N evidencia(s). Revísalas en
    Materiales → Banco de preguntas." — `13px / 20px` (Caption), peso
    `400` Regular, color `#991B1B`. No repite cuáles: eso ya lo marca
    en rojo el contador de cada evidencia dentro del banco
    (`12-spec-modal-banco-items.md`, 2.3).
  - **Habilitado** (todas con 6 o más): como se describe arriba, sin la
    línea de aviso.

**Estado 2 — Publicada, 0 estudiantes unidos todavía:**
A diferencia del Estado 1, acá sí convive con la fila de acciones (2.2,
ya activa) — sin botón propio, la acción ya vive ahí. Mantiene la misma
estructura del Estado 1 (ícono + bloque de texto título/descripción,
mismos gaps `8px`/`4px`, misma tipografía Subencabezado del paso —
título `16/24` Bold `#111111`, descripción `16/24` Regular `#555555`),
sin el botón:
- Ícono `Users`, `32×32px`, stroke `1.5px`, color `#888888` — **no**
  el mismo tratamiento del ícono del Estado 1 (`#111111`/`2.5px`,
  armonizado con un título que lleva a una acción inmediata); acá el
  mensaje es informativo, sin urgencia — coincide además con el único
  patrón que usa este proyecto para íconos en `#888888`: siempre
  `1.5px`, sin excepción, en los otros 10 casos del corpus.
  Gap `8px` (ícono → bloque de texto).
- Título: "Aún no se ha unido ningún estudiante." — `16px / 24px` peso
  `700` Bold, color `#111111`.
- Descripción: "Comparte el código de invitación." — `16px / 24px`
  peso `400` Regular, color `#555555`.

**Estado 3 — Publicada, con estudiantes:**
A diferencia del Estado 2, acá sí convive con la fila de acciones (2.2)
y además tiene su propia lista, con scroll interno si excede el alto
disponible (mismo patrón fijo-arriba/scroll-abajo del resto de la
pestaña).

**Lista, agrupada por estado** — Auto Layout Vertical, Gap `12px` —
una sola lista plana: separador de estado, sus cards de estudiante, el
siguiente separador, sus cards, y así sucesivamente (mismo patrón de
`12-spec-modal-banco-items.md` sección 2.3 y `13-spec-modal-reporte.md`
sección 2.3 — separadores y cards son hermanos directos, sin
contenedor de grupo aparte).

**Se agrupa por estado del veredicto (ADR-022), no alfabético** —
responde la pregunta real de esta pantalla ("¿quién necesita mi
atención?"), mismo criterio consolidado en la Filosofía de separadores
(`03-tokens-diseno.md`). Dentro de cada grupo, orden alfabético por
nombre — ahí sí no hay una dimensión de urgencia que ordenar.

**Orden de los grupos**, de más a menos urgente (mismo criterio que
Reporte):
1. No muestra
2. No concluyente
3. Sin concluir
4. Muestra

Un grupo solo aparece si al menos un estudiante cae en ese estado — sin
grupos vacíos, mismo criterio que banco de ítems y Reporte.

**Separador de estado** — mismo componente que "Separador de brecha"
(`13-spec-modal-reporte.md`, sección 2.3): sin caja, sin fondo, sin
padding, Auto Layout Vertical, Gap `4px`:
- Nombre del estado — `13px / 20px` (Caption), peso `700` Bold, color
  del estado correspondiente: "No muestran" → `#7A391F`, "No
  concluyentes" → `#52514E`, "Sin concluir" → `#888888`, "Muestran" →
  `#29578E`.
- Explicación — `13px / 20px` (Caption), peso `400` Regular, color
  `#555555`, una sola línea:
  - "No muestran": "Basta con que no muestren una evidencia del DBA —
    no hace falta que terminen las demás."
  - "No concluyentes": "Terminaron todo, pero alguna evidencia quedó
    ambigua."
  - "Sin concluir": "No han terminado el DBA — pueden no haber
    empezado, o tener alguna evidencia a medias."
  - "Muestran": "Terminaron el DBA completo, mostrando cada una de sus
    evidencias."

**Card de estudiante** — mismo patrón de dos capas que la Card de ítem
del banco (`12-spec-modal-banco-items.md`, sección 2.4) y la Card de
evidencia de Reporte (`13-spec-modal-reporte.md`, sección 2.3):
Contenedor único, Radio `16px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`,
Padding `16px` (los 4 lados), Auto Layout Vertical, Gap `16px`. Sin
indicador de color propio — el estado ya lo dice el separador del
grupo, repetirlo en la card sería la misma redundancia que ya se evitó
en las cards de evidencia de Reporte.

**Capa 1 — fila colapsada** (siempre visible): Auto Layout Horizontal,
Gap `12px`, Alignment Center:
1. **Avatar** — `32×32px`, Radio `999px` (Full), Fill `#E7E7E7`
   (reutiliza el gris de borde ya existente en todo el sistema, no un
   tono nuevo solo para este fondo). Primero en el layout. *(Corrección
   2026-08-29: antes `44×44px` — ese tamaño se justificaba contra un
   bloque de texto de 2 líneas que ya no existe, ver punto 2. `32px` ya
   está en `iconos_px` desde la corrección del hueco de tokens de esta
   misma sesión, no hace falta agregarlo.)*
   - **Ícono por defecto** (silueta de persona), para cuando no se
     eligió avatar al crear la cuenta — es opcional, no obligatorio:
     `16×16px`, stroke `1.5px`, color `#888888`, centrado en el
     círculo. Mismo tamaño que lupa/chevron/expandir en todo el
     proyecto — proporción `50%` del círculo, cómoda sin quedar
     apretada ni perdida.
2. **Nombre** (Fill): `16px / 24px` peso `700` Bold, color `#111111`,
   truncado a una sola línea con elipsis si excede el ancho disponible.
   Mismo tratamiento que el Título de la Row Card del Dashboard
   (`04-spec-dashboard.md`, línea 121) — es el elemento de identidad de
   la card, no un enunciado-preview. **Sin correo** — *(Corrección
   2026-08-29: se retira; ninguna otra card de este proyecto tiene
   elementos apilados en vertical dentro de la fila colapsada — Card de
   DBA, de ítem, de evidencia, todas son una sola línea de texto.
   Apilar Nombre+Email rompía ese patrón sin necesidad.)*
3. **Ícono expandir**: `16×16px`, stroke `1.5px`, color `#888888` —
   chevron derecha colapsada, chevron abajo expandida (mismo criterio
   que las demás cards con 2 capas).

**Capa 2 — separador** (solo si está expandida): línea `1px`, color
`#E7E7E7`, ancho completo.

**Contenido expandido** (solo si está expandida), hijo directo de la
card, mismo Gap `16px`:

**InfoBlock "Evidencias"** — Label `13px / 20px` (Caption) peso `400`
color `#888888`; Value = subgrupo vertical (Auto Layout Vertical, Gap
`8px`), una fila por evidencia del DBA — **lista, no barra**: con
pocas evidencias por DBA (a veces 1 o 2, no todas aplican a formato
cerrado — ADR-006/QA-012), una barra de distribución se degrada a un
bloque de un solo color o una proporción demasiado gruesa para decir
algo; una lista nombra cada evidencia y su resultado, funciona igual
de bien con 1 que con 6.

**Orden de las filas**: el orden oficial del documento DBA del MEN
(`ADR-024`) — dato fijo de la fuente oficial, no hay IA sugiriendo ni
docente reordenando.

- Cada fila, Auto Layout Horizontal, Gap `4px`, Alignment Center — 2
  elementos separados, mismo criterio conceptual que la evidencia "no
  aplica" de la Card de DBA (`06-spec-crear-experiencia-paso2.md`), no
  fundidos en un solo texto corrido: acá el resultado es el caso normal
  de cada fila, no una excepción, y esta lista existe para que el
  docente escanee resultados rápido — separado a la derecha se barre de
  un vistazo, fundido al final de un párrafo obliga a leer cada
  enunciado completo primero. Gap `4px` (no `12px`): en la resolución
  más común (`1920×1024`), casi ninguna evidencia del documento DBA
  completa una sola línea, y la más extensa apenas llega a 1-2 —
  Alignment Center, no Start, porque el caso de varias líneas es la
  excepción, no la regla:
  - **Enunciado completo de la evidencia** (Fill, **sin truncar**):
    `16px / 24px` peso `400` Regular, color `#111111`. *(Decisión
    explícita, distinta del resto de cards del proyecto: acá varias
    evidencias quedan apiladas y comparadas de cerca dentro de la misma
    card — truncar arriesgaba volver 2 evidencias indistinguibles si
    comparten las primeras palabras, un riesgo que no existe en las
    demás cards, donde el enunciado truncado aparece una sola vez por
    card.)*
  - Resultado — `16px / 24px` peso `700` Bold, color del estado
    correspondiente (mismos 4 colores del separador). **Forma
    singular** ("Muestra" / "No muestra" / "No concluyente" / "Sin
    concluir"), no plural — el plural del separador ("Muestran") solo
    aplica cuando el texto acompaña un conteo de personas; acá describe
    el resultado de una sola evidencia para un solo estudiante
    (glosario, entrada "Diagnóstico").

**Botón "Ver historial completo"** — ancho Fill, alto `44px`, Radio
`12px`, Fill `#111111`, texto centrado `16px / 22px` peso `500` Medium,
color `#FFFFFF`. Abre el modal de historial
(`27-spec-modal-historial-estudiante.md`, Ventana 027 — *antes
"diferido, fuera de alcance"; se diseñó el 2026-10-21*): pregunta por pregunta,
qué ítem enfrentó el estudiante por evidencia, su respuesta, y su
certeza (`Respuesta.certeza`, CRI 0-5, ADR-008 punto 2) — información
más granular que la de este InfoBlock, no la misma repetida. La card
expandida responde "¿por qué está en este grupo?"; el historial
responde "¿qué pasó exactamente?" — dos profundidades distintas, no
una redundante con la otra.

## 3. Texto

- "El grupo inscrito en esta experiencia, estudiante por estudiante."
  (descripción de sección — sin título, ver 2.1).
- "Buscar por nombre" (placeholder de búsqueda, solo si `estado =
  Publicada`, ver 2.2).
- "Código de invitación" (botón, solo si `estado = Publicada`).
- "Aún no hay estudiantes en esta experiencia." (título, Estado 1 —
  Borrador).
- "Publícala para empezar a invitarlos." (descripción, Estado 1).
- "Publicar experiencia" (botón, Estado 1).
- "Aún no se ha unido ningún estudiante." (título, Estado 2 — Publicada
  sin estudiantes).
- "Comparte el código de invitación." (descripción, Estado 2).
- "No muestran", "No concluyentes", "Sin concluir", "Muestran" (nombres
  de los separadores de estado, Estado 3, forma plural).
- "Basta con que no muestren una evidencia del DBA — no hace falta que
  terminen las demás." / "Terminaron todo, pero alguna evidencia quedó
  ambigua." / "No han terminado el DBA — pueden no haber empezado, o
  tener alguna evidencia a medias." / "Terminaron el DBA completo,
  mostrando cada una de sus evidencias." (explicaciones de cada
  separador, Estado 3).
- "Evidencias" (label del InfoBlock, Estado 3).
- "Muestra", "No muestra", "No concluyente", "Sin concluir" (resultado
  individual por evidencia dentro de una card expandida, forma
  singular — distinta de los nombres plurales de los separadores).
- "Ver historial completo" (botón, dentro de una card expandida).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Hover en botón "Código de invitación": opacidad `85%` (mismo criterio
  que los botones primarios).
- Hover en botón "Publicar experiencia": opacidad `85%`.
- Transición Borrador → Publicada: el bloque del Estado 1 (encabezado
  de sección + grupo centrado, sin fila de acciones) se reemplaza por
  la fila de acciones (2.2, recién aparece) + Estado 2 o 3 según haya
  o no estudiantes ya unidos.
- Hover en la fila colapsada de una card de estudiante: Fill cambia de
  `#FFFFFF` a `#FAFAF8` (mismo criterio que la Row Card del Dashboard).
- Clic en la fila colapsada → expande/colapsa esa card (chevron rota),
  muestra u oculta el InfoBlock "Evidencias" y el botón "Ver historial
  completo".
- Hover en botón "Ver historial completo": opacidad `85%`.

## 7. Acciones

- Escribir en el buscador (solo si `estado = Publicada`) → filtra la
  lista de 2.3 por nombre (sin efecto visible en el Estado 2, no hay
  nada que filtrar; en el Estado 3, filtra las cards de estudiante,
  respetando los grupos — un grupo sin coincidencias se oculta
  completo, junto con su separador, mismo criterio que la búsqueda del
  banco de ítems).
- Clic en "Código de invitación" (solo si `estado = Publicada`) → abre
  el modal de código (`16-spec-modal-codigo-invitacion.md`).
- Clic en "Publicar experiencia" (Estado 1, solo si Habilitado — ver
  2.3) → abre el modal de confirmación
  (`15-spec-modal-confirmar-publicar.md`).
- Clic en la fila colapsada de una card de estudiante → expande o
  colapsa esa card (2.3, Estado 3).
- Clic en "Ver historial completo" (card expandida) → abre el modal de
  historial de ese estudiante (`27-spec-modal-historial-estudiante.md`,
  Ventana 027). *(Corrección 2026-10-21: antes decía "diferido, fuera
  de alcance" — un botón que no llevaba a nada. A4 se diseñó.)*

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 14-spec-vista-interna-estudiantes.md
OK — 14-spec-vista-interna-estudiantes.md: todos los colores y valores en px están en tokens.json
```

Pasó limpio en la primera corrida — todo reutiliza componentes y
tokens ya aprobados (Search Input y botón primario del Dashboard, Empty
State del Dashboard, Subencabezado del paso de
`06-spec-crear-experiencia-paso2.md`, CTA de Materiales), sin necesitar
agregar ninguno nuevo a `tokens.json`.

**Hueco preexistente encontrado de paso — corregido 2026-08-29.** El
ícono de `32×32px` (Estados 1 y 2) pasaba la verificación no porque `32`
estuviera en `iconos_px` (`[14, 16, 20, 24]` — no lo estaba), sino porque el
script junta todas las categorías de píxeles en un solo conjunto antes
de comparar, y `32` sí existe en `espaciado_px`. El mismo ícono de
`04-spec-dashboard.md` ya "pasaba" por la misma razón — no era un error
introducido acá.

Se corrigió con ambas piezas, no solo una: `verificar_tokens.py` ahora
detecta cuándo un par `N×Npx` es la declaración de un ícono (la palabra
"ícono" aparece hasta 45 caracteres antes en la misma línea — medido
contra todo el corpus real, ver comentario en el script) y en ese caso
exige que el valor esté específicamente en `iconos_px`, no en el pool
general. Y se agregó `32` a `iconos_px` en `tokens.json`, con nota de
por qué (tamaño propio de íconos de Empty State, más grande que los
íconos funcionales normales). Verificado contra los 14 specs de esta
carpeta — 14/14 limpios, cero regresiones — y contra un caso inventado
(`28px` como ícono) para confirmar que el chequeo nuevo sí detecta un
error real, no que "todo pasa" por otra coincidencia.
