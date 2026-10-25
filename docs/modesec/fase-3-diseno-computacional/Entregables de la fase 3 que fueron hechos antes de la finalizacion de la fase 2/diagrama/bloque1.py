import sys
sys.path.insert(0, ".")
from generador import *

body = ""

# ---- posiciones (calculadas, no a ojo) ----
docente_cx, exp_cx, dba_cx = 220, 620, 1020
row_y = ROW_Y
first_attrib_y = ROW_Y + ENTIDAD_H/2 + 50

# ---- entidades ----
svg, docente_box = entity_box(docente_cx, row_y, "Docente")
body += svg
svg, exp_box = entity_box(exp_cx, row_y, "Experiencia")
body += svg
svg, dba_box = entity_box(dba_cx, row_y, "DBA", fill=REF_FILL)
body += svg

# ---- relaciones ----
crea_cx = (docente_cx + exp_cx) / 2
svg, crea_pt = relation_diamond(crea_cx, row_y, "crea")
body += svg
ancla_cx = (exp_cx + dba_cx) / 2
svg, ancla_pt = relation_diamond(ancla_cx, row_y, "se ancla a")
body += svg

# ---- conectores entidad-relacion-entidad, con cardinalidad ----
body += connector(docente_box[2], row_y, crea_pt[0], row_y, card_a="1")
body += connector(crea_pt[2], row_y, exp_box[0], row_y, card_b="N")
body += connector(exp_box[2], row_y, ancla_pt[0], row_y, card_a="N")
body += connector(ancla_pt[2], row_y, dba_box[0], row_y, card_b="1")

# ---- atributos: TODAS las entidades, completos, siempre que aparezcan ----
svg, _ = attribute_stack(docente_cx, docente_box[3], [
    ("id", True), ("nombre", False), ("correo", False), ("avatar_url", False)
], first_attrib_y)
body += svg

svg, _ = attribute_stack(exp_cx, exp_box[3], [
    ("id", True), ("nombre", False), ("estado", False), ("fecha_creacion", False), ("codigo_invitacion", False)
], first_attrib_y)
body += svg

svg, _ = attribute_stack(dba_cx, dba_box[3], [
    ("area", False), ("grado", False), ("enunciado", False), ("ejemplo", False)
], first_attrib_y)
body += svg

W, H = 1300, 520
svg_final = wrap_svg(W, H, body)
open("bloque1.svg", "w", encoding="utf-8").write(svg_final)

wrap_html(
    "Bloque 1 — Creación y anclaje curricular",
    "El docente crea la experiencia; la experiencia se ancla a un DBA oficial del MEN.",
    [(svg_final, "Fig. 1 — Las 3 entidades con sus atributos completos. DBA no tiene id propio: es dato del MEN, referenciado, no generado por nosotros.")],
    "bloque1.html"
)
print("listo")
