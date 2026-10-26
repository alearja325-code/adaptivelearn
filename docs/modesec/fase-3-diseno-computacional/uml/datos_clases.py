"""Fuente unica del diagrama de clases (13-diagrama-clases.md).

MODESEC: los diagramas de clases *"resultan de la composicion de los casos
de uso"* y deben incluir *"atributos y metodos de cada una de las clases"*.
De ahi salen las dos mitades de cada clase:

  * ATRIBUTOS: los del modelo relacional (`../modelo-relacional/datos_mr.py`)
    menos las columnas que solo existen para una llave foranea -- en un
    modelo de objetos esas columnas son las asociaciones, no atributos.
    `_verificar_uml.py` lo comprueba columna por columna.
  * METODOS: cada uno dice de que casos de uso sale. El verificador
    comprueba que esos casos de uso existan, y que todo metodo que un
    diagrama de secuencia invoca este declarado aqui.

Los nombres de atributo son los mismos del MER y del MR, a proposito: un
mismo dato no cambia de nombre entre documentos.
"""


def clase(nombre, entidad, tabla, atributos, metodos, estereotipo=None,
          abstracta=False, desc=""):
    return dict(nombre=nombre, entidad=entidad, tabla=tabla,
                atributos=list(atributos), metodos=list(metodos),
                estereotipo=estereotipo, abstracta=abstracta, desc=desc)


def m(firma, cus, estatico=False):
    return dict(firma=firma, cus=list(cus), estatico=estatico)


# ============================================================ DOMINIO
CLASES = [
    clase("Credencial", "CREDENCIAL", "credencial",
          [("id_credencial", "int"), ("correo", "string"), ("proveedor", "Proveedor"),
           ("password_hash", "string [0..1]"), ("proveedor_id", "string [0..1]"),
           ("email_verificado", "bool"), ("codigo_verificacion", "string [0..1]"),
           ("codigo_expira_en", "Fecha [0..1]"), ("codigo_ultimo_envio", "Fecha [0..1]"),
           ("intentos_codigo", "int"), ("intentos_login", "int"),
           ("bloqueado_hasta", "Fecha [0..1]"), ("creado_en", "Fecha"),
           ("actualizado_en", "Fecha")],
          [m("verificarContrasena(texto: string): bool", ["CU-06"]),
           m("emitirCodigo(ahora: Fecha): string", ["CU-01", "CU-03", "CU-07"]),
           m("puedeReenviar(ahora: Fecha): bool", ["CU-03"]),
           m("verificarCodigo(codigo: string, ahora: Fecha): bool", ["CU-03"]),
           m("cambiarContrasena(nueva: string)", ["CU-07"]),
           m("registrarFallo(ahora: Fecha)", ["CU-03", "CU-06"]),
           m("estaBloqueada(ahora: Fecha): bool", ["CU-06"]),
           m("tieneRol(): bool", ["CU-02", "CU-06"]),
           m("asignarRol(usuario: Usuario)", ["CU-05"])],
          desc="La cuenta de acceso. Existe desde que la persona se registra, antes de tener rol."),
    clase("Usuario", None, None,
          [("nombres", "string"), ("apellidos", "string"), ("avatar_url", "string [0..1]")],
          [m("nombreCompleto(): string", ["CU-09", "CU-28"]),
           m("actualizarPerfil(nombres: string, apellidos: string, foto: Imagen)", ["CU-05", "CU-09"])],
          abstracta=True,
          desc="Lo que Docente y Estudiante tienen igual. Abstracta: no hay usuarios sin rol, "
               "y en la base no tiene tabla (cada subclase tiene la suya: RF-01-06)."),
    clase("Docente", "DOCENTE", "docente",
          [("id_docente", "int")],
          [m("experiencias(): Experiencia [*]", ["CU-10"])],
          desc="Hereda de Usuario."),
    clase("Estudiante", "ESTUDIANTE", "estudiante",
          [("id_estudiante", "int")],
          [m("inscripciones(): Inscripcion [*]", ["CU-21"])],
          desc="Hereda de Usuario. Solo los datos mínimos (ADR-029)."),
    clase("DBA", "DBA", "dba",
          [("codigo_dba", "string"), ("area", "string"), ("grado", "string"),
           ("enunciado", "string"), ("ejemplo", "string [0..1]")],
          [m("evidenciasAdmitidas(): Evidencia [*]", ["CU-16", "CU-31"])],
          desc="Dato del MEN, de solo lectura."),
    clase("Evidencia", "EVIDENCIA", "evidencia",
          [("numero_evidencia", "int"), ("enunciado", "string")],
          [m("admiteFormatoCerrado(): bool", ["CU-16", "CU-31"])],
          desc="Parte de su DBA (composición): sin él no tiene identidad."),
    clase("EvidenciaDictamen", "EVIDENCIA_DICTAMEN", "evidencia_dictamen",
          [("aplica_formato_cerrado", "bool"), ("formato", "Formato [0..1]"),
           ("justificacion", "string [0..1]"),
           ("fecha_dictamen", "Fecha")],
          [],
          desc="Nuestro juicio sobre una evidencia del MEN, separado del dato oficial (H-6)."),
    clase("Experiencia", "EXPERIENCIA", "experiencia",
          [("id_experiencia", "int"), ("nombre", "string"), ("estado", "EstadoExperiencia"),
           ("fecha_creacion", "Fecha"), ("fecha_publicacion", "Fecha [0..1]"),
           ("codigo_invitacion", "string"), ("servicio_ia", "ServicioIA"),
           ("modelo_ia", "string")],
          [m("faltantesParaPublicar(): int [*]", ["CU-13", "CU-17"]),
           m("puedePublicarse(): bool", ["CU-13"]),
           m("publicar(ahora: Fecha)", ["CU-13"]),
           m("bancoEditable(): bool", ["CU-17", "CU-18", "CU-19", "CU-20"]),
           m("codigoVisible(): string [0..1]", ["CU-14"])]),
    clase("ExperienciaEvidencia", "EXPERIENCIA_EVIDENCIA", "experiencia_evidencia",
          [],
          [m("itemsActivos(): Item [*]", ["CU-17", "CU-23"]),
           m("faltantes(): int", ["CU-13", "CU-17"])],
          desc="Una evidencia que esta experiencia diagnostica. Sin atributos propios: su "
               "identidad es el par (experiencia, evidencia)."),
    clase("Item", "ITEM", "item",
          [("id_item", "int"), ("enunciado", "string"), ("formato", "Formato"),
           ("origen", "Origen"), ("excluido", "bool")],
          [m("esValido(): bool", ["CU-16", "CU-18", "CU-20"]),
           m("editar(enunciado: string, opciones: Opcion [*])", ["CU-18"]),
           m("descartar()", ["CU-19"]),
           m("reincluir()", ["CU-19"]),
           m("evaluar(seleccion: RespuestaOpcion [*]): bool", ["CU-24"])]),
    clase("Opcion", "OPCION", "opcion",
          [("id_opcion", "int"), ("texto", "string"), ("orden", "int [0..1]"),
           ("es_correcta", "bool [0..1]"), ("grupo", "Grupo [0..1]"),
           ("hipotesis_error", "string [0..1]")],
          []),
    clase("Inscripcion", "INSCRIPCION", "inscripcion",
          [("id_inscripcion", "int"), ("fecha_union", "Fecha")],
          [m("progreso(): Progreso", ["CU-21", "CU-23"]),
           m("evidenciaEnCurso(): ExperienciaEvidencia [0..1]", ["CU-23"]),
           m("presentacionPendiente(): Presentacion [0..1]", ["CU-23"]),
           m("presentarSiguiente(ahora: Fecha): Presentacion", ["CU-23"]),
           m("resultados(): Resultado [*]", ["CU-27", "CU-28", "CU-29", "CU-30"])]),
    clase("Presentacion", "PRESENTACION", "presentacion",
          [("orden_presentacion", "int"), ("fecha_presentacion", "Fecha")],
          [m("responder(seleccion: RespuestaOpcion [*], certeza: int): Respuesta", ["CU-24"])],
          desc="Haber MOSTRADO un ítem, distinto de haberlo respondido (H-2, H-3)."),
    clase("Respuesta", "RESPUESTA", "respuesta",
          [("id_respuesta", "int"), ("certeza", "int"), ("fecha_respuesta", "Fecha"),
           ("correcta", "bool")],
          [m("esSenalFuerte(): bool", ["CU-25"])]),
    clase("RespuestaOpcion", "RESPUESTA_OPCION", "respuesta_opcion",
          [("valor_dado", "int [0..1]")],
          [],
          estereotipo="clase asociación",
          desc="Clase asociación de «selecciona»: qué opción eligió y, en emparejar u ordenar, "
               "qué valor le dio."),
    clase("Resultado", "RESULTADO", "resultado",
          [("estado", "EstadoResultado"), ("fecha_calculo", "Fecha")],
          [],
          desc="Fotografía del momento en que se concluyó (RNF-11). Lo crea "
               "ServicioDiagnostico con lo que decide ReglaAdaptativa."),
    clase("Reporte", "REPORTE", None,
          [("/estado_general", "EstadoGeneral [*]"),
           ("/estado_por_evidencia", "Clasificacion [*]")],
          [m("estadoGeneral(i: Inscripcion): EstadoGeneral", ["CU-30"]),
           m("distribucion(e: ExperienciaEvidencia): int [*]", ["CU-27"]),
           m("clasificar(e: ExperienciaEvidencia): Clasificacion", ["CU-27"]),
           m("porEstado(): Estudiante [*]", ["CU-28"])],
          estereotipo="calculada",
          desc="No persiste: se calcula sobre Resultado cada vez que se abre (ADR-022)."),
]

# ------------------------------------------------------------- enumeraciones
# Las 7 primeras deben coincidir valor por valor con los ENUM del MR; las 3
# ultimas son de valores calculados, que no se guardan.
ENUMERACIONES = [
    ("Proveedor", ["correo", "google", "microsoft"], ("credencial", "proveedor")),
    ("EstadoExperiencia", ["Borrador", "Publicada"], ("experiencia", "estado")),
    ("Formato", ["single_choice", "matching", "ordering"], ("item", "formato")),
    ("Origen", ["ia", "editado_docente", "creado_docente"], ("item", "origen")),
    ("ServicioIA", ["gemini", "deepseek"], ("experiencia", "servicio_ia")),
    ("Grupo", ["izquierda", "derecha"], ("opcion", "grupo")),
    ("EstadoResultado", ["muestra", "no_muestra", "no_concluyente"], ("resultado", "estado")),
    ("EstadoGeneral", ["muestra", "no_muestra", "no_concluyente", "sin_concluir"], None),
    ("Clasificacion", ["datos_insuficientes", "brecha_aparente", "sin_brecha_aparente"], None),
    ("Progreso", ["no_iniciada", "en_curso", "completada"], None),
]

# ------------------------------------------------------------- asociaciones
# (todo, parte_o_otro, nombre_MER, mult_a, mult_b, tipo)
#   tipo: "composicion" (rombo lleno en A) | "asociacion" | "derivada"
# El nombre es el de la relacion del MER: el verificador exige que esten
# todas y ninguna mas.
ASOCIACIONES = [
    ("Credencial", "Docente", "accede como", "1", "0..1", "asociacion"),
    ("Credencial", "Estudiante", "accede como", "1", "0..1", "asociacion"),
    ("DBA", "Evidencia", "comprende", "1", "1..*", "composicion"),
    ("Evidencia", "EvidenciaDictamen", "se dictamina", "1", "0..1", "composicion"),
    ("Docente", "Experiencia", "crea", "1", "0..*", "asociacion"),
    ("Experiencia", "DBA", "se ancla a", "0..*", "1", "asociacion"),
    ("Experiencia", "ExperienciaEvidencia", "incluye", "1", "1..*", "composicion"),
    ("Evidencia", "ExperienciaEvidencia", "sobre", "1", "0..*", "asociacion"),
    ("ExperienciaEvidencia", "Item", "genera", "1", "1..*", "composicion"),
    ("Item", "Opcion", "ofrece", "1", "2..*", "composicion"),
    ("Estudiante", "Inscripcion", "realiza", "1", "0..*", "asociacion"),
    ("Inscripcion", "Experiencia", "pertenece a", "0..*", "1", "asociacion"),
    ("Inscripcion", "Presentacion", "atiende", "1", "0..*", "composicion"),
    ("Item", "Presentacion", "se presenta", "1", "0..*", "asociacion"),
    ("Presentacion", "Respuesta", "registra", "1", "0..1", "composicion"),
    ("Respuesta", "Opcion", "selecciona", "0..*", "1..*", "asociacion"),
    ("Inscripcion", "Resultado", "arroja", "1", "0..*", "composicion"),
    ("ExperienciaEvidencia", "Resultado", "mide", "1", "0..*", "asociacion"),
    ("Resultado", "Reporte", "se agrega en", "0..*", "1", "derivada"),
    ("Reporte", "Experiencia", "resume", "0..1", "1", "derivada"),
]
GENERALIZACIONES = [("Docente", "Usuario"), ("Estudiante", "Usuario")]
CLASE_ASOCIACION = ("RespuestaOpcion", "selecciona")

# ========================================================== SERVICIOS
# Las clases de control: lo que recibe la peticion de la IGU y coordina a
# las del dominio. Son las que aparecen en los diagramas de secuencia.
SERVICIOS = [
    clase("ServicioAcceso", None, None, [],
          [m("registrar(correo: string, contrasena: string)", ["CU-01"]),
           m("verificarCorreo(correo: string, codigo: string)", ["CU-03"]),
           m("reenviarCodigo(correo: string)", ["CU-03"]),
           m("entrarConProveedor(token: string): Sesion", ["CU-02"]),
           m("elegirRol(rol: string, perfil: Perfil): Sesion", ["CU-04", "CU-05"]),
           m("iniciarSesion(correo: string, contrasena: string): Sesion", ["CU-06"]),
           m("solicitarRecuperacion(correo: string)", ["CU-07"]),
           m("restablecerContrasena(correo: string, codigo: string, nueva: string)", ["CU-07"]),
           m("cerrarSesion()", ["CU-08"]),
           m("perfil(): Perfil", ["CU-09"]),
           m("editarPerfil(perfil: Perfil)", ["CU-09"])],
          estereotipo="servicio"),
    clase("ServicioExperiencias", None, None, [],
          [m("listar(docente: Docente): Experiencia [*]", ["CU-10"]),
           m("crear(docente: Docente, codigo_dba: string, nombre: string): Experiencia", ["CU-11"]),
           m("consultar(id: int): Experiencia", ["CU-12", "CU-13", "CU-15"]),
           m("publicar(id: int)", ["CU-13"]),
           m("codigoInvitacion(id: int): string", ["CU-14"]),
           m("eliminar(id: int)", ["CU-15"])],
          estereotipo="servicio"),
    clase("Catalogo", None, None, [],
          [m("dbas(area: string, grado: string, texto: string): DBA [*]", ["CU-31"]),
           m("dba(codigo_dba: string): DBA", ["CU-11", "CU-31"])],
          estereotipo="servicio"),
    clase("GeneradorBanco", None, None,
          [("principal", "ServicioGeneracion"), ("respaldo", "ServicioGeneracion")],
          [m("generar(dba: DBA, evidencias: Evidencia [*]): Item [*]", ["CU-16"])],
          estereotipo="servicio"),
    clase("ServicioGeneracion", None, None, [],
          [m("generarItems(dba: DBA, evidencia: Evidencia, cantidad: int): Item [*]", ["CU-16"])],
          estereotipo="interfaz"),
    clase("ClienteGemini", None, None, [("modelo", "string")],
          [m("generarItems(dba: DBA, evidencia: Evidencia, cantidad: int): Item [*]", ["CU-16"])]),
    clase("ClienteDeepSeek", None, None, [("modelo", "string")],
          [m("generarItems(dba: DBA, evidencia: Evidencia, cantidad: int): Item [*]", ["CU-16"])]),
    clase("ServicioBanco", None, None, [],
          [m("banco(id_experiencia: int): ExperienciaEvidencia [*]", ["CU-17"]),
           m("editarItem(id_item: int, enunciado: string, opciones: Opcion [*])", ["CU-18"]),
           m("descartar(id_item: int)", ["CU-19"]),
           m("reincluir(id_item: int)", ["CU-19"]),
           m("agregarItem(id_experiencia: int, numero_evidencia: int): Item", ["CU-20"])],
          estereotipo="servicio"),
    clase("ServicioDiagnostico", None, None, [],
          [m("misInscripciones(estudiante: Estudiante): Inscripcion [*]", ["CU-21"]),
           m("unirse(estudiante: Estudiante, codigo: string): Inscripcion", ["CU-22"]),
           m("consultar(id_inscripcion: int): Inscripcion", ["CU-23", "CU-26"]),
           m("siguientePregunta(id_inscripcion: int): Presentacion [0..1]", ["CU-23"]),
           m("responder(id_inscripcion: int, id_item: int, seleccion: RespuestaOpcion [*], certeza: int)",
             ["CU-24"]),
           m("salir(id_inscripcion: int)", ["CU-26"])],
          estereotipo="servicio"),
    clase("ReglaAdaptativa", None, None,
          [("MINIMO", "int = 4"), ("TOPE", "int = 6"), ("CERTEZA_FUERTE", "int = 3")],
          [m("concluir(respuestas: Respuesta [*]): EstadoResultado [0..1]", ["CU-25"])],
          estereotipo="servicio"),
    clase("ServicioReporte", None, None, [],
          [m("reporte(id_experiencia: int): Reporte", ["CU-27"]),
           m("estudiantesPorEstado(id_experiencia: int): Estudiante [*]", ["CU-28"]),
           m("historial(id_inscripcion: int): Presentacion [*]", ["CU-29"])],
          estereotipo="servicio"),
    clase("ServicioCorreo", None, None, [],
          [m("enviarCodigo(correo: string, codigo: string)", ["CU-03", "CU-07"])],
          estereotipo="interfaz"),
    clase("ProveedorIdentidad", None, None, [],
          [m("validar(token: string): Perfil", ["CU-02"])],
          estereotipo="interfaz"),
]
# (cliente, proveedor, tipo): "usa" (dependencia) | "realiza" (implementa)
DEPENDENCIAS = [
    ("ServicioAcceso", "ServicioCorreo", "usa"),
    ("ServicioAcceso", "ProveedorIdentidad", "usa"),
    ("ServicioExperiencias", "Catalogo", "usa"),
    ("ServicioExperiencias", "GeneradorBanco", "usa"),
    ("GeneradorBanco", "ServicioGeneracion", "usa"),
    ("ClienteGemini", "ServicioGeneracion", "realiza"),
    ("ClienteDeepSeek", "ServicioGeneracion", "realiza"),
    ("ServicioDiagnostico", "ReglaAdaptativa", "usa"),
]

POR_NOMBRE = {c["nombre"]: c for c in CLASES + SERVICIOS}
