"""MER completo en una sola lamina, con la estructura de la v3 del docente.

La revision del docente (2026-09-01) presento su modelo corregido como una
sola lamina: cajas de color por tipo de entidad, con su columna de llaves
(PK / FK), rombos verdes para las relaciones, linea doble para la
participacion total, leyenda abajo. Esta es la misma estructura, con el
contenido del MER final -- y con la disposicion del mapa Chen
(`mapa_chen.py`), que ya se verifico sin cruces.

Es la VISTA DE CONJUNTO, pensada para mirar el modelo entero de un vistazo.
Por eso muestra tambien las llaves foraneas: se calculan de las relaciones
del modelo relacional (`../modelo-relacional/datos_mr.py`), igual que las
deriva `_verificar_mr_mer.py`, asi que no pueden contradecirlo. El MER
formal en Chen estricta, sin FK (hallazgo H-8), son `vista1.svg` a
`vista7.svg` y `mapa-chen.svg`.

Escribe:
  mer-cajas.svg               la lamina
  mer-pantalla-completa.html  la lamina en un visor a pantalla completa,
                              con zoom (rueda), arrastre y ajuste a la pantalla

La geometria la revisa el mismo verificador de los diagramas UML
(`../uml/lienzo.py`): si una linea atraviesa una caja o un rotulo, o dos
textos se encaraman, no se escribe nada.

Uso:  python mapa_cajas.py
"""
import os
import re
import sys
from html import escape

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "uml"))
sys.path.insert(0, os.path.join(AQUI, "..", "modelo-relacional"))

from datos_mer import (ENTIDADES, RELACIONES, DEBILES, N_ENTIDADES,  # noqa: E402
                       N_REL_REALES, N_REL_DERIVADAS)
import datos_mr as MR                                                  # noqa: E402
from lienzo import Lienzo, ancho_texto                                 # noqa: E402

# ------------------------------------------------------------- paleta v3
PALETA = {   # categoria: (borde, cabecera, titulo)
    "propia": ("#7E63B8", "#E7DEF7", "#2E1F4D"),
    "asociativa": ("#C9922F", "#FDF0D5", "#4D3708"),
    "men": ("#A98B4E", "#F5EFE0", "#4A3A16"),
    "debil": ("#C0637B", "#FADCE0", "#4D1E29"),
    "derivada": ("#8A8A8A", "#ECECEC", "#333333"),
}
VERDE_FILL, VERDE_BORDE, VERDE_TEXTO = "#DDF0DD", "#5F9E5F", "#1F4D1F"
LINEA = "#6B7280"
FONDO = "#F3F5F8"

W_CAJA, H_CAB, H_FILA = 320, 30, 20
RX, RY = 84, 33            # medio ancho y medio alto de un rombo

# ------------------------------------------------- contenido de cada caja
ENT = {e[0]: e for e in ENTIDADES}
TABLA = {"CREDENCIAL": "credencial", "DOCENTE": "docente", "ESTUDIANTE": "estudiante",
         "EXPERIENCIA": "experiencia", "DBA": "dba", "EVIDENCIA": "evidencia",
         "EVIDENCIA_DICTAMEN": "evidencia_dictamen",
         "EXPERIENCIA_EVIDENCIA": "experiencia_evidencia", "INSCRIPCION": "inscripcion",
         "ITEM": "item", "OPCION": "opcion", "PRESENTACION": "presentacion",
         "RESPUESTA": "respuesta", "RESPUESTA_OPCION": "respuesta_opcion",
         "RESULTADO": "resultado"}


def fk_derivadas(tabla):
    """Columnas de FK que salen de una relacion: las que llevan la PK de la
    otra entidad (misma regla que _verificar_mr_mer.py)."""
    cols = set()
    for o, cs, dest, cds, *_ in MR.FKS:
        if o == tabla:
            pk = set(MR.pk_de(dest))
            cols |= {c for c, cd in zip(cs, cds) if cd in pk}
    return cols


def filas(nombre):
    """[(marca, nombre, anotacion)] en el orden de las columnas del MR; al
    final, los atributos calculados, que no tienen columna."""
    _, cat, attrs = ENT[nombre]
    anot_mer, marca_mer = {}, {}
    for a, m in attrs:
        partes = a.split(" ", 1)
        anot_mer[partes[0]] = partes[1] if len(partes) > 1 else ""
        marca_mer[partes[0]] = m

    def anot_de(n, base):
        extra = {"D": "(derivado · se guarda)", "C": "(calculado, no se guarda)"}.get(
            marca_mer.get(n, ""), "")
        return " ".join(x for x in (base, extra) if x)

    if nombre == "REPORTE":                      # no tiene tabla: su unica FK sale de «resume»
        return [("FK", "id_experiencia", "")] + [("", n, anot_de(n, an))
                                                   for n, an in anot_mer.items()]
    tabla = TABLA[nombre]
    pk, fks = set(MR.pk_de(tabla)), fk_derivadas(tabla)
    salida = []
    for f in MR.campos_de(tabla):
        n = f["nombre"]
        if n not in anot_mer and n not in fks:
            continue                             # columnas solo del MR (seguridad, redundancia)
        marca = ",".join(m for m, ok in (("PK", n in pk), ("FK", n in fks)) if ok)
        anot = anot_de(n, anot_mer.get(n, ""))
        if f["mysql"].startswith("ENUM"):
            dominio = "/".join(re.findall(r"'([^']*)'", f["mysql"]))
            anot = f"({dominio})" + (f" {anot}" if anot else "")
        salida.append((marca, n, anot))
    for n, m in marca_mer.items():               # calculados: sin columna, al final
        if m == "C":
            salida.append(("", n, anot_de(n, anot_mer[n])))
    return salida


def alto(nombre):
    return H_CAB + 8 + H_FILA * len(filas(nombre)) + 6


# ---------------------------------------------------------- disposicion
# La del mapa Chen, con las columnas mas juntas: aqui los atributos van
# dentro de la caja y no cuelgan al costado. Entre columnas quedan 300 px:
# el rombo y, a cada lado, lugar para un (min,max).
XC, C1, C2, C3, C4, C5 = 60, 640, 1260, 1880, 2500, 3120
F1, F2, F3, F4 = 200, 540, 1160, 1500
POS = {
    "CREDENCIAL": (XC, 740),
    "DBA": (C2, F1), "EVIDENCIA": (C3, F1), "EVIDENCIA_DICTAMEN": (C4, F1),
    "DOCENTE": (C1, F2), "EXPERIENCIA": (C2, F2), "EXPERIENCIA_EVIDENCIA": (C3, F2),
    "ITEM": (C4, F2), "OPCION": (C5, F2),
    "REPORTE": (C2 + 140, 930),
    "ESTUDIANTE": (C1, F3), "INSCRIPCION": (C2, F3), "RESULTADO": (C3, F3),
    "RESPUESTA_OPCION": (C5, F3),
    "PRESENTACION": (C4, F4), "RESPUESTA": (C5, F4),
}
ANCHO_CAJA = {"REPORTE": 300}
ANCHO, ALTO = 3500, 1990
X_ACCEDE = (XC + W_CAJA + C1) / 2           # rombos de «accede como»
X_XOR = XC + W_CAJA + 23                     # arco {xor}, entre CREDENCIAL y esos rombos


def caja(nombre):
    x, y = POS[nombre]
    return (x, y, x + ANCHO_CAJA.get(nombre, W_CAJA), y + alto(nombre))


# Recorrido de cada relacion: (puntos de A al rombo), (rombo), (puntos del
# rombo a B). Todos los tramos son horizontales o verticales.
def recorridos():
    B = {n: caja(n) for n in POS}
    yF1, yF2, yF3 = F1 + 50, F2 + 50, F3 + 50
    R = {}

    def h(a, b, y, xr=None):           # A a la izquierda de B, en la misma fila
        xr = xr if xr is not None else (B[a][2] + B[b][0]) / 2
        return [(B[a][2], y), (xr - RX, y)], (xr, y), [(xr + RX, y), (B[b][0], y)]

    def v(a, b, x, yr=None):           # A abajo, B arriba, en la misma columna
        yr = yr if yr is not None else (B[a][1] + B[b][3]) / 2
        return [(x, B[a][1]), (x, yr + RY)], (x, yr), [(x, yr - RY), (x, B[b][3])]

    def va(a, b, x, yr=None):          # A arriba, B abajo
        yr = yr if yr is not None else (B[a][3] + B[b][1]) / 2
        return [(x, B[a][3]), (x, yr - RY)], (x, yr), [(x, yr + RY), (x, B[b][1])]

    xa, yd, ye = X_ACCEDE, F2 + 60, F3 + 62
    R["accede_docente"] = ([(XC + 160, B["CREDENCIAL"][1]), (XC + 160, yd), (xa - RX, yd)], (xa, yd),
                           [(xa + RX, yd), (B["DOCENTE"][0], yd)])
    R["accede_estudiante"] = ([(XC + 160, B["CREDENCIAL"][3]), (XC + 160, ye), (xa - RX, ye)], (xa, ye),
                              [(xa + RX, ye), (B["ESTUDIANTE"][0], ye)])
    R["comprende"] = h("DBA", "EVIDENCIA", yF1)
    R["se dictamina"] = h("EVIDENCIA", "EVIDENCIA_DICTAMEN", yF1)
    R["crea"] = h("DOCENTE", "EXPERIENCIA", yF2)
    R["se ancla a"] = v("EXPERIENCIA", "DBA", C2 + 160)
    R["incluye"] = h("EXPERIENCIA", "EXPERIENCIA_EVIDENCIA", yF2)
    R["sobre"] = va("EVIDENCIA", "EXPERIENCIA_EVIDENCIA", C3 + 160)
    R["genera"] = h("EXPERIENCIA_EVIDENCIA", "ITEM", yF2)
    R["ofrece"] = h("ITEM", "OPCION", yF2)
    R["realiza"] = h("ESTUDIANTE", "INSCRIPCION", yF3)
    R["pertenece a"] = v("INSCRIPCION", "EXPERIENCIA", C2 + 70, yr=1082)
    R["arroja"] = h("INSCRIPCION", "RESULTADO", yF3)
    R["mide"] = va("EXPERIENCIA_EVIDENCIA", "RESULTADO", C3 + 220, yr=900)
    R["se presenta"] = va("ITEM", "PRESENTACION", C4 + 160, yr=1120)
    xi, yt, xat = C2 + 160, F4 + 80, C3 + 160
    R["atiende"] = ([(xi, B["INSCRIPCION"][3]), (xi, yt), (xat - RX, yt)], (xat, yt),
                    [(xat + RX, yt), (B["PRESENTACION"][0], yt)])
    R["registra"] = h("PRESENTACION", "RESPUESTA", F4 + 50)
    R["selecciona"] = v("RESPUESTA", "RESPUESTA_OPCION", C5 + 160)
    R["resume"] = va("EXPERIENCIA", "REPORTE", C2 + 260)
    xs, ym = C3 + 60, (B["REPORTE"][1] + B["REPORTE"][3]) / 2
    yc = (ym + B["RESULTADO"][1]) / 2
    R["se agrega en"] = ([(xs, B["RESULTADO"][1]), (xs, yc + RY)], (xs, yc),
                         [(xs, yc - RY), (xs, ym), (B["REPORTE"][2], ym)])
    return B, R


# Que extremo de cada recorrido toca a que entidad: los recorridos van del
# primer punto (entidad «a» del MER) al ultimo (entidad «b»), salvo estos,
# que se trazaron al reves por comodidad del dibujo.
INVERTIDOS = {"se ancla a": False, "pertenece a": False, "resume": True, "se agrega en": False,
              "sobre": False, "mide": False}


# ---------------------------------------------------------------- dibujo
def texto_con_anotacion(L, x, y, nombre, anot, negrita, dueno):
    """Nombre de columna y, en letra chica y gris, su dominio o anotacion."""
    w = ancho_texto(nombre, 11.5, negrita) + (ancho_texto(" " + anot, 8.5) if anot else 0)
    L.textos.append(((x, y - 9, x + w, y + 3), nombre + (" " + anot if anot else ""), dueno))
    t = f'<tspan font-size="8.5" font-weight="400" fill="#666666"> {escape(anot)}</tspan>' if anot else ""
    L.crudo(f'<text x="{x}" y="{y}" font-family="Helvetica" font-size="11.5" '
            f'font-weight="{700 if negrita else 400}" fill="#111111">{escape(nombre)}{t}</text>')


def dibujar_caja(L, nombre):
    x0, y0, x1, y1 = caja(nombre)
    cat = ENT[nombre][1]
    borde, cab, tit = PALETA[cat]
    debil = nombre in DEBILES
    dash = ' stroke-dasharray="6,4"' if cat == "derivada" else ""
    if debil:
        L.crudo(f'<rect x="{x0 - 5}" y="{y0 - 5}" width="{x1 - x0 + 10}" height="{y1 - y0 + 10}" '
                f'rx="7" ry="7" fill="none" stroke="{borde}" stroke-width="1.8"/>')
    L.crudo(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="5" ry="5" '
            f'fill="#FFFFFF" stroke="{borde}" stroke-width="1.8"{dash}/>'
            f'<path d="M {x0} {y0 + H_CAB} L {x0} {y0 + 5} Q {x0} {y0} {x0 + 5} {y0} L {x1 - 5} {y0} '
            f'Q {x1} {y0} {x1} {y0 + 5} L {x1} {y0 + H_CAB} Z" fill="{cab}" stroke="{borde}" '
            f'stroke-width="1.8"{dash}/>')
    b = 5 if debil else 0
    L.cajas[nombre] = (x0 - b, y0 - b, x1 + b, y1 + b)
    L.texto((x0 + x1) / 2, y0 + 20, nombre, tam=13, peso=700, color=tit, anchor="middle", dueno=nombre)
    xm = x0 + 62                                      # separador de la columna de llaves
    L.crudo(f'<line x1="{xm - 8}" y1="{y0 + H_CAB}" x2="{xm - 8}" y2="{y1}" stroke="{borde}" '
            f'stroke-width="0.8" opacity="0.55"/>')
    for i, (marca, n, anot) in enumerate(filas(nombre)):
        y = y0 + H_CAB + 8 + H_FILA * i + 13
        if marca:
            L.texto(x0 + 8, y, marca, tam=9.5, peso=700, color=borde, dueno=nombre)
        texto_con_anotacion(L, xm, y, n, anot, "PK" in marca, nombre)


def rombo(L, rid, cx, cy, nombre, ident, derivada):
    pts = lambda dx, dy: f"{cx},{cy - dy} {cx + dx},{cy} {cx},{cy + dy} {cx - dx},{cy}"
    dash = ' stroke-dasharray="5,4"' if derivada else ""
    fill = "#FFFFFF" if derivada else VERDE_FILL
    if ident:
        L.crudo(f'<polygon points="{pts(RX + 8, RY + 6)}" fill="#FFFFFF" stroke="{VERDE_BORDE}" stroke-width="1.6"/>')
    L.crudo(f'<polygon points="{pts(RX, RY)}" fill="{fill}" stroke="{VERDE_BORDE if not derivada else "#8A8A8A"}" '
            f'stroke-width="1.6"{dash}/>')
    m = 8 if ident else 0
    L.cajas["◇" + rid] = (cx - RX * 0.6 - m, cy - RY * 0.6 - m / 2, cx + RX * 0.6 + m, cy + RY * 0.6 + m / 2)
    L.texto(cx, cy + 4, nombre.upper(), tam=10.5, peso=700, color=VERDE_TEXTO if not derivada else "#555555",
            anchor="middle", dueno="◇" + rid)


def tramo(L, pts, total, derivada, permitidos, desc):
    color = "#8A8A8A" if derivada else LINEA
    if total:                     # linea doble: una gruesa y, encima, una del color del fondo
        L.linea(pts, color=color, sw=5.2, permitidos=permitidos, desc=desc)
        L.linea(pts, color=FONDO, sw=2.0, registrar=False)
    else:
        L.linea(pts, color=color, sw=1.5, dash="6,4" if derivada else None,
                permitidos=permitidos, desc=desc)


def rotulo_card(L, p, q, texto, dueno):
    """Cardinalidad junto al extremo p (sobre la entidad), del lado de q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    if dy == 0:
        s = 1 if dx > 0 else -1
        L.texto(p[0] + s * 12, p[1] - 9, texto, tam=13, peso=700, anchor="start" if s > 0 else "end",
                dueno=dueno)
    else:
        s = 1 if dy > 0 else -1
        L.texto(p[0] + 9, p[1] + s * 18 + (4 if s > 0 else 0), texto, tam=13, peso=700, dueno=dueno)


def dibujar():
    L = Lienzo(ANCHO, ALTO)
    L.texto(ANCHO / 2, 62, "DIAGRAMA ENTIDAD - RELACIÓN — versión final", tam=34, peso=700,
            color="#1C2E4A", anchor="middle")
    L.texto(ANCHO / 2, 98, f"ADAPTIVELEARN · FASE III · {N_ENTIDADES} ENTIDADES + REPORTE (DERIVADO) · "
            f"{N_REL_REALES} RELACIONES + {N_REL_DERIVADAS} DERIVADAS · REVISIÓN DEL DOCENTE "
            f"(2026-09-01) ATENDIDA", tam=17, color="#555555", anchor="middle")
    B, R = recorridos()
    for n in POS:
        dibujar_caja(L, n)
    for r in RELACIONES:
        rid = r.get("id", r["nombre"])
        ida, centro, vuelta = R[rid]
        a, b = r["a"], r["b"]
        if INVERTIDOS.get(rid):
            a, b = b, a
        # junto a cada entidad, su participacion (min,max) -- la notacion de la
        # tabla de relaciones de la v3 del docente
        card_a, card_b = r["part_a"], r["part_b"]
        tot_a, tot_b = r["total_a"], r["total_b"]
        if INVERTIDOS.get(rid):
            card_a, card_b, tot_a, tot_b = card_b, card_a, tot_b, tot_a
        destino_b = r.get("asociativa") or b
        if r.get("asociativa"):            # selecciona: cada fila de Respuesta_Opcion es de UNA respuesta
            card_b, tot_b = "(1,1)", True
        der = r.get("derivada", False)
        tramo(L, ida, tot_a, der, {a, "◇" + rid}, f"{a}—{rid}")
        tramo(L, vuelta, tot_b, der, {destino_b, "◇" + rid}, f"{rid}—{destino_b}")
        rombo(L, rid, centro[0], centro[1], r["nombre"], r.get("ident"), der)
        rotulo_card(L, ida[0], ida[1], card_a, None)
        rotulo_card(L, vuelta[-1], vuelta[-2], card_b, None)
        if r.get("asociativa"):            # y Opcion 1 — M Respuesta_Opcion, sin rombo propio
            ro, op = B[r["asociativa"]], B[r["b"]]
            xs = C5 + 160
            pts = [(xs, ro[1]), (xs, op[3])]
            tramo(L, pts, False, False, {r["asociativa"], r["b"]}, "Respuesta_Opcion—Opcion")
            rotulo_card(L, pts[0], pts[1], "(1,1)", None)
            rotulo_card(L, pts[1], pts[0], r["part_b"], None)
            L.texto(xs + 12, (ro[1] + op[3]) / 2 + 4, "«selecciona» N:M,", tam=11, color="#666666")
            L.texto(xs + 12, (ro[1] + op[3]) / 2 + 19, "materializada", tam=11, color="#666666")
    # {xor}: las dos «accede como» son excluyentes (RI-12)
    y1, y2 = R["accede_docente"][0][-1][1], R["accede_estudiante"][0][-1][1]
    L.linea([(X_XOR, y1), (X_XOR, y2)], color="#B4536B", sw=1.4, dash="5,4", desc="xor")
    L.texto(X_XOR + 9, y1 + 92, "{xor}", tam=13, peso=700, color="#B4536B")
    L.texto(X_XOR + 9, y1 + 109, "un solo rol", tam=11, color="#B4536B")
    L.texto(X_XOR + 9, y1 + 124, "(RI-12)", tam=11, color="#B4536B")
    leyenda(L)
    return L


def leyenda(L):
    x0, y0 = 120, 1745
    L.crudo(f'<rect x="{x0}" y="{y0}" width="{ANCHO - 2 * x0}" height="200" rx="10" ry="10" '
            f'fill="#FFFFFF" stroke="#E3E7ED"/>')
    L.texto(x0 + 30, y0 + 30, "LEYENDA", tam=13, peso=700, color="#1C2E4A")
    x = x0 + 30
    for cat, txt in [("propia", "Entidad propia"), ("asociativa", "Entidad asociativa (resuelve M:N)"),
                     ("men", "Dato externo del MEN, referenciado"), ("debil", "Entidad débil (doble borde)"),
                     ("derivada", "Vista derivada: no persiste")]:
        borde, cab, _ = PALETA[cat]
        dash = ' stroke-dasharray="5,4"' if cat == "derivada" else ""
        if cat == "debil":
            L.crudo(f'<rect x="{x - 4}" y="{y0 + 46}" width="42" height="30" rx="5" ry="5" fill="none" '
                    f'stroke="{borde}" stroke-width="1.6"/>')
        L.crudo(f'<rect x="{x}" y="{y0 + 50}" width="34" height="22" rx="4" ry="4" fill="{cab}" '
                f'stroke="{borde}" stroke-width="1.6"{dash}/>')
        w = L.texto(x + 46, y0 + 66, txt, tam=12)
        x += 46 + w + 60
    y = y0 + 112
    L.crudo(f'<polygon points="{x0 + 30},{y} {x0 + 62},{y - 12} {x0 + 94},{y} {x0 + 62},{y + 12}" '
            f'fill="{VERDE_FILL}" stroke="{VERDE_BORDE}" stroke-width="1.6"/>')
    L.texto(x0 + 106, y + 4, "Relación", tam=12)
    xi = x0 + 230
    L.crudo(f'<polygon points="{xi - 6},{y} {xi + 32},{y - 16} {xi + 70},{y} {xi + 32},{y + 16}" '
            f'fill="#FFFFFF" stroke="{VERDE_BORDE}" stroke-width="1.6"/>'
            f'<polygon points="{xi},{y} {xi + 32},{y - 11} {xi + 64},{y} {xi + 32},{y + 11}" '
            f'fill="{VERDE_FILL}" stroke="{VERDE_BORDE}" stroke-width="1.6"/>')
    L.texto(xi + 82, y + 4, "Relación identificadora (rombo doble)", tam=12)
    xl = xi + 400
    L.crudo(f'<line x1="{xl}" y1="{y}" x2="{xl + 60}" y2="{y}" stroke="{LINEA}" stroke-width="5.2"/>'
            f'<line x1="{xl}" y1="{y}" x2="{xl + 60}" y2="{y}" stroke="#FFFFFF" stroke-width="2"/>')
    L.texto(xl + 72, y + 4, "Línea doble: participación obligatoria", tam=12)
    xd = xl + 380
    L.crudo(f'<polygon points="{xd},{y} {xd + 32},{y - 12} {xd + 64},{y} {xd + 32},{y + 12}" '
            f'fill="#FFFFFF" stroke="#8A8A8A" stroke-width="1.6" stroke-dasharray="5,4"/>')
    L.texto(xd + 76, y + 4, "Relación derivada (punteada): se calcula, no se guarda", tam=12)
    L.texto(x0 + 30, y0 + 158, "PK clave primaria · FK clave foránea · (U) valor único · ( ) dominio "
            "o dato derivado · (mín, máx) junto a cada entidad: cuántas veces participa un ejemplar "
            "suyo · {xor}: relaciones excluyentes", tam=12, peso=700)
    L.texto(x0 + 30, y0 + 182, "Vista de conjunto, en la notación de la revisión del docente: muestra "
            "las llaves (PK y FK) para leer cómo se enlaza todo. El MER formal, en notación Chen "
            "estricta y sin llaves foráneas (hallazgo H-8), son las siete vistas de 16-modelo-entidad-relacion.md.",
            tam=11.5, color="#555555")


# ------------------------------------------------------------- visor
VISOR = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MER · AdaptiveLearn</title>
<style>
  html, body { margin: 0; height: 100%; overflow: hidden; background: #ffffff; font-family: "Segoe UI", system-ui, sans-serif;
               user-select: none; -webkit-user-select: none; }
  #lienzo { position: fixed; inset: 0; cursor: grab; touch-action: none; }
  #lienzo.arrastrando { cursor: grabbing; }
  #capa { position: absolute; left: 0; top: 0; transform-origin: 0 0; }
  #mer { display: block; }
  #ayuda { position: fixed; left: 50%; bottom: 18px; transform: translateX(-50%); background: rgba(30,30,30,.82); color: #fff;
           padding: 8px 16px; border-radius: 8px; font-size: 13px; transition: opacity .6s; pointer-events: none; white-space: nowrap; }
  #zoom { position: fixed; right: 14px; top: 12px; background: rgba(30,30,30,.7); color: #fff; padding: 4px 10px;
          border-radius: 6px; font-size: 12px; pointer-events: none; }
</style>
</head>
<body>
<div id="lienzo"><div id="capa">
__SVG__
</div></div>
<div id="zoom">100%</div>
<div id="ayuda">Rueda: acercar o alejar · Arrastrar: mover · Doble clic: acercar o ajustar · 0: ajustar a la pantalla · F11: salir de pantalla completa</div>
<script>
  const lienzo = document.getElementById('lienzo'), capa = document.getElementById('capa');
  const W = __W__, H = __H__;
  let s = 1, x = 0, y = 0, ajuste = 1;
  function pintar() {
    capa.style.transform = `translate(${x}px, ${y}px) scale(${s})`;
    document.getElementById('zoom').textContent = Math.round(s * 100) + '%';
  }
  function ajustar() {
    const vw = lienzo.clientWidth, vh = lienzo.clientHeight;
    ajuste = Math.min(vw / W, vh / H) * 0.97;   // un margen: nada pegado al borde
    s = ajuste; x = (vw - W * s) / 2; y = (vh - H * s) / 2; pintar();
  }
  function zoomEn(px, py, nuevo) {
    nuevo = Math.min(Math.max(nuevo, ajuste * 0.8), 4);
    x = px - (px - x) * (nuevo / s); y = py - (py - y) * (nuevo / s); s = nuevo; pintar();
  }
  lienzo.addEventListener('wheel', (e) => { e.preventDefault(); zoomEn(e.clientX, e.clientY, s * Math.exp(-e.deltaY * 0.0015)); }, { passive: false });
  let arrastre = null;
  lienzo.addEventListener('pointerdown', (e) => { e.preventDefault(); arrastre = { px: e.clientX, py: e.clientY, x, y }; lienzo.classList.add('arrastrando'); lienzo.setPointerCapture(e.pointerId); });
  lienzo.addEventListener('pointermove', (e) => { if (!arrastre) return; x = arrastre.x + e.clientX - arrastre.px; y = arrastre.y + e.clientY - arrastre.py; pintar(); });
  lienzo.addEventListener('pointerup', () => { arrastre = null; lienzo.classList.remove('arrastrando'); });
  lienzo.addEventListener('dblclick', (e) => { if (s > ajuste * 1.05) ajustar(); else zoomEn(e.clientX, e.clientY, Math.max(1, ajuste * 2.5)); });
  addEventListener('keydown', (e) => {
    if (e.key === '0') ajustar();
    if (e.key === '+' || e.key === '=') zoomEn(innerWidth / 2, innerHeight / 2, s * 1.25);
    if (e.key === '-') zoomEn(innerWidth / 2, innerHeight / 2, s / 1.25);
  });
  // reajusta cuando la ventana pasa a pantalla completa o cambia de tamano
  new ResizeObserver(ajustar).observe(lienzo);
  ajustar();
  setTimeout(() => (document.getElementById('ayuda').style.opacity = 0), 7000);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    L = dibujar()
    problemas = L.verificar()
    if problemas:
        print(f"GEOMETRIA: {len(problemas)} problema(s)")
        for p in problemas:
            print(f"   · {p}")
        sys.exit(1)
    svg = L.svg()
    with open(os.path.join(AQUI, "mer-cajas.svg"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)
    svg_visor = svg.replace("<svg ", '<svg id="mer" ', 1)
    with open(os.path.join(AQUI, "mer-pantalla-completa.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(VISOR.replace("__SVG__", svg_visor).replace("__W__", str(ANCHO)).replace("__H__", str(ALTO)))
    print(f"generado: mer-cajas.svg + mer-pantalla-completa.html ({len(POS)} cajas, "
          f"{len(RELACIONES)} relaciones) · geometría limpia")
