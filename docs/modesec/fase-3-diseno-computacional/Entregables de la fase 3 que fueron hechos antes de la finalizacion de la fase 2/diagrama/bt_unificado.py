import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from caja_tabla import entity, diamond, routed, wrap_svg, NEGRO
import datos_mer as D

body = ""
boxes = {}


def put(name, cx, top, data, **kw):
    svg, box = entity(cx, top, *data, **kw)
    boxes[name] = box
    return svg


# tops calculados para que, dentro de cada fila, todas las cajas compartan
# el mismo centro vertical (cy) -- sin eso, un conector "directo" entre dos
# cajas de la misma fila pero de alto distinto queda en diagonal libre.
body += put("docente", 250, 190, D.DOCENTE)
body += put("experiencia", 800, 160, D.EXPERIENCIA)
body += put("dba", 1350, 180, D.DBA)
body += put("evidencia", 1900, 190, D.EVIDENCIA, weak=True)

body += put("estudiante", 250, 740, D.ESTUDIANTE)
body += put("item", 800, 700, D.ITEM)
body += put("opcion", 1350, 710, D.OPCION)

body += put("inscripcion", 250, 1310, D.INSCRIPCION)
body += put("respuesta", 800, 1300, D.RESPUESTA)
body += put("respuesta_opcion", 1350, 1320, D.RESPUESTA_OPCION)
body += put("resultado", 1900, 1310, D.RESULTADO, weak=True)

body += put("reporte", 2450, 700, D.REPORTE, dashed=True)


def rel(a, b, label, card_a, card_b, dxy, side_a="right", side_b="left",
        identifying=False, derivada=False):
    """Relacion horizontal directa -- solo valida si box_a y box_b comparten cy."""
    ba, bb = boxes[a], boxes[b]
    assert abs(ba["cy"] - bb["cy"]) < 1, f"{a}-{b} no comparten cy, usar ruta manual"
    ax = ba["x1"] if side_a == "right" else ba["x0"]
    bx = bb["x1"] if side_b == "right" else bb["x0"]
    d_svg, d = diamond(dxy[0], dxy[1], label, identifying, derivada)
    svg = d_svg
    left_e, right_e = d["cx"] - d["rw"], d["cx"] + d["rw"]
    svg += routed([(ax, ba["cy"]), (left_e if dxy[0] >= ax else right_e, dxy[1])], card_a, dashed=derivada)
    svg += routed([(right_e if dxy[0] >= ax else left_e, dxy[1]), (bx, bb["cy"])], card_b, dashed=derivada)
    return svg


# ---- relaciones directas (cajas de la misma fila, cy compartido) ----
body += rel("docente", "experiencia", "CREA", "1", "N", (525, 252))
body += rel("experiencia", "dba", "SE ANCLA A", "N", "1", (1075, 252))
body += rel("dba", "evidencia", "COMPRENDE", "1", "N", (1625, 252), identifying=True)
body += rel("item", "opcion", "OFRECE", "1", "N", (1075, 802))
body += rel("inscripcion", "respuesta", "PROVIENE DE", "N", "1", (525, 1372))
body += rel("respuesta", "respuesta_opcion", "SELECCIONA", "1", "N", (1075, 1372))

# ---- relaciones verticales directas (misma columna, cx compartido) ----
def rel_v(a, b, label, card_a, card_b, dy, identifying=False, derivada=False):
    ba, bb = boxes[a], boxes[b]
    assert abs(ba["cx"] - bb["cx"]) < 1, f"{a}-{b} no comparten cx"
    d_svg, d = diamond(ba["cx"], dy, label, identifying, derivada)
    svg = d_svg
    svg += routed([(ba["cx"], ba["y1"]), (ba["cx"], dy - d["rw"])], card_a, dashed=derivada)
    svg += routed([(ba["cx"], dy + d["rw"]), (bb["cx"], bb["y0"])], card_b, dashed=derivada)
    return svg


body += rel_v("estudiante", "inscripcion", "REALIZA", "1", "N", 1040)
body += rel_v("experiencia", "item", "GENERA", "1", "N", 460)
body += rel_v("item", "respuesta", "RECIBE", "1", "N", 1080)
body += rel_v("opcion", "respuesta_opcion", "SELECCIONA", "1", "N", 1080)

# ---- relaciones ruteadas por el margen (evitan cruzar cajas intermedias) ----
# ITEM -> EVIDENCIA: por el margen superior (encima de la fila 1). OJO:
# Item esta debajo de Experiencia (misma columna) -- subir derecho desde
# el borde superior de Item atraviesa la caja de Experiencia. Sale por
# el borde derecho de Item primero, al hueco libre entre Experiencia y
# el rombo SE ANCLA A (x=985, dentro del tramo 935-1035 que separa a
# ambos), y de ahi sube.
# y=125, no y=70: a y=70 el rombo de EVALUA (alto total 66px) se metia
# dentro del rombo de RESUME (y=45, mismo corredor superior) -- los 2
# corredores del margen de arriba necesitan su propio carril, separados.
d_svg, d = diamond(1350, 125, "EVALUA")
body += d_svg
body += routed([(935, 802), (985, 802), (985, 125), (1350 - d["rw"], 125)], "N")
body += routed([(1350 + d["rw"], 125), (1900, 125), (1900, 190)], "1")

# INSCRIPCION -> RESULTADO: por el margen inferior (debajo de la fila 3)
d_svg, d = diamond(1075, 1580, "ARROJA", identifying=True)
body += d_svg
body += routed([(250, 1434), (250, 1580), (1075 - d["rw"] - 8, 1580)], "1")
body += routed([(1075 + d["rw"] + 8, 1580), (1900, 1580), (1900, 1434)], "N")

# RESULTADO -> EVIDENCIA (MIDE): por un corredor a la derecha del grupo
# central (x=2180, entre el borde derecho de Resultado/Evidencia y el
# borde izquierdo de Reporte) -- NO una linea recta por el medio: esa
# version pasaba pegada al costado de Item/Opcion/Respuesta y se leia
# como si los cruzara. Ahora rodea el grupo por fuera, mismo criterio
# que ya usan las 2 relaciones de Reporte.
d_svg, d = diamond(2180, 800, "MIDE", identifying=True)
body += d_svg
body += routed([(2035, 1340), (2180, 1340), (2180, 800 + d["rw"])], "N")
body += routed([(2180, 800 - d["rw"]), (2180, 252), (2035, 252)], "1")

# REPORTE -> RESULTADO: tramo directo a la derecha, sin cajas de por medio
d_svg, d = diamond(2450, 1150, "SE AGREGA EN", derivada=True)
body += d_svg
body += routed([(2035, 1404), (2450, 1404), (2450, 1150 + d["rw"])], "N", dashed=True)
body += routed([(2450, 1150 - d["rw"]), (2450, 804)], "1", dashed=True)

# REPORTE -> EXPERIENCIA: por el margen superior, por fuera de todo --
# carril propio (y=45), mas arriba que el de EVALUA (y=125), con hueco
# de sobra entre los dos rombos (45+33=78 vs 125-33=92).
d_svg, d = diamond(1625, 45, "RESUME", derivada=True)
body += d_svg
body += routed([(2450, 700), (2450, 45), (1625 + d["rw"], 45)], "1", dashed=True)
body += routed([(1625 - d["rw"], 45), (800, 45), (800, 160)], "1", dashed=True)

W, H = 2820, 1650
svg_final = wrap_svg(W, H, body)
open(os.path.join(os.path.dirname(__file__), "bt_unificado.svg"), "w").write(svg_final)
print("listo")
