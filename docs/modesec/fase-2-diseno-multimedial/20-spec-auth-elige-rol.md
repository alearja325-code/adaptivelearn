# Ventana 017 — Auth: Elige tu rol

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Marco compartido:** hereda `17-spec-auth-login-registro.md`, sección
2.1 — ancho **fijo** `480px`, no cambia entre pantallas de Auth. El
contenido de esta pantalla en particular (2 cards de `200px` + Gap
`16px` + Padding `32px` a cada lado = `480px`) llena ese fijo exacto,
sin sobrar ni faltar nada — no se fuerza ni se comprime nada para que
quepa.
**Se abre desde:** `19-spec-auth-completa-perfil.md`, botón "Continuar".
**Última pantalla de Auth.** Al confirmar, se crea la cuenta — en
`Docente` o en `Estudiante` (son 2 tablas separadas en el modelo, ver
`04-modelo-relacional.md`) — y se entra a la plataforma según el rol
elegido.
**Sin diseño anterior de referencia** — a diferencia del resto de
pantallas de Auth, esta se construye reutilizando un componente que ya
existe en el proyecto (Card de área), no una captura vieja.

---

## 1. Nombre

`017 — Auth / Elige tu rol`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Título y descripción

Mismo componente de siempre:
- Título: "Elige tu rol" — `24px / 32px` (H2), peso `700` Bold, color
  `#111111`.
- Descripción: "No podrás cambiarlo después." — `16px / 24px` (Body),
  peso `400` Regular, color `#555555`. Informa la consecuencia real de
  esta pantalla — `Docente` y `Estudiante` son 2 tablas separadas, no
  una casilla que se pueda cambiar más adelante — mismo criterio de
  honestidad ya usado en el modal "Publicar experiencia" (¿Se puede
  deshacer? No). 27 caracteres, cabe en una línea a `480px`.

### 2.2 Fila de cards de rol

Reutiliza tal cual la Card de área de
`05-spec-crear-experiencia-paso1.md`, sección 2.2 — **mismo tamaño
fijo, sin reinterpretarlo** (no Fill: acá no hay ningún sobrante de
espacio que llenar, los números ya cuadran exacto con el ancho fijo de
Auth):

Auto Layout Horizontal, Gap `16px`. 2 cards:
- Ancho fijo `200px`, alto fijo `112px`. Radio `16px`, Fill `#FFFFFF`,
  Stroke `1px` `#E7E7E7`. Auto Layout Vertical, Alignment Center,
  Padding `16px`, Gap `8px`.
  - **Default**: Ícono `24×24px`, stroke `2px`, color `#555555`. Label
    `16px / 24px`, peso `500` Medium, color `#555555`.
  - **Hover** (sin seleccionar): Fill `#FAFAF8`.
  - **Seleccionada** (persistente — se puede cambiar de elección
    libremente, "Continuar" avanza): Fill `#F5F3EE`, Stroke `2px`
    `#111111`. Ícono stroke sube a `2.5px`, color `#111111`. Label peso
    `700` Bold, color `#111111`.
- **"Soy Docente"** — ícono de presentación/pizarra.
- **"Soy Estudiante"** — ícono de libro.

### 2.3 Fila de acciones (footer)

Mismo patrón que el footer de
`06-spec-crear-experiencia-paso2.md`, sección 2.5:
- **Botón "Volver"** (Ghost — sin Fill, sin Stroke, ancho Hug): alto
  `48px`, Padding izq/der `24px`, texto `16px / 22px` peso `500`
  Medium, color `#555555`. Vuelve a "Completa tu perfil"
  (`19-spec-auth-completa-perfil.md`) sin perder lo ya escrito ahí
  (nombre, apellido, avatar quedan como estaban).
- **Botón "Continuar"** (ancho Fill, ocupa el resto): alto `48px`,
  Radio `12px`, texto centrado `16px / 22px` peso `500` Medium.
  - **Deshabilitado** (ninguna card seleccionada): Fill `#BDBDBD`,
    texto `#FFFFFF`.
  - **Habilitado** (una card seleccionada): Fill `#111111`, texto
    `#FFFFFF`.

*(Sin mensaje de error: la única falla posible acá es de red o servidor
— genérica, no específica de esta pantalla ni causada por algo que la
persona haya escrito, a diferencia de los errores sí definidos en
`17-spec-auth-login-registro.md`. No se inventa un caso que no tiene una
causa real y propia de esta pantalla.)*

## 3. Texto

- "Elige tu rol" (título).
- "No podrás cambiarlo después." (descripción).
- "Soy Docente" (card).
- "Soy Estudiante" (card).
- "Volver", "Continuar" (botones).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Hover en una card (sin seleccionar): Fill `#FAFAF8`.
- Clic en una card: pasa a Seleccionada — Fill `#F5F3EE`, Stroke
  `#111111`, ícono y label suben de peso. Si había otra seleccionada,
  esa vuelve a Default.
- Botón "Continuar": Deshabilitado → Habilitado apenas hay una card
  seleccionada.
- Hover en botón "Continuar" (solo si Habilitado): opacidad `85%`.

## 7. Acciones

- Clic en una card → la selecciona, deselecciona cualquier otra.
- Clic en "Volver" → vuelve a "Completa tu perfil", con nombre,
  apellido y avatar tal como quedaron.
- Clic en "Continuar" (solo si hay una card seleccionada) → crea la
  cuenta en `Docente` o `Estudiante` según la card elegida, con todos
  los datos ya reunidos en las pantallas anteriores de Auth. Entra a la
  plataforma — Dashboard según el rol.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 20-spec-auth-elige-rol.md
OK — 20-spec-auth-elige-rol.md: todos los colores y valores en px están en tokens.json
```

Pasó limpio en la primera corrida — reutiliza la Card de área del Paso 1 y el footer Volver/Continuar del Paso 2 de Crear Experiencia tal cual, sin ningún ajuste de tamaño. Sin necesitar agregar ningún valor nuevo a `tokens.json`.
