# Ventana 016 — Auth: Completa tu perfil

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Marco compartido:** hereda `17-spec-auth-login-registro.md`, sección
2.1 — mismo card centrado `480px`, no se repite aquí.
**Se abre desde:** con correo+contraseña, después de
`18-spec-auth-verifica-correo.md` (código válido). Con Google/Microsoft,
directo después de `17-spec-auth-login-registro.md` — ese camino salta
la verificación (el proveedor ya la hizo).
**Sigue a:** "Elige tu rol" (Ventana 017, `20-spec-auth-elige-rol.md`) — no
a la plataforma directo. Esta pantalla no crea la cuenta por sí sola.

---

## 1. Nombre

`016 — Auth / Completa tu perfil`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Título y descripción

Mismo componente de siempre:
- Título: "Completa tu perfil" — `24px / 32px` (H2), peso `700` Bold,
  color `#111111`.
- Descripción: "Así te reconocen tu docente o tus estudiantes." —
  `16px / 24px` (Body), peso `400` Regular, color `#555555`. Informa la
  razón real de pedir nombre y apellido (identificación dentro de un
  salón real, no un dato decorativo) — cabe en una sola línea a `480px`
  (47 caracteres).

### 2.2 Selector de avatar

*(Corrección 2026-09-05: se descarta la insignia de cámara en la
esquina — exigía sacar una capa de Auto Layout y posicionarla a mano,
más complicado de lo necesario. Se reemplaza por un patrón mucho más
simple y ya conocido — Facebook, LinkedIn: pasar el cursor sobre la
foto la oscurece y muestra un ícono de cámara encima.)*

**Círculo "Avatar"**: `96×96px`, Radio `999px` (Full) — reutiliza un
valor ya existente en `espaciado_px`, no agrega nada nuevo. Más grande
que el avatar del Sidebar (`56px`) y que el de Tab Estudiantes
(`32px`): acá la foto es el elemento central de toda la pantalla, no un
detalle de esquina.
- **Sin foto elegida** (por defecto): Fill `#E7E7E7`, ícono de galería
  (imagen con flecha hacia arriba, "subir"), centrado, `32×32px` stroke
  `1.5px` color `#888888` — mismo tamaño que los íconos de Empty State
  (elemento visual principal, no un acompañante de texto). **No es el
  mismo ícono de silueta de persona que usa Tab Estudiantes** — a
  propósito: acá el círculo es un control activo de subida (invita a
  la acción), no una etiqueta pasiva como en un roster; mismo dato
  vacío, rol distinto.
- **Con foto**: la imagen llena el círculo completo, recorte automático
  centrado (sin herramienta de recorte manual — "simple pero
  trabajado", no un editor de imágenes).
- **Hover**: aparece encima una capa oscura semitransparente — mismo
  `96×96px`, mismo Radio `999px`, misma posición exacta que el círculo
  (sin desplazar nada, sin calcular esquinas), Fill `#111111` al `60%`
  de opacidad — con el ícono de cámara centrado encima, `24×24px`
  stroke `1.5px` color `#FFFFFF`. Desaparece al quitar el cursor.
- **Mensaje de error** (archivo inválido, condicional), debajo del
  círculo, centrado: `13px / 20px` Caption, color `#991B1B`: "Solo
  imágenes JPG o PNG, máximo 5 MB."

- **Opcional** — no bloquea el botón "Continuar" (ver 2.5). Si no se
  elige nada, la cuenta queda con el ícono por defecto — mismo
  mecanismo ya definido en Tab Estudiantes.
- **Pre-llenado con Google/Microsoft**: si la cuenta viene de login
  social y el proveedor entrega foto de perfil, el "Círculo" llega ya
  con esa foto — editable, no fija (la persona puede reemplazarla
  tocando el círculo igual que en el camino de correo+contraseña).

### 2.3 Campo "Nombres"

*(Corrección 2026-09-05: se retira el Label — reconsiderado. El riesgo
de ambigüedad que justificaba el Label antes era más teórico que real:
Nombres y Apellidos se llenan uno detrás del otro, en orden, así que al
escribir en el segundo, el primero ya está visible y lleno arriba.
Consistencia con Correo/Contraseña (sin Label) pesa más que ese riesgo
bajo. Placeholder plural "Nombres"/"Apellidos" — encaja con la
convención colombiana de registrar varios nombres y apellidos.)*

**Input**: alto `44px`, Radio `12px`, Fill `#FFFFFF`, Stroke `1px`
`#E7E7E7`, Padding interno `16px` cada lado, Auto Layout Horizontal,
Alignment Center, Gap `8px`. Ícono persona `16×16px` stroke `1.5px`
color `#888888`. El nombre del campo hace de placeholder — "Nombres" —
`16px / 22px` (Button/Input), Regular, color `#888888`.
- **Foco**: Stroke `#111111` — mismo criterio de siempre.
- **Pre-llenado con Google/Microsoft**: si el proveedor entrega nombre,
  el campo llega con ese valor, editable.

### 2.4 Campo "Apellidos"

Mismo patrón que 2.3, sin Label:
- **Input**: mismo tratamiento, ícono persona, placeholder "Apellidos".
- **Pre-llenado con Google/Microsoft**: igual que 2.3, con el apellido
  que entregue el proveedor.

### 2.5 Botón "Continuar"

Ancho Fill, alto `48px`, Radio `12px`, texto centrado `16px / 22px`
peso `500` Medium — mismo patrón Deshabilitado/Habilitado de siempre:
- **Deshabilitado** (falta Nombres o Apellidos): Fill `#BDBDBD`, texto
  `#FFFFFF`. El avatar no cuenta para esta condición — es opcional.
- **Habilitado** (Nombres y Apellidos con contenido): Fill `#111111`,
  texto `#FFFFFF`.

## 3. Texto

- "Completa tu perfil" (título).
- "Así te reconocen tu docente o tus estudiantes." (descripción).
- "Solo imágenes JPG o PNG, máximo 5 MB." (error de avatar).
- "Nombres" (placeholder del campo — sin Label separado, ver 2.3).
- "Apellidos" (placeholder del campo — sin Label separado, ver 2.4).
- "Continuar" (botón).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Foco en Nombres o Apellidos: Stroke cambia a `#111111`.
- Hover en el círculo de avatar: aparece la capa oscura con el ícono
  de cámara (ver 2.2), sin transición compleja — se prende y se apaga
  con el cursor.
- Botón "Continuar": Deshabilitado → Habilitado apenas Nombre y
  Apellido tienen contenido.
- Hover en botón "Continuar" (solo si Habilitado): opacidad `85%`.

## 7. Acciones

- Clic en el círculo de avatar → abre el selector de archivo nativo
  del sistema.
  - Archivo válido (JPG/PNG, ≤5MB) → reemplaza el contenido del
    círculo, recorte automático centrado.
  - Archivo inválido → muestra el error de 2.2, el avatar no cambia.
- Escribir en Nombres o Apellidos → habilita "Continuar" cuando ambos
  tienen contenido.
- Clic en "Continuar" (solo si Habilitado) → sigue a "Elige tu rol"
  (Ventana 017, `20-spec-auth-elige-rol.md`). No crea la cuenta todavía —
  falta el rol.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 19-spec-auth-completa-perfil.md
OK — 19-spec-auth-completa-perfil.md: todos los colores y valores en px están en tokens.json
```

Pasó limpio en la primera corrida — reutiliza el marco de `17-spec-auth-login-registro.md`, el ícono de Empty State (`32px`, ya aprobado), el patrón Deshabilitado/Habilitado de siempre, y `96px` ya existente en `espaciado_px` para el círculo de avatar. Sin necesitar agregar ningún valor nuevo a `tokens.json`.
