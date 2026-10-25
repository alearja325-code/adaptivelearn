# Entrega — Fase III, Diseño Computacional

> **⚠ BORRADOR ANTERIOR AL CIERRE DE LA FASE II — no es fuente de verdad.**
> Se hizo entre agosto y septiembre de 2026, mientras la Fase II seguía
> abierta. Después cambiaron decisiones que lo afectan (ADR-026 a
> ADR-029, entre otras). La fuente de verdad es la Fase I, la Fase II y
> `diseno/decisiones.md`; la Fase III se rehace en orden desde
> `10-proceso-desarrollo.md`, y este documento se usa como insumo, no como
> base. Lo que el modelo nuevo debe recibir está en `diseno/pendientes.md`,
> sección "Entrada a Fase III". *(Aviso agregado el 2026-10-21, decisión
> de Alejandro.)*

Este documento es el índice de la entrega. Se escribió para responder a
una crítica concreta de la revisión anterior —el hallazgo **H-11**: *«la
mitad de las fuentes citadas no está en la carpeta entregada… la regla de
construcción existe, pero el lector no puede ejercerla»*— y para que cada
hallazgo se pueda verificar sin buscar.

---

## 0. Los archivos de esta entrega

| PDF | Qué es | Formato |
|---|---|---|
| `0-Entrega-Fase-III-indice.pdf` | Este documento | A4 |
| `1-Modelo-Entidad-Relacion.pdf` | Entregable 1 | A4 |
| `2-Modelo-Relacional.pdf` | Entregable 2 | A4 |
| `3-Diccionario-de-Datos.pdf` | Entregable 3 | A4 apaisado |
| `4-Triaje-de-la-revision-docente.pdf` | Anexo: los 12 hallazgos, clasificados | A4 |
| `5-Diagramas-del-MER.pdf` | Leyenda de notación y las seis vistas, en Chen | A4 apaisado |
| `6-Mapa-completo-MER.pdf` | El mapa completo, una sola lámina | **A2** apaisado |

**Por qué el mapa completo va aparte y en A2:** mide 4200 × 3196 px con
sus 74 atributos. Reducido a una hoja A4 sus rótulos no se leen — se
comprobó. En A2 se lee a tamaño real. Las seis vistas sí caben en A4
apaisado y ahí están.

Los PDF se generan desde los mismos Markdown que se verifican; no se
editan a mano. La herramienta es `herramientas/md_a_pdf.py`.

## 1. Qué pide MODESEC en esta fase, y dónde está

MODESEC lo dice textualmente: *«Se deberá crear un MER…, un MR (Modelo
relacional) basado en el MER y un diccionario de datos para los
metadatos (como tipos, tamaños, y otras cualidades de los campos de
datos)»*.

| Entregable | Archivo | Estado |
|---|---|---|
| **1. Modelo Entidad-Relación** | `01-modelo-entidad-relacion.md` | Quinta revisión (2026-09-08) |
| ↳ Diagramas en notación Chen | `mer-entrega/` — mapa completo + 6 vistas, SVG y PNG | Generados y verificados |
| **2. Modelo Relacional** | `04-modelo-relacional.md` | Actualizado a la Quinta revisión (2026-09-19) |
| ↳ Esquema ejecutable y diagrama | `modelo-relacional/mr_esquema.sql`, `mr_adaptivelearn.dbml` | Generados y probados contra motor |
| **3. Diccionario de datos** | `06-diccionario-datos.md` | **Nuevo** (2026-09-19) — 14 tablas, 72 columnas |

---

## 2. Los 12 hallazgos de la revisión del 2026-09-01

La revisión completa está en `revision-docente/`. El triaje razonado, en
`05-triaje-revision-docente.md`. Aquí, dónde quedó cada uno.

### Los tres bloqueantes

| # | Hallazgo | Cómo se resolvió | Dónde verificarlo |
|---|---|---|---|
| **H-1** | «La configuración del diagnóstico no tiene dónde vivir» | **Cae casi entero, por decisiones posteriores a la versión revisada.** Pedía guardar tres datos por evidencia; dos dejaron de existir: ADR-016 le quitó al docente decidir cuántos ítems (los fija el sistema: mínimo 4, tope 6) y ADR-024 eliminó el orden de evaluación (es el orden oficial del MEN, ni sugerido ni reordenable). El tercero era, en realidad, H-4. | `decisiones.md` → ADR-016, ADR-024 |
| **H-2** | La secuencia adaptativa no se puede reconstruir; RI-11 queda sin poder verificarse | Entidad **`Presentación`** + `Respuesta.fecha_respuesta`. Cierra también el vacío V-1. | MER §Presentación · `presentacion` en el diccionario |
| **H-3** | «Se le presentó y no respondió» no es representable | Respuesta cuelga de Presentación con cardinalidad (0,1): una Presentación **sin** Respuesta es válida y significa exactamente eso. **Probado**: `verificar_mr.py`, prueba en positivo. | MER §Respuesta · `verificar_mr.py` bloque B |

### Los cuatro de contenido

| # | Hallazgo | Cómo se resolvió |
|---|---|---|
| **H-4** | No existe el vínculo Experiencia–Evidencia; RI-1 y RI-2 tapan el hueco | Entidad **`Experiencia_Evidencia`**. Las dos reglas **desaparecen**: pasan a ser estructura. El argumento del hallazgo —«un ciclo que hay que restringir con una regla externa suele indicar que falta una entidad»— se aceptó tal cual. |
| **H-5** | Falta el estado de revisión del ítem | **El atributo sí, la regla no.** Entran `Item.origen` y `Item.estado_revision`. **No** se adopta la regla de publicación asociada: contradice una decisión ya tomada en `12-spec-modal-banco-items.md` (revisar el banco no es prerrequisito para publicar). El vocabulario exacto de estados sigue abierto y queda declarado como **V-7**. |
| **H-6** | `aplica_formato_cerrado` cuelga de una entidad declarada «dato del MEN» | Entidad **`Evidencia_Dictamen`**. El atributo sale de `Evidencia`. Es el mejor hallazgo conceptual de la revisión: ese dato es juicio nuestro, no del MEN, y mezclarlos borraba la frontera que Fase I §2 declara como valor. |
| **H-7** | La regla de parada no está definida en ninguna fuente | **Acierta en el fondo.** ADR-016 sí define la regla de forma cualitativa (el revisor no pudo verla — es su propio H-11), pero **qué combinación exacta de acierto × certeza cuenta como señal fuerte no está definida en ningún lado**. Se declara como vacío **V-5**, previo a cualquier implementación. |

### Los cinco de forma y repositorio

| # | Hallazgo | Cómo se resolvió |
|---|---|---|
| **H-8** | El MER muestra llaves foráneas: deja de ser Chen | **Cerrado: notación Chen.** Los diagramas de `mer-entrega/` son Chen estricto — rectángulos, rombos, elipses; entidad débil con doble borde, relación identificadora con rombo doble, participación total con línea doble, razón de cardinalidad bajo cada rombo. La versión caja-tabla queda como vista de apoyo. |
| **H-9** | RI-7 no fija los mínimos de Opción por formato | Corregido dentro de RI-4: 2 opciones en `single_choice` y `ordering`; **4 en `matching`**, con al menos 2 por grupo. |
| **H-10** | Conviven tres versiones del MER, y las de la carpeta MODESEC son las superadas | `01-modelo-entidad-relacion.md` **declara en su encabezado** que es el vigente. `03-presentacion-mer.html`, que era el obsoleto real, ahora abre con un **aviso rojo** que dice que está superado y a qué documento ir. |
| **H-11** | La mitad de las fuentes citadas no está en la carpeta | **Este documento, más la sección 4.** El paquete de entrega ahora incluye `diseno/` completo. |
| **H-12** | Fase II nunca diseñó las pantallas del diagnóstico ni de Reporte | **Parcialmente resuelto, y se dice cuál parte falta.** Reporte sí se diseñó (Ventana 010 y su modal). La **toma del diagnóstico sigue pendiente** — ver sección 5. |

---

## 3. Lo que este modelo declara como no resuelto

Un modelo que rellena los huecos que no sabe resolver afirma más de lo
que sostiene. Estos quedan marcados:

| Id | Qué falta | Consecuencia |
|---|---|---|
| **V-5** | La regla de parada exacta: qué combinación de `correcta` × `certeza` (CRI 0-5) cuenta como señal fuerte | RI-11 es verificable en forma, no en contenido. **Previo a cualquier implementación.** Nace del H-7. |
| **V-6** | El dictamen de formato cerrado depende del censo QA-014, sin terminar | `evidencia_dictamen` existe y tiene `fecha_dictamen` justamente porque su contenido puede cambiar |
| **V-7** | Vocabulario de `item.estado_revision` | Por eso su tipo es `VARCHAR` y no `ENUM` |
| **V-9** | Versionado de contenido del ítem | Diferido con razón escrita; se evaluó la alternativa propuesta por otro grupo y se descartó para esta versión |
| **Hueco nuevo** | Nada impide que una `presentacion` empareje una inscripción de una experiencia con un ítem de otra | Encontrado al construir el MR. Se declara en vez de resolverse ahí, porque el MER no delegó esa decisión. Ver `04-modelo-relacional.md` |

---

## 4. Dónde están las fuentes citadas (respuesta a H-11)

El modelo cita ADR, QA y documentos de diseño que en la entrega anterior
no estaban. **Todos viven en `diseno/`**, que ahora va incluido:

| Archivo | Qué contiene |
|---|---|
| `diseno/decisiones.md` | **ADR-001 a ADR-025.** Cada decisión con su contexto, su alternativa descartada y su consecuencia reconocida |
| `diseno/preguntas-abiertas.md` | **QA-001 a QA-016.** Las preguntas de diseño y su estado |
| `diseno/glosario.md` | Vocabulario del proyecto |
| `diseno/modelo-conceptual.md` | Conceptos y sus relaciones, previo al MER |
| `diseno/vision.md` | Alcance, y lo que el sistema **no** es |
| `diseno/pendientes.md` | Estado real del trabajo, con lo que falta |

Las tres herramientas de verificación de consistencia
(`verificar_consistencia.py`, `verificar_cadena.py`, y las de cada fase)
también van incluidas: son la forma de comprobar mecánicamente que estos
documentos no se contradicen entre sí.

**Sobre `curriculo_men_normalizado.json`:** no se incluye. Es un
artefacto de datos de una versión anterior del proyecto (ver
`diseno/vision.md`, «Historia de versiones»), no un documento de diseño,
y arrastra el bug de extracción declarado en QA-013.

---

## 5. Qué falta, con honestidad

**La toma del diagnóstico (pantalla del estudiante) sigue sin
diseñarse.** Es el resto vivo del hallazgo H-12, y conviene decir por
qué importa: el propio revisor explicó que H-1, H-2 y H-3 se escaparon
*porque* esa pantalla no existía —«el método del modelo es que un campo
entra si alguna spec ya lo pinta»—. Que hoy el modelo ya incluya
`Presentación` **no** se apoya en esa pantalla, sino en ADR-016, que es
una decisión de mecanismo ya cerrada.

Dicho eso, el riesgo residual es real y se declara: **al diseñar esa
pantalla podría aparecer un campo que hoy falta.** No se afirma lo
contrario.

Fase II está al 80-90%: faltan esa pantalla y los tres últimos puntos de
MODESEC para esa fase (mapa de navegación, guión técnico, índice de
recursos). Esta entrega de Fase III se adelanta a eso porque el
calendario del curso lo pide — es una secuencia forzada, no un cambio de
plan, y queda anotada como tal.

---

## 6. Cómo verificar esta entrega sin leerla entera

Todo lo que este paquete afirma se puede comprobar ejecutando:

```bash
# El MR no se aparta del MER
cd fase-3-diseno-computacional/modelo-relacional
python3 _verificar_mr_mer.py

# El esquema es real: 31 comprobaciones, de las cuales 20
# intentan insertar datos que DEBEN ser rechazados
python3 verificar_mr.py

# Los diagramas Chen no tienen defectos geométricos
cd ../diagrama && python3 _verificar_mapa.py

# Cada relación vive en exactamente una vista
python3 _verificar_vistas.py

# Los documentos de diseño no se contradicen entre sí
cd ../../../../diseno
python3 verificar_consistencia.py
python3 verificar_cadena.py
```

Esa es la diferencia entre revisar con cuidado y comprobar: si una
restricción que este modelo declara «automática» no existe de verdad en
el esquema, `verificar_mr.py` falla — diga lo que diga la prosa.
