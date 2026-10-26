"""Corre la bateria de `pruebas_mr.py` contra un MySQL 8 real.

`verificar_mr.py` prueba el esquema en SQLite, que no es el motor de
produccion. Este script cierra esa distancia: crea una base de prueba,
carga `mr_mysql.sql` tal cual se entregaria, y le aplica las mismas
pruebas. Cada prueba corre dentro de una transaccion que se deshace, asi
que todas parten de la misma semilla.

Usa el cliente `mysql` de linea de comandos, sin dependencias de Python.
Las credenciales van en un archivo de opciones de MySQL (nunca en la
linea de comandos ni en este script):

    [client]
    user=...
    password=...
    host=127.0.0.1
    port=3306

Uso:
    python probar_mysql.py --cnf RUTA\\cliente.cnf [--mysql RUTA\\mysql.exe]

La base de prueba (`adaptivelearn_verificacion_mr`) se crea al empezar y
se borra al terminar. Si ya existe, el script se detiene sin tocarla.
"""
import argparse
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from datos_mr import TABLAS, FKS, CHECKS                       # noqa: E402
from pruebas_mr import SEMILLA, PRUEBAS, CONTEOS, MOTIVO_MYSQL # noqa: E402

DDL = os.path.join(AQUI, "mr_mysql.sql")
BASE = "adaptivelearn_verificacion_mr"

ap = argparse.ArgumentParser()
ap.add_argument("--cnf", required=True, help="archivo de opciones con [client]")
ap.add_argument("--mysql", default="mysql", help="ruta del cliente mysql")
args = ap.parse_args()

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


def mysql(sql, base=None):
    cmd = [args.mysql, f"--defaults-extra-file={args.cnf}",
           "--default-character-set=utf8mb4", "-N", "-B"]
    if base:
        cmd.append(base)
    r = subprocess.run(cmd, input=sql.encode("utf-8"), capture_output=True)
    return (r.returncode, r.stdout.decode("utf-8", "replace"),
            r.stderr.decode("utf-8", "replace").strip())


def error_corto(stderr):
    lineas = [x for x in stderr.splitlines() if x.startswith("ERROR")]
    return lineas[0] if lineas else stderr[:160]


# ------------------------------------------------------------------- 0
rc, out, err = mysql("SELECT VERSION(), @@sql_mode;")
if rc:
    sys.exit(f"No se pudo conectar con MySQL: {error_corto(err)}")
version, modo = out.strip().split("\t")
print("=" * 70)
print(f"Servidor: MySQL {version}")
print(f"sql_mode: {modo}")
print("=" * 70)

rc, out, _ = mysql(f"SELECT COUNT(*) FROM information_schema.SCHEMATA "
                   f"WHERE SCHEMA_NAME = '{BASE}';")
if out.strip() != "0":
    sys.exit(f"La base `{BASE}` ya existe; no se toca. Bórrela a mano si es "
             f"de una corrida anterior interrumpida.")

try:
    # --------------------------------------------------------------- A
    print("A. El motor acepta el esquema de producción")
    print("=" * 70)
    mysql(f"CREATE DATABASE {BASE} CHARACTER SET utf8mb4 "
          f"COLLATE utf8mb4_unicode_ci;")
    rc, _, err = mysql(open(DDL, encoding="utf-8").read(), BASE)
    chk(rc == 0, "mr_mysql.sql se ejecuta completo sin errores"
        + (f" — {error_corto(err)}" if rc else ""))
    if rc:
        raise SystemExit(1)

    def cuenta(sql):
        return int(mysql(sql)[1].strip())

    n = cuenta(f"SELECT COUNT(*) FROM information_schema.TABLES "
               f"WHERE TABLE_SCHEMA = '{BASE}';")
    chk(n == len(TABLAS), f"{n} tablas creadas (el MR declara {len(TABLAS)})")
    n = cuenta(f"SELECT COUNT(*) FROM information_schema.REFERENTIAL_CONSTRAINTS "
               f"WHERE CONSTRAINT_SCHEMA = '{BASE}';")
    chk(n == len(FKS), f"{n} llaves foráneas (el MR declara {len(FKS)})")
    n = cuenta(f"SELECT COUNT(*) FROM information_schema.CHECK_CONSTRAINTS "
               f"WHERE CONSTRAINT_SCHEMA = '{BASE}' "
               f"AND CONSTRAINT_NAME LIKE 'ck\\_%';")
    chk(n == len(CHECKS), f"{n} restricciones CHECK registradas "
        f"(el MR declara {len(CHECKS)})")

    # --------------------------------------------------------------- B
    print()
    print("=" * 70)
    print("B. La misma batería de pruebas que verificar_mr.py")
    print("=" * 70)
    rc, _, err = mysql("START TRANSACTION;\n" + "\n".join(SEMILLA) + "\nCOMMIT;", BASE)
    chk(rc == 0, f"la semilla ({len(SEMILLA)} filas válidas) entra sin errores"
        + (f" — {error_corto(err)}" if rc else ""))
    if rc:
        raise SystemExit(1)

    for prueba in PRUEBAS:
        clase, nombre, sentencias = prueba[:3]
        previas = sentencias[:-1] if clase == "FALLA" else sentencias
        ultima = sentencias[-1:] if clase == "FALLA" else []
        guion = ["START TRANSACTION;", *previas, "SELECT 'PREVIAS_OK';",
                 *ultima, "SELECT 'ULTIMA_OK';"]
        if clase == "QUEDA":
            guion.append("SELECT CONCAT_WS(','," + ",".join(
                f"(SELECT COUNT(*) FROM {t})" for t in CONTEOS) + ");")
        guion.append("ROLLBACK;")
        rc, out, err = mysql("\n".join(guion), BASE)
        previas_ok = "PREVIAS_OK" in out
        ultima_ok = "ULTIMA_OK" in out
        if not previas_ok:
            chk(False, f"{nombre} — falló la PREPARACIÓN: {error_corto(err)}")
        elif clase == "FALLA":
            # rechazar no basta: tiene que rechazar la restriccion nombrada
            motivo = MOTIVO_MYSQL[nombre]
            bien = not ultima_ok and re.search(motivo, err) is not None
            nota = (" — el motor lo ACEPTÓ" if ultima_ok else "" if bien
                    else f" — rechazado por OTRA razón (se esperaba {motivo})")
            chk(bien, f"[rechaza] {nombre}{nota}"
                + (f"\n            ↳ {error_corto(err)[:150]}" if not ultima_ok else ""))
        elif clase == "PASA":
            chk(ultima_ok, f"[acepta]  {nombre}"
                + ("" if ultima_ok else f" — RECHAZADO: {error_corto(err)}"))
        else:
            fila = out.strip().splitlines()[-1].split(",")
            reales = dict(zip(CONTEOS, map(int, fila)))
            dif = {t: (reales[t], n) for t, n in prueba[3].items() if reales[t] != n}
            chk(ultima_ok and not dif, f"[queda]   {nombre}"
                + (f" — difieren (real, esperado): {dif}" if dif else ""))
finally:
    mysql(f"DROP DATABASE IF EXISTS {BASE};")
    print()
    print(f"(base de prueba `{BASE}` borrada)")

print("=" * 70)
if fallas:
    print(f"RESULTADO: {ok} correctas, {len(fallas)} FALLAS")
    for f in fallas:
        print(f"   · {f}")
    sys.exit(1)
print(f"RESULTADO: {ok} comprobaciones contra MySQL {version}, todas correctas.")
print("=" * 70)
