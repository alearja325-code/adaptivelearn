# Glosario — AdaptiveLearn (rediseño)

> Cada término se redacta a dos manos: Alejandro responde primero, Claude critica
> y propone versión completa, Alejandro confirma. Ningún término se cierra sin
> que Alejandro pueda explicarlo de memoria, sin mirar este documento.

---

## DBA (Derecho Básico de Aprendizaje)

**Estado:** confirmado — 2026-08-05

Un aprendizaje **estructurante** — no solo un conocimiento o habilidad valiosa,
sino uno que **organiza el camino hacia aprendizajes futuros** — que el MEN
define como esencial para un grado y un área específicos. Se construye
guardando coherencia con los Lineamientos Curriculares y los Estándares
Básicos de Competencias: los DBA son la forma en que, año a año, se va
alcanzando lo que los Estándares esperan al cierre de cada ciclo.

No es una camisa de fuerza de grado: el docente y la institución pueden
ubicarlo donde resulte más pertinente para sus estudiantes. Tampoco es, por sí
solo, una propuesta curricular. Y es del **tamaño de un año, no de una
experiencia puntual** — no se alcanza con una o unas pocas actividades, sino
con múltiples experiencias trabajadas a lo largo del año.

**Fuente:** [Colombia Aprende — Derechos Básicos de Aprendizaje](https://www.colombiaaprende.edu.co/contenidos/coleccion/derechos-basicos-de-aprendizaje)

---

## Aprendizaje

**Estado:** confirmado — 2026-08-05

Dentro de AdaptiveLearn, un aprendizaje **es, concretamente, un DBA** — la
unidad oficial, estructurante, de tamaño-año que ancla una experiencia. No es
un concepto pedagógico flotante aparte del DBA; es su nombre operativo dentro
del sistema.

---

## Tema

**Estado:** diseño confirmado — 2026-08-05; diferido, fuera de alcance de
esta versión — 2026-08-07

El contenido amplio y libre que el docente piensa de forma natural (ej.
"ecuaciones lineales", "multiplicación y división"). No tiene tamaño fijo y
puede atravesar varios aprendizajes (DBA) a la vez — "ecuaciones lineales",
por ejemplo, toca 8 DBA distintos en 5 grados.

El tema no ancla directamente una experiencia ni persiste como objeto: es una
**búsqueda**, una herramienta para encontrar aprendizajes relevantes dentro de
la biblioteca — no una estructura que se guarda.

**Por qué queda fuera de esta versión:** el tema es lenguaje informal del
docente, que no coincide literalmente con el texto oficial de un DBA —
usarlo como filtro exigiría un puente semántico (búsqueda por
significado, no por coincidencia de texto) que esta versión no va a
construir. En su lugar, la selección de esta versión filtra directo
sobre **Aprendizaje** (el DBA mismo: su área, su grado, su enunciado y
evidencias oficiales) — sin capa de traducción entre lenguaje natural y
vocabulario del MEN. El docente busca con el vocabulario oficial, no con
el suyo — limitación real, no oculta.

---

## Experiencia

**Estado:** confirmado — 2026-08-05; alcance ajustado por ADR-007 — 2026-08-07

Un espacio, anclado a **un** DBA que el docente elige, donde los
estudiantes se enfrentan a las evidencias oficiales de ese DBA que el
sistema puede evaluar, mediante preguntas y ejercicios de formato
cerrado. Cada respuesta alimenta un resultado probable —muestra, no
muestra, o no concluyente; nunca una certeza (ver Diagnóstico, ADR-008)—
sobre el manejo que el estudiante tiene en ese momento frente a esa
evidencia puntual. Es la unidad mínima de trabajo de esta versión del
sistema.

**Alcance de esta versión (ADR-007):** el ciclo ejecutable es
Diagnóstico → Reporte. Práctica y Verificación quedan fuera — no
descartadas, diferidas a una versión posterior, una vez que Diagnóstico
esté validado y estable (ver Práctica, Verificación).

**Dos estados** *(agregado 2026-10-21)*: **Borrador** mientras el
docente prepara el banco, y **Publicada** cuando decide abrirla a sus
estudiantes. Publicar exige al menos 6 preguntas activas por evidencia,
congela el banco y no se puede deshacer (ADR-026). Crear una
experiencia es "todo o nada": si la IA no logra generar el banco, no se
guarda nada (ADR-027). Los estudiantes entran con un código de
invitación (ver Inscripción).

---

## Evidencia

**Estado:** confirmado — 2026-08-05; renombrado de "Punto de aprendizaje" — 2026-08-07

Una evidencia de aprendizaje oficial del DBA, tal como el MEN la redactó
— no una invención de la IA. Se llamó "punto de aprendizaje" mientras el
sistema asumía que cada una necesitaba una escalera de profundidad propia
(herencia de SOLO); al confirmarse que cada evidencia ya trae su propio
nivel de exigencia en el verbo que el MEN usó para redactarla —no es algo
que el sistema le asigne ni una escalera que deba recorrer—, el nombre
"punto de aprendizaje" dejó de aportar algo que "evidencia" no dijera
mejor y con más precisión: es, literalmente, el término del MEN.

En esta versión, las evidencias quedan **sueltas entre sí** — sin
conexión obligatoria ni jerarquía forzada (ver ADR-001) — porque las
evidencias del MEN son, en su fuente, planas: facetas paralelas del mismo
aprendizaje, no una escalera. Se presentan en el orden oficial del
documento DBA del MEN — no lo sugiere la IA ni lo reordena el docente
(ADR-024, que revisa ADR-005 en este punto: nunca existió una interfaz
para ejercer esa capacidad).

El número de evidencias por experiencia no es un rango fijo: lo determina
la cantidad real de evidencias del DBA anclado. El rango que se había
registrado (1 a 6) no es confiable — incluye un bug de extracción de
datos, ver QA-013.

**Pendiente:** el rol exacto de la Taxonomía de Bloom (ADR-003) quedó
ambiguo — se escribió pensando en "graduar profundidad" al estilo de una
escalera por término, lo cual ya no aplica si cada evidencia trae un
nivel fijo, no una escalera que recorrer. Falta una corrección explícita
(ver preguntas-abiertas.md).

---

## Diagnóstico

**Estado:** confirmado — 2026-08-05; mecanismo cerrado por ADR-008,
ajustado por ADR-009 y **revisado por ADR-016** (que reemplaza a ADR-009
en cuántos ítems ve el estudiante) y ADR-015 (descartar ítems) —
actualizado 2026-08-26.

El primer momento del ciclo de la experiencia — y, en esta versión, el
único que el estudiante atraviesa (ver Experiencia, ADR-007). Por cada
evidencia del DBA, determina si el estudiante **la muestra, no la
muestra, o queda no concluyente** — probable, nunca una certeza. No
identifica ni nombra por qué falla (eso quedó fuera de esta versión, ver
ADR-008) — las evidencias del MEN están redactadas para responder si se
alcanza o no un aprendizaje, no para catalogar errores.

Se genera una sola vez, al momento en que el docente crea la experiencia
— no en vivo por cada estudiante (ver ADR-005). El docente puede
revisarlo, corregirlo y completarlo con preguntas propias; nada llega a
un estudiante hasta que el docente publica la experiencia, y al publicar
el banco se congela (ADR-026). *(Corrección 2026-10-21: decía "el
docente lo revisa antes de que cualquier estudiante lo vea", como si
fuera obligatorio; el sistema lo recuerda, no lo exige.)*

El formato de cada ítem —opción múltiple, emparejamiento u ordenar; nunca
texto libre en esta versión (ver QA-012)— se elige por una regla
operativa según la evidencia que se prueba (ver ADR-006). Los
distractores se construyen plausibles, no arbitrarios (principio
heredado del Force Concept Inventory y de Haladyna), pero no se nombran
como hipótesis de error reportada (ADR-008). El **ejemplo** del DBA (su
tercera parte oficial, junto a enunciado y evidencias) se usa como
escenario de referencia al generar estos ítems — no como ítem en sí ni
como material solo pasivo (ver ADR-011); pendiente de que la
normalización lo capture como dato.

Cada respuesta se acompaña de una certeza (CRI, escala 0-5, Hasan et al.
1999): una respuesta con certeza baja —acierto o error— no cuenta como
evidencia fuerte.

Cuántos ítems responde el estudiante por evidencia lo fija el
**sistema**, con una regla adaptativa por certeza: mínimo 4 ítems
siempre —ninguna conclusión se basa en menos—, y a partir de ahí se
detiene en cuanto hay mayoría de señales fuertes en una misma
dirección, con tope de 6 (ADR-016, con fundamento en el rango de 4 a 6
ítems por objetivo que recomienda la literatura de mastery testing —
Shrock & Coscarelli). La regla exacta —certeza alta = 3 a 5; detenerse
cuando más de la mitad de las respuestas son señales fuertes iguales;
la pregunta siguiente, al azar entre las no mostradas— está en ADR-031.
Esto reemplaza la idea anterior de que era el
docente quien decidía ese número (ADR-009): nunca existió una interfaz
para que lo hiciera, así que la responsabilidad no tenía cómo
ejercerse. Mismo motivo por el que el orden de las evidencias dejó de
ser algo que el docente decide (ADR-024, revisa ADR-005) — el docente
sí sigue decidiendo el contenido de los ítems (editar, descartar o
agregar propios — ADR-015, ADR-026). Lo
que el sistema genera por adelantado es un **banco** más grande de lo
que cualquier estudiante llega a ver — base de **12** ítems por
evidencia (ADR-016), para que el docente tenga margen real de dónde
elegir, editar o descartar. Para publicar, cada evidencia necesita al
menos 6 activas — el tope que la regla puede llegar a usar con un
estudiante (ADR-026). Ya no se puede pedir a la IA que genere más: el
docente completa con preguntas propias (ADR-026).

**Cómo lo vive el estudiante (ADR-028):** responde en un solo sentido
(no vuelve a una pregunta ya respondida), sin contador de preguntas,
declara su certeza en un paso aparte después de cada respuesta, y **no
ve sus resultados**: el diagnóstico es formativo para el docente, que es
quien le devuelve la información fuera del sistema.

**Pendiente (ver preguntas-abiertas.md):** auditar los generadores de
preguntas duplicados en el código actual antes de construir el nuevo
(QA-006); el bug de extracción de evidencias y el censo de
compatibilidad con formato cerrado (QA-013, QA-014). Esto describe
**qué es** el diagnóstico y su mecanismo de decisión — falta todavía la
implementación en sí, que es trabajo aparte.

---

## Práctica

**Estado:** diseño confirmado — 2026-08-05; diferida a v2, fuera de
alcance de esta versión (ver ADR-007) — 2026-08-07

El diseño queda registrado para cuando vuelva a estar en alcance — no se
construye en esta versión. El segundo momento del ciclo, donde la
personalización se vuelve concreta.
Toma las brechas con hipótesis de error del diagnóstico y construye una
intervención dirigida a esa necesidad específica — no un repaso genérico del
DBA completo. Sigue una secuencia de hasta seis pasos: descubrimiento guiado
→ explicación breve → ejemplo trabajado → práctica focalizada →
retroalimentación → **comprobación de brecha** (evidencia fresca sobre esa
misma brecha, para ver si la intervención sirvió — distinta del tercer
momento de la experiencia, Verificación, que cubre el DBA completo, no solo
esta brecha). No siempre se generan los seis pasos: el sistema decide, por
brecha, entre intervenir, pedir más evidencia, ofrecer solo repaso/extensión,
o escalar al docente.

Dos principios que se conservan del sistema anterior: la ruta decidida no es
contenido de enseñanza, es una restricción para generarlo después — separa
decidir de generar; y la mejora de esa brecha solo se declara con la
comprobación fresca, nunca por el solo hecho de completar la práctica.

---

## Verificación

**Estado:** diseño confirmado — 2026-08-05; diferida a v2, fuera de
alcance de esta versión (ver ADR-007) — 2026-08-07

El diseño queda registrado para cuando vuelva a estar en alcance — no se
construye en esta versión. El tercer momento del ciclo — **distinto** de la comprobación de brecha que
ya ocurre dentro de práctica (mismo nombre usado antes para dos cosas
distintas; se desambiguó aquí). Ocurre una vez, al cerrar la experiencia
—cuando ya se atendieron todas las evidencias del DBA—, con ítems propios, no
reciclados de diagnóstico ni de práctica, y pone a prueba al estudiante
frente al **DBA completo**, no solo las brechas que fueron intervenidas. Es
necesario cubrir todo el DBA porque lo que el diagnóstico dio por manejado
tampoco era una certeza (ver Diagnóstico) — limitarse a las brechas dejaría
sin revisar todo lo que "parecía" estar bien y quizás no lo estaba. La mejora
de la experiencia completa solo se declara con esta evidencia fresca.

**No ocurre inmediatamente después de práctica: es programable, con una
espera definida**, para que la evidencia refleje aprendizaje consolidado y no
memoria de corto plazo (efecto de espaciamiento, ya mencionado al principio
de esta sesión), y para no fatigar al estudiante.

**Pendiente, fuera de esta versión:** si esta verificación se repite varias
veces a lo largo del año, no solo una vez al cerrar — mismo mecanismo, mayor
frecuencia.

---

## Reporte

**Estado:** confirmado — 2026-08-05; alcance ajustado por ADR-007,
mecanismo cerrado por ADR-010, y revisado después por ADR-013, ADR-017,
ADR-018, ADR-022 y ADR-023 — actualizado 2026-08-26.

A diferencia de diagnóstico, no es un momento que el estudiante atraviesa —
es la capa que convierte lo que diagnóstico produjo (evidencia probable,
nunca certeza) en algo que el docente puede usar a la escala en la que
realmente trabaja: un grupo completo, no un estudiante a la vez. Cuando
práctica y verificación vuelvan a estar en alcance (ver ADR-007), Reporte
combinará también esos momentos — no en esta versión, donde solo existe
diagnóstico.

Reúne el estado de cada evidencia por estudiante y lo agrega por grupo,
traduciéndolo en una **clasificación calculada por umbral** — nunca en una
recomendación redactada por IA (ADR-010 punto 2 descarta eso de forma
deliberada: un "se recomienda reforzar…" inventaría una causa que el
sistema no tiene). Mantiene el mismo principio que diagnóstico: ningún
resultado se declara con lenguaje de certeza ("domina", "aprobó" quedan
explícitamente prohibidos); todo es evidencia formativa, revisable, de uso
formativo, no sumativo.

**Qué muestra la vista principal** (Ventana 010, dos secciones):

- **Estado general:** cuántos estudiantes hay en cada uno de los **cuatro**
  estados posibles frente al DBA completo — muestra, no muestra, no
  concluyente y **sin concluir** (ADR-018, revisado por ADR-022; el cuarto
  cubre a quien todavía no ha terminado todas sus evidencias, que es el
  caso normal mientras el grupo está respondiendo, no una excepción).
- **Estado por evidencia:** para cada evidencia, cuántos estudiantes en
  esos mismos cuatro estados, más una **categoría de brecha** calculada:
  "Brecha aparente", "Datos insuficientes" o "Sin brecha aparente"
  (ADR-017 las redujo de 4 a 3; ADR-023 amplió qué cuenta hacia "Datos
  insuficientes"). **Los umbrales los fija el sistema, no el docente**
  (ADR-013, que revierte ese punto de ADR-010 — no hay datos para
  defender un corte universal, pero tampoco una interfaz donde el docente
  pudiera ajustarlo). Es el aporte que ninguna otra parte del sistema
  puede dar — algo que un docente con 30-40 estudiantes no puede armar a
  mano.

**Y una segunda vista, aparte** (ADR-010 punto 4) — *diseñada:
pestaña Estudiantes (`14-spec`) e historial del estudiante (`27-spec`);
antes decía "todavía sin construir", corregido 2026-10-21*:

- **Vista de estudiantes (aula):** listado del grupo con detalle por
  estudiante — qué material vio y su estado por evidencia. Historial
  dentro de la experiencia, consultable, no agregado: qué pregunta se le
  mostró, en qué orden, qué respondió y con cuánta certeza.

---

## Unidad

**Estado:** pendiente — nombre y ubicación en la jerarquía, sin definir a fondo

La agrupación ordenada de varias experiencias (varios DBA) dentro de una
secuencia mayor que el docente arma. Fuera de alcance de esta versión —
se retoma cuando experiencia esté cerrada y probada.

---

## Inscripción

**Estado:** propuesto — 2026-10-21, **pendiente de que Alejandro lo
confirme** (regla de este glosario: ningún término se cierra sin eso).
Se agrega en el barrido de coherencia antes de Fase III: el término
aparece en el MER, en las pantallas y en el modelo conceptual, y no
tenía entrada propia.

El vínculo entre un estudiante y una experiencia: existe desde que el
estudiante se une con el código de invitación que comparte el docente
(`08-spec-unirse-codigo.md`), y solo si la experiencia está Publicada.
Un estudiante puede tener varias inscripciones (una por experiencia), y
una experiencia agrupa a muchos estudiantes. Todo lo que el estudiante
hace en el diagnóstico —qué preguntas se le mostraron, qué respondió,
sus resultados— cuelga de su inscripción, no de su cuenta en general.

El estudiante puede **salir** de una experiencia: su inscripción se
elimina y, con ella, lo que respondió (`25-spec`): se borra en cascada
solo lo de ese estudiante (ADR-035, que cierra el vacío V-11).
