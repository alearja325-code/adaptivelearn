# Ventana 012 — Modal: Confirmar publicación

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Se abre desde:** `14-spec-vista-interna-estudiantes.md`, sección 2.3,
Estado 1 (Borrador) — botón "Publicar experiencia".

---

## 1. Nombre

`012 — Modal: Confirmar publicación`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Marco del modal

Mismo marco que el resto de modales grandes (`05-spec-crear-experiencia-paso1.md`,
sección 2.1, reutilizado también en `12-spec-modal-banco-items.md` y
`13-spec-modal-reporte.md`):
- Ancho **fijo `912px`**.
- Alto: ajustado al contenido (Hug) — corto, no necesita la lógica de
  máximo `852px` ni scroll interno, mismo caso que
  `07-spec-crear-experiencia-paso3.md`.
- Radio `24px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Padding `32px`
  (los 4 lados), Auto Layout Vertical, Gap `24px`.

**Fila de encabezado** — patrón de 3 zonas, título centrado (mismo
criterio unificado en `05-spec-crear-experiencia-paso1.md`, sección
2.1 — construido con este criterio desde el principio, no es una
corrección):
- Auto Layout Horizontal, ancho Fill, Alignment Center.
- Zona izquierda: caja invisible `32×32px`, sin relleno ni interacción
  — pesa lo mismo que el botón cerrar para que el título quede
  centrado en el ancho completo, no en el espacio libre.
- Título: "¿Publicar esta experiencia?" — `24px / 32px` (H2), peso
  `700` Bold, color `#111111`, centrado.
- Zona derecha — Botón cerrar real: `32×32px`, Radio `8px`, Fill
  transparente, ícono X `16×16px` stroke `1.5px` color `#888888`.
  Hover: Fill `#FAFAF8`.

Sin subencabezado ni stepper — no es un flujo de pasos, es una
confirmación puntual.

### 2.2 Card informativa

Mismo componente que la card informativa de Materiales (`11-spec-vista-interna-materiales.md`,
sección 2.3) y del Paso 3 de Crear Experiencia (`07-spec-crear-experiencia-paso3.md`,
sección 2.4) — Radio `16px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`,
Padding `16px` (los 4 lados), Auto Layout Vertical, Gap `16px`, siempre
expandida, alineada a la izquierda (a diferencia del encabezado, este
componente nunca se centra en ningún uso previo — mismo criterio acá).
3 InfoBlocks (Label `13/20` `#888888`, Value `16/24` `#111111`, Gap
`4px`):

**InfoBlock "¿Qué cambia?"**
- Value: "La experiencia pasa de Borrador a Publicada. Desde ese
  momento, tus estudiantes pueden unirse con el código de invitación y
  entrar de inmediato, y el banco de preguntas ya no se puede
  modificar." *(Corrección 2026-10-21, ADR-026: se agrega el
  congelamiento del banco — es la consecuencia que más importa
  conocer antes de confirmar.)*

**InfoBlock "¿Se puede deshacer?"**
- Value: "No. Una vez publicada, no hay forma de devolver esta
  experiencia a Borrador."

**InfoBlock "¿Qué debo revisar antes?"**
- Value: "Tu banco de preguntas y ejercicios, si todavía no lo
  hiciste — tus estudiantes pueden empezar a responder en cuanto
  publiques."

*(Nota de alcance, actualizada 2026-10-21: antes decía que editar
ítems después de publicar dependía de V-2, "todavía sin resolver". V-2
se resolvió como RI-10 en la Quinta revisión del MER, y ADR-026 va más
lejos: el banco entero se congela al publicar. Este modal solo se abre
si cada evidencia ya tiene 6 ítems activos — el botón que lo abre está
deshabilitado si no, `14-spec-vista-interna-estudiantes.md` 2.3.)*

### 2.3 Fila de acciones (footer)

Auto Layout Horizontal, Gap `12px` — mismo patrón que el footer del
Paso 3 de Crear Experiencia (`07-spec-crear-experiencia-paso3.md`,
sección 2.5), sin divisor (no hay zona con scroll de la que separarse,
mismo caso que ese paso):
- **Botón "Cancelar"** (Ghost — sin Fill, sin Stroke, ancho Hug): alto
  `48px`, Padding izq/der `24px`, texto `16px / 22px` peso `500`
  Medium, color `#555555`.
- **Botón "Publicar experiencia"** (ancho Fill, ocupa el resto): alto
  `48px`, Radio `12px`, Fill `#111111`, texto centrado `16px / 22px`
  peso `500` Medium, color `#FFFFFF`. Sin estado Disabled — no depende
  de ningún campo, solo de haber llegado hasta acá.

## 3. Texto

- "¿Publicar esta experiencia?" (título).
- "¿Qué cambia?" — "La experiencia pasa de Borrador a Publicada. Desde
  ese momento, tus estudiantes pueden unirse con el código de
  invitación y entrar de inmediato, y el banco de preguntas ya no se
  puede modificar."
- "¿Se puede deshacer?" — "No. Una vez publicada, no hay forma de
  devolver esta experiencia a Borrador."
- "¿Qué debo revisar antes?" — "Tu banco de preguntas y ejercicios, si
  todavía no lo hiciste — tus estudiantes pueden empezar a responder en
  cuanto publiques."
- "Cancelar", "Publicar experiencia" (botones).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Hover en botón cerrar: Fill `#FAFAF8`.
- Hover en botón "Publicar experiencia": opacidad `85%`.
- Hover en botón "Cancelar": sin cambio de fondo (Ghost, mismo criterio
  que "Volver" en Crear Experiencia).

## 7. Acciones

- Clic en botón cerrar o "Cancelar" → cierra el modal sin cambios,
  vuelve a Tab Estudiantes, Estado 1 (Borrador).
- Clic en "Publicar experiencia" → `Experiencia.estado` pasa a
  Publicada. Cierra el modal. Tab Estudiantes pasa al Estado 2 o 3
  (según haya o no estudiantes ya unidos — hoy siempre Estado 2, ver
  `14-spec-vista-interna-estudiantes.md`).

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 15-spec-modal-confirmar-publicar.md
OK — 15-spec-modal-confirmar-publicar.md: todos los colores y valores en px están en tokens.json
```

Pasó limpio en la primera corrida — todo reutiliza componentes y
tokens ya aprobados (marco de modal grande de Crear Experiencia, Card
informativa de Materiales/Paso 3, footer Ghost+Primario del Paso 3),
sin necesitar agregar ninguno nuevo a `tokens.json`.
