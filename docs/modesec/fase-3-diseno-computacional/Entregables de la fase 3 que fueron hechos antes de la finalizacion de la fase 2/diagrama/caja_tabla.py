"""Generador de diagramas ER en notacion 'caja-tabla' (Chen + extensiones):
atributos como filas de texto dentro de la caja, con columna PK/FK a la
izquierda, color por categoria de entidad, rombos verdes para relaciones.
Todo calculado desde el contenido (numero de atributos) -- nada a ojo.
"""

W, HEADER_H, ROW_H, PAD_TOP, PAD_BOT = 270, 30, 20, 8, 6
NEGRO, GRIS = "#111111", "#555555"

CATEGORIAS = {
    "propia":     dict(header="#E7DEF7", stroke="#7E63B8", texto="#2E1F4D", pk="#7E63B8"),
    "asociativa": dict(header="#FDF0D5", stroke="#C9922F", texto="#4D3708", pk="#C9922F"),
    "men":        dict(header="#F5EFE0", stroke="#A98B4E", texto="#4A3A16", pk="#A98B4E"),
    "debil":      dict(header="#FADCE0", stroke="#C0637B", texto="#4D1E29", pk="#C0637B"),
    "derivada":   dict(header="#ECECEC", stroke="#8A8A8A", texto="#333333", pk="#8A8A8A"),
}


def measure(attrs):
    return W, HEADER_H + PAD_TOP + len(attrs) * ROW_H + PAD_BOT


def entity(cx, top_y, name, cat, attrs, weak=False, dashed=False):
    """attrs: lista de (texto, etiqueta) -- etiqueta en {'PK','FK','PK,FK',''}.
    Devuelve (svg, geom) -- geom trae bordes y centro para conectar."""
    c = CATEGORIAS[cat]
    w, h = measure(attrs)
    x0, y0 = cx - w / 2, top_y
    x1, y1 = x0 + w, y0 + h
    cy = (y0 + y1) / 2
    dash = ' stroke-dasharray="6,5"' if dashed else ""
    svg = ""
    if weak:
        svg += (f'<rect x="{x0-5}" y="{y0-5}" width="{w+10}" height="{h+10}" '
                f'rx="6" ry="6" fill="none" stroke="{c["stroke"]}" stroke-width="2"/>\n')
    svg += (f'<rect x="{x0}" y="{y0}" width="{w}" height="{HEADER_H+8}" rx="5" ry="5" '
            f'fill="{c["header"]}" stroke="{c["stroke"]}" stroke-width="1.8"{dash}/>\n'
            f'<rect x="{x0}" y="{y0+HEADER_H-4}" width="{w}" height="8" fill="{c["header"]}"/>\n'
            f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="5" ry="5" '
            f'fill="#FFFFFF" stroke="{c["stroke"]}" stroke-width="1.8"{dash}/>\n'
            f'<path d="M {x0} {y0+HEADER_H} L {x0} {y0+5} Q {x0} {y0} {x0+5} {y0} '
            f'L {x1-5} {y0} Q {x1} {y0} {x1} {y0+5} L {x1} {y0+HEADER_H} Z" '
            f'fill="{c["header"]}" stroke="{c["stroke"]}" stroke-width="1.8"{dash}/>\n'
            f'<text x="{cx}" y="{y0+HEADER_H/2+5}" text-anchor="middle" font-family="Helvetica" '
            f'font-size="13" font-weight="700" fill="{c["texto"]}">{name}</text>\n')
    label_col_x = x0 + 8
    text_col_x = x0 + 62
    line_x = x0 + 54
    svg += f'<line x1="{line_x}" y1="{y0+HEADER_H}" x2="{line_x}" y2="{y1-6}" stroke="{c["stroke"]}" stroke-width="0.8" opacity="0.55"/>\n'
    ay = y0 + HEADER_H + PAD_TOP + 12
    for text, label in attrs:
        weight = "700" if label else "400"
        if label:
            svg += f'<text x="{label_col_x}" y="{ay}" font-family="Helvetica" font-size="9.5" font-weight="700" fill="{c["pk"]}">{label}</text>\n'
        svg += f'<text x="{text_col_x}" y="{ay}" font-family="Helvetica" font-size="11.5" font-weight="{weight}" fill="{NEGRO}">{text}</text>\n'
        ay += ROW_H
    geom = dict(x0=x0, y0=y0, x1=x1, y1=y1, cx=cx, cy=cy, w=w, h=h)
    return svg, geom


def diamond(cx, cy, label, identifying=False, derivada=False):
    rw, rh = 40, 33
    dash = ' stroke-dasharray="6,5"' if derivada else ""
    svg = ""
    if identifying:
        pts_out = f"{cx},{cy-rh-8} {cx+rw+8},{cy} {cx},{cy+rh+8} {cx-rw-8},{cy}"
        svg += f'<polygon points="{pts_out}" fill="#DDF0DD" stroke="#5F9E5F" stroke-width="1.6"{dash}/>\n'
    pts = f"{cx},{cy-rh} {cx+rw},{cy} {cx},{cy+rh} {cx-rw},{cy}"
    svg += f'<polygon points="{pts}" fill="#DDF0DD" stroke="#5F9E5F" stroke-width="1.6"{dash}/>\n'
    svg += f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-family="Helvetica" font-size="10.5" font-weight="700" fill="#1F4D1F">{label}</text>\n'
    return svg, dict(cx=cx, cy=cy, rw=rw + (8 if identifying else 0))


def _line(x1, y1, x2, y2, double=False, dashed=False):
    dash = ' stroke-dasharray="5,4"' if dashed else ""
    if double:
        return (f'<line x1="{x1}" y1="{y1-2.5}" x2="{x2}" y2="{y2-2.5}" stroke="{GRIS}" stroke-width="1.2"{dash}/>\n'
                f'<line x1="{x1}" y1="{y1+2.5}" x2="{x2}" y2="{y2+2.5}" stroke="{GRIS}" stroke-width="1.2"{dash}/>\n')
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GRIS}" stroke-width="1.2"{dash}/>\n'


def relate_h(box_a, box_b, label, card_a, card_b, total_a=False, total_b=False,
             identifying=False, derivada=False, gap=95, y=None):
    """A -- card_a -- <diamond> -- card_b -- B, A a la izquierda de B, horizontal."""
    cy = y if y is not None else box_a["cy"]
    mid = (box_a["x1"] + box_b["x0"]) / 2
    d_svg, d = diamond(mid, cy, label, identifying, derivada)
    svg = d_svg
    svg += _line(box_a["x1"], cy, mid - d["rw"], cy, total_a, derivada)
    svg += _line(mid + d["rw"], cy, box_b["x0"], cy, total_b, derivada)
    svg += f'<text x="{box_a["x1"]+14}" y="{cy-8}" text-anchor="middle" font-family="Helvetica" font-size="13" font-weight="700" fill="{NEGRO}">{card_a}</text>\n'
    svg += f'<text x="{box_b["x0"]-14}" y="{cy-8}" text-anchor="middle" font-family="Helvetica" font-size="13" font-weight="700" fill="{NEGRO}">{card_b}</text>\n'
    return svg


def relate_v(box_a, box_b, label, card_a, card_b, total_a=False, total_b=False,
             identifying=False, derivada=False, x=None):
    """A arriba, B abajo, vertical."""
    cx = x if x is not None else box_a["cx"]
    mid = (box_a["y1"] + box_b["y0"]) / 2
    d_svg, d = diamond(cx, mid, label, identifying, derivada)
    svg = d_svg
    svg += _line(cx, box_a["y1"], cx, mid - 33 - (8 if identifying else 0), total_a, derivada)
    svg += _line(cx, mid + 33 + (8 if identifying else 0), cx, box_b["y0"], total_b, derivada)
    svg += f'<text x="{cx+14}" y="{box_a["y1"]+16}" text-anchor="start" font-family="Helvetica" font-size="13" font-weight="700" fill="{NEGRO}">{card_a}</text>\n'
    svg += f'<text x="{cx+14}" y="{box_b["y0"]-8}" text-anchor="start" font-family="Helvetica" font-size="13" font-weight="700" fill="{NEGRO}">{card_b}</text>\n'
    return svg


def direct_v(box_a, box_b, card_a, card_b, total_a=False, total_b=False, x=None):
    """Conector directo sin rombo -- para cuando la entidad asociativa ES
    la relacion (ej. Respuesta -> Respuesta_Opcion), A arriba, B abajo."""
    cx = x if x is not None else box_a["cx"]
    svg = _line(cx, box_a["y1"], cx, box_b["y0"], total_a or total_b)
    svg += f'<text x="{cx+14}" y="{box_a["y1"]+16}" text-anchor="start" font-family="Helvetica" font-size="13" font-weight="700" fill="{NEGRO}">{card_a}</text>\n'
    svg += f'<text x="{cx+14}" y="{box_b["y0"]-8}" text-anchor="start" font-family="Helvetica" font-size="13" font-weight="700" fill="{NEGRO}">{card_b}</text>\n'
    return svg


def direct_h(box_a, box_b, card_a, card_b, total_a=False, total_b=False, y=None):
    """Igual que direct_v pero horizontal, A a la izquierda de B."""
    cy = y if y is not None else box_a["cy"]
    svg = _line(box_a["x1"], cy, box_b["x0"], cy, total_a or total_b)
    svg += f'<text x="{box_a["x1"]+16}" y="{cy-8}" text-anchor="middle" font-family="Helvetica" font-size="13" font-weight="700" fill="{NEGRO}">{card_a}</text>\n'
    svg += f'<text x="{box_b["x0"]-16}" y="{cy-8}" text-anchor="middle" font-family="Helvetica" font-size="13" font-weight="700" fill="{NEGRO}">{card_b}</text>\n'
    return svg


def routed(points, label=None, double=False, dashed=False):
    """Linea/relacion ruteada a 90 grados por puntos explicitos (para conexiones
    largas que no caben en linea recta sin cruzar otras cajas)."""
    d = "M " + " L ".join(f"{x} {y}" for x, y in points)
    dash = ' stroke-dasharray="5,4"' if dashed else ""
    svg = f'<path d="{d}" fill="none" stroke="{GRIS}" stroke-width="1.2"{dash}/>\n'
    if double:
        pass
    if label:
        x0, y0 = points[0]
        x1, y1 = points[1]
        if y0 == y1:
            lx, ly, anchor = x0 + (x1 - x0) * 0.5, y0 - 8, "middle"
        else:
            lx, ly, anchor = x0 + 14, y0 + (y1 - y0) * 0.5, "start"
        svg += f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" font-family="Helvetica" font-size="13" font-weight="700" fill="{NEGRO}">{label}</text>\n'
    return svg


def wrap_svg(width, height, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" font-family="Helvetica">\n'
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="#F3F5F8" rx="20" ry="20" stroke="#E3E7ED"/>\n'
            f'{body}</svg>')
