"""Lo que el catalogo de endpoints no escribe a mano: se calcula de las otras
fuentes de la Fase III. Lo usan `generar_api.py` y `_verificar_api.py`.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "uml"))
sys.path.insert(0, os.path.join(AQUI, "..", "modelo-relacional"))

import datos_api as A                                           # noqa: E402
import datos_casos_uso as CU                                    # noqa: E402
import datos_clases as CL                                       # noqa: E402
import datos_crud as CR                                         # noqa: E402
import datos_mr as MR                                           # noqa: E402
import datos_secuencias as SQ                                   # noqa: E402

ENDPOINTS = A.ENDPOINTS


def nombre(e):
    return f"{e['metodo']} {e['ruta']}"


def numero(e):
    """E-01 a E-35, en el orden del catalogo: el numero con que se reparte la tarea."""
    return f"E-{ENDPOINTS.index(e) + 1:02d}"


def incremento(e):
    return CU.SUBSISTEMAS[e["sub"]][1]


def operacion(op):
    """`Clase.metodo` -> (clase, metodo) del diagrama de clases, o (None, None)."""
    clase, _, metodo = op.partition(".")
    c = CL.POR_NOMBRE.get(clase)
    if not c:
        return None, None
    for m in c["metodos"]:
        if m["firma"].split("(")[0] == metodo:
            return c, m
    return c, None


def propios(e):
    """Los casos de uso del endpoint, menos los que otro de ellos incluye:
    POST /experiencias atiende CU-11, y CU-16 va dentro de CU-11."""
    incluidos = {d for o, t, d, _ in CU.RELACIONES if t == "include" and o in e["cus"]}
    return [c for c in e["cus"] if c not in incluidos] or e["cus"]


def llamadas_igu():
    """(secuencia, 'Clase.metodo', casos de uso de la secuencia): cada mensaje de
    la IGU a un objeto en los diagramas de secuencia."""
    out = []
    for s in SQ.SECUENCIAS:
        clase_de = {p[0]: p[2] for p in s["participantes"]}
        for p in s["pasos"]:
            if p[0] in ("m", "c") and p[1] == "igu" and clase_de.get(p[2]):
                out.append((s["id"], f"{clase_de[p[2]]}.{p[3].split('(')[0].strip()}", s["cus"]))
    return out


def secuencias(e):
    return sorted({sid for sid, op, cus in llamadas_igu()
                   if op == e["op"] and set(propios(e)) & set(cus)})


def cascada(e):
    """Entidades que un DELETE borra en cascada, de las FK ON DELETE CASCADE del MR."""
    if e["metodo"] != "DELETE":
        return []
    out = set()
    for ent, letras in e["crud"].items():
        if "D" in letras:
            out |= {t.upper() for t in CR.en_cascada(ent.lower(), MR.FKS)}
    return sorted(out)


def servicios_expuestos():
    """Operaciones de las clases «servicio»: las que la IGU puede pedir."""
    return [f"{c['nombre']}.{m['firma'].split('(')[0]}"
            for c in CL.SERVICIOS if c["estereotipo"] == "servicio" for m in c["metodos"]]
