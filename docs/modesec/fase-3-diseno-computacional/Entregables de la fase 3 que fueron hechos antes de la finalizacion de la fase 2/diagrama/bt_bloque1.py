import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from caja_tabla import entity, relate_h, wrap_svg
from datos_mer import DOCENTE, EXPERIENCIA, DBA

W, H = 1300, 320
body = ""
docente_svg, docente = entity(180, 80, *DOCENTE)
exp_svg, exp = entity(620, 60, *EXPERIENCIA)
dba_svg, dba = entity(1080, 90, *DBA)
body += docente_svg + exp_svg + dba_svg
body += relate_h(docente, exp, "CREA", "1", "N", total_a=False, total_b=True)
body += relate_h(exp, dba, "SE ANCLA A", "N", "1", total_a=True, total_b=False)

svg = wrap_svg(W, H, body)
open(os.path.join(os.path.dirname(__file__), "bt_bloque1.svg"), "w").write(svg)
print("OK bloque1", docente, exp, dba)
