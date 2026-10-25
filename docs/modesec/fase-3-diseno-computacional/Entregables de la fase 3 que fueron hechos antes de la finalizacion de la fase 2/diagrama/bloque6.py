import sys
sys.path.insert(0, ".")
from generador import *

body = ""

# ---- posiciones (calculadas, no a ojo) -- mismo patron horizontal, version simple de 2 entidades ----
exp_cx, rep_cx = 250, 750
row_y = ROW_Y
first_attrib_y = ROW_Y + ENTIDAD_H/2 + 50

# ---- entidades ----
svg, exp_box = entity_box(exp_cx, row_y, "Experiencia")
body += svg
svg, rep_box = entity_box(rep_cx, row_y, "Reporte", dashed=True)
body += svg

# ---- relacion ----
tiene_cx = (exp_cx + rep_cx) / 2
svg, tiene_pt = relation_diamond(tiene_cx, row_y, "tiene")
body += svg

body += connector(exp_box[2], row_y, tiene_pt[0], row_y, card_a="1")
body += connector(tiene_pt[2], row_y, rep_box[0], row_y, card_b="1")

# ---- atributos: solo Experiencia -- Reporte no tiene atributos propios (vista calculada) ----
svg, _ = attribute_stack(exp_cx, exp_box[3], [
    ("id", True), ("nombre", False), ("estado", False), ("fecha_creacion", False), ("codigo_invitacion", False)
], first_attrib_y)
body += svg

W, H = 1050, 520
svg_final = wrap_svg(W, H, body)
open("bloque6.svg", "w", encoding="utf-8").write(svg_final)

wrap_html(
    "Bloque 6 — Reporte",
    "Reporte no es una tabla propia: es una vista calculada sobre Resultado, una por Experiencia.",
    [(svg_final, "Fig. 6 — Reporte se dibuja con borde punteado y sin atributos porque no persiste datos propios: se recalcula a partir de Resultado cada vez que se consulta. Tiene dos vistas: la principal (grupo × evidencia, con umbrales fijos por sistema, ADR-013) y la de estudiantes/aula (historial por Inscripción, ADR-010 punto 4).")],
    "bloque6.html"
)
print("listo")
