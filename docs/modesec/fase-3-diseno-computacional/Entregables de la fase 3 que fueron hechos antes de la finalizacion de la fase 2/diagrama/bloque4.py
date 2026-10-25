import sys
sys.path.insert(0, ".")
from generador import *

body = ""

# ---- posiciones (calculadas, no a ojo) -- fila superior horizontal (patron de los bloques 1, 3, 5) mas una rama vertical hacia Opcion ----
exp_cx, item_cx, ev_cx = 220, 620, 1020
row_y = ROW_Y
first_attrib_y = ROW_Y + ENTIDAD_H/2 + 50

rama_x = item_cx + 70  # desplazado del centro de Ítem para no atravesar sus elipses de atributos (siempre centradas en item_cx)
opcion_cx, opcion_cy = rama_x, 640
tiene_opcion_y = 480

# ---- entidades ----
svg, exp_box = entity_box(exp_cx, row_y, "Experiencia")
body += svg
svg, item_box = entity_box(item_cx, row_y, "Ítem")
body += svg
svg, ev_box = entity_box(ev_cx, row_y, "Evidencia", fill=REF_FILL)
body += svg
svg, opcion_box = entity_box(opcion_cx, opcion_cy, "Opción")
body += svg

# ---- relaciones fila superior ----
genera_cx = (exp_cx + item_cx) / 2
svg, genera_pt = relation_diamond(genera_cx, row_y, "genera")
body += svg
evalua_cx = (item_cx + ev_cx) / 2
svg, evalua_pt = relation_diamond(evalua_cx, row_y, "se evalúa con")
body += svg

# ---- relacion vertical Ítem -> Opción ----
svg, tiene_op_pt = relation_diamond(rama_x, tiene_opcion_y, "tiene")
body += svg

# ---- conectores fila superior, con cardinalidad ----
body += connector(exp_box[2], row_y, genera_pt[0], row_y, card_a="1")
body += connector(genera_pt[2], row_y, item_box[0], row_y, card_b="N")
body += connector(item_box[2], row_y, evalua_pt[0], row_y, card_a="N")
body += connector(evalua_pt[2], row_y, ev_box[0], row_y, card_b="1")

# ---- conector vertical Ítem -> tiene -> Opción (desplazado del centro, ver rama_x) ----
body += connector(rama_x, row_y + ENTIDAD_H/2, rama_x, tiene_opcion_y - ROMBO_H/2, card_a="1")
body += connector(rama_x, tiene_opcion_y + ROMBO_H/2, opcion_cx, opcion_cy - ENTIDAD_H/2, card_b="N")

# ---- atributos: TODAS las entidades, completos, siempre que aparezcan ----
svg, _ = attribute_stack(exp_cx, exp_box[3], [
    ("id", True), ("nombre", False), ("estado", False), ("fecha_creacion", False), ("codigo_invitacion", False)
], first_attrib_y)
body += svg

svg, _ = attribute_stack(item_cx, item_box[3], [
    ("id", True), ("enunciado", False), ("formato", False), ("distractor", False), ("orden_sugerido", False)
], first_attrib_y)
body += svg

svg, _ = attribute_stack(ev_cx, ev_box[3], [
    ("enunciado", False)
], first_attrib_y)
body += svg

svg, _ = attribute_stack(opcion_cx, opcion_box[3], [
    ("id", True), ("texto", False), ("orden", False), ("es_correcta", False), ("grupo", False)
], opcion_cy + ENTIDAD_H/2 + 50)
body += svg

W, H = 1300, 1000
svg_final = wrap_svg(W, H, body)
open("bloque4.svg", "w", encoding="utf-8").write(svg_final)

wrap_html(
    "Bloque 4 — Banco de diagnóstico",
    "La Experiencia genera su propio banco de Ítems; cada Ítem evalúa exactamente una Evidencia del DBA anclado y tiene sus propias Opciones de respuesta.",
    [(svg_final, "Fig. 4 — Experiencia, Ítem, Opción y Evidencia.")],
    "bloque4.html"
)
print("listo")
