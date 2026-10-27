"""Prueba el esquema del MR contra un motor real, no leyendolo.

Reescrito el 2026-10-21 para el MER final de la Fase III (hoy, 18 tablas). Las
pruebas ya no viven aqui: estan en `pruebas_mr.py`, compartidas con
`probar_mysql.py`, que corre exactamente las mismas contra MySQL 8.

Tres bloques, en orden de fuerza creciente:

  A. El motor acepta el esquema. Una FK hacia una columna inexistente o
     una PK mal declarada hacen fallar esto sin que nadie lo note leyendo.
  B. Pruebas de VIOLACION. Por cada restriccion que este modelo declara
     "automatica", se intenta insertar el dato que la rompe. Si el motor
     lo acepta, la restriccion no existe de verdad -- diga lo que diga el
     documento. Aqui esta lo que distingue comprobar de afirmar. Tambien
     prueba en positivo (lo raro pero valido) y la politica de borrado.
  C. DBML contra SQL. Los dos artefactos describen lo mismo y podrian
     divergir; hoy salen del mismo generador, asi que esto comprueba que
     el generador no se contradiga a si mismo. Y que el esquema del backend
     (`backend/sql/001_esquema.sql`) sea el que el MR genera hoy: si alguien
     lo edita a mano, o cambia el MR sin regenerar, esto falla.

Uso:  python verificar_mr.py
"""
import os
import re
import sqlite3
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from datos_mr import TABLAS                                   # noqa: E402
from pruebas_mr import SEMILLA, PRUEBAS, CONTEOS               # noqa: E402

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
esperadas = {t["tabla"] for t in TABLAS}
chk(tablas == esperadas,
    f"{len(tablas)} tablas creadas, exactamente las del MR "
    f"(difieren: {tablas ^ esperadas or 'ninguna'})")

for t, h in [("credencial", "V-8"), ("experiencia_evidencia", "H-4"),
             ("evidencia_dictamen", "H-6"), ("presentacion", "H-2/H-3"),
             ("area", "R1 del 2026-10-22"), ("grado", "R1 del 2026-10-22"),
             ("documento_oficial", "ADR-036")]:
    chk(t in tablas, f"existe `{t}` — la tabla que responde a {h}")


# ------------------------------------------------------------------- B
print()
print("=" * 70)
print("B. Pruebas de violación, en positivo y de borrado")
print("=" * 70)


def base():
    cx = sqlite3.connect(":memory:")
    cx.execute("PRAGMA foreign_keys = ON")
    cx.executescript(open(SQL, encoding="utf-8").read())
    cx.executescript("\n".join(SEMILLA))
    return cx


try:
    base().close()
    chk(True, f"la semilla ({len(SEMILLA)} filas válidas) entra sin errores")
except sqlite3.Error as e:
    chk(False, f"la SEMILLA misma es rechazada: {e}")
    sys.exit(1)

for prueba in PRUEBAS:
    clase, nombre, sentencias = prueba[:3]
    cx = base()
    # En una FALLA solo la ULTIMA sentencia debe romper algo; las previas
    # preparan el caso y tienen que entrar. Sin esta separacion, un error
    # de preparacion contaria como "rechazo correcto".
    if clase == "FALLA" and len(sentencias) > 1:
        try:
            cx.executescript("\n".join(sentencias[:-1]))
        except sqlite3.Error as e:
            chk(False, f"[rechaza] {nombre} — falló la PREPARACIÓN: {e}")
            cx.close()
            continue
        sentencias = sentencias[-1:]
    try:
        cx.executescript("\n".join(sentencias))
        error = None
    except sqlite3.Error as e:
        error = e
    if clase == "FALLA":
        chk(error is not None, f"[rechaza] {nombre}"
            + ("" if error else " — el motor lo ACEPTÓ"))
    elif clase == "PASA":
        chk(error is None, f"[acepta]  {nombre}"
            + (f" — fue RECHAZADO: {error}" if error else ""))
    else:
        esperado = prueba[3]
        reales = {t: cx.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                  for t in CONTEOS}
        dif = {t: (reales[t], n) for t, n in esperado.items() if reales[t] != n}
        chk(error is None and not dif, f"[queda]   {nombre}"
            + (f" — error: {error}" if error else "")
            + (f" — difieren (real, esperado): {dif}" if dif else ""))
    cx.close()


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
# PRAGMA devuelve UNA FILA POR COLUMNA: las FK compuestas cuentan varias
# veces. Se cuentan los id distintos de FK, no las filas. Este mismo
# detalle produjo un falso positivo en una version anterior del script.
fks_sql = sum(len({r[0] for r in con.execute(f"PRAGMA foreign_key_list({t})")})
              for t in tablas)
chk(refs_dbml == fks_sql,
    f"mismas llaves foráneas: DBML={refs_dbml}, SQL={fks_sql}")

for t in sorted(tablas):
    cols_sql = {r[1] for r in con.execute(f"PRAGMA table_info({t})")}
    bloque = re.search(rf"^Table {t} \{{(.*?)^\}}", txt_dbml, re.M | re.S)
    # `indexes {` tambien empieza con 2 espacios y una palabra: sin
    # excluirlo, el bloque de PK compuesta se cuenta como una columna
    # llamada "indexes".
    cols_dbml = set(re.findall(r"^  (\w+) ", bloque.group(1), re.M)) - {"indexes"}
    if cols_sql != cols_dbml:
        chk(False, f"`{t}`: columnas difieren {cols_sql ^ cols_dbml}")
if not any("columnas difieren" in f for f in fallas):
    chk(True, "todas las tablas tienen las mismas columnas en DBML y SQL")

con.close()

import generar                                                # noqa: E402
txt_backend = (open(generar.SQL_BACKEND, encoding="utf-8").read()
               if os.path.exists(generar.SQL_BACKEND) else "")
chk(txt_backend == generar.sql_mysql(generar.TABLAS_BACKEND),
    "backend/sql/001_esquema.sql es el que el MR genera hoy "
    f"({len(generar.TABLAS_BACKEND)} tablas; si no, correr generar.py)")

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
