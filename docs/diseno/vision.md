# Visión — AdaptiveLearn (rediseño)

**Estado:** confirmada — 2026-08-06

## Historia de versiones

- **V1** — antigua, no se encuentra en el proyecto actual.
- **V2** (`AdaptiveLearn/mvp/`) — versión anterior con backend y
  frontend construidos, llegó a ser una plataforma funcional (FastAPI +
  PostgreSQL, motor de diagnóstico adaptativo, generación curricular
  con IA). **Histórica — no se continúa.** El motor de diagnóstico se
  reconstruye desde cero, no se adapta (ADR-012, con evidencia real:
  acoplado a SOLO y a un modelo curricular ya retirado, con código
  simulado adentro). La infraestructura no específica de diagnóstico
  —autenticación, modelos de Curso/Experiencia/Inscripción, pipeline de
  datos curriculares— se revisa caso por caso como referencia, no se
  copia literal (ADR-012).
- **V3** (actual, este documento y todo lo de `DSE-2/`) — el rediseño
  basado en la metodología MODESEC. **Fase I y Fase II cerradas el
  2026-10-21** (8 documentos de Fase I; 24 especificaciones de ventana,
  mapa de navegación, guión técnico e índice de recursos en Fase II).
  Fase III (Diseño Computacional) parte de ahí, con una excepción
  reconocida: DSE-2
  exige backend *este semestre*, así que el Auth de V3 arranca antes
  de que Fase III empiece formalmente, apoyado en lo que Fase II ya
  dejó definido (specs de Auth, MER) — no en el código de V2. No es un
  cambio de plan, es una secuencia forzada por el calendario del curso.

**Nota de estructura (2026-09-17):** V2 y V3 vivían bajo la misma
carpeta raíz (`AdaptiveLearn/`), sin separación física — causa real de
confusión, más que un problema de control de versiones (`mvp/.git` ni
siquiera estaba activo). **Separados hoy:** V3 (esta carpeta `diseno/`
y `DSE-2/`) se movió a `AdaptiveLearn-V3/`, como proyecto propio; V2
(`mvp/`, con su `docker-compose.yml`, `.github/` y `launch.sh`) se
queda donde estaba, en `AdaptiveLearn/`. *(Actualizado 2026-10-21:
`AdaptiveLearn-V3/` ya es un repositorio git, con remoto en GitHub; el
`.git` heredado de `diseno/` se apartó como historial, y los secretos
del backend quedan excluidos por `.gitignore`.)*

## El problema

Un docente de secundaria en Colombia no tiene una forma fundamentada de
saber, **a la escala de las evidencias de aprendizaje de un DBA**, qué
alcanzó y qué no cada estudiante de su grupo, durante el año. Los
instrumentos que existen trabajan a otra escala: las pruebas Saber son
externas, anuales, censales y reportan por área y competencia; Evaluar
para Avanzar es formativo y gratuito, pero con instrumentos fijos del
ICFES, que el docente no ancla a un DBA de su elección. El marco del MEN
sí define qué observar —las evidencias de cada DBA— pero no le da al
docente el instrumento para observarlo.

*Corrección 2026-10-21. La versión anterior decía que construir el
material "toma horas que [el docente] no tiene". La entrevista técnica
E0 (curso 203447, 2026-09-25, Decisión 1) encontró que ninguna fuente lo
mide, y reformuló el problema alrededor de la escala de medición, que sí
es documentable (ICFES, LEE Javeriana, MEN). Sigue siendo cierto que E0
fue un análisis documental, no una entrevista a un docente real: la
premisa sigue sin confrontarse con uno.*

## La solución

AdaptiveLearn es una biblioteca de experiencias, cada una anclada a un
Derecho Básico de Aprendizaje oficial del MEN. En esta versión, cada
experiencia recorre un ciclo de dos pasos —diagnóstico, reporte—
construido desde las evidencias oficiales de ese DBA, no desde contenido
inventado libremente (práctica y verificación tienen diseño propio, pero
quedan fuera de esta versión — ver ADR-007). El sistema propone; el
docente puede revisar, corregir y completar el banco con preguntas
propias, y **nada llega a un estudiante hasta que el docente decide
publicar** — el sistema le recuerda revisar antes, sin obligarlo, y al
publicar el banco se congela (ADR-026). *(Corrección 2026-10-21: decía
"siempre antes de que un estudiante vea nada", como si la revisión fuera
obligatoria; el sistema no la exige.)*

## Para quién

Docentes de educación secundaria en Colombia.

## Qué lo diferencia

- Cada evidencia que se evalúa es oficial del DBA, no una invención de la
  IA.
- El diagnóstico no depende de preguntas abiertas ni de una taxonomía que no
  aplica a sus formatos reales — usa distractores plausibles, con el mismo
  cuidado de construcción validado en instrumentos como el Force Concept
  Inventory, para detectar si el estudiante muestra o no una evidencia. No
  identifica ni nombra la causa del error en esta versión (ver ADR-008).
- Nada se declara con certeza: ni un acierto certifica dominio, ni un error
  certifica una brecha definitiva.

## Lo que NO es (todavía)

- Un sistema con práctica y verificación construidas. Su diseño ya existe
  (ADR-004 para práctica), pero queda fuera de esta versión — ver ADR-007.
  Diagnóstico y práctica están acoplados; cambiar uno sin el otro firme
  arriesga trabajo desperdiciado.
- Una biblioteca curada por el uso real. Curar con uso es una aspiración,
  sin mecanismo definido — y no hay todavía nada que curar: ni siquiera una
  experiencia completa, de principio a fin, con su funcionamiento diseñado
  (no solo su descripción), existe hoy. Hablar de "biblioteca que se cura"
  antes de eso es adelantarse.
- Una plataforma con unidades (varias experiencias conectadas).
- Un sistema de verificación espaciada en el tiempo.
- Un sistema validado empíricamente con un docente real, fuera de esta
  conversación.
- Un generador que publique por su cuenta: nada llega a un estudiante
  sin la decisión explícita del docente de publicar.
- Un sistema listo para estudiantes reales: no registra la autorización
  del acudiente que exige la Ley 1581 de 2012 para datos de menores
  (ADR-029). Esta versión es una demostración para docentes (ADR-025).

## Metodología

**MODESEC** (Caro & Toscano-Miranda, Universidad de Córdoba) para el orden de
las fases: diseño educativo → diseño multimedial → diseño computacional →
producción → aplicación. Este documento y el glosario **alimentan** la Fase I
(Diseño Educativo), que se entrega en sus 8 sub-etapas propias, en
`DSE-2/Metodologia MODESEC/fase-1-diseño-educativo/`. *(Corrección
2026-08-26: antes decía que este documento y el glosario "cierran" esa fase
— era cierto cuando se escribió, antes de que existieran los 8 documentos
formales; hoy son su fuente, no su entrega.)*

**Kanban con límite de trabajo en curso (uno a la vez)** para la disciplina de
proceso — la causa raíz del desorden anterior no fue falta de documentos, fue
tener demasiados abiertos a la vez sin cerrar ninguno.

**Nota de proceso:** este documento se escribió antes de que empezara el
semestre, sin el plan de curso de DSE-2 a la vista, y se avanzó igual. Lo
que efectivamente se entregó desde entonces: Fase I completa (8
documentos), Fase II completa (24 especificaciones de ventana y los 3
documentos de cierre), y de Fase III el MER, el MR y el diccionario de
datos — ver `diseno/pendientes.md` para el estado real y lo que falta.
