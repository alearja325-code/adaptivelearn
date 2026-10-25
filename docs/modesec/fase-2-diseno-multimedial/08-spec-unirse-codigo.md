# Ventana 005 — Unirse con código

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Origen:** se abre desde el botón "→ Unirse con código" del Dashboard
del estudiante (`04-spec-dashboard.md`, Bloque 2). No comparte marco con
el modal de Crear Experiencia — es una ventana propia, sin pasos, con su
propio tamaño (QA-016: este mecanismo no se afecta ni se retira).

---

## 1. Nombre

`005 — Unirse con código`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Marco del modal

Ancho **fijo `412px`** (agregado a `anchos_layout_px`) — sale de sumar
6 cajas de código (`48px`) + 5 gaps (`12px`) + padding (`32px` × 2).
Alto: ajustado al contenido (Hug) — es corto, no necesita lógica de
máximo. Radio `24px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Padding
`32px` (los 4 lados), Auto Layout Vertical, Alignment Center, Gap
`24px`.

**Botón cerrar** (`32×32px`, Radio `8px`, Fill transparente, ícono X
`16×16px` stroke `1.5px` color `#888888`, hover Fill `#FAFAF8`),
esquina superior derecha — igual al de Crear Experiencia. *(Nota: la
imagen de referencia del sistema anterior no lo mostraba, se agrega
aquí por consistencia con el resto del sistema — un modal siempre debe
poder cerrarse sin tener que adivinar que se hace clic fuera.)*

### 2.2 Título y descripción

Auto Layout Vertical, Alignment Center, Gap `4px`, texto centrado:
- Título: "Unirse con código" — `24px / 32px` (H2), peso `700` Bold,
  color `#111111`.
- Descripción: "Ingresa el código que compartió tu docente." — `16px /
  24px` (Body), peso `400` Regular, color `#555555`.

### 2.3 Fila de cajas de código

Auto Layout Horizontal, Gap `12px`, Alignment Center. 6 cajas, una por
carácter:
- Cada caja: `48×48px` (cuadrada, reutiliza el alto `48` de control
  CTA también como ancho). Radio `12px`, Fill `#FFFFFF`, Stroke `1px`
  `#E7E7E7`. Un carácter centrado, `18px / 26px` (H4), peso `700` Bold,
  color `#111111`.
  - **Foco** (mientras se escribe en esa caja): Stroke `#111111` —
    mismo criterio que el campo Nombre del Paso 3.
  - **Error** (código inválido o experiencia no disponible, después de
    intentar enviar): Stroke `#991B1B` (Error) en las 6 cajas — el
    valor escrito **no se borra**, el estudiante puede corregirlo
    directo sin volver a teclear todo.
- Formato del código: 6 caracteres alfanuméricos, sin distinguir
  mayúsculas/minúsculas (se normaliza a mayúsculas al escribir). Al
  generarlo, el sistema excluye caracteres ambiguos (`0`/`O`, `1`/`I`/`L`)
  — el docente suele dictarlo o escribirlo en el tablero, evitar esa
  ambigüedad es una decisión práctica, no solo estética.

### 2.4 Mensaje de error (condicional)

Solo aparece después de un intento fallido. Texto centrado, `13px /
20px` (Caption), peso `400` Regular, color `#991B1B` (Error):
- Código que no corresponde a ninguna experiencia: "Este código no
  existe. Revisa que esté bien escrito."
- Código válido, pero la experiencia todavía está en Borrador (no
  publicada — Dashboard: "un estudiante nunca ve una Borrador"): "Esta
  experiencia todavía no está disponible. Pregúntale a tu docente."

### 2.5 Botón "Unirse"

Ancho Fill, alto `48px`, Radio `12px`, texto centrado `16px / 22px`
peso `500` Medium.
- **Deshabilitado** (menos de 6 caracteres escritos): Fill `#BDBDBD`,
  texto `#FFFFFF`. No clickeable.
- **Habilitado** (6 caracteres escritos, con o sin error previo): Fill
  `#111111`, texto `#FFFFFF`.

## 3. Texto

- "Unirse con código" (título).
- "Ingresa el código que compartió tu docente." (descripción).
- "Este código no existe. Revisa que esté bien escrito." (error —
  código inexistente).
- "Esta experiencia todavía no está disponible. Pregúntale a tu
  docente." (error — experiencia en Borrador).
- "Unirse" (botón).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Escribir un carácter en una caja → el foco avanza automáticamente a
  la siguiente caja.
- Backspace en una caja vacía → el foco retrocede a la caja anterior.
- Pegar un código de 6 caracteres en cualquier caja → llena las 6
  cajas de una vez, en orden.
- Foco en una caja: Stroke cambia a `#111111`.
- Intento fallido: las 6 cajas cambian su Stroke a `#991B1B` (Error) y
  aparece el mensaje correspondiente debajo; el valor escrito persiste.
- Botón "Unirse": Deshabilitado → Habilitado apenas las 6 cajas tienen
  contenido.
- Hover en botón cerrar: Fill `#FAFAF8`.

## 7. Acciones

- Escribir en las cajas → arma el código, carácter por carácter, con
  avance automático de foco.
- Clic en "Unirse" (solo si las 6 cajas están llenas) → valida el
  código:
  - Válido y la experiencia está Publicada → cierra el modal y entra a
    la vista de esa experiencia (docente o estudiante — según a quién
    pertenezca la sesión; para el estudiante, sea la primera vez que se
    une o ya estuviera unido, el resultado es el mismo: entra directo,
    sin distinguir el caso — para el estudiante, esa vista es la Ventana
    020, `23-spec-toma-diagnostico.md`; corrección 2026-10-21, antes
    decía "se especifica aparte").
  - Inválido, o válido pero la experiencia sigue en Borrador → muestra
    el error correspondiente (2.4), sin cerrar el modal.
- Clic en el botón cerrar (X) → cierra el modal sin unirse a nada.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 08-spec-unirse-codigo.md
OK — 08-spec-unirse-codigo.md: todos los colores y valores en px están en tokens.json
```

Pasó limpio en la primera corrida. Los dos valores nuevos de esta
ventana — el ancho fijo `412px` del modal y el color `#991B1B` Error —
se agregaron primero a `03-tokens-diseno.md` y `tokens.json` (con su
verificación de contraste, 8.31:1 sobre blanco, pasa AAA), antes de
escribir este spec — mismo orden que exige la nota de `tokens.json`
("no editar este archivo sin editar antes el .md"). El resto (cajas de
`48px`, gaps, radios, tipografía) reutiliza tokens ya aprobados en
ventanas anteriores.
