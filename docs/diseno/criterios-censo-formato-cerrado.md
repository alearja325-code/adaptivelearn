# Criterios del censo de formato cerrado (QA-014)

**Escrito:** 2026-11-10. **Estado:** propuesta, la aprueba Alejandro.
**Para qué:** decidir, para cada una de las **1282 evidencias** del
catálogo (`data/curriculo-men/catalogo/catalogo_dba.json`), si se puede
diagnosticar con una pregunta cerrada y con cuál de los tres formatos.
El resultado llena la tabla `evidencia_dictamen` (`aplica_formato_cerrado`,
`formato`, `justificacion`, `fecha_dictamen`; RI-19), que necesita el
incremento I2: *"el formato de los ítems lo determina la evidencia"*
(RF-03-01).

**Fuentes:** ADR-006 (la regla de formato, con su muestra de 8
evidencias), QA-012 (esta versión es solo de formato cerrado, y el
diagnóstico puede apoyarse en un subconjunto de las evidencias, porque el
MEN las trata como "pistas" colectivas), QA-014 (el censo) y ADR-002 (el
método es más débil en Lenguaje y Ciencias Sociales).

## Quién lo hace, y con qué honestidad

No hay en el equipo un juicio pedagógico experto disponible ahora. Por
eso:

1. **Una sesión de Claude en la nube aplica estos criterios** a las 1282
   evidencias, una por una, con su justificación. Lo hace **una sola
   vez**, y el resultado queda en el repositorio, revisable. No lo decide
   la IA que genera las preguntas, en cada generación: daría respuestas
   distintas cada vez.
2. **El resultado queda marcado como "propuesto por IA, sin validar"**
   en el archivo del censo, hasta que el equipo lo valide (sección 5).
   No se presenta como juicio del equipo.
3. **Segunda red:** el docente que usa el sistema revisa cada pregunta
   antes de publicar la experiencia (ADR-026).

## 1. La pregunta, para cada evidencia

> ¿Se puede **observar** esta evidencia en un estudiante con una
> pregunta que tenga **una sola respuesta correcta** (elegir, emparejar u
> ordenar), **sin cambiar lo que la evidencia pide**?

Si la pregunta cerrada solo mide algo más fácil que lo que la evidencia
pide (reconocer en vez de producir), la respuesta es **no**.

## 2. Cuándo NO aplica

Se revisan en orden; la primera que se cumple decide.

| Regla | No aplica cuando la evidencia pide… | Señales típicas | Ejemplo real |
|---|---|---|---|
| **N1. Producir** | que el estudiante **haga un producto**, y la calidad de ese producto es la evidencia | escribe, redacta, produce textos, elabora (un texto, una maqueta, una tabla propia), dibuja, crea, diseña y lleva a cabo, define un plan | MAT-11-09 #2: *"Define el plan de recolección de la información…"* |
| **N2. Comunicar en vivo** | hablar, escuchar o interactuar con otros | participa en conversaciones, expone oralmente, debate, dialoga, dramatiza | LEN-03-07 #1: *"Participa en comunicaciones orales…"* |
| **N3. Sostener una postura propia** | defender una opinión, una valoración o una propuesta personal: **no existe una única respuesta correcta**, y fijar una como "la correcta" le impondría una postura al estudiante | argumenta, asume una postura, propone, valora, opina, toma decisiones | CS-10-04 #4: *"Argumenta el papel desempeñado por los organismos…"* |
| **N4. Actuar en el mundo** | manipular objetos o instrumentos reales, o observar el entorno | mide con instrumentos, usa la regla y el compás, observa y registra, recolecta datos, experimenta | CN-04-03 #3: *"Observa y registra algunos patrones de regularidad…"* |
| **N5. Una actitud o disposición** | un comportamiento sostenido, no un conocimiento | respeta, cuida, muestra interés, se responsabiliza, asume con respeto | LEN 5° DBA-5 (de ADR-006): *"asume una postura crítica y respetuosa"* |

**"Explica" sí aplica** (ADR-006): explicar un hecho tiene una
explicación correcta y otras equivocadas, y se mide con opción múltiple
(Force Concept Inventory, Haladyna). La diferencia con N3 es esa: la
explicación de un hecho tiene una respuesta correcta; una postura propia,
no.

## 3. Si aplica, qué formato (ADR-006)

| Formato | Cuándo | Señales |
|---|---|---|
| **`ordering`** | La evidencia es **explícitamente** secuencial: pasos, etapas, orden temporal | ordena, secuencia, establece el orden, cronología, etapas de un proceso |
| **`matching`** | La evidencia relaciona **explícitamente** dos conjuntos finitos | relaciona, asocia, clasifica según, distingue entre, diferencia… de… |
| **`single_choice`** | **Todo lo demás** (el formato por defecto) | reconoce, identifica, compara, interpreta, explica, estima, predice, resuelve, representa, describe |

Ante la duda entre dos formatos, `single_choice`.

## 4. Casos difíciles

- **Evidencias compuestas** (*"Identifica X y escribe Y"*): se dictamina
  por la **acción principal**, normalmente el primer verbo, que el resto
  complementa. Si aplica, la justificación dice qué parte no queda
  cubierta. Ejemplo: LEN-07-01 #2, *"Selecciona la información principal
  … y la utiliza para apoyar sus producciones"*: aplica
  (`single_choice`), y el diagnóstico cubre "selecciona", no "la utiliza
  en sus producciones".
- **Contexto procedimental en el enunciado** (*"Explica … a partir de
  resultados obtenidos en procedimientos…"*): el procedimiento se puede
  describir en la pregunta; decide el verbo principal.
- **"Representa"**: aplica si se puede elegir la representación correcta
  entre varias (una gráfica, una expresión). Si pide construirla a mano,
  N1.
- **Dudoso:** si después de aplicar las reglas no queda claro, se
  dictamina igual, pero se marca `dudoso` con la razón. Los dudosos van
  primero a la validación.

## 5. Cómo se valida

1. **Muestra al azar de 40 evidencias, 10 por área**, más todas las
   marcadas `dudoso`. La muestra la saca un script con semilla fija,
   para que se pueda repetir.
2. Dos integrantes del equipo, por separado, dicen si están de acuerdo
   con cada dictamen (aplica o no, y formato).
3. **Si discrepan con más de 6 de las 40 (15 %)**, los criterios se
   corrigen y el censo se vuelve a correr. Si no, el censo pasa a
   "validado por muestreo" con la fecha y quiénes lo validaron.

## 6. Qué produce

En `data/curriculo-men/censo/`:

- `censo_formato_cerrado.json`: por evidencia, `aplica`, `formato`,
  `regla` (N1 a N5, o el formato y su señal), `justificacion` (una o dos
  frases que citan el verbo o la frase decisiva), `dudoso`, y el estado
  general del censo (`propuesto-por-ia` o `validado-por-muestreo`).
- `informe-censo.md`: cuántas aplican por área y por grado, y con qué
  formato. **Esto responde la pregunta de fondo de QA-014:** si en
  alguna área aplica una proporción baja, el diagnóstico automático
  dejaría fuera buena parte de esa área, y el informe tiene que decirlo
  claramente.
- `muestra_validacion.md`: las 40 evidencias (más las dudosas), con el
  dictamen y una casilla para cada validador.

## 7. Prueba de los criterios con 20 evidencias reales

Muestra al azar, semilla `20261110`, 5 por área, clasificada a mano con
estos criterios antes de escribirlos en firme:

| Evidencia | Texto (abreviado) | Dictamen |
|---|---|---|
| MAT-04-11 #4 | Anticipa los posibles resultados de una situación aleatoria | aplica · `single_choice` |
| MAT-09-04 #1 | Estima la capacidad de objetos con superficies redondas | aplica · `single_choice` |
| MAT-03-05 #1 | Compara objetos según su longitud, área, capacidad… | aplica · `single_choice` |
| MAT-08-04 #4 | Interpreta las expresiones algebraicas que representan el volumen… | aplica · `single_choice` |
| MAT-11-09 #2 | Define el plan de recolección de la información… | **no aplica** · N1 |
| LEN-08-07 #3 | Prepara una estructura retórica… para debates, plenarias y sustentaciones | **no aplica** · N1 y N2 |
| LEN-07-01 #2 | Selecciona la información principal… y la utiliza para sus producciones | aplica · `single_choice` (solo "selecciona") |
| LEN-06-02 #1 | Utiliza los organizadores gráficos para procesar la información… | **no aplica** · N1, `dudoso` |
| LEN-03-07 #1 | Participa en comunicaciones orales… | **no aplica** · N2 |
| LEN-10-04 #2 | Determina las características de los textos literarios… y los relaciona… | aplica · `single_choice` |
| CN-05-04 #3 | Explica por qué al hacer ejercicio aumentan la frecuencia cardíaca y la respiratoria… | aplica · `single_choice` |
| CN-04-03 #3 | Observa y registra patrones de regularidad, elabora tablas y comunica… | **no aplica** · N4 |
| CN-09-02 #1 | Compara algunas teorías (Arrhenius, Brönsted–Lowry, Lewis)… | aplica · `single_choice` |
| CN-09-03 #1 | Explica qué factores afectan la formación de soluciones… | aplica · `single_choice` |
| CN-07-01 #3 | Representa gráficamente las energías cinética y potencial… | aplica · `single_choice` (elegir la gráfica correcta) |
| CS-09-05 #2 | Examina las implicaciones… y sugiere mecanismos constitucionales | aplica · `single_choice` (solo "examina") |
| CS-03-02 #4 | Expresa por qué en ciertos climas no se cuenta con ciertos productos… | aplica · `single_choice` |
| CS-06-06 #1 | Reconoce algunas formas de gobierno de las sociedades antiguas… | aplica · `single_choice` |
| CS-10-04 #4 | Argumenta el papel de los organismos nacionales e internacionales… | **no aplica** · N3 |
| CS-08-02 #2 | Reconoce los niveles en el Índice de Desarrollo Humano… | aplica · `single_choice` |

**Resultado:** aplican 14 de 20 (70 %). Por área: Matemáticas 4 de 5,
Lenguaje 2 de 5, Ciencias Naturales 4 de 5, Ciencias Sociales 4 de 5.
Lenguaje queda más bajo, como ya advertía ADR-002. En la muestra no salió
ningún `ordering` ni `matching`: son formatos para casos explícitos, y es
esperable que sean minoría. Es una muestra de 20, no una estimación: la
cifra real la da el censo.
