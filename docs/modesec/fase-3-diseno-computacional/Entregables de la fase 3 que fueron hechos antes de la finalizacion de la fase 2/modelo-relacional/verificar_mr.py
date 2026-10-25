"""Prueba el esquema del MR contra un motor real, no leyendolo.

Reescrito el 2026-09-19 para la QUINTA revision del MER. La version
anterior probaba el modelo de 11 tablas y por eso ya no servia: el
esquema tiene 14.

Tres bloques, en orden de fuerza creciente:

  A. El motor acepta el esquema. Una FK hacia una columna inexistente o
     una PK mal declarada hacen fallar esto sin que nadie lo note leyendo.
  B. Pruebas de VIOLACION. Por cada restriccion que este modelo declara
     "automatica", se intenta insertar el dato que la rompe. Si el motor
     lo acepta, la restriccion no existe de verdad -- diga lo que diga el
     documento. Aqui esta lo que distingue comprobar de afirmar.
  C. DBML contra SQL. Los dos artefactos describen lo mismo y podrian
     divergir; hoy salen del mismo generador, asi que esto comprueba que
     el generador no se contradiga a si mismo.

Uso:  python3 verificar_mr.py
"""
import os
import re
import sqlite3
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SQL = os.path.join(AQUI, "mr_esquema.sql")
DBML = os.path.join(AQUI, "mr_adaptivelearn.dbml")

ok = 0
fallas = []


def chk(cond, msg):
    global ok
    if cond:
        ok += 1
        print(f"   OK   {msg}")
    else:
        fallas.append(msg)
        print(f"   FALLA {msg}")


# ------------------------------------------------------------------- A
print("=" * 70)
print("A. El motor acepta el esquema")
print("=" * 70)

con = sqlite3.connect(":memory:")
con.execute("PRAGMA foreign_keys = ON")
try:
    con.executescript(open(SQL, encoding="utf-8").read())
    chk(True, "el esquema se ejecuta completo sin errores")
except sqlite3.Error as e:
    chk(False, f"el esquema NO se ejecuta: {e}")
    sys.exit(1)

tablas = {r[0] for r in con.execute(
    "SELECT name FROM sqlite_master WHERE type='table' "
    "AND name NOT LIKE 'sqlite_%'")}
chk(len(tablas) == 14, f"14 tablas creadas (hay {len(tablas)})")

esperadas = {"docente", "estudiante", "experiencia", "dba", "evidencia",
             "evidencia_dictamen", "experiencia_evidencia", "inscripcion",
             "item", "opcion", "presentacion", "respuesta",
             "respuesta_opcion", "resultado"}
chk(tablas == esperadas,
    f"las 14 son exactamente las del MER (faltan: {esperadas - tablas or 'ninguna'})")

# las 3 entidades que responden a la revision docente
for t, h in [("experiencia_evidencia", "H-4"), ("evidencia_dictamen", "H-6"),
             ("presentacion", "H-2/H-3")]:
    chk(t in tablas, f"existe `{t}` — la entidad que responde a {h}")


# ------------------------------------------------------------------- B
print()
print("=" * 70)
print("B. Pruebas de violacion (cada una DEBE ser rechazada)")
print("=" * 70)


def semilla(cx):
    """Un juego minimo de datos validos, sobre el que probar violaciones."""
    cx.executescript("""
    INSERT INTO docente VALUES (1,'Ana','ana@x.co',NULL);
    INSERT INTO estudiante VALUES (1,'Luis','luis@x.co',NULL);
    INSERT INTO dba VALUES ('mat_8_dba_1','Matematicas','8°','Enunciado','Ej');
    INSERT INTO evidencia VALUES ('mat_8_dba_1',1,'Evidencia 1');
    INSERT INTO evidencia_dictamen VALUES ('mat_8_dba_1',1,1,'porque si','2026-01-01');
    INSERT INTO experiencia VALUES (1,1,'mat_8_dba_1','Exp','Borrador','2026-01-01',NULL,'ABC234');
    INSERT INTO experiencia_evidencia VALUES (1,'mat_8_dba_1',1,1);
    INSERT INTO inscripcion VALUES (1,1,1,'2026-01-02');
    INSERT INTO item VALUES (1,1,'mat_8_dba_1',1,'Pregunta','single_choice','ia','sin_revisar',0);
    INSERT INTO opcion VALUES (1,1,'Opcion A',NULL,1,NULL,NULL);
    INSERT INTO presentacion VALUES (1,1,1,'2026-01-03');
    INSERT INTO respuesta VALUES (1,1,1,5,'2026-01-03',1);
    INSERT INTO respuesta_opcion VALUES (1,1,NULL);
    INSERT INTO resultado VALUES (1,1,'mat_8_dba_1',1,'muestra','2026-01-04');
    """)


def debe_fallar(nombre, sentencia):
    cx = sqlite3.connect(":memory:")
    cx.execute("PRAGMA foreign_keys = ON")
    cx.executescript(open(SQL, encoding="utf-8").read())
    semilla(cx)
    try:
        cx.executescript(sentencia)
        chk(False, f"{nombre} — el motor lo ACEPTO (no deberia)")
    except sqlite3.Error:
        chk(True, nombre)
    finally:
        cx.close()


def debe_pasar(nombre, sentencia):
    cx = sqlite3.connect(":memory:")
    cx.execute("PRAGMA foreign_keys = ON")
    cx.executescript(open(SQL, encoding="utf-8").read())
    semilla(cx)
    try:
        cx.executescript(sentencia)
        chk(True, nombre)
    except sqlite3.Error as e:
        chk(False, f"{nombre} — fue RECHAZADO: {e}")
    finally:
        cx.close()


# --- unicidad (RI-3, RI-1) ---
debe_fallar("correo de docente duplicado (RI-3)",
            "INSERT INTO docente VALUES (2,'Otra','ana@x.co',NULL);")
debe_fallar("correo de estudiante duplicado (RI-3)",
            "INSERT INTO estudiante VALUES (2,'Otro','luis@x.co',NULL);")
debe_fallar("codigo de invitacion duplicado (RI-3)",
            "INSERT INTO experiencia VALUES "
            "(2,1,'mat_8_dba_1','E2','Borrador','2026-01-01',NULL,'ABC234');")
debe_fallar("mismo estudiante inscrito dos veces (RI-1)",
            "INSERT INTO inscripcion VALUES (2,1,1,'2026-01-02');")

# --- dominios ---
debe_fallar("certeza fuera de la escala CRI 0-5 (ADR-008)",
            "INSERT INTO presentacion VALUES (1,1,2,'2026-01-03');"
            "INSERT INTO respuesta VALUES (2,1,1,9,'2026-01-03',1);")
debe_fallar("codigo de invitacion con caracter ambiguo 'O' (08-spec §2.3)",
            "INSERT INTO experiencia VALUES "
            "(3,1,'mat_8_dba_1','E3','Borrador','2026-01-01',NULL,'ABCO34');")
debe_fallar("codigo de invitacion de 5 caracteres",
            "INSERT INTO experiencia VALUES "
            "(4,1,'mat_8_dba_1','E4','Borrador','2026-01-01',NULL,'ABC23');")
debe_fallar("estado de experiencia inventado",
            "INSERT INTO experiencia VALUES "
            "(5,1,'mat_8_dba_1','E5','Archivada','2026-01-01',NULL,'ABC235');")
debe_fallar("formato de item inventado (ADR-006)",
            "INSERT INTO item VALUES "
            "(2,1,'mat_8_dba_1',1,'P','ensayo','ia','sin_revisar',0);")
debe_fallar("origen de item inventado (H-5)",
            "INSERT INTO item VALUES "
            "(3,1,'mat_8_dba_1',1,'P','single_choice','chatgpt','sin_revisar',0);")
debe_fallar("estado de resultado inventado (ADR-008 punto 4)",
            "INSERT INTO resultado VALUES "
            "(1,1,'mat_8_dba_1',1,'aprobado','2026-01-04');")
debe_fallar("numero_evidencia igual a 0",
            "INSERT INTO evidencia VALUES ('mat_8_dba_1',0,'Cero');")
debe_fallar("orden_presentacion igual a 0 (RI-8)",
            "INSERT INTO item VALUES "
            "(9,1,'mat_8_dba_1',1,'P','single_choice','ia','sin_revisar',0);"
            "INSERT INTO presentacion VALUES (1,9,0,'2026-01-03');")

# --- integridad referencial ---
debe_fallar("item que apunta a una evidencia que la experiencia NO incluye (H-4)",
            "INSERT INTO evidencia VALUES ('mat_8_dba_1',2,'Evidencia 2');"
            "INSERT INTO item VALUES "
            "(4,1,'mat_8_dba_1',2,'P','single_choice','ia','sin_revisar',0);")
debe_fallar("respuesta sin presentacion previa (H-3)",
            "INSERT INTO item VALUES "
            "(5,1,'mat_8_dba_1',1,'P','single_choice','ia','sin_revisar',0);"
            "INSERT INTO respuesta VALUES (3,1,5,3,'2026-01-03',1);")
debe_fallar("borrar un item que ya se le presento a un estudiante (RI-10)",
            "DELETE FROM item WHERE id_item = 1;")
debe_fallar("borrar una opcion que un estudiante ya eligio",
            "DELETE FROM opcion WHERE id_opcion = 1;")
debe_fallar("borrar un docente que tiene experiencias",
            "DELETE FROM docente WHERE id_docente = 1;")

# --- las dos garantias nuevas de esta revision ---
debe_fallar("resultado cuya experiencia NO es la de su inscripcion "
            "(la vieja RI-2, ahora estructural)",
            "INSERT INTO experiencia VALUES "
            "(6,1,'mat_8_dba_1','E6','Borrador','2026-01-01',NULL,'ABC236');"
            "INSERT INTO experiencia_evidencia VALUES (6,'mat_8_dba_1',1,1);"
            "INSERT INTO resultado VALUES "
            "(1,6,'mat_8_dba_1',1,'muestra','2026-01-04');")
debe_fallar("resultado sobre una evidencia que esa experiencia no incluye",
            "INSERT INTO evidencia VALUES ('mat_8_dba_1',3,'Evidencia 3');"
            "INSERT INTO resultado VALUES "
            "(1,1,'mat_8_dba_1',3,'muestra','2026-01-04');")

# --- en positivo: lo que SI debe poder pasar ---
debe_pasar("una presentacion SIN respuesta — 'se le mostro y no respondio' (H-3)",
           "INSERT INTO item VALUES "
           "(6,1,'mat_8_dba_1',1,'P','single_choice','ia','sin_revisar',0);"
           "INSERT INTO presentacion VALUES (1,6,2,'2026-01-03');")
debe_pasar("borrar una experiencia arrastra sus inscripciones e inclusiones",
           "DELETE FROM respuesta_opcion; DELETE FROM respuesta;"
           "DELETE FROM resultado; DELETE FROM presentacion;"
           "DELETE FROM experiencia WHERE id_experiencia = 1;")


# ------------------------------------------------------------------- C
print()
print("=" * 70)
print("C. DBML contra SQL — los dos artefactos describen lo mismo")
print("=" * 70)

txt_dbml = open(DBML, encoding="utf-8").read()
tablas_dbml = set(re.findall(r"^Table (\w+) \{", txt_dbml, re.M))
chk(tablas_dbml == tablas,
    f"mismas tablas en DBML y SQL (difieren: "
    f"{tablas_dbml ^ tablas or 'ninguna'})")

refs_dbml = len(re.findall(r"^Ref: ", txt_dbml, re.M))
fks_sql = sum(len(list(con.execute(f"PRAGMA foreign_key_list({t})")))
              for t in tablas)
# PRAGMA devuelve UNA FILA POR COLUMNA: las FK compuestas cuentan varias
# veces. Este mismo detalle produjo un falso positivo en la version
# anterior de este script, y quedo anotado en el MR.
fks_compuestas = sum(1 for t in tablas
                     for r in con.execute(f"PRAGMA foreign_key_list({t})")
                     if r[1] > 0)
fks_reales = fks_sql - fks_compuestas
chk(refs_dbml == fks_reales,
    f"mismas llaves foraneas: DBML={refs_dbml}, SQL={fks_reales}")

for t in sorted(tablas):
    cols_sql = {r[1] for r in con.execute(f"PRAGMA table_info({t})")}
    bloque = re.search(rf"^Table {t} \{{(.*?)^\}}", txt_dbml, re.M | re.S)
    # `indexes {` tambien empieza con 2 espacios y una palabra: sin
    # excluirlo, el bloque de PK compuesta se cuenta como una columna
    # llamada "indexes". Ese fue el primer resultado de este script, y el
    # error estaba aqui, no en el modelo -- misma leccion que ya dejo
    # anotada la version anterior del verificador.
    cols_dbml = set(re.findall(r"^  (\w+) ", bloque.group(1), re.M)) - {"indexes"}
    if cols_sql != cols_dbml:
        chk(False, f"`{t}`: columnas difieren {cols_sql ^ cols_dbml}")
if not any("columnas difieren" in f for f in fallas):
    chk(True, "todas las tablas tienen las mismas columnas en DBML y SQL")

con.close()

# ------------------------------------------------------------------- --
print()
print("=" * 70)
if fallas:
    print(f"RESULTADO: {ok} correctas, {len(fallas)} FALLAS")
    for f in fallas:
        print(f"   · {f}")
    sys.exit(1)
print(f"RESULTADO: {ok} comprobaciones, todas correctas.")
print("=" * 70)
