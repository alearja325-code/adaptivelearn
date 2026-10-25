import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from caja_tabla import entity, relate_h, wrap_svg
from datos_mer import DBA, EVIDENCIA

W, H = 820, 300
body = ""
dba_svg, dba = entity(160, 90, *DBA)
evid_svg, evid = entity(600, 70, *EVIDENCIA, weak=True)
body += dba_svg + evid_svg
body += relate_h(dba, evid, "COMPRENDE", "1", "N", total_a=True, total_b=True, identifying=True)

open(os.path.join(os.path.dirname(__file__), "bt_bloque2.svg"), "w").write(wrap_svg(W, H, body))
print("OK", dba, evid)
