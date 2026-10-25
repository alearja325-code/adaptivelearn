# 10. Descripción del proceso de desarrollo

**Metodología:** MODESEC — Fase III, Diseño Computacional, primera
sub-etapa.
**Fecha:** 2026-10-21.
**Numeración:** los documentos de la Fase III se rehacen en el orden de
MODESEC empezando en `10`. Los numerados `00` a `06` son un **borrador
anterior al cierre de la Fase II** (ver su aviso) y se usan como
insumo, no como base.

MODESEC pide aquí *"las etapas que harán parte del diseño del software,
tales como la selección de una metodología o ciclo de vida, la cual se
incluirá en el material computacional, así como las descripciones
funcionales del sistema. El ciclo de vida permite organizar los
procesos de tal forma que las actividades puedan ser definidas de una
manera más ordenada y con calidad."* Este documento tiene, por eso, dos
partes: el ciclo de vida (1) y la descripción funcional del sistema (2).

**Fuentes de verdad:** Fase I (`fase-1-diseño-educativo/`), Fase II
(`fase-2-diseno-multimedial/`, 27 ventanas) y `diseno/decisiones.md`
(ADR-001 a ADR-029).

---

## 1. Ciclo de vida

> **Estado: confirmado por Alejandro el 2026-10-21.** Es la decisión
> que organiza toda la construcción; se propuso como opción y la tomó
> el equipo, no la IA.

### 1.1 Propuesta: desarrollo incremental, con Kanban para el día a día

El sistema se construye en **4 incrementos**. Cada uno pasa por
requerimientos → diseño → código → prueba, y termina en algo que se
puede mostrar funcionando:

| Incremento | Qué entrega | Subsistemas (sección 2) | Por qué en este orden |
|---|---|---|---|
| **I1 — Acceso** | Registrarse, verificar correo, completar perfil, elegir rol, iniciar sesión, recuperar contraseña, mi perfil | SUB-01 | Todo lo demás necesita saber quién es el usuario. **Ya empezó**: el curso pidió backend este semestre (`DSE-2/backend-auth/`, NestJS + MySQL) |
| **I2 — Experiencia y banco** | Catálogo curricular, crear experiencia (con la generación por IA), banco de preguntas, publicar | SUB-02, SUB-03, SUB-06 | Sin banco no hay diagnóstico. Es además **el incremento de más riesgo** —depende de un servicio de IA externo y de una generación que puede tardar minutos (ADR-027)—, y conviene enfrentarlo pronto |
| **I3 — Diagnóstico** | Unirse con código, toma del diagnóstico con la regla adaptativa por certeza, salir de una experiencia | SUB-04 | Necesita experiencias publicadas (I2) |
| **I4 — Reporte y seguimiento** | Reporte, pestaña Estudiantes, historial del estudiante | SUB-05 | Necesita respuestas reales (I3) |

**Kanban con límite de un trabajo en curso** (ya declarado en
`diseno/vision.md`) para el día a día dentro de cada incremento: no se
abre una tarea nueva sin cerrar la anterior.

### 1.2 Por qué incremental, y no los otros

| Ciclo de vida | Por qué no, para este proyecto |
|---|---|
| **Cascada** (todo el diseño, luego todo el código) | El curso ya exigió código (I1) antes de terminar el diseño de la Fase III. Cascada describiría un proceso que no es el que está ocurriendo. |
| **Espiral** | Su fuerza es el análisis de riesgo formal en cada vuelta; para un equipo de estudiantes en un semestre es más ceremonia de la que se puede sostener. Del espiral se toma una sola idea: atacar pronto el riesgo mayor (por eso I2 va segundo). |
| **Scrum** | Supone roles (dueño de producto, facilitador), sprints de duración fija y reuniones diarias que el equipo no tiene cómo sostener. Kanban da la disciplina de flujo sin esos roles. |
| **Prototipos desechables** | El diseño de pantallas ya cumplió ese papel en la Fase II (27 ventanas especificadas; la mayoría ya construidas en Figma, y las de octubre pendientes de construir). Repetirlo en código sería trabajo duplicado. |

### 1.3 Relación con MODESEC

MODESEC es la metodología de **diseño** (Fases I a III) y de producción
(Fase IV). El ciclo incremental organiza la **construcción** dentro de
la Fase IV: cada incremento toma de la Fase III solo los requerimientos,
casos de uso, clases y secuencias que le corresponden. Por eso todos los
entregables de esta fase marcan a qué subsistema pertenece cada
elemento.

---

## 2. Descripción funcional del sistema

### 2.1 Qué es, en una frase

Una aplicación web, para computador, en la que un **docente** crea una
experiencia anclada a un Derecho Básico de Aprendizaje del MEN, el
sistema genera con IA un banco de preguntas por cada evidencia del DBA,
el docente lo revisa y lo publica, sus **estudiantes** responden un
diagnóstico adaptativo declarando su certeza en cada respuesta, y el
docente recibe un reporte de qué evidencias muestra y cuáles no su
grupo — sin que el sistema afirme nunca una certeza.

### 2.2 Actores

| Actor | Quién es | Qué hace con el sistema |
|---|---|---|
| **Docente** | Docente de secundaria | Crea experiencias, revisa y completa el banco, publica, comparte el código, consulta el reporte y el historial de cada estudiante |
| **Estudiante** | Estudiante de 6° a 11° (11 a 17 años) | Se une con un código y responde el diagnóstico |
| **Servicio de IA** *(externo)* | Gemini y DeepSeek: uno principal y otro de respaldo (ADR-030) | Recibe un DBA y sus evidencias y devuelve el banco. Si el principal falla, el sistema reintenta con el respaldo en la misma espera |
| **Proveedor de identidad** *(externo)* | Google o Microsoft | Autentica a quien entra con esos botones |
| **Servicio de correo** *(externo)* | Envío de correos | Entrega los códigos de verificación y de recuperación de contraseña |

### 2.3 Subsistemas

Seis subsistemas. El análisis de requerimientos (`11`) usa estos
códigos.

**SUB-01 — Acceso y perfil.** Registro con correo y contraseña o con
Google/Microsoft; verificación del correo con un código de 6 dígitos;
completar perfil (nombres, apellidos, foto opcional); elegir rol,
**una sola vez y para siempre**; iniciar y cerrar sesión; recuperar
contraseña; editar el propio perfil. Un correo ya registrado con un
método no se vincula a otro: se avisa cuál usar. *Ventanas 014 a 019 y
026.*

**SUB-02 — Gestión de experiencias (docente).** Crear una experiencia en
3 pasos: área, DBA (filtrable por grado) y nombre. Al confirmar, la
creación es **todo o nada** con la generación del banco (ADR-027).
Consultar la experiencia (Resumen, Materiales, Estudiantes). Publicarla
—exige al menos 6 preguntas activas por evidencia, y congela el banco
(ADR-026)—. Mostrar el código de invitación. Eliminarla. Dos estados:
Borrador y Publicada; no hay "despublicar". *Ventanas 001 (docente),
002 a 004, 006 a 008, 011 a 013, 025.*

**SUB-03 — Banco de preguntas.** Generación por IA de 12 ítems por cada
evidencia incluida, usando el ejemplo del DBA como contexto (ADR-011),
con un servicio principal y otro de respaldo; cada ítem guarda qué
servicio y modelo lo generó (ADR-030).
Tres formatos: selección única, emparejamiento, ordenamiento (ADR-006).
El docente puede editar, descartar, reincluir y **agregar preguntas
propias**, solo mientras la experiencia está en Borrador (ADR-026).
*Ventana 009.*

**SUB-04 — Diagnóstico (estudiante).** Unirse con el código (solo a
experiencias publicadas). Responder evidencia por evidencia, en el orden
oficial del DBA: cada pregunta en dos pasos —respuesta y certeza de 0 a
5—, con la regla adaptativa: mínimo 4 preguntas por evidencia, tope 6,
y se detiene antes si la mayoría de señales fuertes coinciden (ADR-016).
Un solo sentido, sin contador, y **el estudiante no ve sus resultados**
(ADR-028). Retomar donde quedó. Salir de la experiencia. *Ventanas 001
(estudiante), 005, 020 a 023, 025.*

**SUB-05 — Reporte y seguimiento (docente).** Por evidencia y por
estudiante, el resultado (Muestra / No muestra / No concluyente),
guardado como fotografía del momento en que se concluyó (ADR-021). Por
estudiante, el estado general del DBA, con 4 estados y precedencia
(ADR-022). Reporte del grupo con clasificación por umbral fijada por el
sistema (ADR-013, 017, 023). Lista de estudiantes agrupada por estado, e
historial pregunta por pregunta. *Ventanas 010, 011, 027.*

**SUB-06 — Catálogo curricular.** Los DBA del MEN de las 4 áreas
(Matemáticas, Lenguaje, Ciencias Naturales, Ciencias Sociales), con sus
evidencias y ejemplos, más nuestro dictamen de si cada evidencia admite
formato cerrado. Es de **solo lectura** para los usuarios: no tiene
pantalla propia, se consulta al crear una experiencia. *Datos con
problemas conocidos: QA-013 (errores de extracción) y QA-014 (censo de
formato cerrado), pendientes.*

### 2.4 Lo que el sistema no hace en esta versión

| Fuera de alcance | Decisión |
|---|---|
| Práctica y verificación después del diagnóstico | ADR-007 |
| Unidades (varias experiencias encadenadas) | Glosario, "Unidad" |
| Usarse con estudiantes reales: no registra la autorización del acudiente | ADR-029 |
| Celular | ADR-025 |
| Regenerar preguntas con IA, o pedir que genere más | ADR-026 |
| Despublicar o editar el banco después de publicar | ADR-026 |
| Que el docente elija qué evidencias entran, o agregue evidencias propias | QA-010, QA-001 |
| Mostrarle al estudiante sus resultados | ADR-028 |

### 2.5 Restricciones que condicionan el diseño computacional

- **Solo computador**, lienzo de diseño de 1440 × 900 (ADR-025).
- **Demostración con docentes**, no despliegue con estudiantes reales
  (ADR-025, ADR-029).
- **Datos mínimos del estudiante**: nombres, apellidos, correo, foto
  opcional y lo que responde; nada más (ADR-029).
- **Nunca lenguaje de certeza** en lo que el sistema muestra (ADR-008).
- **Backend del curso**: NestJS con MySQL, ya iniciado para el acceso
  (`DSE-2/backend-auth/`). El resto de la pila no está fijado en el
  diseño.
