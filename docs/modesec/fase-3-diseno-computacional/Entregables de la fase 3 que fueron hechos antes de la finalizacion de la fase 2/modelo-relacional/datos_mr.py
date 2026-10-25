"""Fuente unica del Modelo Relacional y del Diccionario de Datos.

MODESEC pide tres artefactos en Fase III: MER, MR y diccionario de datos
"para los metadatos (como tipos, tamanos, y otras cualidades de los
campos)". Este archivo es la fuente de los dos ultimos.

POR QUE EXISTE ESTE ARCHIVO
El 2026-09-19 se descubrio que `04-modelo-relacional.md` seguia basado en
la Tercera revision del MER (2026-08-26) cuando el MER ya iba en la
Quinta (2026-09-08): le faltaban las 3 entidades agregadas justamente
para responder a la revision del docente. Un documento escrito a mano se
desincroniza en silencio. Desde aqui se generan el diccionario, el DBML
y el SQL, y `_verificar_mr_mer.py` comprueba que esto no se aparte del
MER -- que a su vez sale de `diagrama/datos_mer.py`.

Base: `01-modelo-entidad-relacion.md`, QUINTA revision (2026-09-08).

MOTOR OBJETIVO: MariaDB 10.11 (el que pide el curso DSE-2). La columna
`sqlite` de cada campo es el equivalente para `mr_esquema.sql`, que
existe solo para la verificacion mecanica.
"""

# ---------------------------------------------------------------- campos
# Campo: (nombre, mariadb, sqlite, nulo, llave, dominio, defecto,
#         descripcion, fuente)
#   llave: "PK" | "PK,FK" | "FK" | "UNIQUE" | ""
#   nulo:  True = admite NULL

def c(nombre, mariadb, sqlite, nulo, llave, dominio, defecto, desc, fuente):
    return dict(nombre=nombre, mariadb=mariadb, sqlite=sqlite, nulo=nulo,
                llave=llave, dominio=dominio, defecto=defecto, desc=desc,
                fuente=fuente)


ID = "INT UNSIGNED"          # llave sustituta, AUTO_INCREMENT
CORREO = "VARCHAR(254)"      # maximo de una direccion de correo, RFC 5321
URL = "VARCHAR(500)"
NOMBRE_PERSONA = "VARCHAR(120)"
COD_DBA = "VARCHAR(40)"      # ej. "matematicas_8_dba_3"
FECHA = "DATETIME"

TABLAS = [
    # ---------------------------------------------------------------- 1
    dict(tabla="docente", entidad="Docente", clase="propia",
         desc="Quien crea y publica experiencias.",
         campos=[
             c("id_docente", f"{ID} AUTO_INCREMENT", "INTEGER", False, "PK",
               "", "", "Identificador interno.", "MER · Docente"),
             c("nombre", NOMBRE_PERSONA, "TEXT", False, "",
               "", "", "Nombre completo, como lo escribió al registrarse.",
               "19-spec-auth-completa-perfil.md"),
             c("correo", CORREO, "TEXT", False, "UNIQUE",
               "formato de correo", "", "Credencial de acceso.",
               "RI-3 · 17-spec-auth-login-registro.md"),
             c("avatar_url", URL, "TEXT", True, "",
               "", "NULL", "Foto de perfil; opcional, no bloquea el registro.",
               "19-spec-auth-completa-perfil.md §2.3"),
         ]),
    # ---------------------------------------------------------------- 2
    dict(tabla="estudiante", entidad="Estudiante", clase="propia",
         desc="Quien se une a una experiencia y responde el diagnóstico.",
         campos=[
             c("id_estudiante", f"{ID} AUTO_INCREMENT", "INTEGER", False, "PK",
               "", "", "Identificador interno.", "MER · Estudiante"),
             c("nombre", NOMBRE_PERSONA, "TEXT", False, "",
               "", "", "Nombre completo.", "19-spec-auth-completa-perfil.md"),
             c("correo", CORREO, "TEXT", False, "UNIQUE",
               "formato de correo", "", "Credencial de acceso.",
               "RI-3 · 17-spec-auth-login-registro.md"),
             c("avatar_url", URL, "TEXT", True, "",
               "", "NULL", "Foto de perfil; opcional.",
               "19-spec-auth-completa-perfil.md §2.3"),
         ]),
    # ---------------------------------------------------------------- 3
    dict(tabla="experiencia", entidad="Experiencia", clase="propia",
         desc="Un diagnóstico anclado a un único DBA, creado por un docente.",
         campos=[
             c("id_experiencia", f"{ID} AUTO_INCREMENT", "INTEGER", False, "PK",
               "", "", "Identificador interno.", "MER · Experiencia"),
             c("id_docente", ID, "INTEGER", False, "FK",
               "", "", "Docente autor. Participación total: no existe experiencia sin autor.",
               "MER · relación «crea»"),
             c("codigo_dba", COD_DBA, "TEXT", False, "FK",
               "", "", "DBA al que se ancla. Una experiencia, un solo DBA.",
               "ADR-003 · 06-spec-crear-experiencia-paso2.md"),
             c("nombre", "VARCHAR(160)", "TEXT", False, "",
               "", "", "Título que le pone el docente.",
               "07-spec-crear-experiencia-paso3.md"),
             c("estado", "ENUM('Borrador','Publicada')", "TEXT", False, "",
               "Borrador | Publicada", "'Borrador'",
               "Borrador = banco generado, sin revisar. Publicada = visible para estudiantes.",
               "ADR-005 · 04-spec-dashboard.md §2.3"),
             c("fecha_creacion", FECHA, "TEXT", False, "",
               "", "", "Cuándo se creó.", "04-spec-dashboard.md"),
             c("fecha_publicacion", FECHA, "TEXT", True, "",
               "", "NULL",
               "Cuándo pasó a Publicada. NULL mientras siga en Borrador.",
               "Quinta revisión del MER · 15-spec-modal-confirmar-publicar.md"),
             c("codigo_invitacion", "CHAR(6)", "TEXT", False, "UNIQUE",
               "6 caracteres alfanuméricos, sin 0 O 1 I L", "",
               "Código que el docente dicta para que los estudiantes se unan.",
               "RI-3 · 08-spec-unirse-codigo.md §2.3"),
         ]),
    # ---------------------------------------------------------------- 4
    dict(tabla="dba", entidad="DBA", clase="men",
         desc="Derecho Básico de Aprendizaje oficial del MEN. Dato externo, "
              "referenciado, no generado por este sistema.",
         campos=[
             c("codigo_dba", COD_DBA, "TEXT", False, "PK",
               "", "", "Llave natural del MEN. Única llave no sustituta del modelo.",
               "curriculo_men_normalizado.json"),
             c("area", "VARCHAR(40)", "TEXT", False, "",
               "", "", "Área curricular (Matemáticas, Lenguaje, ...).",
               "05-spec-crear-experiencia-paso1.md"),
             c("grado", "VARCHAR(4)", "TEXT", False, "",
               "1° a 11°", "", "Grado escolar. Sin Transición: no hay DBA de Transición en los datos reales.",
               "06-spec-crear-experiencia-paso2.md §2.3"),
             c("enunciado", "TEXT", "TEXT", False, "",
               "", "", "Texto oficial del DBA.", "curriculo_men_normalizado.json"),
             c("ejemplo", "TEXT", "TEXT", True, "",
               "", "NULL",
               "Ejemplo oficial. NULL real: el campo no existe todavía en la normalización (QA-011).",
               "ADR-011 · QA-011"),
         ]),
    # ---------------------------------------------------------------- 5
    dict(tabla="evidencia", entidad="Evidencia", clase="men debil",
         desc="Evidencia de aprendizaje de un DBA. Entidad débil: no tiene "
              "identidad fuera de su DBA. Dato del MEN, sin juicio nuestro.",
         campos=[
             c("codigo_dba", COD_DBA, "TEXT", False, "PK,FK",
               "", "", "DBA al que pertenece. Relación identificadora.",
               "MER · Evidencia"),
             c("numero_evidencia", "TINYINT UNSIGNED", "INTEGER", False, "PK",
               "> 0", "",
               "Posición dentro de la lista de evidencias de ese DBA. Llave parcial.",
               "curriculo_men_normalizado.json"),
             c("enunciado", "TEXT", "TEXT", False, "",
               "", "", "Texto oficial de la evidencia.",
               "curriculo_men_normalizado.json"),
         ]),
    # ---------------------------------------------------------------- 6
    dict(tabla="evidencia_dictamen", entidad="Evidencia_Dictamen",
         clase="propia debil",
         desc="Nuestro juicio sobre una evidencia del MEN: si admite formato "
              "cerrado. Separada de `evidencia` a propósito, para no mezclar "
              "contenido oficial con criterio propio (H-6).",
         campos=[
             c("codigo_dba", COD_DBA, "TEXT", False, "PK,FK",
               "", "", "Evidencia dictaminada (parte 1).", "H-6 · Quinta revisión"),
             c("numero_evidencia", "TINYINT UNSIGNED", "INTEGER", False, "PK,FK",
               "", "", "Evidencia dictaminada (parte 2).", "H-6 · Quinta revisión"),
             c("aplica_formato_cerrado", "BOOLEAN", "INTEGER", False, "",
               "true | false", "",
               "Si esta evidencia se puede diagnosticar con pregunta cerrada.",
               "ADR-006 · pendiente del censo QA-014"),
             c("justificacion", "TEXT", "TEXT", True, "",
               "", "NULL", "Por qué se dictaminó así.", "H-6 · Quinta revisión"),
             c("fecha_dictamen", FECHA, "TEXT", False, "",
               "", "",
               "Cuándo se dictaminó. Obligatoria porque el dictamen puede cambiar al cerrar QA-014.",
               "H-6 · Quinta revisión"),
         ]),
    # ---------------------------------------------------------------- 7
    dict(tabla="experiencia_evidencia", entidad="Experiencia_Evidencia",
         clase="asociativa",
         desc="Qué evidencias del DBA anclado diagnostica realmente esta "
              "experiencia. Existe para que Ítem y Resultado cuelguen de un "
              "solo camino al currículo; elimina las reglas RI-1 y RI-2 de la "
              "versión anterior al volverlas estructura (H-4).",
         campos=[
             c("id_experiencia", ID, "INTEGER", False, "PK,FK",
               "", "", "Experiencia (parte 1 de la llave).", "H-4 · Quinta revisión"),
             c("codigo_dba", COD_DBA, "TEXT", False, "PK,FK",
               "", "", "Evidencia incluida (parte 2).", "H-4 · Quinta revisión"),
             c("numero_evidencia", "TINYINT UNSIGNED", "INTEGER", False, "PK,FK",
               "", "", "Evidencia incluida (parte 3).", "H-4 · Quinta revisión"),
             c("incluida", "BOOLEAN", "INTEGER", False, "",
               "true | false", "TRUE",
               "Si esta evidencia entra al diagnóstico de esta experiencia. "
               "Solo puede ser true si su dictamen lo permite (RI-5).",
               "RI-5 · Quinta revisión"),
         ]),
    # ---------------------------------------------------------------- 8
    dict(tabla="inscripcion", entidad="Inscripción", clase="asociativa",
         desc="Un estudiante unido a una experiencia. Llave propia (no "
              "compuesta) para que Presentación y Resultado no arrastren "
              "llave doble.",
         campos=[
             c("id_inscripcion", f"{ID} AUTO_INCREMENT", "INTEGER", False, "PK",
               "", "", "Identificador interno.", "MER · Inscripción"),
             c("id_estudiante", ID, "INTEGER", False, "FK",
               "", "", "Estudiante inscrito.", "MER · relación «realiza»"),
             c("id_experiencia", ID, "INTEGER", False, "FK",
               "", "", "Experiencia a la que se unió.", "MER · relación «pertenece a»"),
             c("fecha_union", FECHA, "TEXT", False, "",
               "", "", "Cuándo se unió con el código.", "08-spec-unirse-codigo.md"),
         ]),
    # ---------------------------------------------------------------- 9
    dict(tabla="item", entidad="Ítem", clase="propia",
         desc="Pregunta o ejercicio del banco de diagnóstico. Se genera al "
              "crear la experiencia (ADR-005); 12 por evidencia (ADR-016).",
         campos=[
             c("id_item", f"{ID} AUTO_INCREMENT", "INTEGER", False, "PK",
               "", "", "Identificador interno.", "MER · Ítem"),
             c("id_experiencia", ID, "INTEGER", False, "FK",
               "", "", "Parte 1 de la FK compuesta hacia experiencia_evidencia.",
               "H-4 · Quinta revisión"),
             c("codigo_dba", COD_DBA, "TEXT", False, "FK",
               "", "", "Parte 2 de esa misma FK compuesta.", "H-4 · Quinta revisión"),
             c("numero_evidencia", "TINYINT UNSIGNED", "INTEGER", False, "FK",
               "", "", "Parte 3 de esa misma FK compuesta.", "H-4 · Quinta revisión"),
             c("enunciado", "TEXT", "TEXT", False, "",
               "", "", "Texto de la pregunta.", "ADR-014"),
             c("formato", "ENUM('single_choice','matching','ordering')", "TEXT",
               False, "", "single_choice | matching | ordering", "'single_choice'",
               "Cómo se responde el ítem.", "ADR-006"),
             c("origen", "ENUM('ia','editado_docente')", "TEXT", False, "",
               "ia | editado_docente", "'ia'",
               "Distingue un ítem tal como lo generó la IA de uno que el docente intervino. "
               "Fase I §2 eleva esa distincion a valor del proyecto.",
               "H-5 · ADR-015 · Quinta revisión"),
             c("estado_revision", "VARCHAR(30)", "TEXT", False, "",
               "VOCABULARIO SIN DECIDIR (V-7)", "'sin_revisar'",
               "Si el docente ya revisó este ítem. ADR-005 exige la revisión "
               "previa. **El vocabulario exacto de estados sigue sin decidirse "
               "(V-7)** — el tipo queda VARCHAR y no ENUM justamente por eso.",
               "H-5 · ADR-005 · V-7 abierto"),
             c("excluido", "BOOLEAN", "INTEGER", False, "",
               "true | false", "FALSE",
               "Si es true el ítem no se muestra, pero sigue en el banco. Reversible.",
               "ADR-015"),
         ]),
    # --------------------------------------------------------------- 10
    dict(tabla="opcion", entidad="Opción", clase="propia",
         desc="Opción de respuesta de un ítem. Qué columnas aplican depende "
              "del formato del ítem (RI-4).",
         campos=[
             c("id_opcion", f"{ID} AUTO_INCREMENT", "INTEGER", False, "PK",
               "", "", "Identificador interno.", "MER · Opción"),
             c("id_item", ID, "INTEGER", False, "FK",
               "", "", "Ítem al que pertenece.", "MER · relación «ofrece»"),
             c("texto", "TEXT", "TEXT", False, "",
               "", "", "Texto de la opción.", "ADR-014"),
             c("orden", "TINYINT UNSIGNED", "INTEGER", True, "",
               "según el formato (RI-4)", "NULL",
               "En `ordering`: la posición correcta. En `matching`: número de pareja. "
               "NULL en `single_choice`.", "ADR-014 · RI-4"),
             c("es_correcta", "BOOLEAN", "INTEGER", True, "",
               "según el formato (RI-4)", "NULL",
               "Solo aplica a `single_choice`. NULL en los otros dos formatos.",
               "ADR-014 · RI-4"),
             c("grupo", "ENUM('izquierda','derecha')", "TEXT", True, "",
               "izquierda | derecha, solo en matching", "NULL",
               "Solo aplica a `matching`: de qué lado del emparejamiento está.",
               "ADR-014 · RI-4"),
             c("hipotesis_error", "TEXT", "TEXT", True, "",
               "", "NULL",
               "Por qué un estudiante podría elegir esta opción incorrecta. "
               "No se le muestra al estudiante ni se reporta (ADR-008).",
               "ADR-020"),
         ]),
    # --------------------------------------------------------------- 11
    dict(tabla="presentacion", entidad="Presentación", clase="propia debil",
         desc="El hecho de HABER MOSTRADO un ítem a un estudiante — distinto "
              "del hecho de haberlo respondido. Sin esta tabla, «se le mostró "
              "y no respondió» es indistinguible de «nunca se le mostró» (H-3), "
              "y la secuencia adaptativa de ADR-016 no se puede reconstruir (H-2).",
         campos=[
             c("id_inscripcion", ID, "INTEGER", False, "PK,FK",
               "", "", "A quién se le mostró (parte 1 de la llave).",
               "H-2/H-3 · Quinta revisión"),
             c("id_item", ID, "INTEGER", False, "PK,FK",
               "", "", "Qué ítem se mostró (parte 2 de la llave).",
               "H-2/H-3 · Quinta revisión"),
             c("orden_presentacion", "TINYINT UNSIGNED", "INTEGER", False, "",
               "> 0, único por inscripción y evidencia (RI-8)", "",
               "En qué lugar de la secuencia se mostró. Es el dato que permite "
               "reconstruir la secuencia adaptativa.",
               "RI-8 · ADR-016"),
             c("fecha_presentacion", FECHA, "TEXT", False, "",
               "", "", "Cuándo se mostró.", "H-2 · Quinta revisión"),
         ]),
    # --------------------------------------------------------------- 12
    dict(tabla="respuesta", entidad="Respuesta", clase="asociativa",
         desc="Lo que el estudiante respondió a un ítem que se le presentó, "
              "con su nivel de certeza. Cuelga de la Presentación, no de "
              "Inscripción e Ítem por separado.",
         campos=[
             c("id_respuesta", f"{ID} AUTO_INCREMENT", "INTEGER", False, "PK",
               "", "", "Identificador interno.", "MER · Respuesta"),
             c("id_inscripcion", ID, "INTEGER", False, "FK",
               "", "", "Parte 1 de la FK compuesta hacia presentación.",
               "H-3 · Quinta revisión"),
             c("id_item", ID, "INTEGER", False, "FK",
               "", "", "Parte 2 de esa misma FK compuesta.",
               "H-3 · Quinta revisión"),
             c("certeza", "TINYINT UNSIGNED", "INTEGER", False, "",
               "0 a 5 (CRI)", "",
               "Certainty of Response Index (Hasan et al. 1999). Es la senal de "
               "la que depende toda la regla adaptativa.", "ADR-008 punto 2"),
             c("fecha_respuesta", FECHA, "TEXT", False, "",
               "", "",
               "Cuándo se envió. Cierra V-1: sin esto la secuencia adaptativa no "
               "se puede ordenar ni auditar.", "H-2 · Quinta revisión · cierra V-1"),
             c("correcta", "BOOLEAN", "INTEGER", False, "",
               "true | false", "",
               "DERIVADO Y PERSISTIDO (ADR-021): se calcula comparando "
               "respuesta_opcion contra las opciones reales, y se escribe una "
               "sola vez, al registrar la respuesta. No se recalcula al leer.",
               "ADR-019 · ADR-021"),
         ]),
    # --------------------------------------------------------------- 13
    dict(tabla="respuesta_opcion", entidad="Respuesta_Opción",
         clase="asociativa",
         desc="Qué opción u opciones eligió el estudiante — no solo si "
              "acertó. Sin esta tabla, `matching` y `ordering` no son "
              "representables.",
         campos=[
             c("id_respuesta", ID, "INTEGER", False, "PK,FK",
               "", "", "Respuesta a la que pertenece (parte 1).", "ADR-019"),
             c("id_opcion", ID, "INTEGER", False, "PK,FK",
               "", "", "Opción elegida (parte 2).", "ADR-019"),
             c("valor_dado", "TINYINT UNSIGNED", "INTEGER", True, "",
               "según el formato del ítem", "NULL",
               "`single_choice`: NULL, la fila ya es la elección. `ordering`: la "
               "posición que le asignó. `matching`: el número de pareja.",
               "ADR-019"),
         ]),
    # --------------------------------------------------------------- 14
    dict(tabla="resultado", entidad="Resultado", clase="propia debil",
         desc="Lo que las respuestas de un estudiante permiten concluir sobre "
              "UNA evidencia DE ESTA experiencia. Fotografía persistida, no "
              "recalculada al vuelo.",
         campos=[
             c("id_inscripcion", ID, "INTEGER", False, "PK,FK",
               "", "", "De quién es el resultado (parte 1 de la llave).",
               "MER · relación «arroja»"),
             c("id_experiencia", ID, "INTEGER", False, "FK",
               "", "",
               "COLUMNA REDUNDANTE DELIBERADA, decidida en este MR porque el MER "
               "se la delegó explícitamente. Permite que las DOS reglas de "
               "coherencia sean estructurales en vez de triggers — ver la "
               "sección de FK del documento.",
               "MER · Resultado (delegación explícita al MR)"),
             c("codigo_dba", COD_DBA, "TEXT", False, "PK,FK",
               "", "", "Evidencia medida (parte 2 de la llave).", "H-4 · Quinta revisión"),
             c("numero_evidencia", "TINYINT UNSIGNED", "INTEGER", False, "PK,FK",
               "", "", "Evidencia medida (parte 3 de la llave).", "H-4 · Quinta revisión"),
             c("estado", "ENUM('muestra','no_muestra','no_concluyente')", "TEXT",
               False, "", "muestra | no_muestra | no_concluyente", "",
               "DERIVADO Y PERSISTIDO (ADR-021). Nunca una certeza; nunca un "
               "valor que se edite a mano.", "ADR-008 punto 4 · ADR-021"),
             c("fecha_calculo", FECHA, "TEXT", False, "",
               "", "",
               "Cuándo se calculó `estado`. Obligatoria: una fotografía sin fecha "
               "no es auditable. Cierra V-4.", "ADR-021 · cierra V-4"),
         ]),
]

# ------------------------------------------------------------------- FK
# (tabla, [columnas], tabla_destino, [columnas_destino], on_delete, razon)
FKS = [
    ("experiencia", ["id_docente"], "docente", ["id_docente"], "RESTRICT",
     "Raíz: ningún flujo del sistema borra un docente."),
    ("experiencia", ["codigo_dba"], "dba", ["codigo_dba"], "RESTRICT",
     "Raíz: dato del MEN, no se borra por razones de este sistema."),
    ("evidencia", ["codigo_dba"], "dba", ["codigo_dba"], "CASCADE",
     "Entidad débil: sin su DBA no tiene identidad."),
    ("evidencia_dictamen", ["codigo_dba", "numero_evidencia"],
     "evidencia", ["codigo_dba", "numero_evidencia"], "CASCADE",
     "Entidad débil: el dictamen no existe sin la evidencia dictaminada."),
    ("experiencia_evidencia", ["id_experiencia"], "experiencia",
     ["id_experiencia"], "CASCADE",
     "Composición: la inclusión no significa nada sin su experiencia."),
    ("experiencia_evidencia", ["codigo_dba", "numero_evidencia"],
     "evidencia", ["codigo_dba", "numero_evidencia"], "RESTRICT",
     "Hacia el currículo del MEN: no se borra una evidencia oficial."),
    ("inscripcion", ["id_estudiante"], "estudiante", ["id_estudiante"],
     "RESTRICT", "Raíz."),
    ("inscripcion", ["id_experiencia"], "experiencia", ["id_experiencia"],
     "CASCADE", "Sin la experiencia, la inscripción no tiene objeto."),
    ("item", ["id_experiencia", "codigo_dba", "numero_evidencia"],
     "experiencia_evidencia",
     ["id_experiencia", "codigo_dba", "numero_evidencia"], "CASCADE",
     "UNA sola FK compuesta, no dos sueltas: es lo que hace estructural la "
     "coherencia que antes exigía RI-1."),
    ("opcion", ["id_item"], "item", ["id_item"], "CASCADE",
     "Composición pura; protegida aguas arriba por el RESTRICT de presentación."),
    ("presentacion", ["id_inscripcion"], "inscripcion", ["id_inscripcion"],
     "CASCADE", "Sin la inscripción no hay a quién se le mostró."),
    ("presentacion", ["id_item"], "item", ["id_item"], "RESTRICT",
     "PROTECCIÓN REAL: mientras exista el registro de que un ítem se mostró, "
     "ese ítem no se puede borrar. Refuerza ADR-015 y RI-10 a nivel de esquema."),
    ("respuesta", ["id_inscripcion", "id_item"], "presentacion",
     ["id_inscripcion", "id_item"], "CASCADE",
     "UNA sola FK compuesta hacia el hecho de haberse presentado. Una respuesta "
     "sin presentación previa es imposible por estructura."),
    ("respuesta_opcion", ["id_respuesta"], "respuesta", ["id_respuesta"],
     "CASCADE", "Sin la respuesta, la selección no tiene sentido."),
    ("respuesta_opcion", ["id_opcion"], "opcion", ["id_opcion"], "RESTRICT",
     "Protege el historial de qué eligió el estudiante."),
    ("resultado", ["id_inscripcion", "id_experiencia"], "inscripcion",
     ["id_inscripcion", "id_experiencia"], "CASCADE",
     "FK compuesta contra un UNIQUE de inscripción: fuerza que la experiencia "
     "del resultado sea la de su inscripción. Estructural, sin trigger."),
    ("resultado", ["id_experiencia", "codigo_dba", "numero_evidencia"],
     "experiencia_evidencia",
     ["id_experiencia", "codigo_dba", "numero_evidencia"], "RESTRICT",
     "Fuerza que la evidencia medida sea una de las que ESA experiencia incluye. "
     "Junto con la FK anterior, elimina por estructura la vieja RI-2."),
]

# --------------------------------------------------------------- UNIQUE
UNICOS = [
    ("docente", ["correo"], "RI-3"),
    ("estudiante", ["correo"], "RI-3"),
    ("experiencia", ["codigo_invitacion"], "RI-3"),
    ("inscripcion", ["id_estudiante", "id_experiencia"], "RI-1"),
    ("inscripcion", ["id_inscripcion", "id_experiencia"],
     "destino de FK — habilita la comprobación estructural de resultado"),
    ("respuesta", ["id_inscripcion", "id_item"], "una presentación, una respuesta"),
]

# ---------------------------------------------------------------- CHECK
CHECKS = [
    ("evidencia", "numero_evidencia > 0", "posición dentro del DBA"),
    ("experiencia", "codigo_invitacion no usa 0 O 1 I L, 6 posiciones",
     "RI-3 · 08-spec-unirse-codigo.md §2.3"),
    ("respuesta", "certeza BETWEEN 0 AND 5", "ADR-008 punto 2 (CRI)"),
    ("presentacion", "orden_presentacion > 0", "RI-8"),
]


def campos_de(tabla):
    for t in TABLAS:
        if t["tabla"] == tabla:
            return t["campos"]
    raise KeyError(tabla)


def pk_de(tabla):
    return [f["nombre"] for f in campos_de(tabla) if f["llave"].startswith("PK")]


N_TABLAS = len(TABLAS)
N_CAMPOS = sum(len(t["campos"]) for t in TABLAS)
N_FKS = len(FKS)
