"""Fuente unica de los diagramas de secuencia (15-diagramas-secuencia.md).

MODESEC: *"El responsable o actor es quien inicia el ciclo interactuando
inicialmente con la interfaz de usuario (IGU); en seguida se inician todos
los objetos que intervienen en el funcionamiento del aplicativo."* Por eso
cada diagrama empieza en un actor, pasa por la IGU (la ventana de la Fase
II que corresponde) y de ahi a los objetos de servicio y de dominio.

Un mensaje escrito como llamada -- `nombre(args)` -- es una operacion del
receptor: `_verificar_uml.py` comprueba que esa operacion este declarada en
su clase (`datos_clases.py`). Un mensaje en prosa es una accion que no es
una operacion de clase (lo que hace la persona, lo que muestra la IGU, o
una consulta a la base de datos).

Pasos:
  ("m", de, a, texto)        mensaje sincrono
  ("r", de, a, texto)        respuesta (punteada)
  ("c", de, a, texto)        «create»: crea el objeto `a`, cuya cabecera
                              aparece a esa altura
  ("s", de, texto)           mensaje a si mismo
  ("ini", op, guarda)        abre un fragmento: alt | opt | loop
  ("sino", guarda)           otra rama del alt
  ("fin",)                   cierra el fragmento
  ("nota", de, texto)        nota a la derecha de la linea de vida de `de`
"""

# participante: (id, rotulo, clase o None, tipo)  tipo: actor | igu | objeto | externo | bd
SECUENCIAS = [
    dict(
        id="sec-1", archivo="secuencia-1-registro.svg",
        titulo="Registrarse con correo y contraseña",
        cus=["CU-01", "CU-03", "CU-04", "CU-05"],
        ventanas=["014", "015", "016", "017"],
        participantes=[("visitante", "Visitante", None, "actor"),
                       ("igu", "Ventanas 014 a 017", None, "igu"),
                       ("acc", ":ServicioAcceso", "ServicioAcceso", "objeto"),
                       ("cred", "c : Credencial", "Credencial", "objeto"),
                       ("cod", "k : CodigoVerificacion", "CodigoVerificacion", "objeto"),
                       ("doc", "d : Docente", "Docente", "objeto"),
                       ("correo", ":ServicioCorreo", "ServicioCorreo", "externo")],
        pasos=[
            ("m", "visitante", "igu", "escribe correo y contraseña; «Crear cuenta»"),
            ("s", "igu", "habilita el botón: 8+ caracteres, mayúscula, minúscula y número"),
            ("m", "igu", "acc", "registrar(correo, contrasena)"),
            ("s", "acc", "busca una credencial con ese correo"),
            ("ini", "alt", "el correo ya está registrado"),
            ("r", "acc", "igu", "aviso: ya existe, o con qué método entrar (RF-01-04)"),
            ("r", "igu", "visitante", "muestra el aviso; no se crea nada"),
            ("sino", "el correo está libre"),
            ("c", "acc", "cred", "«create» (correo, hash de la contraseña)"),
            ("m", "acc", "cred", "emitirCodigo(verificar_correo, ahora)"),
            ("c", "cred", "cod", "«create» (propósito, hash del código)"),
            ("r", "cred", "acc", "código de 6 dígitos: se guarda solo su hash (ADR-039)"),
            ("m", "acc", "correo", "enviarCodigo(correo, codigo)"),
            ("r", "acc", "igu", "código enviado"),
            ("fin",),
            ("r", "igu", "visitante", "«Verifica tu correo» (ventana 015)"),
            ("m", "visitante", "igu", "escribe el código"),
            ("m", "igu", "acc", "verificarCorreo(correo, codigo)"),
            ("m", "acc", "cod", "verificar(codigo, ahora)"),
            ("r", "cod", "acc", "true: no venció (10 min desde creado_en) y quedan intentos"),
            ("s", "acc", "estado_verificacion = verificado; borra el código"),
            ("r", "igu", "visitante", "«Completa tu perfil» (ventana 016)"),
            ("m", "visitante", "igu", "nombres, apellidos y foto opcional"),
            ("nota", "igu", "El perfil queda en la IGU: la cuenta todavía no existe (RF-01-05)."),
            ("r", "igu", "visitante", "«Elige tu rol» (ventana 017): no se podrá cambiar"),
            ("m", "visitante", "igu", "elige Docente y confirma"),
            ("m", "igu", "acc", "elegirRol(rol, perfil)"),
            ("c", "acc", "doc", "«create» (nombres, apellidos, avatar_url)"),
            ("m", "acc", "cred", "asignarRol(usuario)"),
            ("nota", "acc", "Las dos escrituras van en una sola transacción."),
            ("r", "acc", "igu", "sesión del docente"),
            ("r", "igu", "visitante", "Dashboard del docente"),
        ]),
    dict(
        id="sec-2", archivo="secuencia-2-iniciar-sesion.svg",
        titulo="Iniciar sesión",
        cus=["CU-06"], ventanas=["014"],
        participantes=[("usuario", "Usuario", None, "actor"),
                       ("igu", "Ventana 014", None, "igu"),
                       ("acc", ":ServicioAcceso", "ServicioAcceso", "objeto"),
                       ("cred", "c : Credencial", "Credencial", "objeto")],
        pasos=[
            ("m", "usuario", "igu", "escribe correo y contraseña"),
            ("m", "igu", "acc", "iniciarSesion(correo, contrasena)"),
            ("s", "acc", "busca la credencial del correo"),
            ("ini", "alt", "no existe"),
            ("r", "acc", "igu", "error genérico (RF-01-07)"),
            ("sino", "es de Google o Microsoft"),
            ("r", "acc", "igu", "aviso: con qué método entrar (RF-01-04)"),
            ("sino", "es de correo y contraseña"),
            ("m", "acc", "cred", "estaBloqueada(ahora)"),
            ("m", "acc", "cred", "verificarContrasena(texto)"),
            ("ini", "alt", "bloqueada, o contraseña incorrecta"),
            ("m", "acc", "cred", "registrarFallo(ahora)"),
            ("r", "acc", "igu", "error genérico: no dice qué falló"),
            ("sino", "contraseña correcta"),
            ("m", "acc", "cred", "tieneRol()"),
            ("ini", "alt", "todavía sin rol: registro sin terminar"),
            ("r", "acc", "igu", "continúa en completar perfil (CU-04)"),
            ("sino", "con rol"),
            ("r", "acc", "igu", "sesión del rol"),
            ("fin",),
            ("fin",),
            ("fin",),
            ("r", "igu", "usuario", "el mensaje, o el Dashboard de su rol"),
        ]),
    dict(
        id="sec-3", archivo="secuencia-3-crear-experiencia.svg",
        titulo="Crear una experiencia, con la generación del banco por IA",
        cus=["CU-11", "CU-31", "CU-16"], ventanas=["002", "003", "004", "024"],
        participantes=[("docente", "Docente", None, "actor"),
                       ("igu", "Ventanas 002 a 004, 024", None, "igu"),
                       ("exps", ":ServicioExperiencias", "ServicioExperiencias", "objeto"),
                       ("exp", "e : Experiencia", "Experiencia", "objeto"),
                       ("cat", ":Catalogo", "Catalogo", "objeto"),
                       ("dba", "dba : DBA", "DBA", "objeto"),
                       ("gen", ":GeneradorBanco", "GeneradorBanco", "objeto"),
                       ("pri", "principal : ServicioGeneracion", "ServicioGeneracion", "externo"),
                       ("res", "respaldo : ServicioGeneracion", "ServicioGeneracion", "externo")],
        pasos=[
            ("m", "docente", "igu", "Paso 1: elige el área"),
            ("m", "igu", "cat", "dbas(codigo_area, numero_grado, texto)"),
            ("r", "cat", "igu", "los DBA, con evidencias y ejemplo"),
            ("m", "docente", "igu", "Paso 2: elige el DBA · Paso 3: confirma el nombre"),
            ("r", "igu", "docente", "«Generando las preguntas...» (ventana 024)"),
            ("m", "igu", "exps", "crear(docente, codigo_dba, nombre)"),
            ("m", "exps", "cat", "dba(codigo_dba)"),
            ("m", "exps", "dba", "evidenciasAdmitidas()"),
            ("r", "dba", "exps", "las que el dictamen admite, en orden oficial"),
            ("m", "exps", "gen", "generar(dba, evidencias)"),
            ("ini", "loop", "por cada evidencia admitida"),
            ("m", "gen", "pri", "generarItems(dba, evidencia, cantidad)"),
            ("fin",),
            ("ini", "opt", "el principal falló, se pasó del tiempo o dio un ítem inválido"),
            ("ini", "loop", "por cada evidencia admitida: el banco entero, de nuevo"),
            ("m", "gen", "res", "generarItems(dba, evidencia, cantidad)"),
            ("fin",),
            ("fin",),
            ("r", "gen", "exps", "12 ítems por evidencia de UN solo servicio, o error"),
            ("ini", "alt", "hay banco completo"),
            ("c", "exps", "exp", "«create» en Borrador, con su código de invitación"),
            ("nota", "exps", "Una sola transacción: la experiencia —con el servicio y el modelo que generaron su banco—, sus evidencias incluidas, ítems y opciones (ADR-027)."),
            ("r", "exps", "igu", "la experiencia"),
            ("r", "igu", "docente", "entra a la experiencia (Resumen)"),
            ("sino", "fallaron los dos servicios"),
            ("r", "exps", "igu", "error: no se guardó nada"),
            ("r", "igu", "docente", "Paso 3 con el error; nombre y DBA intactos"),
            ("fin",),
        ]),
    dict(
        id="sec-4", archivo="secuencia-4-publicar.svg",
        titulo="Publicar una experiencia",
        cus=["CU-13"], ventanas=["011", "012"],
        participantes=[("docente", "Docente", None, "actor"),
                       ("igu", "Ventanas 011 y 012", None, "igu"),
                       ("exps", ":ServicioExperiencias", "ServicioExperiencias", "objeto"),
                       ("exp", "e : Experiencia", "Experiencia", "objeto"),
                       ("ee", "ee : ExperienciaEvidencia", "ExperienciaEvidencia", "objeto")],
        pasos=[
            ("m", "docente", "igu", "abre la experiencia"),
            ("m", "igu", "exps", "consultar(id)"),
            ("m", "exps", "exp", "puedePublicarse()"),
            ("ini", "loop", "por cada evidencia incluida"),
            ("m", "exp", "ee", "faltantes()"),
            ("fin",),
            ("r", "exp", "exps", "true solo si a ninguna le faltan ítems"),
            ("r", "exps", "igu", "la experiencia, y si se puede publicar"),
            ("ini", "alt", "a alguna evidencia le faltan ítems activos"),
            ("r", "igu", "docente", "«Publicar» deshabilitado, con cuántos faltan"),
            ("sino", "todas tienen al menos 6 activos"),
            ("m", "docente", "igu", "«Publicar»"),
            ("r", "igu", "docente", "confirmación: no se deshace; el banco se congela"),
            ("m", "docente", "igu", "confirma"),
            ("m", "igu", "exps", "publicar(id)"),
            ("m", "exps", "exp", "puedePublicarse()"),
            ("m", "exps", "exp", "publicar(ahora)"),
            ("nota", "exp", "estado = Publicada · fecha_publicacion = ahora (RI-16)"),
            ("r", "exps", "igu", "publicada"),
            ("r", "igu", "docente", "estado Publicada; el código ya se puede ver"),
            ("fin",),
        ]),
    dict(
        id="sec-5", archivo="secuencia-5-unirse.svg",
        titulo="Unirse a una experiencia con el código",
        cus=["CU-22"], ventanas=["005", "020"],
        participantes=[("est", "Estudiante", None, "actor"),
                       ("igu", "Ventanas 005 y 020", None, "igu"),
                       ("diag", ":ServicioDiagnostico", "ServicioDiagnostico", "objeto"),
                       ("ins", "i : Inscripcion", "Inscripcion", "objeto")],
        pasos=[
            ("m", "est", "igu", "escribe el código"),
            ("m", "igu", "diag", "unirse(estudiante, codigo)"),
            ("s", "diag", "busca la experiencia por código, sin distinguir mayúsculas"),
            ("ini", "alt", "no existe, o está en Borrador"),
            ("r", "diag", "igu", "error"),
            ("r", "igu", "est", "mensaje de error; lo escrito se conserva"),
            ("sino", "el estudiante ya estaba inscrito"),
            ("r", "diag", "igu", "su inscripción de antes (RI-1)"),
            ("sino", "Publicada, y no estaba inscrito"),
            ("c", "diag", "ins", "«create» (fecha_union = ahora)"),
            ("r", "diag", "igu", "la inscripción nueva"),
            ("fin",),
            ("r", "igu", "est", "pantalla de inicio del diagnóstico (ventana 020)"),
        ]),
    dict(
        id="sec-6", archivo="secuencia-6-diagnostico.svg",
        titulo="Tomar el diagnóstico: presentar, responder y aplicar la regla adaptativa",
        cus=["CU-23", "CU-24", "CU-25"], ventanas=["020", "021", "022", "023"],
        participantes=[("est", "Estudiante", None, "actor"),
                       ("igu", "Ventanas 020 a 023", None, "igu"),
                       ("diag", ":ServicioDiagnostico", "ServicioDiagnostico", "objeto"),
                       ("resu", "r : Resultado", "Resultado", "objeto"),
                       ("ins", "i : Inscripcion", "Inscripcion", "objeto"),
                       ("pre", "p : Presentacion", "Presentacion", "objeto"),
                       ("item", "it : Item", "Item", "objeto"),
                       ("regla", ":ReglaAdaptativa", "ReglaAdaptativa", "objeto")],
        pasos=[
            ("m", "est", "igu", "«Comenzar» o «Continuar diagnóstico»"),
            ("ini", "loop", "hasta concluir todas las evidencias"),
            ("m", "igu", "diag", "siguientePregunta(id_inscripcion)"),
            ("m", "diag", "ins", "presentacionPendiente()"),
            ("ini", "alt", "quedó una pregunta mostrada y sin responder"),
            ("r", "ins", "diag", "esa misma presentación (ADR-031)"),
            ("sino", "no quedó ninguna"),
            ("m", "diag", "ins", "presentarSiguiente(ahora)"),
            ("s", "ins", "evidenciaEnCurso()"),
            ("c", "ins", "pre", "«create»: ítem activo al azar, no visto; orden y fecha"),
            ("r", "ins", "diag", "la presentación"),
            ("fin",),
            ("r", "diag", "igu", "la pregunta"),
            ("r", "igu", "est", "la pregunta, sin contador (ventana 021)"),
            ("m", "est", "igu", "elige su respuesta, después su certeza de 0 a 5"),
            ("m", "igu", "diag", "responder(id_inscripcion, id_item, seleccion, certeza)"),
            ("m", "diag", "pre", "responder(seleccion, certeza)"),
            ("m", "pre", "item", "evaluar(seleccion)"),
            ("r", "item", "pre", "correcta o no"),
            ("r", "pre", "diag", "respuesta guardada (RF-04-06)"),
            ("m", "diag", "regla", "concluir(respuestas)"),
            ("r", "regla", "diag", "muestra, no_muestra, no_concluyente o nada"),
            ("ini", "opt", "la regla concluyó la evidencia"),
            ("c", "diag", "resu", "«create» (estado, fecha_calculo = ahora)"),
            ("fin",),
            ("r", "diag", "igu", "ok: nunca dice si acertó (RF-04-08)"),
            ("fin",),
            ("r", "igu", "est", "cierre: el docente puede ver los resultados (ventana 023)"),
        ]),
    dict(
        id="sec-7", archivo="secuencia-7-reporte.svg",
        titulo="Consultar el reporte de la experiencia",
        cus=["CU-27", "CU-30"], ventanas=["010"],
        participantes=[("docente", "Docente", None, "actor"),
                       ("igu", "Ventana 010", None, "igu"),
                       ("srep", ":ServicioReporte", "ServicioReporte", "objeto"),
                       ("rep", "rep : Reporte", "Reporte", "objeto"),
                       ("ins", "i : Inscripcion", "Inscripcion", "objeto")],
        pasos=[
            ("m", "docente", "igu", "abre el Reporte (pestaña Materiales)"),
            ("m", "igu", "srep", "reporte(id_experiencia)"),
            ("c", "srep", "rep", "«create» para la experiencia"),
            ("ini", "loop", "por cada estudiante inscrito"),
            ("m", "rep", "ins", "resultados()"),
            ("s", "rep", "estadoGeneral(i)"),
            ("fin",),
            ("ini", "loop", "por cada evidencia incluida"),
            ("s", "rep", "distribucion(e)"),
            ("s", "rep", "clasificar(e)"),
            ("fin",),
            ("nota", "rep", "Datos insuficientes si no concluyente + sin concluir ≥ 40 % de N; si no, Brecha aparente si hay un no muestra; si no, Sin brecha aparente."),
            ("r", "rep", "srep", "estados generales y clasificación"),
            ("r", "srep", "igu", "el reporte"),
            ("r", "igu", "docente", "el reporte, sin lenguaje de certeza (RNF-04)"),
        ]),
    dict(
        id="sec-8", archivo="secuencia-8-eliminar.svg",
        titulo="Eliminar una experiencia (borrado en cascada)",
        cus=["CU-15"], ventanas=["006", "025", "024"],
        participantes=[("docente", "Docente", None, "actor"),
                       ("igu", "Ventanas 006, 025 y 024", None, "igu"),
                       ("exps", ":ServicioExperiencias", "ServicioExperiencias", "objeto"),
                       ("bd", "Base de datos (MySQL)", None, "bd")],
        pasos=[
            ("m", "docente", "igu", "«Eliminar experiencia»"),
            ("m", "igu", "exps", "consultar(id)"),
            ("r", "exps", "igu", "cuántos inscritos y cuántas respuestas"),
            ("r", "igu", "docente", "confirmación con lo que se pierde (ventana 025)"),
            ("ini", "alt", "confirma"),
            ("m", "igu", "exps", "eliminar(id)"),
            ("m", "exps", "bd", "DELETE de la experiencia"),
            ("nota", "bd", "ON DELETE CASCADE: evidencias incluidas, ítems, opciones, inscripciones, presentaciones, respuestas y resultados. Docentes, estudiantes y currículo no se tocan (V-11)."),
            ("r", "bd", "exps", "hecho"),
            ("r", "exps", "igu", "eliminada"),
            ("r", "igu", "docente", "vuelve a su lista"),
            ("sino", "cancela"),
            ("r", "igu", "docente", "nada cambia"),
            ("fin",),
        ]),
]

# Lo que cada diagrama deja ver, en una frase o dos (va en el documento 15).
EXPLICACION = {
    "sec-1": "Por qué la cuenta con rol se crea al final: entre «Crear cuenta» y «Elegir rol» "
             "solo existe la credencial —hace falta para guardar el código de verificación— y el "
             "perfil viaja en la IGU hasta que se elige el rol (RF-01-05). Docente y credencial se "
             "escriben juntos. El «alt» del principio es RF-01-04: con un correo ya registrado no "
             "se crea nada.",
    "sec-2": "Los caminos de un inicio de sesión que no termina en el Dashboard: el correo no "
             "existe (mensaje genérico), es de una cuenta de Google o Microsoft (aviso del método), "
             "o la contraseña falla o la cuenta está bloqueada (se cuenta el intento). Una "
             "credencial sin rol retoma el registro: es la decisión del alterno 3a de CU-06.",
    "sec-3": "La creación «todo o nada» de ADR-027. El banco se pide al servicio principal; si "
             "falla, se pasa del tiempo o entrega un ítem inválido, el de respaldo lo genera "
             "completo de nuevo, así que un banco nunca mezcla servicios (RF-03-02). Solo si hay "
             "banco se crea la experiencia, en una sola transacción con todo lo que depende de "
             "ella; si fallan los dos, no se guardó nada.",
    "sec-4": "Publicar se comprueba dos veces: al mostrar el botón —para deshabilitarlo y decir "
             "cuántos ítems faltan— y otra vez al confirmar, porque entre una cosa y otra el "
             "docente pudo descartar ítems. Estado y fecha de publicación cambian juntos, que es lo "
             "que exige RI-16.",
    "sec-5": "Las tres respuestas posibles a un código: error (no existe, o la experiencia está "
             "en Borrador: RI-7), la inscripción de antes (RI-1: unirse dos veces no duplica), o "
             "una inscripción nueva.",
    "sec-6": "El centro del diagnóstico. Cada vuelta presenta una pregunta y registra su "
             "respuesta. Lo primero es preguntar si quedó una presentación sin responder: si la "
             "hay, se repite esa (ADR-031) y no se crea otra. La regla adaptativa decide después "
             "de cada respuesta y, cuando concluye, el resultado se guarda como fotografía "
             "(RNF-11). Nada de lo que vuelve a la IGU dice si el estudiante acertó.",
    "sec-7": "El reporte no se guarda: se arma cada vez con los resultados de cada inscrito "
             "(ADR-022). El estado general de cada estudiante y la clasificación de cada evidencia "
             "salen de RF-05-01 y RF-05-02, con umbrales que fija el sistema.",
    "sec-8": "Cómo se cierra el vacío V-11: el servicio solo borra la experiencia; las llaves "
             "foráneas con ON DELETE CASCADE del modelo relacional borran lo que depende de ella. "
             "Por eso la confirmación puede decir exactamente qué se pierde, y por eso las cuentas "
             "y el currículo no se tocan (RESTRICT).",
}
