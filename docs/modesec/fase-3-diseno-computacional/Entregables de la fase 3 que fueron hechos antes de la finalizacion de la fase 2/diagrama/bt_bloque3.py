import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from caja_tabla import entity, relate_h, wrap_svg
from datos_mer import ESTUDIANTE, INSCRIPCION, EXPERIENCIA

W, H = 1300, 320
body = ""
est_svg, est = entity(180, 90, *ESTUDIANTE)
ins_svg, ins = entity(620, 90, *INSCRIPCION)
exp_svg, exp = entity(1080, 60, *EXPERIENCIA)
body += est_svg + ins_svg + exp_svg
body += relate_h(est, ins, "REALIZA", "1", "N", total_a=False, total_b=True)
body += relate_h(ins, exp, "PERTENECE A", "N", "1", total_a=True, total_b=False)

open(os.path.join(os.path.dirname(__file__), "bt_bloque3.svg"), "w").write(wrap_svg(W, H, body))
print("OK", est, ins, exp)
