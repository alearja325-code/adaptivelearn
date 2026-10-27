"""Fuente unica de contenido del MER -- version final de la Fase III (2026-10-21).

Parte de la Quinta revision (2026-09-08, borrador anterior al cierre de la
Fase II) y la lleva a lo que la Fase II cerrada y el analisis de
requerimientos (11) exigen. Cambios, cada uno con su fuente:

  * CREDENCIAL (nueva) y sus dos relaciones "accede como": cierra V-8.
    Ventanas 014-019, RF-01-01..RF-01-09, y la tabla
    `credencial` que el incremento I1 ya construyo (`backend/` del repositorio,
    decision del 2026-09-17).
  * DOCENTE / ESTUDIANTE: `nombre` -> `nombres` + `apellidos` (specs 016 y
    026, RF-01-05, RF-01-11, ADR-029). El correo pasa a CREDENCIAL: es el
    correo de la cuenta, y asi su unicidad vale entre los dos roles
    (RF-01-04), cosa que dos UNIQUE separados no garantizan.
  * ITEM: `origen` con tres valores (ia / editado_docente / creado_docente,
    ADR-026). Sale `estado_revision`: tras ADR-026 revisar el banco no es
    requisito de nada y ningun requerimiento lo usa (cierra V-7).
  * EXPERIENCIA: `servicio_ia` + `modelo_ia` con que se genero su banco
    (RF-03-02, RF-03-03, ADR-030): un dato del banco, no de cada item.
  * EVIDENCIA_DICTAMEN: `formato`, el formato cerrado que admite la
    evidencia (RF-03-01, RF-03-07).
  * INSCRIPCION: `progreso`, calculado (RF-04-01); RESPUESTA pasa a propia.
  * Cardinalidad (min,max) en cada extremo, arco {xor} entre las dos
    «accede como», y los 5 ciclos del modelo con la regla que cierra cada uno.
  * EXPERIENCIA_EVIDENCIA: sale `incluida`. El docente no elige evidencias
    (QA-010) y solo entran las que el dictamen admite (RF-03-01): una fila
    de esta entidad ES una evidencia incluida.
  * Notacion Chen estricta (cierra del todo H-8): las llaves foraneas dejan
    de dibujarse como atributos; la llave parcial de EVIDENCIA va con
    subrayado punteado. Ver el comentario sobre las entidades.

Cambios del 2026-10-26, por la revision del docente del 2026-10-22
(`21-revision-docente-2026-10-22.md`, notas R1 y R3):

  * AREA, GRADO y DOCUMENTO_OFICIAL (nuevas, ADR-036): el catalogo
    curricular deja de guardar el area y el grado como texto suelto dentro
    de cada DBA. DBA pierde `area` y `grado`; entran sus tres relaciones
    (pertenece a, corresponde a, se copia de) y la del documento con su
    area (es de). Forman el ciclo C6, que cierra RI-20.
  * codigo_dba pasa al formato AREA-GG-NN, sin tildes (ADR-036, RI-21).
  * CREDENCIAL: `email_verificado` (si/no) pasa a `estado_verificacion`,
    con los valores procesando / verificado (ADR-037).

Cambios del 2026-10-27 (encargo 03):

  * CODIGO_VERIFICACION (nueva, debil, ADR-039 y nota R4): el codigo de 6
    digitos sale de CREDENCIAL a su propia entidad, con su proposito
    (verificar_correo / recuperar_contrasena), creado_en e intentos. El
    vencimiento (10 min) y la espera para reenviar (30 s) se calculan desde
    creado_en. CREDENCIAL pierde codigo_verificacion, codigo_expira_en y
    codigo_ultimo_envio. Relacion identificadora nueva: «recibe».
  * CREDENCIAL gana `es_admin`, la marca de administrador de la guia del
    docente: falsa por defecto, solo se pone por SQL (ADR-040).

Cada relacion declara en que VISTA vive. Regla dura, verificada por codigo
en _verificar_vistas.py: cada relacion aparece en exactamente una vista;
cada entidad, en al menos una.
"""

# ---------------------------------------------------------------- entidades
# (nombre, categoria, [(atributo, marca)])
#   categoria: propia | men | asociativa | debil | derivada
#   marca: "PK" llave primaria (elipse negra)
#          "PD" llave parcial de una entidad debil (subrayado punteado)
#          "D"  derivado que SE GUARDA (ADR-021): elipse punteada
#          "C"  calculado que NO se guarda: elipse punteada, sin columna en el MR
#          ""   atributo comun
#
# NOTACION CHEN ESTRICTA (hallazgo H-8 del docente): una entidad muestra solo
# SUS atributos. Las llaves foraneas no se dibujan: son lo que la derivacion
# al modelo relacional produce a partir de cada relacion ya dibujada. Asi el
# MER no es "casi el MR", y el MR aporta lo que le corresponde (FK, acciones
# referenciales, tipos). `_verificar_mr_mer.py` comprueba que cada columna de
# llave foranea del MR salga de una relacion de este MER.
#
# Entidades debiles: su identidad = la llave de su(s) duena(s), por la
# relacion identificadora, mas su llave parcial si la tiene. EVIDENCIA tiene
# llave parcial (numero_evidencia: la posicion dentro de su DBA); las otras
# tres debiles no la necesitan, porque las identifica la combinacion de sus
# duenas.

# Lo que el ACCESO necesita como dato (ventanas 014-019). El contador de
# intentos de inicio de sesion, el bloqueo y actualizado_en son
# endurecimiento del backend (RF-01-07): viven en el modelo relacional como
# columnas justificadas, no aqui -- el MER no dibuja mecanismos de
# seguridad. es_admin es la marca de administrador de la guia del docente
# (ADR-040): no es un rol del producto; solo se pone por SQL.
CREDENCIAL = ("CREDENCIAL", "propia", [
    ("id_credencial", "PK"), ("correo (U)", ""), ("proveedor", ""),
    ("password_hash", ""), ("proveedor_id", ""), ("estado_verificacion", ""),
    ("es_admin", ""), ("creado_en", ""),
])
# ADR-039 (nota R4 del docente): el codigo de verificacion deja la
# credencial. Debil: su identidad es la credencial que lo recibe mas su
# proposito (llave parcial), y asi una credencial tiene a lo sumo un codigo
# vigente por proposito. Se guarda el codigo con hash, no el codigo. El
# vencimiento (10 min) y la espera para reenviar (30 s) se calculan desde
# creado_en (RF-01-03); intentos cuenta los fallos con ESE codigo (maximo 5).
CODIGO_VERIFICACION = ("CODIGO_VERIFICACION", "debil", [
    ("proposito", "PD"), ("codigo_hash", ""), ("creado_en", ""), ("intentos", ""),
])
DOCENTE = ("DOCENTE", "propia", [
    ("id_docente", "PK"), ("nombres", ""), ("apellidos", ""), ("avatar_url", ""),
])
ESTUDIANTE = ("ESTUDIANTE", "propia", [
    ("id_estudiante", "PK"), ("nombres", ""), ("apellidos", ""), ("avatar_url", ""),
])
# servicio_ia y modelo_ia viven AQUI y no en cada item: un banco sale entero
# de un solo servicio (RF-03-02), asi que es un dato del banco, no del item.
# Guardarlo por item lo repetia 12 x N veces y dejaba que un banco mezclara
# servicios. El servicio de un item de origen ia o editado_docente es el de
# su experiencia; uno creado_docente no viene de la IA (RF-03-03, RI-17).
EXPERIENCIA = ("EXPERIENCIA", "propia", [
    ("id_experiencia", "PK"), ("nombre", ""), ("estado", ""),
    ("fecha_creacion", ""), ("fecha_publicacion", ""),
    ("codigo_invitacion (U)", ""), ("servicio_ia", ""), ("modelo_ia", ""),
])
# Catalogo curricular normalizado (ADR-036). Las tres son dato de
# referencia: las 4 areas de ADR-033, los grados 1 a 11 con su nivel de la
# Ley 115 de 1994, y el PDF oficial de cada area con la version, el ano, las
# paginas y la direccion que ADR-033 verifico contra los archivos del MEN.
# La version se lee del documento, nunca del nombre del archivo (ADR-033):
# Ciencias Sociales es V.1 aunque su archivo se llame "v2".
AREA = ("AREA", "men", [
    ("codigo_area", "PK"), ("nombre (U)", ""),
])
GRADO = ("GRADO", "men", [
    ("numero", "PK"), ("nombre (U)", ""), ("nivel", ""),
])
DOCUMENTO_OFICIAL = ("DOCUMENTO_OFICIAL", "men", [
    ("id_documento", "PK"), ("titulo", ""), ("version", ""), ("anio", ""),
    ("paginas", ""), ("url_oficial", ""),
])
# area y grado ya no son atributos: son las relaciones «pertenece a» y
# «corresponde a» (ADR-036). codigo_dba tiene el formato AREA-GG-NN (RI-21).
DBA = ("DBA", "men", [
    ("codigo_dba", "PK"), ("enunciado", ""), ("ejemplo", ""),
])
EVIDENCIA = ("EVIDENCIA", "men", [
    ("numero_evidencia", "PD"), ("enunciado", ""),
])
# formato: QUE formato cerrado admite la evidencia. RF-03-01 dice que "el
# formato de los items lo determina la evidencia" y RF-03-07 que una pregunta
# propia "se crea con el formato de esa evidencia": es un juicio nuestro sobre
# la evidencia, como aplica_formato_cerrado, y vive con el (RI-19).
EVIDENCIA_DICTAMEN = ("EVIDENCIA_DICTAMEN", "debil", [
    ("aplica_formato_cerrado", ""), ("formato", ""), ("justificacion", ""),
    ("fecha_dictamen", ""),
])
# Sin atributos propios: su identidad es el par (experiencia, evidencia) que
# le dan sus dos relaciones, incluye y sobre.
EXPERIENCIA_EVIDENCIA = ("EXPERIENCIA_EVIDENCIA", "asociativa", [])
# progreso: No iniciada / En curso / Completada (RF-04-01). Se calcula de sus
# presentaciones y resultados; no se guarda (ADR-022). Es lo que la v3 del
# docente llamaba estado_avance.
INSCRIPCION = ("INSCRIPCION", "asociativa", [
    ("id_inscripcion", "PK"), ("fecha_union", ""), ("progreso", "C"),
])
ITEM = ("ITEM", "propia", [
    ("id_item", "PK"), ("enunciado", ""), ("formato", ""), ("origen", ""),
    ("excluido", ""),
])
OPCION = ("OPCION", "propia", [
    ("id_opcion", "PK"), ("texto", ""), ("orden", ""), ("es_correcta", ""),
    ("grupo", ""), ("hipotesis_error", ""),
])
PRESENTACION = ("PRESENTACION", "debil", [
    ("orden_presentacion", ""), ("fecha_presentacion", ""),
])
# PROPIA, no asociativa: desde H-3 cuelga de una sola entidad (Presentacion,
# por «registra») y no resuelve ninguna N:M. La asociativa de esa parte del
# modelo es RESPUESTA_OPCION.
RESPUESTA = ("RESPUESTA", "propia", [
    ("id_respuesta", "PK"), ("certeza (CRI 0-5)", ""), ("correcta", "D"),
    ("fecha_respuesta", ""),
])
RESPUESTA_OPCION = ("RESPUESTA_OPCION", "asociativa", [
    ("valor_dado", ""),
])
RESULTADO = ("RESULTADO", "debil", [
    ("estado", "D"), ("fecha_calculo", ""),
])
REPORTE = ("REPORTE", "derivada", [
    ("estado_general", "C"), ("estado_por_evidencia", "C"),
])

ENTIDADES = [CREDENCIAL, CODIGO_VERIFICACION, DOCENTE, ESTUDIANTE, EXPERIENCIA, AREA, GRADO,
             DOCUMENTO_OFICIAL, DBA, EVIDENCIA,
             EVIDENCIA_DICTAMEN, EXPERIENCIA_EVIDENCIA, INSCRIPCION, ITEM,
             OPCION, PRESENTACION, RESPUESTA, RESPUESTA_OPCION, RESULTADO,
             REPORTE]

# ------------------------------------------------------------- relaciones
# a, b: nombres de entidad
# card_a/card_b: la RAZON de cardinalidad (1, N, M): sale el 1:n bajo el rombo
# part_a/part_b: (min,max) de cada entidad, la notacion que uso el docente en
#                su v3: cuantas veces participa un ejemplar de esa entidad.
#                Es lo que se rotula junto a cada entidad en los diagramas.
# total_a/total_b: participacion total (linea doble). Debe coincidir con
#                  min >= 1: lo comprueba _verificar_mer.py
# ident: relacion identificadora (rombo doble)
# vista: la UNICA vista donde esta relacion se dibuja
# id: clave interna, solo cuando dos relaciones comparten nombre
# xor: grupo de relaciones mutuamente excluyentes (RI-12)
RELACIONES = [
    # Una credencial accede como a lo sumo UN rol (RI-12). El diagrama lo
    # marca con el arco {xor} entre las dos; el MR lo hace cumplir con un CHECK.
    dict(id="accede_docente",    nombre="accede como", a="CREDENCIAL", b="DOCENTE",
         card_a="1", card_b="1", part_a="(0,1)", part_b="(1,1)",
         total_a=False, total_b=True,  ident=False, vista=1, xor="rol"),
    dict(id="accede_estudiante", nombre="accede como", a="CREDENCIAL", b="ESTUDIANTE",
         card_a="1", card_b="1", part_a="(0,1)", part_b="(1,1)",
         total_a=False, total_b=True,  ident=False, vista=1, xor="rol"),
    # (0,2): a lo sumo un codigo vigente por proposito, y hay dos propositos
    # (ADR-039). Un codigo es siempre de una credencial: identificadora.
    dict(nombre="recibe", a="CREDENCIAL", b="CODIGO_VERIFICACION",
         card_a="1", card_b="N", part_a="(0,2)", part_b="(1,1)",
         total_a=False, total_b=True,  ident=True,  vista=1),

    # Catalogo normalizado (ADR-036). Del lado del DBA las tres son (1,1):
    # todo DBA es de un area, de un grado y de un documento. Del otro lado,
    # (1,N): el catalogo se carga completo (`10`, §2.3), y un area, un grado
    # o un documento sin ningun DBA no tendria nada que ofrecer.
    dict(id="pertenece_area", nombre="pertenece a", a="DBA", b="AREA",
         card_a="N", card_b="1", part_a="(1,1)", part_b="(1,N)",
         total_a=True,  total_b=True,  ident=False, vista=2),
    dict(nombre="corresponde a", a="DBA",                   b="GRADO",
         card_a="N", card_b="1", part_a="(1,1)", part_b="(1,N)",
         total_a=True,  total_b=True,  ident=False, vista=2),
    dict(nombre="se copia de",   a="DBA",                   b="DOCUMENTO_OFICIAL",
         card_a="N", card_b="1", part_a="(1,1)", part_b="(1,N)",
         total_a=True,  total_b=True,  ident=False, vista=2),
    # Un documento por area en esta version (ADR-036); (1,N) del lado del
    # area porque una version nueva del MEN entraria como otro documento
    # (ADR-033, punto 4) sin borrar el anterior.
    dict(nombre="es de",         a="DOCUMENTO_OFICIAL",     b="AREA",
         card_a="N", card_b="1", part_a="(1,1)", part_b="(1,N)",
         total_a=True,  total_b=True,  ident=False, vista=2),

    dict(nombre="comprende",     a="DBA",                   b="EVIDENCIA",
         card_a="1", card_b="N", part_a="(1,N)", part_b="(1,1)",
         total_a=True,  total_b=True,  ident=True,  vista=2),
    dict(nombre="se dictamina",  a="EVIDENCIA",             b="EVIDENCIA_DICTAMEN",
         card_a="1", card_b="1", part_a="(0,1)", part_b="(1,1)",
         total_a=False, total_b=True,  ident=True,  vista=2),

    dict(nombre="crea",          a="DOCENTE",               b="EXPERIENCIA",
         card_a="1", card_b="N", part_a="(0,N)", part_b="(1,1)",
         total_a=False, total_b=True,  ident=False, vista=3),
    dict(nombre="se ancla a",    a="EXPERIENCIA",           b="DBA",
         card_a="N", card_b="1", part_a="(1,1)", part_b="(0,N)",
         total_a=True,  total_b=False, ident=False, vista=3),
    dict(nombre="incluye",       a="EXPERIENCIA",           b="EXPERIENCIA_EVIDENCIA",
         card_a="1", card_b="N", part_a="(1,N)", part_b="(1,1)",
         total_a=True,  total_b=True,  ident=False, vista=3),
    dict(nombre="sobre",         a="EVIDENCIA",             b="EXPERIENCIA_EVIDENCIA",
         card_a="1", card_b="N", part_a="(0,N)", part_b="(1,1)",
         total_a=False, total_b=True,  ident=False, vista=3),

    # (12,N): la IA genera 12 por evidencia incluida (RF-03-01) y un item no
    # se borra -- descartar lo excluye (RF-03-06) --, asi que nunca bajan de 12.
    dict(nombre="genera",        a="EXPERIENCIA_EVIDENCIA", b="ITEM",
         card_a="1", card_b="N", part_a="(12,N)", part_b="(1,1)",
         total_a=True,  total_b=True,  ident=False, vista=4),
    # (2,N): el minimo general; en matching son 4 (RI-4, hallazgo H-9).
    dict(nombre="ofrece",        a="ITEM",                  b="OPCION",
         card_a="1", card_b="N", part_a="(2,N)", part_b="(1,1)",
         total_a=True,  total_b=True,  ident=False, vista=4),

    dict(nombre="realiza",       a="ESTUDIANTE",            b="INSCRIPCION",
         card_a="1", card_b="N", part_a="(0,N)", part_b="(1,1)",
         total_a=False, total_b=True,  ident=False, vista=5),
    dict(nombre="pertenece a",   a="INSCRIPCION",           b="EXPERIENCIA",
         card_a="N", card_b="1", part_a="(1,1)", part_b="(0,N)",
         total_a=True,  total_b=False, ident=False, vista=5),
    dict(nombre="atiende",       a="INSCRIPCION",           b="PRESENTACION",
         card_a="1", card_b="N", part_a="(0,N)", part_b="(1,1)",
         total_a=False, total_b=True,  ident=True,  vista=5),
    dict(nombre="se presenta",   a="ITEM",                  b="PRESENTACION",
         card_a="1", card_b="N", part_a="(0,N)", part_b="(1,1)",
         total_a=False, total_b=True,  ident=True,  vista=5),

    dict(nombre="registra",      a="PRESENTACION",          b="RESPUESTA",
         card_a="1", card_b="1", part_a="(0,1)", part_b="(1,1)",
         total_a=False, total_b=True, ident=False, vista=6),
    # N:M materializada por una entidad asociativa: el rombo DENTRO del
    # rectangulo (RESPUESTA_OPCION), con su atributo propio valor_dado.
    # (1,N): toda respuesta elige al menos una opcion; en single_choice,
    # exactamente una (RI-6).
    dict(nombre="selecciona",    a="RESPUESTA",             b="OPCION",
         card_a="N", card_b="M", part_a="(1,N)", part_b="(0,N)",
         total_a=True,  total_b=False, ident=False,
         vista=6, asociativa="RESPUESTA_OPCION"),

    dict(nombre="arroja",        a="INSCRIPCION",           b="RESULTADO",
         card_a="1", card_b="N", part_a="(0,N)", part_b="(1,1)",
         total_a=False, total_b=True,  ident=True,  vista=7),
    dict(nombre="mide",          a="EXPERIENCIA_EVIDENCIA", b="RESULTADO",
         card_a="1", card_b="N", part_a="(0,N)", part_b="(1,1)",
         total_a=False, total_b=True,  ident=True,  vista=7),
    dict(nombre="se agrega en",  a="RESULTADO",             b="REPORTE",
         card_a="N", card_b="1", part_a="(1,1)", part_b="(0,N)",
         total_a=False, total_b=False, ident=False, vista=7, derivada=True),
    dict(nombre="resume",        a="REPORTE",               b="EXPERIENCIA",
         card_a="1", card_b="1", part_a="(1,1)", part_b="(1,1)",
         total_a=False, total_b=False, ident=False, vista=7, derivada=True),
]

# ------------------------------------------------------------------ ciclos
# El grafo del MER (entidades persistentes; «selecciona» cuenta como dos
# aristas, porque pasa por RESPUESTA_OPCION) tiene 24 aristas y 19 nodos:
# 24 - 19 + 1 = 6 ciclos independientes. Son estos, y cada uno dice si exige
# una regla para cerrarse y quien la hace cumplir. Un ciclo sin regla es
# exactamente lo que el docente señalo en H-4. _verificar_mer.py comprueba
# que sean 6, que cada uno exista en el grafo y que sean independientes.
CICLOS = [
    dict(id="C1", que="La evidencia incluida es del DBA al que se ancla la experiencia",
         camino=["EXPERIENCIA", "EXPERIENCIA_EVIDENCIA", "EVIDENCIA", "DBA", "EXPERIENCIA"],
         regla="RI-18", como="Estructura: llave foránea compuesta (id_experiencia, codigo_dba) "
                             "de experiencia_evidencia hacia experiencia."),
    dict(id="C2", que="El ítem presentado es de la experiencia de la inscripción",
         camino=["INSCRIPCION", "PRESENTACION", "ITEM", "EXPERIENCIA_EVIDENCIA",
                 "EXPERIENCIA", "INSCRIPCION"],
         regla="RI-13", como="Estructura: id_experiencia en presentacion, dentro de las dos "
                             "llaves foráneas compuestas."),
    dict(id="C3", que="El resultado es de una evidencia de la experiencia de la inscripción",
         camino=["INSCRIPCION", "RESULTADO", "EXPERIENCIA_EVIDENCIA", "EXPERIENCIA",
                 "INSCRIPCION"],
         regla="RI-13", como="Estructura: id_experiencia en resultado, dentro de las dos "
                             "llaves foráneas compuestas."),
    dict(id="C4", que="La opción elegida es del ítem que se presentó",
         camino=["RESPUESTA", "PRESENTACION", "ITEM", "OPCION", "RESPUESTA_OPCION",
                 "RESPUESTA"],
         regla="RI-6", como="Estructura: id_item en respuesta_opcion, dentro de las dos "
                            "llaves foráneas compuestas."),
    dict(id="C5", que="Nada: el docente que crea y el estudiante que se inscribe son cuentas distintas",
         camino=["CREDENCIAL", "DOCENTE", "EXPERIENCIA", "INSCRIPCION", "ESTUDIANTE",
                 "CREDENCIAL"],
         regla=None, como="No exige regla: por RI-12 una credencial accede como un solo rol, "
                          "así que los dos extremos son siempre dos credenciales distintas."),
    # Nuevo con ADR-036: el area del DBA y la de su documento oficial tienen
    # que ser la misma. Se cierra con la tecnica de C1 a C4.
    dict(id="C6", que="El documento oficial de un DBA es de su misma área",
         camino=["DBA", "AREA", "DOCUMENTO_OFICIAL", "DBA"],
         regla="RI-20", como="Estructura: llave foránea compuesta (id_documento, codigo_area) "
                             "de dba hacia documento_oficial."),
]

# ------------------------------------------------------------------ vistas
VISTAS = {
    1: ("Acceso y cuentas", "Quién puede entrar, con qué credencial, con cuál de los dos roles, y con qué código verifica su correo o recupera su contraseña."),
    2: ("Currículo oficial", "Qué nos entrega el MEN —cada DBA con su área, su grado y el documento del que se copió—, y cuál es el único juicio nuestro sobre ese material."),
    3: ("Autoría de la experiencia", "Quién crea una experiencia, a qué DBA la ancla, y qué evidencias de ese DBA diagnostica."),
    4: ("Banco de diagnóstico", "El contenido que se genera, se edita o se agrega para cada evidencia incluida."),
    5: ("Inscripción y entrega", "Quién entró a la experiencia, y qué ítem se le mostró en qué orden."),
    6: ("Captura de la respuesta", "Qué respondió exactamente, y con cuánta certeza."),
    7: ("Conclusión y reporte", "En qué se traduce todo lo anterior, por estudiante y por evidencia."),
}


# Entidades DEBILES: no tienen identidad propia fuera de su padre. Se dibujan
# con doble borde, y sus relaciones identificadoras con rombo doble.
DEBILES = {"CODIGO_VERIFICACION", "EVIDENCIA", "EVIDENCIA_DICTAMEN", "PRESENTACION", "RESULTADO"}

# Conteos que el resto de los documentos cita: se calculan, no se escriben.
N_ENTIDADES = len([e for e in ENTIDADES if e[1] != "derivada"])
N_REL_REALES = len([r for r in RELACIONES if not r.get("derivada")])
N_REL_DERIVADAS = len([r for r in RELACIONES if r.get("derivada")])
N_ATRIBUTOS = sum(len(e[2]) for e in ENTIDADES)
