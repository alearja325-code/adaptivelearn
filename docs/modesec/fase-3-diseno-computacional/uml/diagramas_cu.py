"""Diagramas de casos de uso: uno general y uno por subsistema.

El contenido (casos, relaciones) sale de `datos_casos_uso.py`; aqui solo
vive el trazado. Cada caso de uso se dibuja como PROPIO en exactamente un
diagrama; si otro diagrama lo necesita para mostrar un «include» o un
«extend», lo dibuja como REFERENCIA (elipse punteada, rotulada con su
subsistema). Es la misma regla de las "costuras" del MER.
"""
import math

from lienzo import (Lienzo, partir, NEGRO, GRIS, GRIS_CLARO, BLANCO, CREMA,
                    AZUL_FILL, AZUL_STROKE, AZUL_TEXTO)
from datos_casos_uso import POR_ID, RELACIONES, SUBSISTEMAS

RX, RY = 118, 42


# ------------------------------------------------------------- piezas
def actor(L, nombre, x, y):
    """Monigote UML. (x, y) es la cadera; devuelve sus puntos de enganche."""
    L.crudo(f'<circle cx="{x}" cy="{y - 40}" r="11" fill="{BLANCO}" stroke="{NEGRO}" stroke-width="1.6"/>'
            f'<line x1="{x}" y1="{y - 29}" x2="{x}" y2="{y}" stroke="{NEGRO}" stroke-width="1.6"/>'
            f'<line x1="{x - 18}" y1="{y - 18}" x2="{x + 18}" y2="{y - 18}" stroke="{NEGRO}" stroke-width="1.6"/>'
            f'<line x1="{x}" y1="{y}" x2="{x - 14}" y2="{y + 22}" stroke="{NEGRO}" stroke-width="1.6"/>'
            f'<line x1="{x}" y1="{y}" x2="{x + 14}" y2="{y + 22}" stroke="{NEGRO}" stroke-width="1.6"/>')
    L.cajas[nombre] = (x - 20, y - 52, x + 20, y + 23)
    lineas = partir(nombre, 13)
    for i, ln in enumerate(lineas):
        L.texto(x, y + 42 + 15 * i, ln, tam=13, peso=700, anchor="middle", dueno=nombre)
    return dict(der=(x + 22, y - 16), izq=(x - 22, y - 16), arriba=(x, y - 55),
                abajo=(x, y + 42 + 15 * (len(lineas) - 1) + 8), centro=(x, y - 16))


def caso(L, cid, cx, cy, ref=False):
    c = POR_ID[cid]
    L.elipse(cx, cy, RX, RY, fill=CREMA if ref else BLANCO,
             dash="6,4" if ref else None, id=cid)
    lineas = partir(c["nombre"], 26)
    rotulo = f"{cid} · {c['sub']}" if ref else cid
    y0 = cy - 7.5 * len(lineas) + 3
    L.texto(cx, y0, rotulo, tam=11.5, peso=700, color=GRIS_CLARO if ref else GRIS,
            anchor="middle", dueno=cid)
    for i, ln in enumerate(lineas):
        L.texto(cx, y0 + 15 * (i + 1), ln, tam=13, anchor="middle", dueno=cid)


def borde_elipse(c, hacia, rx=RX, ry=RY):
    dx, dy = hacia[0] - c[0], hacia[1] - c[1]
    t = 1 / math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
    return (c[0] + dx * t, c[1] + dy * t)


def borde_rect(r, hacia):
    """Punto donde la recta del centro de r hacia `hacia` corta su borde."""
    cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2
    dx, dy = hacia[0] - cx, hacia[1] - cy
    tx = (r[2] - cx) / abs(dx) if dx else math.inf
    ty = (r[3] - cy) / abs(dy) if dy else math.inf
    t = min(tx, ty)
    return (cx + dx * t, cy + dy * t)


def enganche(puntos, destino):
    x, y = puntos["centro"]
    if destino[0] > x + 60:
        return puntos["der"]
    if destino[0] < x - 60:
        return puntos["izq"]
    return puntos["arriba"] if destino[1] < y else puntos["abajo"]


def rotulo_linea(L, p, q, lineas, t=0.5, lado=1, sep=13, dueno=None):
    """Rotulo junto a una linea: en el punto t, corrido `sep` a un costado."""
    mx, my = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy) or 1
    nx, ny = -dy / n * lado, dx / n * lado        # normal hacia `lado`
    alto = 14 * len(lineas)
    # el bloque de texto se aleja de la linea por su lado mas cercano
    x = mx + nx * sep
    y = my + ny * sep
    if abs(nx) > 0.35:
        anchor = "start" if nx > 0 else "end"
    else:
        anchor = "middle"
    y0 = y - alto + 10 if ny < -0.35 else y + 10 if ny > 0.35 else y - alto / 2 + 10
    for i, ln in enumerate(lineas):
        L.texto(x, y0 + 14 * i, ln, tam=12, color=GRIS, anchor=anchor,
                cursiva=ln.startswith("["), dueno=dueno)


# ------------------------------------------------------------ diagramas
DIAGRAMAS = [
    dict(archivo="cu-1-acceso-crear-cuenta.svg",
         titulo="Casos de uso 1 · SUB-01 Acceso y perfil (1 de 2): crear la cuenta",
         ancho=1300, alto=760, marco=(260, 70, 1010, 520),
         actores=[("Visitante", 110, 320), ("Servicio de correo", 1170, 166),
                  ("Proveedor de identidad", 440, 660)],
         casos=[("CU-01", 440, 160), ("CU-02", 440, 440), ("CU-03", 820, 160),
                ("CU-04", 820, 300), ("CU-05", 820, 440)],
         asociaciones=[("Visitante", "CU-01"), ("Visitante", "CU-02"),
                       ("Servicio de correo", "CU-03"), ("Proveedor de identidad", "CU-02")],
         rotulos={("CU-01", "CU-03"): (0.5, -1), ("CU-01", "CU-04"): (0.42, -1),
                  ("CU-04", "CU-05"): (0.5, -1), ("CU-04", "CU-02"): (0.55, -1)}),
    dict(archivo="cu-2-acceso-sesion-perfil.svg",
         titulo="Casos de uso 2 · SUB-01 Acceso y perfil (2 de 2): sesión y perfil",
         ancho=1300, alto=760, marco=(290, 70, 1010, 690),
         actores=[("Usuario", 130, 350), ("Docente", 70, 600), ("Estudiante", 200, 600),
                  ("Proveedor de identidad", 1170, 136), ("Servicio de correo", 1170, 396)],
         casos=[("CU-06", 470, 260), ("CU-07", 470, 380), ("CU-08", 470, 500),
                ("CU-09", 470, 620)],
         refs=[("CU-02", 470, 140), ("CU-03", 850, 380)],
         asociaciones=[("Usuario", "CU-02"), ("Usuario", "CU-06"), ("Usuario", "CU-07"),
                       ("Usuario", "CU-08"), ("Usuario", "CU-09"),
                       ("Proveedor de identidad", "CU-02"), ("Servicio de correo", "CU-03")],
         generalizaciones=[("Docente", "Usuario"), ("Estudiante", "Usuario")],
         rotulos={("CU-07", "CU-03"): (0.5, -1)}),
    dict(archivo="cu-3-experiencias-catalogo.svg",
         titulo="Casos de uso 3 · SUB-02 Gestión de experiencias y SUB-06 Catálogo curricular",
         ancho=1340, alto=830, marco=(260, 70, 1050, 790),
         actores=[("Docente", 110, 430), ("Servicio de IA", 1200, 316)],
         casos=[("CU-10", 450, 140), ("CU-11", 450, 260), ("CU-12", 450, 380),
                ("CU-13", 450, 500), ("CU-14", 450, 620), ("CU-15", 450, 740),
                ("CU-31", 850, 196)],
         refs=[("CU-16", 850, 326)],
         asociaciones=[("Docente", c) for c in
                       ("CU-10", "CU-11", "CU-12", "CU-13", "CU-14", "CU-15")]
         + [("Servicio de IA", "CU-16")],
         rotulos={("CU-11", "CU-31"): (0.5, -1), ("CU-11", "CU-16"): (0.5, 1)}),
    dict(archivo="cu-4-banco.svg",
         titulo="Casos de uso 4 · SUB-03 Banco de preguntas",
         ancho=1340, alto=650, marco=(260, 70, 1050, 610),
         actores=[("Docente", 110, 360), ("Servicio de IA", 1200, 166)],
         casos=[("CU-16", 850, 160), ("CU-17", 450, 400), ("CU-18", 850, 290),
                ("CU-19", 850, 410), ("CU-20", 850, 530)],
         refs=[("CU-11", 450, 160)],
         asociaciones=[("Docente", "CU-11"), ("Docente", "CU-17"), ("Servicio de IA", "CU-16")],
         rotulos={("CU-11", "CU-16"): (0.5, -1), ("CU-18", "CU-17"): (0.30, 1),
                  ("CU-19", "CU-17"): (0.30, 1), ("CU-20", "CU-17"): (0.30, -1)}),
    dict(archivo="cu-5-diagnostico.svg",
         titulo="Casos de uso 5 · SUB-04 Diagnóstico",
         ancho=1120, alto=640, marco=(260, 70, 1050, 600),
         actores=[("Estudiante", 110, 346)],
         casos=[("CU-21", 450, 140), ("CU-22", 450, 260), ("CU-23", 450, 380),
                ("CU-26", 450, 520), ("CU-24", 850, 380), ("CU-25", 850, 520)],
         asociaciones=[("Estudiante", c) for c in ("CU-21", "CU-22", "CU-23", "CU-26")],
         rotulos={("CU-23", "CU-24"): (0.5, -1), ("CU-24", "CU-25"): (0.5, -1)}),
    dict(archivo="cu-6-reporte.svg",
         titulo="Casos de uso 6 · SUB-05 Reporte y seguimiento",
         ancho=1120, alto=530, marco=(260, 70, 1050, 490),
         actores=[("Docente", 110, 296)],
         casos=[("CU-27", 450, 150), ("CU-28", 450, 280), ("CU-29", 450, 410),
                ("CU-30", 850, 215)],
         asociaciones=[("Docente", c) for c in ("CU-27", "CU-28", "CU-29")],
         rotulos={("CU-27", "CU-30"): (0.5, -1), ("CU-28", "CU-30"): (0.5, 1)}),
]


def dibujar(d):
    L = Lienzo(d["ancho"], d["alto"])
    L.texto(32, 40, d["titulo"], tam=15, peso=700, color="#333333")
    x0, y0, x1, y1 = d["marco"]
    L.rect(x0, y0, x1 - x0, y1 - y0, fill="#FFFFFF", stroke=GRIS, sw=1.4, rx=6)
    L.texto(x0 + 14, y0 + 22, "AdaptiveLearn", tam=13, peso=700, color=GRIS)
    pos = {}
    for cid, x, y in d.get("casos", []):
        caso(L, cid, x, y)
        pos[cid] = (x, y)
    for cid, x, y in d.get("refs", []):
        caso(L, cid, x, y, ref=True)
        pos[cid] = (x, y)
    actores = {n: actor(L, n, x, y) for n, x, y in d["actores"]}
    for a, cid in d["asociaciones"]:
        p = enganche(actores[a], pos[cid])
        q = borde_elipse(pos[cid], p)
        L.linea([p, q], color=NEGRO, sw=1.3, permitidos={a, cid}, desc=f"{a}—{cid}")
    for hijo, padre in d.get("generalizaciones", []):
        p, q = actores[hijo]["arriba"], actores[padre]["abajo"]
        L.linea([p, q], color=NEGRO, sw=1.3, fin="herencia", permitidos={hijo, padre},
                desc=f"{hijo}▷{padre}")
    for o, tipo, dst, guarda in RELACIONES:
        if o in pos and dst in pos:
            p = borde_elipse(pos[o], pos[dst])
            q = borde_elipse(pos[dst], pos[o])
            L.linea([p, q], color=NEGRO, sw=1.3, dash="7,5", fin="abierta",
                     permitidos={o, dst}, desc=f"{o}→{dst}")
            t, lado = d["rotulos"][(o, dst)]
            lineas = [f"«{tipo}»"] + ([f"[{guarda}]"] if guarda and tipo == "extend" else [])
            rotulo_linea(L, p, q, lineas, t=t, lado=lado)
    L.texto(32, d["alto"] - 18,
            "Elipse punteada: caso de uso de otro diagrama, por referencia. «include»: el caso de origen "
            "siempre lo ejecuta. «extend»: se agrega al caso de destino solo bajo la condición entre corchetes.",
            tam=11.5, color=GRIS_CLARO)
    return L


# ------------------------------------------------------ diagrama general
PAQUETES = [("SUB-01", 470, 90), ("SUB-04", 470, 230), ("SUB-02", 470, 380),
            ("SUB-03", 470, 520), ("SUB-05", 470, 660), ("SUB-06", 1000, 380)]


def paquete(L, sub, x, y, w=360, h=72):
    nombre, inc = SUBSISTEMAS[sub]
    L.rect(x, y - 16, 96, 16, fill=AZUL_FILL, stroke=AZUL_STROKE, sw=1.4)
    L.rect(x, y, w, h, fill=AZUL_FILL, stroke=AZUL_STROKE, sw=1.4, id=sub)
    L.texto(x + 14, y + 28, sub, tam=13, peso=700, color=AZUL_TEXTO, dueno=sub)
    L.texto(x + 14, y + 50, nombre, tam=14, color=AZUL_TEXTO, dueno=sub)
    L.texto(x + w - 12, y + 28, f"incremento {inc}", tam=11.5, color=GRIS,
            anchor="end", dueno=sub)
    return (x, y, x + w, y + h)


def dibujar_general():
    L = Lienzo(1480, 830)
    L.texto(32, 40, "Casos de uso 0 · Vista general: actores y subsistemas", tam=15,
            peso=700, color="#333333")
    cajas = {}
    for sub, x, y in PAQUETES:
        cajas[sub] = paquete(L, sub, x, y, w=300 if sub == "SUB-06" else 360)
    actores = {n: actor(L, n, x, y) for n, x, y in [
        ("Visitante", 130, 140), ("Docente", 130, 540), ("Proveedor de identidad", 1380, 110),
        ("Servicio de correo", 1380, 250), ("Estudiante", 1380, 400), ("Servicio de IA", 1380, 590)]}
    # (actor, paquete, altura de llegada sobre el costado del paquete que
    # mira al actor): cada linea entra por su propio punto, sin compartirlo
    uso = [("Visitante", "SUB-01", 26), ("Docente", "SUB-01", 60), ("Docente", "SUB-02", 36),
           ("Docente", "SUB-03", 36), ("Docente", "SUB-05", 36), ("Estudiante", "SUB-01", 62),
           ("Estudiante", "SUB-04", 36), ("Proveedor de identidad", "SUB-01", 14),
           ("Servicio de correo", "SUB-01", 38), ("Servicio de IA", "SUB-03", 36)]
    for a, sub, dy in uso:
        r = cajas[sub]
        c = ((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
        p = enganche(actores[a], c)
        q = (r[0] if p[0] < r[0] else r[2], r[1] + dy)
        if (a, sub) == ("Docente", "SUB-01"):
            # en recta atravesaria SUB-04: sube por el carril libre de x=400
            ruta = [p, (400, 300), (400, q[1]), q]
        else:
            ruta = [p, q]
        L.linea(ruta, color=NEGRO, sw=1.3, permitidos={a, sub}, desc=f"{a}—{sub}")
    # dependencias entre subsistemas
    r2, r6, r3 = cajas["SUB-02"], cajas["SUB-06"], cajas["SUB-03"]
    ym = (r2[1] + r2[3]) / 2
    p, q = (r2[2], ym), (r6[0], ym)
    L.linea([p, q], color=NEGRO, sw=1.3, dash="7,5", fin="abierta", permitidos={"SUB-02", "SUB-06"},
            desc="SUB-02→SUB-06")
    rotulo_linea(L, p, q, ["«include»", "CU-11 → CU-31"], t=0.5, lado=-1, sep=8)
    p, q = (r2[0] + 210, r2[3]), (r3[0] + 210, r3[1])
    L.linea([p, q], color=NEGRO, sw=1.3, dash="7,5", fin="abierta", permitidos={"SUB-02", "SUB-03"},
            desc="SUB-02→SUB-03")
    rotulo_linea(L, p, q, ["«include»", "CU-11 → CU-16"], t=0.5, lado=-1, sep=10)
    L.texto(32, 812, "Cada paquete se detalla en su diagrama (1 a 6). Las flechas punteadas son los "
            "«include» que cruzan de un subsistema a otro.", tam=11.5, color=GRIS_CLARO)
    return L


def todos():
    """[(archivo, titulo, Lienzo)] -- el general primero."""
    salida = [("cu-0-general.svg", "Casos de uso 0 · Vista general", dibujar_general())]
    for d in DIAGRAMAS:
        salida.append((d["archivo"], d["titulo"], dibujar(d)))
    return salida
