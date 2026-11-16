# Informe del censo de formato cerrado (QA-014)

**Encargo 05**, Parte B. **Archivo generado** por `generar_censo.py`: no se edita a mano.
**Estado: propuesto por IA, sin validar** (`propuesto-por-ia`, ADR-042). Fecha: 2026-11-16.
Criterios aplicados: `docs/diseno/criterios-censo-formato-cerrado.md`, **versión 2**: aceptados
el 2026-11-10 y ampliados el 2026-11-16 con N6 (contexto propio) y N7 (necesita ver o escuchar),
por decisión de Alejandro (ADR-044). Los dictámenes que cambió la versión 2 dicen «Antes: …»
(huella sha256 `2d824d1b2631bd71…`, en la cabecera del JSON).

## 1. En una frase

De las **1282 evidencias** del catálogo, **859 (67 %) se pueden diagnosticar
con una pregunta cerrada** y 423 no. Por área: Matemáticas 316 de 437 (72 %); Lenguaje 174 de 333 (52 %); Ciencias Naturales 147 de 184 (80 %); Ciencias Sociales 222 de 328 (68 %).

Es un juicio de IA, no del equipo: lo hizo la sesión de Claude del encargo 05, leyendo cada
evidencia y escribiendo su razón (`dictamenes/`). Antes de usarlo como dato del proyecto, dos
integrantes validan la muestra de `muestra_validacion.md` (criterios §5).

## 2. La respuesta a QA-014: ¿alcanza el formato cerrado?

| Área | Evidencias | Aplican | % | No aplican |
|---|---|---|---|---|
| Matemáticas | 437 | 316 | **72 %** | 121 |
| Lenguaje | 333 | 174 | **52 %** | 159 |
| Ciencias Naturales | 184 | 147 | **80 %** | 37 |
| Ciencias Sociales | 328 | 222 | **68 %** | 106 |
| **Total** | 1282 | 859 | **67 %** | 423 |

**Respuesta:** en Matemáticas, Ciencias Naturales y Ciencias Sociales el formato cerrado
alcanza a la mayoría de las evidencias. **En Lenguaje la proporción es baja: algo más de la
mitad.** Casi la mitad de las evidencias de Lenguaje piden hablar, escuchar o escribir, y una
pregunta cerrada no las observa. Es lo que ADR-002 anticipaba. Consecuencia para el diseño:
en Lenguaje el diagnóstico automático cubre sobre todo la comprensión (leer, identificar,
inferir) y deja fuera la producción oral y escrita, que es una parte central del área. El
sistema no lo esconde: el Paso 2 muestra esas evidencias tachadas (`06-spec` §2.4), y qué hacer
con ellas en otra versión es QA-017.

Áreas por debajo del 60 %: Lenguaje.

### 2.1 Por grado

Cuántas aplican de las que hay, por área y grado:

| Área | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° | 10° | 11° |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Matemáticas | 28/39 | 27/35 | 29/41 | 23/39 | 36/51 | 29/42 | 24/31 | 35/44 | 26/38 | 32/41 | 27/36 |
| Lenguaje | 11/33 | 17/34 | 20/34 | 11/32 | 15/26 | 20/31 | 16/28 | 18/28 | 15/29 | 14/28 | 17/30 |
| Ciencias Naturales | 7/16 | 10/12 | 15/20 | 18/23 | 11/14 | 14/16 | 11/13 | 19/19 | 17/21 | 11/12 | 14/18 |
| Ciencias Sociales | 8/32 | 13/32 | 16/32 | 27/32 | 25/32 | 26/32 | 23/32 | 27/32 | 27/32 | 15/20 | 15/20 |

En los primeros grados de Ciencias Sociales muchas evidencias piden saber algo de la vida del
propio estudiante (su familia, su casa, su municipio): ver la sección 6.

## 3. Con qué formato

| Área | single_choice | matching | ordering |
|---|---|---|---|
| Matemáticas | 302 | 10 | 4 |
| Lenguaje | 158 | 13 | 3 |
| Ciencias Naturales | 126 | 21 | 0 |
| Ciencias Sociales | 206 | 15 | 1 |
| **Total** | 792 | 59 | 8 |

`matching` y `ordering` son minoría, como esperaban los criterios (§7): se usan solo cuando la
evidencia nombra explícitamente dos conjuntos que emparejar (clasifica, diferencia… de…,
relaciona X con Y) o un orden (ordena, el orden de los eventos). Ante la duda, `single_choice`.

## 4. Por qué no aplican: cada regla

| Regla | Qué pide la evidencia | Matemáticas | Lenguaje | Ciencias Naturales | Ciencias Sociales | Total |
|---|---|---|---|---|---|---|
| **N1** | producir | 74 | 57 | 6 | 15 | 152 |
| **N2** | comunicar en vivo | 0 | 76 | 0 | 5 | 81 |
| **N3** | sostener una postura propia | 13 | 9 | 5 | 39 | 66 |
| **N4** | actuar en el mundo | 14 | 3 | 21 | 7 | 45 |
| **N5** | una actitud o disposición | 0 | 2 | 0 | 5 | 7 |
| **N6** | contexto propio | 0 | 0 | 1 | 32 | 33 |
| **N7** | necesita ver o escuchar | 20 | 12 | 4 | 3 | 39 |

- **N1 (producir)** es la regla más usada en Matemáticas y Lenguaje: construir tablas y
  gráficas, proponer estrategias, escribir textos.
- **N2 (comunicar en vivo)** es casi toda de Lenguaje: hablar, leer en voz alta, conversar y
  **escuchar**. Las evidencias sobre lo que el estudiante escucha (un discurso, una voz) se
  dictaminaron N2 porque la pregunta del sistema es escrita: leer un texto cambia lo que la
  evidencia pide. Con la versión 2 serían también N7; se dejaron N2.
- **N3 (postura propia)** es sobre todo de Ciencias Sociales: «argumenta» (que los criterios
  fijan como no aplica), «propone acciones», «expresa sus opiniones».
- **N4 (actuar en el mundo)** incluye medir, experimentar y observar.
- **N6 (contexto propio)** es casi toda de Ciencias Sociales de 1° a 3°: la respuesta depende de
  la familia, el barrio, la escuela o el municipio del estudiante (sección 6.1).
- **N7 (necesita ver o escuchar)** reúne lo que mide leer una gráfica, un plano, un mapa, una
  imagen, un gesto o una voz. Esta versión solo genera preguntas de texto (ADR-043, ADR-044).
  Si la tabla o la figura se puede escribir en el enunciado, la evidencia sigue aplicando.

## 5. DBA sin ninguna evidencia que aplique

**25 DBA** quedan sin ninguna evidencia que admita pregunta cerrada. Según QA-012, **no
se pueden usar para crear una experiencia en esta versión**: el banco no tendría de dónde
generar preguntas. (Qué muestra la pantalla en ese caso es el vacío V-12.)

| DBA | Enunciado | Evidencias | Reglas |
|---|---|---|---|
| `MAT-04-06` | Identifica, describe y representa figuras bidimensionales y tridimensionales, y establece relaciones entre ellas. | 2 | N1, N7 |
| `MAT-06-02` | Utiliza las propiedades de los números enteros y racionales y las propiedades de sus operaciones para proponer estrategias y procedimientos de cálculo en la solución de problemas. | 2 | N1, N3 |
| `MAT-06-04` | Utiliza y explica diferentes estrategias (desarrollo de la forma o plantillas) e instrumentos (regla, compás o software) para la construcción de figuras planas y cuerpos. | 3 | N1, N4, N7 |
| `MAT-08-10` | Propone relaciones o modelos funcionales entre variables e identifica y analiza propiedades de covariación entre variables, en contextos numéricos, geométricos y cotidianos y las representa mediante gráficas (cartesianas de puntos, continuas, formadas por segmentos, etc.). | 2 | N3, N7 |
| `LEN-01-02` | Relaciona códigos no verbales, como los movimientos corporales y los gestos de las manos o del rostro, con el significado que pueden tomar de acuerdo con el contexto. | 4 | N1, N2, N7 ×2 |
| `LEN-01-07` | Enuncia textos orales de diferente índole sobre temas de su interés o sugeridos por otros. | 4 | N2 ×4 |
| `LEN-02-07` | Expresa sus ideas atendiendo a las características del contexto comunicativo en que las enuncia (interlocutores, temas, lugares). | 5 | N2 ×5 |
| `LEN-04-02` | Escribe textos a partir de información dispuesta en imágenes, fotografías, manifestaciones artísticas o conversaciones cotidianas. | 3 | N1 ×2, N7 |
| `LEN-04-07` | Participa en espacios de discusión en los que adapta sus emisiones a los requerimientos de la situación comunicativa. | 4 | N2 ×4 |
| `LEN-06-02` | Crea organizadores gráficos en los que integra signos verbales y no verbales para dar cuenta de sus conocimientos. | 4 | N1 ×2, N7 ×2 |
| `LEN-07-05` | Comprende discursos orales producidos con un objetivo determinado en diversos contextos sociales y escolares. | 4 | N2 ×4 |
| `LEN-07-07` | Construye narraciones orales, para lo cual retoma las características de los géneros que quiere relatar y los contextos de circulación de su discurso. | 4 | N1, N2 ×3 |
| `LEN-08-07` | Reconstruye en sus intervenciones el sentido de los textos desde la relación existente entre la temática, los interlocutores y el contexto histórico-cultural. | 3 | N1, N2 ×2 |
| `LEN-09-08` | Produce textos verbales y no verbales, a partir de los planes textuales que elabora, y siguiendo procedimientos sistemáticos de corrección lingüística. | 3 | N1 ×3 |
| `LEN-10-02` | Planea la producción de textos audiovisuales en los que articula elementos verbales y no verbales de la comunicación para desarrollar un tema o una historia. | 3 | N1 ×3 |
| `LEN-10-07` | Produce textos orales como ponencias, comentarios, relatorías o entrevistas, atendiendo a la progresión temática, a los interlocutores, al propósito y a la situación comunicativa. | 4 | N1, N2 ×3 |
| `LEN-11-07` | Expresa por medio de producciones orales el dominio de un tema, un texto o la obra de un autor. | 5 | N1 ×2, N2 ×3 |
| `CN-01-01` | Comprende que los sentidos le permiten percibir algunas características de los objetos que nos rodean (temperatura, sabor, sonidos, olor, color, texturas y formas). | 4 | N4 ×4 |
| `CN-02-04` | Explica los procesos de cambios físicos que ocurren en el ciclo de vida de plantas y animales de su entorno, en un período de tiempo determinado. | 2 | N1 ×2 |
| `CS-01-01` | Se ubica en el espacio que habita teniendo como referencia su propio cuerpo y los puntos cardinales. | 4 | N1, N6 ×3 |
| `CS-01-05` | Reconoce su individualidad y su pertenencia a los diferentes grupos sociales. | 4 | N1, N4, N5, N6 |
| `CS-02-02` | Reconoce los puntos cardinales y los usa para orientarse en el desplazamiento de un lugar a otro. | 4 | N1, N2, N4, N6 |
| `CS-02-03` | Comprende la importancia de las fuentes históricas para la construcción de la memoria individual, familiar y colectiva. | 4 | N4, N6 ×3 |
| `CS-03-04` | Comprende el legado de los grupos humanos en la gastronomía, la música y el paisaje de la región, municipio, resguardo o lugar donde vive. | 4 | N6 ×4 |
| `CS-03-05` | Comprende la importancia del tiempo en la organización de las actividades sociales, económicas y culturales en su comunidad. | 4 | N1 ×2, N6 ×2 |

Por área: Matemáticas 4, Lenguaje 13, Ciencias Naturales 2, Ciencias Sociales 6.

## 6. Dudosas

**67 evidencias** quedaron dictaminadas pero marcadas `dudoso`, con su razón. Van todas
a la validación (criterios §5). Por motivo:

- «justifica»: entre «explica» (aplica) y «argumenta» (N3): **9**
- la evidencia habla de un proceso o un método que la pregunta no observa; solo ve el resultado: **8**
- cerca de N3: «propone» un valor, «evalúa», «análisis crítico», razones sobre un valor: **7**
- lo que se evalúa es del propio estudiante (sus hipótesis, sus ideas): la pregunta tendría que darlo: **6**
- N7 con matiz: algunas características de la gráfica se podrían decir con palabras: **6**
- ortografía, puntuación y concordancia: elegir la forma correcta es reconocer, no escribir: **5**
- «comunica», «da orientaciones», «utiliza señales»: producir o elegir: **4**
- evidencia compuesta: una parte aplicaría y otra no: **4**
- buscar o consultar fuentes: una acción (N4) o un hábito (N5): **4**
- otros (cada uno con su razón en el JSON): **4**
- «toma decisiones» o «decide» (señal de N3) con una respuesta correcta: **3**
- «plantea modelos» o «modela»: cercano a «representa»: **3**
- escucha: hay que oír algo, y la pregunta es escrita: **3**
- contexto propio: la respuesta depende de la vida del estudiante (su familia, su municipio): **1**

### 6.1 Contexto propio (Ciencias Sociales, sobre todo 1° a 3°)

Varias evidencias piden algo que solo sabe el estudiante: los cumpleaños de sus padres, de dónde
vino su familia, el croquis de su municipio, el manual de convivencia de su colegio. Una pregunta
generada para cualquier estudiante no conoce esa respuesta. En la versión 1 se dictaminaron **N4**
y dudosas; la versión 2 de los criterios les da su regla, **N6**, y dejaron de ser dudosas. Cuando
lo que se pide es general (las formas del relieve, los oficios) y «su comunidad» es solo el lugar
donde se aprende, la evidencia aplica.

## 7. Propuestas de ajuste a los criterios

El encargo 05 no cambió los criterios (B.2): propuso estos ajustes. **Las propuestas 1 y 2 se
decidieron el 2026-11-16** (ADR-044) y son las reglas N6 y N7 de la versión 2. Las otras cinco
siguen abiertas: se deciden con la validación.

1. **Decidida: N6.** **Contexto propio.** Agregar una regla (por ejemplo **N6, contexto propio**: la respuesta
   depende de la vida o el lugar del estudiante) o decir que, si el docente escribe ese contexto
   al crear la experiencia (el municipio, el manual), aplica. Hoy se dictaminan N4 y dudosas.
2. **Decidida: N7, sin imagen ni audio en esta versión.** **Escuchar.** Decidir si el sistema tendrá preguntas con audio. Si no, las evidencias de
   escucha son N2 (así quedaron). Si sí, varias pasarían a `single_choice`. Lo mismo, en menor
   medida, con las evidencias que necesitan una imagen en la pregunta (caricaturas, mapas,
   afiches): se dictaminaron como aplican, pero el banco solo puede generarlas si la pregunta
   puede llevar una imagen.
3. **«Justifica».** Nombrarlo en los criterios: como «explica» (aplica) cuando lo que se justifica
   es un hecho o un procedimiento matemático, o como «argumenta» (N3). Hoy aplica y queda dudoso.
4. **«Propone».** Los criterios lo ponen como señal de N3. En la práctica tiene tres usos: proponer
   un método propio (estrategias, procedimientos, patrones: se dictaminó **N1**), proponer una
   acción o una solución a un problema social (**N3**), y proponer un valor que se comprueba
   («propone números que satisfacen una igualdad»: aplica, dudoso). Conviene escribir los tres.
5. **Ortografía y puntuación.** Decidir si «escribe con la ortografía correcta» se puede observar
   eligiendo la palabra bien escrita (práctica común en pruebas como Saber) o si eso es solo
   reconocer (N1, como quedó).
6. **Orden de las reglas frente al ejemplo de N5.** Por el orden de revisión, «asume una postura
   crítica y respetuosa» sería N3; los criterios la ponen como ejemplo de N5. Se siguió el
   ejemplo. Conviene aclarar cuál manda.
7. **Evidencias compuestas con «argumenta» en segundo lugar** («Conjetura y argumenta», «Compara
   y argumenta»). Se aplicó §4: decide la acción principal y se aplica; «argumenta» queda sin
   cubrir y se dice en la justificación. Si el equipo prefiere que «argumenta» decida siempre,
   cambian unas 10.

## 8. Frente a la prueba de los criterios (§7)

Las 20 evidencias que los criterios clasificaron a mano (con la versión 1) se volvieron a leer y
dictaminar, sin copiar la tabla. Con la versión 1 coincidieron las 20.

Coinciden 19 de 20. Las que difieren:

- `CN-07-01` #3: la tabla dice SC, el censo N7. «Representa gráficamente las energías cinética y potencial gravitacional en función del tiempo»: elegir la gráfica correcta exige mostrar gráficas, y la pregunta es solo de texto (N7). En la prueba de los criterios (§7, versión 1) aplicaba. Antes: SC (criterios v2).

## 9. Cómo se hizo y cómo se comprueba

- **El juicio** está en `dictamenes/MAT.txt`, `LEN.txt`, `CN.txt` y `CS.txt`: una línea por
  evidencia, con el dictamen, la señal (el verbo o la frase que decide) y la justificación, que
  cita esa señal y la regla. Se escribió área por área, grado por grado, leyendo cada evidencia
  con el enunciado de su DBA. No se usó ninguna API de IA externa. Las decisiones de aplicación
  que se repiten (escuchar, contexto propio, experimentos como contexto) están anotadas al
  comienzo de cada archivo.
- **El script** `generar_censo.py` no juzga: cruza las líneas con el catálogo y escribe el JSON,
  este informe y la muestra.
- **El verificador** `_verificar_censo.py` comprueba que hay exactamente un dictamen por cada
  evidencia del catálogo, que `formato` es nulo si y solo si no aplica (RI-19), que toda
  justificación cita su regla, y que la muestra se puede volver a sacar igual con su semilla. Al
  final introduce errores a propósito y comprueba que los atrapa.
- **Lo que no garantiza nada de esto:** que el juicio sea correcto. Eso solo lo dice la
  validación del equipo (criterios §5).
