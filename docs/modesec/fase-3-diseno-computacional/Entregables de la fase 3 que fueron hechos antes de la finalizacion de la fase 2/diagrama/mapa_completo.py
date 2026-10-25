import sys
sys.path.insert(0, ".")
from generador import *

body = ""

# ---- coordenadas por columna (dependencia) y fila (calculadas, no a ojo) ----
# col1: raices (nada depende de otra entidad del modelo)
# col2: depende de col1
# col3: depende de col2
# col4: depende de col3
# col5: cierre del modelo
docente_c   = (220, 150)
estudiante_c= (220, 900)
dba_c       = (220, 1650)

experiencia_c = (850, 150)
evidencia_c   = (850, 1650)

inscripcion_c = (1480, 525)
item_c        = (1480, 1100)

respuesta_c = (2110, 700)
opcion_c    = (2110, 1100)
resultado_c = (2110, 1600)

reporte_c = (2740, 150)

def put(cx_cy, label, **kw):
    svg, box = entity_box(cx_cy[0], cx_cy[1], label, **kw)
    return svg, box

svg, docente_box = put(docente_c, "Docente"); body += svg
svg, estudiante_box = put(estudiante_c, "Estudiante"); body += svg
svg, dba_box = put(dba_c, "DBA", fill=REF_FILL); body += svg
svg, experiencia_box = put(experiencia_c, "Experiencia"); body += svg
svg, evidencia_box = put(evidencia_c, "Evidencia", fill=REF_FILL); body += svg
svg, inscripcion_box = put(inscripcion_c, "Inscripción"); body += svg
svg, item_box = put(item_c, "Ítem"); body += svg
svg, respuesta_box = put(respuesta_c, "Respuesta"); body += svg
svg, opcion_box = put(opcion_c, "Opción"); body += svg
svg, resultado_box = put(resultado_c, "Resultado", double=True); body += svg
svg, reporte_box = put(reporte_c, "Reporte", dashed=True); body += svg

boxes = dict(docente=docente_box, estudiante=estudiante_box, dba=dba_box,
             experiencia=experiencia_box, evidencia=evidencia_box,
             inscripcion=inscripcion_box, item=item_box, respuesta=respuesta_box,
             opcion=opcion_box, resultado=resultado_box, reporte=reporte_box)
centers = dict(docente=docente_c, estudiante=estudiante_c, dba=dba_c,
               experiencia=experiencia_c, evidencia=evidencia_c,
               inscripcion=inscripcion_c, item=item_c, respuesta=respuesta_c,
               opcion=opcion_c, resultado=resultado_c, reporte=reporte_c)

def rel(a, b, label, card_a, card_b, diamond_xy, side_a="right", side_b="left"):
    """Dibuja entidadA -> rombo -> entidadB. side_a/side_b: por que borde
    de la caja sale la linea (siempre borde izq/der a la altura propia de
    la entidad, nunca arriba/abajo -- eso deja el fondo libre para los
    atributos, igual que en todos los bloques anteriores)."""
    ba, ca = boxes[a], centers[a]
    bb, cb = boxes[b], centers[b]
    ax = ba[2] if side_a == "right" else ba[0]
    bx = bb[2] if side_b == "right" else bb[0]
    svg = ""
    s, dpt = relation_diamond(diamond_xy[0], diamond_xy[1], label)
    svg += s
    svg += ortho_connector(ax, ca[1], dpt[0] if diamond_xy[0] >= ax else dpt[2], diamond_xy[1], card=card_a)
    svg += ortho_connector(dpt[2] if diamond_xy[0] >= ax else dpt[0], diamond_xy[1], bx, cb[1], card=card_b)
    return svg

body += rel("docente", "experiencia", "crea", "1", "N", (535, 150))
body += rel("experiencia", "dba", "se ancla a", "N", "1", (535, 1300), side_a="left", side_b="right")
body += rel("dba", "evidencia", "tiene", "1", "N", (535, 1650))
body += rel("estudiante", "inscripcion", "tiene", "1", "N", (1000, 500))
body += rel("experiencia", "inscripcion", "tiene", "1", "N", (1165, 337))
body += rel("experiencia", "item", "genera", "1", "N", (1165, 625))
body += rel("evidencia", "item", "se evalúa con", "1", "N", (1165, 1375))
body += rel("item", "opcion", "tiene", "1", "N", (1795, 1100))
body += rel("inscripcion", "respuesta", "da", "1", "N", (1795, 612))
body += rel("item", "respuesta", "recibe", "1", "N", (1795, 900))
body += rel("inscripcion", "resultado", "tiene", "1", "N", (1750, 1300))
body += rel("evidencia", "resultado", "mide", "1", "N", (1480, 1625), side_a="right", side_b="left")
body += rel("experiencia", "reporte", "tiene", "1", "1", (1795, 150))

# ---- atributos: TODAS las entidades, completos, siempre (cuelgan del
# centro-abajo de cada caja; las relaciones salen siempre por los bordes
# izq/der a la altura propia de la entidad, nunca por abajo -- por eso
# nunca chocan con los atributos, igual que en los 6 bloques) ----
def attrs(name, box, cx, lst, side="left"):
    svg, _ = attribute_stack(cx, box[3], lst, box[3] + 50, side=side)
    return svg

body += attrs("docente", docente_box, docente_c[0], [
    ("id", True), ("nombre", False), ("correo", False), ("avatar_url", False)])
body += attrs("estudiante", estudiante_box, estudiante_c[0], [
    ("id", True), ("nombre", False), ("correo", False), ("avatar_url", False)])
body += attrs("dba", dba_box, dba_c[0], [
    ("area", False), ("grado", False), ("enunciado", False), ("ejemplo", False)])
body += attrs("experiencia", experiencia_box, experiencia_c[0], [
    ("id", True), ("nombre", False), ("estado", False), ("fecha_creacion", False), ("codigo_invitacion", False)])
body += attrs("evidencia", evidencia_box, evidencia_c[0], [
    ("enunciado", False)])
body += attrs("inscripcion", inscripcion_box, inscripcion_c[0], [
    ("id", True), ("fecha_union", False)])
body += attrs("item", item_box, item_c[0], [
    ("id", True), ("enunciado", False), ("formato", False), ("distractor", False), ("orden_sugerido", False)])
body += attrs("respuesta", respuesta_box, respuesta_c[0], [
    ("id", True), ("certeza", False), ("correcta", False)])
body += attrs("opcion", opcion_box, opcion_c[0], [
    ("id", True), ("texto", False), ("orden", False), ("es_correcta", False), ("grupo", False)])
body += attrs("resultado", resultado_box, resultado_c[0], [
    ("estado", False)])
# Reporte: sin atributos (vista calculada) -- no se dibuja stack.

W, H = 3050, 2200
svg_final = wrap_svg(W, H, body)
open("mapa-completo.svg", "w", encoding="utf-8").write(svg_final)

wrap_html(
    "Vista general — mapa completo del MER",
    "Las 11 entidades del modelo, con todos sus atributos, y las 13 relaciones que las conectan, en un solo mapa.",
    [(svg_final, "Mapa completo del Modelo Entidad-Relación de AdaptiveLearn.")],
    "mapa-completo.html"
)
print("listo")
