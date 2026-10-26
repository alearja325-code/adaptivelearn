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
`../mer/datos_mer.py`, que es la fuente del MER final y de sus diagramas.
(Hasta el 2026-10-21 apuntaba a `../diagrama/`, la del borrador.)

Uso:  python _verificar_mr_mer.py
"""
import os
import sys
import unicodedata

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "mer"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datos_mer import ENTIDADES, RELACIONES           # noqa: E402
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

# ------------------------------------------- 2. cada FK sale de una relacion
# Desde el 2026-10-21 el MER esta en notacion Chen estricta (hallazgo H-8):
# no dibuja llaves foraneas. Las FK del MR son lo que la derivacion produce
# de cada relacion del MER, y eso es lo que se comprueba aqui -- en las dos
# direcciones: toda FK del MR realiza una relacion del MER, y toda relacion
# (no derivada) del MER esta realizada por alguna FK.
pares_mer = {frozenset((norm(r["a"]), norm(r["b"])))
             for r in RELACIONES if not r.get("derivada")}
asociativas = {norm(r["asociativa"]): {norm(r["a"]), norm(r["b"])}
               for r in RELACIONES if r.get("asociativa")}


def realiza_relacion(origen, destino):
    return (frozenset((origen, destino)) in pares_mer or
            destino in asociativas.get(origen, set()))


derivadas = {}          # tabla -> columnas que salen de una relacion del MER
for origen, cols, destino, cols_dest, *_ in datos_mr.FKS:
    if not realiza_relacion(origen, destino):
        fallas.append(f"FK {origen}->{destino}: no corresponde a ninguna relacion del MER")
        continue
    # una columna sale de la relacion si lleva la LLAVE PRIMARIA de la otra
    # entidad; si apunta a una columna que no es PK (destino de un UNIQUE),
    # es redundancia del MR y tiene que estar justificada abajo
    pk_dest = set(datos_mr.pk_de(destino))
    for c, cd in zip(cols, cols_dest):
        if cd in pk_dest:
            derivadas.setdefault(origen, set()).add(c)

realizadas = set()
for origen, _, destino, *_ in datos_mr.FKS:
    realizadas.add(frozenset((origen, destino)))
for r in RELACIONES:
    if r.get("derivada"):
        continue
    a, b = norm(r["a"]), norm(r["b"])
    if r.get("asociativa"):
        t = norm(r["asociativa"])
        ok_ = frozenset((t, a)) in realizadas and frozenset((t, b)) in realizadas
    else:
        ok_ = frozenset((a, b)) in realizadas
    if not ok_:
        fallas.append(f"relacion del MER sin FK que la realice: {a} «{r['nombre']}» {b}")

# ----------------------------------------------------- 3. mismos atributos
# Los atributos calculados (marca "C": progreso de la inscripcion) se dibujan
# en el MER pero no se guardan: no tienen columna, y no se buscan en el MR.
attrs_mer = {norm(e[0]): [norm(a[0].split(" ")[0]) for a in e[2] if a[1] != "C"]
             for e in ENTIDADES if norm(e[0]) != "reporte"}
llaves_mer = {norm(e[0]): {norm(a[0].split(" ")[0]) for a in e[2]
                           if a[1] in ("PK", "PD")}
              for e in ENTIDADES if norm(e[0]) != "reporte"}

# Columnas que el MR agrega por decision propia y documentada: ni son
# atributo del MER ni salen de una relacion. Cada una necesita su razon
# escrita aqui -- no se aceptan columnas huerfanas. (resultado.id_experiencia
# ya no esta en esta lista: es parte de la llave de experiencia_evidencia y
# sale de la relacion «mide».)
EXTRA_JUSTIFICADAS = {
    ("presentacion", "id_experiencia"):
        "columna redundante deliberada, como en resultado: sin ella, una "
        "presentacion podia unir un item de una experiencia con la "
        "inscripcion de otra (RI-13). Con ella, las dos FK compuestas lo "
        "impiden sin triggers.",
    ("respuesta_opcion", "id_item"):
        "columna redundante deliberada, la misma tecnica: esta en las dos FK "
        "compuestas y obliga a que la opcion elegida sea del item que se "
        "presento (RI-6, ciclo C4 del MER). Sin ella, una respuesta podia "
        "elegir una opcion de otro item, y el motor lo aceptaba.",
    ("credencial", "intentos_codigo"):
        "endurecimiento del backend de I1 (sql/002): sin limite de "
        "intentos, un codigo de 6 digitos se adivina por fuerza bruta. "
        "El MER no dibuja mecanismos de seguridad; los deja al MR.",
    ("credencial", "intentos_login"):
        "endurecimiento del backend de I1 (sql/002), igual que el anterior.",
    ("credencial", "bloqueado_hasta"):
        "endurecimiento del backend de I1 (sql/002), igual que el anterior.",
    ("credencial", "actualizado_en"):
        "marca tecnica del backend de I1 (sql/002); no es un dato del dominio.",
}

for tabla, cols_mer in sorted(attrs_mer.items()):
    if tabla not in ent_mr:
        continue
    cols_mr = [norm(f["nombre"]) for f in datos_mr.campos_de(tabla)]
    for c in cols_mer:
        if c not in cols_mr:
            fallas.append(f"{tabla}: atributo del MER ausente en el MR -> {c}")
    for c in cols_mr:
        if (c not in cols_mer and c not in derivadas.get(tabla, set())
                and (tabla, c) not in EXTRA_JUSTIFICADAS):
            fallas.append(f"{tabla}: columna del MR que no es atributo del MER ni sale "
                          f"de una relacion -> {c} (si es deliberada, documentala en "
                          f"EXTRA_JUSTIFICADAS)")

# ------------------------------------------------- 4. llaves primarias
# La PK del MR = las llaves que el MER dibuja (PK, o llave parcial de una
# debil) mas, en debiles y asociativas, columnas que salen de sus relaciones.
for tabla, llaves in sorted(llaves_mer.items()):
    if tabla not in ent_mr:
        continue
    pk_mr = {norm(c) for c in datos_mr.pk_de(tabla)}
    if not llaves <= pk_mr:
        fallas.append(f"{tabla}: el MER marca como llave {sorted(llaves - pk_mr)} y no está "
                      f"en la PK del MR")
    sobra = pk_mr - llaves - derivadas.get(tabla, set())
    if sobra:
        fallas.append(f"{tabla}: la PK del MR tiene {sorted(sobra)}, que ni es llave del MER "
                      f"ni sale de una relación")

# ------------------------------------------- 5. las FK apuntan a algo real
tablas = {t["tabla"] for t in datos_mr.TABLAS}
for origen, cols, destino, cols_dest, *_ in datos_mr.FKS:
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

# ------------------------------------------ 6. toda FK declarada como tal
declaradas = {(o, c) for o, cols, *_ in datos_mr.FKS for c in cols}
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

# ---------------------------------- 7. ninguna justificacion queda vieja
for (tabla, col) in EXTRA_JUSTIFICADAS:
    if col in attrs_mer.get(tabla, []):
        fallas.append(f"{tabla}.{col}: ya esta en el MER, sobra en "
                      f"EXTRA_JUSTIFICADAS")
    elif col in derivadas.get(tabla, set()):
        fallas.append(f"{tabla}.{col}: sale de una relacion del MER, sobra en "
                      f"EXTRA_JUSTIFICADAS")
    elif col not in [norm(f["nombre"]) for f in datos_mr.campos_de(tabla)]:
        fallas.append(f"{tabla}.{col}: justificada pero no existe en el MR")

# ------------------------------------------------- 8. metadatos completos
for t in datos_mr.TABLAS:
    for f in t["campos"]:
        for clave in ("mysql", "sqlite", "desc", "fuente"):
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
