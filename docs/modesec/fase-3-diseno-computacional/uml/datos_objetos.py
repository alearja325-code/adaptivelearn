"""Fuente unica del diagrama de objetos (14-diagrama-objetos.md).

MODESEC: un diagrama de objetos *"representa un conjunto de objetos y sus
relaciones en un momento concreto"*. El momento elegido es el que mas
reglas pone a prueba a la vez:

  El martes 4 de noviembre de 2026 a las 09:06, Luis esta respondiendo la
  experiencia que Ana publico el dia anterior. Ya concluyo la evidencia 1
  (Muestra, en la 4.a respuesta) y acaba de ver la primera pregunta de la
  evidencia 2 -- y cerro la pagina sin responderla.

Se dibuja en DOS vistas del mismo momento, como el MER: (1) la experiencia
publicada, con su banco; (2) el diagnostico de Luis. Un objeto que aparece
en las dos se dibuja completo en la primera y como costura en la segunda.

Los VALORES de texto (nombres, correos, modelo de IA, codigo) son
ilustrativos; lo que no es ilustrativo es la estructura y que cada valor
cumpla las reglas: `_verificar_uml.py` comprueba que cada atributo exista
en su clase, que cada enlace sea una asociacion del diagrama de clases, y
que el resultado de la evidencia 1 sea el que da la regla de RF-04-07
aplicada a las respuestas que el diagrama muestra.
"""

# id: (clase, [(atributo, valor)])
OBJETOS = {
    # ------------------------------------------------ vista 1: la experiencia
    "ana": ("Docente", [("id_docente", "1"), ("nombres", '"Ana"'), ("apellidos", '"Pérez"')]),
    "c1": ("Credencial", [("correo", '"ana@colegio.edu.co"'), ("proveedor", "correo"),
                          ("password_hash", '"$argon2id$…"'), ("estado_verificacion", "verificado")]),
    # catalogo (ADR-036): el area, el grado y el documento del DBA
    "mat": ("Area", [("codigo_area", '"MAT"'), ("nombre", '"Matemáticas"')]),
    "g8": ("Grado", [("numero", "8"), ("nombre", '"Octavo"'), ("nivel", "basica_secundaria")]),
    "doc": ("DocumentoOficial", [("version", '"V.2"'), ("anio", "2016"), ("paginas", "88")]),
    "dba": ("DBA", [("codigo_dba", '"MAT-08-01"')]),
    "ev1": ("Evidencia", [("numero_evidencia", "1")]),
    "ev2": ("Evidencia", [("numero_evidencia", "2")]),
    "d1": ("EvidenciaDictamen", [("aplica_formato_cerrado", "true"), ("formato", "single_choice")]),
    "d2": ("EvidenciaDictamen", [("aplica_formato_cerrado", "true"), ("formato", "single_choice")]),
    "exp3": ("Experiencia", [("id_experiencia", "3"), ("estado", "Publicada"),
                             ("fecha_creacion", "2026-11-02 10:40"),
                             ("fecha_publicacion", "2026-11-03 08:15"),
                             ("codigo_invitacion", '"K7M2QX"'), ("servicio_ia", "gemini"),
                             ("modelo_ia", '"gemini-2.5-flash"')]),
    "ee1": ("ExperienciaEvidencia", []),
    "ee2": ("ExperienciaEvidencia", []),
    "it11": ("Item", [("id_item", "31"), ("formato", "single_choice"), ("origen", "ia"),
                      ("excluido", "false")]),
    "it12": ("Item", [("id_item", "32"), ("origen", "editado_docente"), ("excluido", "false")]),
    "it13": ("Item", [("id_item", "33"), ("origen", "ia"), ("excluido", "false")]),
    "it14": ("Item", [("id_item", "34"), ("origen", "ia"), ("excluido", "false")]),
    "it21": ("Item", [("id_item", "45"), ("origen", "creado_docente"),
                      ("excluido", "false")]),
    "op1": ("Opcion", [("id_opcion", "101"), ("es_correcta", "true")]),
    "op2": ("Opcion", [("id_opcion", "102"), ("es_correcta", "false")]),
    # ------------------------------------------------ vista 2: el diagnostico
    "luis": ("Estudiante", [("id_estudiante", "7"), ("nombres", '"Luis"'), ("apellidos", '"Gómez"')]),
    "c2": ("Credencial", [("correo", '"luis@gmail.com"'), ("proveedor", "google"),
                          ("password_hash", "null"), ("proveedor_id", '"g-1847…"'),
                          ("estado_verificacion", "verificado")]),
    "ins": ("Inscripcion", [("id_inscripcion", "15"), ("fecha_union", "2026-11-04 08:57")]),
    "p1": ("Presentacion", [("orden_presentacion", "1"), ("fecha_presentacion", "2026-11-04 09:00")]),
    "p2": ("Presentacion", [("orden_presentacion", "2"), ("fecha_presentacion", "2026-11-04 09:01")]),
    "p3": ("Presentacion", [("orden_presentacion", "3"), ("fecha_presentacion", "2026-11-04 09:03")]),
    "p4": ("Presentacion", [("orden_presentacion", "4"), ("fecha_presentacion", "2026-11-04 09:04")]),
    "p5": ("Presentacion", [("orden_presentacion", "5"), ("fecha_presentacion", "2026-11-04 09:06")]),
    "r1": ("Respuesta", [("certeza", "4"), ("correcta", "true"), ("fecha_respuesta", "2026-11-04 09:01")]),
    "r2": ("Respuesta", [("certeza", "5"), ("correcta", "true"), ("fecha_respuesta", "2026-11-04 09:02")]),
    "r3": ("Respuesta", [("certeza", "1"), ("correcta", "false"), ("fecha_respuesta", "2026-11-04 09:03")]),
    "r4": ("Respuesta", [("certeza", "3"), ("correcta", "true"), ("fecha_respuesta", "2026-11-04 09:05")]),
    "ro1": ("RespuestaOpcion", [("valor_dado", "null")]),
    "res1": ("Resultado", [("estado", "muestra"), ("fecha_calculo", "2026-11-04 09:05")]),
}

# (a, b, asociacion del diagrama de clases)
ENLACES = [
    ("c1", "ana", "accede como"), ("ana", "exp3", "crea"), ("exp3", "dba", "se ancla a"),
    ("dba", "mat", "pertenece a"), ("dba", "g8", "corresponde a"), ("dba", "doc", "se copia de"),
    ("doc", "mat", "es de"),
    ("dba", "ev1", "comprende"), ("dba", "ev2", "comprende"),
    ("ev1", "d1", "se dictamina"), ("ev2", "d2", "se dictamina"),
    ("exp3", "ee1", "incluye"), ("exp3", "ee2", "incluye"),
    ("ev1", "ee1", "sobre"), ("ev2", "ee2", "sobre"),
    ("ee1", "it11", "genera"), ("ee1", "it12", "genera"), ("ee1", "it13", "genera"),
    ("ee1", "it14", "genera"), ("ee2", "it21", "genera"),
    ("it11", "op1", "ofrece"), ("it11", "op2", "ofrece"),
    ("c2", "luis", "accede como"), ("luis", "ins", "realiza"), ("ins", "exp3", "pertenece a"),
    ("ins", "p1", "atiende"), ("ins", "p2", "atiende"), ("ins", "p3", "atiende"),
    ("ins", "p4", "atiende"), ("ins", "p5", "atiende"),
    ("it11", "p1", "se presenta"), ("it12", "p2", "se presenta"), ("it13", "p3", "se presenta"),
    ("it14", "p4", "se presenta"), ("it21", "p5", "se presenta"),
    ("p1", "r1", "registra"), ("p2", "r2", "registra"), ("p3", "r3", "registra"),
    ("p4", "r4", "registra"),
    ("r1", "op1", "selecciona"),
    ("ins", "res1", "arroja"), ("ee1", "res1", "mide"),
]
# el objeto de la clase asociacion y el enlace del que cuelga
OBJETO_ASOCIACION = ("ro1", ("r1", "op1"))

# Lo que el verificador recalcula: la evidencia 1 concluye con estas
# respuestas, en este orden, en el estado que dice res1.
EVIDENCIA_1 = ["r1", "r2", "r3", "r4"]

NOTAS = {
    "n_banco": "ee1 tiene 12 ítems (RF-03-01); aquí se ven los 4 que se le presentaron a "
               "Luis. Todos salieron de Gemini: el servicio es de exp3, no de cada ítem (RI-17), "
               "y it12, que editó Ana, lo sigue teniendo. Publicar exigió 6 activos por evidencia.",
    "n_it21": "it21 lo agregó Ana: no se le atribuye a la IA. Tiene el formato que fija d2 (RI-19).",
    "n_res1": "La regla concluyó en la 4.ª respuesta: 3 de 4 son señales fuertes de "
              "«muestra» (certezas 4, 5 y 3; la de certeza 1 es débil). RF-04-07.",
    "n_p5": "p5 no tiene respuesta: Luis cerró la página con la pregunta en pantalla. "
            "Al volver verá it21 otra vez, no una nueva (ADR-031).",
    "n_luis": "Su estado general es Sin concluir: la evidencia 2 no tiene resultado. "
              "Se calcula al abrir el reporte, no se guarda (ADR-022).",
    "n_dba": "El DBA MAT-08-01 es de Matemáticas, de 8° y se copió del documento de Matemáticas "
             "V.2: el mismo que su área (RI-20). Su código se arma con esa área y ese grado (RI-21).",
    "n_c2": "Entró con Google: sin contraseña guardada y con el correo ya verificado (RI-15).",
}
