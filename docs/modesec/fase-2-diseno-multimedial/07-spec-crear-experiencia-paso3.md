# Ventana 004 — Crear Experiencia: Paso 3 (Confirmar)

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Marco compartido:** hereda el modal de `05-spec-crear-experiencia-paso1.md`
(sección 2.1) — no se repite aquí. Ancho fijo `912px`. A diferencia del
Paso 2, este paso no necesita la lógica de alto máximo `852px` ni scroll
interno — el contenido es corto y cabe entero.

---

## 1. Nombre

`004 — Crear Experiencia / Paso 3 (Confirmar)`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Encabezado y stepper

Igual que los pasos anteriores (fila de encabezado + stepper) — círculo 1
y círculo 2 en estado Completado, círculo 3 en estado Activo.

### 2.2 Subencabezado del paso

Mismo componente que los pasos anteriores (título + descripción
apilados, centrados, gap `4px`):
- Título: "Confirmar" — `16px / 24px` peso `700` Bold, color `#111111`.
- Descripción: "Dale un nombre a la experiencia y revisa qué va a
  ocurrir." — `16px / 24px` peso `400` Regular, color `#555555`.

### 2.3 Campo — Nombre de la experiencia

Auto Layout Vertical, Gap `8px`:
- **Label**: "Nombre de la experiencia" — `13px / 20px` (Caption), peso
  `400` Regular, color `#555555` (Secondary — distinto del `#888888`
  Muted que usan los labels de los InfoBlocks, porque este es un campo
  que el docente debe leer y usar, no texto pasivo de referencia).
- **Input**: mismo patrón que el Search Input del Paso 2, sin ícono
  (es texto simple, no búsqueda). Alto `44px`, Radio `12px`, Fill
  `#FFFFFF`, Stroke `1px` `#E7E7E7`, padding interno `16px` cada lado.
  Texto `16px / 22px` (Button/Input), peso `500` Medium.
  - **Viene pre-llenado, no vacío**, con el **mismo enunciado truncado**
    que ya se calcula y se muestra en la fila colapsada de la Card de
    DBA (Paso 2, sección 2.4) — no se inventa una truncación ni una
    generación de título aparte, es el mismo texto que el docente ya
    vio un paso atrás. **No** se prellena con Área/Grado — esa
    metadata ya la aporta el Paso 1 y el Paso 2, repetirla aquí como
    "nombre" es redundante (corrección de Alejandro).
  - **Color mientras no se edita**: `#888888` (Muted) — mismo
    tratamiento que "sin elegir" en Search Input y Select — se lee como
    sugerencia, no como algo ya decidido.
  - **Al enfocar el campo**: se selecciona todo el texto
    automáticamente, para que el primer caracter que el docente teclee
    reemplace la sugerencia completa, sin tener que borrarla a mano.
  - **Al escribir algo** (así sea una sola tecla): el texto pasa a
    `#111111` (Primary Ink) — mismo criterio que "con un grado elegido"
    en el Select. Si el docente no toca nada, la sugerencia en Muted
    queda como el nombre real al crear — es texto real y válido, no un
    placeholder que desaparece vacío.

### 2.4 Card informativa — "Qué va a pasar"

**Encabezado de sección** (arriba de la card): "Qué va a pasar" —
`16px / 24px` peso `700` Bold, color `#111111`. Margen inferior `8px`
hasta la card.

**Card** — Radio `16px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`,
Padding `16px` (los 4 lados), Auto Layout Vertical, Gap `16px`. **Siempre
expandida** — sin radio de selección, sin badge, sin ícono de expandir;
a diferencia de la Card de DBA (Paso 2), esta no es seleccionable ni
colapsable, es puramente informativa.

3 InfoBlocks (mismo patrón que el Paso 2: Label `13px / 20px` Caption
peso `400` color `#888888`, Value `16px / 24px` Body peso `400` color
`#111111`, Gap `4px` Label→Value):

  **InfoBlock "¿Qué es?"**
  - Value: "Al crear esta experiencia, el sistema genera un banco de
    preguntas y ejercicios para cada evidencia del DBA que elegiste —
    usando como referencia el enunciado oficial del MEN, no contenido
    inventado sin anclar."

  **InfoBlock "¿Para qué sirve?"**
  - Value: "Te da, en un solo lugar, todo el material de diagnóstico de
    este DBA listo para revisar, antes de decidir si es adecuado para
    tu grupo."

  **InfoBlock "¿Cómo funciona?"**
  - Value: "Queda en estado Borrador. Puedes revisar y editar cada
    pregunta antes de publicarla — tus estudiantes no la ven hasta que
    tú decidas hacerlo."

*(Nota deliberada: no se reutilizó el texto equivalente del sistema
anterior — describía una escalera de profundidad de 3 niveles heredada
de SOLO, que ya se retiró — ADR-002 — y que además se intentó reflotar
con Bloom por error y también se corrigió — QA-015: "evidencias tienen
nivel fijo, no escalera". El texto de arriba se escribió desde cero,
consistente con lo que el sistema realmente hace hoy.)*

### 2.5 Fila de acciones (footer)

Auto Layout Horizontal, Gap `12px`, margen superior `24px`:
- **Botón "Volver"** (Ghost — sin Fill, sin Stroke, ancho Hug): alto
  `48px`, Padding izq/der `24px`, texto `16px / 22px` peso `500`
  Medium, color `#555555`. Sin fondo ni borde en la caja.
- **Botón "Crear experiencia"** (ancho Fill, ocupa el resto): alto
  `48px`, Radio `12px`, texto centrado `16px / 22px` peso `500` Medium.
  - **Habilitado** (por defecto — el nombre ya viene pre-llenado):
    Fill `#111111`, texto `#FFFFFF`.
  - **Deshabilitado** (si el docente borra el campo dejándolo vacío):
    Fill `#BDBDBD`, texto `#FFFFFF`. No clickeable.

## 3. Texto

- "Confirmar · Dale un nombre a la experiencia y revisa qué va a
  ocurrir." (subencabezado).
- "Nombre de la experiencia" (label del campo).
- Valor pre-llenado del campo: el mismo enunciado truncado del DBA
  elegido (Paso 2, sección 2.4) — no es un texto fijo, varía según el
  DBA.
- "Qué va a pasar" (encabezado de la card informativa).
- "¿Qué es?", "¿Para qué sirve?", "¿Cómo funciona?" (labels de los
  InfoBlocks — textos completos en 2.4).
- "Volver", "Crear experiencia" (botones).
- "Generando las preguntas..." (título del Modal: Cargando, ADR-027).
- "No se pudieron generar las preguntas. Intenta de nuevo." (error de
  generación).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Focus en el Input de nombre: Stroke cambia a `#111111`, se
  selecciona todo el texto pre-llenado (queda listo para reemplazarse
  con la primera tecla).
- Al escribir en el Input de nombre: el texto pasa de `#888888` Muted a
  `#111111` Primary Ink.
- Botón "Crear experiencia": Deshabilitado → Habilitado / Habilitado →
  Deshabilitado según el campo de nombre tenga o no texto.
- Hover en botones "Volver" y botón cerrar: Fill `#FAFAF8`.
- Sin animación en la card informativa — está siempre expandida, no
  tiene estado que transicionar.

## 7. Acciones

- Escribir en el campo Nombre → reemplaza el valor pre-llenado.
- Clic en "Volver" → regresa al Paso 2, conservando el DBA ya elegido.
- Clic en "Crear experiencia" (solo si el nombre no está vacío) → abre
  el Modal: Cargando (`24-spec-modal-cargando.md`, título "Generando
  las preguntas...") mientras se genera el banco (ADR-005). **Todo o
  nada (ADR-027):**
  - **Si termina bien** → se guardan juntos la experiencia (en estado
    Borrador) y su banco; se cierran los dos modales y el docente entra
    a la Vista Interna de la experiencia nueva.
  - **Si el servicio de IA principal falla**, el sistema reintenta con el
    de respaldo dentro de la misma espera, sin cambiar nada en pantalla
    (ADR-030).
  - **Si fallan los dos, o se agota el tiempo** → no se guarda nada. Se cierra el
    modal de carga y el Paso 3 sigue abierto, con el nombre y el DBA
    intactos, y un mensaje debajo del footer: "No se pudieron generar
    las preguntas. Intenta de nuevo." — `13px / 20px` (Caption), peso
    `400` Regular, color `#991B1B`, centrado. El mismo botón "Crear
    experiencia" sirve para reintentar; el mensaje desaparece al
    reintentar.
  *(Corrección 2026-10-21: antes decía "queda pendiente — generación
  bloqueante vs. en segundo plano". Se eligió esperar en pantalla; ver
  ADR-027 por qué evita agregar estados de generación al modelo.)*
- Clic en el botón cerrar (X, en el encabezado) → cierra el modal sin
  crear nada.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 07-spec-crear-experiencia-paso3.md
OK — 07-spec-crear-experiencia-paso3.md: todos los colores y valores en px están en tokens.json
```

Pasó limpio en la primera corrida — todo lo nuevo (label del campo,
input sin ícono, card informativa siempre expandida, encabezado de
sección) se construyó reutilizando tokens ya aprobados en los pasos
anteriores (`03-tokens-diseno.md`), sin necesitar agregar ninguno nuevo
a `tokens.json`.

**Corrección posterior (sin valores nuevos):** el prellenado original
del campo Nombre usaba `"[Área] · DBA [Grado]°"` — Alejandro señaló que
eso es redundante, esa metadata ya sale de los Pasos 1 y 2, pedirla de
nuevo como "nombre" no aporta nada. Se reemplazó por el enunciado
truncado del DBA (mismo texto que ya se ve en la Card de DBA del Paso
2), en color Muted mientras no se edita, con selección automática de
todo el texto al enfocar. Corrida final, limpia.
