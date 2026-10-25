# Ventana 026 — Modal: Mi perfil

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Se abre desde:** el bloque de perfil del Sidebar —avatar, nombre y
correo, todo el bloque es el botón— (`04-spec-dashboard.md`, 2.2).
Reemplaza al antiguo ítem "Configuración", que llevaba a una pantalla
que nunca se diseñó. Docente y estudiante, mismo modal.
**Reutiliza:** `19-spec-auth-completa-perfil.md` casi completo (avatar,
Nombres, Apellidos) — idea de Alejandro. La diferencia es que acá los
datos ya existen: el modal **edita**, no crea.

**Fuera de alcance, a propósito:**
- **Rol** — no se cambia nunca (`20-spec-auth-elige-rol.md`: Docente y
  Estudiante son 2 tablas distintas).
- **Correo** — se muestra, pero no se edita en esta versión. Cambiarlo
  exige volver a verificarlo; se deja para una versión futura.
- **Contraseña** — no se cambia acá. Quien la quiera cambiar usa
  "¿Olvidaste tu contraseña?" (`21-spec`). Quien entró con
  Google/Microsoft no tiene contraseña en este sistema.
- **Quitar la foto** — se puede reemplazar, no quitar. La foto es
  opcional al crear la cuenta; una vez puesta, reemplazarla cubre el
  caso real.

---

## 1. Nombre

`026 — Modal: Mi perfil`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Marco del modal

Ancho fijo `480px` — el mismo de Auth (`17-spec-auth-login-registro.md`,
2.1), porque el contenido es el mismo de `19-spec`. Alto Hug, Radio
`24px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Padding `32px`, Auto
Layout Vertical, Alignment Center, Gap `24px`. Aparece sobre el
Dashboard (o la pantalla donde esté el usuario), centrado.

**Fila de encabezado** — patrón de 3 zonas de los modales
(`15-spec-modal-confirmar-publicar.md`, 2.1): caja invisible `32×32px`
a la izquierda, título "Mi perfil" al centro — `24px / 32px` (H2),
peso `700` Bold, color `#111111` —, botón cerrar real a la derecha
(`32×32px`, Radio `8px`, ícono X `16×16px` stroke `1.5px` color
`#888888`, hover Fill `#FAFAF8`). A diferencia de Auth, acá sí hay
botón cerrar: es un modal sobre la plataforma, no un paso obligatorio.

**Descripción**, debajo del encabezado, centrada: "Así te reconocen tu
docente o tus estudiantes." — misma frase de `19-spec`, `16px / 24px`
(Body), peso `400` Regular, color `#555555`.

### 2.2 Avatar

Mismo componente de `19-spec`, 2.2 — círculo `96×96px`, Radio `999px`,
hover con capa `#111111` al `60%` y cámara `24×24px` `#FFFFFF`, mismo
mensaje de error. Diferencia: llega con la foto actual de la cuenta, o
con el ícono de galería si nunca se puso una.

**Correo, solo lectura** — debajo del avatar, Gap `8px`, centrado:
el correo de la cuenta, `13px / 20px` (Caption), peso `400` Regular,
color `#888888` — mismo tratamiento que el correo del bloque de perfil
del Sidebar. No es un campo: no tiene borde ni foco.

### 2.3 Campos "Nombres" y "Apellidos"

Mismos inputs de `19-spec`, 2.3 y 2.4 (alto `44px`, Radio `12px`,
ícono persona `16×16px`, foco `#111111`), **llegan con los valores
actuales**, editables.

### 2.4 Botón "Guardar cambios"

Ancho Fill, alto `48px`, Radio `12px`, texto `16px / 22px` peso `500`
Medium, `#FFFFFF`:
- **Deshabilitado** (Fill `#BDBDBD`): si no se cambió nada respecto a
  lo guardado, o si Nombres o Apellidos quedaron vacíos. Guardar sin
  cambios no hace nada; habilitarlo sería un botón que no cumple
  función.
- **Habilitado** (Fill `#111111`): hay al menos un cambio y los 2
  campos tienen contenido.

## 3. Texto

- "Mi perfil" (título).
- "Así te reconocen tu docente o tus estudiantes." (descripción).
- El correo de la cuenta (solo lectura, variable).
- "Solo imágenes JPG o PNG, máximo 5 MB." (error de avatar).
- "Nombres", "Apellidos" (placeholders).
- "Guardar cambios" (botón).
- "Guardando tu perfil..." (título del Modal: Cargando).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Mismas de `19-spec` (foco, hover del avatar).
- "Guardar cambios": Deshabilitado ↔ Habilitado según haya cambios y
  campos llenos.
- Hover en botón cerrar: Fill `#FAFAF8`.

## 7. Acciones

- Clic en el avatar → selector de archivo, mismo comportamiento de
  `19-spec`.
- Clic en "Guardar cambios" (solo si Habilitado) → Modal: Cargando
  (`24-spec`, "Guardando tu perfil...") → guarda nombres, apellidos y
  foto → cierra el modal. El bloque de perfil del Sidebar se actualiza
  con los datos nuevos.
- Clic en el botón cerrar (X) → cierra sin guardar; lo cambiado se
  pierde.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 26-spec-modal-mi-perfil.md
OK — 26-spec-modal-mi-perfil.md: todos los colores y valores en px están en tokens.json
```

Sin valores nuevos: reutiliza el ancho `480px` de Auth, el encabezado de
3 zonas de los modales y todos los componentes de `19-spec`. **Modelo
de datos: sin cambios** — `nombre`, `apellido` y `avatar_url` ya existen
en Docente y Estudiante.
