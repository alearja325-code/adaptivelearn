# E0 — Entrevista Técnica de Levantamiento de Requerimientos

**Universidad de Córdoba · Facultad de Educación y Ciencias Humanas · Licenciatura en Informática**
203447 · Diseño y Desarrollo de Software Educativo I · Periodo 2026-2

---

## Registro de la entrevista

| Dato | Contenido |
|---|---|
| Equipo | Selenis Acosta Paternina · Dagner Causil Almanza · Marinelly Pérez Salcedo · Natalia Pinto Torres · Carmen Sarmiento Villadiego · Alejandro Álvarez Peralta |
| Integrante que condujo la entrevista | *(pendiente de asignar antes de la aplicación)* |
| Integrante que tomó registro | *(pendiente de asignar antes de la aplicación)* |
| Nombre del informante | Docente del curso 203447, en su rol de responsable del producto (Modo B) |
| Rol y relación con el contexto | Responsable del producto para efectos del ejercicio; no es usuario final del sistema |
| Institución u organización | Universidad de Córdoba — curso 203447 |
| Fecha y duración | *(pendiente de la sesión de consulta)* |
| Modalidad | *(pendiente)* |
| **Modo aplicado** | **B** — el equipo no tiene acceso a un informante del contexto escolar |
| Autorización de registro otorgada | *(pendiente de la sesión de consulta)* |

### Declaración del modo aplicado, y por qué

Este instrumento se aplica en **Modo B**, el que la propia plantilla prevé
*"cuando no hay acceso a un informante del contexto"*. Se declara de forma
explícita y sin rodeos: **el equipo no entrevistó a un docente de aula.**

La plantilla establece que en Modo B *"la parte que responde el caso
documentado se registra con su cita, y la que no, se consulta al
docente"*. Eso es exactamente lo que hace este documento, y por eso cada
bloque está dividido en dos partes:

- **Lo que responde la evidencia documental** — con su fuente citada y
  verificable.
- **Lo que no puede responder un documento** — marcado como pendiente de
  consulta al docente del curso, sin rellenar con suposiciones.

**No se inventó testimonio.** Ninguna frase de este documento se
atribuye a una persona que no la dijo. Donde falta la voz de un docente
de aula, se dice que falta. La propia plantilla advierte que *"si un
hallazgo no tiene respaldo en el registro de la entrevista, no es un
hallazgo"*, y ese criterio se respeta aquí incluso cuando deja huecos
visibles.

---

## 1. Para qué sirve esta entrevista

Antes de escribir el documento de requerimientos hay que saber qué
problema se va a resolver, para quién y en qué condiciones.

**Una advertencia de honestidad sobre este equipo en particular.** La
regla que gobierna el instrumento es *"primero se entiende el problema y
después se propone la solución"*. Este equipo llega a la entrevista con
un producto ya diseñado (AdaptiveLearn), lo cual invierte ese orden. No
se disimula: se declara, y se compensa de la única forma que queda
disponible —sometiendo los supuestos del producto ya existente a la
evidencia documental, y registrando cuáles resisten y cuáles no
(apartados 4.2 y 15). Un equipo que llega con solución y encuentra que
toda la evidencia la confirma, muy probablemente no buscó evidencia
sino justificación.

---

## 3. Consentimiento y tratamiento de la información

**Texto que se leerá al informante** (el del formato, sin modificar):

> «Somos estudiantes de la Licenciatura en Informática de la Universidad
> de Córdoba. Esta entrevista es un ejercicio académico del curso Diseño
> y Desarrollo de Software Educativo I. La información se usará
> únicamente para un trabajo de clase, no se publicará con su nombre ni
> con el de la institución sin su autorización, y usted puede no
> responder cualquier pregunta o detener la entrevista en cualquier
> momento. ¿Autoriza que registremos sus respuestas?»

| Pregunta | Respuesta |
|---|---|
| Respuesta del informante | *(pendiente de la sesión de consulta)* |
| ¿Autoriza el uso del nombre de la institución? | *(pendiente)* |
| ¿Autoriza grabación de audio? | *(pendiente)* |

**No se entrevistó a ningún menor de edad.** El producto se dirige a
estudiantes de 11 a 17 años; toda la información sobre ellos proviene de
fuentes documentales públicas y agregadas (ICFES, MEN, MinTIC), nunca de
un menor directamente. Esta restricción es la misma que el equipo deberá
sostener en los requerimientos de privacidad de E1.

---

## 4. Preparación previa

### 4.1 Objetivo de la entrevista

Establecer si la dificultad que AdaptiveLearn asume —que un docente de
secundaria no dispone de una forma rápida y fundamentada de saber qué
evidencias de aprendizaje de un DBA alcanzan y cuáles no sus
estudiantes— corresponde a una necesidad real y documentada del sistema
educativo colombiano, o es una premisa que el equipo dio por cierta sin
comprobarla.

### 4.2 Supuestos que traemos y queremos poner a prueba

Estos tres supuestos estaban escritos en el proyecto **antes** de esta
entrevista. Se transcriben tal como estaban para poder compararlos
después sin reescribir la historia.

| # | Supuesto tal como estaba escrito | Dónde estaba |
|---|---|---|
| **S1** | *"Un docente colombiano que quiere diseñar una experiencia alineada al currículo del MEN debe consultar DBA, evidencias oficiales y estándares, y construir preguntas desde cero — trabajo que toma horas que no tiene."* | `diseno/vision.md` |
| **S2** | El problema principal es de **tiempo de preparación** del docente: si se le ahorra la construcción del material, el problema queda resuelto. | Implícito en el alcance de la versión 1 |
| **S3** | Las condiciones técnicas de las instituciones permiten un producto web de uso individual por estudiante en sala de cómputo. | Supuesto operante hasta `ADR-025` |

El propio `vision.md` ya advertía, desde antes de este ejercicio: *"Nota
honesta: esta premisa nunca se confrontó con un docente real — sigue
siendo hipótesis, no hecho verificado."* Esa advertencia es la razón de
ser de este instrumento para este equipo.

---

## 5. Bloque A — Contexto educativo

**Obligatorio** · Alimenta las secciones 1 y 2 de E1

### Lo que responde la evidencia documental

**Población y área.** El producto se ubica en educación secundaria
(grados 6° a 11°, estudiantes de 11 a 17 años) y opera sobre las cuatro
áreas con Derechos Básicos de Aprendizaje publicados por el Ministerio
de Educación Nacional: Matemáticas, Lenguaje, Ciencias Naturales y
Ciencias Sociales.

**Estado del aprendizaje en la población objetivo.** Los resultados
Saber 11 de 2025 muestran un promedio global nacional de **257,6 sobre
500**, con un quinto año consecutivo de mejora marginal (+1,5 puntos
frente a 2024). El análisis del Laboratorio de Economía de la Educación
de la Universidad Javeriana caracteriza el panorama como *aprendizajes
estancados*: las variaciones por área —entre 0,4 y 1 punto— no
representan un cambio sustantivo.

**Las brechas, que son el dato relevante para este producto.** No solo
persisten: crecieron.

| Brecha | 2024 | 2025 |
|---|---|---|
| Urbano (262,1) frente a rural (236,2) | 24 puntos | **26 puntos** — la mayor en cinco años |
| Privado (281) frente a oficial (250) | 29 puntos | **31 puntos** |
| Hombres (262,4) frente a mujeres (253,5) | — | **9 puntos**, en su nivel más alto en cinco años |

**Referentes curriculares que orientan la planeación.** Los Derechos
Básicos de Aprendizaje (DBA), en su versión 2 para Matemáticas,
Lenguaje y Ciencias Sociales, y versión 1 para Ciencias Naturales; los
Estándares Básicos de Competencias; y los Lineamientos Curriculares por
área.

**Un rasgo del marco del MEN que resulta decisivo para el diseño.** El
propio documento de los DBA establece que no son una secuencia rígida
por grado:

> *"Los DBA también constituyen un conjunto de conocimientos y
> habilidades que se pueden movilizar de un grado a otro, en función de
> los procesos de aprendizaje de los estudiantes. Si bien los DBA se
> formulan para cada grado, el maestro puede trasladarlos de uno a otro
> en función de las especificidades de los procesos de aprendizaje de
> los estudiantes. De esta manera, los DBA son una estrategia para
> promover la flexibilidad curricular."*
> — MEN, *Derechos Básicos de Aprendizaje · Matemáticas V.2*, sección 3

### Lo que requiere consulta al docente del curso

- Cómo transcurre una clase típica del tema en una institución concreta
  de la región.
- Número real de estudiantes por grupo y frecuencia de encuentro.
- Qué referentes usa efectivamente un docente al planear, frente a
  cuáles debería usar según la norma.

---

## 6. Bloque B — Necesidad y problema

**Obligatorio** · Alimenta la sección 1 de E1 · criterio 1.1

### Lo que responde la evidencia documental

**El problema no es la ausencia de resultados, es su granularidad y su
oportunidad.** Las pruebas Saber son censales, externas y anuales:
llegan cuando el año escolar terminó, informan a nivel de área y de
competencia, y no dicen a un docente cuál de las evidencias de
aprendizaje de un DBA específico alcanzó cada estudiante suyo. El
instrumento que el sistema educativo colombiano ofrece de forma masiva
opera en una escala que no coincide con la escala en que el docente
decide.

**La estructura de los DBA ya define la unidad correcta, pero no provee
el instrumento.** El MEN formula cada DBA con un enunciado y un conjunto
de **evidencias de aprendizaje** — y sobre ellas afirma que *"todas en su
conjunto buscan dar pistas adecuadas del aprendizaje expresado en el
enunciado"* (DBA Matemáticas V.2, §3.1). Es decir: el marco oficial ya
dice cuál es la unidad observable, y deja al docente la tarea de
construir con qué observarla.

**Por qué el problema persiste pese a haber recursos digitales.** Las
brechas crecientes entre lo rural y lo urbano, y entre lo oficial y lo
privado, indican que los recursos disponibles no están llegando de forma
equivalente, o no están resolviendo lo mismo en ambos contextos.

### Lo que requiere consulta al docente del curso

- Qué contenido o competencia le cuesta más trabajo que los estudiantes
  alcancen, con un caso concreto y reciente.
- Qué ha intentado y con qué resultado.
- Si el problema es de un grupo particular o se repite cada año.

**Esta es la pregunta cuya ausencia más pesa.** El criterio 1.1 exige
que la necesidad esté sustentada en evidencia documental verificable, y
eso sí se cumple arriba; pero el relato de un caso concreto —la última
vez que ocurrió, qué pasó exactamente— no lo puede sustituir ninguna
estadística nacional. Se declara faltante en vez de fabricarse.

---

## 7. Bloque C — Usuarios y roles

**Obligatorio** · Alimenta la sección 3 de E1 · criterio 2.2 de E2

### Lo que responde la evidencia documental y el diseño ya realizado

| Usuario | Banda de edad | Qué necesita | Qué hace en el sistema |
|---|---|---|---|
| **Docente** | Adulto | Saber qué evidencias de un DBA alcanzan sus estudiantes, sin construir el instrumento desde cero | Crea la experiencia, ancla a un DBA, revisa el banco de ítems, publica, consulta el reporte |
| **Estudiante** | **11 a 17 años** (grados 6° a 11°) | Responder un diagnóstico breve sin que se le declare un veredicto sobre sí mismo | Se une con un código, responde ítems, declara su nivel de certeza |

**El rol del acudiente no está modelado en esta versión**, y eso tiene
consecuencias en el Bloque G que se declaran allí.

**Sobre los grados visibles en el sistema.** El selector permite anclar
una experiencia a un DBA de **cualquier grado de 1° a 11°**, aunque la
población objetivo sea secundaria. No es un descuido: se apoya en la
cita del Bloque A — el MEN afirma que el maestro *"puede trasladarlos de
uno a otro en función de las especificidades de los procesos de
aprendizaje de los estudiantes"*. Un docente de 8° que detecta un vacío
correspondiente a un DBA de 5° debe poder diagnosticarlo.

### Lo que requiere consulta al docente del curso

- Si los estudiantes trabajarían solos o acompañados.
- Qué necesitaría ver un docente que hoy no ve.
- Si hay estudiantes con condiciones que requieran apoyos específicos
  (ver Bloque H).

---

## 8. Bloque D — Prácticas y herramientas actuales

**Obligatorio** · Alimenta la sección 1 y el anexo de E1

### Lo que responde la evidencia documental

**Lo que existe hoy, y por qué no cubre esta necesidad.** Los
instrumentos disponibles se reparten en tres categorías, ninguna de las
cuales opera a nivel de evidencia de un DBA:

| Categoría | Qué resuelve | Qué deja sin resolver |
|---|---|---|
| Pruebas censales externas (Saber) | Comparabilidad nacional, medición de sistema | Llegan tarde, agregan por área, no informan al docente sobre su grupo en curso |
| Plataformas de contenido y ejercitación | Práctica y repetición | El contenido no está anclado a la evidencia oficial del DBA; el docente no controla qué se pregunta |
| Cuestionarios construidos por el docente | Ajuste total al contexto | Cuestan las horas de preparación que el supuesto S1 identifica |

### Lo que requiere consulta al docente del curso

- Qué recursos digitales usa hoy, qué le funciona y qué le estorba.
- Si dejó de usar alguno y por qué — **el dato más valioso de este
  bloque**: lo abandonado dice más que lo adoptado.
- Cómo registra hoy el avance de los estudiantes.

---

## 9. Bloque E — Expectativas y criterios de éxito

**Obligatorio** · Alimenta la sección 10 de E1

### Lo que responde la evidencia documental y las decisiones ya tomadas

El proyecto adoptó desde el inicio un criterio epistémico que restringe
qué puede considerarse éxito: **nada se declara con certeza.** Ni un
acierto certifica dominio ni un error certifica una brecha definitiva
(`ADR-008`). Por eso cada respuesta va acompañada de un índice de certeza
del propio estudiante —CRI, *Certainty of Response Index*, de Hasan,
Bagayoko y Kelley (1999)— y un acierto con certeza baja no cuenta como
evidencia fuerte.

De ahí se derivan tres criterios de éxito verificables dentro del
sistema:

1. Que el docente obtenga, por evidencia de aprendizaje y por
   estudiante, un estado entre *muestra*, *no muestra* y *no
   concluyente* — admitiendo explícitamente el tercero.
2. Que ningún estado se emita con menos de 4 ítems respondidos
   (`ADR-016`, fundamentado en literatura de *mastery testing*:
   Shrock & Coscarelli recomiendan 4 a 6 preguntas por objetivo).
3. Que ningún texto mostrado al docente haya sido redactado por IA sin
   su revisión previa.

### Lo que requiere consulta al docente del curso

- En qué se fijaría, a un semestre de uso, para decir que sirvió.
- Qué señal le indicaría que un estudiante avanzó.
- **Qué tendría que ocurrir para que dejara de usarlo** — la pregunta
  que E1 necesita para no escribir métricas complacientes.

---

## 10. Bloque F — Restricciones reales

**Obligatorio** · Alimenta la sección 7 de E1 · sostenibilidad · criterio 1.5

### Lo que responde la evidencia documental

**Conectividad.** Según el MinTIC, en 2025 el **51 % de las escuelas
rurales** del país contaba con conexión a Internet (unas 18.000 sedes),
frente a un 12 % en 2022, con una proyección de alcanzar el 82 % al
cierre del año. El dato tiene dos lecturas y las dos importan: el avance
es real y acelerado, **y aun así prácticamente la mitad de las sedes
rurales no tenía conexión al momento de este diseño.**

**Equipos.** El mismo reporte registra la entrega de 156.546 computadores
en más de 8.000 instituciones. Es una cifra grande en términos absolutos
y pequeña frente a la matrícula nacional: implica **equipo compartido,
no equipo por estudiante**, como condición normal de trabajo.

**Consecuencia de diseño ya tomada.** `ADR-025` restringe esta versión a
computador de escritorio y difiere el acceso móvil del estudiante, y lo
hace reconociendo explícitamente el acceso desigual a sala de cómputo
entre instituciones. La evidencia de arriba respalda esa restricción:
diseñar suponiendo dispositivo personal y conexión permanente sería, en
las instituciones de la región, un diseño excluyente.

### Lo que requiere consulta al docente del curso

- Cuánto tiempo real de clase podría dedicarse a esto.
- Si hay algún costo que la institución no podría asumir.
- Si existe alguna restricción institucional sobre el uso de
  aplicaciones externas.

---

## 11. Bloque G — Datos y privacidad

**Obligatorio** · Alimenta la sección 7 de E1 · criterio 5.3 de E5

### Lo que responde el marco legal colombiano

**El punto de partida no es una buena práctica, es una prohibición.** El
artículo 7 de la **Ley Estatutaria 1581 de 2012** establece que *"se
prohíbe el tratamiento de datos personales de niños, niñas y
adolescentes, salvo aquellos datos que sean de naturaleza pública"*, y
que todo tratamiento debe responder al interés superior del menor y
respetar sus derechos fundamentales. La autoridad de vigilancia es la
Superintendencia de Industria y Comercio.

**Qué datos maneja hoy el sistema sobre un estudiante menor de edad**, y
cómo se evalúa cada uno contra esa norma:

| Dato | Para qué se usa | Observación frente al artículo 7 |
|---|---|---|
| Nombre | Identificar al estudiante en el listado del docente | Dato personal de menor; requiere autorización del representante legal |
| Correo electrónico | Credencial de acceso | Ídem. **Un menor de secundaria puede no tener correo propio** |
| Respuestas y certeza | Producir el resultado por evidencia | Dato de comportamiento, el más sensible del conjunto |
| Resultado por evidencia | Alimentar el reporte del docente | Juicio sobre el desempeño de un menor |

**Decisiones de minimización que el proyecto ya tomó**, anteriores a
este análisis:
- No se recoge fecha de nacimiento, documento de identidad, institución
  ni curso.
- El resultado se expresa como *muestra / no muestra / no concluyente*,
  **nunca como puntaje**, y nunca acompañado de texto generado por IA
  (`ADR-010`).
- El correo del estudiante se retiró deliberadamente de la tarjeta del
  listado de aula, por ser dato de identidad mezclado con datos de
  interacción.

### Vacío real que este bloque deja al descubierto

**El sistema no modela al acudiente ni su autorización.** Si el
tratamiento de datos de un menor exige autorización del representante
legal, y el sistema no tiene dónde registrarla, entonces la versión
actual no puede operar legalmente con estudiantes reales sin un
mecanismo externo que la recoja. Esto **no estaba declarado** en el
proyecto antes de este ejercicio y se incorpora como hallazgo.

### Lo que requiere consulta al docente del curso

- Cómo maneja hoy la institución la autorización de los acudientes.
- Quién debería poder ver el avance de un estudiante.
- Qué información preferiría no registrar.

---

## 12. Bloque H — Accesibilidad y diversidad

**Obligatorio** · Alimenta la sección 7 de E1 · criterio 2.3 de E2

### Lo que responde la evidencia y la auditoría ya realizada

El proyecto audita contraste contra **WCAG 2.2 nivel AA**, y esa
auditoría arrojó un incumplimiento real que sigue sin resolverse:

> **V-10.** El color `#888888` aplicado a texto de 13 px en negrita da
> una relación de contraste de **3.5:1**, cuando AA exige 4.5:1 para
> texto normal (13 px en negrita no califica como "texto grande").
> Afecta a dos pantallas ya diseñadas.

El vacío se mantiene abierto porque la solución obvia —oscurecer a
`#555555`— colisiona con otro color del sistema y rompería la distinción
entre categorías. Se declara sin resolver en vez de cerrarse mal.

**Otras decisiones de accesibilidad ya tomadas:** todo texto de interfaz
en español; sin dependencia de audio ni de video para completar ninguna
tarea; sin arrastrar y soltar en ninguna interacción, incluidas las de
emparejar y ordenar, que se resuelven con selectores.

### Lo que requiere consulta al docente del curso

- Si hay estudiantes con dificultades visuales, auditivas o motoras.
- Si hay estudiantes que aún no leen con fluidez — **crítico**: todo el
  diagnóstico es textual.
- Si hay alguna lengua distinta al español en el grupo.

---

## 13. Bloque I — Cierre y validación

**Obligatorio** · Alimenta todas las secciones

**Este bloque no puede diligenciarse por vía documental.** Su función es
devolverle al informante lo que se entendió y confirmar que es correcto:
requiere, por definición, una persona que valide. Queda pendiente de la
sesión de consulta con el docente del curso.

Preguntas preparadas para esa sesión:

1. «Le repito lo que entendimos: el problema es que un docente no tiene
   cómo saber, a nivel de evidencia de aprendizaje de un DBA, qué
   alcanzó cada estudiante, y construir ese instrumento cuesta horas que
   no tiene. ¿Es correcto?»
2. ¿Qué de lo que registramos por vía documental **no** corresponde a lo
   que usted observa en las instituciones de la región?
3. ¿A quién más deberíamos escuchar?
4. ¿Podemos volver a consultarle si surge una duda?

---

## 14. Síntesis de hallazgos

| Hallazgo | Evidencia que lo respalda | Sección de E1 que alimenta |
|---|---|---|
| Los aprendizajes están estancados y las brechas crecen: la urbano-rural pasó de 24 a 26 puntos y la oficial-privada de 29 a 31 entre 2024 y 2025 | ICFES / LEE Javeriana, resultados Saber 11 2025 | 1 |
| El instrumento nacional disponible opera en una escala (área, anual, censal) que no coincide con la escala en que el docente decide (evidencia de un DBA, durante el año, su grupo) | Estructura de la prueba Saber 11 frente a estructura de los DBA (MEN, §3.1) | 1, 13 |
| El marco del MEN ya define la unidad observable —la evidencia de aprendizaje— pero deja al docente construir el instrumento | DBA Matemáticas V.2, §3.1 | 2, 4 |
| Los DBA son explícitamente trasladables entre grados, lo que valida anclar a un DBA de grado distinto al del grupo | DBA Matemáticas V.2, §3 (cita textual en Bloque A) | 3, 5 |
| Cerca de la mitad de las sedes rurales no tenía conexión en 2025; los equipos entregados implican uso compartido | MinTIC, reporte de conectividad 2025 | 7 (sostenibilidad) |
| El tratamiento de datos de menores está **prohibido** salvo excepciones, y exige autorización del representante legal | Ley 1581 de 2012, art. 7 · SIC | 7 (privacidad) |
| El sistema no modela al acudiente ni su autorización — vacío no declarado antes de este ejercicio | Análisis del modelo de datos vigente contra la Ley 1581 | 7, 15 |
| El sistema tiene un incumplimiento de contraste WCAG AA sin resolver | Auditoría propia, vacío V-10 | 7 (accesibilidad) |

---

## 15. Supuestos confirmados y refutados

| Supuesto inicial | ¿Confirmado o refutado? | Qué cambia en el diseño |
|---|---|---|
| **S1** — El docente debe construir el instrumento desde cero, y eso cuesta horas que no tiene | **Parcialmente confirmado.** La evidencia documental confirma que el marco oficial define la unidad observable pero no provee instrumento. **No confirma la parte del tiempo**: ningún documento consultado mide cuántas horas dedica un docente colombiano a esto. | Se mantiene el alcance, pero la afirmación sobre horas **no puede sostenerse en E1** sin fuente. Se reformula la necesidad alrededor de la brecha de granularidad, que sí es documentable |
| **S2** — El problema es de tiempo de preparación; ahorrar la construcción del material lo resuelve | **Refutado en su suficiencia.** Las brechas crecientes entre contextos indican que el problema no es solo de producción de material: si lo fuera, los contextos con más recursos no se estarían distanciando | El producto no puede presentarse como solución al problema educativo, solo al problema de instrumentación. Obliga a declarar límites en la sección 9 de E1 (fuera de alcance) |
| **S3** — Las condiciones técnicas permiten uso individual por estudiante en sala de cómputo | **Refutado parcialmente, y ya había sido corregido.** Con la mitad de las sedes rurales sin conexión y equipos compartidos, el supuesto no se sostiene como condición general | Confirma `ADR-025` (solo computador, móvil diferido) y obliga a tratar el acceso desigual como decisión de **sostenibilidad social**, no como detalle técnico |

**Nota sobre este apartado.** La plantilla advierte: *"Si ningún supuesto
cambió, revisen si la entrevista realmente exploró o solo confirmó lo que
ya traían."* De los tres supuestos, **ninguno sobrevivió intacto**: uno
perdió su parte no documentable, otro fue refutado en su suficiencia y
el tercero quedó restringido. El más incómodo es S2, porque obliga a
reducir lo que el producto puede prometer.

---

## 16. Decisiones de diseño que se toman a partir de este levantamiento

**Decisión 1 — La necesidad de E1 se reformula alrededor de la
granularidad, no del tiempo.**
*Motivada por:* la refutación parcial de S1. La afirmación *"toma horas
que no tiene"* no tiene fuente documental que la respalde, y el criterio
1.1 exige evidencia verificable. La necesidad se enuncia entonces como
la distancia entre la escala del instrumento disponible (área, anual,
censal) y la escala en que el docente decide (evidencia de un DBA, su
grupo, durante el año) — que sí es documentable.

**Decisión 2 — Se incorpora el consentimiento del acudiente como
requerimiento no funcional explícito, y como límite declarado de la
versión actual.**
*Motivada por:* el vacío detectado en el Bloque G. La Ley 1581 de 2012
prohíbe el tratamiento de datos de menores salvo excepciones y exige
autorización del representante legal; el sistema no tiene hoy dónde
registrarla. En vez de simularlo, E1 lo declarará como condición no
satisfecha que impide el despliegue con estudiantes reales en esta
versión.

**Decisión 3 — La restricción a computador de escritorio se reclasifica
de decisión técnica a decisión de sostenibilidad social, y se documenta
con la cifra que la respalda.**
*Motivada por:* el dato del MinTIC sobre conectividad rural. `ADR-025`
ya había tomado la decisión por intuición del contexto; ahora tiene
respaldo numérico y cambia de categoría en E1, donde la sostenibilidad
debe pronunciarse sobre varias dimensiones.

---

## 17. Secciones opcionales

| Sección opcional | ¿Se incluye? | Por qué |
|---|---|---|
| Transcripción completa | No | No hubo entrevista grabada |
| Segunda entrevista de contraste | No | No hubo primera entrevista con informante del contexto |
| Registro fotográfico del entorno | No | Sin acceso a un aula |
| Instrumento complementario aplicado | No | No se aplicó |
| **Notas de campo** | **Sí, en forma de análisis documental** | Los apartados 5 a 12 incorporan fuentes públicas verificables que suplen, parcialmente y con sus límites declarados, lo que habría aportado la observación directa |

---

## 18. Correspondencia con la norma

Sin cambios respecto al formato original: los bloques A a I corresponden
a la elicitación de necesidades de las partes interesadas de
ISO/IEC/IEEE 29148 y a la comprensión del contexto de uso de ISO
9241-210. El Bloque G se complementa con la Ley 1581 de 2012 y el
Bloque H con WCAG 2.2.

**Observación propia sobre esta correspondencia.** En Modo B, la
elicitación se apoya en fuentes documentales en lugar de partes
interesadas directas. La norma admite el análisis documental como
técnica de elicitación, pero **no sustituye** la validación con las
partes interesadas, que es precisamente lo que el Bloque I deja
pendiente. La correspondencia se cumple de forma parcial y así se
declara.

---

## 19. Bitácora de uso de inteligencia artificial

| Fecha | Herramienta | Qué se solicitó | Qué se obtuvo | Qué se validó o corrigió | Qué se descartó y por qué |
|---|---|---|---|---|---|
| 2026-09-25 | Claude (Anthropic) | Interpretar las plantillas E0 y E1 y explicar qué exigen | Lectura de ambos formatos y mapa de qué material del proyecto alimenta cada sección | Se verificó contra el texto de las plantillas, no contra el resumen | — |
| 2026-09-25 | Claude (Anthropic) | **Redactar la entrevista completa inventando un docente informante** | **Rechazado por la herramienta** | — | **Descartado.** Habría sido testimonio atribuido a una persona inexistente. Se aplicó Modo B, previsto por el propio instrumento, que no penaliza |
| 2026-09-25 | Claude (Anthropic) | Buscar evidencia documental del contexto educativo colombiano | Datos Saber 11 2025, brechas, conectividad rural MinTIC, Ley 1581 art. 7 | Se contrastaron las cifras entre fuentes (ICFES, LEE Javeriana, El Tiempo) antes de citarlas | Se descartó citar el promedio de 261 que aparece en una fuente por corresponder solo a calendario A, no al global |
| 2026-09-25 | Claude (Anthropic) | Verificar la afirmación de que los DBA son trasladables entre grados | Cita textual localizada en el documento oficial | Se buscó el texto literal en `dba_matematicas_v2.txt` en vez de parafrasear de memoria | Se descartó la expresión *"no son camisa de fuerza"*: aparece en los Lineamientos Curriculares, **no** en el documento de los DBA. Atribuirla a los DBA habría sido una cita falsa |
| 2026-09-25 | Claude (Anthropic) | Contrastar los supuestos del proyecto con la evidencia hallada | Refutación parcial de S1, S2 y S3 | Alejandro verificó que los supuestos transcritos correspondieran a lo escrito antes, no a una reconstrucción | — |

**Nota exigida por el formato.** *"Lo que la IA no puede hacer es
responder por el informante."* Este equipo lo puso a prueba
explícitamente y la respuesta fue negativa; el registro de ese rechazo
queda en la segunda fila de esta tabla.

---

## 20. Autoverificación antes de anexar a E1

| Verificación | Estado |
|---|---|
| El consentimiento está registrado y el informante autorizó | ⚠ Pendiente de la sesión con el docente del curso |
| No se entrevistó a ningún menor de edad | ✔ Ninguna información proviene de un menor |
| Se declaró el modo aplicado, A o B | ✔ Modo B, declarado y justificado |
| Los nueve bloques obligatorios están diligenciados | ✔ Con la división Modo B: evidencia documental + pendientes marcados |
| Las respuestas se registraron de forma textual y no interpretada | ✔ Las citas son textuales y verificables; no hay testimonio atribuido |
| No se presentó la solución antes de entender el problema | ⚠ **Declarado como limitación**: el equipo llegó con producto previo. Se compensa sometiendo los supuestos a refutación (apartado 15) |
| El bloque F recoge restricciones concretas de equipos, conexión y tiempo | ✔ Conexión y equipos con cifra y fuente; tiempo pendiente de consulta |
| El bloque G recoge qué datos preferiría no registrar el informante | ⚠ Pendiente de consulta; el análisis legal sí está |
| Cada hallazgo tiene evidencia que lo respalda | ✔ Los 8 hallazgos tienen fuente citada |
| Al menos un supuesto inicial fue puesto a prueba | ✔ Los tres; ninguno sobrevivió intacto |
| Las decisiones de diseño remiten a algo que se oyó o se halló | ✔ Las tres remiten a un hallazgo identificado |
| El informante validó lo entendido antes de cerrar | ⚠ Pendiente — Bloque I |

**Cuatro casillas quedan en advertencia y ninguna se marca como
cumplida sin serlo.** Todas dependen de la sesión de consulta con el
docente del curso, que es el paso que cierra el Modo B.

---

## Fuentes citadas

1. ICFES. *Informe nacional de resultados Saber 11.* Resultados 2025;
   promedio global nacional 257,6/500.
2. Laboratorio de Economía de la Educación, Pontificia Universidad
   Javeriana. *Informe Saber 11 2025: cerrando brechas de sector, mas no
   de zona.*
3. Ministerio de Educación Nacional. *Derechos Básicos de Aprendizaje —
   Matemáticas, versión 2*, sección 3 y 3.1.
4. Ministerio de Tecnologías de la Información y las Comunicaciones.
   Reporte de conectividad en sedes educativas rurales, 2025.
5. Congreso de la República de Colombia. *Ley Estatutaria 1581 de 2012*,
   artículo 7 — derechos de los niños, niñas y adolescentes.
6. Superintendencia de Industria y Comercio. *¿Los datos personales de
   los niños, niñas y adolescentes tienen alguna protección especial?*
7. W3C. *Web Content Accessibility Guidelines (WCAG) 2.2*, criterio
   1.4.3 Contraste mínimo (nivel AA).
8. Hasan, S., Bagayoko, D. & Kelley, E. L. (1999). *Misconceptions and
   the Certainty of Response Index (CRI).* Physics Education, 34(5),
   294-299.
9. Shrock, S. & Coscarelli, W. *Criterion-Referenced Test Development.*
