import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from caja_tabla import CATEGORIAS, wrap_svg, NEGRO

W, H = 720, 600
body = f'<text x="30" y="36" font-family="Helvetica" font-size="15" font-weight="700" fill="{NEGRO}">LEYENDA</text>\n'

items = [
    ("propia", "Entidad", "Objeto que administramos, con sus atributos adentro."),
    ("asociativa", "Entidad asociativa", "Resuelve una relacion N a N -- la caja ES la relacion."),
    ("men", "Dato externo del MEN", "Curriculo oficial, solo referenciado por el sistema."),
    ("debil", "Entidad debil", "Sin clave propia: la hereda de quien la identifica."),
    ("derivada", "Vista derivada", "No persiste: se calcula cada vez que se consulta."),
]
y = 70
for cat, label, desc in items:
    c = CATEGORIAS[cat]
    dash = ' stroke-dasharray="4,3"' if cat == "derivada" else ""
    body += f'<rect x="30" y="{y}" width="40" height="20" rx="3" ry="3" fill="{c["header"]}" stroke="{c["stroke"]}" stroke-width="1.6"{dash}/>\n'
    body += f'<text x="85" y="{y+10}" font-family="Helvetica" font-size="12.5" font-weight="700" fill="{NEGRO}">{label}</text>\n'
    body += f'<text x="85" y="{y+27}" font-family="Helvetica" font-size="11.5" fill="#555555">{desc}</text>\n'
    y += 62

body += f'<polygon points="50,{y+10} 72,{y+22} 50,{y+34} 28,{y+22}" fill="#DDF0DD" stroke="#5F9E5F" stroke-width="1.4"/>\n'
body += f'<text x="85" y="{y+18}" font-family="Helvetica" font-size="12.5" font-weight="700" fill="{NEGRO}">Relacion</text>\n'
body += f'<text x="85" y="{y+35}" font-family="Helvetica" font-size="11.5" fill="#555555">Como se conectan dos entidades.</text>\n'
y += 55
body += (f'<polygon points="50,{y-2} 76,{y+11} 50,{y+24} 24,{y+11}" fill="#DDF0DD" stroke="#5F9E5F" stroke-width="1.4"/>\n'
         f'<polygon points="50,{y+3} 70,{y+11} 50,{y+19} 30,{y+11}" fill="#DDF0DD" stroke="#5F9E5F" stroke-width="1.4"/>\n')
body += f'<text x="85" y="{y+18}" font-family="Helvetica" font-size="12.5" font-weight="700" fill="{NEGRO}">Relacion identificadora</text>\n'
body += f'<text x="85" y="{y+35}" font-family="Helvetica" font-size="11.5" fill="#555555">La que le da identidad a una entidad debil.</text>\n'
y += 60
body += f'<text x="30" y="{y+15}" font-family="Helvetica" font-size="12.5" font-weight="700" fill="{NEGRO}">PK / FK</text>\n'
body += f'<text x="85" y="{y+15}" font-family="Helvetica" font-size="11.5" fill="#555555">Clave primaria / foranea -- "PK,FK" cuando es las dos.</text>\n'
y += 30
body += f'<text x="30" y="{y+15}" font-family="Helvetica" font-size="12.5" font-weight="700" fill="{NEGRO}">(U) / (derivado)</text>\n'
body += f'<text x="150" y="{y+15}" font-family="Helvetica" font-size="11.5" fill="#555555">Valor unico / se calcula, no se guarda de forma independiente.</text>\n'

svg = wrap_svg(W, H, body)
open(os.path.join(os.path.dirname(__file__), "bt_leyenda.svg"), "w").write(svg)
print("listo")
