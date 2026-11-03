# 11. Análisis de requerimientos

**Metodología:** MODESEC — Fase III, Diseño Computacional, segunda sub-etapa.
**Fecha:** 2026-10-21 (actualizado 2026-10-26). **Archivo generado** por `requerimientos/requerimientos.py`; no se edita a mano.

MODESEC pide aquí tener presente *"la planta física y la población a quien va dirigida"*, establecer los requerimientos *"a partir de la necesidad que se presentó en el proceso de enseñanza y aprendizaje"*, y *"dividir éstos en secciones denominadas subsistemas y requerimientos funcionales"*, en el formato de su Tabla 5 (número, enunciado, usuario o sistema, funcional o no funcional, precondición, postcondición, fechas, responsable, modificación).

## 1. Base del análisis

- **Necesidad:** un docente de secundaria no tiene una forma fundamentada de saber, a la escala de las evidencias de un DBA, qué alcanzó cada estudiante de su grupo (`fase-1/01-analisis-necesidad-educativa.docx`, reformulada por la entrevista E0).
- **Población:** docentes de secundaria en Colombia y sus estudiantes de 6° a 11° (11 a 17 años, menores de edad).
- **Planta física:** computador con navegador y conexión durante el uso. Cerca de la mitad de las sedes rurales no tenía conexión en 2025 (MinTIC, citado en E0): es una limitación de alcance, declarada (ADR-025).
- **Fuentes de cada requerimiento:** las ventanas de la Fase II y las decisiones de `diseno/decisiones.md`. No hay un requerimiento sin fuente; los pocos que agrega la ingeniería lo dicen.
- **El documento E1 de DSE-1** (requerimientos con ISO/IEC/IEEE 29148) se usó solo como contraste, no como base: es anterior a las decisiones de octubre (ADR-026 a ADR-032).
- **Subsistemas:** los 6 de `10-proceso-desarrollo.md`, más un grupo de transversales para los no funcionales. Cada requerimiento dice en qué incremento se construye (I1 a I4).

## 2. Resumen

**58 requerimientos:** 44 funcionales y 14 no funcionales.

| Subsistema | Funcionales | No funcionales | Incremento |
|---|---|---|---|
| **SUB-01** Acceso y perfil | 11 | 0 | I1 |
| **SUB-02** Gestión de experiencias | 7 | 0 | I2 |
| **SUB-03** Banco de preguntas | 8 | 0 | I2 |
| **SUB-04** Diagnóstico | 12 | 0 | I3 |
| **SUB-05** Reporte y seguimiento | 4 | 0 | I4 |
| **SUB-06** Catálogo curricular | 2 | 0 | I2 |
| **SUB-00** Transversales (no funcionales) | 0 | 14 | I1, I2, I3, Todos |

## 3. Requerimientos, por subsistema

Cada requerimiento va en el formato de la Tabla 5 de MODESEC. Comunes a todos: **fecha de creación** 2026-10-21 (actualizado 2026-10-26); **fecha de procesamiento**: pendiente (se llena al construirlo); **responsable**: Área 2 — Levantamiento de requerimientos (`EQUIPO.md`; nombre por asignar); **modificación**: ninguna.

### SUB-01 — Acceso y perfil

#### RF-01-01 — El sistema debe permitir crear una cuenta con correo y contraseña.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Visitante |
| Detalle | La contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula y un número; el botón se habilita solo cuando se cumple. Sin campo de confirmar contraseña: se puede mostrar u ocultar lo escrito. Sin casilla de términos: el documento no existe. |
| Precondición | El correo no está registrado. |
| Postcondición | Se envía un código de verificación al correo y se pasa a verificarlo. |
| Fuente | Ventana 014, Ventana 015 |
| Incremento | I1 |

#### RF-01-02 — El sistema debe permitir crear una cuenta o iniciar sesión con Google o con Microsoft.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Visitante |
| Detalle | Sin Apple (exige cuenta de desarrollador de pago y la plataforma es web). Quien entra así no verifica correo: lo hizo el proveedor. Nombres, apellidos y foto llegan prellenados y editables. |
| Precondición | El proveedor autentica a la persona. |
| Postcondición | Cuenta nueva: pasa a completar perfil. Cuenta existente: entra al Dashboard. |
| Fuente | Ventana 014, Ventana 016 |
| Incremento | I1 |

#### RF-01-03 — El sistema debe verificar el correo con un código numérico de 6 dígitos enviado a ese correo.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Visitante |
| Detalle | El código se puede reenviar después de una cuenta regresiva de 30 segundos. Código incorrecto: mensaje de error, sin borrar lo escrito. La misma pantalla sirve al registro y a la recuperación de contraseña; su enlace "Volver" regresa al paso anterior de cada flujo. |
| Precondición | Se envió un código al correo. |
| Postcondición | Registro: pasa a completar perfil. Recuperación: pasa a nueva contraseña. |
| Fuente | Ventana 015 |
| Incremento | I1 |

#### RF-01-04 — El sistema no debe crear cuentas duplicadas ni vincular métodos de acceso para un mismo correo.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | Funcional |
| Actor | Visitante |
| Detalle | Si el correo ya está registrado con otro método, se avisa cuál usar; si está registrado con el mismo, se avisa que ya existe. |
| Precondición | Se intenta registrar o entrar con un correo existente. |
| Postcondición | No se crea ni se modifica ninguna cuenta. |
| Fuente | Ventana 014 |
| Incremento | I1 |

#### RF-01-05 — El sistema debe pedir nombres y apellidos, y permitir subir una foto de perfil opcional.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Visitante |
| Detalle | Foto: JPG o PNG, máximo 5 MB, recorte cuadrado automático, sin editor. Archivo inválido: mensaje de error y la foto no cambia. "Continuar" se habilita con nombres y apellidos llenos. |
| Precondición | Correo verificado o acceso con proveedor. |
| Postcondición | Pasa a elegir rol; la cuenta todavía no existe. |
| Fuente | Ventana 016 |
| Incremento | I1 |

#### RF-01-06 — El sistema debe pedir elegir rol —Docente o Estudiante— una sola vez, y crear la cuenta en ese momento.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Visitante |
| Detalle | El rol no se puede cambiar después; la pantalla lo advierte. Docente y Estudiante son tipos de usuario separados. |
| Precondición | Perfil completo. |
| Postcondición | Existe la cuenta con su rol, y la persona entra a su Dashboard. |
| Fuente | Ventana 017 |
| Incremento | I1 |

#### RF-01-07 — El sistema debe permitir iniciar sesión con correo y contraseña.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente, Estudiante |
| Detalle | Credenciales incorrectas: mensaje de error genérico. Si la persona creó su cuenta pero no terminó el registro (no eligió rol), retoma en completar perfil (ADR-035). |
| Precondición | La cuenta existe. |
| Postcondición | La persona entra al Dashboard de su rol, o retoma su registro. |
| Fuente | Ventana 014, ADR-035 |
| Incremento | I1 |

#### RF-01-08 — El sistema debe permitir recuperar la contraseña mediante un código enviado al correo.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente, Estudiante |
| Detalle | Al enviar la solicitud, siempre avanza a verificar el código, exista o no la cuenta: no confirma a un desconocido si un correo está registrado. Solo valida el formato del correo. |
| Precondición | La persona no recuerda su contraseña. |
| Postcondición | Si la cuenta existe, se envía el código. |
| Fuente | Ventana 018, Ventana 015 |
| Incremento | I1 |

#### RF-01-09 — El sistema debe permitir definir una contraseña nueva después de verificar el código.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente, Estudiante |
| Detalle | Mismas reglas que al registrarse. "Guardar" se habilita solo cuando se cumplen. |
| Precondición | Código de recuperación válido. |
| Postcondición | La contraseña cambia y se vuelve a iniciar sesión, con un mensaje de confirmación. |
| Fuente | Ventana 019 |
| Incremento | I1 |

#### RF-01-10 — El sistema debe permitir cerrar la sesión desde el menú lateral.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente, Estudiante |
| Detalle | Sin confirmación: no se pierde nada. |
| Precondición | Sesión iniciada. |
| Postcondición | La sesión termina y se muestra iniciar sesión. |
| Fuente | Ventana 001, Ventana 014 |
| Incremento | I1 |

#### RF-01-11 — El sistema debe permitir editar nombres, apellidos y foto desde el bloque de perfil del menú lateral.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente, Estudiante |
| Detalle | Todo el bloque (foto, nombre, correo) abre la edición. El correo se muestra y no se edita; el rol no se edita; la foto se reemplaza, no se quita. "Guardar cambios" se habilita solo si hay cambios y los dos campos están llenos. |
| Precondición | Sesión iniciada. |
| Postcondición | Los datos quedan guardados y el menú lateral se actualiza. |
| Fuente | Ventana 026, Ventana 001 |
| Incremento | I1 |

### SUB-02 — Gestión de experiencias

#### RF-02-01 — El sistema debe listar las experiencias del docente, con búsqueda y filtro por estado.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente |
| Detalle | Cada una muestra estado (Borrador / Publicada), nombre y "Área · Grado · N estudiantes". Sin experiencias: mensaje de lista vacía. |
| Precondición | Sesión de docente. |
| Postcondición | — |
| Fuente | Ventana 001 |
| Incremento | I2 |

#### RF-02-02 — El sistema debe permitir crear una experiencia en tres pasos: área, DBA y nombre.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente |
| Detalle | Paso 1: una de las 4 áreas. Paso 2: el DBA del área, con búsqueda y filtro por grado (1° a 11°), viendo su enunciado, sus evidencias (marcadas las que no admiten formato cerrado) y su ejemplo. Paso 3: nombre, prellenado con el enunciado del DBA y editable, obligatorio. Se puede volver a un paso anterior sin perder lo elegido. |
| Precondición | Sesión de docente. |
| Postcondición | Se dispara la generación del banco (RF-03-01). |
| Fuente | Ventana 002, Ventana 003, Ventana 004, ADR-024 |
| Incremento | I2 |

#### RF-02-03 — La creación de una experiencia debe ser "todo o nada": la experiencia se guarda solo si su banco se generó completo.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | Funcional |
| Actor | Docente |
| Detalle | Mientras se genera, el docente ve la espera "Generando las preguntas...". Si la generación falla del todo, no se guarda nada y el Paso 3 muestra el error con el nombre y el DBA intactos, para reintentar. |
| Precondición | El docente confirmó el Paso 3. |
| Postcondición | Éxito: experiencia en Borrador, con su banco, y el docente entra a ella. Falla: nada guardado. |
| Fuente | Ventana 004, Ventana 024, ADR-027 |
| Incremento | I2 |

#### RF-02-04 — El sistema debe mostrar la experiencia con tres pestañas: Resumen, Materiales y Estudiantes.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente |
| Detalle | Encabezado con el nombre y fila de datos: Estado, Creada, Estudiantes, Área, Grado. Resumen describe el DBA; Materiales da acceso al banco y al reporte; Estudiantes, al grupo. |
| Precondición | El docente es el dueño de la experiencia. |
| Postcondición | — |
| Fuente | Ventana 006, Ventana 007, Ventana 008, Ventana 011 |
| Incremento | I2 |

#### RF-02-05 — El sistema debe permitir publicar una experiencia, con confirmación.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente |
| Detalle | Solo se puede publicar si cada evidencia incluida tiene al menos 6 ítems activos; si no, el botón está deshabilitado y explica por qué. La confirmación advierte que no se puede deshacer y que el banco quedará congelado. |
| Precondición | Experiencia en Borrador con ≥ 6 ítems activos por evidencia incluida. |
| Postcondición | Experiencia Publicada; banco de solo lectura; el código de invitación se puede mostrar. |
| Fuente | Ventana 011, Ventana 012, ADR-026 |
| Incremento | I2 |

#### RF-02-06 — El sistema debe generar un código de invitación único al crear cada experiencia, y mostrarlo solo cuando esté publicada.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | Funcional |
| Actor | Docente |
| Detalle | 6 caracteres, letras y números, sin caracteres ambiguos (0/O, 1/I/L), sin distinguir mayúsculas. Se muestra en una ventana propia con botón para copiarlo. |
| Precondición | Experiencia Publicada (para mostrarlo). |
| Postcondición | El docente puede compartir el código. |
| Fuente | Ventana 013, Ventana 011 |
| Incremento | I2 |

#### RF-02-07 — El sistema debe permitir eliminar una experiencia, con confirmación que diga qué se pierde.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente |
| Detalle | Se permite siempre, aunque tenga estudiantes o respuestas; la confirmación dice cuántos estudiantes inscritos y cuántas respuestas se eliminan, y que es irreversible. |
| Precondición | El docente es el dueño. |
| Postcondición | La experiencia y todo lo que depende de ella —banco, inscripciones y lo respondido— se borran en cascada (ADR-035). |
| Fuente | Ventana 025, Ventana 006, ADR-035 |
| Incremento | I2 |

### SUB-03 — Banco de preguntas

#### RF-03-01 — El sistema debe generar con IA un banco de 12 ítems por cada evidencia incluida de la experiencia.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | Funcional |
| Actor | Servicio de IA |
| Detalle | Solo entran las evidencias cuyo dictamen admite formato cerrado. El formato de los ítems lo determina la evidencia (selección única por defecto; emparejamiento si relaciona conjuntos; ordenamiento si es secuencial). El ejemplo del DBA se usa como contexto. Los distractores son plausibles y no se rotulan como un error específico. |
| Precondición | Experiencia confirmada en el Paso 3. |
| Postcondición | Cada evidencia incluida tiene 12 ítems, con sus opciones, de origen "ia". |
| Fuente | ADR-005, ADR-006, ADR-008, ADR-011, ADR-014, ADR-016 |
| Incremento | I2 |

#### RF-03-02 — La generación debe usar un servicio de IA principal y, si falla o supera el tiempo límite, uno de respaldo, sin que el docente lo note.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | Funcional |
| Actor | Servicio de IA |
| Detalle | Gemini y DeepSeek; cuál es el principal es un ajuste de configuración. Un banco se genera completo con un solo servicio: si el principal falla a mitad de camino, el respaldo lo genera completo de nuevo. Un ítem generado que no pasa la validación de su formato cuenta como falla del servicio (ADR-035). |
| Precondición | Se pidió generar un banco. |
| Postcondición | Banco completo de un solo servicio, o error si fallan los dos. |
| Fuente | ADR-030, ADR-027, ADR-035 |
| Incremento | I2 |

#### RF-03-03 — Cada ítem debe registrar su origen, y cada experiencia, qué servicio y qué modelo de IA generaron su banco.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | Funcional |
| Actor | — |
| Detalle | Origen del ítem: generado por IA, editado por el docente o creado por el docente. El servicio se guarda una vez en la experiencia, porque un banco sale entero de un solo servicio: un ítem generado o editado es de ese servicio; uno creado por el docente no se atribuye a la IA. El docente no ve el servicio. *(Corregido el 2026-10-26: decía que cada ítem guardaba su servicio; ADR-035 lo cambió.)* |
| Precondición | — |
| Postcondición | — |
| Fuente | ADR-026, ADR-030, ADR-035 |
| Incremento | I2 |

#### RF-03-04 — El sistema debe mostrar el banco agrupado por evidencia, en el orden oficial del DBA, con búsqueda y filtro por formato.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente |
| Detalle | Cada evidencia muestra cuántos ítems activos tiene; si son menos de 6, en rojo y con cuántos faltan para publicar. Cada ítem se expande para ver su enunciado y su respuesta correcta. |
| Precondición | Experiencia del docente. |
| Postcondición | — |
| Fuente | Ventana 009, ADR-024, ADR-026 |
| Incremento | I2 |

#### RF-03-05 — El sistema debe permitir editar un ítem —enunciado, opciones y respuesta correcta— con Guardar y Cancelar.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente |
| Detalle | Se pueden agregar o quitar opciones sin bajar del mínimo del formato (2 en selección única y ordenamiento, 4 en emparejamiento). "Guardar" se habilita solo si el ítem es válido: nada vacío, mínimo de opciones, exactamente una correcta en selección única, números de orden completos y sin repetir en emparejamiento y ordenamiento. |
| Precondición | Experiencia en Borrador. |
| Postcondición | Ítem guardado; su origen pasa a "editado_docente". |
| Fuente | Ventana 009, ADR-026 |
| Incremento | I2 |

#### RF-03-06 — El sistema debe permitir descartar un ítem y volver a incluirlo, sin confirmación.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente |
| Detalle | Descartar no borra el ítem: lo excluye de lo que ven los estudiantes y se puede revertir. |
| Precondición | Experiencia en Borrador. |
| Postcondición | El ítem queda excluido o incluido, y el contador de su evidencia se actualiza. |
| Fuente | Ventana 009, ADR-015 |
| Incremento | I2 |

#### RF-03-07 — El sistema debe permitir agregar una pregunta propia a cualquier evidencia.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente |
| Detalle | Se crea con el formato de esa evidencia y el mínimo de opciones vacías, ya en modo edición; se guarda con las mismas reglas de RF-03-05. Cancelar antes de guardar la descarta. |
| Precondición | Experiencia en Borrador. |
| Postcondición | Nuevo ítem activo, de origen "creado_docente". |
| Fuente | Ventana 009, ADR-026 |
| Incremento | I2 |

#### RF-03-08 — Con la experiencia Publicada, el banco debe ser de solo lectura.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | Funcional |
| Actor | Docente |
| Detalle | No se puede editar, descartar, reincluir ni agregar ítems; la pantalla lo avisa. |
| Precondición | Experiencia Publicada. |
| Postcondición | — |
| Fuente | Ventana 009, ADR-026 |
| Incremento | I2 |

### SUB-04 — Diagnóstico

#### RF-04-01 — El sistema debe listar las experiencias del estudiante con su progreso, con búsqueda y filtro por progreso.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Estudiante |
| Detalle | Progreso: No iniciada, En curso o Completada. Cada una muestra "Área · Nombre del docente". |
| Precondición | Sesión de estudiante. |
| Postcondición | — |
| Fuente | Ventana 001 |
| Incremento | I3 |

#### RF-04-02 — El sistema debe permitir unirse a una experiencia con su código de invitación.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Estudiante |
| Detalle | Código inexistente o experiencia en Borrador: mensaje de error, sin borrar lo escrito. Si el estudiante ya estaba inscrito, entra directo. |
| Precondición | La experiencia está Publicada. |
| Postcondición | Existe la inscripción y el estudiante entra a la pantalla de inicio del diagnóstico. |
| Fuente | Ventana 005, Ventana 020 |
| Incremento | I3 |

#### RF-04-03 — El sistema debe mostrar la pantalla de inicio de la experiencia según el progreso del estudiante.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Estudiante |
| Detalle | No iniciada: botón "Comenzar diagnóstico". En curso: botón "Continuar diagnóstico". Completada: aviso, sin botón. |
| Precondición | Estudiante inscrito. |
| Postcondición | — |
| Fuente | Ventana 020 |
| Incremento | I3 |

#### RF-04-04 — El sistema debe presentar las evidencias en el orden oficial del DBA y, dentro de cada una, ítems al azar entre los activos que el estudiante todavía no vio.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | Funcional |
| Actor | — |
| Detalle | No se pasa a la siguiente evidencia sin concluir la actual. Cada vez que se muestra un ítem se registra con su orden y su fecha. |
| Precondición | Estudiante en el diagnóstico. |
| Postcondición | Queda registrada la presentación del ítem. |
| Fuente | Ventana 021, ADR-024, ADR-031 |
| Incremento | I3 |

#### RF-04-05 — El sistema debe permitir responder cada ítem con selectores, en dos pasos: primero la respuesta, después la certeza de 0 a 5.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Estudiante |
| Detalle | Sin arrastrar: emparejar y ordenar también se responden con selectores. En la certeza, los extremos se rotulan "Adiviné" y "Segurísimo/a", y se recuerda lo que respondió. Cada paso se habilita al elegir. |
| Precondición | Ítem presentado. |
| Postcondición | Al confirmar la certeza, se registra la respuesta (RF-04-06). |
| Fuente | Ventana 021, Ventana 022, ADR-008, ADR-028 |
| Incremento | I3 |

#### RF-04-06 — El sistema debe registrar cada respuesta al confirmarla: opciones elegidas, certeza, fecha y si fue correcta.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | Funcional |
| Actor | — |
| Detalle | Correcta: en selección única, si eligió la opción correcta; en emparejamiento y ordenamiento, solo si todos los pares o posiciones están bien. |
| Precondición | Respuesta y certeza elegidas. |
| Postcondición | Respuesta guardada; no se pierde aunque el estudiante salga después. |
| Fuente | Ventana 022, ADR-019, ADR-021, ADR-031 |
| Incremento | I3 |

#### RF-04-07 — El sistema debe concluir cada evidencia con la regla adaptativa: mínimo 4 respuestas, tope 6.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | Funcional |
| Actor | — |
| Detalle | Una señal fuerte es una respuesta con certeza de 3 a 5 (correcta: "muestra"; incorrecta: "no muestra"); con certeza 0 a 2 es débil. Desde la 4.ª respuesta, si más de la mitad son señales fuertes de "muestra", concluye Muestra; si más de la mitad son de "no muestra", concluye No muestra; con 6 respuestas sin cumplirse, No concluyente. |
| Precondición | Respuesta registrada. |
| Postcondición | Al concluir, se guarda el resultado de esa evidencia como fotografía del momento. |
| Fuente | ADR-016, ADR-021, ADR-031 |
| Incremento | I3 |

#### RF-04-08 — El diagnóstico debe ser de un solo sentido, sin contador de preguntas y sin mostrarle resultados al estudiante.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | Funcional |
| Actor | Estudiante |
| Detalle | No se vuelve a una pregunta respondida; no hay barra ni número de progreso (la cantidad varía); el estudiante no ve si acertó, ni su resultado por evidencia, ni el estado general. |
| Precondición | — |
| Postcondición | — |
| Fuente | Ventana 021, Ventana 022, Ventana 023, ADR-028 |
| Incremento | I3 |

#### RF-04-09 — El sistema debe permitir retomar el diagnóstico donde quedó.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Estudiante |
| Detalle | Si salió con una pregunta mostrada y sin responder, al volver ve esa misma pregunta; si no, continúa con la regla normal. |
| Precondición | Diagnóstico En curso. |
| Postcondición | — |
| Fuente | Ventana 020, ADR-031 |
| Incremento | I3 |

#### RF-04-10 — El sistema debe advertir antes de cerrar o abandonar la página en medio del diagnóstico.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | Funcional |
| Actor | Estudiante |
| Detalle | Advertencia del navegador. Las respuestas ya confirmadas no se pierden. |
| Precondición | Pregunta o certeza en pantalla. |
| Postcondición | — |
| Fuente | Ventana 021, Ventana 022, ADR-028 |
| Incremento | I3 |

#### RF-04-11 — El sistema debe mostrar un cierre al concluir todas las evidencias y volver al inicio.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Estudiante |
| Detalle | El cierre dice que el docente puede ver los resultados. |
| Precondición | Todas las evidencias concluidas. |
| Postcondición | La experiencia figura como Completada. |
| Fuente | Ventana 023 |
| Incremento | I3 |

#### RF-04-12 — El sistema debe permitir salir de una experiencia, con confirmación que diga qué se pierde.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Estudiante |
| Detalle | La confirmación dice cuántas respuestas se eliminan y que para volver necesita el código otra vez. |
| Precondición | Estudiante inscrito. |
| Postcondición | La inscripción y lo que ese estudiante respondió se borran en cascada; nada más (ADR-035). |
| Fuente | Ventana 025, Ventana 020, ADR-035 |
| Incremento | I3 |

### SUB-05 — Reporte y seguimiento

#### RF-05-01 — El sistema debe calcular, por estudiante, el estado general frente al DBA.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | Funcional |
| Actor | — |
| Detalle | Con precedencia: No muestra (al menos una evidencia concluida lo indica); Muestra (todas concluidas y todas muestran); No concluyente (todas concluidas y alguna ambigua); Sin concluir (le falta concluir alguna). Se calcula, no se guarda. |
| Precondición | — |
| Postcondición | — |
| Fuente | ADR-018, ADR-022 |
| Incremento | I4 |

#### RF-05-02 — El sistema debe mostrar el Reporte de la experiencia: cuántos estudiantes hay en cada estado general y, por evidencia, la distribución de resultados con su clasificación.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente |
| Detalle | Clasificación por evidencia, sobre N estudiantes inscritos: Datos insuficientes si "no concluyente" + "sin concluir" ≥ 40 % de N; si no, Brecha aparente si al menos 1 tiene "no muestra"; si no, Sin brecha aparente. Los umbrales los fija el sistema. Ningún texto redactado por IA. |
| Precondición | Al menos un estudiante inscrito. |
| Postcondición | — |
| Fuente | Ventana 010, ADR-010, ADR-013, ADR-017, ADR-023, ADR-032 |
| Incremento | I4 |

#### RF-05-03 — El sistema debe listar a los estudiantes de la experiencia agrupados por estado general, con búsqueda por nombre.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente |
| Detalle | Orden de los grupos: No muestra, No concluyente, Sin concluir, Muestra; alfabético dentro de cada uno; grupos vacíos ocultos. Cada estudiante se expande para ver su resultado en cada evidencia. Sin correo del estudiante. |
| Precondición | Experiencia Publicada con estudiantes. |
| Postcondición | — |
| Fuente | Ventana 011, ADR-022, ADR-029 |
| Incremento | I4 |

#### RF-05-04 — El sistema debe mostrar el historial de un estudiante: qué ítems se le mostraron, en qué orden, qué respondió, si fue correcto y con qué certeza.

| Campo | Valor |
|---|---|
| Requerimiento de | Usuario |
| Tipo | Funcional |
| Actor | Docente |
| Detalle | Agrupado por evidencia en orden oficial, con el resultado de cada evidencia. Las preguntas mostradas y no respondidas aparecen como tales. Solo lectura. |
| Precondición | El estudiante está inscrito en la experiencia del docente. |
| Postcondición | — |
| Fuente | Ventana 027, ADR-028 |
| Incremento | I4 |

### SUB-06 — Catálogo curricular

#### RF-06-01 — El sistema debe contener el catálogo de DBA del MEN de Matemáticas, Lenguaje, Ciencias Naturales y Ciencias Sociales, con sus evidencias y su ejemplo.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | Funcional |
| Actor | — |
| Detalle | Texto oficial, sin simplificar ni reescribir. Datos de solo lectura para los usuarios. Problemas conocidos de extracción: QA-013, pendiente. |
| Precondición | — |
| Postcondición | — |
| Fuente | Ventana 003, ADR-001, ADR-011 |
| Incremento | I2 |

#### RF-06-02 — El sistema debe registrar, por evidencia, si admite formato cerrado, y solo incluir en una experiencia las que sí.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | Funcional |
| Actor | — |
| Detalle | Es un juicio del proyecto, no un dato del MEN. Las evidencias que no lo admiten se muestran marcadas al elegir el DBA. Censo pendiente: QA-014. |
| Precondición | — |
| Postcondición | — |
| Fuente | Ventana 003, ADR-006 |
| Incremento | I2 |

### SUB-00 — Transversales (no funcionales)

#### RNF-01 — La interfaz debe diseñarse solo para computador.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | No funcional |
| Actor | — |
| Detalle | Lienzo de diseño de 1440 × 900. No hay versión para celular. |
| Precondición | — |
| Postcondición | — |
| Fuente | ADR-025 |
| Incremento | Todos |

#### RNF-02 — La interfaz debe estar en español.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | No funcional |
| Actor | — |
| Detalle | Ninguna tarea depende de otro idioma. |
| Precondición | — |
| Postcondición | — |
| Fuente | `29-guion-tecnico.md` |
| Incremento | Todos |

#### RNF-03 — La interfaz debe cumplir WCAG 2.2 nivel AA.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | No funcional |
| Actor | — |
| Detalle | Contraste de texto verificado; zonas clicables de al menos 24 × 24 px; ninguna tarea por arrastre; ninguna tarea depende de audio o video. Excepción conocida y declarada: V-10 (un gris de 3,5:1), diferida. |
| Precondición | — |
| Postcondición | — |
| Fuente | `29-guion-tecnico.md`, `30-indice-recursos.md` |
| Incremento | Todos |

#### RNF-04 — Ningún texto del sistema debe afirmar certeza sobre el aprendizaje de un estudiante.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | No funcional |
| Actor | — |
| Detalle | Prohibidos "domina", "aprobó" y equivalentes; nunca un puntaje; los resultados son probables. |
| Precondición | — |
| Postcondición | — |
| Fuente | ADR-008 |
| Incremento | Todos |

#### RNF-05 — El sistema debe guardar solo los datos del estudiante necesarios para el diagnóstico.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | No funcional |
| Actor | — |
| Detalle | Nombres, apellidos, correo, foto opcional, inscripciones, presentaciones, respuestas con certeza y resultados. No fecha de nacimiento, documento, institución ni curso. |
| Precondición | — |
| Postcondición | — |
| Fuente | ADR-029 |
| Incremento | Todos |

#### RNF-06 — Esta versión no debe usarse con estudiantes reales mientras no registre la autorización del acudiente.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | No funcional |
| Actor | — |
| Detalle | Condición no satisfecha y declarada, por la Ley 1581 de 2012 (art. 7). Es una demostración para docentes. |
| Precondición | — |
| Postcondición | — |
| Fuente | ADR-029, ADR-025 |
| Incremento | Todos |

#### RNF-07 — El sistema no debe confirmar si un correo está registrado a quien no inició sesión.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | No funcional |
| Actor | — |
| Detalle | Aplica a recuperar contraseña. Al registrarse sí se avisa, porque es inevitable para no duplicar cuentas. |
| Precondición | — |
| Postcondición | — |
| Fuente | Ventana 018, Ventana 014 |
| Incremento | I1 |

#### RNF-08 — Las contraseñas no deben guardarse en texto legible.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | No funcional |
| Actor | — |
| Detalle | Se guardan con una función de hash para contraseñas. *Agregado por ingeniería (práctica estándar de seguridad), no por una decisión previa del proyecto.* |
| Precondición | — |
| Postcondición | — |
| Fuente | Práctica estándar (OWASP) |
| Incremento | I1 |

#### RNF-09 — Las claves de los servicios externos y de la base de datos no deben estar en el repositorio.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | No funcional |
| Actor | — |
| Detalle | Claves de IA, base de datos y firma de sesiones, en variables de entorno excluidas del control de versiones. |
| Precondición | — |
| Postcondición | — |
| Fuente | ADR-030, `.gitignore` |
| Incremento | Todos |

#### RNF-10 — Un ítem ya presentado a un estudiante, y el banco de una experiencia publicada, no deben poder modificarse.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | No funcional |
| Actor | — |
| Detalle | Protege que lo respondido siga correspondiendo a lo que se mostró. |
| Precondición | — |
| Postcondición | — |
| Fuente | ADR-026, RI-10 (MER) |
| Incremento | I2 |

#### RNF-11 — Los resultados deben guardarse como fotografía del momento en que se concluyeron.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | No funcional |
| Actor | — |
| Detalle | No se recalculan al vuelo si algo cambia después. |
| Precondición | — |
| Postcondición | — |
| Fuente | ADR-021 |
| Incremento | I3 |

#### RNF-12 — Toda espera del servidor debe mostrarse con una pantalla de carga que nombre la acción.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | No funcional |
| Actor | — |
| Detalle | Generando las preguntas, guardando tu perfil, eliminando, etc. No se puede cerrar mientras espera. |
| Precondición | — |
| Postcondición | — |
| Fuente | Ventana 024, ADR-027 |
| Incremento | Todos |

#### RNF-13 — El tiempo límite de la generación del banco debe medirse y registrarse al construir el incremento 2.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | No funcional |
| Actor | — |
| Detalle | Hoy no tiene número: un valor sin medir sería inventado. Con un DBA de muchas evidencias, la espera puede ser de minutos. |
| Precondición | — |
| Postcondición | — |
| Fuente | ADR-027, ADR-030 |
| Incremento | I2 |

#### RNF-14 — El backend debe construirse con NestJS y MySQL.

| Campo | Valor |
|---|---|
| Requerimiento de | Sistema |
| Tipo | No funcional |
| Actor | — |
| Detalle | Exigencia del curso DSE-2; el acceso ya empezó así (`DSE-2/backend-auth/`). |
| Precondición | — |
| Postcondición | — |
| Fuente | Curso DSE-2 |
| Incremento | Todos |

## 4. Trazabilidad: ventana → requerimientos

Toda ventana especificada en la Fase II está cubierta por al menos un requerimiento (lo comprueba el generador).

| Ventana | Requerimientos |
|---|---|
| 001 | RF-01-10, RF-01-11, RF-02-01, RF-04-01 |
| 002 | RF-02-02 |
| 003 | RF-02-02, RF-06-01, RF-06-02 |
| 004 | RF-02-02, RF-02-03 |
| 005 | RF-04-02 |
| 006 | RF-02-04, RF-02-07 |
| 007 | RF-02-04 |
| 008 | RF-02-04 |
| 009 | RF-03-04, RF-03-05, RF-03-06, RF-03-07, RF-03-08 |
| 010 | RF-05-02 |
| 011 | RF-02-04, RF-02-05, RF-02-06, RF-05-03 |
| 012 | RF-02-05 |
| 013 | RF-02-06 |
| 014 | RF-01-01, RF-01-02, RF-01-04, RF-01-07, RF-01-10, RNF-07 |
| 015 | RF-01-01, RF-01-03, RF-01-08 |
| 016 | RF-01-02, RF-01-05 |
| 017 | RF-01-06 |
| 018 | RF-01-08, RNF-07 |
| 019 | RF-01-09 |
| 020 | RF-04-02, RF-04-03, RF-04-09, RF-04-12 |
| 021 | RF-04-04, RF-04-05, RF-04-08, RF-04-10 |
| 022 | RF-04-05, RF-04-06, RF-04-08, RF-04-10 |
| 023 | RF-04-08, RF-04-11 |
| 024 | RF-02-03, RNF-12 |
| 025 | RF-02-07, RF-04-12 |
| 026 | RF-01-11 |
| 027 | RF-05-04 |

## 5. Vacíos que estos requerimientos heredan, declarados

- ~~**V-11**~~ — **cerrado por ADR-035** (2026-10-26): eliminar una experiencia (RF-02-07) o salir de una (RF-04-12) borra en cascada lo que depende de ella.
- **QA-013 / QA-014** — errores de extracción del catálogo y censo de formato cerrado (RF-06-01, RF-06-02).
- **V-10** — una excepción de contraste, diferida (RNF-03).
- **RNF-13** — el tiempo límite de la generación no tiene número todavía; se mide.
- **RNF-06** — la autorización del acudiente: condición no satisfecha que impide usar el sistema con estudiantes reales.
