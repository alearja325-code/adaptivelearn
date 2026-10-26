"""Bateria de pruebas del Modelo Relacional, comun a SQLite y a MySQL.

Una sola lista de pruebas, escrita en SQL que los dos motores entienden.
`verificar_mr.py` la corre contra SQLite en memoria (rapido, sin nada
instalado); `probar_mysql.py` la corre contra un MySQL 8 real. Si un
motor acepta un dato que el otro rechaza, la diferencia aparece aqui y no
en produccion.

Tres clases de prueba:
  FALLA   el dato rompe una regla: el motor DEBE rechazarlo.
  PASA    el dato es valido aunque parezca raro: el motor DEBE aceptarlo.
  QUEDA   se ejecuta y despues se cuentan filas: lo que debe quedar
          (sirve para probar la politica de borrado en cascada, V-11).

En una FALLA, las sentencias previas preparan el caso y deben entrar; solo
la ultima debe romper algo. Y no basta con que el motor rechace: tiene que
rechazar POR LA REGLA QUE LA PRUEBA NOMBRA. MySQL dice en el error que
restriccion se rompio, asi que `probar_mysql.py` lo exige (MOTIVO_MYSQL, al
final). Asi aparecio, el 2026-10-21, una prueba que pasaba por la razon
equivocada: el resultado "de otra experiencia" se rechazaba por llave
primaria duplicada, no por RI-13. SQLite no nombra la restriccion de una
FK rota, y por eso alli solo se exige el rechazo.

Todas parten de la misma SEMILLA: un juego minimo de datos validos con
dos experiencias, para poder probar las reglas que cruzan experiencias.
"""


def v(x):
    if x is None:
        return "NULL"
    if isinstance(x, bool):
        return "1" if x else "0"
    if isinstance(x, int):
        return str(x)
    return "'" + str(x).replace("'", "''") + "'"


def ins(tabla, **cols):
    return (f"INSERT INTO {tabla} ({', '.join(cols)}) "
            f"VALUES ({', '.join(v(x) for x in cols.values())});")


F = "2026-03-02 10:00:00"
MAT = "MAT-08-01"
LEN = "LEN-08-01"                 # otro DBA, para las pruebas de RI-18


def docente(i, nombres="Ana", apellidos="Pérez"):
    return ins("docente", id_docente=i, nombres=nombres, apellidos=apellidos)


def cred_correo(i, correo, **kw):
    base = dict(id_credencial=i, correo=correo, proveedor="correo",
                password_hash="$argon2id$hash", estado_verificacion="verificado")
    base.update(kw)
    return ins("credencial", **base)


def dba(codigo, area="MAT", grado=8, documento=1):
    return ins("dba", codigo_dba=codigo, codigo_area=area, numero_grado=grado,
               id_documento=documento, enunciado="Enunciado oficial", ejemplo=None)


def documento(i, area, version="V.2", paginas=88):
    return ins("documento_oficial", id_documento=i, codigo_area=area,
               titulo=f"Derechos Básicos de Aprendizaje {area}", version=version,
               anio=2016, paginas=paginas, url_oficial="http://www.colombiaaprende.edu.co/x.pdf")


def experiencia(i, codigo, estado="Publicada", fecha_pub=F, **kw):
    base = dict(id_experiencia=i, id_docente=1, codigo_dba=MAT, nombre="Exp",
                estado=estado, fecha_creacion=F, fecha_publicacion=fecha_pub,
                codigo_invitacion=codigo, servicio_ia="gemini",
                modelo_ia="gemini-2.5-flash")
    base.update(kw)
    return ins("experiencia", **base)


def item(i, exp=1, ev=1, origen="ia", formato="single_choice"):
    return ins("item", id_item=i, id_experiencia=exp, codigo_dba=MAT,
               numero_evidencia=ev, enunciado="¿Pregunta?", formato=formato,
               origen=origen, excluido=False)


def dictamen(ev, aplica, formato, dba=MAT):
    return ins("evidencia_dictamen", codigo_dba=dba, numero_evidencia=ev,
               aplica_formato_cerrado=aplica, formato=formato,
               justificacion="juicio del equipo", fecha_dictamen=F)


def eleccion(resp, opcion, it, valor=None):
    return ins("respuesta_opcion", id_respuesta=resp, id_opcion=opcion, id_item=it,
               valor_dado=valor)


def presentacion(insc, it, exp, orden):
    return ins("presentacion", id_inscripcion=insc, id_item=it,
               id_experiencia=exp, orden_presentacion=orden,
               fecha_presentacion=F)


def respuesta(i, insc, it, certeza=4, correcta=True):
    return ins("respuesta", id_respuesta=i, id_inscripcion=insc, id_item=it,
               certeza=certeza, fecha_respuesta=F, correcta=correcta)


def resultado(insc, exp, ev, estado="muestra"):
    return ins("resultado", id_inscripcion=insc, id_experiencia=exp,
               codigo_dba=MAT, numero_evidencia=ev, estado=estado,
               fecha_calculo=F)


SEMILLA = [
    docente(1),
    ins("estudiante", id_estudiante=1, nombres="Luis", apellidos="Gómez"),
    ins("estudiante", id_estudiante=2, nombres="Sara", apellidos="Ruiz"),
    cred_correo(1, "ana@colegio.co", id_docente=1),
    ins("credencial", id_credencial=2, id_estudiante=1, correo="luis@gmail.com",
        proveedor="google", proveedor_id="g-111", estado_verificacion="verificado"),
    # catalogo (ADR-036): dos areas, para poder probar RI-20
    ins("area", codigo_area="MAT", nombre="Matemáticas"),
    ins("area", codigo_area="LEN", nombre="Lenguaje"),
    ins("grado", numero=8, nombre="Octavo", nivel="basica_secundaria"),
    documento(1, "MAT"),
    documento(2, "LEN", paginas=56),
    dba(MAT),
    ins("evidencia", codigo_dba=MAT, numero_evidencia=1, enunciado="Evidencia 1"),
    ins("evidencia", codigo_dba=MAT, numero_evidencia=2, enunciado="Evidencia 2"),
    dictamen(1, True, "single_choice"),
    # experiencia 1: evidencia 1 incluida, un item, un inscrito que respondio
    experiencia(1, "ABC234"),
    ins("experiencia_evidencia", id_experiencia=1, codigo_dba=MAT, numero_evidencia=1),
    item(1),
    ins("opcion", id_opcion=1, id_item=1, texto="A", es_correcta=True),
    ins("opcion", id_opcion=2, id_item=1, texto="B", es_correcta=False),
    ins("inscripcion", id_inscripcion=1, id_estudiante=1, id_experiencia=1, fecha_union=F),
    presentacion(1, 1, 1, 1),
    respuesta(1, 1, 1),
    eleccion(1, 1, 1),
    resultado(1, 1, 1),
    # experiencia 2, del mismo docente: sirve para las pruebas cruzadas
    experiencia(2, "XYZ789"),
    ins("experiencia_evidencia", id_experiencia=2, codigo_dba=MAT, numero_evidencia=1),
    item(2, exp=2),
    ins("inscripcion", id_inscripcion=2, id_estudiante=2, id_experiencia=2, fecha_union=F),
]

# Lo que se cuenta en las pruebas QUEDA
CONTEOS = ["docente", "credencial", "estudiante", "area", "grado", "documento_oficial",
           "dba", "evidencia",
           "experiencia", "experiencia_evidencia", "item", "opcion",
           "inscripcion", "presentacion", "respuesta", "respuesta_opcion",
           "resultado"]

PRUEBAS = [
    # ------------------------------------------------ acceso (V-8, RI-12)
    ("FALLA", "correo repetido entre los dos roles (RI-3, RF-01-04)",
     [docente(2), cred_correo(3, "luis@gmail.com", id_docente=2)]),
    ("FALLA", "correo repetido escrito con otras mayúsculas (RF-01-04)",
     [docente(2), cred_correo(3, "ANA@Colegio.co", id_docente=2)]),
    ("FALLA", "una credencial que da acceso como docente Y como estudiante (RI-12)",
     [docente(2), cred_correo(3, "doble@x.co", id_docente=2, id_estudiante=2)]),
    ("FALLA", "dos credenciales para el mismo docente (relación 1:1)",
     [cred_correo(3, "otra@x.co", id_docente=1)]),
    ("FALLA", "cuenta de correo sin contraseña (RI-15)",
     [cred_correo(3, "sin@x.co", password_hash=None)]),
    ("FALLA", "cuenta de Google con contraseña guardada (RI-15)",
     [ins("credencial", id_credencial=3, correo="g@x.co", proveedor="google",
          password_hash="hash", proveedor_id="g-222", estado_verificacion="verificado")]),
    ("FALLA", "cuenta de Google con el correo todavía «procesando» (RI-15, ADR-037)",
     [ins("credencial", id_credencial=3, correo="g@x.co", proveedor="google",
          proveedor_id="g-222", estado_verificacion="procesando")]),
    ("FALLA", "estado de verificación inventado (ADR-037)",
     [cred_correo(3, "e@x.co", estado_verificacion="vencido")]),
    ("FALLA", "la misma cuenta de Google abriendo una segunda credencial (RF-01-04)",
     [ins("credencial", id_credencial=3, correo="otro@gmail.com", proveedor="google",
          proveedor_id="g-111", estado_verificacion="verificado")]),
    ("FALLA", "proveedor fuera de alcance: Apple (RF-01-02)",
     [ins("credencial", id_credencial=3, correo="a@icloud.com", proveedor="apple",
          proveedor_id="a-1", estado_verificacion="verificado")]),
    ("FALLA", "docente con nombres vacíos (RF-01-05)",
     [docente(2, nombres="   ")]),
    ("FALLA", "borrar un docente que tiene credencial y experiencias (RESTRICT)",
     ["DELETE FROM docente WHERE id_docente = 1;"]),
    ("PASA", "credencial recién creada, sin rol elegido todavía (ventanas 014-017)",
     [cred_correo(3, "nueva@x.co", estado_verificacion="procesando")]),
    ("PASA", "credencial de correo sin estado dicho: nace «procesando» (ADR-037)",
     [ins("credencial", id_credencial=3, correo="nueva@x.co", proveedor="correo",
          password_hash="$argon2id$hash")]),

    # ------------------------------------------------ catálogo (ADR-036, RI-20, RI-21)
    ("FALLA", "un DBA sin área (ADR-036)",
     [dba("MAT-08-02", area=None)]),
    ("FALLA", "un DBA de un área que no existe (ADR-036)",
     [dba("ART-08-01", area="ART")]),
    ("FALLA", "un DBA de Matemáticas copiado del documento de Lenguaje (RI-20, ciclo C6)",
     [dba("MAT-08-02", documento=2)]),
    ("FALLA", "un DBA de un grado fuera del catálogo: Transición, grado 0 (ADR-033)",
     [dba("MAT-00-01", grado=0)]),
    ("FALLA", "código de DBA en el formato viejo, sin ceros (RI-21)",
     [dba("MAT-8-2")]),
    ("FALLA", "código de DBA con un área distinta de la de su fila (RI-21)",
     [dba("LEN-08-02")]),
    ("FALLA", "código de DBA con un grado distinto del de su fila (RI-21)",
     [ins("grado", numero=9, nombre="Noveno", nivel="basica_secundaria"),
      dba("MAT-09-02")]),
    ("FALLA", "código de DBA en minúsculas (RI-21)",
     [dba("mat-08-02")]),
    ("FALLA", "código de DBA con número 00 (RI-21)",
     [dba("MAT-08-00")]),
    ("FALLA", "código de área con tilde (ADR-036)",
     [ins("area", codigo_area="CÑ", nombre="Ciencias")]),
    ("FALLA", "código de área en minúsculas (ADR-036)",
     [ins("area", codigo_area="cs", nombre="Ciencias Sociales")]),
    ("FALLA", "grado con un nivel que no es el de la Ley 115 (ADR-036)",
     [ins("grado", numero=9, nombre="Noveno", nivel="media")]),
    ("FALLA", "grado 12, fuera de la educación básica y media",
     [ins("grado", numero=12, nombre="Duodécimo", nivel="media")]),
    ("FALLA", "la misma versión del documento de un área, cargada dos veces (ADR-033)",
     [documento(3, "MAT")]),
    ("FALLA", "borrar un área que tiene DBA y documento (RESTRICT)",
     ["DELETE FROM area WHERE codigo_area = 'MAT';"]),
    ("PASA", "un DBA de 11° de Ciencias Sociales, con su documento V.1 (ADR-033)",
     [ins("area", codigo_area="CS", nombre="Ciencias Sociales"),
      ins("grado", numero=11, nombre="Undécimo", nivel="media"),
      documento(3, "CS", version="V.1", paginas=52),
      dba("CS-11-05", area="CS", grado=11, documento=3)]),

    # ------------------------------------------------ experiencia (RI-3, RI-16)
    ("FALLA", "código de invitación repetido (RI-3)",
     [experiencia(3, "ABC234")]),
    ("FALLA", "código de invitación repetido en minúsculas (RI-3)",
     [experiencia(3, "abc234")]),
    ("FALLA", "código de invitación con carácter ambiguo 'O' (08-spec §2.3)",
     [experiencia(3, "ABCO34")]),
    ("FALLA", "código de invitación de 5 caracteres",
     [experiencia(3, "ABC23")]),
    ("FALLA", "estado de experiencia inventado",
     [experiencia(3, "QRS234", estado="Archivada")]),
    ("FALLA", "experiencia Publicada sin fecha de publicación (RI-16)",
     [experiencia(3, "QRS234", fecha_pub=None)]),
    ("FALLA", "experiencia en Borrador con fecha de publicación (RI-16)",
     [experiencia(3, "QRS234", estado="Borrador")]),
    ("FALLA", "experiencia sin el servicio de IA que generó su banco (RI-17, RF-03-02)",
     [experiencia(3, "QRS234", servicio_ia=None)]),
    ("FALLA", "servicio de IA fuera de ADR-030",
     [experiencia(3, "QRS234", servicio_ia="chatgpt")]),
    ("FALLA", "una experiencia incluye una evidencia de OTRO DBA (RI-18, ciclo C1)",
     [dba(LEN, area="LEN", documento=2),
      ins("evidencia", codigo_dba=LEN, numero_evidencia=1, enunciado="evidencia de lenguaje"),
      ins("experiencia_evidencia", id_experiencia=1, codigo_dba=LEN, numero_evidencia=1)]),

    # ------------------------------------------------ banco (H-4, RI-17)
    ("FALLA", "ítem sobre una evidencia que su experiencia NO incluye (H-4)",
     [item(9, ev=2)]),
    ("FALLA", "formato de ítem inventado (ADR-006)",
     [item(9, formato="ensayo")]),
    ("FALLA", "origen de ítem inventado",
     [item(9, origen="chatgpt")]),
    ("PASA", "ítem creado por el docente: no se le atribuye a la IA (RF-03-07)",
     [item(9, origen="creado_docente")]),
    ("PASA", "ítem editado por el docente: su servicio sigue siendo el de la experiencia (RF-03-05)",
     [item(9, origen="editado_docente")]),
    ("FALLA", "dictamen que admite formato cerrado sin decir cuál (RI-19)",
     [dictamen(2, True, None)]),
    ("FALLA", "dictamen que no admite formato cerrado y aun así fija uno (RI-19)",
     [dictamen(2, False, "ordering")]),
    ("PASA", "dictamen que no admite formato cerrado, sin formato (RF-06-02)",
     [dictamen(2, False, None)]),
    ("FALLA", "número de evidencia igual a 0",
     [ins("evidencia", codigo_dba=MAT, numero_evidencia=0, enunciado="Cero")]),
    ("FALLA", "borrar una evidencia oficial que una experiencia usa (RESTRICT)",
     [f"DELETE FROM evidencia WHERE codigo_dba = '{MAT}' AND numero_evidencia = 1;"]),

    # ------------------------------------------------ inscripción y entrega
    ("FALLA", "el mismo estudiante inscrito dos veces en la misma experiencia (RI-1)",
     [ins("inscripcion", id_inscripcion=9, id_estudiante=1, id_experiencia=1,
          fecha_union=F)]),
    ("FALLA", "presentar a la inscripción de la experiencia 1 un ítem de la "
              "experiencia 2, declarando la 1 (RI-13)",
     [presentacion(1, 2, 1, 2)]),
    ("FALLA", "lo mismo, declarando la 2 (RI-13: ninguna combinación pasa)",
     [presentacion(1, 2, 2, 2)]),
    ("FALLA", "orden de presentación igual a 0 (RI-8)",
     [item(9), presentacion(1, 9, 1, 0)]),
    ("FALLA", "dos presentaciones con el mismo orden en una inscripción (RI-8)",
     [item(9), presentacion(1, 9, 1, 1)]),
    ("PASA", "una presentación SIN respuesta: «se le mostró y no respondió» (H-3, ADR-031)",
     [item(9), presentacion(1, 9, 1, 2)]),

    # ------------------------------------------------ respuesta
    ("FALLA", "respuesta a un ítem que no se le presentó (H-3)",
     [item(9), respuesta(9, 1, 9)]),
    ("FALLA", "segunda respuesta a la misma presentación",
     [respuesta(9, 1, 1)]),
    ("FALLA", "certeza fuera de la escala CRI 0-5 (ADR-008)",
     [item(9), presentacion(1, 9, 1, 2), respuesta(9, 1, 9, certeza=9)]),
    ("FALLA", "la respuesta al ítem 1 elige una opción del ítem 2, declarando el ítem 1 "
              "(RI-6, ciclo C4)",
     [ins("opcion", id_opcion=50, id_item=2, texto="opción del ítem 2", es_correcta=True),
      eleccion(1, 50, 1)]),
    ("FALLA", "lo mismo, declarando el ítem 2 (RI-6: ninguna combinación pasa)",
     [ins("opcion", id_opcion=50, id_item=2, texto="opción del ítem 2", es_correcta=True),
      eleccion(1, 50, 2)]),

    # ------------------------------------------------ resultado (RI-13)
    ("FALLA", "estado de resultado inventado (ADR-022)",
     ["DELETE FROM resultado;", resultado(1, 1, 1, estado="aprobado")]),
    ("FALLA", "resultado cuya experiencia no es la de su inscripción (RI-13)",
     ["DELETE FROM resultado;", resultado(1, 2, 1)]),
    ("FALLA", "resultado sobre una evidencia que esa experiencia no incluye",
     [resultado(1, 1, 2)]),

    # ------------------------------------------------ política de borrado (V-11)
    ("QUEDA", "eliminar una experiencia arrastra todo lo suyo y nada más (RF-02-07)",
     ["DELETE FROM experiencia WHERE id_experiencia = 1;"],
     dict(docente=1, credencial=2, estudiante=2, area=2, grado=1, documento_oficial=2,
          dba=1, evidencia=2, experiencia=1, experiencia_evidencia=1, item=1, opcion=0,
          inscripcion=1, presentacion=0, respuesta=0, respuesta_opcion=0,
          resultado=0)),
    ("QUEDA", "salir de una experiencia borra lo respondido y deja el banco (RF-04-12)",
     ["DELETE FROM inscripcion WHERE id_inscripcion = 1;"],
     dict(docente=1, credencial=2, estudiante=2, dba=1, evidencia=2,
          experiencia=2, experiencia_evidencia=2, item=2, opcion=2,
          inscripcion=1, presentacion=0, respuesta=0, respuesta_opcion=0,
          resultado=0)),
    ("QUEDA", "«descartar» un ítem no borra nada (RF-03-06, ADR-015)",
     ["UPDATE item SET excluido = 1 WHERE id_item = 1;"],
     dict(item=2, opcion=2, presentacion=1, respuesta=1, respuesta_opcion=1)),
]

# Que restriccion debe ser la que rechaza cada FALLA, en MySQL. Los nombres
# salen de generar.py (ck_/fk_/uq_<tabla>_<n>); un ENUM roto se reconoce por
# la columna. Si se renumera una restriccion, esto falla y hay que mirar.
MOTIVO_MYSQL = {
    "correo repetido entre los dos roles (RI-3, RF-01-04)": "uq_credencial_1",
    "correo repetido escrito con otras mayúsculas (RF-01-04)": "uq_credencial_1",
    "una credencial que da acceso como docente Y como estudiante (RI-12)": "ck_credencial_1",
    "dos credenciales para el mismo docente (relación 1:1)": "uq_credencial_2",
    "cuenta de correo sin contraseña (RI-15)": "ck_credencial_2",
    "cuenta de Google con contraseña guardada (RI-15)": "ck_credencial_2",
    "cuenta de Google con el correo todavía «procesando» (RI-15, ADR-037)": "ck_credencial_2",
    "estado de verificación inventado (ADR-037)": "column 'estado_verificacion'",
    "un DBA sin área (ADR-036)": "'codigo_area' cannot be null",
    "un DBA de un área que no existe (ADR-036)": "fk_dba_1",
    "un DBA de Matemáticas copiado del documento de Lenguaje (RI-20, ciclo C6)": "fk_dba_3",
    "un DBA de un grado fuera del catálogo: Transición, grado 0 (ADR-033)": "fk_dba_2",
    "código de DBA en el formato viejo, sin ceros (RI-21)": "ck_dba_1",
    "código de DBA con un área distinta de la de su fila (RI-21)": "ck_dba_1",
    "código de DBA con un grado distinto del de su fila (RI-21)": "ck_dba_1",
    "código de DBA en minúsculas (RI-21)": "ck_dba_1",
    "código de DBA con número 00 (RI-21)": "ck_dba_1",
    # la columna es ASCII: MySQL rechaza la tilde por el tipo, antes del CHECK
    "código de área con tilde (ADR-036)": "Incorrect string value.*codigo_area",
    "código de área en minúsculas (ADR-036)": "ck_area_1",
    "grado con un nivel que no es el de la Ley 115 (ADR-036)": "ck_grado_1",
    "grado 12, fuera de la educación básica y media": "ck_grado_1",
    "la misma versión del documento de un área, cargada dos veces (ADR-033)":
        "uq_documento_oficial_1",
    "borrar un área que tiene DBA y documento (RESTRICT)": "fk_documento_oficial_1|fk_dba_1",
    "la misma cuenta de Google abriendo una segunda credencial (RF-01-04)": "uq_credencial_4",
    "proveedor fuera de alcance: Apple (RF-01-02)": "column 'proveedor'",
    "docente con nombres vacíos (RF-01-05)": "ck_docente_1",
    "borrar un docente que tiene credencial y experiencias (RESTRICT)":
        "fk_credencial_1|fk_experiencia_1",
    "código de invitación repetido (RI-3)": "uq_experiencia_1",
    "código de invitación repetido en minúsculas (RI-3)": "uq_experiencia_1",
    "código de invitación con carácter ambiguo 'O' (08-spec §2.3)": "ck_experiencia_2",
    "código de invitación de 5 caracteres": "ck_experiencia_2",
    "estado de experiencia inventado": "column 'estado'",
    "experiencia Publicada sin fecha de publicación (RI-16)": "ck_experiencia_1",
    "experiencia en Borrador con fecha de publicación (RI-16)": "ck_experiencia_1",
    "experiencia sin el servicio de IA que generó su banco (RI-17, RF-03-02)":
        "'servicio_ia' cannot be null",
    "servicio de IA fuera de ADR-030": "column 'servicio_ia'",
    "una experiencia incluye una evidencia de OTRO DBA (RI-18, ciclo C1)":
        "fk_experiencia_evidencia_1",
    "ítem sobre una evidencia que su experiencia NO incluye (H-4)": "fk_item_1",
    "formato de ítem inventado (ADR-006)": "column 'formato'",
    "origen de ítem inventado": "column 'origen'",
    "dictamen que admite formato cerrado sin decir cuál (RI-19)": "ck_evidencia_dictamen_1",
    "dictamen que no admite formato cerrado y aun así fija uno (RI-19)":
        "ck_evidencia_dictamen_1",
    "número de evidencia igual a 0": "ck_evidencia_1",
    "borrar una evidencia oficial que una experiencia usa (RESTRICT)":
        "fk_experiencia_evidencia_2",
    "el mismo estudiante inscrito dos veces en la misma experiencia (RI-1)": "uq_inscripcion_1",
    "presentar a la inscripción de la experiencia 1 un ítem de la experiencia 2, "
    "declarando la 1 (RI-13)": "fk_presentacion_2",
    "lo mismo, declarando la 2 (RI-13: ninguna combinación pasa)": "fk_presentacion_1",
    "orden de presentación igual a 0 (RI-8)": "ck_presentacion_1",
    "dos presentaciones con el mismo orden en una inscripción (RI-8)": "uq_presentacion_1",
    "respuesta a un ítem que no se le presentó (H-3)": "fk_respuesta_1",
    "segunda respuesta a la misma presentación": "uq_respuesta_1",
    "certeza fuera de la escala CRI 0-5 (ADR-008)": "ck_respuesta_1",
    "la respuesta al ítem 1 elige una opción del ítem 2, declarando el ítem 1 "
    "(RI-6, ciclo C4)": "fk_respuesta_opcion_2",
    "lo mismo, declarando el ítem 2 (RI-6: ninguna combinación pasa)": "fk_respuesta_opcion_1",
    "estado de resultado inventado (ADR-022)": "column 'estado'",
    "resultado cuya experiencia no es la de su inscripción (RI-13)": "fk_resultado_1",
    "resultado sobre una evidencia que esa experiencia no incluye": "fk_resultado_2",
}
_sin_motivo = [p[1] for p in PRUEBAS if p[0] == "FALLA" and p[1] not in MOTIVO_MYSQL]
assert not _sin_motivo, f"FALLA sin MOTIVO_MYSQL: {_sin_motivo}"
