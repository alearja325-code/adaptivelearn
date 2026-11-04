# Ventana 014 — Auth: Iniciar sesión / Crear cuenta

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Origen:** primera pantalla que ve cualquiera que llegue a la
plataforma sin sesión — no se abre "desde" otra pantalla, es la puerta
de entrada. Sin código ni enlace de por medio (`ADR-025` no cambia
esto; QR/enlace de invitación quedaron fuera de alcance, `pendientes.md`
A2).
**Referencia:** estructura tomada de un diseño anterior de Alejandro
(2 capturas, Login y Registro) — mismo criterio que toda referencia
vieja usada en este proyecto: se reconstruye con nuestros tokens, no se
copia el estilo visual (fondo degradado, texto con gradiente de color,
botones azul/morado — nada de eso se conserva).
**Decisiones tomadas antes de este spec** (`pendientes.md`, A9):
correo+contraseña **y** login social (Google, Microsoft — **sin
Apple**: exige cuenta de desarrollador de pago, USD 99/año, y esta
plataforma es web, no aplica la obligación de la App Store de tenerlo).
Sin checkbox de términos y condiciones — no existe ese documento
todavía, y fingir que sí sería peor que no tenerlo. El rol
(Docente/Estudiante) no se pregunta acá — es un paso propio, al final
de toda la secuencia (Ventana 017, `20-spec-auth-elige-rol.md`).

---

## 1. Nombre

`014 — Auth / Iniciar sesión y Crear cuenta`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Marco de la página

No es un modal — no hay ninguna pantalla detrás de esta (nadie tiene
sesión todavía). Frame completo `1440×900`, Fill `#F7F6F3` (mismo
Canvas del resto del proyecto), Auto Layout Vertical, Alignment Center,
Justify Center — la card queda centrada en el frame completo, no en una
esquina ni pegada arriba.

**Card**: ancho fijo `480px` — valor nuevo, agregado a
`anchos_layout_px` *(corrección 2026-09-05: no reutiliza el `412px` de
"Unirse con código" — ese ancho salió de sumar 6 cajas de tamaño fijo,
acá no hay ningún elemento de tamaño fijo, todo es texto que fluye. El
alto sí lo definen sus elementos, Gap y Padding, de forma natural
—Hug—; el ancho lo decidimos nosotros según lo que el contenido
necesita para verse cómodo, no según lo que ya exista en otro lado. A
`412px` un formulario con esta cantidad de líneas se sentía apretado;
`480px` da más aire a un correo largo o a un mensaje de error sin que
la card deje de leerse como una sola columna enfocada.)*. Alto Hug.
Radio `24px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Padding `32px`
(los 4 lados), Auto Layout Vertical, Alignment Center, Gap `24px`.

### 2.2 Título y descripción

Mismo componente que `08-spec-unirse-codigo.md`, sección 2.2 — Auto
Layout Vertical, Alignment Center, Gap `4px`, texto centrado:
- Título: `24px / 32px` (H2), peso `700` Bold, color `#111111`.
- Descripción: `16px / 24px` (Body), peso `400` Regular, color
  `#555555`.

Por variante *(corrección 2026-09-05: las descripciones originales
—"Continúa tu experiencia.", "Empieza con una experiencia
adaptativa."— no decían nada real, puro relleno de ánimo copiado de la
referencia sin pasarlo por el mismo filtro que el resto del proyecto:
"dice qué es esto en el modelo, no solo instruye". Se corrigen acá)*:
- **Iniciar sesión**: "Bienvenido de vuelta" / "Usa el correo con el
  que te registraste." — informa un hecho real (depende de lo que ya
  elegiste al crear la cuenta), cabe en una línea a `480px` (41
  caracteres).
- **Crear cuenta**: "Crea tu cuenta" / "Para unirte o crear
  experiencias." — informa la razón real de tener cuenta (unirte como
  estudiante, crear como docente), sin nombrar el rol todavía —
  34 caracteres.

### 2.3 Campo "Correo electrónico"

*(Corrección 2026-09-05: se retira el Label separado — con solo 2
campos, tan reconocibles como correo y contraseña, el ícono + el texto
dentro del campo ya identifican qué es cada uno; un Label aparte no
suma nada. El único riesgo real de este patrón —que el texto
identificador desaparece una vez que se escribe— casi no aplica en un
formulario de 2 campos tan estándar: nadie olvida cuál es cuál a mitad
de un login.)*

**Input**: alto `44px`, Radio `12px`, Fill `#FFFFFF`, Stroke `1px`
`#E7E7E7`, Padding interno `16px` cada lado, Auto Layout Horizontal,
Alignment Center, Gap `8px`. Ícono sobre (envelope) `16×16px` stroke
`1.5px` color `#888888`, primero en el layout. El propio nombre del
campo hace de placeholder — "Correo electrónico" — `16px / 22px`
(Button/Input), Regular, color `#888888`.
- **Foco**: Stroke `#111111` — mismo criterio que todos los demás
  campos de texto ya definidos en el proyecto.
- **Error** (formato inválido, tras intentar enviar): Stroke
  `#991B1B` (Error). Mensaje general, ver 2.6.

### 2.4 Campo "Contraseña"

Mismo patrón que 2.3, sin Label, con un ícono adicional a la derecha:
- **Input**: mismo tamaño/Fill/Stroke que 2.3, Auto Layout Horizontal,
  Alignment Center, Gap `8px`. **Ícono candado** (izquierda, primero en
  el layout, mismo lugar que el sobre en 2.3): `16×16px` stroke
  `1.5px` color `#888888`. El nombre del campo hace de placeholder —
  "Contraseña", mismo tratamiento que 2.3 — hasta que el usuario
  empieza a escribir, momento en que se reemplaza por el texto real,
  oculto con puntos. **Ícono ojo** (derecha, clickeable, empujado al
  borde por el Fill del campo entre los dos íconos): `16×16px` stroke
  `1.5px` color `#888888` — alterna entre "ojo" (oculto) y "ojo
  tachado" (visible). Mismo criterio de Foco/Error que 2.3.
- **Solo en Crear cuenta** — texto de ayuda debajo del campo:
  "Mínimo 8 caracteres, con una mayúscula, una minúscula y un número."
  *(Corrección 2026-11-01: se agrega la minúscula, que pide la actividad
  del módulo de autenticación de DSE-2; ver RF-01-01.)* — `13px /
  20px` (Caption), peso `400` Regular, color `#888888`. Responde al
  vacío real que tenía la referencia: sin esto, el error de contraseña
  débil solo se descubre después de enviar el formulario.
  - **Sin campo de "Confirmar contraseña"** — decisión correcta de la
    referencia, no un vacío: con el ícono de mostrar/ocultar ya
    disponible, pedir la contraseña dos veces es redundante (el
    usuario puede verificarla tocando el ojo).

### 2.5 Enlace "¿Olvidaste tu contraseña?" — solo en Iniciar sesión

Alineado a la derecha, alto de la fila, encima del botón primario:
`13px / 20px` (Caption), peso `700` Bold, color `#111111`, con
subrayado. *(Nota de sistema — primer enlace de texto de todo el
proyecto: no existe un color de "link" en la paleta, y no se agrega
uno nuevo solo para esto. Se distingue por el subrayado, no por color,
consistente con un sistema que hasta ahora es monocromo salvo los
colores de estado — ver el mismo criterio en 2.9.)*

### 2.6 Botón primario

Ancho Fill, alto `48px`, Radio `12px`, Fill `#111111`, texto centrado
`16px / 22px` peso `500` Medium, color `#FFFFFF` — mismo estilo CTA de
siempre.
- **Iniciar sesión**: "Iniciar sesión".
- **Crear cuenta**: "Crear cuenta".

**Mensaje de error general** (condicional, aparece encima del botón si
falla): `13px / 20px` Caption, color `#991B1B`, **alineado a la izquierda**,
como los campos y el texto de ayuda de la contraseña *(corrección
2026-11-04, Alejandro: antes, centrado)*:
- Iniciar sesión, credenciales incorrectas: "Correo o contraseña
  incorrectos." — deliberadamente genérico: no dice cuál de los dos
  falló, práctica estándar para no confirmarle a un desconocido que un
  correo existe en el sistema.
- Crear cuenta, correo ya registrado con correo+contraseña: "Ya existe
  una cuenta con este correo. Inicia sesión." — **un solo texto, sin
  enlace** (a propósito, no un descuido: invita a usar el enlace del
  footer, 2.9, que ya hace ese trabajo — no hace falta un segundo
  camino al mismo lugar dentro del propio mensaje de error).
- Crear cuenta o Iniciar sesión, correo registrado con un método
  social: "Esta cuenta usa Google (o Microsoft) para entrar. Continúa
  con ese botón." — resuelve la decisión ya tomada en `pendientes.md`
  (A9): no se vinculan métodos, se avisa cuál usar. Mismo criterio: un
  solo texto, sin enlace propio.

**Mensaje de confirmación** (condicional, solo variante Iniciar sesión,
al llegar desde "Nueva contraseña" con éxito): mismo lugar, tamaño y
alineación que los mensajes de arriba, pero en `#555555` (Secondary) — no es un error:
"Contraseña actualizada. Inicia sesión." Ver
`22-spec-auth-nueva-contrasena.md`, sección 2.4, para el criterio
completo de por qué no usa un color de "éxito" — no existe uno en la
paleta, y no se inventa uno solo para este caso.

### 2.7 Divisor "o"

Auto Layout Horizontal, Alignment Center, Gap `12px`:
- Línea `1px` `#E7E7E7`, ancho Fill.
- Texto "o" — `13px / 20px` Caption, color `#888888`.
- Línea `1px` `#E7E7E7`, ancho Fill.

### 2.8 Botones de login social

*(Corrección 2026-09-05: vuelve a la fila horizontal, solo ícono, tal
cual la referencia — se descarta la versión apilada con texto de la
corrida anterior.)* Auto Layout Horizontal, Gap `12px`, cada botón
ancho Fill (se reparten el espacio en 2 partes iguales — mismo
criterio ya usado en la Fila de cards de material,
`11-spec-vista-interna-materiales.md` sección 2.2).

Cada botón: alto `48px`, Radio `12px`, Fill `#FFFFFF`, Stroke `1px`
`#E7E7E7`, Auto Layout, Alignment Center, Justify Center (el ícono
centrado, sin nada más en el botón):
- Logo oficial de cada proveedor, `20×20px` — colores de marca
  oficiales, sin modificar (no son íconos de este sistema, son marcas
  de terceros con su propia guía de marca): Google, Microsoft.
- Hover: Fill `#FAFAF8` — mismo criterio que el resto de botones
  secundarios del proyecto.
- Sin texto — mismo criterio de la referencia original.

*(Sin Apple — ver nota de alcance al inicio de este documento.)*

### 2.9 Enlace de cambio de variante

Auto Layout Horizontal, Alignment Center, **Gap `8px`** — 2 elementos
de texto separados, no un solo texto con pesos mezclados (mismo
criterio que la leyenda de Reporte, `13-spec-modal-reporte.md`, sección
2.3 — mismo valor de Gap reutilizado, no uno nuevo):
- **Texto 1** — fijo, `13px / 20px` Caption, peso `400` Regular, color
  `#555555`: "¿No tienes cuenta?" (en Iniciar sesión) / "¿Ya tienes
  cuenta?" (en Crear cuenta).
- **Texto 2** — el enlace en sí, mismo tamaño, peso `700` Bold, color
  `#111111`, subrayado — mismo criterio de 2.5: "Regístrate gratis" /
  "Inicia sesión".

## 3. Texto

- "Bienvenido de vuelta" / "Usa el correo con el que te registraste."
  (título + descripción, Iniciar sesión).
- "Crea tu cuenta" / "Para unirte o crear experiencias." (título +
  descripción, Crear cuenta).
- "Correo electrónico" (placeholder del campo — sin Label separado, ver
  2.3).
- "Contraseña" (placeholder del campo — sin Label separado, ver 2.4).
- "Mínimo 8 caracteres, con una mayúscula, una minúscula y un número." (ayuda, solo
  Crear cuenta).
- "¿Olvidaste tu contraseña?" (enlace, solo Iniciar sesión).
- "Correo o contraseña incorrectos." (error, Iniciar sesión).
- "Ya existe una cuenta con este correo. Inicia sesión." (error, Crear
  cuenta).
- "Esta cuenta usa Google (o Microsoft) para entrar. Continúa con ese
  botón." (error, correo registrado con otro método).
- "Iniciar sesión" / "Crear cuenta" (botón primario, por variante).
- "o" (divisor).
- Sin texto propio — los botones sociales (2.8) son solo el logo de
  cada proveedor, sin ningún texto.
- "¿No tienes cuenta? Regístrate gratis" / "¿Ya tienes cuenta? Inicia
  sesión" (enlace de cambio de variante).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Foco en un campo: Stroke cambia a `#111111`.
- Clic en el ícono de ojo: alterna el campo Contraseña entre oculto y
  visible, el ícono cambia entre sus 2 estados.
- Intento fallido (cualquier caso de 2.6): el mensaje de error aparece
  encima del botón primario, sin recargar la página.
- Hover en botón primario: opacidad `85%`.
- Hover en botones sociales: Fill `#FAFAF8`.

## 7. Acciones

- Escribir en Correo o Contraseña → valida formato en el momento en
  que el campo pierde el foco, no mientras se escribe (evita marcar
  error a medio teclear).
- Clic en el ícono de ojo → muestra/oculta la contraseña escrita.
- Clic en "¿Olvidaste tu contraseña?" (Iniciar sesión) → lleva a
  "Recupera tu contraseña" (`21-spec-auth-recupera-contrasena.md`,
  Ventana 018).
- Clic en el botón de Google o de Microsoft (2.8) → abre el flujo de
  autenticación de ese proveedor. Si tiene éxito y es una cuenta nueva,
  el correo llega ya verificado por el proveedor — salta la pantalla
  "Verifica tu correo" (Ventana 015) y continúa directo en "Completa tu
  perfil" (Ventana 016).
- Clic en el botón primario:
  - **Iniciar sesión**, válido → entra a la plataforma, según el rol
    ya guardado de esa cuenta.
  - **Iniciar sesión**, inválido → error "Correo o contraseña
    incorrectos.", los campos no se limpian.
  - **Crear cuenta**, correo nuevo y contraseña válida → sigue a
    "Verifica tu correo" (Ventana 015).
  - **Crear cuenta**, correo ya registrado (mismo método) → error
    correspondiente de 2.6, con enlace a Iniciar sesión.
  - **Cualquiera**, correo registrado con un método distinto → error
    correspondiente de 2.6, sin crear cuenta nueva ni vincular nada.
- Clic en el enlace de cambio de variante (2.9) → cambia entre Iniciar
  sesión y Crear cuenta, sin perder lo ya escrito en Correo si el
  campo es el mismo.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 17-spec-auth-login-registro.md
OK — 17-spec-auth-login-registro.md: todos los colores y valores en px están en tokens.json
```

Pasó limpio, tras la corrección de ancho — reutiliza componentes ya aprobados (Título+descripción de "Unirse con código", campo de texto del Paso 3, botón primario y hover de siempre), salvo por un valor nuevo, agregado deliberadamente: `480px` de ancho de card, documentado en `tokens.json` con su razón (no es una suma de elementos fijos como el `412px` de "Unirse con código" — es una decisión de proporción, para un formulario de puro texto que fluye). Los logos de Google/Microsoft no llevan valores hex propios en este documento — son marcas de terceros, no colores de nuestra paleta.
