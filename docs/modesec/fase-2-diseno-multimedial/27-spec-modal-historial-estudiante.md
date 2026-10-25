# Ventana 027 — Modal: Historial del estudiante

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Se abre desde:** `14-spec-vista-interna-estudiantes.md`, botón "Ver
historial completo" de una card de estudiante expandida (Estado 3).
Solo docente.
**Origen:** pendiente A4 (`diseno/pendientes.md`), "diferido por
complejidad" desde el 2026-08-29. Mientras tanto el botón existía y no
llevaba a nada. Se diseña el 2026-10-21 con la idea de Alejandro:
**reutilizar el banco de preguntas** (`12-spec-modal-banco-items.md`)
en modo lectura, adaptado para mostrar lo que *un* estudiante vio y
respondió.

**Qué responde, y qué no:** la card expandida de la pestaña Estudiantes
responde "¿por qué está en este grupo?" (resultado por evidencia). Este
modal responde "¿qué pasó exactamente?": qué pregunta se le mostró, en
qué orden, qué respondió, si acertó y con cuánta certeza.
**Sin correo ni datos de identidad** más allá del nombre. Cierra la
tensión anotada en A4: el correo es un dato de identidad, no de
historial, y mezclarlos era justo lo que llevó a descartar un "perfil
con secciones distintas".

**Modelo de datos: sin cambios.** Todo sale de entidades que ya existen:
`Presentación` (qué se mostró, `orden_presentacion`), `Respuesta`
(`certeza`, si fue correcta — persistido, ADR-021), `Respuesta_Opción`
(qué eligió o cómo emparejó/ordenó, `valor_dado`) y `Resultado` (el
estado por evidencia).

---

## 1. Nombre

`027 — Modal: Historial del estudiante`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Marco del modal

El mismo del banco (`12-spec`, 2.1): ancho fijo `912px`, alto Hug hasta
un máximo de `852px`, Radio `24px`, Fill `#FFFFFF`, Stroke `1px`
`#E7E7E7`, Padding `32px`, Auto Layout Vertical, Gap `24px`.

**Fila de encabezado** — 3 zonas, igual al banco: caja invisible
`32×32px`, título centrado, botón cerrar real. Título: **nombre completo
del estudiante** — `24px / 32px` (H2), peso `700` Bold, color
`#111111`.

**Descripción**, debajo, centrada: "Lo que respondió, en el orden en
que se le mostró." — `16px / 24px` (Body), peso `400` Regular, color
`#555555`.

**Sin búsqueda ni chips.** El banco los necesita porque tiene 12 ítems
por evidencia; acá hay como máximo 6 por evidencia (ADR-016), y el
orden importa más que filtrar.

### 2.2 Lista, con separadores de evidencia (única zona con scroll)

Misma lista plana del banco (`12-spec`, 2.3): separador, sus cards, el
siguiente separador... Gap `12px`. Evidencias en el orden oficial del
DBA (ADR-024).

**Separador de evidencia** — mismo componente del banco (enunciado de
la evidencia truncado a una línea, `13px / 20px` Bold `#111111`, Space
Between). A la derecha, en vez del contador del banco, **el resultado
de ese estudiante en esa evidencia**, en singular y con su color —
mismo texto y colores que la card expandida de la pestaña Estudiantes:
"Muestra" `#29578E`, "No muestra" `#7A391F`, "No concluyente"
`#52514E`, "Sin concluir" `#888888`. `13px / 20px`, peso `700` Bold.

**Cards de ítem**, en el orden en que se le presentaron
(`Presentación.orden_presentacion`). Mismo contenedor de dos capas del
banco (Radio `16px`, Stroke `1px` `#E7E7E7`, Padding `16px`, Gap
`16px`), **sin acciones de edición**.

**Capa 1 — fila colapsada**, Auto Layout Horizontal, Gap `12px`,
Alignment Center:
1. Badge de formato — mismo del banco ("Selección única" / "Emparejar"
   / "Ordenar").
2. Enunciado truncado (Fill) — mismo del banco.
3. Divisor vertical `1px` `#E7E7E7`, alto `20px`.
4. **Resultado de la pregunta** — `13px / 20px` (Caption), Hug:
   - "Correcta" — peso `700` Bold, color `#111111`.
   - "Incorrecta" — peso `400` Regular, color `#555555`.
   - "Sin responder" — peso `400` Regular, color `#888888` (se le
     mostró y no respondió: `Presentación` sin `Respuesta`, RI-6).

   **Sin color de estado, a propósito.** Acertar una pregunta no es lo
   mismo que "muestra la evidencia": ADR-008 dice que ni un acierto ni
   un error prueban nada por sí solos, y la regla de
   `03-tokens-diseno.md` es un color = un significado. Si "Correcta"
   usara el azul de "Muestra", el docente leería que una sola pregunta
   bien respondida ya demuestra la evidencia. La diferencia se marca
   con peso y tono, no con color.
5. **Certeza** — "Certeza 4/5", `13px / 20px` (Caption), Regular,
   `#888888`. No aparece si la pregunta quedó sin responder.
6. Divisor vertical + ícono expandir `16×16px` — mismos del banco.

**Capa 2 — expandida:** separador `1px` `#E7E7E7` + InfoBlocks (Label
`13/20` `#888888`, Value `16/24` `#111111`, Gap `4px`):
- **"Enunciado"** — texto completo.
- **Respuesta, según el formato:**
  - `single_choice` → Label "Opciones": todas las opciones, con letra,
    como en el banco. La correcta lleva el ícono check en círculo
    `16×16px` `#111111` (el mismo del banco). La que eligió el
    estudiante lleva al final la etiqueta "Su respuesta" — `13px /
    20px` Bold `#111111`. Si eligió la correcta, las dos marcas quedan
    en la misma fila.
  - `matching` → 2 InfoBlocks: "Pares que formó" (lo que hizo, desde
    `Respuesta_Opción`) y "Pares correctos" (mismo formato del banco,
    término → término).
  - `ordering` → 2 InfoBlocks: "Orden que dio" y "Orden correcto"
    (número + texto, como en el banco).
- **"Certeza"** — "4 de 5". Escala CRI 0-5, la misma que el estudiante
  vio en la Ventana 022 (`23-spec`).
- **Sin responder**: solo "Enunciado", y debajo "Se le mostró esta
  pregunta y no la respondió." — `16px / 24px`, Regular, `#555555`.

### 2.3 Estado vacío

Si el estudiante está inscrito pero todavía no se le mostró ninguna
pregunta (no hay `Presentación`), en lugar de la lista va, centrado:
ícono `32×32px` stroke `1.5px` `#888888` + "Todavía no ha respondido
ninguna pregunta." — `16px / 24px` Bold `#111111`. Mismo patrón de
estado sin acción de `14-spec` (Estado 2).

## 3. Texto

- Título: nombre completo del estudiante (variable).
- "Lo que respondió, en el orden en que se le mostró." (descripción).
- "Muestra" / "No muestra" / "No concluyente" / "Sin concluir"
  (resultado por evidencia, en el separador).
- "Correcta" / "Incorrecta" / "Sin responder" (resultado por pregunta).
- "Certeza N/5" (fila colapsada) y "N de 5" (expandida).
- "Enunciado", "Opciones", "Su respuesta", "Pares que formó", "Pares
  correctos", "Orden que dio", "Orden correcto", "Certeza" (labels).
- "Se le mostró esta pregunta y no la respondió."
- "Todavía no ha respondido ninguna pregunta." (estado vacío).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Expandir/colapsar una card: mismo comportamiento del banco.
- Hover en botón cerrar: Fill `#FAFAF8`.

## 7. Acciones

- Clic en el chevron de una card → expande o colapsa.
- Clic en el botón cerrar (X) → vuelve a la pestaña Estudiantes, con la
  card del estudiante como estaba.
- **Ninguna acción sobre los datos.** Es un registro de lo que pasó;
  nada se edita ni se borra desde acá.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 27-spec-modal-historial-estudiante.md
OK — 27-spec-modal-historial-estudiante.md: todos los colores y valores en px están en tokens.json
```

Sin valores nuevos: el marco `912`/`852`, la lista con separadores y la
card de dos capas son los del banco; los 4 colores de resultado son los
de la Paleta de estado.
