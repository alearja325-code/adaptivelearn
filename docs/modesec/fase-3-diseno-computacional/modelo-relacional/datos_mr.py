"""Fuente unica del Modelo Relacional (17) y del Diccionario de Datos (18).

MODESEC pide en la Fase III un MER, "un MR (Modelo relacional) basado en
el MER y un diccionario de datos para los metadatos (como tipos, tamanos,
y otras cualidades de los campos de datos)". Este archivo es la fuente de
los dos ultimos; `generar.py` escribe desde aqui el diccionario, el DBML,
el SQL de verificacion (SQLite) y el SQL de produccion (MySQL).

Base: el MER final de la Fase III (`16-modelo-entidad-relacion.md`, que
sale de `../mer/datos_mer.py`). `_verificar_mr_mer.py` comprueba que esta
fuente no se aparte de el.

Parte del borrador del 2026-09-19 (carpeta "Entregables ... antes de la
finalizacion de la fase 2") y lo lleva a la Fase II cerrada:
  * tabla `credencial` (V-8) -- la misma que el incremento I1 ya construyo;
  * `docente`/`estudiante`: nombres + apellidos; el correo pasa a credencial;
  * `item`: origen con 3 valores; sale estado_revision;
  * `experiencia`: servicio_ia y modelo_ia del banco (RF-03-02: un solo
    servicio por banco), en vez de repetirlos en cada item (RI-17);
  * `experiencia_evidencia`: sale `incluida`;
  * `presentacion`: lleva id_experiencia y FK compuestas, como `resultado`
    -- cierra el hueco que el borrador dejo declarado (RI-13);
  * `evidencia_dictamen`: formato, el que la evidencia admite (RI-19);
  * `experiencia_evidencia` y `respuesta_opcion`: llaves foraneas compuestas
    que cierran los ciclos C1 (RI-18) y C4 (RI-6) del MER;
  * V-11: borrar una experiencia o salir de una borra en cascada todo lo
    que depende de ella (RF-02-07, RF-04-12).

Cambios del 2026-10-26 (revision del docente del 2026-10-22, R1 y R3):
  * tablas `area`, `grado` y `documento_oficial` (ADR-036); `dba` pierde
    `area` y `grado` como texto y gana tres FK. La de su documento es
    compuesta con codigo_area: cierra el ciclo C6 del MER (RI-20), con la
    misma tecnica que C1 a C4;
  * `codigo_dba` pasa a AREA-GG-NN (ADR-036), con un CHECK que lo arma con
    el area y el grado de la fila (RI-21). Los codigos se guardan en ASCII
    con cotejamiento binario: una tilde no cabe y una minuscula no es igual
    a una mayuscula. Decision de esta sesion, declarada en `17`;
  * `credencial.estado_verificacion` (procesando | verificado) reemplaza a
    `email_verificado` (ADR-037), y RI-15 se reescribe con el estado.

Cambios del 2026-10-27 (encargo 03; ADR-039, ADR-040, nota R4):
  * tabla `codigo_verificacion` (ADR-039): el codigo deja la credencial.
    PK (id_credencial, proposito): a lo sumo un codigo por credencial y
    proposito. Se guarda un HMAC-SHA256 del codigo, no el codigo (decision
    de esta sesion, declarada en `17`). `credencial` pierde
    codigo_verificacion, codigo_expira_en, codigo_ultimo_envio e
    intentos_codigo;
  * `credencial.es_admin` (ADR-040): la marca de administrador de la guia
    del docente, falsa por defecto, que solo se pone por SQL;
  * `credencial.nombre_completo`: el `fullName` que la guia pide al
    registrarse, guardado mientras no hay rol. Columna solo del MR,
    justificada en `_verificar_mr_mer.py` (decision de esta sesion).

MOTOR OBJETIVO: MySQL 8 (RNF-14: "NestJS y MySQL"). El DDL generado no usa
nada que MariaDB 10.11 no tenga, para que el backend de I1, que hoy corre
sobre MariaDB, lo acepte igual. La columna `sqlite` es el equivalente para
`mr_esquema.sql`, que existe para la verificacion mecanica.
"""

# ---------------------------------------------------------------- campos
# Campo: (nombre, mysql, sqlite, nulo, llave, dominio, defecto,
#         descripcion, fuente)
#   llave: "PK" | "PK,FK" | "FK" | "UNIQUE" | ""
#   nulo:  True = admite NULL

def c(nombre, mysql, sqlite, nulo, llave, dominio, defecto, desc, fuente):
    return dict(nombre=nombre, mysql=mysql, sqlite=sqlite, nulo=nulo,
                llave=llave, dominio=dominio, defecto=defecto, desc=desc,
                fuente=fuente)


ID = "INT UNSIGNED"          # llave sustituta, AUTO_INCREMENT
CORREO = "VARCHAR(254)"      # maximo de una direccion de correo, RFC 5321
URL = "VARCHAR(500)"
NOMBRE_PERSONA = "VARCHAR(120)"
# Codigos del catalogo (ADR-036): ASCII con cotejamiento binario. ASCII hace
# que una tilde no se pueda guardar (es justo lo que ADR-036 quita), y el
# cotejamiento binario, que "mat" no sea igual a "MAT". Toda columna que
# guarda un codigo usa el mismo tipo: una FK exige tipos iguales.
CODIGO = "CHARACTER SET ascii COLLATE ascii_bin"
COD_DBA = f"VARCHAR(9) {CODIGO}"      # AREA-GG-NN, ej. "MAT-08-03" o "CN-11-02"
COD_AREA = f"VARCHAR(3) {CODIGO}"     # MAT | LEN | CN | CS
FECHA = "DATETIME"

TABLAS = [
    # ---------------------------------------------------------------- 1
    dict(tabla="credencial", entidad="Credencial", clase="propia",
         desc="La cuenta de acceso: con qué correo y qué método se entra, la "
              "verificación del correo y a qué rol da acceso. Existe desde "
              "«Crear cuenta», antes de que exista la fila de docente o de "
              "estudiante, que se crea al elegir el rol (ventana 017). Es la "
              "tabla que el incremento I1 ya construyó (`backend/sql/`).",
         campos=[
             c("id_credencial", f"{ID} AUTO_INCREMENT", "INTEGER", False, "PK",
               "", "", "Identificador interno.", "MER · Credencial"),
             c("id_docente", ID, "INTEGER", True, "FK",
               "", "NULL",
               "Docente al que da acceso. NULL mientras el registro está en curso "
               "o si el rol es estudiante. Nunca a la vez que `id_estudiante` (RI-12).",
               "MER · relación «accede como» · 20-spec-auth-elige-rol.md"),
             c("id_estudiante", ID, "INTEGER", True, "FK",
               "", "NULL", "Estudiante al que da acceso. Mismas reglas que `id_docente`.",
               "MER · relación «accede como» · 20-spec-auth-elige-rol.md"),
             c("correo", CORREO, "TEXT COLLATE NOCASE", False, "UNIQUE",
               "formato de correo", "",
               "Correo de la cuenta. Único entre los dos roles: no hay dos cuentas "
               "con el mismo correo, ni con métodos distintos (RF-01-04).",
               "RI-3 · RF-01-04 · 17-spec-auth-login-registro.md"),
             c("proveedor", "ENUM('correo','google','microsoft')", "TEXT", False, "",
               "correo | google | microsoft", "",
               "Método con el que se creó la cuenta. No se vinculan métodos: se avisa "
               "cuál usar (RF-01-04). Sin Apple.",
               "RF-01-01 · RF-01-02 · 17-spec-auth-login-registro.md §2.8"),
             c("password_hash", "VARCHAR(255)", "TEXT", True, "",
               "hash de contraseña", "NULL",
               "Contraseña con función de hash; nunca en texto legible (RNF-08). "
               "NULL si la cuenta entra con Google o Microsoft (RI-15).",
               "RNF-08 · RF-01-01 · 26-spec-modal-mi-perfil.md"),
             c("proveedor_id", "VARCHAR(255)", "TEXT", True, "",
               "", "NULL",
               "Identificador de la persona en Google o Microsoft. NULL si "
               "`proveedor` es `correo` (RI-15).",
               "RF-01-02"),
             c("estado_verificacion", "ENUM('procesando','verificado')", "TEXT", False, "",
               "procesando | verificado", "'procesando'",
               "`procesando`: se envió el código y todavía no se confirma. `verificado`: "
               "se confirmó con el código. Con Google o Microsoft nace `verificado`: lo "
               "verificó el proveedor (RI-15). Reemplaza al antiguo sí/no "
               "`email_verificado`.",
               "ADR-037 · RF-01-03 · 18-spec-auth-verifica-correo.md"),
             c("es_admin", "BOOLEAN", "INTEGER", False, "",
               "0 | 1", "0",
               "Marca de administrador de la guía del docente: da acceso a `/users`. "
               "Falsa por defecto; solo se pone por SQL, ninguna ruta la asigna. No es "
               "un rol del producto: ninguna pantalla la usa.",
               "ADR-040 · guía JWT del docente v2, prueba 4"),
             c("nombre_completo", "VARCHAR(240)", "TEXT", True, "",
               "", "NULL",
               "El nombre que la persona escribió al registrarse (`fullName` de la "
               "guía). Sirve para mostrarla y para proponer nombres y apellidos al "
               "completar el perfil; los nombres oficiales viven en `docente` o "
               "`estudiante` (ventana 016).",
               "ADR-040 · guía JWT del docente v2, §2 · 19-spec-auth-completa-perfil.md"),
             c("intentos_login", "TINYINT UNSIGNED", "INTEGER", False, "",
               ">= 0", "0", "Intentos de inicio de sesión fallidos seguidos.",
               "RF-01-07 · backend I1, sql/002 · encargo 03"),
             c("bloqueado_hasta", FECHA, "TEXT", True, "",
               "", "NULL", "Si se superó el límite de intentos (5), hasta cuándo no se "
               "admite iniciar sesión (15 minutos).", "RF-01-07 · backend I1, sql/002"),
             c("creado_en", FECHA, "TEXT", False, "",
               "", "CURRENT_TIMESTAMP", "Cuándo se creó la cuenta.",
               "MER · Credencial · backend I1"),
             c("actualizado_en", FECHA, "TEXT", False, "",
               "", "CURRENT_TIMESTAMP",
               "Última modificación. En MySQL se actualiza sola (ON UPDATE).",
               "backend I1, sql/002"),
         ]),
    # --------------------------------------------------------------- 1b
    dict(tabla="codigo_verificacion", entidad="Codigo_Verificacion", clase="propia debil",
         desc="El código de 6 dígitos que se envía por correo para verificar la "
              "cuenta (ventana 015) o para recuperar la contraseña (ventana 018). "
              "Entidad débil de la credencial: a lo sumo uno por credencial y "
              "propósito; uno nuevo reemplaza al anterior. El vencimiento (10 min) "
              "y la espera para reenviar (30 s) se calculan desde `creado_en`. "
              "La tarea nocturna borra los vencidos (ADR-039).",
         campos=[
             c("id_credencial", ID, "INTEGER", False, "PK,FK",
               "", "", "Credencial que lo recibió. Relación identificadora «recibe».",
               "MER · relación «recibe» · ADR-039"),
             c("proposito", "ENUM('verificar_correo','recuperar_contrasena')", "TEXT",
               False, "PK", "verificar_correo | recuperar_contrasena", "",
               "Para qué es el código. Llave parcial: un código vigente por propósito.",
               "ADR-039 · RF-01-03 · RF-01-08"),
             c("codigo_hash", f"CHAR(64) {CODIGO}", "TEXT", False, "",
               "64 caracteres hexadecimales", "",
               "HMAC-SHA256 del código, en hexadecimal. El código nunca se guarda "
               "legible: quien lea la tabla no puede usarlo (RNF-08).",
               "ADR-039 · RNF-08"),
             c("creado_en", FECHA, "TEXT", False, "",
               "", "CURRENT_TIMESTAMP",
               "Cuándo se envió. Vence a los 10 minutos y se puede reenviar a los "
               "30 segundos: los dos se calculan desde aquí, no se guardan.",
               "ADR-039 · nota R4 · RF-01-03"),
             c("intentos", "TINYINT UNSIGNED", "INTEGER", False, "",
               "0 a 5", "0",
               "Intentos fallidos con este código. Al quinto, el código deja de "
               "servir y hay que pedir otro (fuerza bruta: RNF-07).",
               "ADR-039 · RNF-07"),
         ]),
    # ---------------------------------------------------------------- 2
    dict(tabla="docente", entidad="Docente", clase="propia",
         desc="Quien crea y publica experiencias. Se crea al elegir el rol "
              "Docente (ventana 017); el rol no cambia después.",
         campos=[
             c("id_docente", f"{ID} AUTO_INCREMENT", "INTEGER", False, "PK",
               "", "", "Identificador interno.", "MER · Docente"),
             c("nombres", NOMBRE_PERSONA, "TEXT", False, "",
               "no vacío", "", "Nombres. Obligatorio.",
               "RF-01-05 · 19-spec-auth-completa-perfil.md §2.3"),
             c("apellidos", NOMBRE_PERSONA, "TEXT", False, "",
               "no vacío", "", "Apellidos. Obligatorio.",
               "RF-01-05 · 19-spec-auth-completa-perfil.md §2.4"),
             c("avatar_url", URL, "TEXT", True, "",
               "JPG o PNG, ≤ 5 MB", "NULL",
               "Foto de perfil; opcional. Se reemplaza, no se quita (ventana 026).",
               "RF-01-05 · RF-01-11 · 26-spec-modal-mi-perfil.md"),
         ]),
    # ---------------------------------------------------------------- 3
    dict(tabla="estudiante", entidad="Estudiante", clase="propia",
         desc="Quien se une a una experiencia y responde el diagnóstico. Solo "
              "los datos mínimos (ADR-029): nombres, apellidos, foto opcional; "
              "el correo está en su credencial.",
         campos=[
             c("id_estudiante", f"{ID} AUTO_INCREMENT", "INTEGER", False, "PK",
               "", "", "Identificador interno.", "MER · Estudiante"),
             c("nombres", NOMBRE_PERSONA, "TEXT", False, "",
               "no vacío", "", "Nombres. Obligatorio.", "RF-01-05 · ADR-029"),
             c("apellidos", NOMBRE_PERSONA, "TEXT", False, "",
               "no vacío", "", "Apellidos. Obligatorio.", "RF-01-05 · ADR-029"),
             c("avatar_url", URL, "TEXT", True, "",
               "JPG o PNG, ≤ 5 MB", "NULL", "Foto de perfil; opcional.",
               "RF-01-05 · ADR-029"),
         ]),
    # ---------------------------------------------------------------- 4
    dict(tabla="experiencia", entidad="Experiencia", clase="propia",
         desc="Un diagnóstico anclado a un único DBA, creado por un docente. "
              "Se guarda solo si su banco se generó completo (ADR-027).",
         campos=[
             c("id_experiencia", f"{ID} AUTO_INCREMENT", "INTEGER", False, "PK",
               "", "", "Identificador interno.", "MER · Experiencia"),
             c("id_docente", ID, "INTEGER", False, "FK",
               "", "", "Docente autor. Participación total: no existe experiencia sin autor.",
               "MER · relación «crea»"),
             c("codigo_dba", COD_DBA, "TEXT", False, "FK",
               "", "", "DBA al que se ancla. Una experiencia, un solo DBA.",
               "RF-02-02 · 06-spec-crear-experiencia-paso2.md"),
             c("nombre", "VARCHAR(160)", "TEXT", False, "",
               "no vacío", "",
               "Título; llega prellenado con el enunciado del DBA y es editable.",
               "RF-02-02 · 07-spec-crear-experiencia-paso3.md"),
             c("estado", "ENUM('Borrador','Publicada')", "TEXT", False, "",
               "Borrador | Publicada", "'Borrador'",
               "Borrador = el banco se puede editar. Publicada = banco congelado y "
               "visible para estudiantes. No hay vuelta atrás (ADR-026).",
               "RF-02-05 · ADR-026 · 04-spec-dashboard.md"),
             c("fecha_creacion", FECHA, "TEXT", False, "",
               "", "", "Cuándo se creó.", "RF-02-04 · 09-spec-vista-interna-marco.md"),
             c("fecha_publicacion", FECHA, "TEXT", True, "",
               "NULL ⇔ Borrador (RI-16)", "NULL",
               "Cuándo pasó a Publicada. NULL mientras siga en Borrador.",
               "RF-02-05 · 15-spec-modal-confirmar-publicar.md"),
             c("codigo_invitacion", "CHAR(6)", "TEXT COLLATE NOCASE", False, "UNIQUE",
               "6 caracteres, sin 0 O 1 I L", "",
               "Código para unirse. Se genera al crear la experiencia y se muestra "
               "solo cuando está publicada. Sin distinguir mayúsculas.",
               "RI-3 · RF-02-06 · 08-spec-unirse-codigo.md §2.3"),
             c("servicio_ia", "ENUM('gemini','deepseek')", "TEXT", False, "",
               "gemini | deepseek", "",
               "Servicio de IA que generó el banco: el principal, o el de respaldo si el "
               "principal falló. Un banco sale entero de un solo servicio (RF-03-02), así "
               "que es un dato del banco y no de cada ítem: el de un ítem de origen ia o "
               "editado_docente es este (RI-17). El docente no lo ve.",
               "RF-03-02 · RF-03-03 · ADR-030"),
             c("modelo_ia", "VARCHAR(80)", "TEXT", False, "",
               "", "", "Qué modelo de ese servicio generó el banco.",
               "RF-03-03 · ADR-030"),
         ]),
    # ---------------------------------------------------------------- 5
    dict(tabla="area", entidad="Área", clase="men",
         desc="Área del currículo con DBA en esta versión: las 4 de ADR-033. Dato de "
              "referencia, de solo lectura (SUB-06). Se carga con el catálogo.",
         campos=[
             c("codigo_area", COD_AREA, "TEXT", False, "PK",
               "MAT | LEN | CN | CS", "",
               "Código del área, sin tildes: Matemáticas `MAT`, Lenguaje `LEN`, Ciencias "
               "Naturales `CN`, Ciencias Sociales `CS`. Encabeza el código de cada DBA (RI-21).",
               "ADR-036 · ADR-033"),
             c("nombre", "VARCHAR(40)", "TEXT", False, "UNIQUE",
               "no vacío", "", "Nombre del área, como lo escribe el MEN.",
               "ADR-036 · 05-spec-crear-experiencia-paso1.md"),
         ]),
    # ---------------------------------------------------------------- 6
    dict(tabla="grado", entidad="Grado", clase="men",
         desc="Grado de la educación básica y media, de 1° a 11°. Sin Transición "
              "(ADR-033). Dato de referencia, de solo lectura.",
         campos=[
             c("numero", "TINYINT UNSIGNED", "INTEGER", False, "PK",
               "1 a 11", "", "Número del grado. Va, con dos cifras, en el código de cada DBA (RI-21).",
               "ADR-036 · ADR-033"),
             c("nombre", "VARCHAR(20)", "TEXT", False, "UNIQUE",
               "Primero a Undécimo", "", "Nombre del grado.", "ADR-036"),
             c("nivel", "ENUM('basica_primaria','basica_secundaria','media')", "TEXT", False, "",
               "basica_primaria | basica_secundaria | media", "",
               "Nivel de la educación formal: básica primaria (1° a 5°), básica secundaria "
               "(6° a 9°) o media (10° y 11°). Un CHECK lo ata al número.",
               "ADR-036 · Ley 115 de 1994"),
         ]),
    # ---------------------------------------------------------------- 7
    dict(tabla="documento_oficial", entidad="Documento_Oficial", clase="men",
         desc="El PDF del MEN del que se copiaron los DBA de un área. Uno por área en "
              "esta versión, con los datos que ADR-033 verificó contra los archivos "
              "oficiales: la versión se lee del documento, nunca del nombre del archivo.",
         campos=[
             c("id_documento", f"{ID} AUTO_INCREMENT", "INTEGER", False, "PK",
               "", "", "Identificador interno.", "MER · Documento_Oficial"),
             c("codigo_area", COD_AREA, "TEXT", False, "FK",
               "", "", "Área cuyos DBA trae el documento.", "MER · relación «es de» · ADR-036"),
             c("titulo", "VARCHAR(200)", "TEXT", False, "",
               "no vacío", "", "Título del documento.", "ADR-036"),
             c("version", "VARCHAR(10)", "TEXT", False, "",
               "como la escribe el documento, ej. `V.2`", "",
               "Versión que dice la portada del documento. Ciencias Sociales es `V.1` "
               "aunque su archivo se llame «v2» (ADR-033).",
               "ADR-033 · ADR-036"),
             c("anio", "SMALLINT UNSIGNED", "INTEGER", False, "",
               "", "", "Año de publicación. Los cuatro de esta versión, 2016.", "ADR-033"),
             c("paginas", "SMALLINT UNSIGNED", "INTEGER", False, "",
               "> 0", "", "Número de páginas del PDF oficial.", "ADR-033"),
             c("url_oficial", URL, "TEXT", False, "",
               "dirección en Colombia Aprende", "",
               "Dónde publica hoy el MEN ese documento.", "ADR-033 · ADR-036"),
         ]),
    # ---------------------------------------------------------------- 8
    dict(tabla="dba", entidad="DBA", clase="men",
         desc="Derecho Básico de Aprendizaje oficial del MEN. Dato externo, de "
              "solo lectura para los usuarios (SUB-06). El área y el grado ya no son "
              "texto: son llaves foráneas hacia `area` y `grado` (ADR-036).",
         campos=[
             c("codigo_dba", COD_DBA, "TEXT", False, "PK",
               "`ÁREA-GG-NN` (RI-21)", "",
               "Código del DBA: código del área, grado y número del DBA con dos cifras, "
               "sin tildes (`MAT-01-01`, `CS-11-05`). Se arma con el área, el grado y el "
               "`numero` de cada registro de `curriculo_men_normalizado.json`; reemplaza al "
               "identificador viejo (`matemáticas_1_dba_1` → `MAT-01-01`). Los datos de hoy "
               "repiten 13 identificadores: se corrige en la auditoría (A12), no aquí.",
               "ADR-036 · curriculo_men_normalizado.json · RF-06-01"),
             c("codigo_area", COD_AREA, "TEXT", False, "FK",
               "", "", "Área del DBA. Está también en la FK hacia su documento: obliga a "
               "que el documento sea de esta misma área (RI-20).",
               "MER · relación «pertenece a» · ADR-036"),
             c("numero_grado", "TINYINT UNSIGNED", "INTEGER", False, "FK",
               "", "", "Grado del DBA. Se llama `numero_grado` y no `numero` para no "
               "confundirlo con el número del DBA, que va al final del código.",
               "MER · relación «corresponde a» · ADR-036"),
             c("id_documento", ID, "INTEGER", False, "FK",
               "", "", "Documento oficial del que se copió.",
               "MER · relación «se copia de» · ADR-036"),
             c("enunciado", "TEXT", "TEXT", False, "",
               "", "", "Texto oficial, sin simplificar ni reescribir.", "RF-06-01"),
             c("ejemplo", "TEXT", "TEXT", True, "",
               "", "NULL",
               "Ejemplo oficial; se usa como contexto al generar el banco (ADR-011). "
               "Admite NULL mientras la normalización no lo tenga (QA-011).",
               "RF-06-01 · ADR-011 · QA-011"),
         ]),
    # ---------------------------------------------------------------- 9
    dict(tabla="evidencia", entidad="Evidencia", clase="men debil",
         desc="Evidencia de aprendizaje de un DBA. Entidad débil: no tiene "
              "identidad fuera de su DBA. Dato del MEN, sin juicio nuestro.",
         campos=[
             c("codigo_dba", COD_DBA, "TEXT", False, "PK,FK",
               "", "", "DBA al que pertenece. Relación identificadora.",
               "MER · Evidencia"),
             c("numero_evidencia", "TINYINT UNSIGNED", "INTEGER", False, "PK",
               "> 0", "",
               "Posición dentro de la lista de evidencias de ese DBA: es también el "
               "orden oficial en que se diagnostican (ADR-024).",
               "curriculo_men_normalizado.json · ADR-024"),
             c("enunciado", "TEXT", "TEXT", False, "",
               "", "", "Texto oficial de la evidencia.", "RF-06-01"),
         ]),
    # --------------------------------------------------------------- 10
    dict(tabla="evidencia_dictamen", entidad="Evidencia_Dictamen",
         clase="propia debil",
         desc="Nuestro juicio sobre una evidencia del MEN: si admite formato "
              "cerrado, y cuál. Separada de `evidencia` a propósito, para no mezclar "
              "contenido oficial con criterio propio (H-6).",
         campos=[
             c("codigo_dba", COD_DBA, "TEXT", False, "PK,FK",
               "", "", "Evidencia dictaminada (parte 1).", "H-6 · MER"),
             c("numero_evidencia", "TINYINT UNSIGNED", "INTEGER", False, "PK,FK",
               "", "", "Evidencia dictaminada (parte 2).", "H-6 · MER"),
             c("aplica_formato_cerrado", "BOOLEAN", "INTEGER", False, "",
               "true | false", "",
               "Si esta evidencia se puede diagnosticar con pregunta cerrada.",
               "RF-06-02 · ADR-006 · censo QA-014 pendiente"),
             c("formato", "ENUM('single_choice','matching','ordering')", "TEXT", True, "",
               "single_choice | matching | ordering", "NULL",
               "Qué formato cerrado admite: «el formato de los ítems lo determina la "
               "evidencia» (RF-03-01), y una pregunta propia se crea con él (RF-03-07). "
               "NULL si no admite formato cerrado (RI-19).",
               "RF-03-01 · RF-03-07 · ADR-006"),
             c("justificacion", "TEXT", "TEXT", True, "",
               "", "NULL", "Por qué se dictaminó así.", "H-6 · MER"),
             c("fecha_dictamen", FECHA, "TEXT", False, "",
               "", "",
               "Cuándo se dictaminó. Obligatoria porque el dictamen puede cambiar al cerrar QA-014.",
               "H-6 · MER · V-6"),
         ]),
    # --------------------------------------------------------------- 11
    dict(tabla="experiencia_evidencia", entidad="Experiencia_Evidencia",
         clase="asociativa",
         desc="Las evidencias que diagnostica esta experiencia: una fila por "
              "evidencia incluida, fijada al crearla (solo las que el dictamen "
              "admite, RI-5). Hace que Ítem y Resultado cuelguen de un solo "
              "camino al currículo (H-4).",
         campos=[
             c("id_experiencia", ID, "INTEGER", False, "PK,FK",
               "", "", "Experiencia (parte 1 de la llave).", "H-4 · MER"),
             c("codigo_dba", COD_DBA, "TEXT", False, "PK,FK",
               "", "", "Evidencia incluida (parte 2).", "H-4 · MER"),
             c("numero_evidencia", "TINYINT UNSIGNED", "INTEGER", False, "PK,FK",
               "", "", "Evidencia incluida (parte 3).", "H-4 · MER"),
         ]),
    # --------------------------------------------------------------- 12
    dict(tabla="inscripcion", entidad="Inscripción", clase="asociativa",
         desc="Un estudiante unido a una experiencia con su código. Llave propia "
              "(no compuesta) para que Presentación y Resultado no arrastren "
              "llave doble.",
         campos=[
             c("id_inscripcion", f"{ID} AUTO_INCREMENT", "INTEGER", False, "PK",
               "", "", "Identificador interno.", "MER · Inscripción"),
             c("id_estudiante", ID, "INTEGER", False, "FK",
               "", "", "Estudiante inscrito.", "MER · relación «realiza»"),
             c("id_experiencia", ID, "INTEGER", False, "FK",
               "", "", "Experiencia a la que se unió.", "MER · relación «pertenece a»"),
             c("fecha_union", FECHA, "TEXT", False, "",
               "", "", "Cuándo se unió con el código.", "RF-04-02 · 08-spec-unirse-codigo.md"),
         ]),
    # --------------------------------------------------------------- 13
    dict(tabla="item", entidad="Ítem", clase="propia",
         desc="Pregunta del banco de diagnóstico. La IA genera 12 por evidencia "
              "al crear la experiencia; el docente puede editarlas, descartarlas "
              "y agregar las suyas mientras esté en Borrador (ADR-026).",
         campos=[
             c("id_item", f"{ID} AUTO_INCREMENT", "INTEGER", False, "PK",
               "", "", "Identificador interno.", "MER · Ítem"),
             c("id_experiencia", ID, "INTEGER", False, "FK",
               "", "", "Parte 1 de la FK compuesta hacia experiencia_evidencia.",
               "H-4 · MER"),
             c("codigo_dba", COD_DBA, "TEXT", False, "FK",
               "", "", "Parte 2 de esa misma FK compuesta.", "H-4 · MER"),
             c("numero_evidencia", "TINYINT UNSIGNED", "INTEGER", False, "FK",
               "", "", "Parte 3 de esa misma FK compuesta.", "H-4 · MER"),
             c("enunciado", "TEXT", "TEXT", False, "",
               "", "", "Texto de la pregunta.", "ADR-014 · RF-03-05"),
             c("formato", "ENUM('single_choice','matching','ordering')", "TEXT",
               False, "", "single_choice | matching | ordering", "'single_choice'",
               "Cómo se responde: lo determina la evidencia.", "ADR-006 · RF-03-01"),
             c("origen", "ENUM('ia','editado_docente','creado_docente')", "TEXT",
               False, "", "ia | editado_docente | creado_docente", "'ia'",
               "Generado por IA, editado por el docente o creado por el docente. "
               "Editar uno generado lo pasa a `editado_docente`. Qué servicio y modelo "
               "lo generó está en su experiencia (RI-17).",
               "RF-03-03 · RF-03-05 · RF-03-07 · ADR-026"),
             c("excluido", "BOOLEAN", "INTEGER", False, "",
               "true | false", "FALSE",
               "«Descartar»: no se muestra a los estudiantes, pero sigue en el banco. "
               "Reversible.", "RF-03-06 · ADR-015"),
         ]),
    # --------------------------------------------------------------- 14
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
               "No se muestra ni se reporta (ADR-008).",
               "ADR-020"),
         ]),
    # --------------------------------------------------------------- 15
    dict(tabla="presentacion", entidad="Presentación", clase="propia debil",
         desc="El hecho de HABER MOSTRADO un ítem a un estudiante — distinto "
              "del de haberlo respondido. Una pregunta mostrada y sin responder "
              "se vuelve a mostrar al retomar (ADR-031).",
         campos=[
             c("id_inscripcion", ID, "INTEGER", False, "PK,FK",
               "", "", "A quién se le mostró (parte 1 de la llave).",
               "H-2/H-3 · MER"),
             c("id_item", ID, "INTEGER", False, "PK,FK",
               "", "", "Qué ítem se mostró (parte 2 de la llave).",
               "H-2/H-3 · MER"),
             c("id_experiencia", ID, "INTEGER", False, "FK",
               "", "",
               "COLUMNA REDUNDANTE DELIBERADA, igual que en `resultado`: está en "
               "las dos FK compuestas y obliga a que el ítem sea de la misma "
               "experiencia que la inscripción (RI-13). Estructural, sin trigger.",
               "RI-13 · MER (Presentación) · cierra el hueco del borrador del MR"),
             c("orden_presentacion", "TINYINT UNSIGNED", "INTEGER", False, "",
               "> 0, único por inscripción (RI-8)", "",
               "Lugar en la secuencia completa del diagnóstico de esa inscripción. "
               "Reconstruye la secuencia adaptativa.",
               "RF-04-04 · RI-8 · ADR-016"),
             c("fecha_presentacion", FECHA, "TEXT", False, "",
               "", "", "Cuándo se mostró.", "RF-04-04 · H-2"),
         ]),
    # --------------------------------------------------------------- 16
    dict(tabla="respuesta", entidad="Respuesta", clase="asociativa",
         desc="Lo que el estudiante respondió a un ítem que se le presentó, con "
              "su certeza. Se guarda al confirmar la certeza, no al final "
              "(RF-04-06).",
         campos=[
             c("id_respuesta", f"{ID} AUTO_INCREMENT", "INTEGER", False, "PK",
               "", "", "Identificador interno.", "MER · Respuesta"),
             c("id_inscripcion", ID, "INTEGER", False, "FK",
               "", "", "Parte 1 de la FK compuesta hacia presentación.",
               "H-3 · MER"),
             c("id_item", ID, "INTEGER", False, "FK",
               "", "", "Parte 2 de esa misma FK compuesta.", "H-3 · MER"),
             c("certeza", "TINYINT UNSIGNED", "INTEGER", False, "",
               "0 a 5 (CRI)", "",
               "Certeza declarada (CRI, Hasan et al. 1999). De 3 a 5 es señal fuerte "
               "(RF-04-07).", "ADR-008 punto 2 · RF-04-05"),
             c("fecha_respuesta", FECHA, "TEXT", False, "",
               "", "", "Cuándo se confirmó.", "RF-04-06 · H-2"),
             c("correcta", "BOOLEAN", "INTEGER", False, "",
               "true | false", "",
               "DERIVADO Y PERSISTIDO (ADR-021). En emparejamiento y ordenamiento, "
               "verdadero solo si todos los pares o posiciones están bien.",
               "RF-04-06 · ADR-019 · ADR-021"),
         ]),
    # --------------------------------------------------------------- 17
    dict(tabla="respuesta_opcion", entidad="Respuesta_Opción",
         clase="asociativa",
         desc="Qué opción u opciones eligió el estudiante — no solo si acertó. "
              "Sin esta tabla, `matching` y `ordering` no son representables.",
         campos=[
             c("id_respuesta", ID, "INTEGER", False, "PK,FK",
               "", "", "Respuesta a la que pertenece (parte 1).", "ADR-019"),
             c("id_opcion", ID, "INTEGER", False, "PK,FK",
               "", "", "Opción elegida (parte 2).", "ADR-019"),
             c("id_item", ID, "INTEGER", False, "FK",
               "", "",
               "COLUMNA REDUNDANTE DELIBERADA, como id_experiencia en presentacion: está "
               "en las dos FK compuestas y obliga a que la opción elegida sea del ítem que "
               "se presentó (RI-6, ciclo C4 del MER). Estructural, sin trigger.",
               "RI-6 · ciclo C4 del MER"),
             c("valor_dado", "TINYINT UNSIGNED", "INTEGER", True, "",
               "según el formato del ítem", "NULL",
               "`single_choice`: NULL, la fila ya es la elección. `ordering`: la "
               "posición que le asignó. `matching`: el número de pareja.",
               "ADR-019"),
         ]),
    # --------------------------------------------------------------- 18
    dict(tabla="resultado", entidad="Resultado", clase="propia debil",
         desc="Lo que las respuestas de un estudiante permiten concluir sobre "
              "UNA evidencia DE ESTA experiencia. Fotografía del momento en que "
              "se concluyó, no recalculada al vuelo (RNF-11).",
         campos=[
             c("id_inscripcion", ID, "INTEGER", False, "PK,FK",
               "", "", "De quién es el resultado (parte 1 de la llave).",
               "MER · relación «arroja»"),
             c("id_experiencia", ID, "INTEGER", False, "FK",
               "", "",
               "COLUMNA REDUNDANTE DELIBERADA, que el MER delega al MR: permite que "
               "las dos reglas de coherencia sean estructurales (RI-13).",
               "MER · Resultado (delegación explícita al MR)"),
             c("codigo_dba", COD_DBA, "TEXT", False, "PK,FK",
               "", "", "Evidencia medida (parte 2 de la llave).", "H-4 · MER"),
             c("numero_evidencia", "TINYINT UNSIGNED", "INTEGER", False, "PK,FK",
               "", "", "Evidencia medida (parte 3 de la llave).", "H-4 · MER"),
             c("estado", "ENUM('muestra','no_muestra','no_concluyente')", "TEXT",
               False, "", "muestra | no_muestra | no_concluyente", "",
               "DERIVADO Y PERSISTIDO con la regla de RF-04-07 (cierra V-5). Nunca "
               "una certeza; nunca un valor que se edite a mano.",
               "RF-04-07 · ADR-016 · ADR-021"),
             c("fecha_calculo", FECHA, "TEXT", False, "",
               "", "", "Cuándo se concluyó. Una fotografía sin fecha no es auditable.",
               "ADR-021 · RNF-11"),
         ]),
]

# ------------------------------------------------------------------- FK
# (tabla, [columnas], tabla_destino, [columnas_destino], on_delete, razon
#  [, on_update])  -- on_update es CASCADE salvo que se diga otra cosa; al
# final del bloque se completa, asi que todas quedan con 7 elementos.
#
# Politica de borrado (cierra V-11): eliminar una experiencia (RF-02-07) o
# salir de una (RF-04-12) borra en cascada todo lo que depende de ella; las
# raices que ningun flujo borra (docente, estudiante, DBA, evidencia)
# quedan en RESTRICT, como seguro. Una credencial si se borra: la tarea
# nocturna borra las que quedaron sin terminar (ADR-039), y el
# administrador de la guia puede borrar un usuario (ADR-040); sus codigos
# se van con ella.
FKS = [
    ("codigo_verificacion", ["id_credencial"], "credencial", ["id_credencial"], "CASCADE",
     "Entidad débil: un código no existe sin su credencial. Borrar la credencial "
     "(tarea nocturna, ADR-039) borra sus códigos."),
    ("credencial", ["id_docente"], "docente", ["id_docente"], "RESTRICT",
     "Raíz: ningún flujo borra un docente. Sin ON UPDATE CASCADE: MySQL no admite "
     "un CHECK sobre una columna con acción referencial, y aquí lo hay (RI-12).",
     "RESTRICT"),
    ("credencial", ["id_estudiante"], "estudiante", ["id_estudiante"], "RESTRICT",
     "Igual que la anterior.", "RESTRICT"),
    ("experiencia", ["id_docente"], "docente", ["id_docente"], "RESTRICT",
     "Raíz: ningún flujo del sistema borra un docente."),
    ("experiencia", ["codigo_dba"], "dba", ["codigo_dba"], "RESTRICT",
     "Raíz: dato del MEN, no se borra por razones de este sistema."),
    # Catalogo (ADR-036): todo en RESTRICT, tambien al actualizar. Un codigo
    # del catalogo no cambia, y MySQL no admite un CHECK sobre una columna
    # con accion referencial: el de RI-21 lee codigo_area y numero_grado.
    ("documento_oficial", ["codigo_area"], "area", ["codigo_area"], "RESTRICT",
     "Raíz: el catálogo no se borra por razones de este sistema.", "RESTRICT"),
    ("dba", ["codigo_area"], "area", ["codigo_area"], "RESTRICT",
     "Raíz. Sin ON UPDATE CASCADE: el CHECK de RI-21 lee esta columna.", "RESTRICT"),
    ("dba", ["numero_grado"], "grado", ["numero"], "RESTRICT",
     "Raíz. Sin ON UPDATE CASCADE, por la misma razón.", "RESTRICT"),
    ("dba", ["id_documento", "codigo_area"], "documento_oficial",
     ["id_documento", "codigo_area"], "RESTRICT",
     "Compuesta con codigo_area: el documento del que se copió el DBA es de su misma "
     "área (RI-20, ciclo C6 del MER).", "RESTRICT"),
    ("evidencia", ["codigo_dba"], "dba", ["codigo_dba"], "CASCADE",
     "Entidad débil: sin su DBA no tiene identidad."),
    ("evidencia_dictamen", ["codigo_dba", "numero_evidencia"],
     "evidencia", ["codigo_dba", "numero_evidencia"], "CASCADE",
     "Entidad débil: el dictamen no existe sin la evidencia dictaminada."),
    ("experiencia_evidencia", ["id_experiencia", "codigo_dba"], "experiencia",
     ["id_experiencia", "codigo_dba"], "CASCADE",
     "Compuesta con codigo_dba: la evidencia incluida tiene que ser del DBA al que se "
     "ancla la experiencia (RI-18, ciclo C1 del MER). Eliminar la experiencia elimina "
     "sus evidencias incluidas (V-11)."),
    ("experiencia_evidencia", ["codigo_dba", "numero_evidencia"],
     "evidencia", ["codigo_dba", "numero_evidencia"], "RESTRICT",
     "Hacia el currículo del MEN: no se borra una evidencia oficial en uso."),
    ("inscripcion", ["id_estudiante"], "estudiante", ["id_estudiante"],
     "RESTRICT", "Raíz."),
    ("inscripcion", ["id_experiencia"], "experiencia", ["id_experiencia"],
     "CASCADE", "Eliminar la experiencia elimina a sus inscritos de ella (V-11, RF-02-07)."),
    ("item", ["id_experiencia", "codigo_dba", "numero_evidencia"],
     "experiencia_evidencia",
     ["id_experiencia", "codigo_dba", "numero_evidencia"], "CASCADE",
     "UNA sola FK compuesta: el ítem es de una evidencia que su experiencia incluye."),
    ("opcion", ["id_item"], "item", ["id_item"], "CASCADE",
     "Composición: una opción no existe sin su ítem."),
    ("presentacion", ["id_inscripcion", "id_experiencia"], "inscripcion",
     ["id_inscripcion", "id_experiencia"], "CASCADE",
     "Salir de la experiencia borra lo que se le presentó (V-11, RF-04-12). La "
     "columna compartida id_experiencia hace estructural RI-13."),
    ("presentacion", ["id_item", "id_experiencia"], "item",
     ["id_item", "id_experiencia"], "CASCADE",
     "El ítem presentado es de la misma experiencia (RI-13). CASCADE y no RESTRICT: "
     "un ítem solo desaparece cuando desaparece su experiencia entera (ADR-026: "
     "descartar no borra), y eso debe poder hacerse aunque tenga respuestas (RF-02-07)."),
    ("respuesta", ["id_inscripcion", "id_item"], "presentacion",
     ["id_inscripcion", "id_item"], "CASCADE",
     "Una respuesta sin presentación previa es imposible por estructura (H-3)."),
    ("respuesta_opcion", ["id_respuesta", "id_item"], "respuesta", ["id_respuesta", "id_item"],
     "CASCADE", "Sin la respuesta, la selección no tiene sentido. Compuesta con id_item: "
     "fija de qué ítem es la respuesta (RI-6)."),
    ("respuesta_opcion", ["id_opcion", "id_item"], "opcion", ["id_opcion", "id_item"], "CASCADE",
     "Compuesta con id_item: la opción elegida es del ítem que se presentó (RI-6, ciclo C4). "
     "CASCADE y no RESTRICT: una opción solo se borra editando un ítem en Borrador, "
     "cuando todavía no hay respuestas (ADR-026, RI-10), o al eliminar la "
     "experiencia entera, que debe poder hacerse (RF-02-07)."),
    ("resultado", ["id_inscripcion", "id_experiencia"], "inscripcion",
     ["id_inscripcion", "id_experiencia"], "CASCADE",
     "La experiencia del resultado es la de su inscripción (RI-13). Salir borra "
     "los resultados (V-11)."),
    ("resultado", ["id_experiencia", "codigo_dba", "numero_evidencia"],
     "experiencia_evidencia",
     ["id_experiencia", "codigo_dba", "numero_evidencia"], "CASCADE",
     "La evidencia medida es una que esa experiencia incluye. CASCADE para que "
     "eliminar la experiencia no quede bloqueado por sus resultados (V-11)."),
]

FKS = [fk if len(fk) == 7 else fk + ("CASCADE",) for fk in FKS]

# --------------------------------------------------------------- UNIQUE
UNICOS = [
    ("credencial", ["correo"], "RI-3 · RF-01-04: una cuenta por correo, entre los dos roles"),
    ("credencial", ["id_docente"], "una credencial por docente (1:1)"),
    ("credencial", ["id_estudiante"], "una credencial por estudiante (1:1)"),
    ("credencial", ["proveedor", "proveedor_id"],
     "RF-01-04: una misma cuenta de Google o Microsoft no abre dos credenciales"),
    ("experiencia", ["codigo_invitacion"], "RI-3"),
    ("area", ["nombre"], "dos áreas no se llaman igual"),
    ("grado", ["nombre"], "dos grados no se llaman igual"),
    ("documento_oficial", ["codigo_area", "version"],
     "una misma versión de un área se carga una sola vez (ADR-033, punto 4)"),
    ("documento_oficial", ["id_documento", "codigo_area"],
     "destino de FK: habilita la comprobación estructural de RI-20"),
    ("experiencia", ["id_experiencia", "codigo_dba"],
     "destino de FK: habilita la comprobación estructural de RI-18"),
    ("inscripcion", ["id_estudiante", "id_experiencia"], "RI-1"),
    ("inscripcion", ["id_inscripcion", "id_experiencia"],
     "destino de FK: habilita la comprobación estructural de RI-13"),
    ("item", ["id_item", "id_experiencia"],
     "destino de FK: habilita la comprobación estructural de RI-13"),
    ("presentacion", ["id_inscripcion", "orden_presentacion"], "RI-8"),
    ("respuesta", ["id_inscripcion", "id_item"], "una presentación, una respuesta"),
    ("respuesta", ["id_respuesta", "id_item"],
     "destino de FK: habilita la comprobación estructural de RI-6"),
    ("opcion", ["id_opcion", "id_item"],
     "destino de FK: habilita la comprobación estructural de RI-6"),
]

# ---------------------------------------------------------------- CHECK
# (tabla, expresion, descripcion, fuente). La expresion es SQL comun a
# SQLite y MySQL; si cambia por dialecto, va como dict {sqlite, mysql}.
_COD = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
CHECKS = [
    ("credencial", "id_docente IS NULL OR id_estudiante IS NULL",
     "una credencial accede como un solo rol", "RI-12 · 20-spec-auth-elige-rol.md"),
    ("credencial",
     "(proveedor = 'correo' AND password_hash IS NOT NULL AND proveedor_id IS NULL) OR "
     "(proveedor <> 'correo' AND password_hash IS NULL AND proveedor_id IS NOT NULL "
     "AND estado_verificacion = 'verificado')",
     "contraseña solo con correo; identificador externo y correo verificado solo "
     "con Google o Microsoft", "RI-15 · RF-01-01 · RF-01-02"),
    ("codigo_verificacion", "intentos <= 5",
     "a lo sumo 5 intentos fallidos por código", "ADR-039 · RNF-07"),
    ("codigo_verificacion",
     {"sqlite": "length(codigo_hash) = 64 AND codigo_hash NOT GLOB '*[^0-9a-f]*'",
      "mysql": "codigo_hash REGEXP '^[0-9a-f]{64}$'"},
     "el hash es hexadecimal de 64 caracteres: un código de 6 dígitos sin hash "
     "no cabe", "ADR-039 · RNF-08"),
    ("docente", "TRIM(nombres) <> '' AND TRIM(apellidos) <> ''",
     "nombres y apellidos no vacíos", "RF-01-05"),
    ("estudiante", "TRIM(nombres) <> '' AND TRIM(apellidos) <> ''",
     "nombres y apellidos no vacíos", "RF-01-05"),
    ("experiencia",
     "(estado = 'Borrador' AND fecha_publicacion IS NULL) OR "
     "(estado = 'Publicada' AND fecha_publicacion IS NOT NULL)",
     "fecha de publicación solo si está Publicada", "RI-16 · RF-02-05"),
    ("experiencia",
     {"sqlite": "length(codigo_invitacion) = 6 AND " + " AND ".join(
         f"substr(upper(codigo_invitacion),{i},1) GLOB '[{_COD}]'" for i in range(1, 7)),
      "mysql": f"codigo_invitacion REGEXP '^[{_COD}]{{6}}$'"},
     "6 caracteres de letras y números, sin 0 O 1 I L", "RI-3 · RF-02-06"),
    ("area",
     {"sqlite": "codigo_area GLOB '[A-Z][A-Z]' OR codigo_area GLOB '[A-Z][A-Z][A-Z]'",
      "mysql": "codigo_area REGEXP '^[A-Z]{2,3}$'"},
     "2 o 3 letras mayúsculas, sin tildes (en MySQL la columna es ASCII binaria: "
     "una tilde no cabe y el REGEXP distingue mayúsculas)", "ADR-036"),
    ("grado",
     "(numero BETWEEN 1 AND 5 AND nivel = 'basica_primaria') OR "
     "(numero BETWEEN 6 AND 9 AND nivel = 'basica_secundaria') OR "
     "(numero BETWEEN 10 AND 11 AND nivel = 'media')",
     "grados 1 a 11, sin Transición, y el nivel que les da la Ley 115",
     "ADR-036 · ADR-033 · Ley 115 de 1994"),
    ("documento_oficial", "paginas > 0 AND TRIM(titulo) <> '' AND TRIM(version) <> ''",
     "título y versión no vacíos; al menos una página", "ADR-036"),
    ("dba",
     {"sqlite": "codigo_dba = codigo_area || '-' || printf('%02d', numero_grado) || '-' "
                "|| substr(codigo_dba, -2) AND substr(codigo_dba, -2) GLOB '[0-9][0-9]' "
                "AND substr(codigo_dba, -2) <> '00'",
      "mysql": "codigo_dba = CONCAT(codigo_area, '-', LPAD(numero_grado, 2, '0'), '-', "
               "RIGHT(codigo_dba, 2)) AND RIGHT(codigo_dba, 2) REGEXP '^[0-9]{2}$' "
               "AND RIGHT(codigo_dba, 2) <> '00'"},
     "el código es ÁREA-GG-NN, con el área y el grado de la fila y un número de "
     "dos cifras desde 01", "RI-21 · ADR-036"),
    ("evidencia", "numero_evidencia > 0", "posición dentro del DBA", "MER"),
    ("evidencia_dictamen",
     "(aplica_formato_cerrado = 1 AND formato IS NOT NULL) OR "
     "(aplica_formato_cerrado = 0 AND formato IS NULL)",
     "si admite formato cerrado dice cuál; si no, no tiene formato", "RI-19 · RF-03-01"),
    ("presentacion", "orden_presentacion > 0", "orden desde 1", "RI-8"),
    ("respuesta", "certeza BETWEEN 0 AND 5", "escala CRI", "ADR-008 punto 2"),
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
