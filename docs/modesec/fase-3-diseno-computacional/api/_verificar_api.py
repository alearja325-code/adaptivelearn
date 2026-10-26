"""Comprueba que el catalogo de endpoints no se aparte del resto de la Fase III.

Cuatro bloques:

  A. Trazabilidad: todo caso de uso tiene al menos un endpoint; la operacion
     de cada endpoint existe en una clase «servicio» del diagrama de clases y
     atiende uno de sus casos de uso; toda operacion de servicio tiene ruta o
     dice por que no; toda llamada de la IGU en un diagrama de secuencia es
     un endpoint del catalogo.
  B. Datos: lo que toca cada endpoint sale de la matriz CRUD de sus casos de
     uso, y todo lo que un caso de uso hace lo hace alguno de sus endpoints;
     GET solo lee, DELETE borra, PATCH modifica; nadie modifica un hecho ni
     borra lo que ningun flujo borra.
  C. Acceso e incremento: quien llama es el actor del caso de uso; cada
     endpoint cae en un solo incremento; solo I1 tiene endpoints hechos, y
     el estado de cada uno es el del codigo real: se leen los controladores
     de `backend/src/` del repositorio.
  D. Rutas: ninguna repetida, ninguna de las que no se deben agregar, y las
     nuevas en espanol.

Uso:  python _verificar_api.py
"""
import glob
import os
import re
import sys

import calculos as K
from calculos import A, CU, CL, CR, ENDPOINTS, nombre

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


def titulo(t):
    print("=" * 70)
    print(t)
    print("=" * 70)


# =============================================================== A
titulo("A. Trazabilidad: casos de uso, diagrama de clases y secuencias")
todos_cu = {c["id"] for c in CU.CASOS}
citados = {c for e in ENDPOINTS for c in e["cus"]}
chk(not citados - todos_cu, f"todo caso de uso citado existe (sobran: {sorted(citados - todos_cu)})")
chk(todos_cu <= citados, f"los {len(todos_cu)} casos de uso tienen al menos un endpoint "
    f"(sin endpoint: {sorted(todos_cu - citados)})")

malas = []
for e in ENDPOINTS:
    clase, m = K.operacion(e["op"])
    if not m or clase["estereotipo"] != "servicio":
        malas.append(f"{nombre(e)}: {e['op']} no es una operación de servicio")
    elif not set(m["cus"]) & set(e["cus"]):
        malas.append(f"{nombre(e)}: {e['op']} atiende {m['cus']}, no {e['cus']}")
chk(not malas, "la operación de cada endpoint existe en una clase «servicio» y atiende uno de "
    "sus casos de uso" + "".join(f"\n         · {x}" for x in malas))

expuestas = {e["op"] for e in ENDPOINTS}
servicio = set(K.servicios_expuestos())
sin_ruta = servicio - expuestas - set(A.INTERNOS)
chk(not sin_ruta, f"las {len(servicio)} operaciones de servicio tienen ruta o están en INTERNOS "
    f"(sin ninguna: {sorted(sin_ruta)})")
chk(set(A.INTERNOS) <= servicio and not set(A.INTERNOS) & expuestas,
    "INTERNOS son operaciones de servicio que de verdad no tienen ruta")

huerfanas = [f"{sid}: {op}" for sid, op, _ in K.llamadas_igu()
             if not any(sid in K.secuencias(e) and e["op"] == op for e in ENDPOINTS)]
chk(not huerfanas, f"las {len(K.llamadas_igu())} llamadas de la IGU en los diagramas de "
    f"secuencia son endpoints del catálogo (sin endpoint: {huerfanas})")

# =============================================================== B
print()
titulo("B. Datos: el CRUD de cada endpoint es el de sus casos de uso")
entidades = {ent for d in CR.CRUD.values() for ent in d}
desconocidas = {ent for e in ENDPOINTS for ent in e["crud"]} - entidades
chk(not desconocidas, f"toda entidad citada está en la matriz CRUD (desconocidas: {sorted(desconocidas)})")

sobra = []
for e in ENDPOINTS:
    for ent, letras in e["crud"].items():
        for L in letras:
            if not any(L in CR.CRUD[c].get(ent, "") for c in e["cus"]):
                sobra.append(f"{nombre(e)}: {L} en {ent}")
chk(not sobra, "nada de lo que toca un endpoint queda fuera del CRUD de sus casos de uso"
    + "".join(f"\n         · {x}" for x in sobra))

falta = []
for cu, d in CR.CRUD.items():
    for ent, letras in d.items():
        for L in letras:
            if not any(cu in e["cus"] and L in e["crud"].get(ent, "") for e in ENDPOINTS):
                falta.append(f"{cu}: {L} en {ent}")
chk(not falta, "todo lo que un caso de uso crea, lee, modifica o borra lo hace alguno de sus "
    "endpoints" + "".join(f"\n         · {x}" for x in falta))

letras = {nombre(e): "".join(e["crud"].values()) for e in ENDPOINTS}
chk(all(set(letras[nombre(e)]) <= {"R"} for e in ENDPOINTS if e["metodo"] == "GET"),
    "todo GET solo lee")
chk(all("D" in letras[nombre(e)] for e in ENDPOINTS if e["metodo"] == "DELETE"),
    "todo DELETE borra algo")
chk(all("U" in letras[nombre(e)] for e in ENDPOINTS if e["metodo"] == "PATCH"),
    "todo PATCH modifica algo")
chk(not any(set(l) & {"U", "D"} for e in ENDPOINTS for ent, l in e["crud"].items()
            if ent in CR.INMUTABLES),
    "ningún endpoint modifica ni borra una presentación, una respuesta o un resultado "
    "(RNF-10, RNF-11)")
borra = {ent for e in ENDPOINTS for ent, l in e["crud"].items() if "D" in l}
chk(borra <= set(CR.BORRABLES), f"solo se borra lo que un flujo borra: {sorted(borra)}")
casc = {nombre(e): K.cascada(e) for e in ENDPOINTS if e["metodo"] == "DELETE"}
chk(all(casc.values()), "cada DELETE tiene su cascada calculada de las FK del modelo relacional")

# =============================================================== C
print()
titulo("C. Acceso e incremento")
chk(all(e["acceso"] in A.ACCESOS for e in ENDPOINTS), "todo acceso está definido en ACCESOS")
mal_acceso = []
for e in ENDPOINTS:
    admitidos = set().union(*(A.ACCESO_DE_ACTOR.get(CU.POR_ID[c]["actor"], set())
                              for c in e["cus"]))
    if e["acceso"] not in admitidos:
        mal_acceso.append(f"{nombre(e)}: {e['acceso']} no es de {sorted(admitidos)}")
chk(not mal_acceso, "quien llama a cada endpoint es el actor de su caso de uso"
    + "".join(f"\n         · {x}" for x in mal_acceso))
chk(all(e["acceso"] not in ("docente_dueno", "estudiante_dueno") or ":id" in e["ruta"]
        for e in ENDPOINTS),
    "todo endpoint de dueño lleva en la ruta el recurso del que se es dueño")

mal_sub = [nombre(e) for e in ENDPOINTS
           if e["sub"] not in {CU.POR_ID[c]["sub"] for c in e["cus"]}]
chk(not mal_sub, f"el subsistema de cada endpoint es el de uno de sus casos de uso {mal_sub}")
mixtos = [nombre(e) for e in ENDPOINTS
          if len({CU.SUBSISTEMAS[CU.POR_ID[c]["sub"]][1] for c in e["cus"]}) != 1]
chk(not mixtos, f"cada endpoint cae en un solo incremento {mixtos}")
chk(set(A.INCREMENTOS) == {v[1] for v in CU.SUBSISTEMAS.values()},
    "los incrementos son los de los subsistemas (I1 a I4)")
chk(all(e["estado"] in A.ESTADOS for e in ENDPOINTS), "todo estado está definido")
chk(all(K.incremento(e) == "I1" for e in ENDPOINTS if e["estado"] in ("hecho", "ajustar")),
    "solo hay endpoints hechos en I1, el único incremento empezado")
chk(all(e["nota"] for e in ENDPOINTS if e["estado"] in ("ajustar", "opcional")),
    "todo endpoint por ajustar u opcional dice por qué")
# Las rutas que existen de verdad: los controladores de NestJS del backend I1.
BACKEND = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", "..", "..", "..", "backend", "src"))
reales = set()
for ts in glob.glob(os.path.join(BACKEND, "**", "*.controller.ts"), recursive=True):
    txt = open(ts, encoding="utf-8").read()
    base = re.search(r"@Controller\('([^']*)'\)", txt)
    for metodo, sub in re.findall(r"@(Get|Post|Patch|Put|Delete)\((?:'([^']*)')?\)", txt):
        partes = [p for p in (base.group(1) if base else "", sub) if p]
        reales.add(f"{metodo.upper()} /" + "/".join(partes))
chk(bool(reales), f"se leen las rutas del backend I1 en `backend/src/` ({len(reales)} rutas)")
existen = {nombre(e) for e in ENDPOINTS if e["estado"] in ("hecho", "ajustar")}
chk(existen <= reales, f"todo endpoint hecho o por ajustar existe en el código {sorted(existen - reales)}")
no_hechos = {nombre(e) for e in ENDPOINTS if e["estado"] in ("falta", "opcional")}
chk(not (no_hechos & reales), f"ningún endpoint que falta ya existe en el código {sorted(no_hechos & reales)}")
ajenos = {r for r, _ in A.AJENOS_I1}
chk(reales <= existen | ajenos,
    f"toda ruta del backend está en el catálogo o entre las ajenas {sorted(reales - existen - ajenos)}")

# =============================================================== D
print()
titulo("D. Rutas")
nombres = [nombre(e) for e in ENDPOINTS]
chk(len(nombres) == len(set(nombres)), f"ningún (método, ruta) repetido ({len(nombres)} endpoints)")
chk(all(e["metodo"] in ("GET", "POST", "PATCH", "DELETE") for e in ENDPOINTS),
    "solo GET, POST, PATCH y DELETE")
prohibidos = []
for regla in A.NO_AGREGAR:
    for e in ENDPOINTS:
        if re.search(regla["patron"], nombre(e)) and (
                "accesos" not in regla or e["acceso"] in regla["accesos"]):
            prohibidos.append(f"{nombre(e)}: {regla['que']}")
chk(not prohibidos, f"ninguna ruta hace algo de las {len(A.NO_AGREGAR)} que no se deben agregar"
    + "".join(f"\n         · {x}" for x in prohibidos))
ingles = {"users", "profile", "register", "login", "logout", "students", "report", "answers"}
nuevas_en_ingles = [nombre(e) for e in ENDPOINTS if e["estado"] in ("falta", "opcional")
                    and set(re.split(r"[/-]", e["ruta"])) & ingles]
chk(not nuevas_en_ingles, f"las rutas nuevas van en español {nuevas_en_ingles}")
chk(all(e["recibe"] and e["responde"] for e in ENDPOINTS), "todo endpoint dice qué recibe y qué responde")

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
