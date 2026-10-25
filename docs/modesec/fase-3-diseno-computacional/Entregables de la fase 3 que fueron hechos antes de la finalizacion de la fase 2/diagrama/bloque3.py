import sys
sys.path.insert(0, ".")
from generador import *

body = ""

# ---- posiciones (calculadas, no a ojo) -- mismo patron horizontal del Bloque 1 ----
est_cx, insc_cx, exp_cx = 220, 620, 1020
row_y = ROW_Y
first_attrib_y = ROW_Y + ENTIDAD_H/2 + 50

# ---- entidades ----
svg, est_box = entity_box(est_cx, row_y, "Estudiante")
body += svg
svg, insc_box = entity_box(insc_cx, row_y, "Inscripción")
body += svg
svg, exp_box = entity_box(exp_cx, row_y, "Experiencia")
body += svg

# ---- relaciones ----
tiene1_cx = (est_cx + insc_cx) / 2
svg, tiene1_pt = relation_diamond(tiene1_cx, row_y, "tiene")
body += svg
tiene2_cx = (insc_cx + exp_cx) / 2
svg, tiene2_pt = relation_diamond(tiene2_cx, row_y, "tiene")
body += svg

# ---- conectores entidad-relacion-entidad, con cardinalidad ----
body += connector(est_box[2], row_y, tiene1_pt[0], row_y, card_a="1")
body += connector(tiene1_pt[2], row_y, insc_box[0], row_y, card_b="N")
body += connector(insc_box[2], row_y, tiene2_pt[0], row_y, card_a="N")
body += connector(tiene2_pt[2], row_y, exp_box[0], row_y, card_b="1")

# ---- atributos: TODAS las entidades, completos, siempre que aparezcan ----
svg, _ = attribute_stack(est_cx, est_box[3], [
    ("id", True), ("nombre", False), ("correo", False), ("avatar_url", False)
], first_attrib_y)
body += svg

svg, _ = attribute_stack(insc_cx, insc_box[3], [
    ("id", True), ("fecha_union", False)
], first_attrib_y)
body += svg

svg, _ = attribute_stack(exp_cx, exp_box[3], [
    ("id", True), ("nombre", False), ("estado", False), ("fecha_creacion", False), ("codigo_invitacion", False)
], first_attrib_y)
body += svg

W, H = 1300, 520
svg_final = wrap_svg(W, H, body)
open("bloque3.svg", "w", encoding="utf-8").write(svg_final)

wrap_html(
    "Bloque 3 — Inscripción",
    "Un estudiante se une a una experiencia con su código de invitación; Inscripción registra ese vínculo.",
    [(svg_final, "Fig. 3 — Inscripción resuelve la relación N a N entre Estudiante y Experiencia: cada fila es un vínculo concreto entre un estudiante y una experiencia.")],
    "bloque3.html"
)
print("listo")
