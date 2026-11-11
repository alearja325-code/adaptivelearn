#!/usr/bin/env python3
"""Fuente unica de los requerimientos de AdaptiveLearn (MODESEC Fase III).

Genera ../11-analisis-requerimientos.md y verifica antes de escribir:
  - que toda Ventana especificada (001-027) este cubierta por algun requerimiento
  - que toda ADR citada exista en diseno/decisiones.md
  - que no haya identificadores repetidos
  - que cada subsistema tenga al menos un requerimiento funcional
  - que todo requerimiento tenga al menos una fuente

Uso: python3 requerimientos.py
"""
import glob, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
F3 = os.path.dirname(AQUI)
MODESEC = os.path.dirname(F3)
F2 = os.path.join(MODESEC, "fase-2-diseno-multimedial")
# 2026-10-24: en el repositorio nuevo, diseno/ vive junto a modesec/
# dentro de docs/ (antes estaba en la raiz de AdaptiveLearn-V3).
DOCS = os.path.dirname(MODESEC)
DECISIONES = os.path.join(DOCS, "diseno", "decisiones.md")

FECHA = "2026-10-21 (actualizado 2026-10-26)"
RESPONSABLE = "Área 2 — Levantamiento de requerimientos (`EQUIPO.md`; nombre por asignar)"

SUB = {
    "SUB-01": "Acceso y perfil",
    "SUB-02": "Gestión de experiencias",
    "SUB-03": "Banco de preguntas",
    "SUB-04": "Diagnóstico",
    "SUB-05": "Reporte y seguimiento",
    "SUB-06": "Catálogo curricular",
    "SUB-00": "Transversales (no funcionales)",
}

# Cada requerimiento:
# id, sub, de ("Usuario"|"Sistema"), tipo ("Funcional"|"No funcional"),
# actor, enunciado, detalle, pre, post, fuentes, incremento
R = []
def req(id, sub, de, tipo, actor, enunciado, detalle, pre, post, fuentes, inc):
    R.append(dict(id=id, sub=sub, de=de, tipo=tipo, actor=actor,
                  enunciado=enunciado, detalle=detalle, pre=pre, post=post,
                  fuentes=fuentes, inc=inc))

F, NF, U, S = "Funcional", "No funcional", "Usuario", "Sistema"

# ===================================================== SUB-01 Acceso y perfil
req("RF-01-01", "SUB-01", U, F, "Visitante",
    "El sistema debe permitir crear una cuenta con correo y contraseña.",
    "La contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula y un número; el botón se habilita solo cuando se cumple. Sin campo de confirmar contraseña: se puede mostrar u ocultar lo escrito. Sin casilla de términos: el documento no existe.",
    "El correo no está registrado.", "Se envía un código de verificación al correo y se pasa a verificarlo.",
    ["V-014", "V-015"], "I1")
req("RF-01-02", "SUB-01", U, F, "Visitante",
    "El sistema debe permitir crear una cuenta o iniciar sesión con Google o con Microsoft.",
    "Sin Apple (exige cuenta de desarrollador de pago y la plataforma es web). Quien entra así no verifica correo: lo hizo el proveedor. Nombres, apellidos y foto llegan prellenados y editables.",
    "El proveedor autentica a la persona.", "Cuenta nueva: pasa a completar perfil. Cuenta existente: entra al Dashboard.",
    ["V-014", "V-016"], "I1")
req("RF-01-03", "SUB-01", U, F, "Visitante",
    "El sistema debe verificar el correo con un código numérico de 6 dígitos enviado a ese correo.",
    "El código se puede reenviar después de una cuenta regresiva de 30 segundos. Código incorrecto: mensaje de error, sin borrar lo escrito. La misma pantalla sirve al registro y a la recuperación de contraseña; su enlace \"Volver\" regresa al paso anterior de cada flujo.",
    "Se envió un código al correo.", "Registro: pasa a completar perfil. Recuperación: pasa a nueva contraseña.",
    ["V-015"], "I1")
req("RF-01-04", "SUB-01", S, F, "Visitante",
    "El sistema no debe crear cuentas duplicadas ni vincular métodos de acceso para un mismo correo.",
    "Si el correo ya está registrado con otro método, se avisa cuál usar; si está registrado con el mismo, se avisa que ya existe.",
    "Se intenta registrar o entrar con un correo existente.", "No se crea ni se modifica ninguna cuenta.",
    ["V-014"], "I1")
req("RF-01-05", "SUB-01", U, F, "Visitante",
    "El sistema debe pedir nombres y apellidos, y permitir subir una foto de perfil opcional.",
    "Foto: JPG o PNG, máximo 5 MB, recorte cuadrado automático, sin editor. Archivo inválido: mensaje de error y la foto no cambia. \"Continuar\" se habilita con nombres y apellidos llenos.",
    "Correo verificado o acceso con proveedor.", "Pasa a elegir rol; la cuenta todavía no existe.",
    ["V-016"], "I1")
req("RF-01-06", "SUB-01", U, F, "Visitante",
    "El sistema debe pedir elegir rol —Docente o Estudiante— una sola vez, y crear la cuenta en ese momento.",
    "El rol no se puede cambiar después; la pantalla lo advierte. Docente y Estudiante son tipos de usuario separados.",
    "Perfil completo.", "Existe la cuenta con su rol, y la persona entra a su Dashboard.",
    ["V-017"], "I1")
req("RF-01-07", "SUB-01", U, F, "Docente, Estudiante",
    "El sistema debe permitir iniciar sesión con correo y contraseña.",
    "Credenciales incorrectas: mensaje de error genérico. Si la persona creó su cuenta pero no terminó el registro (no eligió rol), retoma en completar perfil (ADR-035).",
    "La cuenta existe.", "La persona entra al Dashboard de su rol, o retoma su registro.",
    ["V-014", "ADR-035"], "I1")
req("RF-01-08", "SUB-01", U, F, "Docente, Estudiante",
    "El sistema debe permitir recuperar la contraseña mediante un código enviado al correo.",
    "Al enviar la solicitud, siempre avanza a verificar el código, exista o no la cuenta: no confirma a un desconocido si un correo está registrado. Solo valida el formato del correo.",
    "La persona no recuerda su contraseña.", "Si la cuenta existe, se envía el código.",
    ["V-018", "V-015"], "I1")
req("RF-01-09", "SUB-01", U, F, "Docente, Estudiante",
    "El sistema debe permitir definir una contraseña nueva después de verificar el código.",
    "Mismas reglas que al registrarse. \"Guardar\" se habilita solo cuando se cumplen.",
    "Código de recuperación válido.", "La contraseña cambia y se vuelve a iniciar sesión, con un mensaje de confirmación.",
    ["V-019"], "I1")
req("RF-01-10", "SUB-01", U, F, "Docente, Estudiante",
    "El sistema debe permitir cerrar la sesión desde el menú lateral.",
    "Sin confirmación: no se pierde nada.",
    "Sesión iniciada.", "La sesión termina y se muestra iniciar sesión.",
    ["V-001", "V-014"], "I1")
req("RF-01-11", "SUB-01", U, F, "Docente, Estudiante",
    "El sistema debe permitir editar nombres, apellidos y foto desde el bloque de perfil del menú lateral.",
    "Todo el bloque (foto, nombre, correo) abre la edición. El correo se muestra y no se edita; el rol no se edita; la foto se reemplaza, no se quita. \"Guardar cambios\" se habilita solo si hay cambios y los dos campos están llenos.",
    "Sesión iniciada.", "Los datos quedan guardados y el menú lateral se actualiza.",
    ["V-026", "V-001"], "I1")

# ============================================ SUB-02 Gestión de experiencias
req("RF-02-01", "SUB-02", U, F, "Docente",
    "El sistema debe listar las experiencias del docente, con búsqueda y filtro por estado.",
    "Cada una muestra estado (Borrador / Publicada), nombre y \"Área · Grado · N estudiantes\". Sin experiencias: mensaje de lista vacía.",
    "Sesión de docente.", "—",
    ["V-001"], "I2")
req("RF-02-02", "SUB-02", U, F, "Docente",
    "El sistema debe permitir crear una experiencia en tres pasos: área, DBA y nombre.",
    "Paso 1: una de las 4 áreas. Paso 2: el DBA del área, con búsqueda y filtro por grado (1° a 11°), viendo su enunciado, sus evidencias (marcadas las que no admiten formato cerrado) y su ejemplo. Paso 3: nombre, prellenado con el enunciado del DBA y editable, obligatorio. Se puede volver a un paso anterior sin perder lo elegido.",
    "Sesión de docente.", "Se dispara la generación del banco (RF-03-01).",
    ["V-002", "V-003", "V-004", "ADR-024"], "I2")
req("RF-02-03", "SUB-02", S, F, "Docente",
    "La creación de una experiencia debe ser \"todo o nada\": la experiencia se guarda solo si su banco se generó completo.",
    "Mientras se genera, el docente ve la espera \"Generando las preguntas...\". Si la generación falla del todo, no se guarda nada y el Paso 3 muestra el error con el nombre y el DBA intactos, para reintentar.",
    "El docente confirmó el Paso 3.", "Éxito: experiencia en Borrador, con su banco, y el docente entra a ella. Falla: nada guardado.",
    ["V-004", "V-024", "ADR-027"], "I2")
req("RF-02-04", "SUB-02", U, F, "Docente",
    "El sistema debe mostrar la experiencia con tres pestañas: Resumen, Materiales y Estudiantes.",
    "Encabezado con el nombre y fila de datos: Estado, Creada, Estudiantes, Área, Grado. Resumen describe el DBA; Materiales da acceso al banco y al reporte; Estudiantes, al grupo.",
    "El docente es el dueño de la experiencia.", "—",
    ["V-006", "V-007", "V-008", "V-011"], "I2")
req("RF-02-05", "SUB-02", U, F, "Docente",
    "El sistema debe permitir publicar una experiencia, con confirmación.",
    "Solo se puede publicar si cada evidencia incluida tiene al menos 6 ítems activos; si no, el botón está deshabilitado y explica por qué. La confirmación advierte que no se puede deshacer y que el banco quedará congelado.",
    "Experiencia en Borrador con ≥ 6 ítems activos por evidencia incluida.", "Experiencia Publicada; banco de solo lectura; el código de invitación se puede mostrar.",
    ["V-011", "V-012", "ADR-026"], "I2")
req("RF-02-06", "SUB-02", S, F, "Docente",
    "El sistema debe generar un código de invitación único al crear cada experiencia, y mostrarlo solo cuando esté publicada.",
    "6 caracteres, letras y números, sin caracteres ambiguos (0/O, 1/I/L), sin distinguir mayúsculas. Se muestra en una ventana propia con botón para copiarlo.",
    "Experiencia Publicada (para mostrarlo).", "El docente puede compartir el código.",
    ["V-013", "V-011"], "I2")
req("RF-02-07", "SUB-02", U, F, "Docente",
    "El sistema debe permitir eliminar una experiencia, con confirmación que diga qué se pierde.",
    "Se permite siempre, aunque tenga estudiantes o respuestas; la confirmación dice cuántos estudiantes inscritos y cuántas respuestas se eliminan, y que es irreversible.",
    "El docente es el dueño.", "La experiencia y todo lo que depende de ella —banco, inscripciones y lo respondido— se borran en cascada (ADR-035).",
    ["V-025", "V-006", "ADR-035"], "I2")

# ===================================================== SUB-03 Banco de preguntas
req("RF-03-01", "SUB-03", S, F, "Servicio de IA",
    "El sistema debe generar con IA un banco de 12 ítems por cada evidencia incluida de la experiencia.",
    "Solo entran las evidencias cuyo dictamen admite formato cerrado. El formato de los ítems lo determina la evidencia (selección única por defecto; emparejamiento si relaciona conjuntos; ordenamiento si es secuencial). El ejemplo del DBA se usa como contexto. Los distractores son plausibles y no se rotulan como un error específico.",
    "Experiencia confirmada en el Paso 3.", "Cada evidencia incluida tiene 12 ítems, con sus opciones, de origen \"ia\".",
    ["ADR-005", "ADR-006", "ADR-008", "ADR-011", "ADR-014", "ADR-016"], "I2")
req("RF-03-02", "SUB-03", S, F, "Servicio de IA",
    "La generación debe usar un servicio de IA principal y, si falla o supera el tiempo límite, uno de respaldo, sin que el docente lo note.",
    "Gemini y DeepSeek; cuál es el principal es un ajuste de configuración. Un banco se genera completo con un solo servicio: si el principal falla a mitad de camino, el respaldo lo genera completo de nuevo. Un ítem generado que no pasa la validación de su formato cuenta como falla del servicio (ADR-035).",
    "Se pidió generar un banco.", "Banco completo de un solo servicio, o error si fallan los dos.",
    ["ADR-030", "ADR-027", "ADR-035"], "I2")
req("RF-03-03", "SUB-03", S, F, "—",
    "Cada ítem debe registrar su origen, y cada experiencia, qué servicio y qué modelo de IA generaron su banco.",
    "Origen del ítem: generado por IA, editado por el docente o creado por el docente. El servicio se guarda una vez en la experiencia, porque un banco sale entero de un solo servicio: un ítem generado o editado es de ese servicio; uno creado por el docente no se atribuye a la IA. El docente no ve el servicio. *(Corregido el 2026-10-26: decía que cada ítem guardaba su servicio; ADR-035 lo cambió.)*",
    "—", "—",
    ["ADR-026", "ADR-030", "ADR-035"], "I2")
req("RF-03-04", "SUB-03", U, F, "Docente",
    "El sistema debe mostrar el banco agrupado por evidencia, en el orden oficial del DBA, con búsqueda y filtro por formato.",
    "Cada evidencia muestra cuántos ítems activos tiene; si son menos de 6, en rojo y con cuántos faltan para publicar. Cada ítem se expande para ver su enunciado y su respuesta correcta.",
    "Experiencia del docente.", "—",
    ["V-009", "ADR-024", "ADR-026"], "I2")
req("RF-03-05", "SUB-03", U, F, "Docente",
    "El sistema debe permitir editar un ítem —enunciado, opciones y respuesta correcta— con Guardar y Cancelar.",
    "Se pueden agregar o quitar opciones sin bajar del mínimo del formato (2 en selección única y ordenamiento, 4 en emparejamiento). \"Guardar\" se habilita solo si el ítem es válido: nada vacío, mínimo de opciones, exactamente una correcta en selección única, números de orden completos y sin repetir en emparejamiento y ordenamiento.",
    "Experiencia en Borrador.", "Ítem guardado; su origen pasa a \"editado_docente\".",
    ["V-009", "ADR-026"], "I2")
req("RF-03-06", "SUB-03", U, F, "Docente",
    "El sistema debe permitir descartar un ítem y volver a incluirlo, sin confirmación.",
    "Descartar no borra el ítem: lo excluye de lo que ven los estudiantes y se puede revertir.",
    "Experiencia en Borrador.", "El ítem queda excluido o incluido, y el contador de su evidencia se actualiza.",
    ["V-009", "ADR-015"], "I2")
req("RF-03-07", "SUB-03", U, F, "Docente",
    "El sistema debe permitir agregar una pregunta propia a cualquier evidencia.",
    "Se crea con el formato de esa evidencia y el mínimo de opciones vacías, ya en modo edición; se guarda con las mismas reglas de RF-03-05. Cancelar antes de guardar la descarta.",
    "Experiencia en Borrador.", "Nuevo ítem activo, de origen \"creado_docente\".",
    ["V-009", "ADR-026"], "I2")
req("RF-03-08", "SUB-03", S, F, "Docente",
    "Con la experiencia Publicada, el banco debe ser de solo lectura.",
    "No se puede editar, descartar, reincluir ni agregar ítems; la pantalla lo avisa.",
    "Experiencia Publicada.", "—",
    ["V-009", "ADR-026"], "I2")

# ========================================================= SUB-04 Diagnóstico
req("RF-04-01", "SUB-04", U, F, "Estudiante",
    "El sistema debe listar las experiencias del estudiante con su progreso, con búsqueda y filtro por progreso.",
    "Progreso: No iniciada, En curso o Completada. Cada una muestra \"Área · Nombre del docente\".",
    "Sesión de estudiante.", "—",
    ["V-001"], "I3")
req("RF-04-02", "SUB-04", U, F, "Estudiante",
    "El sistema debe permitir unirse a una experiencia con su código de invitación.",
    "Código inexistente o experiencia en Borrador: mensaje de error, sin borrar lo escrito. Si el estudiante ya estaba inscrito, entra directo.",
    "La experiencia está Publicada.", "Existe la inscripción y el estudiante entra a la pantalla de inicio del diagnóstico.",
    ["V-005", "V-020"], "I3")
req("RF-04-03", "SUB-04", U, F, "Estudiante",
    "El sistema debe mostrar la pantalla de inicio de la experiencia según el progreso del estudiante.",
    "No iniciada: botón \"Comenzar diagnóstico\". En curso: botón \"Continuar diagnóstico\". Completada: aviso, sin botón.",
    "Estudiante inscrito.", "—",
    ["V-020"], "I3")
req("RF-04-04", "SUB-04", S, F, "—",
    "El sistema debe presentar las evidencias en el orden oficial del DBA y, dentro de cada una, ítems al azar entre los activos que el estudiante todavía no vio.",
    "No se pasa a la siguiente evidencia sin concluir la actual. Cada vez que se muestra un ítem se registra con su orden y su fecha.",
    "Estudiante en el diagnóstico.", "Queda registrada la presentación del ítem.",
    ["V-021", "ADR-024", "ADR-031"], "I3")
req("RF-04-05", "SUB-04", U, F, "Estudiante",
    "El sistema debe permitir responder cada ítem con selectores, en dos pasos: primero la respuesta, después la certeza de 0 a 5.",
    "Sin arrastrar: emparejar y ordenar también se responden con selectores. En la certeza, los extremos se rotulan \"Adiviné\" y \"Segurísimo/a\", y se recuerda lo que respondió. Cada paso se habilita al elegir.",
    "Ítem presentado.", "Al confirmar la certeza, se registra la respuesta (RF-04-06).",
    ["V-021", "V-022", "ADR-008", "ADR-028"], "I3")
req("RF-04-06", "SUB-04", S, F, "—",
    "El sistema debe registrar cada respuesta al confirmarla: opciones elegidas, certeza, fecha y si fue correcta.",
    "Correcta: en selección única, si eligió la opción correcta; en emparejamiento y ordenamiento, solo si todos los pares o posiciones están bien.",
    "Respuesta y certeza elegidas.", "Respuesta guardada; no se pierde aunque el estudiante salga después.",
    ["V-022", "ADR-019", "ADR-021", "ADR-031"], "I3")
req("RF-04-07", "SUB-04", S, F, "—",
    "El sistema debe concluir cada evidencia con la regla adaptativa: mínimo 4 respuestas, tope 6.",
    "Una señal fuerte es una respuesta con certeza de 3 a 5 (correcta: \"muestra\"; incorrecta: \"no muestra\"); con certeza 0 a 2 es débil. Desde la 4.ª respuesta, si más de la mitad son señales fuertes de \"muestra\", concluye Muestra; si más de la mitad son de \"no muestra\", concluye No muestra; con 6 respuestas sin cumplirse, No concluyente.",
    "Respuesta registrada.", "Al concluir, se guarda el resultado de esa evidencia como fotografía del momento.",
    ["ADR-016", "ADR-021", "ADR-031"], "I3")
req("RF-04-08", "SUB-04", S, F, "Estudiante",
    "El diagnóstico debe ser de un solo sentido, sin contador de preguntas y sin mostrarle resultados al estudiante.",
    "No se vuelve a una pregunta respondida; no hay barra ni número de progreso (la cantidad varía); el estudiante no ve si acertó, ni su resultado por evidencia, ni el estado general.",
    "—", "—",
    ["V-021", "V-022", "V-023", "ADR-028"], "I3")
req("RF-04-09", "SUB-04", U, F, "Estudiante",
    "El sistema debe permitir retomar el diagnóstico donde quedó.",
    "Si salió con una pregunta mostrada y sin responder, al volver ve esa misma pregunta; si no, continúa con la regla normal.",
    "Diagnóstico En curso.", "—",
    ["V-020", "ADR-031"], "I3")
req("RF-04-10", "SUB-04", S, F, "Estudiante",
    "El sistema debe advertir antes de cerrar o abandonar la página en medio del diagnóstico.",
    "Advertencia del navegador. Las respuestas ya confirmadas no se pierden.",
    "Pregunta o certeza en pantalla.", "—",
    ["V-021", "V-022", "ADR-028"], "I3")
req("RF-04-11", "SUB-04", U, F, "Estudiante",
    "El sistema debe mostrar un cierre al concluir todas las evidencias y volver al inicio.",
    "El cierre dice que el docente puede ver los resultados.",
    "Todas las evidencias concluidas.", "La experiencia figura como Completada.",
    ["V-023"], "I3")
req("RF-04-12", "SUB-04", U, F, "Estudiante",
    "El sistema debe permitir salir de una experiencia, con confirmación que diga qué se pierde.",
    "La confirmación dice cuántas respuestas se eliminan y que para volver necesita el código otra vez.",
    "Estudiante inscrito.", "La inscripción y lo que ese estudiante respondió se borran en cascada; nada más (ADR-035).",
    ["V-025", "V-020", "ADR-035"], "I3")

# ============================================== SUB-05 Reporte y seguimiento
req("RF-05-01", "SUB-05", S, F, "—",
    "El sistema debe calcular, por estudiante, el estado general frente al DBA.",
    "Con precedencia: No muestra (al menos una evidencia concluida lo indica); Muestra (todas concluidas y todas muestran); No concluyente (todas concluidas y alguna ambigua); Sin concluir (le falta concluir alguna). Se calcula, no se guarda.",
    "—", "—",
    ["ADR-018", "ADR-022"], "I4")
req("RF-05-02", "SUB-05", U, F, "Docente",
    "El sistema debe mostrar el Reporte de la experiencia: cuántos estudiantes hay en cada estado general y, por evidencia, la distribución de resultados con su clasificación.",
    "Clasificación por evidencia, sobre N estudiantes inscritos: Datos insuficientes si \"no concluyente\" + \"sin concluir\" ≥ 40 % de N; si no, Brecha aparente si al menos 1 tiene \"no muestra\"; si no, Sin brecha aparente. Los umbrales los fija el sistema. Ningún texto redactado por IA.",
    "Al menos un estudiante inscrito.", "—",
    ["V-010", "ADR-010", "ADR-013", "ADR-017", "ADR-023", "ADR-032"], "I4")
req("RF-05-03", "SUB-05", U, F, "Docente",
    "El sistema debe listar a los estudiantes de la experiencia agrupados por estado general, con búsqueda por nombre.",
    "Orden de los grupos: No muestra, No concluyente, Sin concluir, Muestra; alfabético dentro de cada uno; grupos vacíos ocultos. Cada estudiante se expande para ver su resultado en cada evidencia. Sin correo del estudiante.",
    "Experiencia Publicada con estudiantes.", "—",
    ["V-011", "ADR-022", "ADR-029"], "I4")
req("RF-05-04", "SUB-05", U, F, "Docente",
    "El sistema debe mostrar el historial de un estudiante: qué ítems se le mostraron, en qué orden, qué respondió, si fue correcto y con qué certeza.",
    "Agrupado por evidencia en orden oficial, con el resultado de cada evidencia. Las preguntas mostradas y no respondidas aparecen como tales. Solo lectura.",
    "El estudiante está inscrito en la experiencia del docente.", "—",
    ["V-027", "ADR-028"], "I4")

# ======================================================= SUB-06 Catálogo
req("RF-06-01", "SUB-06", S, F, "—",
    "El sistema debe contener el catálogo de DBA del MEN de Matemáticas, Lenguaje, Ciencias Naturales y Ciencias Sociales, con sus evidencias y su ejemplo.",
    "Texto oficial, sin simplificar ni reescribir. Datos de solo lectura para los usuarios. Problemas conocidos de extracción: QA-013, pendiente.",
    "—", "—",
    ["V-003", "ADR-001", "ADR-011"], "I2")
req("RF-06-02", "SUB-06", S, F, "—",
    "El sistema debe registrar, por evidencia, si admite formato cerrado, y solo incluir en una experiencia las que sí.",
    "Es un juicio del proyecto, no un dato del MEN. Las evidencias que no lo admiten se muestran marcadas al elegir el DBA. El censo QA-014 (encargo 05) lo propone para las 1282 evidencias; falta validarlo por muestreo (ADR-042).",
    "—", "—",
    ["V-003", "ADR-006"], "I2")

# ===================================================== SUB-00 No funcionales
req("RNF-01", "SUB-00", S, NF, "—",
    "La interfaz debe diseñarse solo para computador.",
    "Lienzo de diseño de 1440 × 900. No hay versión para celular.",
    "—", "—", ["ADR-025"], "Todos")
req("RNF-02", "SUB-00", S, NF, "—",
    "La interfaz debe estar en español.",
    "Ninguna tarea depende de otro idioma.",
    "—", "—", ["V-029"], "Todos")
req("RNF-03", "SUB-00", S, NF, "—",
    "La interfaz debe cumplir WCAG 2.2 nivel AA.",
    "Contraste de texto verificado; zonas clicables de al menos 24 × 24 px; ninguna tarea por arrastre; ninguna tarea depende de audio o video. Excepción conocida y declarada: V-10 (un gris de 3,5:1), diferida.",
    "—", "—", ["V-029", "V-030"], "Todos")
req("RNF-04", "SUB-00", S, NF, "—",
    "Ningún texto del sistema debe afirmar certeza sobre el aprendizaje de un estudiante.",
    "Prohibidos \"domina\", \"aprobó\" y equivalentes; nunca un puntaje; los resultados son probables.",
    "—", "—", ["ADR-008"], "Todos")
req("RNF-05", "SUB-00", S, NF, "—",
    "El sistema debe guardar solo los datos del estudiante necesarios para el diagnóstico.",
    "Nombres, apellidos, correo, foto opcional, inscripciones, presentaciones, respuestas con certeza y resultados. No fecha de nacimiento, documento, institución ni curso.",
    "—", "—", ["ADR-029"], "Todos")
req("RNF-06", "SUB-00", S, NF, "—",
    "Esta versión no debe usarse con estudiantes reales mientras no registre la autorización del acudiente.",
    "Condición no satisfecha y declarada, por la Ley 1581 de 2012 (art. 7). Es una demostración para docentes.",
    "—", "—", ["ADR-029", "ADR-025"], "Todos")
req("RNF-07", "SUB-00", S, NF, "—",
    "El sistema no debe confirmar si un correo está registrado a quien no inició sesión.",
    "Aplica a recuperar contraseña. Al registrarse sí se avisa, porque es inevitable para no duplicar cuentas.",
    "—", "—", ["V-018", "V-014"], "I1")
req("RNF-08", "SUB-00", S, NF, "—",
    "Las contraseñas no deben guardarse en texto legible.",
    "Se guardan con una función de hash para contraseñas. *Agregado por ingeniería (práctica estándar de seguridad), no por una decisión previa del proyecto.*",
    "—", "—", ["Práctica estándar (OWASP)"], "I1")
req("RNF-09", "SUB-00", S, NF, "—",
    "Las claves de los servicios externos y de la base de datos no deben estar en el repositorio.",
    "Claves de IA, base de datos y firma de sesiones, en variables de entorno excluidas del control de versiones.",
    "—", "—", ["ADR-030", "`.gitignore`"], "Todos")
req("RNF-10", "SUB-00", S, NF, "—",
    "Un ítem ya presentado a un estudiante, y el banco de una experiencia publicada, no deben poder modificarse.",
    "Protege que lo respondido siga correspondiendo a lo que se mostró.",
    "—", "—", ["ADR-026", "RI-10 (MER)"], "I2")
req("RNF-11", "SUB-00", S, NF, "—",
    "Los resultados deben guardarse como fotografía del momento en que se concluyeron.",
    "No se recalculan al vuelo si algo cambia después.",
    "—", "—", ["ADR-021"], "I3")
req("RNF-12", "SUB-00", S, NF, "—",
    "Toda espera del servidor debe mostrarse con una pantalla de carga que nombre la acción.",
    "Generando las preguntas, guardando tu perfil, eliminando, etc. No se puede cerrar mientras espera.",
    "—", "—", ["V-024", "ADR-027"], "Todos")
req("RNF-13", "SUB-00", S, NF, "—",
    "El tiempo límite de la generación del banco debe medirse y registrarse al construir el incremento 2.",
    "Hoy no tiene número: un valor sin medir sería inventado. Con un DBA de muchas evidencias, la espera puede ser de minutos.",
    "—", "—", ["ADR-027", "ADR-030"], "I2")
req("RNF-14", "SUB-00", S, NF, "—",
    "El backend debe construirse con NestJS y MySQL.",
    "Exigencia del curso DSE-2; el acceso ya empezó así (`DSE-2/backend-auth/`).",
    "—", "—", ["Curso DSE-2"], "Todos")

# --------------------------------------------------------- ventanas fuente
# Ventanas que se citan como V-0NN. 029/030 no son ventanas: se mapean a
# documentos de Fase II para RNF-02/03.
DOCS_EXTRA = {"V-029": "29-guion-tecnico.md", "V-030": "30-indice-recursos.md"}


def verificar():
    fallos = []
    ids = [r["id"] for r in R]
    for i in sorted(set(x for x in ids if ids.count(x) > 1)):
        fallos.append(f"identificador repetido: {i}")
    # ventanas especificadas
    esp = set()
    for f in glob.glob(os.path.join(F2, "[0-9][0-9]-spec*.md")):
        m = re.match(r"# Ventana (\d{3})(?:-(\d{3}))?", open(f, encoding="utf-8").readline())
        a = int(m.group(1)); b = int(m.group(2) or a)
        esp |= {f"V-{n:03d}" for n in range(a, b + 1)}
    citadas = {f for r in R for f in r["fuentes"] if f.startswith("V-")}
    for v in sorted(esp - citadas):
        fallos.append(f"{v} no está cubierta por ningún requerimiento")
    for v in sorted(citadas - esp - set(DOCS_EXTRA)):
        fallos.append(f"{v} citada pero no es una ventana especificada")
    # adr citadas
    adrs = set(re.findall(r"^## (ADR-\d{3})", open(DECISIONES, encoding="utf-8").read(), re.M))
    for r in R:
        for f in r["fuentes"]:
            if f.startswith("ADR-") and f not in adrs:
                fallos.append(f"{r['id']}: cita {f}, que no existe")
        if not r["fuentes"]:
            fallos.append(f"{r['id']}: sin fuente")
    for s in SUB:
        if s != "SUB-00" and not any(r["sub"] == s and r["tipo"] == F for r in R):
            fallos.append(f"{s} sin requerimientos funcionales")
    return esp, fallos


def fuente_md(f):
    if f.startswith("V-") and f in DOCS_EXTRA:
        return f"`{DOCS_EXTRA[f]}`"
    if f.startswith("V-"):
        return f"Ventana {f[2:]}"
    return f


def generar(esp):
    L = []
    w = L.append
    w("# 11. Análisis de requerimientos")
    w("")
    w("**Metodología:** MODESEC — Fase III, Diseño Computacional, segunda sub-etapa.")
    w(f"**Fecha:** {FECHA}. **Archivo generado** por `requerimientos/requerimientos.py`; no se edita a mano.")
    w("")
    w("MODESEC pide aquí tener presente *\"la planta física y la población a quien va dirigida\"*, establecer los requerimientos *\"a partir de la necesidad que se presentó en el proceso de enseñanza y aprendizaje\"*, y *\"dividir éstos en secciones denominadas subsistemas y requerimientos funcionales\"*, en el formato de su Tabla 5 (número, enunciado, usuario o sistema, funcional o no funcional, precondición, postcondición, fechas, responsable, modificación).")
    w("")
    w("## 1. Base del análisis")
    w("")
    w("- **Necesidad:** un docente de secundaria no tiene una forma fundamentada de saber, a la escala de las evidencias de un DBA, qué alcanzó cada estudiante de su grupo (`fase-1/01-analisis-necesidad-educativa.docx`, reformulada por la entrevista E0).")
    w("- **Población:** docentes de secundaria en Colombia y sus estudiantes de 6° a 11° (11 a 17 años, menores de edad).")
    w("- **Planta física:** computador con navegador y conexión durante el uso. Cerca de la mitad de las sedes rurales no tenía conexión en 2025 (MinTIC, citado en E0): es una limitación de alcance, declarada (ADR-025).")
    w("- **Fuentes de cada requerimiento:** las ventanas de la Fase II y las decisiones de `diseno/decisiones.md`. No hay un requerimiento sin fuente; los pocos que agrega la ingeniería lo dicen.")
    w("- **El documento E1 de DSE-1** (requerimientos con ISO/IEC/IEEE 29148) se usó solo como contraste, no como base: es anterior a las decisiones de octubre (ADR-026 a ADR-032).")
    w("- **Subsistemas:** los 6 de `10-proceso-desarrollo.md`, más un grupo de transversales para los no funcionales. Cada requerimiento dice en qué incremento se construye (I1 a I4).")
    w("")
    nf = sum(1 for r in R if r["tipo"] == F); nnf = len(R) - nf
    w("## 2. Resumen")
    w("")
    w(f"**{len(R)} requerimientos:** {nf} funcionales y {nnf} no funcionales.")
    w("")
    w("| Subsistema | Funcionales | No funcionales | Incremento |")
    w("|---|---|---|---|")
    for s, nombre in SUB.items():
        rs = [r for r in R if r["sub"] == s]
        incs = sorted(set(r["inc"] for r in rs))
        w(f"| **{s}** {nombre} | {sum(1 for r in rs if r['tipo']==F)} | {sum(1 for r in rs if r['tipo']==NF)} | {', '.join(incs)} |")
    w("")
    w("## 3. Requerimientos, por subsistema")
    w("")
    w("Cada requerimiento va en el formato de la Tabla 5 de MODESEC. Comunes a todos: **fecha de creación** " + FECHA + "; **fecha de procesamiento**: pendiente (se llena al construirlo); **responsable**: " + RESPONSABLE + "; **modificación**: ninguna.")
    w("")
    for s, nombre in SUB.items():
        w(f"### {s} — {nombre}")
        w("")
        for r in [x for x in R if x["sub"] == s]:
            w(f"#### {r['id']} — {r['enunciado']}")
            w("")
            w("| Campo | Valor |")
            w("|---|---|")
            w(f"| Requerimiento de | {r['de']} |")
            w(f"| Tipo | {r['tipo']} |")
            w(f"| Actor | {r['actor']} |")
            w(f"| Detalle | {r['detalle']} |")
            w(f"| Precondición | {r['pre']} |")
            w(f"| Postcondición | {r['post']} |")
            w(f"| Fuente | {', '.join(fuente_md(f) for f in r['fuentes'])} |")
            w(f"| Incremento | {r['inc']} |")
            w("")
    w("## 4. Trazabilidad: ventana → requerimientos")
    w("")
    w("Toda ventana especificada en la Fase II está cubierta por al menos un requerimiento (lo comprueba el generador).")
    w("")
    w("| Ventana | Requerimientos |")
    w("|---|---|")
    for v in sorted(esp):
        rs = [r["id"] for r in R if v in r["fuentes"]]
        w(f"| {v[2:]} | {', '.join(rs)} |")
    w("")
    w("## 5. Vacíos que estos requerimientos heredan, declarados")
    w("")
    w("- ~~**V-11**~~ — **cerrado por ADR-035** (2026-10-26): eliminar una experiencia (RF-02-07) o salir de una (RF-04-12) borra en cascada lo que depende de ella.")
    w("- **QA-013 / QA-014** — los errores de extracción del catálogo se corrigieron (encargo 02); el censo de formato cerrado está hecho y falta validarlo por muestreo (encargo 05, ADR-042) (RF-06-01, RF-06-02).")
    w("- **V-10** — una excepción de contraste, diferida (RNF-03).")
    w("- **RNF-13** — el tiempo límite de la generación no tiene número todavía; se mide.")
    w("- **RNF-06** — la autorización del acudiente: condición no satisfecha que impide usar el sistema con estudiantes reales.")
    w("")
    return "\n".join(L)


def main():
    esp, fallos = verificar()
    if fallos:
        print("FALLO — requerimientos")
        for f in fallos:
            print("  " + f)
        sys.exit(1)
    open(os.path.join(F3, "11-analisis-requerimientos.md"), "w", encoding="utf-8").write(generar(esp))
    nf = sum(1 for r in R if r["tipo"] == F)
    print(f"OK — {len(R)} requerimientos ({nf} funcionales, {len(R)-nf} no funcionales); "
          f"las {len(esp)} ventanas cubiertas; todas las ADR citadas existen.")
    print("generado: 11-analisis-requerimientos.md")


if __name__ == "__main__":
    main()
