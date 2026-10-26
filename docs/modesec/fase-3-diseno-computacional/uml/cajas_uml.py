"""Cajas UML de clase y de objeto, con su medida calculada.

Una caja se mide antes de ubicarse: el trazado de cada diagrama decide
donde va cada una conociendo su ancho y su alto reales.
"""
from lienzo import (ancho_texto, NEGRO, GRIS, GRIS_CLARO, BLANCO, CREMA,
                    AZUL_FILL, AZUL_STROKE, AZUL_TEXTO, VERDE_FILL, VERDE_STROKE)

T_MIEMBRO = 12
LH = 16           # alto de linea de un miembro
PAD = 7           # relleno vertical de cada compartimento
PAD_X = 12


def _cabecera(c):
    lineas = []
    if c.get("estereotipo"):
        lineas.append(("«" + c["estereotipo"] + "»", 11, 400))
    lineas.append((c["nombre"], 14, 700))
    if c.get("abstracta"):
        lineas.append(("{abstracta}", 11, 400))
    return lineas


def _miembros(c):
    attrs = [f"- {n}: {t}" for n, t in c["atributos"]]
    mets = [("+ " + x["firma"], x["estatico"]) for x in c["metodos"]]
    return attrs, mets


def medir_clase(c):
    cab = _cabecera(c)
    attrs, mets = _miembros(c)
    anchos = [ancho_texto(s, t, p >= 600) for s, t, p in cab]
    anchos += [ancho_texto(s, T_MIEMBRO) for s in attrs]
    anchos += [ancho_texto(s, T_MIEMBRO) for s, _ in mets]
    w = max(170, max(anchos) + 2 * PAD_X)
    h_cab = 10 + sum(t + 4 for _, t, _ in cab) + 4
    h_attr = 2 * PAD + LH * max(len(attrs), 0) if attrs else 14
    h_met = 2 * PAD + LH * len(mets) if mets else 14
    return round(w), round(h_cab + h_attr + h_met)


def caja_clase(L, c, x, y, w=None, fill_cab=AZUL_FILL, stroke=NEGRO):
    wm, h = medir_clase(c)
    w = w or wm
    dash = "6,4" if c.get("estereotipo") == "calculada" else None
    if c.get("estereotipo") == "enumeración":
        fill_cab = CREMA
    elif c.get("estereotipo") in ("servicio",):
        fill_cab = VERDE_FILL
    elif c.get("estereotipo") == "interfaz":
        fill_cab = BLANCO
    cab = _cabecera(c)
    h_cab = 10 + sum(t + 4 for _, t, _ in cab) + 4
    L.rect(x, y, w, h, fill=BLANCO, stroke=stroke, sw=1.5, dash=dash, id=c["nombre"])
    L.rect(x, y, w, h_cab, fill=fill_cab, stroke=stroke, sw=1.5, dash=dash)
    yy = y + 6
    for s, t, p in cab:
        yy += t + 4
        cursiva = c.get("abstracta") and p >= 600
        L.texto(x + w / 2, yy - 3, s, tam=t, peso=p, anchor="middle",
                color=NEGRO if p >= 600 else GRIS, cursiva=cursiva, dueno=c["nombre"])
    attrs, mets = _miembros(c)
    yy = y + h_cab
    h_attr = 2 * PAD + LH * len(attrs) if attrs else 14
    for i, s in enumerate(attrs):
        L.texto(x + PAD_X, yy + PAD + LH * i + 12, s, tam=T_MIEMBRO, dueno=c["nombre"])
    yy += h_attr
    L.crudo(f'<line x1="{x}" y1="{yy}" x2="{x + w}" y2="{yy}" stroke="{stroke}" stroke-width="1.2"/>')
    for i, (s, est) in enumerate(mets):
        L.texto(x + PAD_X, yy + PAD + LH * i + 12, s, tam=T_MIEMBRO, subrayado=est,
                dueno=c["nombre"])
    return (x, y, x + w, y + h)


def medir_enum(nombre, valores):
    lineas = ["«enumeración»", nombre] + valores
    w = max(ancho_texto(s, 12, i == 1) for i, s in enumerate(lineas)) + 2 * PAD_X
    return round(max(w, 130)), 46 + 2 * PAD + LH * len(valores)


def caja_enum(L, nombre, valores, x, y, w=None):
    wm, h = medir_enum(nombre, valores)
    w = w or wm
    L.rect(x, y, w, h, fill=BLANCO, stroke=NEGRO, sw=1.3, id=nombre)
    L.rect(x, y, w, 46, fill=CREMA, stroke=NEGRO, sw=1.3)
    L.texto(x + w / 2, y + 17, "«enumeración»", tam=11, color=GRIS, anchor="middle", dueno=nombre)
    L.texto(x + w / 2, y + 36, nombre, tam=13, peso=700, anchor="middle", dueno=nombre)
    for i, v in enumerate(valores):
        L.texto(x + PAD_X, y + 46 + PAD + LH * i + 12, v, tam=12, dueno=nombre)
    return (x, y, x + w, y + h)


# --------------------------------------------------------------- objetos
def medir_objeto(titulo, valores):
    lineas = [ancho_texto(titulo, 13, True)] + [ancho_texto(f"{k} = {v}", 12) for k, v in valores]
    return round(max(160, max(lineas) + 2 * PAD_X)), 34 + (2 * PAD + LH * len(valores) if valores else 10)


def caja_objeto(L, id, titulo, valores, x, y, w=None, fill=AZUL_FILL):
    wm, h = medir_objeto(titulo, valores)
    w = w or wm
    L.rect(x, y, w, h, fill=BLANCO, stroke=NEGRO, sw=1.5, id=id)
    L.rect(x, y, w, 34, fill=fill, stroke=NEGRO, sw=1.5)
    L.texto(x + w / 2, y + 22, titulo, tam=13, peso=700, anchor="middle", subrayado=True, dueno=id)
    for i, (k, v) in enumerate(valores):
        L.texto(x + PAD_X, y + 34 + PAD + LH * i + 12, f"{k} = {v}", tam=12, dueno=id)
    return (x, y, x + w, y + h)
