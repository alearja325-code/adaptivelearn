"""Comprueba la coherencia interna del MER (datos_mer.py).

Tres cosas que un diagrama no deja ver y que el docente reviso en su
revision del 2026-09-01:

  1. Participacion. La linea doble (total) y el (min,max) de cada extremo
     dicen lo mismo dos veces: total si y solo si min >= 1. Si no
     coinciden, el diagrama se contradice a si mismo.
  2. Ciclos. Un ciclo en el MER es un camino que vuelve a su entidad de
     partida; si ese camino exige que algo coincida (la evidencia incluida
     sea del DBA de la experiencia, por ejemplo), hace falta una regla que
     lo cierre -- es exactamente el argumento del hallazgo H-4. El numero
     de ciclos independientes de un grafo conexo es aristas - nodos + 1;
     aqui se exige que CICLOS declare exactamente esa cantidad, que cada
     uno sea un camino real del grafo, y que sean independientes entre si
     (ninguno es combinacion de los otros). Asi no puede quedar un ciclo
     sin declarar.
  3. Marcas. Toda marca de atributo es una de las conocidas; las entidades
     debiles tienen relacion identificadora.

Uso:  python _verificar_mer.py
"""
import sys

from datos_mer import ENTIDADES, RELACIONES, CICLOS, DEBILES

fallas = []
ok = 0


def chk(cond, msg):
    global ok
    if cond:
        ok += 1
        print(f"   OK   {msg}")
    else:
        fallas.append(msg)
        print(f"   FALLA {msg}")


def minimo(part):
    return int(part.strip("()").split(",")[0])


print("=" * 66)
print("MER — coherencia interna")
print("=" * 66)

# ------------------------------------------------------- 1. participacion
malas = []
for r in RELACIONES:
    if r.get("derivada"):
        continue
    for lado in "ab":
        total, part = r[f"total_{lado}"], r[f"part_{lado}"]
        if total != (minimo(part) >= 1):
            malas.append(f"{r.get('id', r['nombre'])}.{lado}: total={total} y {part}")
chk(not malas, "línea doble ⇔ mínimo ≥ 1, en los dos extremos de cada relación "
    + ("" if not malas else f"(contradicen: {malas})"))

grupos = {}
for r in RELACIONES:
    if r.get("xor"):
        grupos.setdefault(r["xor"], []).append(r)
chk(all(len(g) >= 2 and len({x["a"] for x in g}) == 1 for g in grupos.values()),
    "cada grupo {xor} reúne al menos dos relaciones de una misma entidad")

# --------------------------------------------------------------- 2. ciclos
persistentes = {e[0] for e in ENTIDADES if e[1] != "derivada"}
aristas = []
for r in RELACIONES:
    if r.get("derivada"):
        continue
    if r.get("asociativa"):
        aristas += [frozenset((r["a"], r["asociativa"])), frozenset((r["asociativa"], r["b"]))]
    else:
        aristas.append(frozenset((r["a"], r["b"])))
chk(len(set(aristas)) == len(aristas), "no hay dos relaciones entre el mismo par de entidades "
    "(si las hubiera, cada par sería un ciclo más)" if len(set(aristas)) == len(aristas)
    else "hay relaciones paralelas: revisar el conteo de ciclos")

# conexo?
vistos, pila = set(), [next(iter(persistentes))]
while pila:
    n = pila.pop()
    if n in vistos:
        continue
    vistos.add(n)
    pila += [m for a in aristas if n in a for m in a if m != n]
chk(vistos == persistentes, f"el grafo de las {len(persistentes)} entidades persistentes es conexo")

rango = len(aristas) - len(persistentes) + 1
chk(len(CICLOS) == rango, f"{len(aristas)} aristas − {len(persistentes)} entidades + 1 = "
    f"{rango} ciclos independientes; declarados: {len(CICLOS)}")

indice = {a: i for i, a in enumerate(aristas)}
vectores = []
for c in CICLOS:
    cam = c["camino"]
    pasos = [frozenset(p) for p in zip(cam, cam[1:])]
    existe = cam[0] == cam[-1] and all(p in indice for p in pasos)
    chk(existe, f"{c['id']} es un camino cerrado del MER: {' → '.join(cam)}")
    v = 0
    for p in pasos:
        if p in indice:
            v ^= 1 << indice[p]
    vectores.append(v)

# independencia sobre GF(2): eliminacion gaussiana con mascaras de bits
base = []
for v in vectores:
    for b in base:
        v = min(v, v ^ b)
    if v:
        base.append(v)
chk(len(base) == len(CICLOS), "los ciclos declarados son independientes: ninguno es la "
    "combinación de otros, así que entre todos cubren cualquier ciclo del modelo")
for c in CICLOS:
    chk(bool(c["como"]), f"{c['id']}: dice cómo se cierra" + (f" ({c['regla']})" if c["regla"] else
                                                               " (no exige regla, y dice por qué)"))

# ---------------------------------------------------------------- 3. marcas
marcas = {m for e in ENTIDADES for _, m in e[2]}
chk(marcas <= {"PK", "PD", "D", "C", ""}, f"marcas de atributo conocidas ({sorted(marcas)})")
ident = {r["b"] for r in RELACIONES if r.get("ident")} | {r["a"] for r in RELACIONES if r.get("ident")}
chk(all(d in ident for d in DEBILES), "toda entidad débil tiene una relación identificadora")

print()
print("=" * 66)
if fallas:
    print(f"RESULTADO: {ok} correctas, {len(fallas)} FALLAS")
    for f in fallas:
        print(f"   · {f}")
    sys.exit(1)
print(f"RESULTADO: {ok} comprobaciones, todas correctas.")
print("=" * 66)
