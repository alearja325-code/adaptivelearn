import sys
sys.path.insert(0, ".")
from generador import *

body = ""

# ---- posiciones (calculadas, no a ojo) -- mismo patron horizontal de los bloques 1, 3 y 4 ----
item_cx, resp_cx, insc_cx, result_cx, ev_cx = 200, 600, 1000, 1400, 1800
row_y = ROW_Y
first_attrib_y = ROW_Y + ENTIDAD_H/2 + 50

# ---- entidades ----
svg, item_box = entity_box(item_cx, row_y, "Ítem")
body += svg
svg, resp_box = entity_box(resp_cx, row_y, "Respuesta")
body += svg
svg, insc_box = entity_box(insc_cx, row_y, "Inscripción")
body += svg
svg, result_box = entity_box(result_cx, row_y, "Resultado", double=True)
body += svg
svg, ev_box = entity_box(ev_cx, row_y, "Evidencia", fill=REF_FILL)
body += svg

# ---- relaciones ----
recibe_cx = (item_cx + resp_cx) / 2
svg, recibe_pt = relation_diamond(recibe_cx, row_y, "recibe")
body += svg
da_cx = (resp_cx + insc_cx) / 2
svg, da_pt = relation_diamond(da_cx, row_y, "da")
body += svg
tiene_cx = (insc_cx + result_cx) / 2
svg, tiene_pt = relation_diamond(tiene_cx, row_y, "tiene")
body += svg
mide_cx = (result_cx + ev_cx) / 2
svg, mide_pt = relation_diamond(mide_cx, row_y, "mide")
body += svg

# ---- conectores entidad-relacion-entidad, con cardinalidad ----
body += connector(item_box[2], row_y, recibe_pt[0], row_y, card_a="1")
body += connector(recibe_pt[2], row_y, resp_box[0], row_y, card_b="N")

body += connector(resp_box[2], row_y, da_pt[0], row_y, card_a="N")
body += connector(da_pt[2], row_y, insc_box[0], row_y, card_b="1")

body += connector(insc_box[2], row_y, tiene_pt[0], row_y, card_a="1")
body += connector(tiene_pt[2], row_y, result_box[0], row_y, card_b="N")

body += connector(result_box[2], row_y, mide_pt[0], row_y, card_a="N")
body += connector(mide_pt[2], row_y, ev_box[0], row_y, card_b="1")

# ---- atributos: TODAS las entidades, completos, siempre que aparezcan ----
svg, _ = attribute_stack(item_cx, item_box[3], [
    ("id", True), ("enunciado", False), ("formato", False), ("distractor", False), ("orden_sugerido", False)
], first_attrib_y)
body += svg

svg, _ = attribute_stack(resp_cx, resp_box[3], [
    ("id", True), ("certeza", False), ("correcta", False)
], first_attrib_y)
body += svg

svg, _ = attribute_stack(insc_cx, insc_box[3], [
    ("id", True), ("fecha_union", False)
], first_attrib_y)
body += svg

svg, _ = attribute_stack(result_cx, result_box[3], [
    ("estado", False)
], first_attrib_y)
body += svg

svg, _ = attribute_stack(ev_cx, ev_box[3], [
    ("enunciado", False)
], first_attrib_y)
body += svg

W, H = 2100, 520
svg_final = wrap_svg(W, H, body)
open("bloque5.svg", "w", encoding="utf-8").write(svg_final)

wrap_html(
    "Bloque 5 — Respuesta y resultado",
    "Cada Respuesta liga un Ítem con la Inscripción que la dio; cada Resultado resume, por Evidencia, lo que esas respuestas permiten concluir sobre esa Inscripción.",
    [(svg_final, "Fig. 5 — Resultado no tiene identificador propio: depende de la combinación Inscripción + Evidencia, por eso se dibuja como entidad débil (doble borde). Su único atributo es un estado (muestra / no muestra / no concluyente), nunca una certeza (ADR-008).")],
    "bloque5.html"
)
print("listo")
