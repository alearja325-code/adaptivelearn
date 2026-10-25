import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from caja_tabla import entity, relate_h, wrap_svg
from datos_mer import INSCRIPCION, RESULTADO, EVIDENCIA

W, H = 1300, 300
body = ""
insc_svg, insc = entity(180, 90, *INSCRIPCION)
res_svg, res = entity(620, 70, *RESULTADO, weak=True)
evid_svg, evid = entity(1080, 90, *EVIDENCIA, weak=True)
body += insc_svg + res_svg + evid_svg
body += relate_h(insc, res, "ARROJA", "1", "N", total_a=False, total_b=True, identifying=True)
body += relate_h(res, evid, "MIDE", "N", "1", total_a=True, total_b=False, identifying=True)

open(os.path.join(os.path.dirname(__file__), "bt_bloque6.svg"), "w").write(wrap_svg(W, H, body))
print("OK", insc, res, evid)
