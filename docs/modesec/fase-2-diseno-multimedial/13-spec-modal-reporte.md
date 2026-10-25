# Ventana 010 — Modal: Reporte

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Se abre desde:** `11-spec-vista-interna-materiales.md`, sección 2.4 —
botón "Ver reporte" (card Reportes seleccionada).
**Mecanismo que representa:** ADR-010 (dos vistas de Reporte — esta es
la vista principal, grupo × evidencia), ADR-013 + ADR-017 (umbrales y
categorías de clasificación — ADR-017 simplifica las 4 categorías de
ADR-013 a 3), ADR-016 (mecanismo de Diagnóstico que alimenta estos
resultados — ver `12-spec-modal-banco-items.md` para el banco de
ítems), ADR-001 (las evidencias del MEN son planas, sin secuencia
obligatoria — por eso la sección 2.3 puede agrupar por brecha en vez
de mantener el orden del MEN, sin contradecir nada oficial), y
ADR-018 (mecanismo de la sección 2.2 — cómo se agregan las evidencias
de un mismo estudiante en un solo veredicto por DBA), ADR-022 (revisa
ADR-018: agrega un 4.º estado, "sin concluir", con precedencia sobre
los otros 3 — ver 2.2), y ADR-023 (revisa ADR-013/017: el umbral de
"Datos insuficientes" en 2.3 ahora también cuenta a los estudiantes sin
concluir, no solo a los "no concluyente").

---

## 1. Nombre

`010 — Modal: Reporte`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Marco del modal

Mismo marco que el resto de modales grandes (`05-spec-crear-experiencia-paso1.md`
sección 2.1, reutilizado también en `12-spec-modal-banco-items.md`):
- Ancho **fijo `912px`**.
- Alto: ajustado al contenido (Hug) hasta un **máximo de `852px`**.
- Radio `24px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Padding `32px`
  (los 4 lados), Auto Layout Vertical, Gap `24px`.

**Fila de encabezado** — patrón de 3 zonas, título centrado (mismo
criterio que `05-spec-crear-experiencia-paso1.md`, sección 2.1 —
*Corrección 2026-08-29: reemplaza el Space Between título-izquierda de
la versión anterior*):
- Auto Layout Horizontal, ancho Fill, Alignment Center.
- Zona izquierda: caja invisible `32×32px`, sin relleno ni interacción.
- Título "Reporte": `24px / 32px` (H2), peso `700` Bold, color
  `#111111`, centrado — corto, coincide directo con el botón "Ver
  reporte" que lo abre.
- Zona derecha — Botón cerrar real: `32×32px`, Radio `8px`, Fill
  transparente, ícono X `16×16px` stroke `1.5px` color `#888888`. Hover:
  Fill `#FAFAF8`.

Sin subencabezado adicional — las dos secciones (2.2, 2.3) ya se
explican con su propio título y descripción. Sin barra de
búsqueda/filtro — con el volumen esperado de evidencias por DBA (un
puñado), no resuelve un problema real, mismo criterio ya aplicado en
`12-spec-modal-banco-items.md`. Sin footer con botón — es de solo
lectura; "Publicar experiencia" no vive aquí (ver nota al final de
`12-spec-modal-banco-items.md`).

### 2.2 Sección 1 — Estado general (zona con scroll, junto con 2.3)

**Encabezado de sección** — mismo componente "Subencabezado del paso"
ya usado en Materiales (`11-spec-vista-interna-materiales.md`, sección
2.1) y en Crear Experiencia Paso 2:
- Título: "Estado general" — `16px / 24px` peso `700` Bold, color
  `#111111`. *(Corrección 2026-08-26, ADR-022: antes "Resultados
  generales" — "sin concluir" no es un resultado, es la ausencia de
  uno; "estado" sí cubre los 4 valores sin mentir sobre ninguno.)*
- Descripción: "Cuántos estudiantes, por estado, frente al DBA
  completo." — `16px / 24px` peso `400` Regular, color `#555555`.
  Empieza con "Cuántos" a propósito, no con "el estado de cada
  estudiante": esa segunda forma pone al estudiante como sujeto de la
  frase y se lee como una vista de perfiles uno por uno — que es
  justo lo que hace la *otra* vista de Reporte (Tab Estudiantes,
  ADR-010 punto 4), no esta. Esta sección es un conteo agregado, no un
  listado; "Cuántos" lo deja claro desde la primera palabra.

**4 cards de estado** (ADR-022 agrega la 4.ª — antes eran 3;
"cards de estado", no "de resultado" — mismo motivo que el título de
arriba) —
Auto Layout Horizontal, Gap `16px` (fila horizontal de cards hermanas —
mismo gap que la Fila de cards de área del Paso 1 y la fila de Card de
material en Materiales; `12px` es la regla para listas verticales, no
para esto — corregido), ancho Fill (se reparten el espacio en **4**
partes iguales). Reutiliza el mismo contenedor de la Card de área
(`05-spec-crear-experiencia-paso1.md`, sección 2.2) / Card de material
(`11-spec-vista-interna-materiales.md`, sección 2.2): Radio `16px`,
Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Auto Layout Vertical, Alignment
Center, Padding `16px`, Gap `8px` — mismo shell ya aprobado, solo
cambia el contenido de adentro:
- **Número**, formato `X/total` (ej. "25/45" — no porcentaje: con un
  grupo chico, un porcentaje sugiere más precisión de la que el dato
  tiene; la fracción es honesta sobre el tamaño real de la muestra, y
  de paso repite el total en cada card, así que no hace falta una
  línea de contexto aparte): `24px / 32px` (H2), peso `700` Bold,
  color del estado correspondiente — `#29578E` (Muestra), `#7A391F`
  (No muestra), `#52514e` (No concluyente), **`#888888` (Sin
  concluir — reutiliza el token Muted existente, no se agrega color
  nuevo; contraste 3.5:1 sobre blanco, pasa AA para texto grande, que
  es lo que aplica acá — 24/32 Bold —, ver ADR-022)**.
- **Label** ("Muestran" / "No muestran" / "No concluyentes" / **"Sin
  concluir"** — plural, concuerda con contar varios estudiantes; el
  nombre técnico del estado sigue siendo singular
  "muestra"/"no muestra"/"no concluyente"/"sin concluir" en ADR-008 /
  ADR-022, el glosario y el modelo de datos, esto es solo el texto de
  display cuando acompaña un conteo de personas, no un cambio al
  estado en sí): `16px / 24px` peso `400` Regular, color `#111111` —
  sin colorear, para que el color quede solo en el número y la
  pantalla no se sature (ver revisión de paleta en
  `03-tokens-diseno.md`).

### 2.3 Sección 2 — Estado por evidencia (misma zona con scroll que 2.2)

**Encabezado de sección** — mismo componente, margen superior `24px`
desde el final de 2.2:
- Título: "Estado por evidencia" — mismo tratamiento que el título de
  2.2. *(Corrección 2026-08-26, ADR-022: antes "Resultados por
  evidencia", mismo motivo que 2.2.)*
- Descripción: "El estado de cada evidencia, por separado." — mismo
  tratamiento (parejo con la de 2.2 — mismo dato, agregado vs.
  desglosado). Acá "cada evidencia" como sujeto sí es correcto y no
  genera la misma confusión que en 2.2: no existe ninguna otra vista
  del sistema organizada por evidencia con la que pueda confundirse.

**Lista, agrupada por brecha** — Auto Layout Vertical, Gap `12px` —
una sola lista plana: separador de brecha, sus cards de evidencia, el
siguiente separador, sus cards, y así sucesivamente (mismo patrón de
`12-spec-modal-banco-items.md` sección 2.3 — separadores y cards son
hermanos directos, sin contenedor de grupo aparte).

**Se agrupa por categoría de brecha (ADR-017), no por el orden del
MEN — decisión revisada.** Las evidencias del MEN son planas, sin
secuencia obligatoria entre ellas (ADR-001); agruparlas por qué tan
urgente es cada una sirve directo al propósito ya definido de esta
sección ("para saber en cuál enfocarte"), más que mantener un orden
curricular sin relación con eso.

**Orden de los grupos**, de más a menos urgente:
1. Brecha aparente
2. Datos insuficientes
3. Sin brecha aparente

Un grupo solo aparece si al menos una evidencia cae en esa categoría —
sin grupos vacíos, mismo criterio que el banco de ítems.

**Separador de brecha** — antes de las evidencias de cada categoría,
siempre visible, sin estado de colapsar (mismo criterio que el
separador del banco de ítems). A diferencia de ese separador —que era
solo el texto de la evidencia—, este lleva nombre de la categoría +
una explicación breve, de una sola línea, porque el nombre solo no
basta para que se entienda qué significa. Sin caja, sin fondo, sin
padding — Auto Layout Vertical, Gap `4px` (mismo Gap Label→Value de un
InfoBlock):
- Nombre de la categoría — `13px / 20px` (Caption), peso `700` Bold,
  color del estado correspondiente (mismos 3 colores que tenía el
  badge que se retira de las cards — el color pasa a vivir aquí, a
  nivel de grupo, no repetido por card):
  - "Brecha aparente" — `#7A391F` (Naranja).
  - "Datos insuficientes" — `#52514e` (Gris neutro).
  - "Sin brecha aparente" — `#29578E` (Azul).
- Explicación — `13px / 20px` (Caption), peso `400` Regular, color
  `#555555`, una sola línea, sin extenderse (eso más a fondo va en la
  card informativa de Reportes, `11-spec-vista-interna-materiales.md`
  sección 2.3, no aquí):
  - "Brecha aparente": "Una parte del grupo no muestra esta evidencia."
  - "Datos insuficientes": "Todavía no hay suficientes respuestas
    concluyentes."
  - "Sin brecha aparente": "El grupo, en general, muestra esta
    evidencia."

**Card de evidencia** — a diferencia de la versión anterior (Card
informativa, siempre expandida), ahora **sí colapsa** — mismo patrón
de dos capas que la Card de ítem del banco (`12-spec-modal-banco-items.md`
sección 2.4), **sin badge** (ya no hace falta, la categoría la dice el
separador del grupo) y **sin íconos de acción** (esta pantalla sigue
siendo de solo lectura). Contenedor único: Radio `16px`, Fill
`#FFFFFF`, Stroke `1px` `#E7E7E7`, Padding `16px` (los 4 lados), Auto
Layout Vertical, Gap `16px`.

**Capa 1 — fila colapsada** (siempre visible): Auto Layout Horizontal,
Gap `12px`, Alignment Center:
1. **Enunciado truncado** (Fill, una sola línea con elipsis): `16px /
   24px` peso `400` Regular, color `#111111`.
2. **Ícono expandir**: `16×16px`, stroke `1.5px`, color `#888888` —
   chevron derecha colapsada, chevron abajo expandida.

**Capa 2 — separador** (solo si está expandida): línea `1px`, color
`#E7E7E7`, ancho completo.

**Contenido expandido** (solo si está expandida), hijo directo de la
card, mismo Gap `16px` — **2 InfoBlocks** (no 3 elementos sueltos):

1. **InfoBlock "Evidencia"**: Label `13px / 20px` (Caption) peso `400`
   color `#888888`; Value = enunciado completo (la fila colapsada solo
   alcanza a mostrar una línea truncada — aquí se repite completo).
2. **InfoBlock "Estado"**: mismo tratamiento de Label que el anterior
   *(Corrección 2026-08-26, ADR-022: antes "Resultado" — el Value
   incluye "Sin concluir", que no es un resultado; ver la corrección
   de los títulos de sección para el mismo motivo)*. Value = subgrupo
   vertical (Auto Layout Vertical, Gap
   `8px` — mismo patrón de anidado de 3 niveles ya usado en el
   InfoBlock de Opciones de `12-spec-modal-banco-items.md`: InfoBlock →
   subgrupo del Value → sus partes) con dos elementos:
   1. **Barra apilada** — Auto Layout Horizontal, ancho Fill, alto
      `32px` (reutiliza `alturas_control_px`), Gap `4px`. **4 segmentos**
      (ADR-022 agrega el 4.º — antes eran 3), cada uno con Radio `8px`
      propio (a diferencia de la versión anterior, ya no es un solo
      contenedor con overflow oculto — ahora son piezas separadas por
      el gap). Ancho proporcional al conteo de esta evidencia en cada
      estado, calculado **sobre el ancho disponible después de restar
      los 3 gaps** (con 4 piezas hay 3 huecos entre ellas, no 2 — ancho
      disponible = ancho del contenedor − 3×`4px`; si el ancho se
      reparte sobre el ancho total sin restar los gaps, la barra se
      desborda): `#29578E` (Muestra), `#7A391F` (No muestra), `#52514e`
      (No concluyente), `#888888` (Sin concluir — mismo token Muted que
      la 4.ª card de 2.2, ver ADR-022).
   2. **Fila de leyenda** — Auto Layout Horizontal, Gap `24px`. Un
      grupo por estado, Auto Layout Horizontal, Gap `8px`, Alignment
      Center — `13px / 20px` (Caption), **2 elementos de texto
      separados** (no un solo texto con pesos mezclados — mismo
      criterio que el Número/Label de las 4 cards de 2.2):
      - Punto de color: `8×8px`, Radio `999px` (Full), Fill del color
        correspondiente al estado.
      - Texto 1 — conteo, formato `X/total`: peso `700` Bold, color del
        estado correspondiente (mismo criterio que el Número de 2.2 —
        el color vive en el número).
      - Texto 2 — label ("Muestran" / "No muestran" / "No
        concluyentes" / "Sin concluir", mismo plural que 2.2): peso
        `400` Regular, color `#111111`, sin colorear (mismo criterio
        que el Label de 2.2).
      - Orden: número primero, label después (ej. "**25/45** Muestran")
        — mismo orden que las cards de 2.2, no "label — número" como en
        la primera versión de este spec.

## 3. Texto

- "Reporte" (título del modal).
- "Estado general" (título de sección 1).
- "Cuántos estudiantes, por estado, frente al DBA completo."
  (descripción de sección 1).
- "Muestran", "No muestran", "No concluyentes", "Sin concluir"
  (labels de las 4 cards de la sección 1, y de la leyenda de cada card
  de evidencia en la sección 2 — plural, ver nota en 2.2. ADR-022
  agrega "Sin concluir").
- "Estado por evidencia" (título de sección 2).
- "El estado de cada evidencia, por separado." (descripción de
  sección 2).
- "Brecha aparente", "Datos insuficientes", "Sin brecha aparente"
  (nombre de cada separador de grupo, ADR-013 + ADR-017).
- "Una parte del grupo no muestra esta evidencia.", "Todavía no hay
  suficientes respuestas concluyentes.", "El grupo, en general,
  muestra esta evidencia." (explicación breve de cada separador).
- "Evidencia", "Estado" (labels de los 2 infoblocks de cada card, en
  su estado expandido).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Expandir/colapsar una card de evidencia: el chevron cambia de
  dirección, el contenido expandido (InfoBlock, barra, leyenda)
  aparece o desaparece — sin animación compleja (mismo criterio que la
  Card de ítem del banco). Los separadores de brecha no tienen este
  comportamiento — son texto fijo, sin estado (mismo criterio que el
  separador de evidencia del banco de ítems).
- Hover en botón cerrar: Fill `#FAFAF8`.

## 7. Acciones

- Clic en el chevron de una card de evidencia → expande/colapsa esa
  card, mostrando u ocultando el InfoBlock, la barra y la leyenda.
- Clic en el botón cerrar (X) → cierra el modal, vuelve a la Vista
  Interna, tab Materiales.
- **Pendiente, no en esta versión:** ninguna acción sobre los datos —
  este modal solo muestra lo que Diagnóstico ya produjo (ADR-010,
  ADR-016). La otra vista de Reporte (estudiantes/aula, ADR-010 punto
  4) es la pestaña Estudiantes (`14-spec-vista-interna-estudiantes.md`),
  y "Publicar experiencia" vive ahí mismo, con su modal
  (`15-spec-modal-confirmar-publicar.md`). *(Corrección 2026-10-21:
  decía "se especifica aparte".)*

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 13-spec-modal-reporte.md
```

Todo lo que usa esta ventana ya existía: el marco de modal, el patrón
"Subencabezado del paso", la Card de área/Card de material (para las 4
cards de 2.2), el patrón de dos capas de la Card de ítem y el
separador del banco de ítems (para 2.3), los 3 colores de la Paleta de
estado — Resultado de evidencia, y **`#888888` (Muted), reutilizado
para "Sin concluir" (ADR-022) — token ya existente, ningún color nuevo
agregado a `tokens.json`.** Sin Search Input/Filter Chip, sin badge de
fondo `#F5F3EE` — ninguno de los dos se usa ya en este modal.

**Correcciones posteriores:**
1. Se descartó la idea inicial de crear 3 tintes de fondo para los
   badges de brecha (habría sido el primer badge del sistema con fondo
   variable, rompiendo el patrón ya establecido) — se diferencian solo
   por color de texto.
2. La sección 2.2 (Resultados generales) pasó de una barra apilada
   grande a **3 cards** (reutilizando el shell de la Card de área /
   Card de material) con el número en formato `X/total` — visto
   implementado, la barra grande se veía casi igual a las barras de
   evidencia de la sección 2.3, sin distinguir "esto es el resumen" de
   "esto es el detalle". Se eliminó también la línea aparte de "N
   estudiantes inscritos": el total ya queda repetido en cada card.
3. Los 2 colores de la Paleta de estado (Azul, Naranja) se revisaron a
   versiones más oscuras/apagadas — ver la nota completa en
   `03-tokens-diseno.md`. El Naranja original era, medido, el color más
   saturado y claro de todo el sistema.
4. La descripción de la sección 1 se reescribió — explicaba la
   mecánica de conteo ("cada evidencia cuenta por separado") en vez de
   el propósito de la sección, y de paso mencionaba "evidencia" justo
   antes de una sección que se llama "Resultados por evidencia",
   confundiendo cuál es el resumen y cuál el detalle.
5. Las 3 cards de 2.2 tenían Gap `12px` — error: la regla de `12px` es
   para listas verticales, no para una fila horizontal de cards
   hermanas, que en los dos precedentes reales (Fila de cards de área,
   Paso 1; fila de Card de material, Materiales) usa `16px`. Corregido.
6. Los labels de estado pasaron de singular ("Muestra", "No muestra",
   "No concluyente") a plural ("Muestran", "No muestran", "No
   concluyentes") — acompañan un conteo de varios estudiantes, y el
   singular no concordaba gramaticalmente. El nombre técnico del
   estado (ADR-008, glosario, modelo de datos) sigue en singular, sin
   cambios — esto es solo el texto de display.
7. La sección 2.3 (Barra apilada y Fila de leyenda) quedó, en un
   momento, apuntando a "el mismo componente de 2.2" para su barra y
   leyenda — referencia rota, porque 2.2 dejó de tener barra cuando
   pasó a las 3 cards (corrección 2). Se le devolvió su propia
   definición completa, autónoma.
8. Las descripciones de las secciones 2.2 y 2.3 se reescribieron una
   segunda vez — la primera versión de cada una hacía referencia a la
   otra sección para explicarse (inconsistente: ninguna otra
   descripción del sistema hace eso). Se reescribieron para que cada
   una explique qué es esa sección en el modelo, por separado, mismo
   criterio ya documentado en `06-spec-crear-experiencia-paso2.md`
   (Subencabezado del paso, sección 2.2).
9. El badge de brecha pasó de 4 categorías a 3 (ADR-017) — la división
   de severidad "Brecha extendida"/"Brecha aislada" era la parte menos
   fundamentada del diseño original, y se fusionaron en una sola,
   renombrada "Brecha aparente" (antes se consideró "Brecha
   detectada", descartado por afirmar más certeza de la que el
   diagnóstico puede sostener).
10. La descripción de 2.2 no dejaba claro que el `X/total` cuenta
    estudiantes, no evidencias — mencionaba "evidencias" sin nunca
    decir "estudiante". Corregida.
11. Cambio grande: la sección 2.3 pasó de listar las evidencias en el
    orden oficial del MEN a **agruparlas por categoría de brecha**, con
    separadores (mismo patrón del banco de ítems) — decisión revisada,
    justificada porque ADR-001 ya estableció que las evidencias son
    planas, y agrupar por urgencia sirve más al propósito de la
    sección. El badge de brecha se retiró de cada card (quedó
    redundante con el grupo) y ese color se trasladó al nombre de cada
    separador. Las cards de evidencia dejaron de ser Card informativa
    (siempre expandida) y pasaron al patrón de dos capas de la Card de
    ítem (colapsada por defecto, sin badge ni acciones).
12. El contenido expandido de la Card de evidencia pasó de 3 elementos
    sueltos (InfoBlock "Evidencia", Barra apilada, Fila de leyenda,
    los 3 hermanos directos) a **2 InfoBlocks** ("Evidencia" y
    "Resultado"), donde la barra y la leyenda pasan a vivir juntas
    dentro del Value del segundo — mismo patrón de anidado de 3 niveles
    que el InfoBlock de Opciones del banco de ítems. El gap entre barra
    y leyenda bajó de `12px` a `8px` para seguir ese mismo patrón (la
    regla de `12px` es para hermanos de una lista o filas chicas, no
    para el interior de una card). Se evaluó primero quitar la barra
    del todo (dejar solo la leyenda, igual que las 3 cards de 2.2, que
    no llevan gráfico) pero se decidió conservarla, agrupada bajo su
    propio infoblock.
13. Se formalizó el mecanismo de la sección 2.2 ("Resultados
    generales"), que no estaba definido — ADR-018: regla de todo-o-nada
    para agregar, por estudiante, sus N resultados por evidencia en un
    solo veredicto por DBA (todas muestran → Muestra; al menos una no
    muestra → No muestra; ninguna no muestra pero alguna no concluyente
    → No concluyente), con las evidencias de peso igual entre sí.
14. La Barra apilada del InfoBlock "Resultado" pasó de un solo
    contenedor con overflow oculto (3 segmentos contiguos, sin gap) a 3
    piezas separadas por Gap `4px`, cada una con su propio Radio `8px`
    — visto implementado, se leía mejor así. Se agregó la nota técnica
    de restar el espacio de los gaps al ancho disponible antes de
    repartir la proporción de cada segmento, para que la barra no se
    desborde del 100%. La Fila de leyenda pasó de un solo texto con
    pesos mezclados a 2 elementos de texto separados (Número Bold
    coloreado por estado + Label Regular sin colorear), en ese orden
    (número primero) — mismo criterio que el Número/Label de las 3
    cards de 2.2, no una regla nueva.
15. **ADR-022 agrega un 4.º estado, "Sin concluir"** (2026-08-26): la
    sección 2.2 pasó de 3 a 4 cards, la barra apilada y la leyenda de
    cada card de evidencia (2.3) pasan de 3 a 4 segmentos/entradas. El
    color reutiliza el token Muted (`#888888`), ya existente — no se
    agregó ningún color nuevo a `tokens.json`. La categoría de brecha
    "Datos insuficientes" (separador de 2.3) no cambió de texto —
    ADR-023 amplió qué cuenta hacia su umbral (ahora también "sin
    concluir", no solo "no concluyente"), pero el label y la
    explicación visibles siguen siendo los mismos, ya los cubrían.
16. **Renombrado "resultado" → "estado" en 4 lugares** (2026-08-26,
    mismo ADR-022): "Resultados generales" → "Estado general";
    "Resultados por evidencia" → "Estado por evidencia"; "cards de
    resultado" → "cards de estado"; `InfoBlock "Resultado"` →
    `InfoBlock "Estado"`. Motivo: "Sin concluir" no es un resultado, es
    la ausencia de uno — llamar "resultado" a un conjunto que incluye
    esa ausencia era impreciso, mismo tipo de error que ya se corrigió
    antes con "Brecha detectada" (ADR-017, afirmaba más certeza de la
    que había). Las descripciones de 2.2 y 2.3 se reescribieron de
    paso, más cortas que su primera versión — y la de 2.2 no arranca
    con "el estado de cada estudiante" porque esa forma sonaba a una
    vista de perfiles uno por uno (que es la *otra* vista de Reporte,
    Tab Estudiantes, no esta); arranca con "Cuántos" para dejar claro
    que es un conteo agregado.
