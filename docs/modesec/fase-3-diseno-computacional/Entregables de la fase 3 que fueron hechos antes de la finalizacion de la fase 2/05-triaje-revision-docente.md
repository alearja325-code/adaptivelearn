# Triaje de la revisión del docente al MER

**Qué es este documento.** El docente del curso (203453 — Diseño y
Desarrollo de Software Educativo II) revisó el Modelo Entidad-Relación
del proyecto y entregó una crítica profesional con 12 hallazgos y una
propuesta de modelo corregido. Este archivo registra **qué de esa
crítica sigue siendo válido contra el estado real del proyecto hoy**, y
qué ya no. No reemplaza su documento: lo tría.

**Documento original:** `revision-docente/revision-docente-2026-09-01.html`
(copiado al repo el 2026-09-04 — estaba solo en la carpeta de descargas
personal, que es el mismo problema que su propio hallazgo H-10 señala).

**Triaje elaborado:** 2026-09-04.

---

## Lo primero, y lo que más importa

El docente revisó una versión del MER del **2026-08-20**, junto con
Fase I y Fase II tal como estaban hace 2-4 semanas. Desde entonces el
proyecto cambió de forma sustancial: se escribieron ADR-016 a ADR-024,
el MER se revisó 4 veces (última: 2026-08-27), se derivó el Modelo
Relacional completo, y se especificaron 6 ventanas más de Fase II
incluyendo todo Reporte.

**Por eso su crítica no se puede aplicar tal cual.** Parte de lo que
señala ya está corregido; parte se apoya en decisiones que después
reemplazamos; y parte sigue siendo enteramente válida. Aplicarla sin
triar sería reintroducir decisiones que ya descartamos con razones
escritas.

## Su veredicto, en una frase

El MER cubre sin huecos las 8 ventanas de Fase II, pero **no sostiene
el mecanismo de diagnóstico que Fase I describe** — que es la razón de
existir del proyecto.

Su explicación de la causa (hallazgo H-12) es la parte más valiosa de
toda la revisión, y es correcta:

> "El método del modelo es que un campo entra si alguna spec ya lo
> pinta; y como la pantalla donde el estudiante responde nunca se
> especificó, ninguna spec podía pedir el registro de la presentación.
> El método funcionó exactamente como está escrito, y aun así el hueco
> pasó — porque la fuente que lo exigía era Fase I, no Fase II."

Esto confirma el riesgo que el propio MER declara en su sección "Por
qué esto se adelanta a Fase III sin haber cerrado Fase II". No
descubrió algo que ignorábamos: documentó el precio de habernos
adelantado.

---

## Triaje de los 12 hallazgos

### Grupo A — Válidos e independientes de las pantallas que faltan (5)

Estos son problemas del modelo que existirían igual aunque Fase II
estuviera terminada. **No se pueden justificar diciendo "falta Fase
II".**

| # | Hallazgo | Por qué se acepta |
|---|---|---|
| **H-4** | Falta el vínculo directo Experiencia–Evidencia; RI-1 y RI-2 existen solo para tapar ese hueco | "Un ciclo que hay que restringir con una regla externa suele indicar que falta una entidad, no que sobra un camino." Argumento correcto. |
| **H-6** | `aplica_formato_cerrado` vive en `Evidencia`, que el propio modelo declara "dato oficial del MEN" | Ese dato **no** lo produce el MEN: es dictamen nuestro (ADR-006, pendiente de QA-014). Ponerlo ahí contradice el valor que Fase I §2 declara — "el sistema no se atribuye autoridad curricular que no tiene". El mejor hallazgo conceptual de la revisión. |
| **H-9** | Los mínimos de Opción por formato no están fijados (`matching` necesita 4, no 2) | Correcto y pequeño. |
| **H-8** | El MER muestra llaves foráneas → deja de ser notación Chen y se solapa con el MR | Decisión de formato legítima, pero hay que tomarla a propósito. **Pendiente de confirmar con el docente o la rúbrica del curso.** |
| **H-11** | La mitad de las fuentes citadas (ADR, glosario, `decisiones.md`) no estaba en la carpeta entregada | Problema de **empaquetado**, no de diseño. Media crítica se apoya en documentos que él nunca pudo ver. Se corrige en la próxima entrega incluyendo `/diseno/`. |

### Grupo B — Se disuelven al diseñar las pantallas que faltan (3)

Los tres que él marca como **bloqueantes**. No son descuidos del
modelo: son consecuencia directa de que la pantalla donde el estudiante
responde el diagnóstico (pendiente A5) nunca se diseñó.

| # | Hallazgo | Qué lo resuelve |
|---|---|---|
| **H-2** | No se puede reconstruir la secuencia adaptativa; RI-11 queda enunciada pero no verificable | Diseñar la toma del diagnóstico obliga a definir qué se le presenta al estudiante y cuándo. De ahí sale la entidad que falta. |
| **H-3** | "Se le presentó y no respondió" no es representable — es indistinguible de "nunca se le mostró" | Mismo origen. **Nota:** esto afecta un texto que ya escribimos — el separador "Sin concluir" de Tab Estudiantes promete distinguir "no ha empezado" de "tiene alguna evidencia a medias", y hoy el modelo no puede hacerlo. |
| **H-12** | Fase II nunca diseñó las pantallas del diagnóstico ni de Reporte | **Parcialmente resuelto:** Reporte sí se diseñó (Ventana 010 + su modal). Falta solo la toma del diagnóstico. |

### Grupo C — Obsoletos o a medias: juzgó una versión anterior (4)

| # | Hallazgo | Estado real |
|---|---|---|
| **H-1** | "La configuración del diagnóstico no tiene dónde vivir" — pide guardar 3 datos por evidencia | **Cae casi entero.** ADR-016 quitó al docente la decisión de cuántos ítems (el sistema fija mín. 4 / tope 6). ADR-024 eliminó el orden sugerido por IA y reordenable. De los 3 datos que pide, 2 dejan de existir. El tercero (qué evidencias diagnostica la experiencia) es en realidad H-4. |
| **H-5** | Falta `estado_revision` del ítem, y propone que ninguna Experiencia se publique con ítems sin revisar | **El atributo sí, la regla no.** `origen` y `estado_revision` son valiosos (es nuestro vacío V-7). Pero su regla propuesta **contradice una decisión explícita**: `12-spec-modal-banco-items.md` dice que revisar el banco no es prerrequisito para publicar — el docente puede no abrir nunca ese modal y aun así publicar. **No se adopta.** |
| **H-7** | "La regla de parada no está definida en ninguna fuente" | **Media razón, por el motivo equivocado.** ADR-016 sí la define (mín. 4, se detiene con mayoría de señales fuertes, tope 6) — él no pudo verla, es su propio H-11. **Pero acierta en el fondo:** qué combinación exacta de acierto × certeza (CRI 0-5) cuenta como "señal fuerte" no está definida en ningún lado. Ese vacío es real. |
| **H-10** | Conviven 3 versiones del MER y las de la carpeta MODESEC son las superadas | **Parcialmente resuelto.** `01-modelo-entidad-relacion.md` ya lleva 4 revisiones hasta el 2026-08-27 e incluye `Respuesta_Opción`. El obsoleto real es `03-presentacion-mer.html` (2026-08-19), que sigue sin marcarse como superado. |

---

## Lo que su crítica destapó y él no vio

Su hallazgo H-1 obligó a releer `08-diseno-aprendizaje.docx`, y ahí
apareció un error nuestro, de la misma semana: el documento todavía
dice, dos veces, que el sistema "sugiere un orden de evaluación de las
evidencias, estimado por dificultad (ADR-005)" y que el estudiante
responde "en el orden que el docente definió".

**ADR-024 eliminó las dos cosas.** La cascada de esa ADR no llegó a
Fase I. Es deuda del 2026-08-29, pendiente de corregir.

---

## Decisiones pendientes, que no son técnicas

1. **Notación del MER (H-8).** Hay que confirmar con el docente o con
   la rúbrica del curso si se evalúa notación Chen estricta. Si sí, el
   MER actual no lo es. No se decide por omisión.
2. **Vacío nuevo: la regla de parada exacta (su V-5, nuestro H-7).**
   Qué umbral de certeza cuenta como señal fuerte. Sin eso,
   `Resultado.estado` no es computable y RI-11 no es verificable.

## Ruta acordada

Fecha de entrega de Fase III: final del semestre — hay margen para
hacerlo en el orden correcto de MODESEC, no a parches.

1. Cascada de ADR-024 a Fase I (deuda inmediata).
2. Cerrar Fase II: **toma del diagnóstico** (pendiente A5) — es la
   pantalla de la que sale todo lo que el Grupo B reclama.
3. Definir la regla de parada exacta.
4. **Recién entonces:** MER v2 incorporando el Grupo A, y de ahí el
   Modelo Relacional actualizado.
5. En paralelo y barato: incluir `/diseno/` en la próxima entrega
   (H-11) y marcar `03-presentacion-mer.html` como superado (H-10).

**Sobre responderle al docente:** la respuesta honesta no es "todo esto
se resuelve al terminar Fase II" — eso solo aplica al Grupo B. El
Grupo A son hallazgos que aceptamos, y el Grupo C requiere mostrarle
las decisiones posteriores (ADR-016, ADR-022, ADR-024) que él no tuvo a
la vista, que es justamente su hallazgo H-11.
