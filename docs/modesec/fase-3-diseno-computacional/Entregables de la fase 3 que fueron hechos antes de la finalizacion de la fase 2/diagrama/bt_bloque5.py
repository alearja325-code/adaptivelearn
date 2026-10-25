import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from caja_tabla import entity, relate_h, direct_v, direct_h, wrap_svg
from datos_mer import ITEM, RESPUESTA, INSCRIPCION, RESPUESTA_OPCION, OPCION

W, H = 1300, 700
body = ""
item_svg, item = entity(180, 50, *ITEM)
resp_svg, resp = entity(620, 70, *RESPUESTA)
insc_svg, insc = entity(1080, 60, *INSCRIPCION)
ro_svg, ro = entity(620, 450, *RESPUESTA_OPCION)
op_svg, op = entity(1080, 430, *OPCION)
body += item_svg + resp_svg + insc_svg + ro_svg + op_svg
body += relate_h(item, resp, "RECIBE", "1", "N", total_a=False, total_b=True)
body += relate_h(resp, insc, "PROVIENE DE", "N", "1", total_a=True, total_b=False)
body += direct_v(resp, ro, "1", "N", total_a=True, total_b=True)
body += direct_h(ro, op, "M", "1", total_a=True, total_b=True)

open(os.path.join(os.path.dirname(__file__), "bt_bloque5.svg"), "w").write(wrap_svg(W, H, body))
print("OK", item, resp, insc, ro, op)
