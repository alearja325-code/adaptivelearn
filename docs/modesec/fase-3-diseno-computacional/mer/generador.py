"""Generador de diagramas ER en notacion Chen, por bloques.
Sistema de coordenadas exacto -- nada a ojo, todo calculado.
"""

# ---------- Tokens del diagrama (consistentes en los 6 bloques) ----------
ENTIDAD_W, ENTIDAD_H = 180, 60
ROMBO_W, ROMBO_H = 130, 70
ATRIB_W, ATRIB_H = 110, 40
GAP_ATRIB = 20          # espacio horizontal entre elipses de atributos
FAN_DROP = 110          # distancia vertical de la entidad a su fila de atributos
ROW_Y = 110             # y del centro de la fila principal de entidades
MARGIN = 60

AZUL_FILL, AZUL_STROKE = "#DCE8FA", "#3B7DD8"
NEGRO = "#111111"
GRIS_MEDIO = "#555555"
GRIS_ATRIB = "#888888"
BLANCO = "#FFFFFF"
REF_FILL = "#F5F3EE"
CARD_FONT = "13"
LABEL_FONT = "14"
ATTR_FONT = "12.5"

def entity_box(cx, cy, label, fill=BLANCO, dashed=False, double=False):
    # el ancho se adapta al nombre: con ancho fijo, EXPERIENCIA_EVIDENCIA
    # y RESPUESTA_OPCION rozaban los bordes de su propia caja
    w = max(ENTIDAD_W, len(label) * 8.7 + 30)
    x, y = cx - w / 2, cy - ENTIDAD_H / 2
    svg = ""
    dash = ' stroke-dasharray="6,5"' if dashed else ""
    if double:
        svg += f'<rect x="{x-5}" y="{y-5}" width="{w+10}" height="{ENTIDAD_H+10}" fill="none" stroke="{NEGRO}" stroke-width="2"/>\n'
    svg += f'<rect x="{x}" y="{y}" width="{w}" height="{ENTIDAD_H}" fill="{fill}" stroke="{NEGRO}" stroke-width="2"{dash}/>\n'
    svg += f'<text x="{cx}" y="{cy+5}" text-anchor="middle" font-family="Helvetica" font-size="{LABEL_FONT}" font-weight="700" fill="{NEGRO}">{label}</text>\n'
    # el bbox devuelto es el borde VISUAL real: si es doble, el exterior
    # (5px mas afuera) -- lineas y atributos deben partir de ahi, no del
    # recuadro interior, o quedan atravesados por el segundo borde.
    b = 5 if double else 0
    return svg, (x - b, y - b, x + w + b, y + ENTIDAD_H + b)

def relation_diamond(cx, cy, label):
    pts = f"{cx},{cy-ROMBO_H/2} {cx+ROMBO_W/2},{cy} {cx},{cy+ROMBO_H/2} {cx-ROMBO_W/2},{cy}"
    svg = f'<polygon points="{pts}" fill="{AZUL_FILL}" stroke="{AZUL_STROKE}" stroke-width="1.5"/>\n'
    svg += f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-family="Helvetica" font-size="{CARD_FONT}" fill="#1C3A5E">{label}</text>\n'
    return svg, (cx - ROMBO_W/2, cy, cx + ROMBO_W/2, cy)

def connector(x1, y1, x2, y2, card_a=None, card_b=None):
    svg = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GRIS_MEDIO}" stroke-width="1.2"/>\n'
    # en linea horizontal, la etiqueta se despega subiendola (offset en Y);
    # en linea vertical subir no la aparta del trazo -- hay que despegarla
    # al lado (offset en X, hacia la derecha, que es el espacio libre).
    vertical = (x1 == x2)
    if card_a:
        lx, ly = x1 + (x2 - x1) * 0.16, y1 + (y2 - y1) * 0.16
        if vertical:
            lx, ly, anchor = lx + 14, ly + 4, "start"
        else:
            ly, anchor = ly - 8, "middle"
        svg += f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" font-family="Helvetica" font-size="{CARD_FONT}" font-weight="700" fill="{NEGRO}">{card_a}</text>\n'
    if card_b:
        lx, ly = x1 + (x2 - x1) * 0.84, y1 + (y2 - y1) * 0.84
        if vertical:
            lx, ly, anchor = lx + 14, ly + 4, "start"
        else:
            ly, anchor = ly - 8, "middle"
        svg += f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" font-family="Helvetica" font-size="{CARD_FONT}" font-weight="700" fill="{NEGRO}">{card_b}</text>\n'
    return svg

def ortho_connector(x1, y1, x2, y2, card=None):
    """Linea de x1,y1 a x2,y2 usando solo tramos a 0, 45 o 90 grados --
    nunca una diagonal a angulo libre. Un tramo recto (el eje que domina)
    mas un tramo a 45 grados que entra al punto de destino."""
    dx, dy = x2 - x1, y2 - y1
    pts = [(x1, y1)]
    if dx == 0 or dy == 0 or abs(dx) == abs(dy):
        pts.append((x2, y2))
    elif abs(dx) > abs(dy):
        run = abs(dx) - abs(dy)
        mx = x1 + (run if dx > 0 else -run)
        pts.append((mx, y1))
        pts.append((x2, y2))
    else:
        run = abs(dy) - abs(dx)
        my = y1 + (run if dy > 0 else -run)
        pts.append((x1, my))
        pts.append((x2, y2))

    d = "M " + " L ".join(f"{px} {py}" for px, py in pts)
    svg = f'<path d="{d}" fill="none" stroke="{GRIS_MEDIO}" stroke-width="1.2"/>\n'
    if card:
        p0, p1 = pts[0], pts[1]
        lx, ly = p0[0] + (p1[0] - p0[0]) * 0.4, p0[1] + (p1[1] - p0[1]) * 0.4
        if p0[1] == p1[1]:
            ly -= 8
            anchor = "middle"
        elif p0[0] == p1[0]:
            lx += 12
            anchor = "start"
        else:
            ly -= 10
            anchor = "middle"
        svg += f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" font-family="Helvetica" font-size="{CARD_FONT}" font-weight="700" fill="{NEGRO}">{card}</text>\n'
    return svg

ATRIB_GAP_V = 18  # espacio vertical entre elipses apiladas

def attribute_stack(entity_cx, entity_bottom_y, attrs, first_row_y, side="left", column_dx=0):
    """attrs: lista de (texto, es_llave_primaria). Columna vertical bajo entity_cx,
    con una sola linea-espina que baja derecho y un tramo corto a cada elipse
    (evita el efecto zigzag de una curva por atributo).
    side="left" o "right": de que lado cuelga la espina -- se usa "right" cuando
    el lado izquierdo de la entidad ya lo ocupa una linea de relacion."""
    n = len(attrs)
    sign = -1 if side == "left" else 1
    col_cx = entity_cx + column_dx        # centro de la columna de elipses
    spine_x = col_cx + sign * (ENTIDAD_W / 2 + 34)
    hook_x = entity_cx + sign * (ENTIDAD_W / 2 - 16)
    centers = [first_row_y + i * (ATRIB_H + ATRIB_GAP_V) for i in range(n)]
    last_bottom = centers[-1] + ATRIB_H / 2

    svg = ""
    # gancho curvo desde la entidad hasta el inicio de la espina
    svg += (f'<path d="M {hook_x} {entity_bottom_y} '
            f'C {hook_x} {entity_bottom_y+30}, '
            f'{spine_x} {entity_bottom_y+10}, '
            f'{spine_x} {centers[0]}" '
            f'fill="none" stroke="{GRIS_ATRIB}" stroke-width="1"/>\n')
    # espina recta hasta el ultimo atributo
    if n > 1:
        svg += f'<line x1="{spine_x}" y1="{centers[0]}" x2="{spine_x}" y2="{centers[-1]}" stroke="{GRIS_ATRIB}" stroke-width="1"/>\n'

    for cy, (text, marca) in zip(centers, attrs):
        pk = marca.startswith("PK")
        # PD = llave parcial (discriminador) de una entidad debil: en Chen va
        # con subrayado punteado, no en elipse negra -- sola no identifica
        parcial = marca == "PD"
        # D = derivado que se guarda (ADR-021); C = calculado, no se guarda.
        # En Chen, todo atributo derivado va en elipse PUNTEADA.
        derivado = marca in ("D", "C")
        sufijo = {"PD": "", "D": " (derivado · se guarda)", "C": " (calculado)"}.get(
            marca, f" ({marca})" if marca else "")
        etiqueta = text + sufijo
        # el ancho de la elipse se calcula del texto -- con ancho fijo, los
        # nombres largos (numero_evidencia, aplica_formato_cerrado) se salian
        rx = max(ATRIB_W / 2, len(etiqueta) * 3.55 + 12)
        svg += f'<line x1="{spine_x}" y1="{cy}" x2="{col_cx+sign*rx}" y2="{cy}" stroke="{GRIS_ATRIB}" stroke-width="1"/>\n'
        fill_e, stroke_e, fill_t = (NEGRO, NEGRO, BLANCO) if pk else (BLANCO, GRIS_ATRIB, NEGRO)
        dash_e = ' stroke-dasharray="4,3"' if derivado else ""
        svg += f'<ellipse cx="{col_cx}" cy="{cy}" rx="{rx}" ry="{ATRIB_H/2}" fill="{fill_e}" stroke="{stroke_e}" stroke-width="1"{dash_e}/>\n'
        svg += f'<text x="{col_cx}" y="{cy+4}" text-anchor="middle" font-family="Helvetica" font-size="{ATTR_FONT}" fill="{fill_t}">{etiqueta}</text>\n'
        if parcial:
            mitad = len(etiqueta) * 3.4
            svg += (f'<line x1="{col_cx - mitad}" y1="{cy + 8}" x2="{col_cx + mitad}" y2="{cy + 8}" '
                    f'stroke="{NEGRO}" stroke-width="1" stroke-dasharray="3,2"/>\n')

    return svg, last_bottom

def wrap_svg(width, height, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" font-family="Helvetica">\n'
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="#F3F5F8" rx="20" ry="20" stroke="#E3E7ED"/>\n'
            f'{body}</svg>')

def wrap_html(title, sub, svgs_with_captions, path):
    parts = []
    for svg, caption in svgs_with_captions:
        parts.append(f'<div class="bloque">{svg}<p class="caption">{caption}</p></div>')
    html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><title>{title}</title>
<style>
  body {{ margin:0; padding:40px; background:#FFFFFF; font-family:Helvetica,Arial,sans-serif; }}
  h1 {{ font-size:20px; color:#111111; margin:0 0 4px 0; }}
  p.sub {{ font-size:13px; color:#555555; margin:0 0 32px 0; }}
  .bloque {{ margin-bottom: 32px; }}
  p.caption {{ font-size:13px; color:#555555; margin:8px 4px 0 4px; }}
  svg {{ display:block; }}
</style></head><body>
<h1>{title}</h1><p class="sub">{sub}</p>
{"".join(parts)}
</body></html>"""
    open(path, "w", encoding="utf-8").write(html)


# ==========================================================================
# Extensiones -- Quinta revision (2026-09-08), para las 6 vistas en Chen.
# Notacion que faltaba expresar: relacion identificadora, participacion
# total y entidad asociativa.
# ==========================================================================

def razon_cardinalidad(card_a, card_b):
    """Razon de cardinalidad en forma compacta (1:1, 1:n, n:n) -- lo que va
    debajo del rombo. Es el TIPO de la relacion, no su participacion: un
    '0..1' se normaliza a 1, porque que sea opcional lo dice la linea
    (participacion), no la razon."""
    def norm(c):
        c = c.replace("0..", "")
        return c.lower() if c.upper() in ("N", "M") else c
    return f"{norm(card_a)}:{norm(card_b)}"


def relation_diamond2(cx, cy, label, ident=False, derivada=False, razon=None,
                      razon_lado="abajo"):
    """Rombo de relacion. ident=True dibuja el rombo DOBLE (relacion
    identificadora de una entidad debil). derivada=True lo dibuja
    punteado (Reporte no persiste, se calcula)."""
    def pts(w, h):
        return f"{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}"
    dash = ' stroke-dasharray="6,4"' if derivada else ""
    svg = ""
    if ident:
        svg += (f'<polygon points="{pts(ROMBO_W+14, ROMBO_H+14)}" fill="none" '
                f'stroke="{AZUL_STROKE}" stroke-width="1.5"{dash}/>\n')
    svg += (f'<polygon points="{pts(ROMBO_W, ROMBO_H)}" fill="{AZUL_FILL}" '
            f'stroke="{AZUL_STROKE}" stroke-width="1.5"{dash}/>\n')
    svg += (f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-family="Helvetica" '
            f'font-size="{CARD_FONT}" fill="#1C3A5E">{label}</text>\n')
    if razon:
        # En una relacion VERTICAL la razon debajo del rombo cae encima de la
        # propia linea de conexion y queda tachada: en ese caso va al lado.
        if razon_lado == "izq":
            xx = cx - ROMBO_W / 2 - (7 if ident else 0) - 8
            svg += (f'<text x="{xx}" y="{cy+4}" text-anchor="end" font-family="Helvetica" '
                    f'font-size="{CARD_FONT}" font-weight="700" fill="{GRIS_MEDIO}">{razon}</text>\n')
        else:
            yy = cy + ROMBO_H / 2 + (7 if ident else 0) + 20
            svg += (f'<text x="{cx}" y="{yy}" text-anchor="middle" font-family="Helvetica" '
                    f'font-size="{CARD_FONT}" font-weight="700" fill="{GRIS_MEDIO}">{razon}</text>\n')
    b = 7 if ident else 0
    return svg, (cx - ROMBO_W/2 - b, cy - ROMBO_H/2 - b,
                 cx + ROMBO_W/2 + b, cy + ROMBO_H/2 + b)


def link(x1, y1, x2, y2, card=None, total=False, derivada=False):
    """Tramo recto entre una entidad y un rombo. total=True lo dibuja como
    linea DOBLE (participacion total: todo ejemplar participa)."""
    dash = ' stroke-dasharray="6,4"' if derivada else ""
    svg = ""
    if total:
        # dos lineas paralelas, separadas 3px en perpendicular al trazo
        dx, dy = x2 - x1, y2 - y1
        ln = max((dx*dx + dy*dy) ** 0.5, 1)
        ox, oy = -dy / ln * 2, dx / ln * 2
        for s in (1, -1):
            svg += (f'<line x1="{x1+ox*s}" y1="{y1+oy*s}" x2="{x2+ox*s}" y2="{y2+oy*s}" '
                    f'stroke="{GRIS_MEDIO}" stroke-width="1.2"{dash}/>\n')
    else:
        svg += (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="{GRIS_MEDIO}" stroke-width="1.2"{dash}/>\n')
    if card:
        vertical = abs(x2 - x1) < abs(y2 - y1)
        diagonal = abs(x2 - x1) > 1 and abs(y2 - y1) > 1
        lx, ly = x1 + (x2 - x1) * 0.5, y1 + (y2 - y1) * 0.5
        if diagonal:
            # en un tramo diagonal, «arriba» o «al lado» no lo despega de la
            # linea: se corre en perpendicular, hacia arriba
            dx, dy = x2 - x1, y2 - y1
            ln = (dx * dx + dy * dy) ** 0.5
            nx, ny = -dy / ln, dx / ln
            if ny > 0:
                nx, ny = -nx, -ny
            lx, ly, anchor = lx + nx * 24, ly + ny * 24 + 4, "middle"
        elif vertical:
            lx, ly, anchor = lx + 12, ly + 4, "start"
        else:
            ly, anchor = ly - 9, "middle"
        svg += (f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" font-family="Helvetica" '
                f'font-size="{CARD_FONT}" font-weight="700" fill="{NEGRO}">{card}</text>\n')
    return svg


ASOC_PAD_X, ASOC_PAD_Y = 26, 18

def associative_entity(cx, cy, label, rel_label, razon=None, razon_lado="abajo",
                       label_lado="arriba"):
    """Entidad asociativa: el rombo de la relacion DENTRO del rectangulo de
    la entidad -- la relacion hecha entidad, porque tiene atributos propios
    y llave propia. Mismo patron que 'Membresia' en la referencia de
    Semilleros."""
    w, h = ROMBO_W + ASOC_PAD_X * 2, ROMBO_H + ASOC_PAD_Y * 2
    x, y = cx - w / 2, cy - h / 2
    svg = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BLANCO}" '
           f'stroke="{NEGRO}" stroke-width="2"/>\n')
    d, _ = relation_diamond2(cx, cy, rel_label)
    svg += d
    # Con conexion vertical por arriba, el rotulo centrado encima queda
    # tachado por la propia linea: en ese caso va al costado derecho.
    if label_lado == "der":
        svg += (f'<text x="{x+w+12}" y="{cy+5}" text-anchor="start" font-family="Helvetica" '
                f'font-size="{LABEL_FONT}" font-weight="700" fill="{NEGRO}">{label}</text>\n')
    else:
        svg += (f'<text x="{cx}" y="{y-10}" text-anchor="middle" font-family="Helvetica" '
                f'font-size="{LABEL_FONT}" font-weight="700" fill="{NEGRO}">{label}</text>\n')
    if razon:
        if razon_lado == "izq":
            svg += (f'<text x="{x-10}" y="{cy+4}" text-anchor="end" font-family="Helvetica" '
                    f'font-size="{CARD_FONT}" font-weight="700" fill="{GRIS_MEDIO}">{razon}</text>\n')
        else:
            svg += (f'<text x="{cx}" y="{y+h+18}" text-anchor="middle" font-family="Helvetica" '
                    f'font-size="{CARD_FONT}" font-weight="700" fill="{GRIS_MEDIO}">{razon}</text>\n')
    return svg, (x, y, x + w, y + h)


# Estilo de "costura": una entidad ya presentada en una vista anterior, que
# reaparece solo para mostrar el enganche. Borde atenuado + fondo de
# referencia, para que nadie cuente 20 entidades donde hay 14.
def entity_ref(cx, cy, label, vista_origen):
    svg, bbox = entity_box(cx, cy, label, fill=REF_FILL, dashed=True)
    svg += (f'<text x="{cx}" y="{cy + ENTIDAD_H/2 + 16}" text-anchor="middle" '
            f'font-family="Helvetica" font-size="11" fill="{GRIS_ATRIB}">'
            f'ya presentada · Vista {vista_origen}</text>\n')
    return svg, bbox
