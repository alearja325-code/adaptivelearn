# Ventana 019 — Auth: Nueva contraseña

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Marco compartido:** hereda `17-spec-auth-login-registro.md`, sección
2.1 — mismo card centrado `480px`, mismo Fill/Radio/Stroke/Padding, no
se repite aquí.
**Se abre desde:** `18-spec-auth-verifica-correo.md` (Ventana 015),
flujo 2 (recuperación), tras verificar el código con éxito.
**Última pantalla del flujo de recuperación.** Al guardar, la contraseña
de la cuenta queda actualizada y la persona vuelve a
`17-spec-auth-login-registro.md`, variante Iniciar sesión, con un
mensaje de confirmación — ver 2.4.

---

## 1. Nombre

`019 — Auth / Nueva contraseña`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Título y descripción

Mismo componente de siempre (`17-spec-auth-login-registro.md`, sección
2.2) — Auto Layout Vertical, Alignment Center, Gap `4px`, texto
centrado:
- Título: "Crea una nueva contraseña" — `24px / 32px` (H2), peso `700`
  Bold, color `#111111`.
- Descripción: "Se usará la próxima vez que inicies sesión." — `16px /
  24px` (Body), peso `400` Regular, color `#555555`. Informa un hecho
  real, no solo instruye — 43 caracteres, cabe en una línea a `480px`.

### 2.2 Campo "Nueva contraseña"

Idéntico a `17-spec-auth-login-registro.md`, sección 2.4 — sin Label
separado, ícono candado a la izquierda, ícono ojo a la derecha:
- **Input**: alto `44px`, Radio `12px`, Fill `#FFFFFF`, Stroke `1px`
  `#E7E7E7`, Padding interno `16px` cada lado, Auto Layout Horizontal,
  Alignment Center, Gap `8px`. Ícono candado (izquierda) `16×16px`
  stroke `1.5px` color `#888888`. Placeholder "Nueva contraseña" —
  `16px / 22px` (Button/Input), Regular, color `#888888`, oculto con
  puntos una vez escrito. Ícono ojo (derecha, clickeable) `16×16px`
  stroke `1.5px` color `#888888`, alterna oculto/visible.
- **Foco**: Stroke `#111111`. *(Corrección 2026-09-11: se retira el
  estado de Error por formato inválido — ver la corrección de 2.3: una
  vez el botón exige la regla completa para habilitarse, no hay forma
  de llegar a un intento de guardar con formato inválido. Un estado
  visual que nunca puede ocurrir no se dibuja.)*
- **Texto de ayuda**, debajo del campo: "Mínimo 8 caracteres, con una
  mayúscula, una minúscula y un número." *(Corrección 2026-11-01: se
  agrega la minúscula, como en 17 §2.4.)* — `13px / 20px` (Caption), peso `400`
  Regular, color `#888888`. Mismo texto y mismo criterio que
  `17-spec-auth-login-registro.md`, sección 2.4. Esta es la misma regla
  que gatilla el botón en 2.3 — el texto de ayuda ya no es solo
  informativo, es la condición exacta que la persona está cumpliendo o
  no mientras escribe.
- **Un solo campo, sin "Confirmar contraseña"** — mismo criterio ya
  fijado en `17-spec-auth-login-registro.md`, sección 2.4: con el
  ícono de mostrar/ocultar disponible, pedir la contraseña dos veces es
  redundante.

### 2.3 Botón primario

*(Corrección 2026-09-11: la primera versión no tenía estado
Deshabilitado, copiando sin cuestionar el patrón de
`17-spec-auth-login-registro.md`. Acá hay un solo campo con una regla
de completitud exacta y ya visible en pantalla —el texto de ayuda de
2.2—, mismo caso que el botón de `21-spec-auth-recupera-contrasena.md`:
se corrige al mismo patrón Deshabilitado/Habilitado que ya usa el resto
del proyecto para esta situación.)*

Ancho Fill, alto `48px`, Radio `12px`, texto centrado `16px / 22px`
peso `500` Medium — "Guardar":
- **Deshabilitado** (la contraseña no cumple los 4 requisitos del texto
  de ayuda: mínimo 8 caracteres, una mayúscula, una minúscula, un número): Fill
  `#BDBDBD`, texto `#FFFFFF`.
- **Habilitado** (cumple los 4 requisitos): Fill `#111111`, texto
  `#FFFFFF`.

*(Sin mensaje de error de formato: sirve la misma regla exacta de
completitud para habilitar el botón, así que no existe un intento de
guardar con formato inválido que mostrar — un mensaje para un caso que
no puede ocurrir no se inventa, mismo criterio ya usado en
`20-spec-auth-elige-rol.md` para descartar un error sin causa propia.
La única falla posible acá, igual que en Elige tu rol, es de red o
servidor — genérica, no específica de esta pantalla.)*

### 2.4 Confirmación al volver a Iniciar sesión

Al guardar con éxito, la pantalla de destino
(`17-spec-auth-login-registro.md`, sección 2.6) muestra, en el mismo
lugar que su mensaje de error pero en
`#555555` (Secondary, no `#991B1B` — no es un error): "Contraseña
actualizada. Inicia sesión." *(Extensión deliberada de
`17-spec-auth-login-registro.md`, 2.6: ese mensaje estaba definido solo
para el caso de fallo; este es el primer caso de éxito que aparece en
la misma posición, y reutiliza el tamaño/posición pero no el color —
`#555555` porque no hay un color de "éxito" en la paleta y no se
inventa uno solo para este caso, mismo criterio ya documentado en
`03-tokens-diseno.md` sobre no usar verde=bien / rojo=mal.)*

## 3. Texto

- "Crea una nueva contraseña" (título).
- "Se usará la próxima vez que inicies sesión." (descripción).
- "Nueva contraseña" (placeholder del campo).
- "Mínimo 8 caracteres, con una mayúscula, una minúscula y un número." (ayuda —
  también la regla que habilita el botón, ver 2.2 y 2.3).
- "Guardar" (botón).
- "Contraseña actualizada. Inicia sesión." (confirmación, en la
  pantalla de Iniciar sesión).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Foco en el campo: Stroke cambia a `#111111`.
- Botón "Guardar": Deshabilitado → Habilitado apenas la contraseña
  escrita cumple los 4 requisitos — validación continua, mismo
  criterio que las 6 cajas de "Unirse con código", no espera a que el
  campo pierda el foco.
- Clic en el ícono de ojo: alterna el campo entre oculto y visible.
- Hover en botón primario (solo si Habilitado): opacidad `85%`.

## 7. Acciones

- Escribir en Nueva contraseña → el botón pasa a Habilitado en cuanto
  el texto cumple los 4 requisitos del texto de ayuda (validación
  continua, gatilla el botón) — no hay una validación de formato
  distinta esperando a que el campo pierda el foco, la regla es una
  sola y es la misma que ya se muestra en pantalla.
- Clic en el ícono de ojo → muestra/oculta la contraseña escrita.
- Clic en "Guardar" (solo si Habilitado) → actualiza la contraseña de
  la cuenta y vuelve a `17-spec-auth-login-registro.md`, variante
  Iniciar sesión, con el mensaje de confirmación de 2.4.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 22-spec-auth-nueva-contrasena.md
OK — 22-spec-auth-nueva-contrasena.md: todos los colores y valores en px están en tokens.json
```

Pasó limpio en la primera corrida — reutiliza el marco, el campo de
contraseña con su ícono de ojo, el botón primario y el criterio de
mensaje de error/confirmación de `17-spec-auth-login-registro.md`, sin
ningún ajuste. Sin necesitar agregar ningún valor nuevo a
`tokens.json`.
