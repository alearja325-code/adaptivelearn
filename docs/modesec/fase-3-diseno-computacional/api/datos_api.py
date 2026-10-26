"""Fuente unica del catalogo de endpoints (20-catalogo-endpoints.md).

MODESEC no tiene una sub-etapa para la interfaz de programacion: la Fase III
termina en el diccionario de datos. Este catalogo es el puente hacia la
construccion: dice, para cada peticion que el frontend le hara al backend,
que caso de uso atiende, que operacion del diagrama de clases la resuelve,
que entidades toca y quien puede hacerla. No inventa nada: cada endpoint
sale de un caso de uso de `../uml/datos_casos_uso.py` y de una operacion de
servicio de `../uml/datos_clases.py`, y su CRUD es el de la matriz de
`../uml/datos_crud.py`.

`_verificar_api.py` comprueba esa coherencia. Lo que NO se escribe aqui a
mano, porque se calcula:
  * en que diagrama de secuencia aparece cada endpoint (de `datos_secuencias`);
  * que se borra en cascada con cada DELETE (de las llaves foraneas del MR).

Estado de cada endpoint frente al backend del incremento I1 (`backend/` del
repositorio, comprobado el 2026-10-26 contra su codigo: `auth.controller.ts`,
`user/user.controller.ts` y `example.controller.ts`):
  hecho     existe en I1 y hace lo que dice el diseno
  ajustar   existe en I1, pero el diseno le pide algo distinto (dice que)
  falta     no existe todavia
  opcional  el diseno no lo necesita; se puede hacer
"""


def ep(metodo, ruta, sub, cus, op, acceso, crud, estado, recibe, responde,
       reglas=(), nota=""):
    return dict(metodo=metodo, ruta=ruta, sub=sub, cus=list(cus), op=op,
                acceso=acceso, crud=dict(crud), estado=estado, recibe=recibe,
                responde=responde, reglas=list(reglas), nota=nota)


# Quien puede llamar a cada endpoint. Todo token es un JWT en la cabecera
# `Authorization: Bearer`; el tipo va dentro del token.
ACCESOS = {
    "publico": ("Público", "Sin token."),
    "registro": ("Token de registro",
                 "El que entrega el registro (CU-01), o la primera entrada con Google o Microsoft "
                 "(CU-02). Identifica una credencial que todavía no tiene rol: sirve para verificar "
                 "el correo y para elegir el rol; no abre ninguna pantalla del producto."),
    "recuperacion": ("Token de recuperación",
                     "El que entrega la verificación del código de recuperación. Solo sirve para "
                     "fijar la contraseña nueva; no abre sesión (I1 ya lo prueba: 401)."),
    "sesion": ("Sesión", "Docente o estudiante con sesión iniciada."),
    "docente": ("Docente", "Sesión con rol docente."),
    "docente_dueno": ("Docente dueño",
                      "Sesión del docente dueño de la experiencia; para un ítem o una inscripción, "
                      "el de la experiencia a la que pertenecen."),
    "estudiante": ("Estudiante", "Sesión con rol estudiante."),
    "estudiante_dueno": ("Estudiante dueño", "Sesión del estudiante dueño de la inscripción."),
}

# Que accesos admite el actor de un caso de uso (12-casos-de-uso.md, sección 1).
# El Servicio de IA, el Proveedor de identidad y el Servicio de correo son
# actores externos: nunca llaman al backend.
ACCESO_DE_ACTOR = {
    "Visitante": {"publico", "registro"},
    "Usuario": {"publico", "recuperacion", "sesion"},
    "Docente": {"docente", "docente_dueno"},
    "Estudiante": {"estudiante", "estudiante_dueno"},
}

ESTADOS = {"hecho": "Hecho en I1", "ajustar": "Por ajustar", "falta": "Falta",
           "opcional": "Opcional"}

# Los incrementos de `10-proceso-desarrollo.md` §1.1, en su orden.
INCREMENTOS = {"I1": "Acceso", "I2": "Experiencia y banco", "I3": "Diagnóstico",
               "I4": "Reporte y seguimiento"}

# Codigos de error comunes. Cada endpoint dice cuales usa y por que.
ERRORES = [
    ("400", "Los datos no cumplen una regla: formato, campo vacío, contraseña débil, ítem inválido."),
    ("401", "Sin token, token vencido o de otro tipo; o credenciales incorrectas, con un mensaje "
            "que no dice qué falló (RF-01-07)."),
    ("403", "El token es válido, pero de otro rol o de quien no es el dueño. Así lo hace I1 "
            "(«Modificar perfil ajeno → 403»)."),
    ("404", "No existe."),
    ("409", "El estado no lo permite: correo ya registrado, rol ya elegido, banco congelado, "
            "experiencia ya publicada, pregunta ya respondida."),
    ("429", "Demasiados intentos fallidos."),
    ("503", "Fallaron el servicio de IA principal y el de respaldo; no se guardó nada."),
]

SUB_PUBLICADA = ("409", "la experiencia está Publicada: el banco es de solo lectura (RF-03-08, ADR-026)")

# ===================================================================== I1
ENDPOINTS = [
    ep("POST", "/auth/register", "SUB-01", ["CU-01"], "ServicioAcceso.registrar", "publico",
       {"CREDENCIAL": "CR"}, "hecho",
       "`email`, `password` (nombres de campo de I1)",
       "201: token de registro. El código de 6 dígitos sale al correo; en desarrollo, I1 lo "
       "imprime en la terminal del servidor",
       [("400", "contraseña sin 8 caracteres, una mayúscula y un número (RF-01-01)"),
        ("409", "el correo ya tiene cuenta; si es de Google o Microsoft, el mensaje dice qué "
                "método usar y no vincula (RF-01-04, RI-3)")],
       nota="I1 acepta además `fullName`, que viene de la guía. En el diseño los nombres se "
            "piden en Completar perfil (CU-04) y se guardan al elegir el rol."),
    ep("POST", "/auth/verificar-correo", "SUB-01", ["CU-03"], "ServicioAcceso.verificarCorreo",
       "registro", {"CREDENCIAL": "RU"}, "hecho",
       "`codigo`; la credencial la identifica el token de registro",
       "200: correo verificado; sigue Completar perfil (CU-04)",
       [("400", "código incorrecto: se cuenta un intento fallido (CU-03 3a)"),
        ("400", "código vencido: hay que pedir otro (CU-03 3b)"),
        ("429", "demasiados intentos fallidos (`intentos_codigo`)")]),
    ep("POST", "/auth/reenviar-codigo", "SUB-01", ["CU-03"], "ServicioAcceso.reenviarCodigo",
       "publico", {"CREDENCIAL": "RU"}, "hecho",
       "`email`",
       "201 siempre, `{ ok: true }`, exista o no la cuenta. Solo si existe, es de correo y ya "
       "pasaron 30 s desde el último envío, genera un código nuevo que reemplaza al anterior "
       "(CU-03 1a)",
       [("400", "el correo no tiene formato de correo"),
        ("—", "pedirlo antes de 30 s responde igual y no reenvía: un 429 delataría que la "
              "cuenta existe (RNF-07)")],
       nota="Sirve a los dos flujos, registro y recuperación, como la ventana 015 (CU-03). Así "
            "lo hace I1."),
    ep("POST", "/auth/google", "SUB-01", ["CU-02"], "ServicioAcceso.entrarConProveedor", "publico",
       {"CREDENCIAL": "CR", "DOCENTE": "R", "ESTUDIANTE": "R"}, "falta",
       "`token` que entregó Google",
       "200: sesión, si la cuenta ya tiene rol. Si es nueva, crea la credencial con el correo "
       "ya verificado y responde token de registro con nombres, apellidos y foto para "
       "prellenar el perfil (CU-02 3a)",
       [("401", "Google rechaza el token, o la persona canceló (CU-02 2a)"),
        ("409", "el correo ya está registrado con otro método: dice cuál; no crea ni vincula "
                "(RF-01-04, CU-02 3b)")]),
    ep("POST", "/auth/microsoft", "SUB-01", ["CU-02"], "ServicioAcceso.entrarConProveedor",
       "publico", {"CREDENCIAL": "CR", "DOCENTE": "R", "ESTUDIANTE": "R"}, "falta",
       "`token` que entregó Microsoft",
       "Igual que `POST /auth/google`",
       [("401", "Microsoft rechaza el token, o la persona canceló (CU-02 2a)"),
        ("409", "el correo ya está registrado con otro método (RF-01-04)")],
       nota="Sin Apple: exige cuenta de desarrollador de pago (RF-01-02)."),
    ep("POST", "/auth/elegir-rol", "SUB-01", ["CU-04", "CU-05"], "ServicioAcceso.elegirRol",
       "registro", {"CREDENCIAL": "RU", "DOCENTE": "C", "ESTUDIANTE": "C"}, "ajustar",
       "`role` (docente o estudiante), `nombres`, `apellidos` y `foto` opcional, en "
       "multipart/form-data",
       "201: sesión del rol. En una sola operación crea el docente o el estudiante con su "
       "perfil y lo asocia a la credencial (CU-05 paso 3)",
       [("400", "nombres o apellidos vacíos; foto que no es JPG ni PNG, o de más de 5 MB "
                "(CU-04 2a)"),
        ("403", "el correo de la credencial no está verificado (precondición de CU-04)"),
        ("409", "la credencial ya tiene rol: el rol no se cambia (RF-01-06, RI-12). I1 ya lo "
                "prueba")],
       nota="En I1 recibe solo `role`, y el perfil se completa antes con `PATCH /users/:id`. "
            "En el diseño la cuenta nace con su perfil al elegir el rol: CU-04 dice que «estos "
            "datos se guardan al elegir el rol» (RF-01-05), y nombres, apellidos y foto viven "
            "en DOCENTE o ESTUDIANTE, que no existen antes del rol."),
    ep("POST", "/auth/login", "SUB-01", ["CU-06"], "ServicioAcceso.iniciarSesion", "publico",
       {"CREDENCIAL": "RU", "DOCENTE": "R", "ESTUDIANTE": "R"}, "hecho",
       "`email`, `password`",
       "201 (el de NestJS por defecto, como en I1): token de sesión y rol. Si la credencial "
       "todavía no tiene rol, token de registro para seguir en Completar perfil (CU-06 3a, "
       "decisión por confirmar)",
       [("401", "correo o contraseña incorrectos, sin decir cuál (RF-01-07); se cuenta un "
                "intento fallido (`intentos_login`)"),
        ("409", "la cuenta es de Google o Microsoft: dice qué método usar (RF-01-04, CU-06 2c)"),
        ("429", "entrada bloqueada por intentos fallidos (`bloqueado_hasta`)")]),
    ep("POST", "/auth/recuperar-contrasena", "SUB-01", ["CU-07"],
       "ServicioAcceso.solicitarRecuperacion", "publico", {"CREDENCIAL": "RU"}, "hecho",
       "`email`",
       "202 siempre, exista o no la cuenta; si existe, envía el código (RNF-07). I1 ya responde "
       "igual en los dos casos",
       [("400", "el correo no tiene formato de correo (CU-07 paso 2)"),
        ("—", "pedirlo otra vez antes de 30 s responde igual, 202, y no reenvía: un 429 "
              "delataría que la cuenta existe (RNF-07)")]),
    ep("POST", "/auth/recuperar-contrasena/verificar", "SUB-01", ["CU-07", "CU-03"],
       "ServicioAcceso.verificarCorreo", "publico", {"CREDENCIAL": "RU"}, "hecho",
       "`email`, `codigo`",
       "200: token de recuperación",
       [("400", "código incorrecto o vencido (CU-03 3a, 3b)"),
        ("429", "demasiados intentos fallidos")]),
    ep("POST", "/auth/nueva-contrasena", "SUB-01", ["CU-07"],
       "ServicioAcceso.restablecerContrasena", "recuperacion", {"CREDENCIAL": "RU"}, "hecho",
       "`password` nueva, con el token de recuperación",
       "204: contraseña cambiada; la pantalla lleva a iniciar sesión (CU-07 paso 5)",
       [("400", "la contraseña no cumple las reglas del registro (RF-01-01)"),
        ("401", "token de recuperación inválido o vencido; un token de sesión no sirve aquí")],
       nota="`restablecerContrasena(correo, codigo, nueva)` va partida en dos peticiones, "
            "verificar el código y fijar la contraseña, con el token de recuperación en medio. "
            "Así lo hace I1, y es compatible con el diseño."),
    ep("GET", "/auth/profile", "SUB-01", ["CU-09"], "ServicioAcceso.perfil", "sesion",
       {"CREDENCIAL": "R", "DOCENTE": "R", "ESTUDIANTE": "R"}, "hecho",
       "nada",
       "200: correo, rol, nombres, apellidos y foto: lo que muestra el bloque de perfil del "
       "menú lateral (CU-09 paso 1)",
       [("401", "sin token, o con uno de registro o de recuperación")]),
    ep("PATCH", "/users/:id", "SUB-01", ["CU-09"], "ServicioAcceso.editarPerfil", "sesion",
       {"DOCENTE": "RU", "ESTUDIANTE": "RU"}, "ajustar",
       "`nombres`, `apellidos` y `foto` opcional, en multipart/form-data",
       "200: el perfil guardado",
       [("400", "nombres o apellidos vacíos, o foto inválida: la foto no cambia (CU-09 3a)"),
        ("400", "intenta cambiar el correo o el rol, que no se editan (CU-09 paso 2)"),
        ("403", "el perfil no es el propio. I1 ya lo prueba")],
       nota="En I1 sirve para completar el perfil **antes** de elegir el rol. En el diseño eso "
            "pasa en `POST /auth/elegir-rol`, y esta ruta queda solo para Editar mi perfil "
            "(CU-09), sobre la fila de DOCENTE o ESTUDIANTE; además recibe la foto."),
    ep("POST", "/auth/cerrar-sesion", "SUB-01", ["CU-08"], "ServicioAcceso.cerrarSesion", "sesion",
       {}, "opcional",
       "nada",
       "204",
       nota="Con JWT basta con que el navegador borre el token: cerrar sesión no cambia nada "
            "guardado (CU-08). Hace falta solo si se quiere invalidar tokens en el servidor."),

    # ================================================================= I2
    ep("GET", "/catalogo/dbas", "SUB-06", ["CU-31"], "Catalogo.dbas", "docente",
       {"DBA": "R", "AREA": "R", "GRADO": "R"}, "falta",
       "`codigo_area` (`MAT`, `LEN`, `CN` o `CS`), `numero_grado` (1 a 11) y `q` (texto), "
       "en la consulta",
       "200: los DBA del área, cada uno con su código `ÁREA-GG-NN`, su grado (número y "
       "nombre) y su enunciado",
       [("400", "falta el área, o no es una de las 4 (CU-11 paso 1); o el grado no está "
                "entre 1 y 11")],
       nota="Las 4 áreas son fijas (CU-11 paso 1, ADR-033): la pantalla las tiene, con los "
            "mismos códigos de la tabla `area` (ADR-036), y no se piden al backend."),
    ep("GET", "/catalogo/dbas/:codigo", "SUB-06", ["CU-31", "CU-11"], "Catalogo.dba", "docente",
       {"DBA": "R", "AREA": "R", "GRADO": "R", "DOCUMENTO_OFICIAL": "R", "EVIDENCIA": "R",
        "EVIDENCIA_DICTAMEN": "R"}, "falta",
       "nada (`:codigo` es el código `ÁREA-GG-NN`, ej. `MAT-08-01`)",
       "200: enunciado oficial, ejemplo, área, grado, el documento oficial del que se copió "
       "(título y versión) y las evidencias en el orden oficial, cada una marcada si admite "
       "o no formato cerrado (RF-06-02). El enunciado prellena el nombre en el Paso 3",
       [("404", "no existe ese DBA")]),
    ep("GET", "/experiencias", "SUB-02", ["CU-10"], "ServicioExperiencias.listar", "docente",
       {"EXPERIENCIA": "R", "DBA": "R", "AREA": "R", "GRADO": "R", "INSCRIPCION": "R"}, "falta",
       "`estado` (borrador o publicada) y `q`, en la consulta",
       "200: solo las experiencias del docente, cada una con estado, nombre, área, grado y "
       "número de estudiantes (CU-10 paso 1)"),
    ep("POST", "/experiencias", "SUB-02", ["CU-11", "CU-16"], "ServicioExperiencias.crear",
       "docente",
       {"EXPERIENCIA": "C", "EXPERIENCIA_EVIDENCIA": "C", "ITEM": "C", "OPCION": "C",
        "DBA": "R", "EVIDENCIA": "R", "EVIDENCIA_DICTAMEN": "R"}, "falta",
       "`codigo_dba`, `nombre`",
       "201: la experiencia en Borrador, con 12 ítems por evidencia incluida, su código de "
       "invitación, y el servicio y el modelo de IA que generaron el banco",
       [("503", "fallaron el servicio principal y el de respaldo: no se guarda nada, y la "
                "pantalla conserva nombre y DBA para reintentar (RF-02-03, ADR-027, CU-11 5a)"),
        ("—", "si el principal falla o pasa del tiempo límite (RNF-13), se pide el banco "
              "entero al de respaldo; un banco no mezcla servicios (RF-03-02, RI-17)"),
        ("—", "solo entran las evidencias cuyo dictamen admite formato cerrado (RI-5), y cada "
              "ítem sale con el formato de ese dictamen (RI-19)"),
        ("404", "no existe el DBA")],
       nota="Puede tardar minutos: ver la generación asíncrona en «Adicionales que conviene agregar»."),
    ep("GET", "/experiencias/:id", "SUB-02", ["CU-12", "CU-13", "CU-15"],
       "ServicioExperiencias.consultar", "docente_dueno",
       {"EXPERIENCIA": "R", "DBA": "R", "AREA": "R", "GRADO": "R", "EVIDENCIA": "R",
        "EXPERIENCIA_EVIDENCIA": "R", "ITEM": "R", "INSCRIPCION": "R", "RESPUESTA": "R"}, "falta",
       "nada",
       "200: encabezado (nombre, estado, fecha, área, grado, número de inscritos), el DBA, "
       "cuántos ítems activos faltan por evidencia para publicar (CU-13 1a), y cuántos "
       "inscritos y respuestas se perderían al eliminarla (CU-15 paso 2)",
       [("403", "la experiencia no es del docente"),
        ("404", "no existe")]),
    ep("POST", "/experiencias/:id/publicar", "SUB-02", ["CU-13"], "ServicioExperiencias.publicar",
       "docente_dueno", {"EXPERIENCIA": "RU", "EXPERIENCIA_EVIDENCIA": "R", "ITEM": "R"}, "falta",
       "nada",
       "200: la experiencia Publicada, con su fecha de publicación; el banco queda congelado "
       "(RF-03-08)",
       [("409", "ya está Publicada: publicar no se deshace (ADR-026)"),
        ("409", "alguna evidencia tiene menos de 6 ítems activos; dice cuántos faltan (RF-02-05, "
                "RI-14)")]),
    ep("GET", "/experiencias/:id/codigo", "SUB-02", ["CU-14"],
       "ServicioExperiencias.codigoInvitacion", "docente_dueno", {"EXPERIENCIA": "R"}, "falta",
       "nada",
       "200: el código de 6 caracteres, sin 0/O ni 1/I/L (RI-3)",
       [("409", "la experiencia está en Borrador: el código existe, pero no se muestra "
                "(RF-02-06, CU-14 1a)")]),
    ep("DELETE", "/experiencias/:id", "SUB-02", ["CU-15"], "ServicioExperiencias.eliminar",
       "docente_dueno", {"EXPERIENCIA": "RD"}, "falta",
       "nada",
       "204",
       [("—", "irreversible; las cuentas de los estudiantes siguen existiendo (CU-15)")]),
    ep("GET", "/experiencias/:id/banco", "SUB-03", ["CU-17"], "ServicioBanco.banco",
       "docente_dueno",
       {"EXPERIENCIA": "R", "EXPERIENCIA_EVIDENCIA": "R", "ITEM": "R", "OPCION": "R"}, "falta",
       "`formato` y `q`, en la consulta",
       "200: las evidencias en el orden oficial del DBA, cada una con su formato, sus ítems "
       "—opciones y respuesta correcta— y cuántos activos le faltan para publicar (RF-03-04)",
       [("—", "con la experiencia Publicada responde igual, marcada de solo lectura "
              "(CU-17 4a)")]),
    ep("PATCH", "/items/:id", "SUB-03", ["CU-18"], "ServicioBanco.editarItem", "docente_dueno",
       {"ITEM": "RU", "OPCION": "CRUD"}, "falta",
       "`enunciado` y la lista completa de `opciones` (`texto`, `es_correcta`, `orden`, `grupo`)",
       "200: el ítem guardado; si venía de la IA, su origen pasa a `editado_docente` (RF-03-03)",
       [("400", "ítem inválido: algo vacío, menos opciones que el mínimo del formato, dos "
                "correctas en selección única, orden incompleto o repetido (CU-18 paso 3, RI-4)"),
        SUB_PUBLICADA]),
    ep("POST", "/items/:id/descartar", "SUB-03", ["CU-19"], "ServicioBanco.descartar",
       "docente_dueno", {"ITEM": "U"}, "falta",
       "nada",
       "204: el ítem queda excluido, sin borrarse y sin confirmación (RF-03-06)",
       [SUB_PUBLICADA]),
    ep("POST", "/items/:id/reincluir", "SUB-03", ["CU-19"], "ServicioBanco.reincluir",
       "docente_dueno", {"ITEM": "U"}, "falta",
       "nada",
       "204: el ítem vuelve a estar activo, con el mismo contenido",
       [SUB_PUBLICADA]),
    ep("POST", "/experiencias/:id/evidencias/:n/items", "SUB-03", ["CU-20"],
       "ServicioBanco.agregarItem", "docente_dueno",
       {"ITEM": "C", "OPCION": "C", "EVIDENCIA_DICTAMEN": "R"}, "falta",
       "`:n` es el número de la evidencia; el cuerpo, como en `PATCH /items/:id`",
       "201: ítem activo, de origen `creado_docente`, con el formato del dictamen de esa "
       "evidencia (RI-19)",
       [("400", "ítem inválido, con las reglas de CU-18"),
        ("404", "esa evidencia no está incluida en la experiencia (RI-5, RI-18)"),
        SUB_PUBLICADA],
       nota="Se llama al guardar, no al abrir el formulario: la pantalla arma el ítem vacío con "
            "el formato que ya trae el banco. Así «Cancelar» no deja nada (CU-20 3a)."),

    # ================================================================= I3
    ep("GET", "/inscripciones", "SUB-04", ["CU-21"], "ServicioDiagnostico.misInscripciones",
       "estudiante",
       {"INSCRIPCION": "R", "EXPERIENCIA": "R", "DOCENTE": "R", "PRESENTACION": "R",
        "RESULTADO": "R"}, "falta",
       "`progreso` (no_iniciada, en_curso o completada) y `q`, en la consulta",
       "200: las experiencias del estudiante, cada una con su progreso, área y nombre del "
       "docente (CU-21 paso 1)",
       [("—", "el progreso se calcula, no se guarda: `progreso` es un atributo calculado del "
              "MER")]),
    ep("POST", "/inscripciones", "SUB-04", ["CU-22"], "ServicioDiagnostico.unirse", "estudiante",
       {"EXPERIENCIA": "R", "INSCRIPCION": "CR"}, "falta",
       "`codigo`, sin distinguir mayúsculas",
       "201: la inscripción nueva; 200 con la que ya existía si el estudiante ya estaba "
       "inscrito, sin duplicarla (RI-1, CU-22 3a)",
       [("404", "no hay una experiencia Publicada con ese código: el mismo mensaje para un "
                "código que no existe y para uno en Borrador (CU-22 2a, RI-7)")]),
    ep("GET", "/inscripciones/:id", "SUB-04", ["CU-23", "CU-26"],
       "ServicioDiagnostico.consultar", "estudiante_dueno",
       {"INSCRIPCION": "R", "EXPERIENCIA_EVIDENCIA": "R", "PRESENTACION": "R", "RESULTADO": "R",
        "RESPUESTA": "R"}, "falta",
       "nada",
       "200: la experiencia y su progreso, que decide «Comenzar» o «Continuar» (CU-23 paso 1), "
       "y cuántas respuestas se perderían al salir (CU-26 paso 2)",
       [("403", "la inscripción no es del estudiante"),
        ("—", "no incluye resultados ni aciertos (RF-04-08, ADR-028)")]),
    ep("POST", "/inscripciones/:id/presentaciones", "SUB-04", ["CU-23"],
       "ServicioDiagnostico.siguientePregunta", "estudiante_dueno",
       {"INSCRIPCION": "R", "EXPERIENCIA_EVIDENCIA": "R", "ITEM": "R", "OPCION": "R",
        "PRESENTACION": "CR", "RESULTADO": "R"}, "falta",
       "nada",
       "201: el ítem presentado —enunciado, formato y opciones—. 200 con la misma pregunta si "
       "quedó una sin responder (ADR-031). 200 sin pregunta si ya concluyeron todas las "
       "evidencias, y la pantalla muestra el cierre (RF-04-11)",
       [("—", "POST y no GET: cada llamada puede crear una PRESENTACIÓN, con su orden y su "
              "fecha (RI-8)"),
        ("—", "la evidencia es la primera sin concluir en el orden oficial; el ítem, uno activo "
              "no visto, al azar (ADR-024, RI-9)"),
        ("—", "nunca envía `es_correcta` ni `hipotesis_error` de las opciones, ni el número de "
              "pregunta, ni cuántas faltan (RF-04-08)"),
        ("409", "la experiencia ya está completada (CU-23 1a)")]),
    ep("POST", "/inscripciones/:id/respuestas", "SUB-04", ["CU-24", "CU-25"],
       "ServicioDiagnostico.responder", "estudiante_dueno",
       {"PRESENTACION": "R", "ITEM": "R", "OPCION": "R", "RESPUESTA": "CR",
        "RESPUESTA_OPCION": "C", "RESULTADO": "C"}, "falta",
       "`id_item`, las `opciones` elegidas (con `valor_dado` al emparejar y al ordenar) y "
       "`certeza` de 0 a 5",
       "201, sin decir si acertó ni cómo va (RF-04-08)",
       [("400", "certeza fuera de 0 a 5; ninguna opción, o más de una en selección única (RI-6)"),
        ("400", "una opción de otro ítem: el motor también la rechaza (RI-6, ciclo C4)"),
        ("409", "el ítem no es la pregunta pendiente, o ya se respondió: una respuesta no se "
                "cambia (RNF-10)"),
        ("—", "aplica la regla adaptativa (CU-25: mínimo 4, tope 6, señal fuerte con certeza de "
              "3 a 5) y, si concluye, guarda el resultado de la evidencia como fotografía "
              "(RNF-11)")]),
    ep("DELETE", "/inscripciones/:id", "SUB-04", ["CU-26"], "ServicioDiagnostico.salir",
       "estudiante_dueno", {"INSCRIPCION": "D"}, "falta",
       "nada",
       "204",
       [("—", "para volver necesita el código otra vez, y la experiencia aparece «No iniciada» "
              "(CU-26)")]),

    # ================================================================= I4
    ep("GET", "/experiencias/:id/reporte", "SUB-05", ["CU-27", "CU-30"],
       "ServicioReporte.reporte", "docente_dueno",
       {"REPORTE": "R", "RESULTADO": "R", "INSCRIPCION": "R", "EXPERIENCIA_EVIDENCIA": "R"},
       "falta",
       "nada",
       "200: cuántos estudiantes hay en cada estado general y, por evidencia, la distribución "
       "de resultados y su clasificación (CU-27 paso 4)",
       [("—", "se calcula al abrirlo, no se guarda (ADR-022)"),
        ("—", "ningún texto afirma certeza (RNF-04)")]),
    ep("GET", "/experiencias/:id/estudiantes", "SUB-05", ["CU-28"],
       "ServicioReporte.estudiantesPorEstado", "docente_dueno",
       {"REPORTE": "R", "ESTUDIANTE": "R", "INSCRIPCION": "R", "RESULTADO": "R"}, "falta",
       "`estado` y `q` (nombre), en la consulta",
       "200: los estudiantes agrupados por estado general —No muestra, No concluyente, Sin "
       "concluir, Muestra—, en orden alfabético y con su resultado en cada evidencia (CU-28)",
       [("—", "sin el correo del estudiante (ADR-029, RNF-05)")]),
    ep("GET", "/inscripciones/:id/historial", "SUB-05", ["CU-29"], "ServicioReporte.historial",
       "docente_dueno",
       {"PRESENTACION": "R", "RESPUESTA": "R", "RESPUESTA_OPCION": "R", "ITEM": "R",
        "OPCION": "R", "RESULTADO": "R"}, "falta",
       "nada",
       "200: por evidencia y con su resultado, los ítems presentados en orden: qué respondió, "
       "si fue correcto y con qué certeza; las preguntas sin respuesta aparecen como tales "
       "(CU-29)",
       [("403", "solo el docente dueño de la experiencia de esa inscripción; el estudiante "
                "nunca (ADR-028)")]),
]

# Operaciones de clases «servicio» que no tienen ruta propia, y por que.
INTERNOS = {
    "GeneradorBanco.generar": "la llama `ServicioExperiencias.crear`: CU-11 incluye CU-16, y la "
                              "generación es parte de crear la experiencia (todo o nada, "
                              "ADR-027).",
    "ReglaAdaptativa.concluir": "la llama `ServicioDiagnostico.responder`: CU-24 incluye CU-25, y "
                                "la regla se aplica a cada respuesta.",
}

# En el backend I1 (`backend/src/`), pero no son del producto.
AJENOS_I1 = [
    ("POST /users", "Crear usuario"),
    ("GET /users", "Listar usuarios"),
    ("GET /users/:id", "Ver un usuario por su id"),
    ("GET /example/protected", "Ruta protegida de ejemplo"),
    ("GET /example/docente", "Ruta de ejemplo con rol docente"),
]

# Adicionales: no los pide ningun requerimiento, pero ayudan a construir,
# probar o presentar. (ruta, para que, efecto en el MER)
ADICIONALES = [
    ("`GET /docs`", "Documentación interactiva (Swagger/OpenAPI, `@nestjs/swagger`): el docente "
                    "puede probar cada endpoint desde el navegador, sin Insomnia.",
     "Ninguno."),
    ("`GET /health`", "Comprobar en la demostración que el servidor y la base responden.",
     "Ninguno."),
    ("`POST /auth/refresh`", "Renovar la sesión sin volver a pedir la contraseña.",
     "Si los tokens de renovación se guardan para poder revocarlos, es una tabla que el MER no "
     "tiene."),
    ("Generación asíncrona: `POST /experiencias` responde 202 y la espera consulta "
     "`GET /experiencias/generaciones/:id`",
     "Generar el banco puede tardar minutos (RNF-13), y una sola petición larga puede cortarse. "
     "La pantalla de espera (RNF-12) consulta hasta que termine. El «todo o nada» (ADR-027) no "
     "cambia: la experiencia se guarda solo al final.",
     "Si el estado de la generación se guarda en la base, es una tabla nueva, fuera del MER; en "
     "memoria, ninguno. Decidirlo al medir RNF-13 en I2."),
    ("Límite de peticiones por IP en login, códigos y recuperación (no es un endpoint: "
     "`@nestjs/throttler`)",
     "Complementa el bloqueo por credencial que ya tiene I1.",
     "Ninguno."),
]

# Lo que no se debe agregar: contradice una decision tomada. Cada entrada
# lleva un patron sobre "METODO RUTA" (y, si hace falta, los accesos a los que
# aplica) para que el verificador compruebe que ningun endpoint lo hace.
NO_AGREGAR = [
    dict(que="Regenerar el banco, o pedirle a la IA más ítems", fuente="ADR-026 (`10` §2.4)",
         patron=r"regenera|generar-mas|mas-items|/items/generar"),
    dict(que="Despublicar, o editar el banco de una experiencia publicada",
         fuente="ADR-026, RF-03-08 (`10` §2.4)", patron=r"despublica|/borrador$"),
    dict(que="Que el docente elija qué evidencias entran, o agregue evidencias propias",
         fuente="QA-010, QA-001, RI-5 (`10` §2.4)",
         patron=r"^(POST|PUT|PATCH|DELETE) /experiencias/:id/evidencias(/:n)?$"),
    dict(que="Mostrarle al estudiante sus resultados, su historial o el reporte",
         fuente="ADR-028, RF-04-08 (`10` §2.4)", patron=r"/(resultados|reporte|historial)",
         accesos={"estudiante", "estudiante_dueno"}),
    dict(que="Cambiar el rol", fuente="RF-01-06, RI-12",
         patron=r"cambiar-rol|^(PUT|PATCH|DELETE) /auth/elegir-rol|/rol$"),
    dict(que="Borrar un ítem: descartar no borra", fuente="CU-19, RF-03-06",
         patron=r"^DELETE /items"),
    dict(que="Modificar o borrar una presentación, una respuesta o un resultado",
         fuente="RNF-10, RNF-11, ADR-021",
         patron=r"^(PUT|PATCH|DELETE) .*(presentaciones|respuestas|resultados)"),
    dict(que="Administrar usuarios: listar, crear o borrar cuentas",
         fuente="no hay rol administrador (`10` §2.2)", patron=r"^(GET|POST|DELETE) /users"),
]
