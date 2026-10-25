import sys
sys.path.insert(0, ".")
from generador import *

def label(cx, top_y, lines):
    svg = ""
    for i, line in enumerate(lines):
        svg += (f'<text x="{cx}" y="{top_y + i*16}" text-anchor="middle" '
                f'font-family="Helvetica" font-size="11.5" fill="{GRIS_MEDIO}">{line}</text>\n')
    return svg

def name(cx, y, text):
    return (f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="Helvetica" '
            f'font-size="12.5" font-weight="700" fill="{NEGRO}">{text}</text>\n')

body = ""
cols = [170, 470, 770, 1070]
row1_shape_y, row1_name_y, row1_label_y = 70, 118, 138
row2_shape_y, row2_name_y, row2_label_y = 260, 308, 328

# 1. Entidad
svg, _ = entity_box(cols[0], row1_shape_y, "Entidad", fill=BLANCO)
body += svg + name(cols[0], row1_name_y, "Rectángulo") + label(cols[0], row1_label_y, ["Un objeto que se guarda", "(Docente, Experiencia...)."])

# 2. Relación
svg, _ = relation_diamond(cols[1], row1_shape_y, "relación")
body += svg + name(cols[1], row1_name_y, "Rombo") + label(cols[1], row1_label_y, ["Cómo se conectan dos", "entidades (crea, tiene...)."])

# 3. Atributo
cx3 = cols[2]
body += f'<ellipse cx="{cx3}" cy="{row1_shape_y}" rx="{ATRIB_W/2}" ry="{ATRIB_H/2}" fill="{BLANCO}" stroke="{GRIS_ATRIB}" stroke-width="1"/>\n'
body += f'<text x="{cx3}" y="{row1_shape_y+4}" text-anchor="middle" font-family="Helvetica" font-size="{ATTR_FONT}" fill="{NEGRO}">atributo</text>\n'
body += name(cx3, row1_name_y, "Elipse blanca") + label(cx3, row1_label_y, ["Un dato / campo de", "la entidad."])

# 4. Llave primaria
cx4 = cols[3]
body += f'<ellipse cx="{cx4}" cy="{row1_shape_y}" rx="{ATRIB_W/2}" ry="{ATRIB_H/2}" fill="{NEGRO}" stroke="{NEGRO}" stroke-width="1"/>\n'
body += f'<text x="{cx4}" y="{row1_shape_y+4}" text-anchor="middle" font-family="Helvetica" font-size="{ATTR_FONT}" fill="{BLANCO}">id (PK)</text>\n'
body += name(cx4, row1_name_y, "Elipse negra") + label(cx4, row1_label_y, ["El identificador único", "de la entidad."])

# 5. Entidad débil
svg, _ = entity_box(cols[0], row2_shape_y, "Entidad débil", double=True)
body += svg + name(cols[0], row2_name_y, "Doble borde") + label(cols[0], row2_label_y, ["Depende de otras para", "existir, sin id propio (Resultado)."])

# 6. Vista calculada
svg, _ = entity_box(cols[1], row2_shape_y, "Vista calculada", dashed=True)
body += svg + name(cols[1], row2_name_y, "Borde punteado") + label(cols[1], row2_label_y, ["No es tabla: se calcula", "al consultar (Reporte)."])

# 7. Dato externo (MEN)
svg, _ = entity_box(cols[2], row2_shape_y, "Dato externo", fill=REF_FILL)
body += svg + name(cols[2], row2_name_y, "Color tostado") + label(cols[2], row2_label_y, ["Currículo oficial, solo", "referenciado (DBA, Evidencia)."])

# 8. Cardinalidad
cx8 = cols[3]
body += f'<circle cx="{cx8-70}" cy="{row2_shape_y}" r="5" fill="{NEGRO}"/>\n'
body += f'<line x1="{cx8-70}" y1="{row2_shape_y}" x2="{cx8+70}" y2="{row2_shape_y}" stroke="{GRIS_MEDIO}" stroke-width="1.2"/>\n'
body += f'<circle cx="{cx8+70}" cy="{row2_shape_y}" r="5" fill="{NEGRO}"/>\n'
body += f'<text x="{cx8-55}" y="{row2_shape_y-10}" text-anchor="middle" font-family="Helvetica" font-size="{CARD_FONT}" font-weight="700" fill="{NEGRO}">1</text>\n'
body += f'<text x="{cx8+55}" y="{row2_shape_y-10}" text-anchor="middle" font-family="Helvetica" font-size="{CARD_FONT}" font-weight="700" fill="{NEGRO}">N</text>\n'
body += name(cx8, row2_name_y, "Números en la línea") + label(cx8, row2_label_y, ["Cuántas veces participa", "cada entidad en la relación."])

W, H = 1250, 370
svg_final = wrap_svg(W, H, body)
open("legend.svg", "w", encoding="utf-8").write(svg_final)

wrap_html(
    "Notación empleada",
    "Los símbolos usados en los 6 bloques, con su significado.",
    [(svg_final, "")],
    "legend.html"
)
print("listo")
