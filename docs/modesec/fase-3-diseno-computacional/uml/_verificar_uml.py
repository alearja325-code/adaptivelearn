"""Comprueba que los entregables UML no se aparten de su fuente ni entre si.

Cinco bloques:

  A. Casos de uso contra el analisis de requerimientos (`../11`): los 44
     requerimientos funcionales cubiertos; ningun RF, RNF ni ventana citado
     que no exista; cada caso de uso dibujado como propio en exactamente un
     diagrama; cada «include» que el flujo menciona, dibujado (y al reves).
  B. Clases contra el modelo relacional y el MER: los atributos de cada
     clase son las columnas de su tabla menos las de llave foranea; las
     enumeraciones son los ENUM del MR valor por valor; las asociaciones son
     las relaciones del MER, ni una mas ni una menos; todo caso de uso
     aporta al menos un metodo.
  C. Objetos: cada atributo existe en su clase y cada enlace es una
     asociacion. Y la prueba fuerte: el diagrama de objetos se CARGA en el
     esquema real (`../modelo-relacional/mr_esquema.sql`). Si la fotografia
     violara una restriccion, el motor la rechazaria.
  D. La regla adaptativa: el resultado que muestra el diagrama de objetos y
     los ejemplos de la prueba de aceptacion de CU-25 son los que da RF-04-07.
  E. Secuencias: toda llamada `operacion(...)` esta declarada en la clase
     del receptor; todo caso de uso y ventana citados existen.
  F. Matriz CRUD (datos_crud.py): toda entidad tiene quien la cree, los
     hechos y fotografias nunca se modifican, y lo que se borra en cascada
     -- calculado de las llaves foraneas del MR -- es lo que dicen CU-15 y
     CU-26.

Uso:  python _verificar_uml.py
"""
import os
import re
import sqlite3
import sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
FASE3 = os.path.join(AQUI, "..")
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(FASE3, "modelo-relacional"))
sys.path.insert(0, os.path.join(FASE3, "mer"))

import datos_casos_uso as CU                                   # noqa: E402
import datos_clases as CL                                      # noqa: E402
import datos_objetos as OB                                     # noqa: E402
import datos_secuencias as SQ                                  # noqa: E402
import diagramas_cu                                            # noqa: E402
import regla                                                   # noqa: E402
import datos_mr as MR                                          # noqa: E402
import datos_mer as MER                                        # noqa: E402
from generar import orden_creacion                             # noqa: E402

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


# =============================================================== A
print("=" * 70)
print("A. Casos de uso contra el análisis de requerimientos")
print("=" * 70)
txt11 = open(os.path.join(FASE3, "11-analisis-requerimientos.md"), encoding="utf-8").read()
rf_11 = set(re.findall(r"^#### (RF-\d\d-\d\d)", txt11, re.M))
rnf_11 = set(re.findall(r"^#### (RNF-\d\d)", txt11, re.M))
ventanas_11 = set(re.findall(r"^\| (\d{3}) \|", txt11, re.M))
chk(len(rf_11) == 44, f"el análisis tiene 44 requerimientos funcionales (leídos: {len(rf_11)})")

citados = {r for c in CU.CASOS for r in c["rf"]}
chk(rf_11 <= citados, f"los 44 RF están cubiertos por algún caso de uso "
    f"(sin cubrir: {sorted(rf_11 - citados) or 'ninguno'})")
inexistentes = citados - rf_11 - rnf_11
chk(not inexistentes, f"ningún caso de uso cita un requerimiento inexistente "
    f"({sorted(inexistentes) or 'ninguno'})")
v_cit = {v for c in CU.CASOS for v in c["ventanas"]}
chk(v_cit <= ventanas_11, f"toda ventana citada existe ({sorted(v_cit - ventanas_11) or 'ok'})")
mal_sub = [c["id"] for c in CU.CASOS
           if any(r.startswith("RF-") and f"SUB-{r[3:5]}" != c["sub"] for r in c["rf"])]
chk(not mal_sub, f"cada caso de uso está en el subsistema de sus RF ({mal_sub or 'todos'})")
ids = [c["id"] for c in CU.CASOS]
chk(len(ids) == len(set(ids)), f"{len(ids)} casos de uso, sin identificadores repetidos")

propios = Counter()
for d in diagramas_cu.DIAGRAMAS:
    for cid, *_ in d.get("casos", []):
        propios[cid] += 1
    for cid, *_ in d.get("refs", []):
        chk(cid in CU.POR_ID, f"{d['archivo']}: la referencia {cid} existe")
chk(all(propios[i] == 1 for i in ids) and set(propios) == set(ids),
    "cada caso de uso se dibuja como propio en exactamente un diagrama "
    f"({ {i: propios[i] for i in ids if propios[i] != 1} or 'ok'})")

for o, tipo, dst, _ in CU.RELACIONES:
    if tipo == "include":
        chk(dst in " ".join(CU.POR_ID[o]["flujo"]),
            f"«include» {o} → {dst}: el flujo de {o} lo menciona")
mencionados = {(c["id"], m) for c in CU.CASOS for paso in c["flujo"]
               for m in re.findall(r"[Ss]e incluye (CU-\d\d)", paso)}
dibujados = {(o, d) for o, t, d, _ in CU.RELACIONES if t == "include"}
chk(mencionados == dibujados, "cada «Se incluye CU-xx» de un flujo es un «include» dibujado "
    f"(difieren: {mencionados ^ dibujados or 'ninguno'})")

# =============================================================== B
print()
print("=" * 70)
print("B. Clases contra el modelo relacional y el MER")
print("=" * 70)
mr_tabla = {t["tabla"]: t for t in MR.TABLAS}
fk_cols = {}
for fk in MR.FKS:
    fk_cols.setdefault(fk[0], set()).update(fk[1])


def atributos(nombre):
    c = CL.POR_NOMBRE[nombre]
    propios_ = [a for a, _ in c["atributos"]]
    for hijo, padre in CL.GENERALIZACIONES:
        if hijo == nombre:
            propios_ = atributos(padre) + propios_
    return propios_


for c in CL.CLASES:
    if not c["tabla"]:
        continue
    esperado = {f["nombre"] for f in mr_tabla[c["tabla"]]["campos"]} - fk_cols.get(c["tabla"], set())
    real = set(atributos(c["nombre"]))
    chk(real == esperado, f"{c['nombre']}: atributos = columnas de `{c['tabla']}` sin las de FK"
        + ("" if real == esperado else f" (difieren: {sorted(real ^ esperado)})"))
tablas_con_clase = {c["tabla"] for c in CL.CLASES if c["tabla"]}
chk(tablas_con_clase == set(mr_tabla), "cada tabla del MR tiene su clase "
    f"({sorted(set(mr_tabla) - tablas_con_clase) or 'todas'})")

for nombre, valores, origen in CL.ENUMERACIONES:
    if not origen:
        continue
    tabla, col = origen
    tipo = next(f["mysql"] for f in mr_tabla[tabla]["campos"] if f["nombre"] == col)
    vals_mr = re.findall(r"'([^']*)'", tipo)
    chk(vals_mr == valores, f"enumeración {nombre} = ENUM de {tabla}.{col}")
    clase = next(c for c in CL.CLASES if c["tabla"] == tabla)
    t_attr = dict(clase["atributos"])[col].split(" ")[0]
    chk(t_attr == nombre, f"{clase['nombre']}.{col} es de tipo {nombre}")

entidad_de = {c["nombre"]: c["entidad"] for c in CL.CLASES}
mer_pares = Counter((r["nombre"], frozenset((r["a"], r["b"]))) for r in MER.RELACIONES)
uml_pares = Counter((n, frozenset((entidad_de[a], entidad_de[b])))
                    for a, b, n, *_ in CL.ASOCIACIONES)
chk(mer_pares == uml_pares, f"las {len(CL.ASOCIACIONES)} asociaciones son las "
    f"{len(MER.RELACIONES)} relaciones del MER, con las mismas entidades "
    f"(difieren: {set(mer_pares) ^ set(uml_pares) or 'ninguna'})")
cus_metodos = {cu for c in CL.CLASES + CL.SERVICIOS for m in c["metodos"] for cu in m["cus"]}
chk(cus_metodos <= set(ids), f"todo método cita casos de uso que existen "
    f"({sorted(cus_metodos - set(ids)) or 'ok'})")
chk(set(ids) <= cus_metodos, "todo caso de uso aporta al menos un método "
    f"(sin método: {sorted(set(ids) - cus_metodos) or 'ninguno'})")

# =============================================================== C
print()
print("=" * 70)
print("C. Objetos: contra las clases, y cargados en el esquema real")
print("=" * 70)
asoc = {}
for a, b, n, *_ in CL.ASOCIACIONES:
    asoc[(a, b, n)] = asoc[(b, a, n)] = True
for oid, (clase, valores) in OB.OBJETOS.items():
    disponibles = set(atributos(clase))
    faltan = [k for k, _ in valores if k not in disponibles]
    chk(not faltan, f"{oid} : {clase} — sus atributos existen en la clase "
        + ("" if not faltan else f"(no existen: {faltan})"))
malos = [(a, b, n) for a, b, n in OB.ENLACES
         if (OB.OBJETOS[a][0], OB.OBJETOS[b][0], n) not in asoc]
chk(not malos, f"los {len(OB.ENLACES)} enlaces son instancias de asociaciones del diagrama "
    f"de clases ({malos or 'todos'})")


def valor(v):
    if v == "null":
        return None
    if v in ("true", "false"):
        return 1 if v == "true" else 0
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return v.strip('"')


tabla_de = {c["nombre"]: c["tabla"] for c in CL.CLASES}
filas = {}
for oid, (clase, valores) in OB.OBJETOS.items():
    filas[oid] = {k: valor(v) for k, v in valores}
ro, (r_a, r_b) = OB.OBJETO_ASOCIACION
vecinos = {oid: [] for oid in OB.OBJETOS}
for a, b, n in OB.ENLACES:
    if not (a, b) == (r_a, r_b):
        vecinos[a].append(b)
        vecinos[b].append(a)
vecinos[ro] = [r_a, r_b]

# Rellenar: llaves sustitutas no mostradas, FK desde los enlaces, y las
# columnas NOT NULL sin defecto que el diagrama no muestra (marcador).
siguiente = Counter()
for oid, (clase, _) in OB.OBJETOS.items():
    t = mr_tabla[tabla_de[clase]]
    pk = MR.pk_de(t["tabla"])
    if len(pk) == 1 and "AUTO_INCREMENT" in t["campos"][0]["mysql"] and pk[0] not in filas[oid]:
        siguiente[t["tabla"]] += 1
        filas[oid][pk[0]] = 900 + siguiente[t["tabla"]]
pendientes = set(OB.OBJETOS)
for _ in range(10):
    for oid in list(pendientes):
        tabla = tabla_de[OB.OBJETOS[oid][0]]
        listo = True
        for o, cols, dest, cols_d, *_ in MR.FKS:
            if o != tabla:
                continue
            otros = [v for v in vecinos[oid] if tabla_de[OB.OBJETOS[v][0]] == dest]
            if not otros:
                continue
            fila_d = filas[otros[0]]
            if not all(c in fila_d for c in cols_d):
                listo = False
                continue
            for c, cd in zip(cols, cols_d):
                filas[oid][c] = fila_d[cd]
        if listo:
            pendientes.discard(oid)
for oid, (clase, _) in OB.OBJETOS.items():
    for f in mr_tabla[tabla_de[clase]]["campos"]:
        if f["nombre"] in filas[oid] or f["nulo"] or f["defecto"]:
            continue
        tipo = f["mysql"]
        filas[oid][f["nombre"]] = ("2026-10-01 00:00" if tipo.startswith("DATETIME") else
                                   re.findall(r"'([^']*)'", tipo)[0] if tipo.startswith("ENUM") else
                                   1 if "INT" in tipo else "texto ilustrativo")

con = sqlite3.connect(":memory:")
con.execute("PRAGMA foreign_keys = ON")
con.executescript(open(os.path.join(FASE3, "modelo-relacional", "mr_esquema.sql"),
                       encoding="utf-8").read())
orden = orden_creacion()          # cada tabla despues de aquellas a las que apunta
cargados, errores = 0, []
for tabla in orden:
    for oid, (clase, _) in OB.OBJETOS.items():
        if tabla_de[clase] != tabla:
            continue
        f = filas[oid]
        try:
            con.execute(f"INSERT INTO {tabla} ({', '.join(f)}) VALUES ({', '.join('?' * len(f))})",
                        list(f.values()))
            cargados += 1
        except sqlite3.Error as e:
            errores.append((oid, str(e)))
chk(not errores and cargados == len(OB.OBJETOS),
    f"los {len(OB.OBJETOS)} objetos se cargan en mr_esquema.sql sin violar ninguna restricción"
    + ("" if not errores else f" — rechazados: {errores}"))
fila = con.execute("SELECT COUNT(*) FROM presentacion p JOIN item i ON i.id_item = p.id_item "
                   "WHERE i.id_experiencia <> p.id_experiencia").fetchone()[0]
chk(fila == 0, "cada ítem presentado es de la experiencia de la inscripción (RI-13)")
sin_resp = con.execute("SELECT COUNT(*) FROM presentacion p LEFT JOIN respuesta r USING "
                       "(id_inscripcion, id_item) WHERE r.id_respuesta IS NULL").fetchone()[0]
chk(sin_resp == 1, "hay exactamente una presentación sin respuesta, la que se retoma (ADR-031)")
con.close()

# =============================================================== D
print()
print("=" * 70)
print("D. La regla adaptativa (RF-04-07)")
print("=" * 70)
resp = [(filas[r]["certeza"], bool(filas[r]["correcta"])) for r in OB.EVIDENCIA_1]
n, estado = regla.primera_conclusion(resp)
chk((n, estado) == (4, filas["res1"]["estado"]),
    f"el diagrama de objetos: la regla concluye «{estado}» en la respuesta {n}, "
    f"y res1 dice «{filas['res1']['estado']}»")
chk(regla.primera_conclusion([(4, True), (5, True), (1, True), (3, True)]) == (4, "muestra"),
    "CU-25, prueba de aceptación: certezas 4, 5, 1 y 3, correctas → Muestra en la 4.ª")
chk(regla.primera_conclusion([(c, ok_) for c, ok_ in
                              [(0, True), (1, False), (2, True), (2, True), (1, False), (0, True)]])
    == (6, "no_concluyente"),
    "CU-25, prueba de aceptación: seis respuestas con certeza 0 a 2 → No concluyente")
chk(regla.primera_conclusion([(5, False), (4, False), (3, False), (1, True)]) == (4, "no_muestra"),
    "tres señales fuertes de «no muestra» de cuatro → No muestra en la 4.ª")

# =============================================================== E
print()
print("=" * 70)
print("E. Secuencias contra clases y casos de uso")
print("=" * 70)


def metodos(nombre):
    c = CL.POR_NOMBRE[nombre]
    nombres = {m["firma"].split("(")[0] for m in c["metodos"]}
    for hijo, padre in CL.GENERALIZACIONES:
        if hijo == nombre:
            nombres |= metodos(padre)
    return nombres


for s in SQ.SECUENCIAS:
    clase_de = {p[0]: p[2] for p in s["participantes"]}
    malas = []
    for paso in s["pasos"]:
        if paso[0] in ("m", "s"):
            receptor = paso[2] if paso[0] == "m" else paso[1]
            texto = paso[3] if paso[0] == "m" else paso[2]
            llamada = re.fullmatch(r"([a-zA-Z]+)\(.*\)", texto)
            if llamada and clase_de.get(receptor):
                if llamada.group(1) not in metodos(clase_de[receptor]):
                    malas.append(f"{clase_de[receptor]}.{llamada.group(1)}")
        if paso[0] == "c" and clase_de.get(paso[2]) not in CL.POR_NOMBRE:
            malas.append(f"«create» de una clase inexistente: {paso[2]}")
    chk(not malas, f"{s['archivo']}: toda operación invocada existe en su clase "
        + ("" if not malas else f"(no existen: {malas})"))
    chk(set(s["cus"]) <= set(ids) and set(s["ventanas"]) <= ventanas_11,
        f"{s['archivo']}: sus casos de uso y ventanas existen")

# =============================================================== F
print()
print("=" * 70)
print("F. Matriz CRUD: quién crea, lee, modifica y borra cada entidad")
print("=" * 70)
import datos_crud as CR                                        # noqa: E402

entidades_mer = {e[0] for e in MER.ENTIDADES}
nombradas = {ent for d in CR.CRUD.values() for ent in d}
chk(nombradas <= entidades_mer, "la matriz solo nombra entidades del MER "
    f"({sorted(nombradas - entidades_mer) or 'ok'})")
chk(set(CR.CRUD) == set(ids), "la matriz tiene una fila por cada caso de uso")
chk(all(set(op) <= set("CRUD") for d in CR.CRUD.values() for op in d.values()),
    "solo usa las letras C, R, U y D")
creadas = {ent for d in CR.CRUD.values() for ent, op in d.items() if "C" in op}
chk(entidades_mer - creadas == set(CR.SIN_CREADOR),
    "toda entidad tiene un caso de uso que la crea, salvo las del catálogo y el Reporte, "
    f"que dicen por qué (sin creador ni razón: {sorted(entidades_mer - creadas - set(CR.SIN_CREADOR)) or 'ninguna'})")
vacios = {cu for cu, d in CR.CRUD.items() if not d}
chk(vacios == set(CR.SIN_DATOS), "todo caso de uso toca al menos una entidad, salvo los que "
    "dicen por qué")
modificadas = {ent for d in CR.CRUD.values() for ent, op in d.items() if "U" in op}
chk(not modificadas & set(CR.INMUTABLES), "Presentación, Respuesta, Respuesta_Opción y Resultado "
    "nunca se modifican: son hechos y fotografías (RNF-10, RNF-11)")
borradas = {ent for d in CR.CRUD.values() for ent, op in d.items() if "D" in op}
chk(borradas == set(CR.BORRABLES), f"solo se borra directamente {sorted(CR.BORRABLES)}")
raices = {"DOCENTE", "ESTUDIANTE", "CREDENCIAL", "AREA", "GRADO", "DOCUMENTO_OFICIAL", "DBA",
          "EVIDENCIA", "EVIDENCIA_DICTAMEN"}
casc_exp = {t.upper() for t in CR.en_cascada("experiencia", MR.FKS)}
casc_ins = {t.upper() for t in CR.en_cascada("inscripcion", MR.FKS)}
chk(casc_exp == {"EXPERIENCIA_EVIDENCIA", "ITEM", "OPCION", "INSCRIPCION", "PRESENTACION",
                 "RESPUESTA", "RESPUESTA_OPCION", "RESULTADO"},
    "eliminar una experiencia (CU-15) borra en cascada exactamente lo que el caso de uso "
    f"dice: {sorted(casc_exp)}")
chk(casc_ins == {"PRESENTACION", "RESPUESTA", "RESPUESTA_OPCION", "RESULTADO"},
    f"salir de una experiencia (CU-26) borra en cascada lo respondido y nada más: {sorted(casc_ins)}")
chk(not (casc_exp | casc_ins) & raices, "la cascada nunca alcanza una cuenta ni el currículo")

# ------------------------------------------------------------------ --
print()
print("=" * 70)
if fallas:
    print(f"RESULTADO: {ok} correctas, {len(fallas)} FALLAS")
    for f in fallas:
        print(f"   · {f}")
    sys.exit(1)
print(f"RESULTADO: {ok} comprobaciones, todas correctas.")
print("=" * 70)
