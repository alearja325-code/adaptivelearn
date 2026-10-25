"""Fuente unica de contenido del MER -- Quinta revision (2026-09-08).

Una sola fuente para las 6 vistas, el mapa completo y las dos notaciones
(Chen y caja-tabla), para que ningun diagrama pueda desalinearse del
documento `01-modelo-entidad-relacion.md` ni de los otros diagramas.

Cada relacion declara en que VISTA vive. Regla dura, verificada por
codigo en _verificar_vistas.py: cada relacion aparece en exactamente una
vista; cada entidad, en al menos una.
"""

# ---------------------------------------------------------------- entidades
# (nombre, categoria, [(atributo, marca)])
#   categoria: propia | men | asociativa | debil | derivada
#   marca: "PK" | "PK,FK" | "FK" | "" (los PK se dibujan en elipse negra)

DOCENTE = ("DOCENTE", "propia", [
    ("id_docente", "PK"), ("nombre", ""), ("correo (U)", ""), ("avatar_url", ""),
])
ESTUDIANTE = ("ESTUDIANTE", "propia", [
    ("id_estudiante", "PK"), ("nombre", ""), ("correo (U)", ""), ("avatar_url", ""),
])
EXPERIENCIA = ("EXPERIENCIA", "propia", [
    ("id_experiencia", "PK"), ("id_docente", "FK"), ("codigo_dba", "FK"),
    ("nombre", ""), ("estado", ""), ("fecha_creacion", ""),
    ("fecha_publicacion", ""), ("codigo_invitacion (U)", ""),
])
DBA = ("DBA", "men", [
    ("codigo_dba", "PK"), ("area", ""), ("grado", ""), ("enunciado", ""),
    ("ejemplo", ""),
])
EVIDENCIA = ("EVIDENCIA", "men", [
    ("codigo_dba", "PK,FK"), ("numero_evidencia", "PK"), ("enunciado", ""),
])
EVIDENCIA_DICTAMEN = ("EVIDENCIA_DICTAMEN", "debil", [
    ("codigo_dba", "PK,FK"), ("numero_evidencia", "PK,FK"),
    ("aplica_formato_cerrado", ""), ("justificacion", ""), ("fecha_dictamen", ""),
])
EXPERIENCIA_EVIDENCIA = ("EXPERIENCIA_EVIDENCIA", "asociativa", [
    ("id_experiencia", "PK,FK"), ("codigo_dba", "PK,FK"),
    ("numero_evidencia", "PK,FK"), ("incluida", ""),
])
INSCRIPCION = ("INSCRIPCION", "asociativa", [
    ("id_inscripcion", "PK"), ("id_estudiante", "FK"), ("id_experiencia", "FK"),
    ("fecha_union", ""),
])
ITEM = ("ITEM", "propia", [
    ("id_item", "PK"), ("id_experiencia", "FK"), ("codigo_dba", "FK"),
    ("numero_evidencia", "FK"), ("enunciado", ""), ("formato", ""),
    ("origen", ""), ("estado_revision", ""), ("excluido", ""),
])
OPCION = ("OPCION", "propia", [
    ("id_opcion", "PK"), ("id_item", "FK"), ("texto", ""), ("orden", ""),
    ("es_correcta", ""), ("grupo", ""), ("hipotesis_error", ""),
])
PRESENTACION = ("PRESENTACION", "debil", [
    ("id_inscripcion", "PK,FK"), ("id_item", "PK,FK"),
    ("orden_presentacion", ""), ("fecha_presentacion", ""),
])
RESPUESTA = ("RESPUESTA", "asociativa", [
    ("id_respuesta", "PK"), ("id_inscripcion", "FK"), ("id_item", "FK"),
    ("certeza (CRI 0-5)", ""), ("correcta (derivado)", ""),
    ("fecha_respuesta", ""),
])
RESPUESTA_OPCION = ("RESPUESTA_OPCION", "asociativa", [
    ("id_respuesta", "PK,FK"), ("id_opcion", "PK,FK"), ("valor_dado", ""),
])
RESULTADO = ("RESULTADO", "debil", [
    ("id_inscripcion", "PK,FK"), ("codigo_dba", "PK,FK"),
    ("numero_evidencia", "PK,FK"), ("estado (derivado)", ""),
    ("fecha_calculo", ""),
])
REPORTE = ("REPORTE", "derivada", [
    ("id_experiencia", "FK"), ("estado_general (calc.)", ""),
    ("estado_por_evidencia (calc.)", ""),
])

ENTIDADES = [DOCENTE, ESTUDIANTE, EXPERIENCIA, DBA, EVIDENCIA,
             EVIDENCIA_DICTAMEN, EXPERIENCIA_EVIDENCIA, INSCRIPCION, ITEM,
             OPCION, PRESENTACION, RESPUESTA, RESPUESTA_OPCION, RESULTADO,
             REPORTE]

# ------------------------------------------------------------- relaciones
# a, b: nombres de entidad · card_a/card_b: lo que se rotula en cada extremo
# total_a/total_b: participacion total (linea doble)
# ident: relacion identificadora (rombo doble)
# vista: la UNICA vista donde esta relacion se dibuja
RELACIONES = [
    dict(nombre="comprende",     a="DBA",                   b="EVIDENCIA",
         card_a="1", card_b="N", total_a=True,  total_b=True,  ident=True,  vista=1),
    dict(nombre="se dictamina",  a="EVIDENCIA",             b="EVIDENCIA_DICTAMEN",
         card_a="1", card_b="1", total_a=False, total_b=True,  ident=True,  vista=1),

    dict(nombre="crea",          a="DOCENTE",               b="EXPERIENCIA",
         card_a="1", card_b="N", total_a=False, total_b=True,  ident=False, vista=2),
    dict(nombre="se ancla a",    a="EXPERIENCIA",           b="DBA",
         card_a="N", card_b="1", total_a=True,  total_b=False, ident=False, vista=2),
    dict(nombre="incluye",       a="EXPERIENCIA",           b="EXPERIENCIA_EVIDENCIA",
         card_a="1", card_b="N", total_a=True,  total_b=True,  ident=False, vista=2),
    dict(nombre="sobre",         a="EVIDENCIA",             b="EXPERIENCIA_EVIDENCIA",
         card_a="1", card_b="N", total_a=False, total_b=True,  ident=False, vista=2),

    dict(nombre="genera",        a="EXPERIENCIA_EVIDENCIA", b="ITEM",
         card_a="1", card_b="N", total_a=False, total_b=True,  ident=False, vista=3),
    dict(nombre="ofrece",        a="ITEM",                  b="OPCION",
         card_a="1", card_b="N", total_a=True,  total_b=True,  ident=False, vista=3),

    dict(nombre="realiza",       a="ESTUDIANTE",            b="INSCRIPCION",
         card_a="1", card_b="N", total_a=False, total_b=True,  ident=False, vista=4),
    dict(nombre="pertenece a",   a="INSCRIPCION",           b="EXPERIENCIA",
         card_a="N", card_b="1", total_a=True,  total_b=False, ident=False, vista=4),
    dict(nombre="atiende",       a="INSCRIPCION",           b="PRESENTACION",
         card_a="1", card_b="N", total_a=False, total_b=True,  ident=True,  vista=4),
    dict(nombre="se presenta",   a="ITEM",                  b="PRESENTACION",
         card_a="1", card_b="N", total_a=False, total_b=True,  ident=True,  vista=4),

    dict(nombre="registra",      a="PRESENTACION",          b="RESPUESTA",
         card_a="1", card_b="0..1", total_a=False, total_b=True, ident=False, vista=5),
    # N:M materializada por una entidad asociativa: se dibuja como el rombo
    # DENTRO del rectangulo (RESPUESTA_OPCION), con su atributo propio
    # valor_dado colgando -- mismo patron que "Membresia" en la referencia
    # de Semilleros. Tiene llave propia (id_respuesta, id_opcion), no
    # subrogada: no es una entidad mas, es la relacion hecha entidad.
    dict(nombre="selecciona",    a="RESPUESTA",             b="OPCION",
         card_a="N", card_b="M", total_a=True,  total_b=False, ident=False,
         vista=5, asociativa="RESPUESTA_OPCION"),

    dict(nombre="arroja",        a="INSCRIPCION",           b="RESULTADO",
         card_a="1", card_b="N", total_a=False, total_b=True,  ident=True,  vista=6),
    dict(nombre="mide",          a="EXPERIENCIA_EVIDENCIA", b="RESULTADO",
         card_a="1", card_b="N", total_a=False, total_b=True,  ident=True,  vista=6),
    dict(nombre="se agrega en",  a="RESULTADO",             b="REPORTE",
         card_a="N", card_b="1", total_a=False, total_b=False, ident=False, vista=6, derivada=True),
    dict(nombre="resume",        a="REPORTE",               b="EXPERIENCIA",
         card_a="1", card_b="1", total_a=False, total_b=False, ident=False, vista=6, derivada=True),
]

# ------------------------------------------------------------------ vistas
VISTAS = {
    1: ("Currículo oficial", "Qué nos entrega el MEN, y cuál es el único juicio nuestro sobre ese material."),
    2: ("Autoría de la experiencia", "Quién crea una experiencia, a qué DBA la ancla, y qué evidencias de ese DBA diagnostica realmente."),
    3: ("Banco de diagnóstico", "El contenido que el sistema genera para cada evidencia incluida."),
    4: ("Inscripción y entrega", "Quién entró a la experiencia, y qué ítem se le mostró en qué orden."),
    5: ("Captura de la respuesta", "Qué respondió exactamente, y con cuánta certeza."),
    6: ("Conclusión y reporte", "En qué se traduce todo lo anterior, por estudiante y por evidencia."),
}


# Entidades DEBILES: no tienen identidad propia fuera de su padre. Se dibujan
# con doble borde, y sus relaciones identificadoras con rombo doble.
DEBILES = {"EVIDENCIA", "EVIDENCIA_DICTAMEN", "PRESENTACION", "RESULTADO"}
