import sys
sys.path.insert(0, ".")
from generador import *

body = ""

dba_cx, ev_cx = 300, 700
row_y = ROW_Y
first_attrib_y = ROW_Y + ENTIDAD_H/2 + 50

svg, dba_box = entity_box(dba_cx, row_y, "DBA", fill=REF_FILL)
body += svg
svg, ev_box = entity_box(ev_cx, row_y, "Evidencia", fill=REF_FILL)
body += svg

tiene_cx = (dba_cx + ev_cx) / 2
svg, tiene_pt = relation_diamond(tiene_cx, row_y, "tiene")
body += svg

body += connector(dba_box[2], row_y, tiene_pt[0], row_y, card_a="1")
body += connector(tiene_pt[2], row_y, ev_box[0], row_y, card_b="N")

svg, _ = attribute_stack(dba_cx, dba_box[3], [
    ("area", False), ("grado", False), ("enunciado", False), ("ejemplo", False)
], first_attrib_y)
body += svg

svg, _ = attribute_stack(ev_cx, ev_box[3], [
    ("enunciado", False)
], first_attrib_y)
body += svg

W, H = 900, 460
svg_final = wrap_svg(W, H, body)
open("bloque2.svg", "w", encoding="utf-8").write(svg_final)

wrap_html(
    "Bloque 2 — Currículo oficial (MEN)",
    "DBA y Evidencia son datos oficiales del MEN, referenciados por el sistema, no creados ni editados por nosotros.",
    [(svg_final, "Fig. 2 — Ninguna de las dos tiene id propio: no generamos identificador para dato oficial del MEN.")],
    "bloque2.html"
)
print("listo")
