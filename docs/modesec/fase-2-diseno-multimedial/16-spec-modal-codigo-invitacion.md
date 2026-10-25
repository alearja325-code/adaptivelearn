# Ventana 013 — Modal: Código de invitación

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Se abre desde:** `14-spec-vista-interna-estudiantes.md`, sección 2.2
— botón "Código de invitación" (solo si `estado = Publicada`).
**Reutiliza:** el marco chico de `08-spec-unirse-codigo.md` — mismo
tamaño, misma fila de cajas de código. Es su contraparte de solo
lectura: esa pantalla es donde el estudiante *escribe* el código, esta
es donde el docente lo *muestra*. Sin QR — diferido, fuera de alcance
de esta versión (`08-spec-unirse-codigo.md` sigue siendo tecleo manual
de 6 casillas, no hay ruta por URL que un QR pudiera abrir hoy).

---

## 1. Nombre

`013 — Modal: Código de invitación`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Marco del modal

Mismo marco que `08-spec-unirse-codigo.md`, sección 2.1 — ancho **fijo
`412px`**, alto Hug, Radio `24px`, Fill `#FFFFFF`, Stroke `1px`
`#E7E7E7`, Padding `32px` (los 4 lados), Auto Layout Vertical,
Alignment Center, Gap `24px`.

**Botón cerrar** (`32×32px`, Radio `8px`, Fill transparente, ícono X
`16×16px` stroke `1.5px` color `#888888`, hover Fill `#FAFAF8`),
esquina superior derecha — igual al de Unirse con código. Este modal ya
nació centrado (mismo criterio unificado en toda la Fase II), no
necesita corrección.

### 2.2 Título y descripción

Auto Layout Vertical, Alignment Center, Gap `4px`, texto centrado:
- Título: "Código de invitación" — `24px / 32px` (H2), peso `700`
  Bold, color `#111111`.
- Descripción: "Comparte el código con tus estudiantes" — `16px / 24px`
  (Body), peso `400` Regular, color `#555555`. Cabe en una sola línea a
  `412px` de ancho (39 caracteres, contra los ~44 que ya caben en una
  línea en `08-spec-unirse-codigo.md`) — la versión anterior, más
  larga, envolvía a 2 líneas por el ancho fijo del modal.

### 2.3 Fila de cajas de código — solo lectura

Auto Layout Horizontal, Gap `12px`, Alignment Center. 6 cajas, una por
carácter — mismo tamaño y tipografía que `08-spec-unirse-codigo.md`,
sección 2.3, pero **sin** sus estados Foco/Error: acá no hay nada que
teclear ni que pueda fallar, es una etiqueta que muestra el
`Experiencia.codigo_invitacion` real, siempre completo.
- Cada caja: `48×48px`, Radio `12px`, Fill `#FFFFFF`, Stroke `1px`
  `#E7E7E7`. Un carácter centrado, `18px / 26px` (H4), peso `700` Bold,
  color `#111111`. Sin cursor, sin foco, no son campos — son texto
  dentro de una caja.

### 2.4 Botón "Copiar código"

Ancho Fill, alto `48px`, Radio `12px`, Fill `#111111`, texto centrado
`16px / 22px` peso `500` Medium, color `#FFFFFF`. Sin estado Disabled —
el código siempre está completo, no depende de ningún campo.

**Retroalimentación al copiar**: el texto cambia de "Copiar código" a
"¡Código copiado!" durante `2s`, después vuelve a "Copiar código" —
mismo vocabulario entre los dos estados, no un texto suelto aparte. Sin
esto, el docente hace clic y no tiene ninguna señal de que funcionó. No
es un componente nuevo: es el mismo botón cambiando su propio texto,
mismo criterio de simplicidad que el resto de animaciones de este
proyecto (sin toasts ni componentes nuevos para esto).

## 3. Texto

- "Código de invitación" (título).
- "Comparte el código con tus estudiantes" (descripción).
- "Copiar código" / "¡Código copiado!" (botón, con y sin
  retroalimentación).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Hover en botón cerrar: Fill `#FAFAF8`.
- Hover en botón "Copiar código": opacidad `85%`.
- Clic en "Copiar código": el texto del botón cambia a "¡Código
  copiado!" por `2s`, vuelve a "Copiar código" — ver 2.4.

## 7. Acciones

- Clic en "Copiar código" → copia `Experiencia.codigo_invitacion` al
  portapapeles. El modal **no se cierra** — el docente puede necesitar
  seguir mostrando el código en pantalla mientras lo dicta, la misma
  razón por la que este mecanismo es un modal y no un swap de texto en
  un botón (`pendientes.md`, A1).
- Clic en el botón cerrar (X) → cierra el modal, vuelve a Tab
  Estudiantes.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 16-spec-modal-codigo-invitacion.md
OK — 16-spec-modal-codigo-invitacion.md: todos los colores y valores en px están en tokens.json
```

Pasó limpio en la primera corrida — reutiliza el marco chico y la fila
de cajas de `08-spec-unirse-codigo.md` casi sin cambios (solo se quitan
los estados Foco/Error, no se agrega ningún valor), sin necesitar
agregar nada nuevo a `tokens.json`.
