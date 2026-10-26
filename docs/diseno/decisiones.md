# Registro de decisiones (ADR) — AdaptiveLearn (rediseño)

> Una decisión por entrada, numerada. Nunca se edita una decisión vieja — si
> cambia, se escribe una nueva que dice "reemplaza a ADR-00X".

---

## ADR-001 — Los puntos de aprendizaje quedan sueltos, sin conexión obligatoria

**Fecha:** 2026-08-05
**Estado:** aceptada; **modificada por ADR-024** — la sugerencia de orden o conexión por IA queda sin efecto: el orden es el oficial del MEN y ninguna pantalla mostraba esa sugerencia (barrido de coherencia, 2026-10-21).

**Contexto:** el mapa exigía que todo punto tuviera al menos una conexión
("no se permiten puntos aislados en el grafo"), y derivaba fundacional /
intermedio / avanzado de esas conexiones. Al anclar el punto de aprendizaje a
evidencias oficiales del DBA, se hizo evidente que esas evidencias vienen en
un **plano** (facetas paralelas del mismo aprendizaje), no en una secuencia —
el propio MEN no las presenta como pasos sucesivos.

**Decisión:** se elimina la obligación de conectar puntos y la jerarquía
fundacional/intermedio/avanzado derivada de ella, para esta versión. Los
puntos quedan sueltos, tal como el MEN entrega las evidencias. La IA puede
proponer una conexión u orden, pero como **sugerencia**, nunca como estructura
garantizada; el docente decide si la usa.

La adaptabilidad del sistema no depende de un grafo pre-declarado: puede
ocurrir en vivo, según la evidencia que entrega el estudiante, sin necesitar
una jerarquía fija entre puntos.

**Consecuencia reconocida:** esto deja fuera del alcance de esta versión la
teoría de espacios de conocimiento (Doignon y Falmagne) como base directa de
la relación entre puntos — esa teoría depende de una estructura de
prerrequisitos que aquí se está retirando. No se descarta para siempre; se
retira para esta versión concreta.

**Reemplaza a:** ninguna (primera decisión registrada).

---

## ADR-002 — SOLO se retira como taxonomía de medición del diagnóstico

**Fecha:** 2026-08-05
**Estado:** aceptada; **acotada por ADR-008** (se retira el reporte de hipótesis de error nombrada).

**Contexto:** SOLO (Biggs & Collis) se adoptó para poder generar y defender
preguntas conectadas del banco de diagnóstico. Su definición original
clasifica la complejidad estructural de una respuesta **ya producida**,
ajustándose mejor a respuestas abiertas. Verificado contra la fuente: ninguno
de los formatos de interacción existentes en el sistema (`single_choice`,
`matching`, `ordering`, `fill_blank`, `short_text`) permite observar esa
estructura genuinamente — todos son de respuesta cerrada o comparada contra
texto esperado, no analizados por su estructura. Usar la etiqueta SOLO sobre
ellos afirmaba una medición que el sistema no hacía — mismo patrón que
Lineamientos (resumen sin fidelidad verificada) y EBC (normalización
genérica): un nombre con prestigio académico puesto sobre algo que no cumplía
su propia definición.

**Decisión:** se retira SOLO como taxonomía de medición del diagnóstico en
esta versión. El mecanismo real de diagnóstico pasa a ser el **distractor
mapeado a una hipótesis de error específica** — método validado en
inventarios de conceptos (ej. Force Concept Inventory, Hestenes et al. 1992),
aplicable a formatos de respuesta cerrada (ABCD, matching, ordering). La
hipótesis de error la propone la IA (marcada `generado_ia_no_curado`) y el
docente la confirma o corrige con su criterio de aula.

**Consecuencia reconocida:** la pregunta de cómo variar la profundidad o
dificultad *dentro* de un diagnóstico —que antes resolvía nominalmente
SOLO— queda abierta (ver QA-005). No se resuelve en esta decisión. El ajuste
del método de distractores tampoco es parejo entre áreas: más fuerte en
Matemáticas y Ciencias Naturales, más débil en Lenguaje y Ciencias Sociales,
donde el error discreto pesa menos que la interpretación.

**Reemplaza a:** ninguna decisión formal previa — SOLO nunca tuvo su propio
registro de decisión; se adoptó sin dejar rastro de por qué, que es parte del
problema original.

---

## ADR-003 — La Taxonomía de Bloom (revisada) reemplaza a SOLO para graduar profundidad

**Fecha:** 2026-08-06
**Estado:** **reemplazada por ADR-008** — Bloom queda sin función en el diagnóstico (QA-015).

**Contexto:** ADR-002 retiró SOLO sin proponer reemplazo (QA-005, QA-007),
porque necesitaba observar respuestas ya producidas y ninguno de los formatos
de interacción del sistema lo permite. Se necesitaba algo diseñado para
clasificar preguntas de **respuesta cerrada** desde su creación, no para
juzgar respuestas abiertas después. Verificado contra fuentes: la Taxonomía
de Bloom (revisada) sí está diseñada y validada para clasificar preguntas de
opción múltiple por nivel cognitivo — a diferencia de SOLO, este es su
propósito original, no un préstamo forzado.

**Decisión:** se adoptan cuatro niveles de Bloom —Recordar, Comprender,
Aplicar, Analizar— para graduar la profundidad de los ítems de diagnóstico y
práctica, reemplazando `target_solo`/N2-N3-N4-N5. Se excluyen los dos niveles
superiores (Evaluar, Crear): exigen defender un juicio o producir algo nuevo,
lo cual requiere respuesta abierta genuina — mismo límite que ya sacó a N5 de
SOLO.

Es un eje independiente del distractor con hipótesis de error: Bloom dice qué
tan exigente es la tarea; el distractor dice qué revela una respuesta
incorrecta específica. Se combinan, no compiten.

**Consecuencia reconocida:** ni siquiera Bloom garantiza que un ítem
"diseñado para Analizar" resulte empíricamente más difícil que uno "diseñado
para Comprender" — es heurístico y revisable, igual que todo lo demás en esta
versión. El docente, con su criterio, es quien confirma si el nivel asignado
tiene sentido; el sistema nunca lo asegura.

**Reemplaza a:** ninguna decisión formal — es la resolución de QA-005 y
QA-007, que quedan cerradas por esta decisión.

---

## ADR-004 — La práctica se pre-genera; el docente la revisa antes de que exista un estudiante

**Fecha:** 2026-08-07
**Estado:** aceptada; **diferida a v2 por ADR-007** (Práctica fuera de esta versión).

**Contexto:** QA-008 planteaba si tenía sentido generar y aprobar de
antemano todas las intervenciones de práctica posibles, en vez de generar en
vivo por estudiante — el universo de brechas por DBA es enumerable (pocas
evidencias, pocos errores conocidos por evidencia). La propuesta pasó por
tres correcciones de Alejandro antes de quedar clara:

1. Un primer borrador confundía "pre-generar" (decisión de arquitectura,
   posible ya) con "curar" (validación empírica de que las rutas funcionan
   con uso real — imposible hoy, no hay estudiantes usando el sistema
   todavía). Son dos cosas distintas; esta decisión resuelve solo la
   primera.
2. Un segundo borrador arrastraba sin querer la generación de ítems de
   diagnóstico al alcance de esta decisión. Diagnóstico es un momento
   aparte, anterior a práctica (ver Experiencia en el glosario) — no se
   decide aquí, solo se reconoce como dependencia externa.
3. Quedó sin claridad qué aportaba "el docente revisa antes de que el
   estudiante vea nada" si ese principio ya existía desde antes en el
   sistema — la respuesta es que pre-generar es lo que **crea la ventana**
   para esa revisión de una sola vez; sin pre-generar, no hay nada fijo que
   revisar antes del primer estudiante.

**Decisión:**

1. **¿Se pre-genera?** Sí.
2. **¿Qué entra?** Por cada combinación (punto de aprendizaje, hipótesis de
   error) que diagnóstico pueda entregar, una ruta de práctica ya generada
   de antemano — no en el momento en que un estudiante la necesita.
3. El docente revisa cada ruta **una sola vez**, antes de que cualquier
   estudiante la encuentre. Esto es posible gracias a que la ruta ya existe
   por pre-generación, no porque se agregue un paso nuevo de revisión al
   ciclo.

Se descartó un cuarto punto (fallback para el caso de un error de estudiante
sin ruta pre-generada que lo cubra): innecesario, siempre que diagnóstico
use solo formatos de respuesta **cerrada** (opción múltiple, emparejar,
ordenar). Con formato cerrado el conjunto de errores posibles es finito y
conocido de antemano — no existe la posibilidad de una respuesta sin
mapear. Verificado con Alejandro: la lógica se sostiene porque es
justamente la propiedad que hace "enumerable" el universo de brechas en
primer lugar.

**Consecuencia reconocida:** esta garantía de "sin fallback necesario" se
rompe si algún día se agregan formatos de respuesta libre (`fill_blank`,
`short_text`) al diagnóstico — un error en texto libre no siempre cae en
una hipótesis pre-mapeada. Si eso ocurre, este punto debe revisarse de
nuevo, no asumirse heredado. Además, "curar" en el sentido de validar con
uso real que las rutas pre-generadas funcionan sigue sin resolverse — no es
parte de esta decisión, requiere datos de estudiantes reales que no existen
todavía. Depende también de QA-006 (auditar los generadores de diagnóstico
duplicados): el catálogo de ítems/distractores debe curarse una vez para
que el universo de brechas sea de verdad enumerable, tal como asume el
punto 2.

**Reemplaza a:** ninguna — es la resolución de QA-008, que queda cerrada
por esta decisión.

---

## ADR-005 — El diagnóstico se genera al crear la experiencia; la IA sugiere el orden

**Fecha:** 2026-08-07
**Estado:** aceptada; **punto 2 reemplazado por ADR-024** (orden de las evidencias).

**Contexto:** al abrir "mecanismo de diagnóstico" se planteó, como primer
punto, si diagnóstico se genera en vivo por estudiante o de antemano. Un
primer intento de respuesta mezcló dos ideas distintas: pre-generar el
contenido de **toda la biblioteca** (inviable, sin presupuesto ni tiempo
para producir material de los 342 DBA de una vez) con pre-generar **una
experiencia concreta** cuando el docente la crea. Al separarlas, quedó
claro que biblioteca ya existe como catálogo oficial de DBA y evidencias
(dato del MEN, no generado por nosotros) — lo único que falta generar es
el contenido de la experiencia puntual que un docente decide crear, DBA
por DBA, bajo demanda.

Como segundo punto, se preguntó en qué orden el diagnóstico evalúa las
evidencias de un DBA, dado que son planas entre sí (ADR-001, sin jerarquía
de prerrequisito).

**Decisión:**

1. El diagnóstico de una experiencia se genera **una sola vez, en el
   momento en que el docente la crea** (elige el DBA que ancla la
   experiencia) — no en vivo por cada estudiante, no pre-generado para el
   catálogo completo de antemano. Es una propuesta de IA que el docente
   revisa y edita bajo su criterio, antes de que cualquier estudiante la
   vea. Mismo patrón de generación-única-revisión-única que ADR-004 le dio
   a práctica.
2. El orden en que se presentan las evidencias dentro de un diagnóstico lo
   **sugiere la IA**, estimando dificultad a partir del propio
   enunciado/evidencia del DBA — coherente con lo que el diagnóstico
   realmente mide (no se declara un punto "más fácil" si sus ítems reales
   no lo reflejan). El docente puede reordenar libremente.

**Consecuencia reconocida:** la dificultad estimada por IA es heurística y
revisable, igual que la clasificación por niveles de Bloom (ADR-003) —
nunca una garantía del sistema. Esta decisión resuelve **solo** el
momento de generación y el orden; no resuelve cuántos ítems hacen falta
por evidencia ni cuándo hay confianza suficiente para avanzar o enviar a
práctica — eso queda abierto como su propio bloque de investigación
(regla de confianza suficiente), pendiente de tratarse aparte por
requerir fuentes de evaluación adaptativa/psicométrica, no solo criterio
de diseño.

**Reemplaza a:** ninguna.

---

## ADR-006 — Regla operativa de formato por evidencia: `single_choice` por defecto

**Fecha:** 2026-08-07
**Estado:** aceptada

**Contexto:** QA-003 había dejado ejemplos sueltos de mapeo evidencia→
formato (`ordering` para secuencia, `matching` para relación/clasificación,
`single_choice` para discriminación), pero sin una regla operativa
aplicable a evidencias no vistas antes. Para construirla, se tomó una
muestra real de 8 evidencias limpias (evitando los 5 registros con bug de
extracción de QA-013), 2 por cada área curricular.

La muestra mostró que la mayoría de verbos —opera, reconoce, representa,
describe, explica, comprende, predice, indica, compara— no necesitan un
formato especial: encajan en `single_choice` con distractor mapeado a una
hipótesis de error. Esto no es una simplificación conveniente: coincide
con la práctica real del Force Concept Inventory (que prueba "explica" y
"predice" en física exclusivamente con opción múltiple) y con Haladyna
(*Developing and Validating Multiple-Choice Test Items*, referencia
estándar en diseño de ítems), que documenta que la opción múltiple puede
medir válidamente comprensión, aplicación y pensamiento crítico —no solo
reconocimiento simple— siempre que cada ítem se construya sobre un único
tipo de demanda cognitiva.

**Decisión:**

1. **Formato por defecto: `single_choice`** con distractor mapeado a
   hipótesis de error — cubre la gran mayoría de evidencias,
   independientemente de la complejidad del verbo.
2. **`matching`** cuando la evidencia relaciona explícitamente dos
   conjuntos finitos ("relaciona", "diferencia... de", "clasifica según",
   "distingue entre").
3. **`ordering`** cuando la evidencia es explícitamente secuencial o
   procedimental (pasos, orden temporal).

**Consecuencia reconocida:** no todas las evidencias caen limpiamente
aquí. En la misma muestra de verificación aparecieron 2 casos reales —no
error de datos— que resisten cualquier formato cerrado: evidencias de
producción creativa (Lenguaje 1° DBA-4: "expresa opiniones a través de
dibujos, caricaturas, canciones") y evidencias actitudinales/
disposicionales (Lenguaje 5° DBA-5: "asume una postura crítica y
respetuosa"). Ambas cayeron en Lenguaje, coherente con la sospecha ya
anotada en ADR-002 de que el método de distractor es más débil en esa
área. Estas evidencias quedan fuera del diagnóstico automático, según la
regla ya fijada en QA-012. Cuántas evidencias caen así, y en qué
proporción por área, sigue sin saberse — eso es exactamente lo que mide
el censo pendiente de QA-014.

**Reemplaza a:** ninguna — resuelve la parte pendiente de QA-003.

---

## ADR-007 — Esta versión se limita a Diagnóstico + Reporte; Práctica y Verificación quedan diferidas

**Fecha:** 2026-08-07
**Estado:** aceptada

**Contexto:** al construir la regla de confianza suficiente de
diagnóstico (siguiente pieza del mecanismo, todavía abierta) surgió una
pregunta más grande: diagnóstico, práctica y verificación no son
independientes entre sí — están acoplados en cascada. Práctica ya
depende del catálogo de brechas que diagnóstico produce (ADR-004,
"por cada combinación evidencia/hipótesis de error"), y verificación
depende de que se hayan atendido las evidencias intervenidas por
práctica. Diagnóstico sigue en diseño activo — hoy mismo se corrigió un
error real (ver QA-015, la aplicación de Bloom) — así que cualquier
cambio ahí se propagaría a práctica y de ahí a verificación. Diseñar los
tres módulos a la vez, sobre una base que todavía se mueve, arriesga
trabajo desperdiciado o decisiones incoherentes entre capas.

**Decisión:** esta versión del sistema se limita al ciclo
**Diagnóstico → Reporte**. Práctica y Verificación quedan fuera de
alcance — no se descartan, se **difieren** a una versión posterior, una
vez que Diagnóstico esté validado y estable. El diseño ya hecho para
práctica (ADR-004) sigue siendo válido y no se revierte; simplemente no
se construye todavía. Reporte, en esta versión, agrega solo lo que
Diagnóstico produce — no los tres momentos que se habían previsto
originalmente (esto deja sin objeto a QA-009 por ahora).

**Consecuencia reconocida:** el producto de esta versión es más chico de
lo que planteaba la visión original — un docente recibe un reporte de
brechas probables por evidencia, pero no una ruta de intervención
generada automáticamente; decidir qué hacer con esa información queda en
manos del docente. No es necesariamente una limitación grave —hay
herramientas de diagnóstico formativo reales que se quedan justo ahí—,
pero es un recorte de alcance real, no un detalle. `vision.md`,
`glosario.md` y `modelo-conceptual.md` se actualizan para reflejarlo
explícitamente, siguiendo el mismo principio de honestidad ya aplicado a
Unidad y a la curación de biblioteca.

**Reemplaza a:** ninguna — acota el alcance de Experiencia y Reporte tal
como estaban descritos en el glosario original; no contradice ninguna
decisión previa.

---

## ADR-008 — Mecanismo final de diagnóstico: detectar alcance por evidencia, no nombrar el error

**Fecha:** 2026-08-07
**Estado:** aceptada; **punto 3 reemplazado por ADR-016** (cantidad de ítems).

**Contexto:** el diseño del mecanismo de diagnóstico pasó por varias
correcciones en la misma sesión: se intentó usar Bloom como escalera de
profundidad por evidencia (error, corregido — ver QA-015, evidencias
tienen nivel fijo, no escalera); se propuso CRI (Certainty of Response
Index, Hasan et al. 1999) para distinguir acierto real de adivinanza; se
propuso construir un "mapa de hipótesis de error" por evidencia antes de
generar ítems. Al revisar esto último, surgió la pregunta de fondo: las
evidencias del MEN están redactadas para que el docente identifique **si
se alcanza o no** el aprendizaje (fuente ya citada en ADR-006: "las
evidencias... muestran a los maestros si se está alcanzando el
aprendizaje") — no para catalogar por qué falla un estudiante. El
catálogo de hipótesis de error solo tenía sentido como insumo de
Práctica (ADR-004: "por cada combinación evidencia/hipótesis, una ruta
de práctica"), y Práctica quedó fuera de esta versión (ADR-007). Sin ese
consumidor, mantener el mapa de hipótesis era complejidad sin uso real —
el mismo patrón ya identificado dos veces hoy con SOLO y con Bloom.

**Decisión:** el mecanismo de diagnóstico de esta versión es:

1. Por cada evidencia evaluable en formato cerrado (ADR-006, QA-012), se
   generan ítems con distractores **plausibles y bien construidos**
   (principio ya validado en ADR-002 y en Haladyna) — pero esos
   distractores **no se nombran ni se reportan como una hipótesis de
   error específica** en esta versión. Sirven para que el ítem discrimine
   bien, no para catalogar el error.
2. Cada respuesta se acompaña de una **certeza (CRI, escala 0-5)**. Un
   acierto con certeza baja no cuenta como evidencia fuerte de que el
   estudiante muestra la evidencia; un error con certeza baja no cuenta
   como evidencia fuerte de que no la muestra — ambos quedan como señal
   débil, no concluyente.
3. La cantidad de ítems por evidencia **no es fija**: se empieza con 1
   ítem; si el resultado es decisivo (certeza alta, en cualquiera de los
   dos sentidos), se detiene ahí; si es no concluyente, se agrega hasta 1
   ítem más sobre la misma evidencia (tope: 3 ítems), para no fatigar al
   estudiante encadenando preguntas indefinidamente sobre lo mismo (mismo
   principio ya usado en Verificación).
4. El resultado por evidencia, por estudiante, es uno de tres:
   **muestra la evidencia / no la muestra / no concluyente** — probable,
   nunca una certeza. Reporte agrega esto por grupo (ver ADR-007).

**Consecuencia reconocida:** esta decisión retira, para esta versión, la
parte de ADR-002 que proponía "el mecanismo real de diagnóstico" como
distractor-mapeado-a-hipótesis-nombrada. No se descarta el principio de
fondo (distractores plausibles siguen siendo mejor práctica de
construcción de ítems, validado en Haladyna y en el propio FCI) ni se
contradice ADR-002 en su totalidad — se acota su alcance: la hipótesis
de error deja de ser un dato que el sistema nombra y reporta, aunque el
distractor elegido sigue quedando registrado por si en una versión
futura, con práctica de vuelta en alcance (ADR-007), vale la pena
recuperarlo. Bloom (ADR-003) queda sin función en este mecanismo —
resuelve QA-015 en ese sentido: no hay escalera que graduar.

**Reemplaza a:** ninguna en su totalidad — acota el alcance de ADR-002
(retira el reporte de hipótesis nombrada, mantiene el principio de
distractor plausible) y resuelve QA-015 (Bloom no tiene función en el
mecanismo de diagnóstico de esta versión).

---

## ADR-009 — Cantidad y orden de ítems observados: control del docente; banco: número base del sistema

**Fecha:** 2026-08-07
**Estado:** **reemplazada** — punto 1 por ADR-016 (cantidad) y ADR-024 (orden); punto 2 por ADR-016 (banco de 12) y ADR-026 (se retira "pedir generar más").

**Contexto:** ADR-008 (punto 3) proponía una regla del sistema para
cuántos ítems ve un estudiante por evidencia, apoyada en la probabilidad
de adivinar (mínimo 2 aciertos seguidos, tope 4). Alejandro la consideró
débil incluso con esa justificación — sin datos reales de calibración,
ningún número que nosotros propongamos se puede defender con certeza. La
salida no es seguir buscando un número más convincente, sino reconocer
que esta decisión no nos corresponde a nosotros: el sistema ya le da al
docente autoridad sobre el orden de evidencias (ADR-005) y sobre el
contenido de los ítems — la misma autoridad debe extenderse a cuántos
ítems ve el estudiante y en qué orden. Lo que sí nos corresponde decidir
es un número distinto y más simple: cuánto generar por adelantado para
que el docente tenga con qué trabajar (el banco, ADR-005).

**Decisión:**

1. La cantidad de ítems que un estudiante ve por evidencia, y el orden en
   que se presentan, las decide el docente por completo — el sistema no
   propone número ni valor por defecto aquí. Misma autoridad que ya tiene
   sobre el orden de evidencias (ADR-005) y sobre el contenido de los
   ítems.
2. El banco de ítems generado por evidencia (al crear la experiencia,
   ADR-005) sí tiene un número base definido por el sistema: **6 ítems
   por evidencia** — margen práctico para que el docente elija, no una
   cifra con respaldo estadístico. El docente puede pedir generar más si
   lo necesita.

**Consecuencia reconocida:** esto no resuelve la falta de datos reales
sobre cuánta evidencia hace falta para confiar en un resultado — sigue
sin resolverse con certeza. Traslada la decisión correctamente: cuánto
generar es una decisión de ingeniería (nuestra); cuánto mostrar y en qué
orden es una decisión de aula (del docente). **Alejandro dejó constancia
de que considera el número base del banco (6) pobre/insuficiente**, pero
no lo bloqueó por no considerarlo urgente ahora — queda marcado como
revisable, no como acordado con firmeza.

**Reemplaza a:** ADR-008, solo en su punto 3 (cantidad fija de ítems
observados). Los puntos 1 (distractores plausibles), 2 (CRI) y 4
(resultado muestra/no muestra/no concluyente) de ADR-008 siguen vigentes.

---

## ADR-010 — Mecanismo de Reporte: dos vistas, clasificación por umbral, sin texto generado

**Fecha:** 2026-08-07
**Estado:** aceptada; **punto 3 reemplazado por ADR-013** (umbrales). Punto 4 (vista de aula) diseñado en `14-spec` y `27-spec`.

**Contexto:** Reporte tenía descripción (glosario) pero no mecanismo. Su
único insumo en esta versión es lo que Diagnóstico produce (ADR-007,
ADR-008): por estudiante, por evidencia, uno de tres estados —muestra,
no muestra, no concluyente—, nunca una hipótesis de por qué. Cualquier
mecanismo de Reporte tiene que construirse sobre esos tres estados
exactamente, sin inventar más de lo que hay.

**Decisión:**

1. **Vista principal (grupo × evidencia):** por cada evidencia del DBA,
   estadística agregada de cuántos estudiantes caen en cada uno de los
   tres estados. Esta es la vista que justifica Reporte — la que un
   docente con 30-40 estudiantes no puede armar a mano.
2. **Clasificación por umbral, no texto generado por IA:** cada evidencia
   se etiqueta según la proporción del grupo en cada estado —por ejemplo,
   "brecha extendida" (la mayoría no muestra), "brecha aislada" (pocos
   estudiantes), "sin brecha aparente", "datos insuficientes" (muchos no
   concluyentes)— calculada, no redactada por IA. Se descarta
   deliberadamente que la IA genere una "recomendación" en texto libre:
   ya se vio hoy, más de una vez (SOLO, Bloom, hipótesis de error
   nombrada), qué pasa cuando el sistema afirma algo que los datos no
   respaldan; un texto generado del estilo "se recomienda reforzar..."
   corre el mismo riesgo, inventando una causa que el sistema no tiene.
3. **Los umbrales que definen "mayoría"/"pocos" los ajusta el docente**,
   no el sistema — mismo patrón y misma razón que ADR-009 (no hay datos
   para defender un corte universal).
4. **Vista de estudiantes (aula), separada de la principal:** listado del
   grupo con detalle por estudiante — qué material/ítems vio y su estado
   por evidencia. Es historial dentro de la experiencia, no agregado. Se
   consideró incluir aquí el concepto de "ciclos", pero se descarta: ese
   término pertenece al estado de práctica/verificación (repetición a lo
   largo del tiempo), que están fuera de esta versión (ADR-007) — no hay
   ciclos que registrar todavía.

**Consecuencia reconocida:** la idea de que el estudiante pueda repetir
el diagnóstico varias veces en el tiempo (no solo una vez) quedó
mencionada como razonable pero fuera de esta versión — mismo tipo de
pendiente que ya tiene Verificación (repetición espaciada). No se pierde,
queda para cuando se revise ese alcance.

**Reemplaza a:** ninguna — es la primera decisión de mecanismo para
Reporte.

---

## ADR-011 — El "ejemplo" del DBA se usa como contexto de generación, no como ítem ni como material pasivo

**Fecha:** 2026-08-07
**Estado:** aceptada

**Contexto:** el DBA tiene tres partes oficiales — enunciado, evidencias,
ejemplo (glosario, DBA) — y solo las dos primeras tenían rol asignado
(QA-011). Antes de decidir, se verificó contra los 4 documentos oficiales
ya extraídos localmente si el ejemplo era mayormente texto o imagen —
sospecha de Alejandro. Resultado: en su gran mayoría es texto real
describiendo una actividad concreta y contextualizada (ej. "a partir de
una colección de objetos cotidianos..."), no imágenes — menciones
explícitas de figuras fueron rara excepción (2 a 8 casos, contra 21 a 115
secciones de ejemplo, según el área). El propio MEN explica su función:
"los ejemplos muestran lo que el niño debe estar en capacidad de hacer...
pueden ser contextualizados... según su región, características
étnicas".

**Decisión:** el ejemplo se usa como **contexto/escenario para la
generación de ítems de diagnóstico** de las evidencias de ese DBA — no
se convierte directamente en un ítem (no está redactado como pregunta
con respuesta correcta, es una escena) y no se limita a material pasivo
solo visible para el docente (desperdiciaría un escenario ya validado y
contextualizado por el MEN). Al generar un ítem para una evidencia, el
ejemplo del DBA se ofrece como escenario de referencia, para que la IA
no invente un contexto genérico o descontextualizado desde cero.

**Consecuencia reconocida:** esta decisión define el rol, pero no lo
habilita todavía — el campo "ejemplo" no existe hoy en
`curriculo_men_normalizado.json` (la normalización actual no lo capturó).
Usarlo en la práctica depende de que se extienda esa extracción, misma
naturaleza de dependencia que QA-006 y QA-013 — trabajo de datos, no de
diseño, pospuesto hasta que exista la UI para revisarlo.

**Reemplaza a:** ninguna — resuelve QA-011.

---

## ADR-012 — Se construye de nuevo el backend de diagnóstico/reporte; no se adapta el existente

**Fecha:** 2026-08-07
**Estado:** aceptada

**Contexto:** QA-006 pedía auditar el código de generación de diagnóstico
antes de tocar nada nuevo. La auditoría (sobre `ia_service.py`,
`interaction_evidence_planner.py` y los routers que los conectan)
encontró:

1. **Dos generadores de diagnóstico activos**, alternados en tiempo real
   por la variable de entorno `DIAGNOSTIC_GENERATION_STRATEGY` (default
   `"staged"`): la estrategia `"unified"` usa terminología SOLO literal
   ("Uniestructural", "Multiestructural", "Relacional"), un grafo de
   prerrequisitos fundacional/intermedio/avanzado, y genera 21 preguntas
   por "punto de aprendizaje" — el modelo exacto que ADR-001 y ADR-002 ya
   retiraron, no una variación menor. La estrategia `"staged"` usa varios
   `interaction_type` vía `interaction_evidence_planner.py`, pero sigue
   atada a SOLO y a "subtema" inventado por IA, no a evidencia oficial.
2. `generar_preguntas_n5_opcionales` es código simulado — comentario
   propio: "Mock: retornar estructura sin hacer llamada a Gemini (para
   test)" — no ejecuta nada real pero está mezclado como si lo hiciera.
3. `interaction_evidence_planner.py` sí contiene una idea reutilizable:
   reglas por patrón de texto (secuencia → `ordering`, relación →
   `matching`, etc.) para elegir formato — conceptualmente cercana a
   ADR-006, aunque incluye formatos abiertos ya descartados (QA-012) y
   depende de SOLO/subtema, no de evidencia oficial.

El acoplamiento a SOLO y al grafo de prerrequisitos está en el texto
mismo de los prompts, no es superficial — adaptar exigiría reescribir la
lógica de todos modos. Alejandro había elegido "construir de nuevo" por
instinto (código grande y desorganizado) antes de que esta auditoría
terminara; los hallazgos confirman esa elección con evidencia concreta,
no la contradicen.

**Decisión:** el backend de diagnóstico y reporte de esta versión se
construye nuevo — no se adaptan `_generar_preguntas_diagnostico_unificado`
ni `generar_preguntas_diagnostico_por_etapas`. Se reutiliza, revisando
caso por caso (no copiando literal): infraestructura no específica de
diagnóstico (autenticación, modelos de Curso/Experiencia/Inscripción,
pipeline de datos curriculares) y la **idea** del planner de interacción
por patrones de texto de `interaction_evidence_planner.py`, adaptada a
evidencia oficial y sin formatos abiertos.

**Consecuencia reconocida:** más trabajo inicial que adaptar, a cambio de
evitar heredar acoplamiento a un modelo ya retirado y código simulado
mezclado con código real, sin que nadie lo note a tiempo.

**Reemplaza a:** ninguna — resuelve QA-006.

---

## ADR-013 — Los umbrales de clasificación del Reporte los fija el sistema, no el docente, en esta versión

**Fecha:** 2026-08-18
**Estado:** aceptada; **modificada por ADR-017** (categorías) **y ADR-023** (qué cuenta como datos insuficientes); **precisada por ADR-032**.

**Contexto:** ADR-010 (punto 3) dejaba los umbrales que separan
"mayoría"/"pocos" en manos del docente, mismo patrón que ADR-009 usó
para la cantidad de ítems observados — la razón entonces era "no hay
datos para defender un corte universal". Al construir el modelo
entidad-relación de esta versión, surgió la pregunta de dónde
persistiría esa elección si fuera configurable, y no había ninguna
decisión sobre eso. En vez de agregar una tabla o un campo nuevo solo
para guardar una preferencia que todavía no sabemos si un docente real
necesita ajustar, se decidió no construir esa configurabilidad en esta
versión.

**Decisión:** los umbrales del Reporte quedan fijos, definidos por el
sistema, no ajustables por el docente en esta versión:

1. **Datos insuficientes**: 40 % o más de los resultados de una
   evidencia son "no concluyente".
2. Si no aplica lo anterior, sobre los resultados restantes (muestra +
   no muestra):
   - **Brecha extendida**: 50 % o más no muestra la evidencia.
   - **Brecha aislada**: entre 1 % y 49 % no muestra la evidencia.
   - **Sin brecha aparente**: nadie (o prácticamente nadie) no muestra
     la evidencia.

Con umbrales fijos, no hace falta ninguna tabla ni campo nuevo para
persistir una preferencia del docente — se calcula en el momento,
igual para todas las experiencias.

**Consecuencia reconocida:** estos números son simples y redondos, sin
respaldo estadístico — mismo tipo de decisión de ingeniería que el
banco base de 6 ítems (ADR-009), revisable si en el futuro se decide
permitir que el docente los ajuste. Esta decisión no significa que
ajustar umbrales sea mala idea permanentemente — se difiere a una
versión posterior, igual que Práctica y Verificación (ADR-007), no se
descarta.

**Reemplaza a:** ADR-010, solo en su punto 3 (umbrales ajustables por
el docente). Los puntos 1, 2 y 4 de ADR-010 siguen vigentes.

---

## ADR-014 — El contenido del Ítem se modela con un enunciado propio y una entidad Opción, para representar sus tres formatos cerrados

**Fecha:** 2026-08-19
**Estado:** aceptada; **atributo `distractor` reemplazado por ADR-020**.

**Contexto:** al construir el modelo entidad-relación se verificó que
ningún documento de diseño (glosario, decisiones, modelo conceptual)
define el contenido propio de un Ítem — el enunciado de la pregunta y
sus opciones de respuesta. ADR-005 confirma que el diagnóstico se genera
y se persiste para que el docente lo revise antes de que un estudiante lo
vea, lo cual exige que ese contenido se almacene en alguna parte; sin
embargo, la estructura de datos nunca se decidió. Los tres formatos
cerrados de esta versión (ADR-006: `single_choice`, `matching`,
`ordering`) necesitan una lista de opciones, pero de forma distinta:
`single_choice` necesita saber cuál opción es correcta; `ordering`
necesita saber el orden correcto de las opciones; `matching` necesita
saber qué opción de un grupo corresponde a cuál del otro.

**Decisión:**

1. Ítem incorpora el atributo `enunciado` — el texto de la pregunta,
   necesario en los tres formatos.
2. Se crea la entidad **Opción**, con cardinalidad 1 a N desde Ítem (un
   ítem tiene varias opciones): `id`, `texto`, `orden`, `es_correcta`,
   `grupo`.
   - `orden` cumple dos roles según el formato: posición de presentación
     (`single_choice`), o posición en la secuencia correcta (`ordering`).
   - `es_correcta` marca la opción correcta en `single_choice`; en
     `ordering` y `matching` no se usa de la misma forma.
   - `grupo` solo aplica a `matching` — identifica si la opción
     pertenece a la columna izquierda o derecha; dos opciones de
     distinto grupo con el mismo `orden` forman la pareja correcta.
3. Esta estructura es deliberadamente genérica: cubre los tres formatos
   con las mismas columnas, en vez de crear una tabla distinta por
   formato, a costa de que algunos campos queden sin uso según el caso.

**Consecuencia reconocida:** es una decisión de diseño nueva, tomada
durante la construcción del MER, no heredada de un ADR anterior — el
vacío existía desde antes y no había sido detectado. Es un diseño mínimo
suficiente para el modelo entidad-relación; si alcanza para representar
bien un ítem de `matching` complejo en la implementación real, queda por
probarse — no se afirma como validado empíricamente.

**Reemplaza a:** ninguna — es la primera decisión sobre el contenido
propio del Ítem.

---

## ADR-015 — Ítem incorpora el atributo `excluido`, para que "descartar" un ítem sea persistente y no solo un estado visual

**Fecha:** 2026-08-21
**Estado:** aceptada; **ampliada por ADR-026** (el docente también agrega preguntas; el banco se congela al publicar).

**Contexto:** al diseñar la pantalla de revisión del banco de preguntas
y ejercicios (Fase II, Diseño Multimedial —
`12-spec-modal-banco-items.md`), se definió que el docente necesita
poder sacar un ítem generado por IA de lo que el estudiante va a ver,
sin borrarlo de la base de datos. Se consideró "eliminar" (borrar el
Ítem para siempre), pero se descartó: no encaja con una pantalla de
revisión (el docente decide qué se publica, no limpia la base de
datos), y hubiera necesitado su propio modal de confirmación por ser
irreversible. "Descartar" — reversible, de bajo riesgo mientras el
banco no está publicado — fue la decisión tomada en su lugar. Para que
ese estado se recuerde después de cerrar y reabrir el modal, y no sea
solo un estado visual de la sesión, Ítem necesita guardarlo.

**Decisión:** Ítem incorpora el atributo `excluido` (booleano, por
defecto `falso`). Cuando es verdadero, el ítem no se muestra al
estudiante durante el diagnóstico, aunque sigue existiendo en el banco
— el docente puede volver a incluirlo en cualquier momento (revertir a
`falso`), sin límite de tiempo ni de intentos.

**Consecuencia reconocida:** esta decisión se toma durante Fase II
(Diseño Multimedial), no durante Fase III (Diseño Computacional) —
todavía no se refleja en `01-modelo-entidad-relacion.md`, que se
reconstruye cuando se retome Fase III con todas las decisiones
acumuladas hasta ese momento, esta incluida. Mismo patrón que ADR-014
(Opción): un vacío real detectado al diseñar la pantalla, no al
revisar el modelo en abstracto — documentado aquí primero, incorporado
al MER formalmente después.

**Reemplaza a:** ninguna — es la primera decisión sobre el estado de
exclusión de un Ítem.

---

## ADR-016 — Cantidad de ítems por evidencia: regla fija por sistema, mínimo 4 / tope 6, con fundamento en literatura de mastery testing

**Fecha:** 2026-08-21
**Estado:** aceptada; **precisada por ADR-031** (corte de certeza, mayoría exacta, selección del ítem siguiente).

**Contexto:** al diseñar Reporte se detectó que ADR-009 dejó la
cantidad de ítems que un estudiante ve por evidencia como decisión del
docente ("el sistema no propone número ni valor por defecto"), pero
nunca se construyó —ni se planeó— ninguna interfaz donde el docente
pudiera ejercer esa decisión. Es una responsabilidad asignada sin forma
de cumplirla.

Al revisar alternativas, surgieron dos preguntas de fondo: (1) si tiene
sentido mantener un mecanismo *adaptativo* (parar antes si la señal ya
es clara) ahora que SOLO —origen histórico de la idea de "adaptativo"
en el proyecto— ya fue retirado (ADR-002); y (2) si un solo ítem, por
alta que sea su certeza reportada, es una base suficiente para concluir
algo (objeción real: un estudiante puede adivinar y reportar certeza
alta sin que sea honesto, o sin ser preciso en su autoevaluación).

Sobre (1): lo adaptativo de ADR-008 punto 3 nunca dependió de SOLO —es
una lógica distinta, basada en certeza (parar cuando la señal ya es
confiable), no en dificultad progresiva (subir de nivel si el
estudiante responde bien, que sí era la lógica de SOLO). Las dos ideas
son independientes; retirar SOLO no invalida la primera.

Sobre (2): se buscó una base defendible en literatura real de mastery
testing / pruebas criterio-referenciadas, en vez de fijar un número a
ojo. Se consideró primero el SPRT (Sequential Probability Ratio Test,
Wald 1945), la herramienta formal para este problema exacto, pero se
descartó implementarlo con rigor real en esta versión: requiere
parámetros de ítem calibrados con datos reales de estudiantes, que este
proyecto no tiene todavía — implementarlo sin esos datos sería fingir
un rigor que no existe, el mismo error ya cometido antes con SOLO y con
Bloom. En su lugar, se adoptó un rango práctico ampliamente citado en
la literatura clásica de pruebas criterio-referenciadas: Shrock &
Coscarelli (*Criterion-Referenced Test Development*) recomiendan 4 a 6
preguntas por objetivo; una fuente independiente (EBSCO Research
Starters, sobre pruebas criterio-referenciadas) recomienda al menos 5
por concepto cuando la prueba tiene consecuencias reales — nuestro
caso, porque el resultado alimenta el Reporte que el docente usa para
decidir. Ambas fuentes coinciden en el mismo rango.

**Decisión:**

1. La cantidad de ítems que un estudiante responde por evidencia la fija
   el **sistema**, no el docente — revierte ese punto de ADR-009 (sin
   interfaz para ejercerla, no tiene sentido dejarla como decisión
   ajena). Mismo patrón que ADR-013 (umbrales de Reporte, fijos por
   sistema en esta versión).
2. Regla adaptativa por certeza (mantiene el principio de ADR-008 punto
   3, con números revisados): **mínimo 4 ítems siempre** — ninguna
   conclusión se basa en menos de 4 respuestas, sin importar qué tan
   decisiva parezca la primera. A partir del ítem 4, si hay mayoría de
   señales fuertes en una misma dirección (ADR-008 punto 2, sigue
   vigente: acierto+certeza alta = señal fuerte "muestra"; error+certeza
   alta = señal fuerte "no muestra"; certeza baja = señal débil,
   cualquiera sea el resultado), se detiene y concluye esa dirección. Si
   no hay mayoría clara, continúa hasta el **tope de 6**. Al llegar a 6
   sin mayoría clara, concluye "no concluyente".
3. El banco de ítems por evidencia (ADR-009, generado al crear la
   experiencia) sube de 6 a **12** — dos veces el tope de esta regla,
   con margen para que el docente descarte o edite varios (ADR-015) y
   aun así queden suficientes.

**Consecuencia reconocida:** el rango 4-6 es un punto de partida
defendible —tomado de fuentes reales, no inventado— pero no es una
calibración estadística hecha para AdaptiveLearn específicamente; eso
requiere datos reales de estudiantes que no existen todavía. Queda
marcado como revisable cuando existan, igual que el resto de números
sin respaldo estadístico propio de esta versión (banco base, umbrales
de Reporte). El SPRT queda como candidato real para una versión futura,
una vez haya datos para calibrarlo con honestidad.

**Reemplaza a:** ADR-009, en su punto sobre quién decide la cantidad de
ítems (pasa de "el docente" a "el sistema, con esta regla"); el punto 2
de ADR-009 (banco base de ítems) también se actualiza, de 6 a 12. ADR-008
puntos 1, 2 y 4 siguen vigentes sin cambios; el punto 3 de ADR-008 queda
formalmente reemplazado por esta decisión (ya lo estaba parcialmente por
ADR-009; esta decisión lo completa con números revisados y fuente real).

---

## ADR-017 — Clasificación de brecha en Reporte simplificada a 3 categorías, con nombres que no declaran más certeza de la que hay

**Fecha:** 2026-08-21
**Estado:** aceptada; **precisada por ADR-032** (cortes exactos, sin "~").

**Contexto:** al diseñar la pantalla de Reporte (Ventana 010) se
cuestionó si las 4 categorías de ADR-013 (Datos insuficientes, Brecha
extendida, Brecha aislada, Sin brecha aparente) eran necesarias, dado
que la sección "Resultados generales" de esa misma pantalla ya muestra
los 3 estados base (Muestra, No muestra, No concluyente) sin necesitar
una cuarta categoría. Al revisar cómo se construyen las 4 categorías,
se confirmó que no son una simple renombrada de esos 3 estados: son un
cálculo derivado — una comprobación de suficiencia de datos, más una
división en 3 franjas de severidad sobre la proporción de "no
muestra". Esa división de severidad (extendida ≥50% vs. aislada
1%-49%) resultó ser la parte menos fundamentada del diseño original —
un corte redondo, sin respaldo estadístico, del mismo tipo ya
reconocido antes en este proyecto (banco de ítems, tope adaptativo).

Además, se revisó el nombre que iba a reemplazar la fusión de
"extendida"/"aislada" — "Brecha detectada" — contra el principio ya
aplicado en todo el proyecto de no declarar más certeza de la que el
dato sostiene (ADR-008: "probable, nunca una certeza"). "Detectada"
suena a confirmado; no calzaba con el matiz que ya tenía su opuesto,
"Sin brecha **aparente**".

**Decisión:**

1. Se simplifica de 4 a 3 categorías, eliminando la división de
   severidad entre "Brecha extendida" y "Brecha aislada":
   - **Datos insuficientes** — igual que ADR-013 (≥40% no concluyente).
   - **Brecha aparente** — cualquier proporción de "no muestra" mayor a
     ~0% entre los resultados definidos (reemplaza "Brecha extendida" +
     "Brecha aislada" combinadas).
   - **Sin brecha aparente** — igual que ADR-013 (~0% no muestra).
2. La categoría de la brecha usa el mismo matiz que su opuesto —
   "aparente" en los dos, no "detectada" — para que ningún nombre de
   los 3 afirme más de lo que el diagnóstico, con tan pocos ítems por
   evidencia (ADR-016: mínimo 4, tope 6), puede sostener con
   honestidad.

**Consecuencia reconocida:** se pierde la distinción entre una brecha
"aislada" (pocos estudiantes) y una "extendida" (la mayoría) — el
docente ya no ve esa diferencia en el badge, solo en los números
crudos de la card (que siguen mostrando el detalle completo, formato
`X/total`). Es un cambio deliberado hacia menos precisión afirmada, no
menos información disponible — los números siguen ahí.

**Reemplaza a:** ADR-013, en su división de severidad (los puntos de
"Brecha extendida"/"Brecha aislada" se funden en una sola categoría) y
en el nombre de esa categoría. El umbral de "Datos insuficientes" y de
"Sin brecha aparente" (ADR-013) siguen vigentes sin cambios.

---

## ADR-018 — Mecanismo de "Resultados generales": veredicto por DBA, agregando evidencias por estudiante

**Fecha:** 2026-08-24
**Estado:** aceptada; **modificada por ADR-022** (4.º estado y regla de precedencia).

**Contexto:** al escribir la sección "Resultados generales" de Reporte
(Ventana 010, `13-spec-modal-reporte.md`, sección 2.2) se definió su
texto y su forma visual (3 cards, conteo de estudiantes en formato
`X/total`) sin definir el mecanismo que las produce. Al revisar
ADR-010 (el que formalizó el mecanismo de Reporte) se confirmó que
esta sección no corresponde a ninguna de las 2 vistas que ese ADR
define: la vista principal es agregada **por evidencia** (cuántos
estudiantes en cada estado, evidencia por evidencia — eso es la
sección 2.3, no la 2.2), y la vista de estudiantes/aula es un
historial por estudiante, todavía sin construir. Faltaba una regla
real: cómo se combinan, para un mismo estudiante, sus N resultados
por evidencia (uno de muestra/no muestra/no concluyente por cada
evidencia del DBA) en un solo veredicto por DBA.

El propio MEN da fundamento para que tenga sentido un veredicto
agregado, no solo por evidencia — `dba_matematicas_v2.txt` (líneas
204-207) dice, sobre las evidencias de un DBA: "Algunas de ellas
podrán observarse más rápido; otras exigen un proceso más largo, pero
**todas en su conjunto buscan dar pistas adecuadas del aprendizaje
expresado en el enunciado**." Ninguna evidencia certifica el
aprendizaje por sí sola — es el conjunto el que da la pista. Pero esa
cita no dice cómo combinarlas: no da una fórmula ni una ponderación.

**Decisión:** regla de todo-o-nada, deliberadamente conservadora
(mismo criterio epistémico de ADR-008 — nunca declarar más certeza de
la que hay), con las 3 evidencias de peso igual entre sí:

- **Muestra** (a nivel DBA) ⟺ **todas** las evidencias de ese
  estudiante son "muestra". Si falta una sola, el conjunto no está
  completo.
- **No muestra** ⟺ **al menos una** evidencia de ese estudiante es "no
  muestra" — basta una señal fuerte en contra para no poder afirmar
  que el aprendizaje completo está alcanzado; no se promedia lo malo
  con lo bueno.
- **No concluyente** ⟺ ninguna evidencia es "no muestra", pero al
  menos una es "no concluyente" (el resto son "muestra") — no hay nada
  en contra, pero falta certeza en al menos una pieza.

**Consecuencia reconocida:** la cita del MEN ("algunas se observan más
rápido, otras exigen un proceso más largo") sugiere que no todas las
evidencias son necesariamente iguales en dificultad o en cuánto
informan del aprendizaje — pero el texto no lo afirma directamente
para efectos de evaluación, y el sistema no tiene, en esta versión,
datos para decidir qué evidencia "pesa más" (mismo problema de falta
de fundamento ya reconocido en ADR-009 y en el rechazo de SPRT
completo en ADR-016). El docente sí podría tener ese criterio por
contexto propio — de hecho ADR-005 ya le da control sobre el **orden**
de presentación por esa misma razón. Ponderar evidencias por
importancia queda como dirección válida para una versión futura, donde
el docente tenga más protagonismo sobre el sistema, pero no se
implementa ahora.

**Reemplaza a:** ninguna — ADR-010 dejó esta agregación sin definir;
esto la completa, no la contradice.

---

## ADR-019 — Respuesta_Opción: entidad para registrar qué eligió el estudiante, no solo si acertó

**Fecha:** 2026-08-25
**Estado:** aceptada

**Contexto:** al construir el modelo entidad-relación con todo lo
acumulado hasta ahora, se verificó `Respuesta` (ADR-008 punto 2, ADR-014)
contra los tres formatos reales de Ítem (ADR-006: `single_choice`,
`matching`, `ordering`) y la estructura de `Opción` (ADR-014: `id`,
`texto`, `orden`, `es_correcta`, `grupo`). El resultado: `Respuesta` solo
guarda `certeza` y `correcta` — ninguna columna conecta una Respuesta con
la o las Opciones que el estudiante efectivamente eligió. Para
`single_choice` esto ya es un vacío (se pierde cuál distractor
específico escogió, si fue el caso); para `matching` y `ordering` es más
grave — no hay ninguna forma de registrar qué emparejó o en qué orden
puso las opciones, solo si el resultado final fue correcto. Confirmado
también, como segunda fuente, en el modelo entidad-relación de un
compañero de curso, que ya resuelve esto con una entidad asociativa
equivalente — coincide con el vacío detectado por razonamiento propio,
no es la única razón.

**Decisión:**

1. Se crea la entidad **Respuesta_Opción**, con PK compuesta
   `(id_respuesta, id_opcion)` — una fila por cada Opción que una
   Respuesta involucró.
2. Atributo `valor_dado` (entero), con significado según el formato del
   Ítem — mismo criterio de "campo compartido, uso distinto por formato"
   ya aceptado en `Opción.orden` (ADR-014):
   - `single_choice`: sin uso — la existencia de la fila ya es la
     elección (una sola fila por Respuesta).
   - `ordering`: la posición que el estudiante le asignó a esa opción.
   - `matching`: un número de pareja asignado por el estudiante,
     compartido por las 2 opciones que emparejó entre sí.
3. `Respuesta.correcta` pasa a ser un valor **derivado** — se calcula
   comparando las filas de Respuesta_Opción contra `es_correcta`/`orden`/
   `grupo` de las Opciones reales, no se guarda de forma independiente.

**Consecuencia reconocida:** esta decisión no resuelve cómo se
implementa exactamente la comparación que deriva `correcta` — queda
como trabajo de implementación, no de este modelo. Tampoco persiste una
"hipótesis de error percibida" del estudiante — solo registra qué
eligió; cruzarlo con la hipótesis de error de la Opción (ver ADR-020)
es lo que permitiría, en una versión futura con Práctica de vuelta en
alcance (ADR-007), saber qué error específico cometió cada estudiante.

**Reemplaza a:** ninguna directamente — completa un vacío estructural
que ADR-014 dejó abierto sin notarlo. No contradice ADR-008 puntos 2 y
4 (certeza, resultado por evidencia siguen vigentes sin cambios).

---

## ADR-020 — La hipótesis de error se modela por Opción, no por Ítem

**Fecha:** 2026-08-25
**Estado:** aceptada

**Contexto:** ADR-008 (2026-08-07, punto 1) habla de "el distractor
elegido" en singular, asumiendo implícitamente un distractor por Ítem
— pero esa decisión es **12 días anterior** a ADR-014 (2026-08-19), que
introdujo la entidad Opción precisamente porque un Ítem de
`single_choice` tiene **varias** opciones incorrectas, no una. Las dos
decisiones nunca se reconciliaron: el modelo entidad-relación seguía
cargando `distractor` como atributo único de Ítem, incapaz de
distinguir cuál de las N opciones incorrectas representa qué error
específico — contradice directamente a ADR-002 y ADR-006, que hablan de
distractores **plurales**, cada uno construido para representar un
error plausible distinto (principio de Haladyna y del Force Concept
Inventory). Verificado también, como segunda fuente, contra el modelo
del compañero, que ya lo ubica en Opción — coincide con la
inconsistencia encontrada por revisión propia de ADR-008 vs. ADR-014,
no es la única razón.

**Decisión:** se retira el atributo `distractor` de Ítem; se agrega
`hipotesis_error` (texto, nulo si la opción es correcta o si todavía no
se le asignó una) a **Opción** — cada opción incorrecta puede llevar su
propia hipótesis de error interna, independiente de las demás opciones
del mismo Ítem. La restricción de ADR-008 punto 1 sigue vigente sin
cambios: este dato **nunca se nombra ni se reporta** al docente o al
estudiante en esta versión — cambia dónde vive el dato dentro del
modelo, no su visibilidad.

**Consecuencia reconocida:** ningún spec de Fase II ya cerrado expone
este campo hoy — verificado directamente contra
`12-spec-modal-banco-items.md` (el InfoBlock de Opciones del modal de
banco de ítems no muestra `hipotesis_error` en ninguno de los dos
modos, lectura ni edición) — así que esta decisión no rompe ninguna
pantalla ya diseñada.

**Reemplaza a:** ADR-014, solo en el atributo `distractor` de Ítem (se
retira, se reemplaza por `hipotesis_error` en Opción); el resto de
ADR-014 (estructura de Opción, roles de `orden`/`es_correcta`/`grupo`)
sigue vigente sin cambios. Aclara ADR-008 punto 1: la restricción de no
reportar sigue vigente, ahora aplicada al nivel de granularidad
correcto (por opción, no por ítem).

---

## ADR-021 — Los valores derivados del diagnóstico se persisten como fotografía, no se recalculan al vuelo

**Fecha:** 2026-08-26
**Estado:** aceptada

**Contexto:** al construir el Modelo Relacional
(`fase-3-diseno-computacional/04-modelo-relacional.md`) se detectó una
contradicción real en un primer borrador de ese documento. El MER marca
`Resultado.estado` y `Respuesta.correcta` como **derivados** (se
calculan, no se capturan del usuario) y dejó explícitamente abierto si
se persisten o no: *"Si además se persiste como fotografía, falta la
marca de cuándo se calculó (V-4)"*. El borrador del MR resolvió ese
vacío por su cuenta, recomendando **no** persistirlos —implementarlos
como vista o columna calculada— con el argumento de que así RI-11 (que
el valor guardado coincida con el recálculo) quedaba satisfecha por
construcción, sin nada que sincronizar.

Al revisarlo, ese argumento resultó incoherente en el caso de
`Resultado`: `estado` es su **único atributo no-clave**. Si no se
persiste, no queda una tabla con una columna calculada — no queda tabla
en absoluto, queda una vista. Y eso contradice al propio MER, que
declara a Resultado **entidad débil** y distingue ese concepto
explícitamente de "vista derivada" (marca así a Reporte, y no a
Resultado). Además Resultado perdería sus llaves foráneas y el
mecanismo de RI-4, que es justamente su llave primaria compuesta.

**Decisión:**

1. **`Resultado.estado` se persiste** como columna real. Resultado
   sigue siendo una tabla y una entidad débil, tal como el MER la
   declara.
2. **Resultado incorpora `fecha_calculo`** (fecha/hora). No es un
   agregado opcional: es la consecuencia obligatoria de persistir una
   fotografía — un estado guardado sin saber de cuándo es, no es
   auditable. Esto cierra V-4.
3. **`Respuesta.correcta` también se persiste**, por el mismo criterio.
   No necesita marca de tiempo propia: una Respuesta corresponde a un
   único evento (el momento en que el estudiante respondió), y la falta
   de esa marca ya está declarada aparte como V-1, sin cambios.

**Por qué persistir y no recalcular, más allá de la incoherencia
estructural:** (a) la regla de cálculo es versionable y ya cambió una
vez —ADR-016 reemplazó a ADR-009 en cuántos ítems se observan—, y un
resultado histórico no debe mutar retroactivamente porque la regla
cambió después; (b) V-2 sigue abierto (nada impide editar una Opción
después de que existan Respuestas), y con recálculo al vuelo esa edición
cambiaría en silencio resultados ya emitidos, incluyendo los que un
docente ya vio en su Reporte.

**Consecuencia reconocida:** RI-11 deja de estar "resuelta por
construcción" y pasa a ser una obligación activa — el valor persistido
debe escribirse en el mismo momento del cálculo y no volver a tocarse;
si algo lo invalida, se recalcula explícitamente, no en silencio. Esto
sube la prioridad de V-2: mientras editar una Opción con Respuestas
reales siga permitido, existe la posibilidad de que un `correcta`
persistido quede históricamente desalineado de la Opción que hoy se lee
en pantalla. V-2 no se resuelve aquí, pero deja de ser un detalle
teórico.

**Reemplaza a:** ninguna — resuelve V-4, que el MER había declarado
abierto, y corrige un borrador del MR que nunca llegó a ser versión
confirmada.

---

## ADR-022 — Veredicto por DBA: se agrega un 4.º estado ("sin concluir") y una regla de precedencia; resuelve V-3

**Fecha:** 2026-08-26
**Estado:** aceptada

**Contexto:** al retomar Fase II para diseñar Tab Estudiantes (Vista
Interna, ADR-010 punto 4), se evaluó agrupar el listado de estudiantes
por su veredicto general de DBA (ADR-018), reutilizando ese cálculo tal
como Reporte ya lo usa. Alejandro objetó, con razón: al iniciar una
experiencia, antes de que nadie responda nada, ¿todos caerían en "no
concluyente"? Rastrear la pregunta hasta el final encontró que ADR-018
nunca definió qué pasa con un estudiante que **todavía no completó
todas las evidencias del DBA** — que no es un caso raro, es el estado
normal de casi cualquier estudiante mientras el curso está respondiendo.

Las 3 reglas de ADR-018, leídas con cuidado sobre un estudiante con
evidencias sin concluir (no solo el caso extremo de cero respondidas):
"Muestra" exige que *todas* sean "muestra" — una evidencia sin concluir
no es "muestra", así que esta falla, correctamente. "No muestra" exige
que *al menos una* sea "no muestra" — con nada evaluado aún en ese
sentido, esto también falla. "No concluyente" exige que *al menos una*
sea "no concluyente" — una evidencia sin concluir tampoco es eso: no es
que haya concluido de forma ambigua, es que **no ha concluido**, son
cosas distintas. Resultado: un estudiante a mitad de camino no cae en
**ninguna** de las 3 categorías. ADR-018 asumió, sin decirlo, que el
cálculo solo se hace cuando el estudiante ya terminó — pero Reporte y
esta pantalla nueva necesitan poder mostrar algo mientras el curso
todavía está respondiendo, que es la mayor parte del tiempo real de uso.

**Decisión:** se agrega un 4.º estado y se ordena la evaluación con
precedencia explícita — no son 4 condiciones independientes, se
comprueban en este orden:

1. **No muestra** ⟺ existe **al menos una** evidencia del DBA con
   Resultado ya concluido en estado "no muestra" — sin importar cómo
   estén las demás. Se evalúa primero y tiene precedencia sobre todo lo
   demás: una señal fuerte en contra es una alerta real desde el momento
   en que aparece, no hace sentido esperar a que el estudiante termine
   el resto para poder mostrarla (mismo principio de ADR-018 original,
   "no se promedia lo malo con lo bueno" — aquí se extiende a "tampoco
   se hace esperar").
2. **Muestra** ⟺ (no aplica 1) y **todas** las evidencias del DBA tienen
   Resultado concluido, y todas son "muestra".
3. **No concluyente** ⟺ (no aplica 1) y **todas** las evidencias del DBA
   tienen Resultado concluido, y al menos una es "no concluyente" (el
   resto "muestra").
4. **Sin concluir** ⟺ (no aplica 1) y **al menos una** evidencia del DBA
   todavía no tiene Resultado — sea porque el estudiante no ha
   respondido nada de esa evidencia, o porque va en curso sin llegar
   todavía al mínimo/tope de ADR-016.

Los 4 casos son exhaustivos y no se superponen — se verificó explícito,
no se asume: toda evidencia de un estudiante está, en un momento dado,
en uno de exactamente 3 lugares (concluida-muestra, concluida-no
muestra, concluida-no concluyente, o sin concluir), y las 4 reglas de
arriba cubren cada combinación posible de esos 4 valores sin dejar
ningún caso fuera y sin que dos reglas puedan aplicar a la vez (por eso
la precedencia: sin ella, un estudiante con 1 evidencia "no muestra" y
otra "sin concluir" activaría tanto la regla 1 como la 4).

**Resuelve V-3 del MER** ("distinguir 'no respondió' de 'respondió y no
concluyente'"): la distinción ya no depende de un dato nuevo — un
estudiante "sin concluir" se reconoce por la simple ausencia de fila en
`Resultado` para alguna evidencia del DBA (confirmado contra
`04-modelo-relacional.md`: `Resultado` solo se inserta cuando el proceso
adaptativo de ADR-016 concluye; antes de eso, no hay fila). No hace
falta ninguna columna ni tabla nueva — el esquema ya lo soporta, faltaba
la regla de lectura.

**Sub-distinción, sin ADR propio, para la interfaz (no para el
esquema):** dentro de "sin concluir", puede interesar separar "no ha
respondido nada de esta experiencia" (cero filas en `Respuesta` para esa
Inscripción) de "ya empezó, sigue en curso" (al menos una fila en
`Respuesta`, pero `Resultado` sigue sin existir para alguna evidencia).
Ambos se derivan de conteos ya existentes, sin estructura nueva — se
deja como decisión de presentación, no de modelo de datos.

**Consecuencia reconocida, con una pregunta que sigue abierta:** las 3
cards de "Resultados generales" en Reporte (`13-spec-modal-reporte.md`,
Ventana 010, ADR-018 original) solo contaban 3 estados — con el 4.º
agregado, esas 3 cards ya no suman el total de inscritos si algún
estudiante está "sin concluir", y el spec de Reporte todavía no lo
refleja. Esto no se corrige en esta decisión — Reporte no está en el
alcance de la sesión en curso (se está trabajando Tab Estudiantes); se
deja anotado como trabajo pendiente real, a resolver cuando se retome
esa pantalla.

**Reemplaza a:** ADR-018, en su definición de "Muestra"/"No
muestra"/"No concluyente" — pasan de 3 condiciones independientes a 3
de las 4 ramas de una regla con precedencia y un caso nuevo. El
razonamiento de fondo de ADR-018 (peso igual entre evidencias, sin
ponderar por dificultad) sigue vigente sin cambios.

---

## ADR-023 — "Datos insuficientes" (ADR-013/017) se amplía para contar también "sin concluir", no solo "no concluyente"

**Fecha:** 2026-08-26
**Estado:** aceptada

**Contexto:** al auditar el impacto de ADR-022 sobre
`13-spec-modal-reporte.md`, apareció el mismo vacío a nivel de una
evidencia individual (sección 2.3), no solo a nivel del veredicto por
DBA (sección 2.2). La categoría "Datos insuficientes" se calcula sobre
"40% o más de los resultados... son 'no concluyente'" (ADR-013) — un
umbral que solo cuenta evidencias ya concluidas de forma ambigua, sin
ninguna forma de contar a los estudiantes que todavía no han concluido
esa evidencia en absoluto. Sin corregirlo, una evidencia que nadie ha
empezado a responder tendría 0% "no concluyente" y no calificaría para
esa etiqueta — siendo exactamente el caso que más la necesita.

**Decisión:** el umbral de "Datos insuficientes" cuenta, juntos, a los
estudiantes en estado "no concluyente" (ya concluyó, quedó ambiguo) y a
los estudiantes "sin concluir" (ADR-022, todavía no llega a un
resultado) — ambos significan lo mismo para esta categoría: "todavía no
hay una lectura confiable de esta evidencia sobre el grupo". El umbral
numérico (40%) no cambia, solo se amplía qué cuenta hacia él.

Se evaluó crear una categoría separada ("Sin datos") en vez de ampliar
la existente — se descartó: dividiría en dos una distinción que el
docente lee igual ("todavía no sé"), el mismo tipo de precisión de más
que ADR-017 ya retiró una vez (4 categorías de brecha a 3).

**Consecuencia reconocida:** el texto del separador ("Todavía no hay
suficientes respuestas concluyentes") no se reescribe — ya cubre
honestamente el caso extremo de cero respuestas concluyentes. Distinto
es el conteo visible por estado (2.2 y la barra/leyenda de cada
evidencia en 2.3): ahí "sin concluir" sí se muestra aparte, con su
propio color — la unión de esta decisión aplica solo al umbral/label de
brecha, no al detalle numérico.

**Reemplaza a:** ADR-013, en qué cuenta hacia el umbral de "Datos
insuficientes" (antes: solo "no concluyente"; ahora: "no concluyente" +
"sin concluir"). El número del umbral (40%) y el resto de ADR-013/017
siguen vigentes.

---

## ADR-024 — El orden de las evidencias es el oficial del DBA (MEN); se retira la capacidad de reordenar

**Fecha:** 2026-08-29
**Estado:** aceptada

**Contexto:** al especificar en qué orden se listan las evidencias de un
estudiante dentro de la card expandida de Tab Estudiantes
(`14-spec-vista-interna-estudiantes.md`, Estado 3), se citó ADR-005
punto 2 ("el orden lo sugiere la IA... el docente puede reordenar
libremente") como la fuente de ese orden. Alejandro señaló que esa
capacidad no existe en ninguna parte del sistema — se verificó
buscando en las 16 specs de Fase II: ninguna pantalla tiene una función
de reordenar evidencias, ni para la IA sugerirlo ni para el docente
ejercerlo. Es el mismo problema estructural que tuvo ADR-009 antes de
ADR-016: una decisión que otorga una capacidad sin que exista ninguna
interfaz para ejercerla, así que la responsabilidad nunca tuvo cómo
hacerse real.

**Decisión:** el orden de las evidencias dentro de un diagnóstico es el
orden oficial en que aparecen en el documento DBA del MEN — dato fijo
de la fuente oficial. No lo sugiere la IA estimando dificultad, no lo
edita el docente. Se retira esa pieza del mecanismo de generación del
diagnóstico.

**Consecuencia reconocida:** simplifica el mecanismo — ya no hace falta
que la IA generadora estime dificultad para ordenar evidencias, y no
hace falta diseñar ninguna interfaz de reordenamiento en ninguna
pantalla futura. Quedan desactualizadas las citas a ADR-005 que
mencionan control del docente sobre el orden de evidencias, en
`decisiones.md` (líneas 399, 403, 407, 410, 413, 626, 893),
`glosario.md` (104, 136, 163-164) y `preguntas-abiertas.md` (268) — se
corrigen en la misma sesión en que se escribe esta ADR.

**Reemplaza a:** ADR-005, **punto 2 únicamente** (el orden sugerido por
IA y reordenable por el docente). El punto 1 de ADR-005 (el diagnóstico
se genera una sola vez, al crear la experiencia) sigue vigente, sin
cambios.

---

## ADR-025 — Esta versión se diseña solo para computador; el acceso móvil del estudiante queda diferido

**Fecha:** 2026-09-04
**Estado:** aceptada

**Contexto:** `05-habilidades-requeridas.docx` (Fase I) dejó el
dispositivo del estudiante sin decidir a propósito — describe el
requisito físico como "manejo básico de un dispositivo con pantalla
(clic o toque, desplazamiento)", cubriendo computador y celular por
igual, sin comprometerse con ninguno. Al empezar a diseñar el flujo del
estudiante (Fase II), esa ambigüedad ya no se puede sostener: cada
pantalla necesita un tamaño de frame y un patrón de interacción
concretos.

Alejandro aclaró dos cosas relevantes para decidir: (1) esta versión de
la plataforma no está pensada para desplegarse con estudiantes reales
— es una demo para presentar el concepto a docentes; (2) pensando en
una versión real futura, lo más común sería el celular propio del
estudiante o un computador, pero no todas las instituciones cuentan
con sala de cómputo, y la plataforma cubre cualquier área oficial del
MEN, no solo las que tienen mejor acceso a esa sala.

**Decisión:** para esta versión, el flujo del estudiante se diseña
**solo para computador** — mismo tamaño de frame y mismos componentes
ya usados en todo el flujo del docente (`1440×900`, Sidebar, Panel de
contenido). No se diseña una variante para celular.

**Consecuencia reconocida:** el acceso desigual a sala de cómputo entre
instituciones es una limitación real, no un detalle menor — se
reconoce explícitamente, no se ignora. Diseñar tocando ambos
dispositivos ahora exigiría un sistema de diseño paralelo completo
(otra navegación, otro tamaño de objetivo táctil, otros patrones de
modal) que frenaría cerrar Fase II. Se **difiere**, no se descarta —
mismo criterio que ADR-007 con Práctica y Verificación: la razón para
no resolverlo ahora queda escrita, para que una versión futura no
tenga que redescubrirla.

**Reemplaza a:** ninguna — resuelve una ambigüedad que
`05-habilidades-requeridas.docx` dejó abierta a propósito, no
contradice ninguna decisión previa.

---

## ADR-026 — El banco de preguntas es del docente: puede agregar las suyas; se congela al publicar y exige 6 activas por evidencia

**Fecha:** 2026-10-21
**Estado:** aceptada

**Contexto:** al reunir lo pendiente para cerrar Fase II aparecieron
tres vacíos ligados al banco de preguntas (`12-spec-modal-banco-items.md`):

1. **Una capacidad prometida sin pantalla.** ADR-009 punto 2 dice que
   "el docente puede pedir generar más" ítems. ADR-016 actualizó el
   número del banco (6 → 12) pero nunca retiró esa frase, y el propio
   banco descartó un botón "Regenerar". Es el patrón que el checklist
   de ADR-024 obliga a buscar.
2. **Nada impedía dejar una evidencia sin preguntas suficientes.** El
   docente puede descartar cualquier cantidad de los 12 ítems de una
   evidencia (ADR-015). ADR-016 necesita hasta **6** con un mismo
   estudiante (sigue hasta 6 cuando la señal no es clara); con menos,
   la regla se rompe justo en el estudiante más incierto. RI-9 ya
   limita las Presentaciones al número de ítems no excluidos, pero
   nada impedía publicar en esa condición.
3. **Editar el banco después de publicar quedaba abierto.** RI-10 solo
   prohíbe editar un ítem ya mostrado a alguien. Agregar, descartar o
   editar ítems todavía no mostrados haría que estudiantes de una misma
   experiencia respondan bancos distintos, y el Reporte agregaría
   resultados no comparables.

Alejandro planteó el principio de fondo: el docente es quien decide
sobre su experiencia, y las preguntas son lo más importante de ella en
cualquier versión. Si lo generado no lo convence, regenerar con un
botón probablemente daría algo parecido; lo que necesita es poder
corregirlo o completarlo él mismo. Regenerar *con instrucciones* sí
cambiaría el resultado, pero tiene su propia complejidad y se deja para
una versión futura. Además se evita multiplicar llamadas a la API.

**Decisión:**

1. **Se retira la capacidad "pedir generar más"** (ADR-009 punto 2, en
   esa frase). En esta versión, la IA genera el banco una sola vez, al
   crear la experiencia.
2. **El docente puede agregar preguntas propias**, dentro de cada
   evidencia del banco. Se crean con el mismo modo edición que ya
   existe para corregir un ítem generado (`12-spec`, 2.4b), arrancando
   en blanco. Heredan el formato de los ítems de esa evidencia (ADR-006
   asigna el formato por evidencia) y arrancan con el mínimo de
   opciones del formato (RI-4: 2 en `single_choice` y `ordering`, 4 en
   `matching`).
3. **El modo edición confirma con Guardar/Cancelar**, y Guardar solo se
   habilita si el ítem cumple las reglas de su formato (RI-4). Antes no
   estaba escrito cómo se confirmaba un cambio.
4. **Para publicar, cada evidencia incluida necesita al menos 6 ítems
   activos** (no excluidos). El botón "Publicar experiencia" queda
   deshabilitado mientras alguna no llegue, y la pantalla dice cuáles.
5. **Al publicar, el banco se congela**: queda de solo lectura. Todos
   los estudiantes de la experiencia responden sobre el mismo banco.
6. **Modelo de datos:**
   - `Ítem.origen` pasa de 2 valores a 3: `ia`, `editado_docente`,
     `creado_docente`.
   - **Se retira `Ítem.estado_revision`.** Entró en la Quinta revisión
     (H-5, aceptado en parte) sin vocabulario definido (V-7) y ninguna
     pantalla lo marca ni lo lee. La regla de publicación asociada de
     H-5 ya se había rechazado. Lo que pretendía asegurar —que el
     docente revise antes de que un estudiante vea el banco— lo cubren
     ahora el mínimo del punto 4, el recordatorio del modal de
     publicar y el congelamiento del punto 5. Retirarlo cierra V-7.

**Consecuencia reconocida:** con el banco congelado, un error que el
docente descubra después de publicar no se puede corregir en esta
versión. Se acepta: el modal de publicar ya lo advierte ("¿Se puede
deshacer? No" / "¿Qué debo revisar antes?"), y la alternativa
(versionar ítems) ya se evaluó y descartó en RI-10 por costar
estructura en tres entidades. Queda abierta una pregunta de modelado
para Fase III: el formato se decide por evidencia (ADR-006) pero se
guarda por ítem; hoy nada impide formatos mezclados dentro de una misma
evidencia.

**Reemplaza a:** ADR-009, en la frase "el docente puede pedir generar
más" de su punto 2. Amplía ADR-015 (agregar, además de descartar) y
completa RI-9/RI-10 con una regla de publicación y de congelamiento.

---

## ADR-027 — Crear una experiencia es "todo o nada": el docente espera la generación, y si falla no se guarda nada

**Fecha:** 2026-10-21
**Estado:** aceptada

**Contexto:** `07-spec-crear-experiencia-paso3.md` dejó pendiente qué
pasa entre el clic en "Crear experiencia" y el banco ya generado. Había
dos caminos: esperar en pantalla, o generar en segundo plano mientras
el docente sigue trabajando. El segundo exige que el modelo registre
estados intermedios ("generándose", "falló") que hoy no existen, y
pantallas para cada uno.

**Decisión:**

1. El docente **espera en pantalla**, con el Modal: Cargando
   (`24-spec-modal-cargando.md`, título "Generando las preguntas...").
   Decisión de Alejandro.
2. **Todo o nada**: la experiencia y su banco se guardan juntos, solo si
   la generación termina bien. Si falla o se agota el tiempo, no queda
   nada guardado. El Paso 3 muestra un mensaje de error y el mismo
   botón sirve para intentar de nuevo, sin perder el nombre ni el DBA
   ya elegidos.
3. `Experiencia.estado` sigue teniendo solo 2 valores: Borrador y
   Publicada. No se agregan estados de generación.

**Consecuencia reconocida:** con un DBA de muchas evidencias (12 ítems
por cada una), la generación puede tardar del orden de minutos, y el
modal de carga no se puede cerrar (excepción ya documentada en
`24-spec`). Para una primera versión se acepta. Si la espera resulta
excesiva al construir el backend, el camino de salida es el segundo
plano, y ese cambio sí obligaría a agregar estados al modelo.

**Reemplaza a:** ninguna — cierra la conversación pendiente de
`07-spec-crear-experiencia-paso3.md` §7.

---

## ADR-028 — Reglas de la toma del diagnóstico: un solo sentido, sin contador, certeza en paso aparte, y el estudiante no ve sus resultados

**Fecha:** 2026-10-21 (decisiones de Alejandro tomadas entre el
2026-09-12 y el 2026-09-27 al diseñar A5; se formalizan hoy).
**Estado:** aceptada

**Contexto:** al diseñar la Toma del diagnóstico
(`23-spec-toma-diagnostico.md`, Ventanas 020-023) se fijaron cinco
reglas del flujo del estudiante. Quedaron escritas solo dentro de la
especificación de pantalla, sin una decisión formal. Una de ellas —el
estudiante no ve sus resultados— define la pedagogía del producto
completo, y `pendientes.md` llegó a atribuirle un origen equivocado (el
glosario y ADR-018, que no la mencionan). La revisión de coherencia del
2026-10-21 lo encontró.

**Decisión:**

1. **Un solo sentido.** El estudiante no vuelve a una pregunta ya
   respondida. La regla adaptativa (ADR-016) decide la pregunta
   siguiente según las anteriores: cambiar una respuesta invalidaría
   una decisión que el sistema ya tomó. Además, RI-10 protege lo ya
   respondido.
2. **Sin contador ni barra de progreso.** La cantidad de preguntas por
   evidencia varía entre 4 y 6 según las respuestas (ADR-016); un total
   mostrado sería falso una parte de las veces.
3. **La certeza se pide en un paso aparte**, después de elegir la
   respuesta (escala CRI 0-5, ADR-008 punto 2). Decisión de Alejandro;
   duplica las pantallas por pregunta y queda revisable al probarlo.
4. **El estudiante no ve resultados**: ni si acertó una pregunta, ni su
   resultado por evidencia, ni el estado general al terminar. Razones:
   - La evaluación es **formativa para el docente**: su propósito es
     informar la decisión pedagógica del docente sobre su grupo
     (`02-fines-educativos`, `07-diseno-pedagogico`). La
     retroalimentación al estudiante ocurre, pero la da el docente,
     fuera del sistema.
   - Los resultados son probables, no ciertos ("no concluyente", "sin
     concluir"). Mostrárselos a un menor sin la mediación del docente
     arriesga que los lea como una nota, que es justo el lenguaje de
     certeza que el proyecto prohíbe.
   - Saber durante la secuencia si acertó cambiaría cómo responde y
     cómo reporta su certeza en las preguntas siguientes, y con eso la
     validez de la propia medición.
5. **Salir a medias no pierde nada.** Cerrar la pestaña dispara la
   advertencia del navegador; cada respuesta se guarda al confirmarla,
   y al volver el estudiante retoma exactamente donde quedó
   (reconstruido desde `Presentación`).

**Consecuencia reconocida:** un revisor de pedagogía puede objetar que
una evaluación "formativa" no le devuelve nada al estudiante; la
respuesta está en el punto 4. Alejandro dejó anotada una idea a futuro:
mostrarle al estudiante su resultado por evidencia al completar. Eso
exige revisar el punto 4 de esta decisión primero, no solo agregar una
pantalla.

**Reemplaza a:** ninguna — formaliza reglas que solo existían en
`23-spec-toma-diagnostico.md`.

---

## ADR-029 — Datos de estudiantes menores de edad: esta versión no registra la autorización del acudiente, y por eso no se usa con estudiantes reales

**Fecha:** 2026-10-21
**Estado:** aceptada

**Contexto:** la entrevista técnica E0 (curso 203447, Bloque G,
2026-09-25) encontró que el artículo 7 de la Ley Estatutaria 1581 de
2012 prohíbe el tratamiento de datos personales de niños, niñas y
adolescentes salvo los de naturaleza pública, que todo tratamiento debe
responder a su interés superior, y que exige la autorización del
representante legal; vigila la Superintendencia de Industria y
Comercio. Los estudiantes de AdaptiveLearn tienen entre 11 y 17 años.
El sistema no modela al acudiente ni su autorización. E0 decidió
(Decisión 2) declararlo como requisito no cumplido y límite de la
versión, pero esa decisión no había llegado a ningún documento de
diseño ni al modelo de datos.

**Decisión:**

1. La autorización del acudiente es un **requisito para usar el
   sistema con estudiantes reales**. Esta versión **no lo cumple**: no
   tiene dónde registrarla.
2. Por eso esta versión se usa **solo como demostración con
   docentes**, nunca con estudiantes menores reales — coherente con
   ADR-025, que ya la definía como demo.
3. **Datos que el sistema guarda de un estudiante**, y ninguno más:
   nombres, apellidos, correo (credencial), foto (opcional), sus
   inscripciones, qué preguntas se le mostraron, sus respuestas con su
   certeza, y sus resultados. **No** se recogen fecha de nacimiento,
   documento de identidad, institución ni curso. El correo no aparece
   en las vistas del docente sobre el aula ni en el historial
   (`14-spec`, `27-spec`).
4. **Modelo de datos (Fase III):** no se agrega una entidad Acudiente
   en esta versión. La ausencia de la autorización se declara como
   vacío del modelo, no se simula.

**Consecuencia reconocida:** un despliegue real necesitaría, como
mínimo: registrar al acudiente y su autorización (con fecha y medio),
una política de tratamiento de datos y términos de uso reales
(`17-spec` ya registra que hoy no existen), y revisar si la **foto del
estudiante** debe seguir siendo posible. La foto no es necesaria para
el diagnóstico, y es la imagen de un menor; hoy es opcional y la versión
no se usa con estudiantes reales, así que no bloquea nada, pero es lo
primero que un análisis de minimización señalaría.

**Reemplaza a:** ninguna — complementa ADR-025 y lleva al diseño la
Decisión 2 de E0.

---

## ADR-030 — El banco se genera con dos servicios de IA: uno principal y otro de respaldo; cada ítem guarda cuál lo generó

**Fecha:** 2026-10-21
**Estado:** aceptada; **punto 4 modificado por ADR-035** (el servicio y el modelo se guardan en la experiencia, no en cada ítem).

**Contexto:** el diseño nunca fijó qué servicio de IA genera el banco de
preguntas (`10-proceso-desarrollo.md` lo dejaba "sin fijar"; la versión
2 usaba Gemini y DeepSeek). Alejandro decidió usar los dos. Hacía falta
decidir *cómo*, porque cada forma cambia el diseño distinto. Además, la
generación es el punto de más riesgo del sistema: con ADR-027, si falla,
el docente no obtiene nada y tiene que reintentar.

**Decisión:**

1. **Gemini y DeepSeek, uno principal y otro de respaldo.** Cuál es el
   principal es un **ajuste de configuración** del sistema, no una
   decisión de diseño: se puede invertir sin cambiar ningún documento.
2. Si el principal **falla o supera el tiempo límite**, el sistema
   reintenta con el respaldo **dentro de la misma espera** (el modal
   "Generando las preguntas...", ADR-027). El docente no nota el cambio.
   Solo si fallan los dos se muestra el error de `07-spec`.
3. **Un banco, un servicio.** Si el principal falla a mitad de camino, el
   respaldo genera el banco completo de nuevo; no se mezclan preguntas de
   los dos en una misma experiencia. Así el "todo o nada" de ADR-027 se
   mantiene, y el banco de una experiencia es homogéneo.
4. **Cada ítem guarda qué servicio y qué modelo lo generó**
   (por ejemplo, el proveedor y el nombre del modelo que respondió). El
   docente no lo ve. Sirve para rastrear de dónde vino una pregunta mal
   generada y para comparar la calidad de los dos servicios con datos.
   Un ítem creado por el docente (ADR-026) no tiene servicio. Si el
   docente edita un ítem generado, conserva el servicio de origen: su
   `origen` ya dice que fue editado.

**Consecuencia reconocida:** en el peor caso (el principal se agota y
el respaldo responde) la espera del docente se alarga, y ADR-027 ya
reconocía que puede ser del orden de minutos. **El tiempo límite no se
fija aquí**: se mide al construir el incremento 2 y se registra. Son dos
claves de API que proteger: van en el `.env` del backend, que
`.gitignore` ya excluye; nunca en el repositorio.

**Reemplaza a:** ninguna — fija lo que `10-proceso-desarrollo.md` dejaba
"sin fijar" y complementa ADR-027.

---

## ADR-031 — Regla exacta del diagnóstico: qué es una señal fuerte, cuándo se detiene, qué pregunta sigue

**Fecha:** 2026-10-21
**Estado:** aceptada

**Contexto:** ADR-016 fijó la regla del diagnóstico de forma
cualitativa: mínimo 4 preguntas por evidencia, tope 6, y detenerse
"cuando hay mayoría de señales fuertes en una misma dirección". Nunca se
dijo qué es exactamente una señal fuerte, mayoría de qué, ni qué
pregunta se muestra a continuación. El docente del curso lo señaló en
la revisión del 2026-09-01 (hallazgo H-7), y el MER lo declaró como
vacío V-5, "previo a cualquier implementación": sin esta regla, el
resultado por evidencia no se puede calcular. Al empezar el análisis
de requerimientos de la Fase III ya no se podía postergar. Alejandro
decidió los cinco puntos el 2026-10-21.

**Decisión:**

1. **Certeza alta = 3, 4 o 5** en la escala de 0 a 5. Es el corte del
   artículo original del índice (Hasan, Bagayoko y Kelley, 1999: un CRI
   mayor a 2,5 es alto).
2. **Cada respuesta es una de tres señales:**
   - **Fuerte de "muestra"**: correcta, con certeza 3 a 5.
   - **Fuerte de "no muestra"**: incorrecta, con certeza 3 a 5.
   - **Débil**: cualquier respuesta con certeza 0 a 2, correcta o no
     (ADR-008 punto 2).
3. **Cuándo es correcta una respuesta:** en selección única, si eligió
   la opción correcta; en emparejamiento y ordenamiento, **solo si todos
   los pares o todas las posiciones están bien**. Un acierto parcial
   cuenta como incorrecta.
4. **Cuándo se detiene**, por evidencia, contando solo las preguntas
   respondidas (n):
   - Con n menor que 4, nunca se detiene.
   - Desde n = 4, después de cada respuesta: si **más de la mitad de las
     n respuestas** son señales fuertes de "muestra", concluye
     **Muestra**; si más de la mitad son señales fuertes de "no
     muestra", concluye **No muestra**. Las dos cosas no pueden pasar a
     la vez.
   - Si llega a n = 6 sin cumplirse ninguna, concluye **No
     concluyente**.
   - En la práctica: con 4 o 5 respuestas hacen falta 3 señales fuertes
     iguales; con 6, hacen falta 4.
5. **Qué pregunta sigue:** una **al azar** entre los ítems activos (no
   excluidos) de esa evidencia que todavía no se le mostraron a ese
   estudiante. Las evidencias van en el orden oficial del DBA (ADR-024),
   y no se pasa a la siguiente sin concluir la actual. El banco nunca se
   agota: al publicar, cada evidencia tiene al menos 6 ítems activos y
   ya no cambia (ADR-026).
6. **Al retomar:** si el estudiante salió con una pregunta mostrada y
   sin responder, al volver ve **esa misma pregunta**, no una nueva. No
   pierde uno de sus 6 cupos por haber cerrado la pestaña. *(Corrige lo
   que decía `23-spec`, Ventana 020, Estado B.)*

**Consecuencia reconocida:** el corte de certeza y la mayoría son
puntos de partida con fuente, no una calibración propia de
AdaptiveLearn; la misma reserva que ADR-016 ya hacía con el rango 4-6.
El criterio de "todo o nada" en emparejar y ordenar es deliberadamente
prudente: un estudiante que acierta 3 de 4 pares deja una señal de "no
muestra" si respondió seguro. Queda revisable cuando haya datos reales.
Con el azar, dos estudiantes de una misma experiencia no ven
necesariamente las mismas preguntas. Es justo lo que dificulta copiarse,
pero también hace que la comparación entre ellos sea por evidencia y no
pregunta a pregunta.

**Reemplaza a:** ninguna. **Precisa a ADR-016** (que sigue vigente en
el rango 4-6) y resuelve el vacío **V-5** del MER (hallazgo H-7).

---

## ADR-032 — Regla exacta de clasificación del Reporte por evidencia

**Fecha:** 2026-10-21
**Estado:** aceptada

**Contexto:** ADR-013, ADR-017 y ADR-023 definen las 3 categorías con
que el Reporte etiqueta cada evidencia para el grupo, pero dos cortes
quedaron escritos de forma aproximada: "Brecha aparente" como
"cualquier proporción de 'no muestra' mayor a **~0 %**" y "Sin brecha
aparente" como "nadie **(o prácticamente nadie)**". Un requerimiento no
puede decir "~" ni "prácticamente". Se encontró al preparar el análisis
de requerimientos de la Fase III, y Alejandro decidió el corte.

**Decisión:** para cada evidencia de una experiencia, sobre **N =
estudiantes inscritos**, en este orden:

1. Si **"no concluyente" + "sin concluir" ≥ 40 % de N** → **Datos
   insuficientes** (ADR-013, ampliada por ADR-023).
2. Si no, y **al menos 1 estudiante** tiene "no muestra" → **Brecha
   aparente**.
3. Si no → **Sin brecha aparente**.

Con N = 0 no hay reporte (la pestaña Estudiantes muestra su Estado 2).

**Consecuencia reconocida:** en un grupo de 35, un solo estudiante con
"no muestra" basta para "Brecha aparente". Es deliberado: el docente
quiere saber quién necesita atención, y la tarjeta muestra la magnitud
(por ejemplo, 1/35), así que la etiqueta no exagera. Un umbral
porcentual habría sido inventado, porque no hay datos reales que lo
respalden.

**Reemplaza a:** ninguna. **Precisa a ADR-017** (sus "~0 %") **y a
ADR-013** ("prácticamente nadie").

---

## ADR-033 — Alcance curricular de esta versión: 4 áreas, en sus versiones oficiales vigentes, verificadas contra lo que hoy publica el MEN

**Fecha:** 2026-10-24
**Estado:** aceptada

**Contexto:** el docente del curso pidió adelantar en el MER tablas para
el área y el grado de los DBA. Al revisarlo apareció que la aplicación
ofrece 4 áreas sin que ninguna decisión dijera por qué, aunque el MEN
publica DBA también para **Transición** y para **Inglés** (de
transición y primaria, y de 6° a 11°, este último de 2016, programa
Colombia Bilingüe). Áreas como Artística, Educación Física o Tecnología
no tienen DBA. Además, no se había comprobado que los PDF usados fueran
las versiones vigentes.

**Verificación (2026-10-24):** se descargaron los 4 PDF que hoy publica
el MEN en Colombia Aprende (colección "Derechos Básicos de Aprendizaje",
publicados el 25/05/2026) y se compararon con los de
`data/curriculo-men/pdfs/`:

| Área | Versión | Páginas | Archivo oficial (Colombia Aprende) | ¿Igual al nuestro? |
|---|---|---|---|---|
| Matemáticas | **V.2** | 88 | `files_public/2026-06/dba_matematicas-min.pdf` | Idéntico byte a byte |
| Lenguaje | **V.2** | 56 | `files_public/2026-05/dba_lenguaje-min.pdf` | Idéntico |
| Ciencias Naturales | **V.1** | 44 | `files_public/2026-05/dba_c.naturales-min.pdf` | Idéntico |
| Ciencias Sociales | **V.1** | 52 | `files_public/2026-05/dba_c.sociales-v2_0.pdf` | Idéntico |

Los 4 archivos oficiales fueron creados en octubre de 2016 y son la
versión más reciente que el MEN publica: **no hay una versión 2 de
Ciencias Naturales ni de Ciencias Sociales**. El propio documento lo
dice: *"…en las áreas de lenguaje, matemáticas en su segunda versión,
ciencias sociales y ciencias naturales en su primera versión"*.

**Corrección que deja esta verificación:** Ciencias Sociales se venía
citando como **"V.2"** (en `curriculo_men_normalizado.json` y en los
documentos `01` y `06` de la Fase I). Es **V.1**. El error viene del
nombre del archivo, que el propio MEN publica como `…sociales-v2_0.pdf`
—y que en este repositorio se llama `dba_ciencias_sociales_v2.pdf`—,
aunque su portada y sus 50 encabezados dicen "V.1".

**Decisión:**

1. La aplicación ofrece los DBA de **Matemáticas, Lenguaje, Ciencias
   Naturales y Ciencias Sociales**, grados **1° a 11°**, en las versiones
   de la tabla: Matemáticas V.2, Lenguaje V.2, Ciencias Naturales V.1,
   Ciencias Sociales V.1.
2. **Inglés queda fuera**, por decisión de Alejandro: es un área que
   exige más de lo que esta versión ofrece —no se puede reducir a
   preguntas de formato cerrado: hablar, escuchar, escribir—, y su
   conjunto de DBA no está completo.
3. **Transición queda fuera**: es preescolar, fuera de la población del
   producto (secundaria), y sus DBA no están organizados por área.
4. Si el MEN publica una versión nueva de un área, se actualiza con una
   decisión nueva; la verificación de esta tabla se repite contra los
   archivos oficiales, no contra su nombre.

**Consecuencia reconocida:** Inglés de 6° a 11° es de secundaria, la
población del producto; dejarlo fuera es una limitación de alcance, no
un olvido. Que el nombre de un archivo oficial contradiga su contenido
deja una lección para la auditoría del currículo (`pendientes.md`,
A12): **la versión se lee del documento, nunca del nombre del archivo**.

**Reemplaza a:** ninguna — fija un alcance que estaba implícito.

---

## ADR-034 — La cuenta de acceso es una entidad propia, CREDENCIAL, separada de Docente y Estudiante

**Fecha:** 2026-10-26
**Estado:** aceptada

**Contexto:** en agosto se evaluó una entidad "Cuenta" común a Docente
y Estudiante y no se adoptó (vacío V-8 del MER: autenticación y
credencial, sin resolver). El diseño del acceso en la Fase II
(ventanas 014 a 019) mostró dos cosas que sin esa entidad no tienen
dónde vivir:

1. El **código de verificación del correo** tiene que guardarse *antes*
   de que exista el docente o el estudiante: la cuenta se crea con su
   rol al final del registro (ventana 017, RF-01-06).
2. El **correo es único entre los dos roles** (RF-01-04): no puede haber
   un docente y un estudiante con el mismo correo. Dos restricciones de
   unicidad separadas, una por tabla, no lo garantizan.

El backend del incremento I1 ya resolvió así el acceso
(`backend/sql/001_esquema_auth.sql`, tabla `credencial`). El MER final
de la Fase III (`16-modelo-entidad-relacion.md`, 2026-10-26, hecho por
el compañero del equipo) incorporó la entidad CREDENCIAL, y faltaba la
decisión formal que la respalda.

**Decisión:**

1. **CREDENCIAL** es la cuenta de acceso: correo (único, sin distinguir
   mayúsculas), método de acceso (correo y contraseña, Google o
   Microsoft), contraseña con hash o identificador del proveedor, si el
   correo está verificado y el código de verificación vigente.
2. Una credencial da acceso a **un solo rol**, Docente **o** Estudiante,
   nunca a los dos (RI-12); cada docente y cada estudiante tiene
   exactamente una credencial.
3. **Docente y Estudiante dejan de guardar el correo**: está en su
   credencial. Guardan `nombres`, `apellidos` y la foto opcional.

**Consecuencia reconocida:** el modelo pasa de 14 a 15 entidades. La
no-adopción de agosto se revierte con una razón que en agosto no
existía: el flujo de registro de la Fase II. `diseno/modelo-conceptual.md`,
que hasta hoy decía "no existe una entidad Cuenta común", se corrige.

**Reemplaza a:** la no-adopción de "Cuenta" registrada como V-8 en el MER
de la Quinta revisión. **Cierra V-8.**

---

## ADR-035 — Se confirman las decisiones que la Fase III dejó abiertas para el equipo

**Fecha:** 2026-10-26
**Estado:** aceptada

**Contexto:** al hacer la Fase III (documentos `12` a `20`), el
compañero del equipo tuvo que decidir cosas que los requerimientos no
decían, y las declaró en vez de resolverlas en silencio
(`19-entrega-fase-3.md` §4; `12-casos-de-uso.md` §7). Una de ellas
contradice una decisión vigente (ADR-030, punto 4). Alejandro las
revisó y las confirmó el 2026-10-26.

**Decisión:**

1. **El servicio y el modelo de IA se guardan una vez, en la
   Experiencia** (RI-17), no en cada ítem. ADR-030 punto 3 ya dice que un
   banco sale entero de un solo servicio, así que guardarlo por ítem
   repite el mismo dato en los 12 ítems de cada evidencia y además
   permitiría, por error, un banco con servicios mezclados. El propósito
   de ADR-030 —saber de dónde vino una pregunta y comparar los dos
   servicios— se mantiene: un ítem generado o editado es del servicio de
   su experiencia; uno creado por el docente (`origen = creado_docente`)
   no se atribuye a la IA. **Modifica ADR-030, punto 4.**
2. **Registro a medias** (`12`, CU-06, alterno 3a): quien creó su
   credencial pero no eligió rol y vuelve a iniciar sesión, retoma el
   registro en "Completa tu perfil". No queda atrapado ni empieza de
   nuevo.
3. **Ítem generado inválido** (`12`, CU-16, alterno 4a): si la IA genera
   un ítem que no pasa la validación de su formato (RI-4), se trata como
   una falla de ese servicio y se pasa al de respaldo. Mantiene el
   "todo o nada" de ADR-027 y "un banco, un servicio" de ADR-030.
4. **Eliminar una experiencia o salir de ella borra en cascada** lo que
   depende de ella (`17-modelo-relacional.md`). Es lo que ya advierten
   los modales de la ventana 025 ("se elimina") y lo que se eligió al
   diseñarlos ("permitir siempre, con advertencia"). Comprobado contra el
   motor: eliminar una experiencia borra exactamente su banco, sus
   inscripciones y todo lo respondido; salir borra solo lo respondido
   por ese estudiante. **Cierra V-11.**
5. **`Item.estado_revision` sale.** Ya estaba decidido en ADR-026; el
   documento `19` lo listaba como "por confirmar" porque el triaje del
   2026-09-04 lo había aceptado. No se reabre.

**Consecuencia reconocida:** RF-03-03 cambia de "cada ítem registra su
servicio" a "la experiencia registra su servicio, cada ítem su origen".
Con la cascada, un docente que elimina una experiencia con estudiantes
pierde esos datos sin vuelta atrás: el modal ya lo dice con números.

**Reemplaza a:** ADR-030, en su punto 4.

---

## ADR-036 — El catálogo curricular se normaliza: Área, Grado y Documento oficial como entidades, con códigos sin tildes

**Fecha:** 2026-10-26
**Estado:** aceptada

**Contexto:** en la revisión del 2026-10-22
(`fase-3-diseno-computacional/21-revision-docente-2026-10-22.md`), el
docente del curso pidió *"tabla para grados y área y codificar"*. En el
MER final (`16`), el área y el grado son textos sueltos dentro de cada
DBA (`area`, `grado`), y el código del DBA es el identificador que dejó
la normalización de la V2: `matemáticas_1_dba_1`, con tilde. Nada impide
escribir mal un área, no hay dónde guardar de qué documento oficial
salió cada DBA (y ADR-033 mostró que eso importa: Ciencias Sociales se
citaba con la versión equivocada), y una tilde en una llave es fuente de
errores entre sistemas.

**Decisión:**

1. **ÁREA** — `codigo_area` (PK) y `nombre`. Las 4 de ADR-033:

   | Código | Nombre |
   |---|---|
   | `MAT` | Matemáticas |
   | `LEN` | Lenguaje |
   | `CN` | Ciencias Naturales |
   | `CS` | Ciencias Sociales |

2. **GRADO** — `numero` (PK, 1 a 11), `nombre` ("Primero" a "Undécimo")
   y `nivel`: **básica primaria** (1° a 5°), **básica secundaria** (6° a
   9°) o **media** (10° y 11°), según los niveles de la educación formal
   de la Ley 115 de 1994. Sin Transición (ADR-033).
3. **DOCUMENTO_OFICIAL** — el PDF del MEN del que se copiaron los DBA de
   un área: título, versión, año, número de páginas y dirección oficial.
   Uno por área en esta versión, con los datos verificados en ADR-033
   (Matemáticas V.2, Lenguaje V.2, Ciencias Naturales V.1, Ciencias
   Sociales V.1; los cuatro de 2016). Recomendación del 2026-10-24,
   aceptada por Alejandro: no la pidió el docente, pero es la que deja
   trazable que nada se inventó.
4. **DBA** deja de tener `area` y `grado` como texto: **pertenece a** un
   Área, **corresponde a** un Grado y **se copia de** un Documento
   oficial. El documento de un DBA tiene que ser de su misma área.
5. **Código del DBA:** `ÁREA-GG-NN`, con ceros a la izquierda y sin
   tildes: `MAT-01-01`, `CS-11-05`. Se arma desde el área, el grado y el
   número de cada DBA. **El código es único por diseño; los datos de hoy
   no lo cumplen:** la normalización de la V2 asignó al grado anterior el
   primer DBA de algunas páginas, y 13 identificadores viejos quedaron
   repetidos (por ejemplo, hay dos `matemáticas_2_dba_1`: el segundo es el
   DBA 1 de 3°). Se corrige en la auditoría (pendientes, A12), no
   relajando el modelo. *(Corrección del mismo día: una primera versión
   de este punto decía que la equivalencia con el identificador viejo
   era "directa".)*

**Consecuencia reconocida:** el MER pasa de 15 a 18 entidades. Que el
documento de un DBA sea de su misma área forma un ciclo nuevo
(DBA → Área ← Documento oficial ← DBA), que tiene que declararse y
cerrarse con una regla, como los otros cinco. Los datos de
`data/curriculo-men/` **no se tocan a mano**: las tablas se llenan desde
ellos, y la auditoría (pendientes A12) sigue pendiente.

**Reemplaza a:** ninguna. Responde a la revisión del docente del
2026-10-22.

---

## ADR-037 — La verificación del correo se guarda como un estado, no como sí/no

**Fecha:** 2026-10-26
**Estado:** aceptada

**Contexto:** el docente pidió, en la misma revisión, *"cambiar email a
estado_verificado, estado_procesando"*. Hoy CREDENCIAL (ADR-034) guarda
`email_verificado` como verdadero/falso.

**Decisión:** `email_verificado` se reemplaza por
**`estado_verificacion`**, con dos valores: **`procesando`** (se envió el
código y todavía no se confirma) y **`verificado`**. Quien entra con
Google o Microsoft queda `verificado` desde que se crea su credencial:
el proveedor ya lo verificó (RF-01-02).

**Consecuencia reconocida:** un estado admite crecer (por ejemplo, un
`vencido`) sin cambiar el tipo del campo. La otra parte de la misma
nota del docente —quitar `codigo_expira_en` y `codigo_ultimo_envio`—
**no se decide aquí**: sin esos campos, el vencimiento del código y la
espera de 30 segundos para reenviarlo (RF-01-03) necesitan otro lugar, y
se le preguntó al docente qué prefiere.

**Reemplaza a:** ninguna. Modifica un atributo de la entidad de ADR-034.
