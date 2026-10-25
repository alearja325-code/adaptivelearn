# Ventana 015 — Auth: Verifica tu correo

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Marco compartido:** hereda `17-spec-auth-login-registro.md`, sección
2.1 — mismo card centrado `480px`, mismo Fill/Radio/Stroke/Padding, no
se repite aquí. Distinta de las pantallas de Vista Interna en algo
importante: no hay nada detrás (sigue sin haber sesión), así que
"compartir marco" acá significa mismo contenedor visual, no la misma
lógica de zona fija/zona con scroll — esta card es corta, cabe entera.
**Se abre desde:** 2 flujos distintos, con destino distinto al
verificar con éxito:
1. `17-spec-auth-login-registro.md`, variante Crear cuenta, tras un
   registro válido con correo+contraseña (no aplica si se registró con
   Google/Microsoft — ese correo ya viene verificado por el proveedor).
2. `21-spec-auth-recupera-contrasena.md` (Ventana 018) — mismo
   componente de 6 casillas, reutilizado, no una segunda pantalla
   aparte.

---

## 1. Nombre

`015 — Auth / Verifica tu correo`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Título y descripción

Mismo componente de siempre (Auto Layout Vertical, Alignment Center,
centrado), con un cambio: la descripción son **2 líneas fijas, no una
sola oración con el correo mezclado adentro** — *(decisión 2026-09-05:
si el correo fuera parte de una sola oración larga, la altura de esta
card cambiaría de forma impredecible según qué tan largo sea el correo
de cada persona; con 2 líneas separadas, la altura queda fija siempre
igual, sin importar el correo)*:
- Título: "Verifica tu correo" — `24px / 32px` (H2), peso `700` Bold,
  color `#111111`.
- Línea 1 (fija): "Enviamos un código de 6 dígitos a" — `16px / 24px`
  (Body), peso `400` Regular, color `#555555`.
- Línea 2 (dato real, no fijo): el correo de la cuenta — `16px / 24px`
  (Body), peso `700` Bold, color `#111111`, **truncado a una sola
  línea con elipsis** si excede el ancho disponible (mismo criterio de
  "Enunciado truncado" ya usado en el resto del proyecto) — con toda
  la card para él solo, casi ningún correo real llega a necesitarlo;
  si trunca, trunca solo esta línea, nunca la fija de arriba.
- Gap `4px` entre las 3 líneas, mismo criterio de siempre.

### 2.2 Fila de casillas de código

Mismo componente que `08-spec-unirse-codigo.md`, sección 2.3 — `48×48px`
por caja, Radio `12px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, carácter
centrado `18px / 26px` (H4) Bold `#111111`, Gap `12px`, Foco cambia
Stroke a `#111111` — **con una diferencia real, no solo de contexto**:
- **Solo dígitos (0-9), no alfanumérico.** El código de "Unirse con
  código" excluye caracteres ambiguos (`0/O`, `1/I/L`) porque un
  docente lo dicta en voz alta a 30 personas — acá no hay nadie
  dictando: el sistema lo genera y la misma persona que lo recibe por
  correo lo escribe. No aplica esa razón, y la propia referencia dice
  "código de 6 dígitos" — son solo números. Cualquier tecla que no sea
  un dígito, la caja la ignora.
- **Error** (código incorrecto, tras intentar verificar): Stroke
  `#991B1B` (Error) en las 6 cajas, el valor escrito no se borra —
  mismo criterio que "Unirse con código". Mensaje debajo, ver 2.4.

### 2.3 Botón "Verificar"

Ancho Fill, alto `48px`, Radio `12px`, texto centrado `16px / 22px`
peso `500` Medium — mismo patrón Deshabilitado/Habilitado que el botón
"Unirse" de `08-spec-unirse-codigo.md`:
- **Deshabilitado** (menos de 6 dígitos escritos): Fill `#BDBDBD`,
  texto `#FFFFFF`.
- **Habilitado** (6 dígitos escritos): Fill `#111111`, texto `#FFFFFF`.

### 2.4 Mensaje de error (condicional)

Solo aparece tras un intento fallido, encima del botón — mismo lugar y
tratamiento que el mensaje de error de
`17-spec-auth-login-registro.md`, sección 2.6: `13px / 20px` Caption,
color `#991B1B`, centrado:
- "Código incorrecto. Revisa que esté bien escrito."

### 2.5 Reenviar código

Auto Layout Horizontal, Alignment Center, Gap `8px` — mismo criterio de
"2 textos separados" ya usado en `17-spec-auth-login-registro.md`,
sección 2.9, con un componente nuevo: el enlace tiene una **cuenta
regresiva antes de poder usarse**, no existía ese caso todavía en el
proyecto:
- **Texto 1** — fijo, `13px / 20px` Caption, color `#555555`: "¿No
  recibiste el código?"
- **Texto 2** — el estado cambia con el tiempo:
  - **Contando** (`00:30` → `00:01`, apenas se entra a esta pantalla o
    tras pedir un reenvío): "Reenviar (00:29)" — el número baja cada
    segundo — color `#888888` (Muted), sin subrayado, no clickeable.
    Mismo criterio que cualquier estado inactivo del proyecto.
  - **Activo** (`00:00`): el texto cambia a solo "Reenviar" (sin
    número) — peso `700` Bold, color `#111111`, subrayado, clickeable
    — mismo tratamiento de enlace que el resto de Auth.

### 2.6 Enlace "Volver"

*(Corrección 2026-09-11: la primera versión decía "Volver a inicio de
sesión" con destino fijo a Login — error real, encontrado al revisar
esta pantalla junto con el flujo de recuperación. Esta pantalla se abre
desde 2 flujos distintos (ver "Se abre desde", arriba) y un destino fijo
solo tenía sentido para uno de los dos: alguien que viene de **Crear
cuenta** todavía no tiene nada que "reanudar" en Login, y encima el
link le hacía perder el correo y la contraseña ya escritos. Se corrige
a texto genérico, sin nombrar el destino — mismo criterio que el botón
"Volver" de `20-spec-auth-elige-rol.md`, sección 2.3: vuelve al paso
anterior exacto, sin perder lo ya escrito ahí. El camino a Login no se
pierde: sigue disponible un clic más allá, en el enlace "¿Ya tienes
cuenta? Inicia sesión" de `17-spec-auth-login-registro.md`, sección
2.9.)*

Centrado, `13px / 20px` Caption, peso `700` Bold, color `#111111`,
subrayado — un solo texto, no 2 (a diferencia de 2.5): es una sola
acción completa, no una afirmación más una acción aparte, mismo
criterio que "¿Olvidaste tu contraseña?" en
`17-spec-auth-login-registro.md`, sección 2.5. Texto fijo, "Volver" —
el destino real depende del flujo (ver 7. Acciones), pero el texto no
lo nombra a propósito: así no puede quedar mal si en el futuro esta
pantalla se reutiliza en un tercer flujo.

## 3. Texto

- "Verifica tu correo" (título).
- "Enviamos un código de 6 dígitos a" (descripción, línea fija).
- Correo de la cuenta (descripción, línea 2, dato real).
- "Código incorrecto. Revisa que esté bien escrito." (error).
- "Verificar" (botón).
- "¿No recibiste el código?" (texto fijo, 2.5).
- "Reenviar (00:29)" (contando, cuenta baja cada segundo) / "Reenviar"
  (activo, sin número) (2.5).
- "Volver" (enlace — destino contextual, ver 2.6 y 7).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Escribir un dígito en una caja → el foco avanza automáticamente a la
  siguiente, mismo criterio que "Unirse con código".
- Backspace en una caja vacía → el foco retrocede a la anterior.
- Pegar un código de 6 dígitos en cualquier caja → llena las 6 de una
  vez, en orden.
- Intento fallido: las 6 cajas cambian su Stroke a `#991B1B`, aparece
  el mensaje de 2.4, el valor escrito persiste.
- Botón "Verificar": Deshabilitado → Habilitado apenas las 6 cajas
  tienen contenido.
- "Reenviar" (2.5): cada segundo, el número baja en 1 mientras cuenta;
  al llegar a `00:00`, cambia de golpe al estado Activo (Bold,
  subrayado, sin número).
- Hover en botón "Verificar" (solo si Habilitado): opacidad `85%`.

## 7. Acciones

- Escribir en las cajas → arma el código, dígito por dígito, con avance
  automático de foco. Solo acepta dígitos.
- Clic en "Verificar" (solo si las 6 cajas están llenas) → valida el
  código:
  - Válido → según de dónde vino esta pantalla (ver "Se abre desde",
    arriba): si fue de Crear cuenta, sigue a
    `19-spec-auth-completa-perfil.md` (Ventana 016); si fue de
    recuperar contraseña, sigue a
    `22-spec-auth-nueva-contrasena.md` (Ventana 019).
  - Inválido → error de 2.4, sin cerrar ni limpiar las cajas.
- Clic en "Reenviar" (solo en estado Activo, 2.5) → reenvía el código
  al mismo correo, reinicia la cuenta regresiva a `00:30`.
- Clic en "Volver" (2.6) → destino según de dónde vino esta pantalla
  (ver "Se abre desde", arriba), no un destino fijo:
  - Si fue de Crear cuenta → vuelve a
    `17-spec-auth-login-registro.md`, variante Crear cuenta, con el
    correo y la contraseña ya escritos tal como quedaron.
  - Si fue de recuperar contraseña → vuelve a
    `21-spec-auth-recupera-contrasena.md` (Ventana 018), con el correo
    ya escrito tal como quedó.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 18-spec-auth-verifica-correo.md
OK — 18-spec-auth-verifica-correo.md: todos los colores y valores en px están en tokens.json
```

Pasó limpio en la primera corrida — reutiliza el marco de `17-spec-auth-login-registro.md`, las cajas de código y el patrón Deshabilitado/Habilitado de `08-spec-unirse-codigo.md`, y el criterio de enlaces ya establecido en esta misma pantalla de Auth. Sin necesitar agregar ningún valor nuevo a `tokens.json`.
