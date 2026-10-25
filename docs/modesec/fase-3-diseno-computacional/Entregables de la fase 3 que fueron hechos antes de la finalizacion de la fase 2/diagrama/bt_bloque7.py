import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from caja_tabla import entity, relate_h, wrap_svg
from datos_mer import RESULTADO, REPORTE, EXPERIENCIA

W, H = 1300, 300
body = ""
res_svg, res = entity(180, 70, *RESULTADO, weak=True)
rep_svg, rep = entity(620, 90, *REPORTE, dashed=True)
exp_svg, exp = entity(1080, 60, *EXPERIENCIA)
body += res_svg + rep_svg + exp_svg
body += relate_h(res, rep, "SE AGREGA EN", "N", "1", total_a=False, total_b=False, derivada=True)
body += relate_h(rep, exp, "RESUME", "1", "1", total_a=False, total_b=False, derivada=True)

open(os.path.join(os.path.dirname(__file__), "bt_bloque7.svg"), "w").write(wrap_svg(W, H, body))
print("OK", res, rep, exp)
