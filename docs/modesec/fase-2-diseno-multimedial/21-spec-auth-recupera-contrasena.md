# Ventana 018 — Auth: Recupera tu contraseña

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Marco compartido:** hereda `17-spec-auth-login-registro.md`, sección
2.1 — mismo card centrado `480px`, mismo Fill/Radio/Stroke/Padding, no
se repite aquí.
**Se abre desde:** `17-spec-auth-login-registro.md`, variante Iniciar
sesión, sección 2.5, enlace "¿Olvidaste tu contraseña?".
**Lleva a:** `18-spec-auth-verifica-correo.md` (Ventana 015), flujo 2 —
mismo componente de 6 casillas que usa Crear cuenta, reutilizado, no una
pantalla de verificación aparte.
**Decisión de seguridad — sin "correo no encontrado":** al hacer clic en
"Enviar código", la pantalla avanza siempre al mismo paso, exista o no
una cuenta con ese correo. Confirmarle a un desconocido si un correo
está o no registrado es una fuga de información real (enumeración de
cuentas) — mismo criterio ya aplicado en el error de
`17-spec-auth-login-registro.md`, sección 2.6 ("Correo o contraseña
incorrectos.", deliberadamente genérico, sin decir cuál de los dos
falló). La única validación que sí se hace acá es de **formato**
(¿parece un correo?), no de **existencia** (¿existe esa cuenta?) — esas
son dos preguntas distintas, y solo la primera es segura de responder.

---

## 1. Nombre

`018 — Auth / Recupera tu contraseña`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Título y descripción

Mismo componente de siempre (`17-spec-auth-login-registro.md`, sección
2.2) — Auto Layout Vertical, Alignment Center, Gap `4px`, texto
centrado:
- Título: "¿Olvidaste tu contraseña?" — `24px / 32px` (H2), peso `700`
  Bold, color `#111111`.
- Descripción: "Te enviaremos un código a tu correo." — `16px / 24px`
  (Body), peso `400` Regular, color `#555555`. Informa lo que va a
  pasar, sin prometer que la cuenta existe — 36 caracteres, cabe en una
  línea a `480px`.

### 2.2 Campo "Correo electrónico"

Idéntico a `17-spec-auth-login-registro.md`, sección 2.3 — sin Label
separado, ícono sobre a la izquierda, el propio placeholder identifica
el campo:
- **Input**: alto `44px`, Radio `12px`, Fill `#FFFFFF`, Stroke `1px`
  `#E7E7E7`, Padding interno `16px` cada lado, Auto Layout Horizontal,
  Alignment Center, Gap `8px`. Ícono sobre (envelope) `16×16px` stroke
  `1.5px` color `#888888`. Placeholder "Correo electrónico" — `16px /
  22px` (Button/Input), Regular, color `#888888`.
- **Foco**: Stroke `#111111`.
- **Error** (formato inválido, tras intentar enviar): Stroke `#991B1B`
  (Error). Mensaje debajo, ver 2.4. **No existe un estado de error para
  "correo no encontrado"** — ver nota de seguridad al inicio de este
  documento.

### 2.3 Botón primario

*(Corrección 2026-09-11: la primera versión de este documento no tenía
estado Deshabilitado, copiando sin cuestionar el patrón del botón de
`17-spec-auth-login-registro.md`. Con un solo campo y una sola
condición de completitud verificable en el cliente —¿el correo tiene
formato válido?—, el patrón correcto es el que ya usa el resto del
proyecto para ese mismo caso: "Unirse con código", "Verificar" código
y "Continuar" de Elige tu rol. Se corrige acá.)*

Ancho Fill, alto `48px`, Radio `12px`, texto centrado `16px / 22px`
peso `500` Medium — "Enviar código" (verbo específico, dice qué pasa
realmente al hacer clic, mismo criterio que "Iniciar sesión"/"Crear
cuenta"/"Verificar" — no "Continuar", reservado para pasos donde no
hay una sola acción nombrable):
- **Deshabilitado** (el campo está vacío o no tiene formato de correo
  válido): Fill `#BDBDBD`, texto `#FFFFFF`.
- **Habilitado** (formato de correo válido): Fill `#111111`, texto
  `#FFFFFF`.

### 2.4 Mensaje de error (condicional)

Solo aparece si el correo no tiene formato válido, encima del botón —
mismo lugar y tratamiento que
`17-spec-auth-login-registro.md`, sección 2.6: `13px / 20px` Caption,
color `#991B1B`, centrado:
- "Escribe un correo válido."

### 2.5 Enlace "Volver a inicio de sesión"

Centrado, `13px / 20px` Caption, peso `700` Bold, color `#111111`,
subrayado — un solo texto, no 2, mismo criterio y mismo componente que
`18-spec-auth-verifica-correo.md`, sección 2.6.

## 3. Texto

- "¿Olvidaste tu contraseña?" (título).
- "Te enviaremos un código a tu correo." (descripción).
- "Correo electrónico" (placeholder del campo).
- "Escribe un correo válido." (error, formato).
- "Enviar código" (botón).
- "Volver a inicio de sesión" (enlace).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Foco en el campo: Stroke cambia a `#111111`.
- Botón "Enviar código": Deshabilitado → Habilitado apenas el texto
  escrito tiene forma de correo — validación continua, mismo criterio
  que las 6 cajas de "Unirse con código", no espera a que el campo
  pierda el foco.
- Formato inválido tras intentar enviar: el mensaje de error aparece
  encima del botón, sin recargar la página.
- Hover en botón primario (solo si Habilitado): opacidad `85%`.

## 7. Acciones

- Escribir en Correo → el botón pasa a Habilitado en cuanto el texto
  tiene forma de correo válida (validación continua, gatilla el
  botón). El Stroke de error rojo es una validación distinta y sigue
  esperando a que el campo pierda el foco o se intente enviar, mismo
  criterio que `17-spec-auth-login-registro.md` — son dos
  comprobaciones separadas, una habilita el botón, la otra muestra el
  error visual.
- Clic en "Enviar código" (solo si Habilitado) → **siempre** avanza a
  "Verifica tu correo" (`18-spec-auth-verifica-correo.md`, Ventana 015,
  flujo 2), exista o no una cuenta con ese correo — ver nota de
  seguridad al inicio de este documento.
- Clic en "Volver a inicio de sesión" → vuelve a
  `17-spec-auth-login-registro.md`, variante Iniciar sesión.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 21-spec-auth-recupera-contrasena.md
OK — 21-spec-auth-recupera-contrasena.md: todos los colores y valores en px están en tokens.json
```

Pasó limpio en la primera corrida — reutiliza el marco, el campo de
correo, el botón primario y el criterio de mensaje de error de
`17-spec-auth-login-registro.md`, y el enlace de
`18-spec-auth-verifica-correo.md`, sin ningún ajuste. Sin necesitar
agregar ningún valor nuevo a `tokens.json`.
