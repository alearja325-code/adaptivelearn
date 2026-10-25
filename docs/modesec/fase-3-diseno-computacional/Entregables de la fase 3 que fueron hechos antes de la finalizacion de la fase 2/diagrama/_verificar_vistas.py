"""Verifica la particion en vistas del MER.

Regla dura que hace legible un diagrama por bloques: cada relacion se
dibuja en EXACTAMENTE una vista (si aparece en dos, el lector no sabe
cual leer; si no aparece en ninguna, falta y nadie lo nota). Y cada
entidad debe aparecer al menos una vez.

Esto no se comprueba a ojo -- se comprueba aca.
"""
import sys
from datos_mer import ENTIDADES, RELACIONES, VISTAS

nombres = {e[0] for e in ENTIDADES}
err = []

# 1 -- toda relacion apunta a entidades que existen
for r in RELACIONES:
    for lado in ("a", "b"):
        if r[lado] not in nombres:
            err.append(f"relacion '{r['nombre']}': {lado}='{r[lado]}' no es una entidad declarada")

# 2 -- toda relacion vive en una vista declarada
for r in RELACIONES:
    if r["vista"] not in VISTAS:
        err.append(f"relacion '{r['nombre']}': vista {r['vista']} no existe")

# 3 -- ninguna relacion repetida (mismo par + mismo nombre)
vistos = {}
for r in RELACIONES:
    k = (r["nombre"], r["a"], r["b"])
    if k in vistos:
        err.append(f"relacion duplicada: {k} en vistas {vistos[k]} y {r['vista']}")
    vistos[k] = r["vista"]

# 4 -- toda entidad aparece en al menos una vista
en_vista = {}
for r in RELACIONES:
    lados = ["a", "b"] + (["asociativa"] if r.get("asociativa") else [])
    for lado in lados:
        en_vista.setdefault(r[lado], set()).add(r["vista"])
huerfanas = sorted(nombres - set(en_vista))
for h in huerfanas:
    err.append(f"entidad '{h}' no aparece en ninguna vista")

# ------------------------------------------------------------------ salida
reales = [r for r in RELACIONES if not r.get("derivada")]
deriv = [r for r in RELACIONES if r.get("derivada")]
print(f"Entidades: {len(ENTIDADES)}  (14 + REPORTE, que es vista derivada)")
print(f"Relaciones: {len(reales)} reales + {len(deriv)} derivadas")
print()
for v, (titulo, _) in VISTAS.items():
    rs = [r for r in RELACIONES if r["vista"] == v]
    ents = sorted({e for r in rs for e in
                   ([r["a"], r["b"]] + ([r["asociativa"]] if r.get("asociativa") else []))})
    print(f"  Vista {v} · {titulo}")
    print(f"     relaciones ({len(rs)}): {', '.join(r['nombre'] for r in rs)}")
    print(f"     entidades  ({len(ents)}): {', '.join(ents)}")
print()
if err:
    print("FALLO:")
    for e in err:
        print("  -", e)
    sys.exit(1)
print("OK - particion valida: cada relacion en exactamente una vista, "
      "cada entidad en al menos una.")
