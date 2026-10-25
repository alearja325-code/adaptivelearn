# Ventana 024 — Modal: Cargando

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Componente genérico, reutilizable en cualquier modal del sistema que
espere una respuesta del servidor.** Se define acá porque
`23-spec-toma-diagnostico.md` es donde más veces se necesita (cada
`Respuesta` enviada), pero no le pertenece — cualquier acción futura que
hoy salta de Habilitado a su resultado sin transición (ej. "Unirse",
"Publicar experiencia", los botones de Auth) puede citar este documento
en vez de redefinirlo.
**Vacío real que esto cierra:** ninguno de los 19 specs anteriores tenía
definido qué se ve mientras se espera una respuesta del servidor —
`verificar_tokens.py` y una búsqueda de "cargando/loading/spinner" en
los 22 documentos existentes no encontraron ninguno.

---

## 1. Nombre

`024 — Modal: Cargando`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Marco del modal

Reutiliza el marco **chico**, el mismo de
`16-spec-modal-codigo-invitacion.md` (que a su vez reutiliza
`08-spec-unirse-codigo.md`, sección 2.1): ancho fijo `412px`, alto
ajustado al contenido (Hug), Radio `24px`, Fill `#FFFFFF`, Stroke `1px`
`#E7E7E7`, Padding `32px` (los 4 lados), Auto Layout Vertical,
Alignment Center, Gap `24px`.

**Sin botón cerrar — excepción documentada a la regla general.**
`08-spec-unirse-codigo.md` establece que "un modal siempre debe poder
cerrarse". Acá se rompe a propósito: cerrar este modal mientras una
acción está en curso (por ejemplo, a mitad de guardar una `Respuesta`)
es ambiguo —¿cancela la acción o solo la oculta mientras sigue
corriendo?— y las acciones que dispara este modal en esta versión son
casi instantáneas (sin carga real de producción), así que el costo de
no poder cerrarlo es bajo frente al riesgo de dejar una escritura a
medias. Si una versión futura tiene acciones más lentas, esta excepción
debe revisarse primero, no heredarse sin más.

### 2.2 Spinner

Ícono circular animado, `32×32px` (mismo tamaño que los íconos de
Estado por defecto de Vista Interna — el elemento visual principal acá,
no un acompañante de texto), stroke `2px`, color `#111111`. Gira sobre
su propio eje, sin dirección de lectura que aprenda nada nuevo —
únicamente comunica "esto sigue en curso".

*Se consideró un patrón más elaborado (barra de progreso, animación de
puntos) y se descartó: un spinner simple es el patrón más reconocido
para "espera corta e indeterminada" y no exige poder calcular ni
mostrar un porcentaje real de avance — mostrar un progreso falso sería
el mismo error que ya se evitó en el selector de certeza y en la
ausencia de contador de `23-spec-toma-diagnostico.md`.*

### 2.3 Título y descripción

Auto Layout Vertical, Alignment Center, Gap `4px`, texto centrado:
- Título: la acción en curso, en gerundio — ej. "Guardando tu
  respuesta...", "Uniéndote a la experiencia...". `20px / 28px` (H3),
  peso `500` Medium, color `#111111`. *(H3, no H2 — este modal no
  necesita el mismo peso visual que un título de decisión como
  "¿Publicar esta experiencia?"; es un estado transitorio, no un punto
  de decisión.)*
- Descripción (opcional, según el llamador): mensaje de estado breve —
  ej. "Esto toma solo un momento." `16px / 24px` (Body), peso `400`
  Regular, color `#555555`.

## 3. Texto

- Título: variable, provisto por quien invoca el modal (siempre en
  gerundio, describe la acción real en curso — nunca un genérico
  "Cargando" sin contexto, mismo criterio de honestidad del resto del
  proyecto).
- Descripción (opcional): "Esto toma solo un momento."

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Spinner: rotación continua mientras el modal está abierto.
- Aparece al iniciar la acción que lo invoca; se cierra solo — nunca
  por interacción del usuario — al recibir la respuesta del servidor,
  dando paso al siguiente estado (éxito, error, o la pantalla que
  corresponda).

## 7. Acciones

- Ninguna acción del usuario disponible dentro de este modal —
  intencional (ver 2.1). El único evento posible es el que dispara su
  cierre automático desde quien lo invoca.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 24-spec-modal-cargando.md
OK — 24-spec-modal-cargando.md: todos los colores y valores en px están en tokens.json
```

Ningún valor nuevo — reutiliza el marco de `412px` ya aprobado, el
ícono de `32px` ya reconocido para íconos de estado, y los colores
existentes.
