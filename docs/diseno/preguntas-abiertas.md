# Preguntas abiertas — AdaptiveLearn (rediseño)

> Lo que se identifica como relevante pero no se resuelve en el momento en que
> aparece. Se retoma cuando el término/documento que lo necesita esté en curso.

---

## QA-001 — ¿El docente puede añadir evidencias propias?

Más allá de las evidencias oficiales del DBA, ¿se le permite al docente
agregar una evidencia que él considere necesaria para su contexto?

*(Redacción actualizada el 2026-08-26: la pregunta se escribió con el
término "punto de aprendizaje", que se renombró a "evidencia" el
2026-08-07. Sigue **abierta**, así que se enuncia en el vocabulario
vigente — una pregunta viva escrita con un término retirado se lee como
si tratara de otra cosa. La línea "Surgió en" conserva el término
original a propósito: ahí sí es historia.)*

**Surgió en:** definición de "punto de aprendizaje" — 2026-08-05
**Decisión de Alejandro:** probablemente versión futura, no esta.
**Retomar cuando:** se cierre el diseño base de experiencia y se abra la
siguiente versión de alcance.

---

## QA-002 — Cantidad de ítems por nivel SOLO

**Estado:** resuelta por ADR-008 (2026-08-07), números revisados por
ADR-016 (2026-08-21). No hay niveles ni hipótesis que triangular — la
cantidad de ítems por evidencia es adaptativa (mínimo 4, tope 6), no un
número fijo por nivel.

**Surgió en:** definición de "punto de aprendizaje" — 2026-08-05

---

## QA-003 — Tipos de interacción para preguntas/ejercicios

**Estado:** resuelta por ADR-006 (2026-08-07) — regla operativa: `single_choice`
por defecto (con distractor-hipótesis, respaldado en el FCI y en Haladyna),
`matching` para relación/clasificación explícita entre dos conjuntos,
`ordering` para secuencia/procedimiento explícito. Verificada contra una
muestra real de 8 evidencias de las 4 áreas. Quedan, como excepción
reconocida, evidencias actitudinales o de producción creativa que no caben
en ningún formato cerrado (ver ADR-006, QA-014).

**Surgió en:** definición de "punto de aprendizaje" — 2026-08-05

---

## QA-004 — ¿La jerarquía fundacional/intermedio/avanzado vive entre DBA, no dentro de uno?

Si las evidencias de un mismo DBA son planas (facetas paralelas, no escalones),
¿la idea de "prerrequisito" tiene más sentido entre DBA de distintos grados
(ej. un DBA de grado 7 como base de uno de grado 9) que entre evidencias de un
mismo DBA?

**Surgió en:** definición de "punto de aprendizaje" — 2026-08-05, a raíz del
catch de Alejandro sobre el grafo vs. el plano. Resuelto para esta versión por
ADR-001 (los puntos quedan sueltos dentro de un DBA).
**Retomar cuando:** se defina el término "unidad" — Alejandro señala que esta
idea (prerrequisito entre DBA de distintos grados) pertenece ahí, no a la
experiencia individual.

---

## QA-005 — ¿Cómo se gradúa la profundidad/dificultad dentro de un diagnóstico, sin SOLO?

**Estado:** superada por ADR-008 (2026-08-07). ADR-003 (2026-08-06) había
propuesto Bloom como reemplazo de SOLO para graduar profundidad, pero el
mecanismo final de diagnóstico (ADR-008) no gradúa profundidad en
absoluto — solo determina muestra/no muestra/no concluyente por
evidencia. La pregunta original queda sin objeto en esta versión: no hay
"profundidad" que graduar porque no hay escalera (ver también QA-015).

**Surgió en:** discusión de SOLO / diagnóstico — 2026-08-05

---

## QA-006 — Auditar los generadores de preguntas de diagnóstico duplicados

**Estado:** resuelta por ADR-012 (2026-08-07) — auditoría completa. Dos
generadores activos tras un env var (`DIAGNOSTIC_GENERATION_STRATEGY`),
ambos atados al modelo retirado (SOLO, grafo de prerrequisitos, "punto
de aprendizaje" inventado); código simulado (`generar_preguntas_n5_opcionales`)
mezclado como si fuera real; `interaction_evidence_planner.py` con una
idea reutilizable (reglas por patrón de texto → interacción) aunque no
el código en sí. Decisión: se construye de nuevo, no se adapta.

**Surgió en:** discusión de SOLO / diagnóstico — 2026-08-05

---

## QA-007 — `target_solo` también llega hasta práctica, no solo diagnóstico

`intervention_path.py` usa `target_solo` para construir las fases de la
intervención (profundidad del ejemplo trabajado y la práctica focalizada).
Retirar SOLO sin reemplazo deja a práctica sin esa señal.

**Estado:** sin objeto por ahora — 2026-08-07. Doblemente superada: ADR-007
dejó práctica fuera de esta versión, y ADR-008 retiró la función de Bloom
que QA-005/ADR-003 le habían asignado a diagnóstico (mismo reemplazo que
esta pregunta esperaba heredar). Se reabre, si hace falta, cuando
práctica vuelva a estar en alcance — y ahí habrá que resolverla de nuevo,
no asumir que Bloom sigue siendo la respuesta.

**Surgió en:** definición de "práctica" — 2026-08-05

---

## QA-008 — ¿Pre-generar y curar la práctica antes de cualquier interacción del estudiante?

**Estado:** resuelta por ADR-004 (2026-08-07) — se pre-genera una ruta de
práctica por cada (punto de aprendizaje, hipótesis de error) posible; el
docente la revisa una sola vez antes del primer estudiante; sin fallback
necesario mientras diagnóstico use solo formatos cerrados. "Curar" con uso
real queda sin resolver — depende de datos que no existen todavía.

**Depende de:** QA-006 (auditar generadores de diagnóstico) — el catálogo de
ítems/distractores también tendría que curarse una vez, no regenerarse cada
vez, para que el universo de brechas sea de verdad enumerable.

**Surgió en:** definición de "práctica" — 2026-08-05, idea de Alejandro.

---

## QA-009 — ¿Cómo combina Reporte los datos de diagnóstico, práctica y verificación?

**Estado:** sin objeto en esta versión — 2026-08-07. ADR-007 dejó práctica y
verificación fuera de alcance; en esta versión Reporte solo agrega lo que
diagnóstico produce, no hay tres orígenes que combinar. Se reabre cuando
práctica/verificación vuelvan a estar en alcance.

**Surgió en:** definición de "reporte" — 2026-08-05

---

## QA-010 — ¿Puede el docente elegir qué evidencias de un DBA entran en la experiencia?

En esta versión, todas las evidencias oficiales del DBA que el sistema
puede evaluar entran a la experiencia — sin selección. A futuro, el
docente podría decidir cuáles incluir según su contexto (mismo tipo de
idea que QA-001).

**Surgió en:** modelo conceptual — 2026-08-06
**Retomar cuando:** se abra la siguiente versión de alcance (junto con QA-001).

---

## QA-011 — ¿Para qué sirve el "ejemplo" del DBA (tercera parte de su estructura oficial)?

**Estado:** resuelta por ADR-011 (2026-08-07) — el ejemplo se usa como
contexto/escenario para la generación de ítems de diagnóstico, verificado
contra los 4 documentos oficiales (mayoría texto real, no imágenes).
**Datos cargados el 2026-11-10 (encargo 05, en revisión):** el catálogo
(`data/curriculo-men/catalogo/catalogo_dba.json`) trae el ejemplo de cada
DBA, copiado exacto y verificado contra su página, y la marca
`ejemplo_tiene_imagen`; el backend lo carga y el Paso 2 lo muestra
(`06-spec` §2.4). **Hallazgo que corrige a ADR-011:** las figuras no son
"2 a 8 por área": 259 de los 343 ejemplos incluyen una (imagen, dibujo,
tabla o fórmula aparte), aunque casi todos traen también texto completo.
Ciencias Sociales V.1 trae ejemplo en solo 21 de 82 DBA. Detalle en
`catalogo/informe-correccion.md` §8.

**Surgió en:** discusión de Bloom / diagnóstico — 2026-08-06, catch de
Alejandro.

---

## QA-012 — Costo de revisión recurrente si algún día se usa formato abierto

**Estado:** cerrada — 2026-08-07. Esta versión de diagnóstico se queda en
formato **cerrado únicamente**. Verificado contra la fuente oficial (DBA
Matemáticas V.2, "Comentarios finales sobre los DBA", punto d): "las
evidencias de aprendizaje... todas en su conjunto buscan dar pistas
adecuadas del aprendizaje" — el MEN mismo las trata como indicios
colectivos, no como una lista exhaustiva de cumplimiento obligatorio. Por
tanto el diagnóstico automático puede apoyarse en el **subconjunto** de
evidencias oficiales que sí aceptan formato cerrado, sin inventar
evidencias nuevas y sin debilitar el principio de "evidencia oficial, no
invención de la IA". Si algún DBA no tuviera ninguna evidencia compatible
con formato cerrado, ese DBA completo queda fuera del diagnóstico
automático en esta versión — se marca explícito para el docente, no se
fuerza un ajuste imperfecto ni se calla el vacío.

Los niveles altos de Bloom (Analizar) y algunas evidencias de tipo
"producción" pueden necesitar respuesta abierta genuina — pero abierta
cambia el tipo de revisión: el docente ya no revisa **una vez** (como en
ADR-004), sino **cada respuesta de cada estudiante**, de forma recurrente.
Ese costo es la razón de fondo para quedarnos en cerrado-únicamente por
ahora.

**Relacionado con:** QA-003 (criterio operativo de formato por evidencia
— resuelta por ADR-006) y la condición de ADR-004 sobre formatos cerrados
(el "sin fallback necesario" se rompe si esto se habilita).

**Surgió en:** discusión de Bloom / diagnóstico — 2026-08-06, catch de
Alejandro.

---

## QA-013 — Bug de extracción en las evidencias del currículo normalizado

Al verificar si existe algún DBA con una sola evidencia (para el punto 4 del
mecanismo de diagnóstico), se encontraron errores reales en
`curriculo_men_normalizado.json`: los 3 registros con conteo "1" no son
casos genuinos, son extracción rota — 2 tienen varias evidencias fusionadas
en un solo string por una viñeta del PDF no reconocida (aparece como una
"m" suelta entre evidencias), y 1 tiene la evidencia cortada a media
oración. Se encontraron 2 casos más del mismo bug de viñeta en registros
que sí tienen más de una evidencia (no bajaron a conteo 1, pero igual están
mal separados). Esto invalida el "1" del rango que quedó escrito en
`modelo-conceptual.md`, y sugiere que puede haber más casos sin detectar
en los 342 DBA totales.

**Alcance de la revisión pendiente:** no es compleja técnicamente, pero sí
extensa — comparar cada uno de los 342 DBA contra su página oficial del
MEN. Alejandro prefiere hacerla cuando exista un frontend/UI definido para
revisar esto cómodamente, no ahora en texto plano.

**Surgió en:** discusión del punto 4 (formato por evidencia) — 2026-08-07,
al intentar verificar si un DBA con 1 evidencia existe realmente.
**Retomar cuando:** exista una UI de revisión de datos curriculares.

---

## QA-014 — Censo real de qué proporción de evidencias/DBA admite formato cerrado

Antes de comprometer el diseño de diagnóstico al enfoque cerrado-únicamente
(QA-012) como algo viable en la práctica —no solo válido en principio—,
hace falta saber qué porcentaje de las evidencias reales del currículo
admite razonablemente `single_choice`/`matching`/`ordering`. Si la
proporción es baja, el enfoque cerrado-únicamente dejaría fuera del
diagnóstico automático una porción significativa del currículo — sería un
problema de fondo para el diseño completo, no un detalle a ajustar
después. Hay antecedente para sospechar que varía por área: ADR-002 ya
advirtió que el método de distractor-con-hipótesis-de-error es más fuerte
en Matemáticas y Ciencias Naturales que en Lenguaje y Ciencias Sociales.

**Depende de:** QA-013 — no tiene sentido censar formato-compatible sobre
evidencias con extracción rota (truncadas o con viñetas fusionadas); el
resultado no sería confiable.

**Surgió en:** cierre de la discusión del punto 4 — 2026-08-07, catch de
Alejandro.
**Retomar cuando:** se audite/corrija QA-013, y exista una UI para hacer
el censo cómodamente (mismo motivo que QA-013).

**Estado (2026-11-10): censo hecho, propuesto por IA, falta validarlo.**
Cómo: ADR-042 y `criterios-censo-formato-cerrado.md`. Resultado
(encargo 05, `data/curriculo-men/censo/informe-censo.md`): **904 de 1282
evidencias (71 %) admiten formato cerrado**: Matemáticas 77 %, Ciencias
Naturales 83 %, Ciencias Sociales 70 %, y **Lenguaje 56 %**. La respuesta
a la pregunta de fondo: el enfoque cerrado-únicamente es viable en tres
áreas, pero **en Lenguaje deja fuera casi la mitad** (hablar, escuchar,
escribir), como anticipaba ADR-002. **16 DBA quedan sin ninguna evidencia
aplicable** (10 de Lenguaje) y no se pueden usar para crear una
experiencia en esta versión (QA-012). Se cierra cuando dos integrantes
validen la muestra (`censo/muestra_validacion.md`, criterios §5).

---

## QA-015 — ADR-003 quedó ambiguo sobre si Bloom es escalera o clasificación

**Estado:** resuelta por ADR-008 (2026-08-07). Bloom no tiene función en
el mecanismo final de diagnóstico — no hay escalera de profundidad por
evidencia ni catalogación de nivel; el mecanismo solo determina
muestra/no muestra/no concluyente por evidencia. ADR-003 sigue siendo
válida como registro histórico de por qué se adoptó Bloom en su momento,
pero su aplicación práctica queda retirada por ADR-008.

**Surgió en:** discusión de la regla de confianza suficiente — 2026-08-07,
catch de Alejandro.

---

## QA-016 — ¿Puede un estudiante crear su propia experiencia (autoestudio)?

Hasta ahora todo el diseño asume que quien crea una Experiencia es el
docente, y que el estudiante solo responde el diagnóstico. Surgió la
idea de que un estudiante también pudiera crear una experiencia para sí
mismo (autoestudio), uniéndose además a las que otros docentes crean.

**Por qué se difiere, no solo se pospone por complejidad:** rompe el
fundamento de dos decisiones ya tomadas, no solo agrega trabajo. ADR-005
exige que el docente revise el banco antes de que un estudiante lo vea —
si el creador y quien lo usa son la misma persona, esa revisión
independiente pierde su función (autoevaluación no es lo mismo que
revisión con criterio pedagógico externo). *(Precisión 2026-10-21: la
revisión no es obligatoria — el sistema la recuerda, no la exige
(ADR-026) — pero sigue siendo el docente quien decide publicar; con un
creador-estudiante, esa decisión externa desaparece igual.)* Y Reporte está diseñado para
agregar a nivel de grupo ("un docente con 30-40 estudiantes") — con un
solo estudiante como creador, no hay grupo que agregar.

**Consecuencia para esta versión:** el Dashboard y el flujo de creación
quedan exclusivos del rol docente. El estudiante solo puede unirse a
experiencias ya creadas, vía código de invitación — este mecanismo
("Unirse con código") no se afecta ni se retira.

**Surgió en:** diseño del Dashboard, Fase II — 2026-08-07, idea de
Alejandro.
**Retomar cuando:** se abra una versión de alcance que reconsidere el rol
del estudiante, junto con QA-001 y QA-010 (mismo tipo de expansión de
alcance).

---

## QA-017 — ¿Qué hacer, en una versión futura, con las evidencias que el formato cerrado no alcanza?

**Estado:** abierta, para la próxima versión de alcance. **Esta versión
no cambia:** cumple hasta donde el MEN lo permite (QA-012). El censo de
formato cerrado (`criterios-censo-formato-cerrado.md`) dice cuáles
evidencias quedan fuera; el Paso 2 las muestra tachadas con "no aplica a
formato cerrado" (`06-spec` §2.4), así que el docente ve el vacío en vez
de que se esconda.

**La duda de fondo (Alejandro, 2026-11-10):** son muchas las evidencias
que piden producir, comunicar, argumentar, actuar o una actitud (reglas
N1 a N5 del censo). ¿Se pueden crear otras evidencias a partir de ellas,
adaptarlas, o diagnosticarlas de otra forma?

**Caminos posibles, sin decidir.** Cada uno, con lo que choca:

1. **Formatos abiertos** (respuesta corta, texto, archivo), con la IA
   proponiendo una valoración y el docente decidiendo. Choca con el costo
   que cerró QA-012: el docente revisa cada respuesta de cada estudiante,
   no el banco una sola vez. Y una valoración de la IA sobre un
   estudiante roza "nunca un texto sobre un estudiante redactado por IA".
2. **Registro de observación del docente.** Para lo que se ve en clase
   (comunicar en vivo, actuar, actitudes: N2, N4, N5), el docente marca
   directamente, por estudiante, uno de los estados que el sistema ya
   usa (muestra, no muestra, no concluyente). Sin IA y sin preguntas: el
   sistema solo guarda y agrega. Encaja con el modelo de estados actual.
3. **Indicadores derivados del docente.** Partir una evidencia amplia en
   indicadores más pequeños, como ya hacen muchas instituciones con sus
   indicadores de desempeño (el Decreto 1290 de 2009 les da autonomía
   para definir su sistema de evaluación). Es la misma idea de QA-001.
   Condición: un indicador derivado **nunca se presenta como del MEN**;
   va separado del contenido oficial y enlazado a la evidencia de origen,
   como el dictamen está separado de la evidencia (H-6).
4. **Reescribir o "adaptar" la evidencia oficial.** **No**, en ninguna
   versión: el contenido del MEN se copia exacto. Lo que se quiera
   adaptar entra como el camino 3.
5. **Que la IA proponga los indicadores derivados.** Posible solo como
   propuesta que el docente revisa y acepta. Si no, rompe el principio
   "evidencia oficial, no invención de la IA" (QA-012).

**Lo que hay que saber antes de decidir:** el censo de esta versión dice
cuántas evidencias quedan fuera, por área y por regla. Si son pocas, el
camino 2 basta; si son muchas en Lenguaje y Ciencias Sociales, como
anticipa ADR-002, conviene pensar en el 1 o el 3.

**Relacionado con:** QA-001 (evidencias propias del docente), QA-012
(solo formato cerrado), QA-014 (el censo), ADR-002, ADR-006.

**Surgió en:** aprobación de los criterios del censo — 2026-11-10,
Alejandro.
