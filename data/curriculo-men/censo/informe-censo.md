# Informe del censo de formato cerrado (QA-014)

**Encargo 05**, Parte B. **Archivo generado** por `generar_censo.py`: no se edita a mano.
**Estado: propuesto por IA, sin validar** (`propuesto-por-ia`, ADR-042). Fecha: 2026-11-10.
Criterios aplicados: `docs/diseno/criterios-censo-formato-cerrado.md`, aceptados el 2026-11-10
(huella sha256 `05f290ff18fb9ca8…`, en la cabecera del JSON).

## 1. En una frase

De las **1282 evidencias** del catálogo, **904 (71 %) se pueden diagnosticar
con una pregunta cerrada** y 378 no. Por área: Matemáticas 336 de 437 (77 %); Lenguaje 186 de 333 (56 %); Ciencias Naturales 152 de 184 (83 %); Ciencias Sociales 230 de 328 (70 %).

Es un juicio de IA, no del equipo: lo hizo la sesión de Claude del encargo 05, leyendo cada
evidencia y escribiendo su razón (`dictamenes/`). Antes de usarlo como dato del proyecto, dos
integrantes validan la muestra de `muestra_validacion.md` (criterios §5).

## 2. La respuesta a QA-014: ¿alcanza el formato cerrado?

| Área | Evidencias | Aplican | % | No aplican |
|---|---|---|---|---|
| Matemáticas | 437 | 336 | **77 %** | 101 |
| Lenguaje | 333 | 186 | **56 %** | 147 |
| Ciencias Naturales | 184 | 152 | **83 %** | 32 |
| Ciencias Sociales | 328 | 230 | **70 %** | 98 |
| **Total** | 1282 | 904 | **71 %** | 378 |

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
| Matemáticas | 30/39 | 28/35 | 31/41 | 25/39 | 39/51 | 31/42 | 25/31 | 36/44 | 27/38 | 35/41 | 29/36 |
| Lenguaje | 16/33 | 19/34 | 21/34 | 12/32 | 16/26 | 22/31 | 16/28 | 18/28 | 15/29 | 14/28 | 17/30 |
| Ciencias Naturales | 8/16 | 10/12 | 15/20 | 18/23 | 11/14 | 14/16 | 12/13 | 19/19 | 19/21 | 11/12 | 15/18 |
| Ciencias Sociales | 10/32 | 15/32 | 17/32 | 27/32 | 25/32 | 27/32 | 25/32 | 27/32 | 27/32 | 15/20 | 15/20 |

En los primeros grados de Ciencias Sociales muchas evidencias piden saber algo de la vida del
propio estudiante (su familia, su casa, su municipio): ver la sección 6.

## 3. Con qué formato

| Área | single_choice | matching | ordering |
|---|---|---|---|
| Matemáticas | 316 | 16 | 4 |
| Lenguaje | 169 | 14 | 3 |
| Ciencias Naturales | 131 | 21 | 0 |
| Ciencias Sociales | 213 | 16 | 1 |
| **Total** | 829 | 67 | 8 |

`matching` y `ordering` son minoría, como esperaban los criterios (§7): se usan solo cuando la
evidencia nombra explícitamente dos conjuntos que emparejar (clasifica, diferencia… de…,
relaciona X con Y) o un orden (ordena, el orden de los eventos). Ante la duda, `single_choice`.

## 4. Por qué no aplican: cada regla

| Regla | Qué pide la evidencia | Matemáticas | Lenguaje | Ciencias Naturales | Ciencias Sociales | Total |
|---|---|---|---|---|---|---|
| **N1** | producir | 74 | 57 | 6 | 15 | 152 |
| **N2** | comunicar en vivo | 0 | 76 | 0 | 5 | 81 |
| **N3** | sostener una postura propia | 13 | 9 | 5 | 39 | 66 |
| **N4** | actuar en el mundo | 14 | 3 | 21 | 34 | 72 |
| **N5** | una actitud o disposición | 0 | 2 | 0 | 5 | 7 |

- **N1 (producir)** es la regla más usada en Matemáticas y Lenguaje: construir tablas y
  gráficas, proponer estrategias, escribir textos.
- **N2 (comunicar en vivo)** es casi toda de Lenguaje: hablar, leer en voz alta, conversar y
  **escuchar**. Las evidencias sobre lo que el estudiante escucha (un discurso, una voz) se
  dictaminaron N2 porque la pregunta del sistema es escrita: leer un texto cambia lo que la
  evidencia pide (ver la propuesta 7.2).
- **N3 (postura propia)** es sobre todo de Ciencias Sociales: «argumenta» (que los criterios
  fijan como no aplica), «propone acciones», «expresa sus opiniones».
- **N4 (actuar en el mundo)** incluye medir, experimentar y observar, y en Ciencias Sociales las
  evidencias de contexto propio (sección 6).

## 5. DBA sin ninguna evidencia que aplique

**16 DBA** quedan sin ninguna evidencia que admita pregunta cerrada. Según QA-012, **no
se pueden usar para crear una experiencia en esta versión**: el banco no tendría de dónde
generar preguntas. (Qué muestra la pantalla en ese caso es el vacío V-12.)

| DBA | Enunciado | Evidencias | Reglas |
|---|---|---|---|
| `MAT-06-02` | Utiliza las propiedades de los números enteros y racionales y las propiedades de sus operaciones para proponer estrategias y procedimientos de cálculo en la solución de problemas. | 2 | N1, N3 |
| `LEN-01-07` | Enuncia textos orales de diferente índole sobre temas de su interés o sugeridos por otros. | 4 | N2 ×4 |
| `LEN-02-07` | Expresa sus ideas atendiendo a las características del contexto comunicativo en que las enuncia (interlocutores, temas, lugares). | 5 | N2 ×5 |
| `LEN-04-07` | Participa en espacios de discusión en los que adapta sus emisiones a los requerimientos de la situación comunicativa. | 4 | N2 ×4 |
| `LEN-07-05` | Comprende discursos orales producidos con un objetivo determinado en diversos contextos sociales y escolares. | 4 | N2 ×4 |
| `LEN-07-07` | Construye narraciones orales, para lo cual retoma las características de los géneros que quiere relatar y los contextos de circulación de su discurso. | 4 | N1, N2 ×3 |
| `LEN-08-07` | Reconstruye en sus intervenciones el sentido de los textos desde la relación existente entre la temática, los interlocutores y el contexto histórico-cultural. | 3 | N1, N2 ×2 |
| `LEN-09-08` | Produce textos verbales y no verbales, a partir de los planes textuales que elabora, y siguiendo procedimientos sistemáticos de corrección lingüística. | 3 | N1 ×3 |
| `LEN-10-02` | Planea la producción de textos audiovisuales en los que articula elementos verbales y no verbales de la comunicación para desarrollar un tema o una historia. | 3 | N1 ×3 |
| `LEN-10-07` | Produce textos orales como ponencias, comentarios, relatorías o entrevistas, atendiendo a la progresión temática, a los interlocutores, al propósito y a la situación comunicativa. | 4 | N1, N2 ×3 |
| `LEN-11-07` | Expresa por medio de producciones orales el dominio de un tema, un texto o la obra de un autor. | 5 | N1 ×2, N2 ×3 |
| `CN-01-01` | Comprende que los sentidos le permiten percibir algunas características de los objetos que nos rodean (temperatura, sabor, sonidos, olor, color, texturas y formas). | 4 | N4 ×4 |
| `CN-02-04` | Explica los procesos de cambios físicos que ocurren en el ciclo de vida de plantas y animales de su entorno, en un período de tiempo determinado. | 2 | N1 ×2 |
| `CS-01-05` | Reconoce su individualidad y su pertenencia a los diferentes grupos sociales. | 4 | N1, N4 ×2, N5 |
| `CS-02-03` | Comprende la importancia de las fuentes históricas para la construcción de la memoria individual, familiar y colectiva. | 4 | N4 ×4 |
| `CS-03-05` | Comprende la importancia del tiempo en la organización de las actividades sociales, económicas y culturales en su comunidad. | 4 | N1 ×2, N4 ×2 |

Por área: Matemáticas 1, Lenguaje 10, Ciencias Naturales 2, Ciencias Sociales 3.

## 6. Dudosas

**90 evidencias** quedaron dictaminadas pero marcadas `dudoso`, con su razón. Van todas
a la validación (criterios §5). Por motivo:

- contexto propio: la respuesta depende de la vida del estudiante (su familia, su municipio): **28**
- «justifica»: entre «explica» (aplica) y «argumenta» (N3): **9**
- la evidencia habla de un proceso o un método que la pregunta no observa; solo ve el resultado: **8**
- cerca de N3: «propone» un valor, «evalúa», «análisis crítico», razones sobre un valor: **7**
- lo que se evalúa es del propio estudiante (sus hipótesis, sus ideas): la pregunta tendría que darlo: **6**
- «comunica», «da orientaciones», «utiliza señales»: producir o elegir: **5**
- ortografía, puntuación y concordancia: elegir la forma correcta es reconocer, no escribir: **5**
- evidencia compuesta: una parte aplicaría y otra no: **4**
- escucha: hay que oír algo, y la pregunta es escrita: **4**
- buscar o consultar fuentes: una acción (N4) o un hábito (N5): **4**
- otros (cada uno con su razón en el JSON): **4**
- «toma decisiones» o «decide» (señal de N3) con una respuesta correcta: **3**
- «plantea modelos» o «modela»: cercano a «representa»: **3**

### 6.1 Contexto propio (Ciencias Sociales, sobre todo 1° a 3°)

Varias evidencias piden algo que solo sabe el estudiante: los cumpleaños de sus padres, de dónde
vino su familia, el croquis de su municipio, el manual de convivencia de su colegio. Una pregunta
generada para cualquier estudiante no conoce esa respuesta. Los criterios no tienen una regla
para esto: se dictaminaron **N4** (requieren observar o consultar su entorno) y se marcaron
dudosas. Ver la propuesta 7.1.

## 7. Propuestas de ajuste a los criterios

No se cambiaron los criterios (encargo 05, B.2). Estos patrones no quedan bien cubiertos y se
proponen para que el equipo decida:

1. **Contexto propio.** Agregar una regla (por ejemplo **N6, contexto propio**: la respuesta
   depende de la vida o el lugar del estudiante) o decir que, si el docente escribe ese contexto
   al crear la experiencia (el municipio, el manual), aplica. Hoy se dictaminan N4 y dudosas.
2. **Escuchar.** Decidir si el sistema tendrá preguntas con audio. Si no, las evidencias de
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

Las 20 evidencias que los criterios clasificaron a mano se volvieron a leer y dictaminar, sin
copiar la tabla.

**Coinciden las 20.** El censo da el mismo dictamen que la tabla en todas, incluido
`LEN-06-02` #1 como N1 dudoso.

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
