import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from caja_tabla import entity, relate_h, relate_v, wrap_svg
from datos_mer import EXPERIENCIA, ITEM, EVIDENCIA, OPCION

W, H = 1300, 620
body = ""
exp_svg, exp = entity(180, 60, *EXPERIENCIA)
item_svg, item = entity(620, 50, *ITEM)
evid_svg, evid = entity(1080, 80, *EVIDENCIA, weak=True)
op_svg, op = entity(620, 420, *OPCION)
body += exp_svg + item_svg + evid_svg + op_svg
body += relate_h(exp, item, "GENERA", "1", "N", total_a=False, total_b=True)
body += relate_h(item, evid, "EVALUA", "N", "1", total_a=True, total_b=False)
body += relate_v(item, op, "OFRECE", "1", "N", total_a=True, total_b=True)

open(os.path.join(os.path.dirname(__file__), "bt_bloque4.svg"), "w").write(wrap_svg(W, H, body))
print("OK", exp, item, evid, op)
