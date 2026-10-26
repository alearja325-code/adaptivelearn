"""Diagrama de objetos, en dos vistas del mismo momento.

Vista 1: la experiencia publicada y su banco (lo que Ana hizo).
Vista 2: el diagnostico de Luis, en curso (lo que Luis hizo).
Los objetos de la vista 1 que la vista 2 necesita se dibujan alli como
costura: borde punteado, sin valores, "ver vista 1".
"""
from lienzo import Lienzo, ancho_texto, partir, NEGRO, GRIS, GRIS_CLARO, CREMA, BLANCO
from cajas_uml import caja_objeto, medir_objeto
from datos_objetos import OBJETOS, ENLACES, NOTAS, OBJETO_ASOCIACION


def titulo_obj(oid):
    return f"{oid} : {OBJETOS[oid][0]}"


def objeto(L, oid, x, y):
    return caja_objeto(L, oid, titulo_obj(oid), OBJETOS[oid][1], x, y)


def costura(L, oid, x, y):
    t = titulo_obj(oid)
    w = max(150, ancho_texto(t, 13, True) + 24)
    L.rect(x, y, w, 46, fill=CREMA, stroke=GRIS, sw=1.3, dash="6,4", id=oid)
    L.texto(x + w / 2, y + 20, t, tam=13, peso=700, anchor="middle", subrayado=True,
            color=GRIS, dueno=oid)
    L.texto(x + w / 2, y + 37, "ver vista 1", tam=10.5, anchor="middle", color=GRIS_CLARO, dueno=oid)
    return (x, y, x + w, y + 46)


def nota(L, nid, x, y, w, hacia=None):
    """Nota UML (rectangulo con la esquina doblada), opcionalmente enganchada."""
    lineas = []
    for parrafo in [NOTAS[nid]]:
        lineas += partir(parrafo, int((w - 20) / 6.4))
    h = 16 + 15 * len(lineas)
    d = 12
    L.crudo(f'<path d="M{x},{y} L{x + w - d},{y} L{x + w},{y + d} L{x + w},{y + h} L{x},{y + h} Z" '
            f'fill="#FFFBEA" stroke="{GRIS_CLARO}" stroke-width="1.2"/>'
            f'<path d="M{x + w - d},{y} L{x + w - d},{y + d} L{x + w},{y + d}" fill="none" '
            f'stroke="{GRIS_CLARO}" stroke-width="1.2"/>')
    L.cajas[nid] = (x, y, x + w, y + h)
    for i, ln in enumerate(lineas):
        L.texto(x + 10, y + 19 + 15 * i, ln, tam=11.5, color="#5A4A1A", dueno=nid)
    if hacia:
        oid, p = hacia
        L.linea([p[0], p[1]], color=GRIS_CLARO, sw=1.1, dash="3,3", permitidos={nid, oid},
                desc=f"nota {nid}")
    return (x, y, x + w, y + h)


def enlace(L, a, b, ruta):
    L.linea(ruta, color=NEGRO, sw=1.3, permitidos={a, b}, desc=f"{a}—{b}")


def mitad(B, n, eje):
    x0, y0, x1, y1 = B[n]
    return (x0 + x1) / 2 if eje == "x" else (y0 + y1) / 2


# ================================================================= vista 1
def vista1():
    L = Lienzo(1900, 1060)
    L.texto(32, 40, "Diagrama de objetos · vista 1 de 2 — La experiencia publicada "
            "(martes 4 de noviembre de 2026, 09:06)", tam=16, peso=700, color="#333333")
    B = {}
    for oid, x, y in [("dba", 760, 70), ("d1", 40, 250), ("ev1", 330, 250), ("exp3", 770, 250),
                      ("ev2", 1320, 250), ("d2", 1580, 250), ("ee1", 330, 470), ("ee2", 1320, 470),
                      ("ana", 880, 520), ("c1", 880, 690), ("it11", 40, 640), ("it12", 250, 640),
                      ("it13", 460, 640), ("it14", 670, 640), ("it21", 1320, 640),
                      ("op1", 40, 880), ("op2", 250, 880)]:
        B[oid] = objeto(L, oid, x, y)
    cy = lambda n: mitad(B, n, "y")
    cx = lambda n: mitad(B, n, "x")
    yd = B["dba"][1] + 40
    enlace(L, "dba", "ev1", [(B["dba"][0], yd), (440, yd), (440, B["ev1"][1])])
    enlace(L, "dba", "ev2", [(B["dba"][2], yd), (1430, yd), (1430, B["ev2"][1])])
    enlace(L, "ev1", "d1", [(B["ev1"][0], cy("ev1")), (B["d1"][2], cy("ev1"))])
    enlace(L, "ev2", "d2", [(B["ev2"][2], cy("ev2")), (B["d2"][0], cy("ev2"))])
    enlace(L, "exp3", "dba", [(930, B["exp3"][1]), (930, B["dba"][3])])
    enlace(L, "ev1", "ee1", [(440, B["ev1"][3]), (440, B["ee1"][1])])
    enlace(L, "ev2", "ee2", [(1430, B["ev2"][3]), (1430, B["ee2"][1])])
    ye = cy("ee1")
    enlace(L, "exp3", "ee1", [(B["exp3"][0], 360), (650, 360), (650, ye), (B["ee1"][2], ye)])
    enlace(L, "exp3", "ee2", [(B["exp3"][2], 360), (1220, 360), (1220, ye), (B["ee2"][0], ye)])
    enlace(L, "exp3", "ana", [(930, B["exp3"][3]), (930, B["ana"][1])])
    enlace(L, "c1", "ana", [(930, B["c1"][1]), (930, B["ana"][3])])
    for it in ("it11", "it12", "it13", "it14"):
        enlace(L, "ee1", it, [(cx("ee1"), B["ee1"][3]), (cx(it), B[it][1])])
    enlace(L, "ee2", "it21", [(1430, B["ee2"][3]), (1430, B["it21"][1])])
    for op in ("op1", "op2"):
        enlace(L, "it11", op, [(cx("it11"), B["it11"][3]), (cx(op), B[op][1])])
    nota(L, "n_banco", 470, 880, 400)
    nota(L, "n_it21", 1560, 660, 300, hacia=("it21", [(1560, 690), (B["it21"][2], 690)]))
    L.texto(32, 1040, "Rectángulo con nombre subrayado: un objeto («nombre : Clase») con los valores "
            "que tiene en este momento. Línea: un enlace, instancia de una asociación del diagrama "
            "de clases. Textos, correos y códigos son ilustrativos.", tam=11.5, color=GRIS_CLARO)
    return L


# ================================================================= vista 2
def vista2():
    L = Lienzo(1900, 1130)
    L.texto(32, 40, "Diagrama de objetos · vista 2 de 2 — El diagnóstico de Luis, en curso "
            "(mismo momento)", tam=16, peso=700, color="#333333")
    B = {}
    for oid, x, y in [("c2", 330, 80), ("luis", 330, 290), ("ins", 330, 520),
                      ("res1", 330, 780)]:
        B[oid] = objeto(L, oid, x, y)
    B["exp3"] = costura(L, "exp3", 40, 529)
    B["ee1"] = costura(L, "ee1", 330, 960)
    filas = [190 + 200 * k for k in range(5)]
    items = ["it11", "it12", "it13", "it14", "it21"]
    for k, (p, it) in enumerate(zip(["p1", "p2", "p3", "p4", "p5"], items)):
        B[p] = objeto(L, p, 760, filas[k])
        B[it] = costura(L, it, 820, filas[k] - 80)
    for k, r in enumerate(["r1", "r2", "r3", "r4"]):
        B[r] = objeto(L, r, 1160, filas[k] - 8)
    cy = lambda n: mitad(B, n, "y")
    cx = lambda n: mitad(B, n, "x")
    xb = cx("c2")
    enlace(L, "c2", "luis", [(xb, B["c2"][3]), (xb, B["luis"][1])])
    enlace(L, "luis", "ins", [(xb, B["luis"][3]), (xb, B["ins"][1])])
    enlace(L, "ins", "res1", [(xb, B["ins"][3]), (xb, B["res1"][1])])
    enlace(L, "ee1", "res1", [(xb, B["ee1"][1]), (xb, B["res1"][3])])
    enlace(L, "ins", "exp3", [(B["ins"][0], cy("exp3")), (B["exp3"][2], cy("exp3"))])
    for p in ["p1", "p2", "p3", "p4", "p5"]:
        enlace(L, "ins", p, [(B["ins"][2], cy("ins")), (B[p][0], cy(p))])
    for p, it in zip(["p1", "p2", "p3", "p4", "p5"], items):
        x = cx(it)
        enlace(L, it, p, [(x, B[it][3]), (x, B[p][1])])
    for p, r in zip(["p1", "p2", "p3", "p4"], ["r1", "r2", "r3", "r4"]):
        enlace(L, p, r, [(B[p][2], cy(p)), (B[r][0], cy(p))])
    # r1 —selecciona— op1, con el objeto de la clase asociacion colgando
    B["op1"] = costura(L, "op1", 1640, cy("p1") - 23)
    ys = cy("p1")
    enlace(L, "r1", "op1", [(B["r1"][2], ys), (B["op1"][0], ys)])
    ro, _ = OBJETO_ASOCIACION
    B[ro] = objeto(L, ro, 1440, 66)
    xm = (B["r1"][2] + B["op1"][0]) / 2
    L.linea([(xm, ys), (xm, B[ro][3])], color=NEGRO, sw=1.1, dash="4,4", permitidos={ro},
            desc="objeto de la clase asociación")
    nota(L, "n_c2", 40, 80, 270, hacia=("c2", [(310, 120), (B["c2"][0], 120)]))
    nota(L, "n_luis", 40, 290, 270, hacia=("luis", [(310, 330), (B["luis"][0], 330)]))
    nota(L, "n_res1", 40, 760, 270, hacia=("res1", [(310, 820), (B["res1"][0], 820)]))
    nota(L, "n_p5", 1160, filas[4] - 4, 380, hacia=("p5", [(1160, cy("p5")), (B["p5"][2], cy("p5"))]))
    L.texto(32, 1110, "Costura (borde punteado, «ver vista 1»): el mismo objeto de la vista 1, sin "
            "repetir sus valores. Punteado desde un enlace: el objeto de la clase asociación "
            "RespuestaOpcion de ese enlace.", tam=11.5, color=GRIS_CLARO)
    return L


def todos():
    return [("objetos-1-experiencia.svg", "Diagrama de objetos · vista 1", vista1()),
            ("objetos-2-diagnostico.svg", "Diagrama de objetos · vista 2", vista2())]
