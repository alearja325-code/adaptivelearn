"""Comprueba que el Modelo Relacional no se aparte del MER.

NACE DE UN ERROR REAL. El 2026-09-19 se encontro que
`04-modelo-relacional.md` seguia basado en la TERCERA revision del MER
mientras el MER ya iba en la QUINTA: le faltaban las 3 entidades
agregadas para responder a la revision del docente
(Experiencia_Evidencia, Evidencia_Dictamen, Presentacion). Nadie lo
noto porque `verificar_mr.py` comprueba el MR contra si mismo (DBML vs
SQL) -- nunca contra el MER. Esa era la brecha: dos documentos
internamente coherentes y contradictorios entre si.

Este script cierra esa brecha. Compara `datos_mr.py` contra
`../diagrama/datos_mer.py`, que es la fuente del MER y de sus diagramas.

Uso:  python3 _verificar_mr_mer.py
"""
import os
import sys
import unicodedata

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "diagrama"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datos_mer import ENTIDADES                       # noqa: E402
import datos_mr                                       # noqa: E402


def norm(s):
    """MER escribe en espanol natural (Ítem, Opción); MR en snake_case sin
    acentos. Esta es la unica traduccion permitida entre los dos."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s.lower()


fallas = []

# ---------------------------------------------------- 1. mismas entidades
# El MER cuenta Reporte aparte: es vista derivada, no persiste, y por eso
# no tiene tabla. Se excluye a proposito, no por olvido.
ent_mer = {norm(e[0]) for e in ENTIDADES} - {"reporte"}
ent_mr = {norm(t["tabla"]) for t in datos_mr.TABLAS}

for falta in sorted(ent_mer - ent_mr):
    fallas.append(f"entidad del MER sin tabla en el MR: {falta}")
for sobra in sorted(ent_mr - ent_mer):
    fallas.append(f"tabla del MR que no existe como entidad en el MER: {sobra}")

# ----------------------------------------------------- 2. mismos atributos
attrs_mer = {norm(e[0]): [norm(a[0].split(" ")[0]) for a in e[2]]
             for e in ENTIDADES if norm(e[0]) != "reporte"}

# Columnas que el MR agrega por decision propia y documentada. Cada una
# necesita su razon escrita aqui, igual que las excepciones de
# verificar_consistencia.py -- no se aceptan columnas huerfanas.
EXTRA_JUSTIFICADAS = {
    ("resultado", "id_experiencia"):
        "el MER delega explicitamente esta decision al MR "
        "('que esa deduccion se resuelva con una columna redundante o con "
        "una regla, lo decide el Modelo Relacional'). Permite que las dos "
        "reglas de coherencia sean estructurales en vez de triggers.",
}

for tabla, cols_mer in sorted(attrs_mer.items()):
    if tabla not in ent_mr:
        continue
    cols_mr = [norm(f["nombre"]) for f in datos_mr.campos_de(tabla)]
    for c in cols_mer:
        if c not in cols_mr:
            fallas.append(f"{tabla}: atributo del MER ausente en el MR -> {c}")
    for c in cols_mr:
        if c not in cols_mer and (tabla, c) not in EXTRA_JUSTIFICADAS:
            fallas.append(f"{tabla}: columna del MR que el MER no declara "
                          f"-> {c} (si es deliberada, documentala en "
                          f"EXTRA_JUSTIFICADAS)")

# ------------------------------------------------- 3. llaves primarias
for e in ENTIDADES:
    tabla = norm(e[0])
    if tabla == "reporte" or tabla not in ent_mr:
        continue
    pk_mer = {norm(a[0].split(" ")[0]) for a in e[2] if a[1].startswith("PK")}
    pk_mr = {norm(c) for c in datos_mr.pk_de(tabla)}
    if pk_mer != pk_mr:
        fallas.append(f"{tabla}: PK distinta. MER={sorted(pk_mer)} "
                      f"MR={sorted(pk_mr)}")

# ------------------------------------------- 4. las FK apuntan a algo real
tablas = {t["tabla"] for t in datos_mr.TABLAS}
for origen, cols, destino, cols_dest, _, _ in datos_mr.FKS:
    if destino not in tablas:
        fallas.append(f"FK {origen}->{destino}: la tabla destino no existe")
        continue
    if len(cols) != len(cols_dest):
        fallas.append(f"FK {origen}->{destino}: {len(cols)} columnas origen "
                      f"vs {len(cols_dest)} destino")
    nombres_origen = {f["nombre"] for f in datos_mr.campos_de(origen)}
    nombres_dest = {f["nombre"] for f in datos_mr.campos_de(destino)}
    for col in cols:
        if col not in nombres_origen:
            fallas.append(f"FK {origen}->{destino}: {origen}.{col} no existe")
    for col in cols_dest:
        if col not in nombres_dest:
            fallas.append(f"FK {origen}->{destino}: {destino}.{col} no existe")
    # una FK compuesta solo es valida contra la PK del destino o un UNIQUE
    pk_dest = set(datos_mr.pk_de(destino))
    unicos_dest = [set(u[1]) for u in datos_mr.UNICOS if u[0] == destino]
    if set(cols_dest) != pk_dest and set(cols_dest) not in unicos_dest:
        fallas.append(f"FK {origen}->{destino}({', '.join(cols_dest)}): el "
                      f"destino no es ni la PK ni un UNIQUE declarado")

# ------------------------------------------ 5. toda FK declarada como tal
declaradas = {(o, c) for o, cols, _, _, _, _ in datos_mr.FKS for c in cols}
for t in datos_mr.TABLAS:
    for f in t["campos"]:
        marcada = "FK" in f["llave"]
        real = (t["tabla"], f["nombre"]) in declaradas
        if marcada and not real:
            fallas.append(f"{t['tabla']}.{f['nombre']}: marcada FK pero no "
                          f"aparece en ninguna FK de FKS")
        if real and not marcada:
            fallas.append(f"{t['tabla']}.{f['nombre']}: usada en una FK pero "
                          f"no marcada como FK en su campo")

# ------------------------------------------------- 6. metadatos completos
for t in datos_mr.TABLAS:
    for f in t["campos"]:
        for clave in ("mariadb", "sqlite", "desc", "fuente"):
            if not str(f[clave]).strip():
                fallas.append(f"{t['tabla']}.{f['nombre']}: falta '{clave}' "
                              f"-- MODESEC exige los metadatos completos")

# ---------------------------------------------------------------- salida
print("=" * 66)
print("MR contra MER — comprobacion de alineacion")
print("=" * 66)
print(f"  entidades del MER (sin Reporte): {len(ent_mer)}")
print(f"  tablas del MR:                   {len(ent_mr)}")
print(f"  columnas:                        {datos_mr.N_CAMPOS}")
print(f"  llaves foraneas:                 {datos_mr.N_FKS}")
print()

if fallas:
    print(f"{len(fallas)} PROBLEMA(S):")
    for f in fallas:
        print(f"   · {f}")
    print("\n" + "=" * 66)
    sys.exit(1)

print("OK — el MR no se aparta del MER.")
print("=" * 66)
