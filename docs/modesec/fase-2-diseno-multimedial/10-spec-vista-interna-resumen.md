# Ventana 007 — Vista Interna de la Experiencia: Tab Resumen

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Marco compartido:** hereda `09-spec-vista-interna-marco.md` — sidebar,
encabezado, metadata y nav de tabs no se repiten aquí. "Resumen" es la
pestaña activa por defecto al entrar a una experiencia.

---

## 1. Nombre

`007 — Vista Interna de la Experiencia / Tab Resumen`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Encabezado de sección — zona fija, no scrollea

**Descripción de sección** — no el componente completo "Subencabezado
del paso" de Crear Experiencia, solo su línea de descripción (regla
compartida documentada en `09-spec-vista-interna-marco.md`: dentro de
las 3 pestañas, sin el título Bold, que competía en tipografía con el
nav activo y la fila de metadata). Ancho **Hug**, centrado — se acomoda
solo al centro por el `Alignment Center` del Panel de contenido
(`09-spec-vista-interna-marco.md`, sección 2.3). *(Corrección
2026-08-29: revierte la versión anterior, que la dejaba alineada a la
izquierda — esa decisión se tomó antes de unificar el criterio de
centrado en todo el marco compartido, ver `09-spec-vista-interna-marco.md`
y la fila de encabezado de `05-spec-crear-experiencia-paso1.md`.)*
- "El DBA que ancla esta experiencia, con sus evidencias oficiales." —
  `16px / 24px` peso `400` Regular, color `#555555`.

*(Corrección 2026-08-26: se retira el título "Aprendizaje". Mismo
texto de descripción, sin cambios — ya cumplía la regla de decir qué es
esto en el modelo.)*

Este encabezado de sección queda del lado **fijo** del panel, igual que
la fila de encabezado, metadata y nav de tabs del marco compartido —
solo lo que sigue (2.2) scrollea.

### 2.2 Card de DBA — zona con scroll, siempre visible, sin selección

Radio `16px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Padding `16px`
(los 4 lados), Auto Layout Vertical, Gap `16px`. A diferencia de la
Card de DBA del Paso 2 (`06-spec-crear-experiencia-paso2.md`), aquí
**no hay** radio de selección, badge, ni ícono de expandir — no hay
nada que seleccionar (es la única DBA de la experiencia) ni que
colapsar (siempre está completa). El badge se descartó también: ya es
redundante con "Área" y "Grado" de la fila de metadata del marco
compartido.

Contenido: los mismos 3 InfoBlocks del Paso 2, mismos valores y mismo
tratamiento — reutilizados sin cambios, con los datos reales de la DBA
de esta experiencia:

  **InfoBlock "Enunciado"** — Label `13/20` Caption `#888888`, Gap
  `4px`, Value `16/24` Body `#111111`: texto completo del enunciado
  del DBA.

  **InfoBlock "Evidencias"** — mismo Label. Value: subgrupo propio
  (Auto Layout Vertical, Gap `8px`), una fila por evidencia:
  - Aplica a formato cerrado: `16/24` Regular, color `#111111`.
  - No aplica: mismo tamaño, decoración Strikethrough, seguido de
    " — no aplica a formato cerrado" en color `#6D28D9` (Informativo —
    mismo tratamiento del Paso 2, no el rojo de Error, son conceptos
    distintos).

  **InfoBlock "Ejemplo"** — mismo Label. Value: solo texto (mismo
  criterio del Paso 3 — sin imagen en esta versión).

El Panel de contenido (heredado del marco compartido) tiene alto
**Fill**, igual que el Sidebar — ambos ocupan los `852px` disponibles
de forma fija, para que el Sidebar nunca desaparezca al hacer scroll.
Si el enunciado + evidencias + ejemplo de este DBA exceden ese alto, es
la Card de DBA (2.2) la que scrollea internamente — el encabezado de
sección (2.1), y todo lo del marco compartido, quedan fijos arriba.
*(Corrección respecto a la versión anterior de este archivo, que decía
que scrollaba la página completa.)*

## 3. Texto

- "El DBA que ancla esta experiencia, con sus evidencias oficiales."
  (descripción de sección — sin título, ver 2.1).
- "Enunciado", "Evidencias", "Ejemplo" (labels de los InfoBlocks).
- " — no aplica a formato cerrado" (texto informativo, evidencia
  descartada).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

Ninguna — es contenido estático, sin interacción (no hay selección, no
hay expandir/colapsar).

## 7. Acciones

Ninguna dentro de esta pestaña — es de solo lectura. Cambiar de pestaña
(Materiales, Estudiantes) es una acción del marco compartido, no de
este contenido.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 10-spec-vista-interna-resumen.md
OK — 10-spec-vista-interna-resumen.md: todos los colores y valores en px están en tokens.json
```

**Historial real, no ocultado:** primera corrida limpia en valores —
todo reutiliza tokens ya aprobados. Sí hubo un error de contenido (no
de token) al redactar: escribí el color Error `#991B1B` en vez del
Informativo `#6D28D9` para el texto "no aplica a formato cerrado" —
corregido antes de cerrar el archivo, ver 2.2.
