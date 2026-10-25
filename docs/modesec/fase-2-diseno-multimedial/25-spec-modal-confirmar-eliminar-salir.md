# Ventana 025 — Modal: Confirmar eliminación / salida

**Metodología:** MODESEC — Fase II, punto 3 y 6.
**Tokens:** ver `03-tokens-diseno.md` / `tokens.json`. Verificado con
`verificar_tokens.py` — resultado al final.
**Se abre desde:** el botón "..." del encabezado de Vista Interna
(`09-spec-vista-interna-marco.md`, que dejaba su contenido "pendiente,
fuera de esta ventana") y de la Ventana 020
(`23-spec-toma-diagnostico.md`, Pantalla de inicio). Mismo modal, **2
variantes por rol** — mismo criterio ya usado en
`18-spec-auth-verifica-correo.md` (una ventana, reutilizada por 2
flujos distintos).

**Por qué es un solo botón, no un menú desplegable:** cada rol tiene
exactamente **una** acción real disponible acá — Docente: eliminar la
experiencia. Estudiante: salir de ella. Un desplegable con un único
ítem agrega un paso sin agregar ninguna opción; se decidió que el botón
"..." abre este modal directo.

---

## 1. Nombre

`025 — Modal: Confirmar eliminación (Docente) / Confirmar salida (Estudiante)`

## 2. Imagen — construcción paso a paso en Figma

### 2.1 Marco del modal

Mismo marco grande que `15-spec-modal-confirmar-publicar.md` — ancho
fijo `912px`, alto Hug, Radio `24px`, Fill `#FFFFFF`, Stroke `1px`
`#E7E7E7`, Padding `32px`, Auto Layout Vertical, Gap `24px`. Misma fila
de encabezado de 3 zonas (caja invisible `32×32px` a la izquierda,
título centrado, botón cerrar real a la derecha).

**Título — según variante:**
- Docente: "¿Eliminar esta experiencia?"
- Estudiante: "¿Salir de esta experiencia?"

### 2.2 Card informativa

Mismo componente que `15-spec-modal-confirmar-publicar.md`, sección
2.2 — Radio `16px`, Fill `#FFFFFF`, Stroke `1px` `#E7E7E7`, Padding
`16px`, Auto Layout Vertical, Gap `16px`, alineada a la izquierda. 3
InfoBlocks (Label `13/20` `#888888`, Value `16/24` `#111111`, Gap
`4px`), mismas 3 preguntas que "Publicar experiencia" — misma
estructura de honestidad, adaptada a una acción destructiva:

**Variante Docente:**

- **"¿Qué cambia?"** — "La experiencia y todo su banco de preguntas y
  ejercicios se eliminan por completo. Deja de aparecer en tu lista y
  en la de cualquier estudiante inscrito."
- **"¿Se puede deshacer?"** — "No. Esta acción es irreversible."
- **"¿Qué se pierde?"** — valor dinámico, según haya o no datos reales
  detrás:
  - Sin estudiantes inscritos: "Todavía no hay ningún estudiante
    inscrito — no se pierde ningún dato de diagnóstico."
  - Con estudiantes y/o respuestas registradas: "**N** estudiante(s)
    inscrito(s) y **M** respuesta(s) ya registradas se eliminan junto
    con la experiencia." (N de `Inscripción`, M de `Respuesta` vía
    `Experiencia_Evidencia`).

**Variante Estudiante:**

- **"¿Qué cambia?"** — "Dejas de estar inscrito en esta experiencia. Ya
  no aparece en tu lista, y tu docente deja de verte en la suya."
- **"¿Se puede deshacer?"** — "No directamente. Si quieres volver a
  entrar, vas a necesitar el código de invitación otra vez."
- **"¿Qué se pierde?"** — valor dinámico:
  - Sin respuestas todavía (Estado A o C de la Ventana 020 — en C no
    debería llegar a mostrarse este modal salvo que se decida permitir
    salir después de completar, ver Acciones): "Todavía no respondiste
    ninguna pregunta — no se pierde ningún dato."
  - Con respuestas registradas (Estado B, En curso): "Ya respondiste
    **N** pregunta(s) en esta experiencia. Esa información se elimina
    junto con tu inscripción."

*(Nota de alcance, mismo criterio que `15-spec-modal-confirmar-publicar.md`:
qué pasa exactamente con las filas de `Presentación`/`Respuesta` al
eliminar una `Inscripción` o una `Experiencia` —si se borran físicamente
o se conservan de algún modo— no está decidido a nivel de modelo
relacional todavía. Se declara como vacío nuevo en `diseno/pendientes.md`
en vez de asumir un comportamiento. El texto de este modal no promete
un mecanismo técnico, solo advierte la consecuencia visible.)*

### 2.3 Fila de acciones (footer)

Mismo patrón que `15-spec-modal-confirmar-publicar.md`, sección 2.3:
- **Botón "Cancelar"** (Ghost, ancho Hug): alto `48px`, Padding izq/der
  `24px`, texto `16px / 22px` peso `500` Medium, color `#555555`.
- **Botón de confirmación** (ancho Fill): alto `48px`, Radio `12px`,
  texto centrado `16px / 22px` peso `500` Medium, color `#FFFFFF`. **Fill
  `#991B1B` (Error) — primer uso de este color como fondo de botón en
  el sistema** (hasta ahora solo se usaba en texto/borde de validación,
  `08-spec-unirse-codigo.md`). Se documenta como decisión nueva, no
  heredada: es la primera acción genuinamente destructiva del proyecto,
  y el rojo ya está reservado en la paleta para "algo va a salir mal /
  hay que prestar atención" — mismo significado, aplicado a una
  consecuencia que el propio usuario provoca a propósito, no a un
  error de formulario. Contraste ya verificado (8.31:1 sobre blanco,
  `03-tokens-diseno.md`) — texto blanco encima sigue pasando AAA.
  - Docente: "Eliminar experiencia".
  - Estudiante: "Salir de la experiencia".

## 3. Texto

- "¿Eliminar esta experiencia?" / "¿Salir de esta experiencia?"
  (títulos).
- Los 6 pares Label/Value de 2.2 (3 por variante).
- "Cancelar", "Eliminar experiencia" / "Salir de la experiencia"
  (botones).

## 4. Audio

No aplica.

## 5. Video

No aplica.

## 6. Animación

- Hover en botón cerrar: Fill `#FAFAF8`.
- Hover en botón de confirmación: opacidad `85%` (mismo tratamiento que
  "Publicar experiencia").
- Hover en "Cancelar": sin cambio de fondo (Ghost).

## 7. Acciones

- Clic en botón cerrar o "Cancelar" → cierra el modal sin cambios,
  vuelve a la Ventana 020 o a Vista Interna Tab Estudiantes, según
  desde dónde se abrió.
- Clic en "Eliminar experiencia" (Docente) → pasa por la Ventana 024
  (Cargando: "Eliminando la experiencia...") → elimina la `Experiencia`
  → vuelve al Dashboard del docente, la card desaparece de la lista.
- Clic en "Salir de la experiencia" (Estudiante) → pasa por la Ventana
  024 (Cargando: "Saliendo de la experiencia...") → elimina la
  `Inscripción` del estudiante → vuelve al Dashboard del estudiante, la
  card desaparece de su lista.

---

## Verificación de tokens

```
$ python3 verificar_tokens.py 25-spec-modal-confirmar-eliminar-salir.md
OK — 25-spec-modal-confirmar-eliminar-salir.md: todos los colores y valores en px están en tokens.json
```

Reutiliza el marco de `912px` y el footer Ghost+Primario ya aprobados;
el único cambio real es el color de fondo del botón de confirmación
(`#991B1B`, Error), que ya existía en `tokens.json` — no fue necesario
agregar ningún valor nuevo.
