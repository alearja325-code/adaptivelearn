# 1. Planeación del Proceso de Producción

**Metodología:** MODESEC — Fase II, primera sub-etapa.
**Actualizada:** 2026-10-21, al cerrar la fase. La versión del
2026-08-11 planeaba la fase antes de empezarla; esta registra además lo
que efectivamente se hizo y cuándo.

**Precisión de alcance, verificada contra el texto original:** la propia
introducción de Fase II dice que se encarga *"de la descripción de las
etapas que permitirán conocer la planeación de actividades a
desarrollar, utilizando representaciones gráficas y recursos multimedia
que en conjunto mostrarán el diseño de cada interfaz y la estructura que
se va a utilizar en el software"* — es decir, esta planeación es sobre
las actividades **de esta fase** (diagramas, ventanas, guión técnico,
recursos), no del proyecto completo. MODESEC reserva la planeación de
codificación e implementación para su propia Fase IV: Producción — mezclar
ambas invadiría una separación que el modelo mantiene limpia a propósito.

## Metas y objetivos de esta fase

Diseñar todas las pantallas de esta versión del sistema, coherentes con
las decisiones registradas en `/diseno`, y dejarlas listas para el
Diseño Computacional (Fase III):

1. **Ventana estándar**: sistema de diseño (colores, letra, medidas)
   verificado, `03-tokens-diseno.md`.
2. **Flujo del docente**: Dashboard, crear experiencia (3 pasos), Vista
   Interna (3 pestañas), banco de preguntas, Reporte, publicar, código
   de invitación, historial de un estudiante.
3. **Flujo del estudiante**: unirse con código y la toma del
   diagnóstico (inicio, pregunta, certeza, cierre). Se incluyó desde la
   planeación original porque, sin ella, el sistema no genera ningún
   dato: el estudiante es quien responde y aporta la certeza que el
   diagnóstico necesita (ADR-008).
4. **Acceso**: iniciar sesión, crear cuenta, verificar correo, completar
   perfil, elegir rol, recuperar contraseña. *No estaba en la planeación
   original*: se agregó en septiembre porque el curso exige backend este
   semestre y el acceso es lo primero que construye (V-8).
5. **Componentes comunes**: espera (cargando), eliminar o salir, mi
   perfil.
6. **Cierre de MODESEC**: mapa de navegación, guión técnico e índice de
   recursos.

**Resultado:** 27 ventanas en 24 especificaciones (`04` a `27`), más los
documentos `28`, `29` y `30`.

## Distribución de funciones

Limitada a las actividades propias de esta fase. Corresponde a las áreas
de `EQUIPO.md` (raíz del repositorio), donde el equipo registra quién
asume cada una:

| Función de Fase II | Qué cubre | Área de `EQUIPO.md` |
|---|---|---|
| Diseño pedagógico y curricular | Que cada pantalla refleje las decisiones de Fase I | Área 1 — Fundamentación educativa |
| Diseño de interfaz | Ventana estándar, cada ventana, mapa de navegación | Área 3 — Diseño de interfaz |
| Producción multimedial | Guión técnico, índice de recursos | Área 3 — Diseño de interfaz |
| Aseguramiento de calidad | Coherencia entre pantallas, `/diseno` y el texto de MODESEC; verificadores automáticos | Área 5 — Aseguramiento de calidad |

**Responsables:** los nombres los asigna el equipo en `EQUIPO.md` (hoy
"por asignar"). *Nota honesta:* en la práctica, estas funciones las
cubrió un integrante con asistencia de IA bajo su dirección; el registro
de uso de IA está en las bitácoras de los entregables del curso.

## Cronograma de actividades

La planeación original fijaba el **orden** y no fechas. Este es el
cronograma ejecutado, con las fechas que registra `/diseno/pendientes.md`:

| # | Actividad | Fechas | Documentos |
|---|---|---|---|
| 1 | Planeación de la fase | 11 de agosto | `01` |
| 2 | Ventana estándar, Dashboard y crear experiencia | 11 al 17 de agosto | `03` a `08` |
| 3 | Vista Interna, banco de preguntas y Reporte | 21 al 30 de agosto | `09` a `13` |
| 4 | Auditoría de consistencia (4 pasadas) y diagrama de contenidos | 26 y 27 de agosto | `02`, verificadores |
| 5 | Pestaña Estudiantes, publicar, código de invitación | 29 al 31 de agosto | `14` a `16` |
| 6 | Acceso (6 pantallas) | 4 al 11 de septiembre | `17` a `22` |
| 7 | Ajustes del Dashboard del estudiante | 12 de septiembre | `04` |
| 8 | Toma del diagnóstico, cargando, eliminar o salir | 26 y 27 de septiembre | `23` a `25` |
| 9 | Cierre: decisiones finales del banco, mi perfil, historial, mapa de navegación, guión técnico, índice de recursos, revisión de coherencia con Fase I | 21 de octubre | `26` a `30` |

**Desvíos frente al orden planeado, y por qué:**
- El orden original era: docente → estudiante → mapa, guión e índice.
  El acceso (paso 6) se adelantó antes que la toma del diagnóstico
  porque el curso pidió backend, y el acceso es lo primero que se
  construye.
- La toma del diagnóstico, marcada como "prioritaria" en la planeación
  original, se pausó del 4 al 26 de septiembre por esa misma razón.
