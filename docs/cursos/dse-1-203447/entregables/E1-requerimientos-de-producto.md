# E1 — Documento de Requerimientos de Producto

**Universidad de Córdoba · Facultad de Educación y Ciencias Humanas · Licenciatura en Informática**
203447 · Diseño y Desarrollo de Software Educativo I · Periodo 2026-2

| Dato | Contenido |
|---|---|
| Nombre del equipo | *(pendiente de definir)* |
| Integrantes | Selenis Acosta Paternina · Dagner Causil Almanza · Marinelly Pérez Salcedo · Natalia Pinto Torres · Carmen Sarmiento Villadiego · Alejandro Álvarez Peralta |
| Producto que diseñan | **AdaptiveLearn** — diagnóstico por evidencias de aprendizaje, anclado a los DBA del MEN |
| Enlace al repositorio | *(pendiente de publicar — ver nota CT-03 al final)* |
| Fecha de entrega real | *(pendiente)* |
| Versión del documento | 1.0 |

> **Anexo obligatorio:** este documento se acompaña de `E0 — Entrevista
> Técnica`, aplicado en **Modo B**. Sin él la entrega no es admisible.

---

## 1. Contexto y necesidad educativa

**Obligatoria** · Corte 1

### Contexto

Educación secundaria oficial colombiana, grados 6° a 11°. Los resultados
Saber 11 de 2025 arrojaron un promedio global nacional de **257,6 sobre
500** — quinto año consecutivo de mejora, pero de magnitud marginal
(+1,5 puntos frente a 2024). El análisis del Laboratorio de Economía de
la Educación de la Universidad Javeriana caracteriza el conjunto como
*aprendizajes estancados*: las variaciones por área, de entre 0,4 y 1
punto, no representan cambio sustantivo.

Lo que sí cambió son las brechas, y cambiaron en la dirección
equivocada:

| Brecha | 2024 | 2025 |
|---|---|---|
| Urbano (262,1) — rural (236,2) | 24 puntos | **26 puntos**, la mayor en cinco años |
| Privado (281) — oficial (250) | 29 puntos | **31 puntos** |
| Hombres (262,4) — mujeres (253,5) | — | **9 puntos**, el más alto en cinco años |

### Necesidad identificada

**Existe una distancia estructural entre la escala en que el sistema
educativo mide y la escala en que el docente decide.**

El instrumento de evaluación disponible de forma masiva —las pruebas
Saber— es censal, externo y anual: informa por área y competencia, y sus
resultados llegan cuando el año escolar ya terminó. El docente, en
cambio, decide durante el año, sobre su grupo, y respecto de aprendizajes
concretos.

El marco curricular oficial **ya define cuál es la unidad observable en
esa escala menor**: los Derechos Básicos de Aprendizaje se formulan con
un enunciado y un conjunto de **evidencias de aprendizaje**, sobre las
cuales el MEN afirma que *"todas en su conjunto buscan dar pistas
adecuadas del aprendizaje expresado en el enunciado"*. Pero el marco
define la unidad y **no provee el instrumento** para observarla. Esa es
la necesidad.

### Fuente de la que proviene

1. ICFES, *Informe nacional de resultados Saber 11*, resultados 2025.
2. Laboratorio de Economía de la Educación, Pontificia Universidad
   Javeriana, *Informe Saber 11 2025*.
3. Ministerio de Educación Nacional, *Derechos Básicos de Aprendizaje —
   Matemáticas V.2*, secciones 3 y 3.1.

### Evidencia que la sustenta, y qué NO sustenta

La evidencia documental sostiene que el problema de granularidad existe
y que las brechas crecen.

**Lo que la evidencia no sostiene, y por eso no se afirma aquí:** el
equipo partía del supuesto de que construir el instrumento *"toma horas
que el docente no tiene"*. Ninguna de las fuentes consultadas mide el
tiempo que un docente colombiano dedica a diseñar evaluación formativa.
Ese supuesto fue **refutado en su parte no documentable** durante el
levantamiento (E0, apartado 15) y la necesidad se reformuló alrededor de
la granularidad, que sí es verificable.

> **Declaración de orden, exigida por el criterio 1.1.** Este equipo
> llegó al levantamiento con un producto previamente diseñado, lo que
> invierte el orden que el instrumento prescribe. No se disimula: se
> declara, y se compensó sometiendo los tres supuestos de partida a
> refutación documental. Ninguno sobrevivió intacto (E0, apartado 15).
> Un equipo que encuentra que toda la evidencia confirma lo que ya
> traía, probablemente buscó justificación y no evidencia.

---

## 2. Referentes curriculares del área

**Obligatoria** · Corte 1

### Área y grado

Cuatro áreas con DBA publicados: Matemáticas, Lenguaje, Ciencias
Naturales y Ciencias Sociales. Grados 6° a 11° como población objetivo.

### Referente utilizado

**Derechos Básicos de Aprendizaje (DBA)** — versión 2 para Matemáticas,
Lenguaje y Ciencias Sociales; versión 1 para Ciencias Naturales.
Complementados por los Estándares Básicos de Competencias y los
Lineamientos Curriculares por área.

### Aprendizajes del referente que aborda el producto

El producto **no define aprendizajes propios**. Opera exclusivamente
sobre las evidencias de aprendizaje que el MEN ya formuló para cada DBA.
Esta es una decisión declarada del proyecto: *el sistema no se atribuye
autoridad curricular que no tiene*.

En consecuencia, la estructura del referente baja directamente al modelo
de datos: un DBA tiene evidencias; una experiencia se ancla a un único
DBA y diagnostica las evidencias de ese DBA; el resultado se emite **por
evidencia**, nunca como un puntaje global.

### Una lectura del referente que condiciona el diseño

Los DBA **no son una secuencia rígida por grado**. El documento oficial
lo establece:

> *"Los DBA también constituyen un conjunto de conocimientos y
> habilidades que se pueden movilizar de un grado a otro […] Si bien los
> DBA se formulan para cada grado, el maestro puede trasladarlos de uno
> a otro en función de las especificidades de los procesos de
> aprendizaje de los estudiantes. De esta manera, los DBA son una
> estrategia para promover la flexibilidad curricular."*
> — MEN, *DBA Matemáticas V.2*, sección 3

Por eso el sistema permite anclar una experiencia a un DBA **de
cualquier grado entre 1° y 11°**, aunque los usuarios sean de
secundaria: un docente de 8° que detecta un vacío correspondiente a un
DBA de 5° debe poder diagnosticarlo. Restringir el selector al grado del
grupo habría contradicho al propio referente.

---

## 3. Usuarios y roles

**Obligatoria** · Corte 1

### Usuario 1 — Docente

| Atributo | Descripción |
|---|---|
| Perfil | Docente de educación secundaria oficial, de una de las cuatro áreas con DBA |
| Banda de edad | Adulto (mayor de edad) |
| Necesidad | Saber, por evidencia de aprendizaje y por estudiante, qué alcanza y qué no su grupo, sin construir el instrumento desde cero |
| Acciones | Crea una experiencia y la ancla a un DBA · revisa y edita el banco de ítems generado · publica · comparte el código de invitación · consulta el reporte por evidencia y por estudiante |

### Usuario 2 — Estudiante

| Atributo | Descripción |
|---|---|
| Perfil | Estudiante de secundaria, grados 6° a 11° |
| **Banda de edad** | **11 a 17 años — menores de edad.** Este dato condiciona todas las decisiones de privacidad (sección 7) y de interfaz (E2) |
| Necesidad | Responder un diagnóstico breve, sin que el sistema le declare un veredicto sobre sí mismo |
| Acciones | Se une con un código · responde ítems uno a uno · declara su nivel de certeza en cada respuesta |

### Usuario 3 — Acudiente o representante legal

| Atributo | Descripción |
|---|---|
| Perfil | Representante legal del estudiante menor de edad |
| Banda de edad | Adulto |
| Necesidad | Autorizar el tratamiento de los datos de su representado, exigido por la Ley 1581 de 2012 |
| Acciones | **Ninguna en esta versión.** El rol se identifica pero **no está modelado en el sistema** |

> **Consecuencia declarada.** Que el acudiente no esté modelado no es una
> omisión menor: significa que la versión actual **no puede desplegarse
> con estudiantes reales** sin un mecanismo externo que recoja esa
> autorización. Ver sección 7 y sección 15.

---

## 4. Propuesta pedagógica

**Obligatoria** · Corte 1

### Modelo o enfoque pedagógico, y por qué

**Evaluación formativa criterio-referenciada, con medición de certeza.**

Criterio-referenciada significa que el resultado se compara contra un
criterio externo —la evidencia de aprendizaje del DBA— y no contra el
desempeño de los demás estudiantes. No hay ranking, no hay percentil, no
hay nota.

Se eligió este enfoque porque **se deriva directamente de la necesidad
de la sección 1**: si el problema es que la medición disponible no opera
a nivel de evidencia, el enfoque tiene que ser uno cuyo criterio *sea* la
evidencia. Un enfoque normativo habría reproducido, a menor escala, el
mismo problema que se quiere resolver.

### El componente que distingue esta propuesta: la certeza

Cada respuesta va acompañada del **CRI** (*Certainty of Response Index*,
Hasan, Bagayoko y Kelley, 1999), una escala de 0 a 5 en la que el propio
estudiante declara qué tan seguro estaba.

Su función es epistémica: **un acierto con certeza baja no es evidencia
de que el estudiante muestra el aprendizaje** —pudo adivinar—, y un
error con certeza baja tampoco es evidencia firme de que no lo muestra.
Ambos casos quedan como señal débil. Sin esta medida, un diagnóstico de
opción cerrada confunde sistemáticamente saber con acertar.

### Competencias u objetivos de aprendizaje

Los del DBA al que se ancle cada experiencia. **El producto no formula
objetivos propios** — ver sección 2.

### Criterios de logro dentro del sistema

El sistema emite, por evidencia y por estudiante, uno de tres estados:

| Estado | Cuándo se emite |
|---|---|
| **Muestra** | Mayoría de señales fuertes en esa dirección (acierto + certeza alta) |
| **No muestra** | Mayoría de señales fuertes en la dirección contraria (error + certeza alta) |
| **No concluyente** | No hay mayoría clara al llegar al tope de ítems |

Dos reglas restringen cuándo puede emitirse:

1. **Mínimo 4 ítems respondidos**, siempre. Ninguna conclusión se emite
   con menos, por decisiva que parezca la primera respuesta.
2. **Tope de 6 ítems.** Si al sexto no hay mayoría clara, el estado es
   *no concluyente* y ahí se detiene, para no fatigar al estudiante.

El rango 4-6 no se fijó a ojo: procede de la literatura de *mastery
testing*. Shrock y Coscarelli recomiendan de 4 a 6 preguntas por
objetivo, y una fuente independiente sugiere al menos 5 cuando la prueba
tiene consecuencias reales.

> **Por qué *no concluyente* es un resultado legítimo y no una falla.**
> Un sistema que siempre emite veredicto afirma más de lo que sus datos
> sostienen. Admitir que con 6 ítems no se puede concluir es más
> honesto, y más útil para el docente, que forzar una respuesta.

---

## 5. Funcionalidades

**Obligatoria** · Corte 1

**F1 — Autenticación y perfil.** Registro e ingreso por correo y
contraseña o por proveedor externo; verificación de correo; recuperación
de contraseña; elección de rol (docente o estudiante), irreversible.

**F2 — Creación de la experiencia (docente).** Selección de área,
selección del DBA con sus evidencias, confirmación. Al confirmar, el
sistema genera automáticamente el banco de ítems.

**F3 — Revisión del banco (docente).** Consulta de los ítems generados
por IA, con su formato y sus opciones; edición del enunciado y del
contenido; exclusión reversible de ítems.

**F4 — Publicación e invitación (docente).** Paso de borrador a
publicada; generación y consulta de un código de invitación de 6
caracteres.

**F5 — Ingreso a la experiencia (estudiante).** Unirse con el código;
consultar las experiencias a las que pertenece y el estado de su propio
avance.

**F6 — Toma del diagnóstico (estudiante).** Presentación de ítems uno a
uno, en tres formatos (selección única, emparejar, ordenar); captura de
la respuesta y de la certeza.

**F7 — Reporte (docente).** Estado general por estudiante y estado por
evidencia para todo el grupo, con categorización de brecha por umbral
fijo.

**F8 — Vista de aula (docente).** Listado del grupo agrupado por estado,
con detalle por estudiante.

---

## 6. Requerimientos funcionales

**Obligatoria** · Corte 1

Enunciados de forma que permitan decidir sin discusión si se cumplieron.

| ID | Requerimiento |
|---|---|
| **RF-01** | El sistema debe permitir que un docente cree una experiencia anclada a **exactamente un** DBA. |
| **RF-02** | El sistema debe generar, al confirmarse la creación, un banco de **12 ítems por cada evidencia incluida** del DBA anclado. |
| **RF-03** | El sistema debe permitir al docente excluir un ítem del banco de forma **reversible**, sin eliminarlo. |
| **RF-04** | El sistema debe generar un código de invitación de **6 caracteres alfanuméricos**, único, sin los caracteres `0`, `O`, `1`, `I` ni `L`. |
| **RF-05** | El sistema debe impedir que un estudiante se una a una experiencia en estado *borrador*. |
| **RF-06** | El sistema debe impedir que un mismo estudiante quede inscrito dos veces en la misma experiencia. |
| **RF-07** | El sistema debe presentar los ítems **uno a uno** y registrar, por cada presentación, el orden y el momento en que ocurrió. |
| **RF-08** | El sistema debe exigir, por cada respuesta, un valor de certeza **entero entre 0 y 5**. |
| **RF-09** | El sistema debe registrar **qué opción u opciones** eligió el estudiante, no solo si la respuesta fue correcta. |
| **RF-10** | El sistema debe presentar **como mínimo 4 ítems** por evidencia antes de emitir cualquier estado. |
| **RF-11** | El sistema debe detener la presentación de ítems de una evidencia al alcanzar **6 ítems**, y emitir *no concluyente* si no hay mayoría clara. |
| **RF-12** | El sistema debe poder distinguir un ítem que se presentó y no fue respondido, de uno que nunca se presentó. |
| **RF-13** | El sistema debe emitir, por cada evidencia y cada estudiante, exactamente uno de tres estados: *muestra*, *no muestra* o *no concluyente*, con la fecha de cálculo. |
| **RF-14** | El sistema debe impedir la modificación de un ítem o de sus opciones una vez que ese ítem **ya fue presentado** a algún estudiante. |
| **RF-15** | El sistema no debe mostrar al estudiante ningún resultado, estado ni veredicto sobre su propio desempeño. |
| **RF-16** | El sistema debe mostrar al docente el conteo de estudiantes en cada estado, por evidencia, en formato `X/total`. |

---

## 7. Requerimientos no funcionales

**Obligatoria** · Corte 1

### 7.1 Privacidad y protección de datos de menores

El punto de partida no es una buena práctica: es una prohibición legal.
El **artículo 7 de la Ley Estatutaria 1581 de 2012** prohíbe el
tratamiento de datos personales de niños, niñas y adolescentes salvo los
de naturaleza pública, y exige que todo tratamiento responda al interés
superior del menor. La autoridad de vigilancia es la Superintendencia de
Industria y Comercio.

| ID | Requerimiento |
|---|---|
| **RNF-01** | El sistema debe recoger del estudiante **únicamente** nombre y correo. No debe recoger documento de identidad, fecha de nacimiento, institución, curso ni fotografía obligatoria. |
| **RNF-02** | El sistema **no debe** expresar el resultado de un estudiante como puntaje, nota ni percentil; solo como uno de los tres estados definidos. |
| **RNF-03** | El resultado de un estudiante debe ser visible **únicamente** para el docente de esa experiencia. |
| **RNF-04** | El sistema debe registrar la autorización del representante legal antes de tratar datos de un estudiante menor de edad. |

> **RNF-04 no está satisfecho en esta versión, y se declara.** El
> sistema no modela al acudiente ni dispone de dónde registrar esa
> autorización. **Consecuencia: la versión 1 no puede desplegarse con
> estudiantes reales**; solo con datos de prueba o en demostración ante
> docentes. Declararlo es preferible a simular un cumplimiento que no
> existe.

### 7.2 Accesibilidad

Referencia: **WCAG 2.2, nivel AA**.

| ID | Requerimiento |
|---|---|
| **RNF-05** | Todo texto debe cumplir una relación de contraste mínima de **4.5:1** sobre su fondo. |
| **RNF-06** | Ninguna tarea debe requerir arrastrar y soltar. Emparejar y ordenar deben resolverse con selectores. |
| **RNF-07** | Ninguna tarea debe depender de audio o video para completarse. |
| **RNF-08** | Ningún estado debe comunicarse **solo** por color. |

> **RNF-05 tiene un incumplimiento conocido y sin resolver.** La
> auditoría propia detectó que el gris `#888888` sobre texto de 13 px en
> negrita da **3.5:1**, por debajo del mínimo. Afecta a dos pantallas ya
> diseñadas. No se cerró en falso porque la corrección obvia —oscurecer
> el gris— colisiona con otro color del sistema y rompería la distinción
> entre categorías de resultado. Queda como defecto declarado.

### 7.3 Sostenibilidad

El curso exige pronunciarse sobre más de una dimensión. Son cuatro y no
dicen lo mismo.

**Social — la dimensión decisiva en este contexto.** Según el MinTIC, en
2025 el **51 % de las sedes educativas rurales** contaba con conexión a
Internet (unas 18.000 sedes), frente al 12 % de 2022. El avance es real;
aun así, cerca de la mitad de las sedes rurales no tenía conexión al
momento de este diseño. En equipos, los 156.546 computadores entregados
en más de 8.000 instituciones implican **uso compartido, no equipo por
estudiante**.

| ID | Requerimiento |
|---|---|
| **RNF-09** | El sistema debe funcionar en computador de escritorio de gama baja, sin exigir dispositivo personal por estudiante. |
| **RNF-10** | El diagnóstico debe poder completarse en **una sesión de clase**, sin requerir trabajo en casa. |

**Técnica.** El banco se genera una sola vez, al crear la experiencia, y
no se regenera en cada uso: la llamada costosa a un modelo de lenguaje
ocurre una vez por experiencia, no una vez por estudiante.

**Económica.** Sin costo por estudiante ni licencia por institución en
el alcance de esta versión. Se descartó deliberadamente la integración
con Apple por requerir una cuenta de desarrollador de pago (99 USD/año)
sin beneficio para una plataforma web.

**Ambiental.** Consecuencia directa de la técnica: generar el banco una
vez por experiencia, y no por sesión, reduce el consumo de cómputo
asociado a los modelos de lenguaje, que es donde está el grueso de la
huella de este producto.

### 7.4 Uso de inteligencia artificial en el producto

| ID | Requerimiento |
|---|---|
| **RNF-11** | Todo contenido generado por IA debe ser **revisable y editable** por el docente antes de que cualquier estudiante lo vea. |
| **RNF-12** | El sistema debe distinguir y registrar si un ítem está **tal como lo generó la IA** o si el docente ya lo intervino. |
| **RNF-13** | Ningún texto mostrado en el reporte al docente debe ser redactado por IA. Los estados se calculan; no se narran. |
| **RNF-14** | La IA debe generar ítems **únicamente** a partir de la evidencia oficial del DBA, no de contenido libre. |

> **Por qué RNF-13.** Un texto generado que interprete el desempeño de
> un menor introduciría un juicio sin responsable identificable. El
> sistema calcula estados y los muestra; la interpretación es del
> docente.

### 7.5 Otros

| ID | Requerimiento |
|---|---|
| **RNF-15** | Interfaz íntegramente en español. |
| **RNF-16** | La generación del banco de una experiencia debe completarse sin requerir que el docente permanezca esperando en la pantalla. |

---

## 8. Alcance por versión

**Obligatoria** · Corte 1

### Versión 1 — el diagnóstico completo, de punta a punta

Autenticación y roles · creación de la experiencia anclada a un DBA ·
generación y revisión del banco · publicación e invitación · toma del
diagnóstico por el estudiante con captura de certeza · cálculo del estado
por evidencia · reporte al docente.

**Es la mínima que ya entrega valor educativo** porque cierra el ciclo
completo: sin la toma del diagnóstico no hay dato, y sin el reporte el
dato no llega a quien decide.

### Versión 2

Práctica focalizada sobre las evidencias en estado *no muestra*, y
verificación posterior. Su diseño pedagógico ya existe, pero está
deliberadamente fuera de la versión 1: diagnóstico y práctica están
acoplados, y construir la práctica sobre un diagnóstico aún no validado
arriesga trabajo desperdiciado.

También en v2: registro del consentimiento del acudiente (RNF-04), que
es lo que habilita el despliegue con estudiantes reales.

### Versiones posteriores

Acceso desde dispositivo móvil para el estudiante · unidades con varias
experiencias conectadas · biblioteca curada por uso real · versionado del
contenido de los ítems.

---

## 9. Fuera de alcance

**Obligatoria** · Corte 1

| No se hará | Motivo |
|---|---|
| Asignar nota, puntaje o calificación | Contradice el enfoque criterio-referenciado. El producto informa al docente; la calificación es decisión suya y de su institución |
| Nombrar la causa del error del estudiante | Los distractores se construyen con hipótesis de error, pero **no se reportan como diagnóstico de causa**. Nombrar la causa exigiría una validación empírica que el proyecto no tiene |
| Mostrar al estudiante su propio resultado | El producto está diseñado para informar una decisión docente, no para devolverle un juicio a un menor sobre sí mismo |
| Preguntas abiertas | Requieren calificación automática de texto libre, cuya fiabilidad no se puede sostener con el rigor que el resto del producto exige |
| Acceso móvil del estudiante en v1 | Decisión de sostenibilidad: en el contexto documentado, el escenario realista es la sala de cómputo compartida |
| Funcionar sin conexión | Reconocido como limitación real frente al 49 % de sedes rurales sin conexión. **No se resuelve y no se disimula** |
| Que el docente decida cuántos ítems ve el estudiante | Se evaluó y se revirtió: la cantidad la fija el sistema con la regla 4-6, fundamentada en literatura. Dejarla al docente era asignar una responsabilidad sin criterio que la respalde |

> Delimitar es una decisión de diseño. Las dos últimas filas registran
> decisiones que el equipo tomó y **luego revocó**, con su razón.

---

## 10. Métricas de éxito

**Obligatoria** · Corte 1

### Métrica de aprendizaje

**M1 — Cambio de estado por evidencia entre dos aplicaciones.** Para las
evidencias que en una primera aplicación quedaron en *no muestra*, y
sobre las cuales el docente declara haber intervenido, se mide qué
proporción cambia a *muestra* en una segunda aplicación del mismo
diagnóstico.

*Meta de referencia:* que al menos el 40 % de las evidencias
intervenidas cambie de estado.

> **Límite honesto de M1.** Requiere una segunda aplicación, que es
> funcionalidad de la **versión 2**. En la versión 1 esta métrica **no
> es medible**. Se declara así en vez de sustituirla por una métrica de
> uso disfrazada de aprendizaje.

**M2 — Concordancia con el juicio del docente.** Proporción de
estudiantes en los que el estado emitido por el sistema coincide con lo
que el docente, de forma independiente y antes de ver el reporte,
esperaba de ese estudiante en esa evidencia.

*Meta de referencia:* concordancia superior al 70 %, con las
discordancias revisadas una a una.

> M2 sí es medible en la versión 1, y mide algo pedagógicamente
> relevante: si el instrumento discrimina. Una concordancia del 100 %
> sería sospechosa —significaría que el sistema no aporta información
> que el docente no tuviera ya.

### Métrica de uso

**M3 — Tasa de finalización.** Proporción de estudiantes inscritos que
completan el diagnóstico de todas las evidencias de la experiencia.
*Meta:* superior al 85 % dentro de una sesión de clase.

**M4 — Intervención del docente sobre el banco.** Proporción de ítems
que el docente edita o excluye antes de publicar. *Sin meta numérica,
pero se vigila:* un 0 % indicaría que el docente no está revisando, y la
revisión previa es una garantía central del producto.

### Métrica de calidad

**M5 — Tasa de *no concluyente*.** Proporción de pares
estudiante-evidencia que terminan sin conclusión tras los 6 ítems.
*Meta:* por debajo del 25 %. Una tasa superior indicaría que los ítems
no discriminan.

---

## 11. Anexo: comparación de modelos y selección de la metodología

**Obligatoria** · Corte 1

### Declaración previa

El proyecto **ya venía trabajando con MODESEC** cuando se elaboró esta
comparación. Esto no es, por tanto, una evaluación previa a la elección;
es la justificación de una elección ya tomada, y se presenta como tal.
Presentarla como deliberación inicial sería falsear el proceso.

### Criterios de comparación

| Criterio | Por qué importa en este proyecto |
|---|---|
| **C1** — ¿Trata el diseño pedagógico como una fase propia? | Un producto educativo cuyo modelo pedagógico se improvisa es un producto cualquiera con contenido escolar |
| **C2** — ¿Produce artefactos verificables en cada fase? | El equipo necesitaba poder comprobar mecánicamente que un documento no contradice a otro |
| **C3** — ¿Tolera requisitos cambiantes? | El modelo de datos cambió cinco veces en dos meses |
| **C4** — ¿Es practicable por un equipo de estudiantes sin cliente real disponible? | Restricción efectiva de este equipo, documentada en E0 (Modo B) |
| **C5** — ¿Encaja con la evaluación por entregables del curso? | Restricción institucional |

### Los tres modelos frente a cada criterio

| | **MODESEC** | **ADDIE** | **Scrum** |
|---|---|---|---|
| **C1** Diseño pedagógico como fase | **Sí.** La Fase I completa es diseño educativo antes de tocar interfaz | **Sí.** Análisis y Diseño son instruccionales por definición | **No.** Es un marco de gestión; el contenido pedagógico le es ajeno |
| **C2** Artefactos verificables | **Sí.** Cada fase tiene entregables nombrados (MER, MR, diccionario, ventanas) | Parcial. Define fases, no artefactos concretos | Parcial. Define incrementos y ceremonias, no documentos |
| **C3** Tolerancia al cambio | Media. Las fases son secuenciales; rehacer una arrastra las siguientes | Baja en su forma clásica; media en sus variantes iterativas | **Alta.** Es su razón de ser |
| **C4** Sin cliente disponible | **Alta.** Se apoya en referentes curriculares documentados, no en un cliente | Alta | **Baja.** Depende de un *Product Owner* que priorice |
| **C5** Encaje con el curso | **Alto.** Es la metodología del programa | Medio | Medio |

### Metodología elegida y consecuencias de la elección

**MODESEC**, por C1, C2 y C4: es la única de las tres que trata el diseño
educativo como fase con entregables propios, y la que mejor funciona sin
un cliente disponible —que es exactamente la situación documentada en E0.

**Las consecuencias, incluidas las malas:**

1. **C3 es su punto débil, y se pagó.** El modelo entidad-relación pasó
   por cinco revisiones. En una de ellas se descubrió que el modelo
   relacional había quedado **dos revisiones atrás** sin que nadie lo
   notara, porque la secuencialidad de MODESEC no obliga a revisar
   aguas abajo cuando cambia algo aguas arriba.
2. **Se compensó con herramientas propias.** El equipo construyó
   verificadores automáticos que comparan cada documento contra su
   fuente. Esa compensación **no viene de MODESEC**: es trabajo que la
   metodología no pide y que hubo que agregar.
3. **Se adoptó un elemento ajeno:** límite de trabajo en curso, de
   Kanban. La causa del desorden en una etapa anterior no fue falta de
   documentos, fue tener demasiados abiertos sin cerrar ninguno.

> Elegir MODESEC no fue elegir bien en todo. Fue elegir el que mejor
> resolvía C1, C2 y C4, y **asumir el costo de C3 construyendo algo que
> la metodología no trae**.

---

## 12. Bitácora de uso de inteligencia artificial

**Obligatoria** · Corte 1 · 8 % de la nota del documento

| Fecha | Herramienta | Qué se solicitó | Qué se obtuvo | Qué se validó o corrigió | Qué se descartó y por qué |
|---|---|---|---|---|---|
| 2026-09-25 | Claude | Interpretar las plantillas E0 y E1 | Lectura de ambas y mapa de qué material del proyecto alimenta cada sección | Se verificó contra el texto de las plantillas | — |
| 2026-09-25 | Claude | **Redactar la entrevista E0 inventando un docente informante** | **Rechazado por la herramienta** | — | **Descartado.** Era testimonio atribuido a persona inexistente. Se aplicó Modo B, previsto por el instrumento y sin penalización |
| 2026-09-25 | Claude | Buscar evidencia del contexto educativo colombiano | Saber 11 2025, brechas, conectividad MinTIC, Ley 1581 art. 7 | Cifras contrastadas entre ICFES, LEE Javeriana y prensa antes de citarlas | Se descartó el promedio de 261 puntos: corresponde solo a calendario A, no al global |
| 2026-09-25 | Claude | Verificar que los DBA son trasladables entre grados | Cita textual del documento oficial | Se buscó el texto literal en el archivo fuente | Se descartó la expresión *"no son camisa de fuerza"*: está en los Lineamientos, **no** en los DBA. Habría sido cita falsa |
| 2026-09-25 | Claude | Redactar la métrica de aprendizaje de la sección 10 | Propuesta de métrica de cambio de estado entre aplicaciones | Se detectó que **no es medible en la versión 1** y se declaró ese límite en vez de ocultarlo | Se descartó presentar la tasa de finalización como métrica de aprendizaje: es de uso |
| 2026-08 a 09 | Claude | Diseño del modelo de datos y de las 22 ventanas del producto | Modelo entidad-relación, modelo relacional, diccionario y especificaciones | Cada decisión quedó registrada con su alternativa descartada en un registro de 25 decisiones de arquitectura | Se descartaron dos taxonomías (SOLO y Bloom) por no corresponder a la estructura real de las evidencias del MEN |

> **Sobre la exigencia de que la bitácora registre descartes.** Este
> documento registra seis, de los cuales dos son correcciones de errores
> que la IA misma introdujo (una cita mal atribuida y una métrica que no
> medía lo que decía medir).

---

## 13. Problema y oportunidad *(opcional)*

**Por qué el problema persiste.** Los instrumentos existentes resuelven
problemas distintos: las pruebas censales miden el sistema, las
plataformas de contenido ejercitan, y los cuestionarios propios del
docente cuestan tiempo de preparación. Ninguno opera sobre la unidad que
el marco curricular define como observable —la evidencia de aprendizaje—
ni durante el año, sobre el grupo propio.

**Qué oportunidad abre.** Que el MEN haya formulado las evidencias de
aprendizaje de forma explícita y pública significa que **el criterio ya
está escrito**: no hay que inventar qué observar, solo construir con qué
observarlo. Esa es una condición poco común y es la que hace viable un
producto que no se atribuye autoridad curricular propia.

---

## 15. Supuestos y restricciones *(opcional)*

### Supuestos

| # | Supuesto | Estado |
|---|---|---|
| A1 | El docente tiene la voluntad y el tiempo de revisar el banco antes de publicar | **Sin verificar.** Si no revisa, la garantía central de RNF-11 se vuelve nominal |
| A2 | El estudiante declara su certeza con honestidad | **Sin verificar.** Todo el mecanismo depende de esto |
| A3 | El sistema tiene acceso a los DBA normalizados de las cuatro áreas | Parcialmente cierto: la normalización tiene un defecto de extracción conocido y sin corregir |

### Restricciones

| # | Restricción | Origen |
|---|---|---|
| R1 | No se pueden tratar datos de menores sin autorización del representante legal | Ley 1581 de 2012, art. 7 — **restricción legal, no de diseño** |
| R2 | Cerca de la mitad de las sedes rurales no tenía conexión en 2025 | MinTIC |
| R3 | Equipos compartidos, no individuales | MinTIC |
| R4 | El equipo no tuvo acceso a un docente de aula | Documentado en E0, Modo B |
| R5 | La regla exacta que convierte respuestas en estado no está definida | Vacío propio declarado, previo a cualquier implementación |

---

## 16. Glosario *(opcional)*

| Término | Definición |
|---|---|
| **DBA** | Derecho Básico de Aprendizaje. Aprendizaje estructurante que el MEN formula por grado y área |
| **Evidencia de aprendizaje** | Componente de un DBA que describe algo observable en el estudiante. Es la unidad sobre la que opera este producto |
| **Experiencia** | En este producto: un diagnóstico creado por un docente, anclado a un único DBA |
| **CRI** | *Certainty of Response Index.* Escala 0-5 en que el estudiante declara su certeza (Hasan et al., 1999) |
| **Señal fuerte / débil** | Fuerte: respuesta con certeza alta. Débil: certeza baja, no concluye en ninguna dirección |
| **No concluyente** | Estado legítimo cuando 6 ítems no alcanzan mayoría clara. No es una falla del sistema |
| **Evaluación criterio-referenciada** | Compara el desempeño contra un criterio externo, no contra el grupo |

---

## Autoverificación antes de entregar

| Verificación | Estado |
|---|---|
| Las doce secciones obligatorias están presentes | ✔ |
| La necesidad cita fuente documental identificable y no se dedujo de la solución | ✔ Fuentes citadas · la inversión de orden se declara explícitamente en §1 |
| Cada usuario tiene declarada su banda de edad | ✔ Docente adulto · estudiante 11-17 · acudiente adulto |
| La propuesta pedagógica no podría aplicarse igual a otro producto | ✔ Se deriva de la unidad "evidencia de aprendizaje" del MEN |
| Los RNF cubren privacidad, accesibilidad, sostenibilidad y uso de IA | ✔ §7.1 a §7.4 |
| La sostenibilidad se pronuncia sobre más de una dimensión | ✔ Social, técnica, económica y ambiental |
| Fuera de alcance diligenciada y argumentada | ✔ 7 exclusiones con motivo |
| Hay al menos una métrica de aprendizaje | ✔ M1 y M2, con el límite de M1 declarado |
| La comparación de modelos contrasta alternativas | ✔ 3 modelos × 5 criterios, con las consecuencias malas de la elección |
| La bitácora registra al menos un descarte o corrección | ✔ Seis |
| El repositorio registra la distribución de responsabilidades (CT-03) | ⚠ **Pendiente** |
| Video de sustentación de 8 minutos o menos | ⚠ **Pendiente** |

> **Advertencia sobre CT-03.** Es criterio de **admisibilidad**: sin ese
> registro la entrega no se recibe. Hoy no existe repositorio público
> del equipo. Es lo primero que hay que resolver, antes que cualquier
> otra cosa de este documento.

---

## Fuentes

1. ICFES. *Informe nacional de resultados Saber 11*, 2025.
2. Laboratorio de Economía de la Educación, Universidad Javeriana.
   *Informe Saber 11 2025.*
3. MEN. *Derechos Básicos de Aprendizaje — Matemáticas V.2*, §3 y §3.1.
4. MinTIC. Reporte de conectividad en sedes educativas rurales, 2025.
5. Congreso de Colombia. *Ley Estatutaria 1581 de 2012*, art. 7.
6. Superintendencia de Industria y Comercio. Protección especial de
   datos de niños, niñas y adolescentes.
7. W3C. *WCAG 2.2*, criterio 1.4.3 (nivel AA).
8. Hasan, Bagayoko & Kelley (1999). *Misconceptions and the Certainty of
   Response Index.* Physics Education, 34(5), 294-299.
9. Shrock, S. & Coscarelli, W. *Criterion-Referenced Test Development.*
10. Caro & Toscano-Miranda. *MODESEC*, Universidad de Córdoba.
