"""Mapa completo del MER en notacion Chen -- version final de la Fase III.

Las 15 entidades (+ Reporte, derivado), todos sus atributos y las 20
relaciones en un solo lienzo. Mismo contenido que las 7 vistas, porque
las dos cosas salen de datos_mer.py; lo unico que cambia es el layout.

Parte del mapa de la Quinta revision (mismas reglas, comprobadas por
_verificar_mapa.py):
  1. Cada entidad cuelga su columna de atributos DESPLAZADA a un costado,
     para que la vertical que sale de la entidad quede libre.
  2. El costado de cada columna va del lado por donde NO pasa una linea.

Dos cambios de trazado de esta version:
  * Todo se corre 600 px a la derecha para abrir un carril izquierdo:
    ahi va CREDENCIAL, entre DOCENTE y ESTUDIANTE, con sus dos rombos
    "accede como" alineados con cada uno -- dos tramos ortogonales.
  * REPORTE deja la banda de abajo y pasa al cuadro libre que encierran
    EXPERIENCIA, EXPERIENCIA_EVIDENCIA, INSCRIPCION y RESULTADO: sus dos
    relaciones derivadas quedan cortas y dentro de ese cuadro, en vez de
    cruzar medio mapa.
"""
import generador as g
from vistas_chen import Lienzo
from datos_mer import (RELACIONES, ENTIDADES, N_ENTIDADES, N_REL_REALES,
                       N_REL_DERIVADAS, N_ATRIBUTOS)

# --------------------------------------------------------------- reticula
X0 = 420                                             # carril de CREDENCIAL
C1, C2, C3, C4, C5 = 1080, 1900, 2720, 3540, 4360    # columnas
F1, F2, F3, F4 = 170, 870, 1570, 2270                # filas
FM = (F2 + F3) // 2                                  # fila media: 1220

DX = 195          # cuanto se corre la columna de atributos hacia el costado
CAIDA = 140       # cuanto baja el primer atributo respecto al centro de la caja

m = Lienzo()


def ent(nombre, cx, cy, lado="right", **kw):
    """Entidad con su columna de atributos corrida a un costado."""
    dx = DX if lado == "right" else -DX
    return m.ent(nombre, cx, cy, dx=dx, side=lado, first_row=cy + CAIDA, **kw)


# -------------------------------------------------- carril de acceso (x0)
ent("CREDENCIAL", X0, FM, lado="left")

# ---------------------------------------------- fila 1 - curriculo oficial
ent("DBA",                C2, F1)
ent("EVIDENCIA",          C3, F1)
ent("EVIDENCIA_DICTAMEN", C4, F1)

# ------------------------------------ fila 2 - autoria y banco de contenido
# DOCENTE cuelga a la IZQUIERDA: por su derecha pasa 'crea'.
ent("DOCENTE",               C1, F2, lado="left")
# EXPERIENCIA a la IZQUIERDA: su derecha da al cuadro central de REPORTE.
ent("EXPERIENCIA",           C2, F2, lado="left")
ent("EXPERIENCIA_EVIDENCIA", C3, F2)
ent("ITEM",                  C4, F2)
ent("OPCION",                C5, F2)

# --------------------------------------- fila 3 - inscripcion y resultados
ent("ESTUDIANTE", C1, F3)
# INSCRIPCION a la IZQUIERDA: por su derecha sale la diagonal de 'atiende'.
ent("INSCRIPCION", C2, F3, lado="left")
ent("RESULTADO",   C3, F3)
m.asoc("RESPUESTA_OPCION", C5, F3, "selecciona", dx=-DX, first_row=F3 + CAIDA,
       razon_lado="izq", label_lado="der")

# ------------------------------------------- fila 4 - entrega y respuesta
ent("PRESENTACION", C4, F4)
ent("RESPUESTA",    C5, F4)

# ------------------------------------- cuadro central - lo que se calcula
# REPORTE no persiste: borde punteado, en el cuadro libre entre las cuatro
# entidades de las que depende. Su columna va a la izquierda, lejos de la
# diagonal de 'se agrega en'.
XR = (C2 + C3) // 2                                  # 2310
ent("REPORTE", XR, FM, lado="left", dashed=True)

# ------------------------------------------------------------ relaciones
m.rel("accede_docente",    X0, F2, razon_lado="izq")
m.rel("accede_estudiante", X0, F3, razon_lado="izq")
m.rel("comprende",    2310, F1)
m.rel("se dictamina", 3130, F1)
m.rel("se ancla a",   C2,   520,  razon_lado="izq")
m.rel("sobre",        C3,   520,  razon_lado="izq")
m.rel("crea",         1490, F2)
m.rel("incluye",      2310, F2)
m.rel("genera",       3130, F2)
m.rel("ofrece",       3950, F2)
m.rel("pertenece a",  C2,   FM,   razon_lado="izq")
m.rel("mide",         C3,   FM,   razon_lado="izq")
m.rel("realiza",      1490, F3)
m.rel("arroja",       2310, F3)
m.rel("se presenta",  C4,   F3,   razon_lado="izq")
m.rel("atiende",      2650, 1950)
m.rel("registra",     3950, F4)
m.rel("resume",       XR,   FM - 180, razon_lado="izq")
m.rel("se agrega en", XR,   FM + 180, razon_lado="izq")

# ------------------------------------------------------------- conexiones
m.conecta("CREDENCIAL", "accede_docente", "DOCENTE")
m.conecta("CREDENCIAL", "accede_estudiante", "ESTUDIANTE")
# {xor}: punteado vertical que une las dos «accede como» (RI-12), a la derecha
# de CREDENCIAL, de una linea de relacion a la otra
m.body += (f'<line x1="600" y1="{F2}" x2="600" y2="{F3}" stroke="#B4536B" stroke-width="1.4" '
           f'stroke-dasharray="5,4"/>\n'
           f'<text x="612" y="{FM - 6}" font-family="Helvetica" font-size="13" font-weight="700" '
           f'fill="#B4536B">{{xor}}</text>\n'
           f'<text x="612" y="{FM + 12}" font-family="Helvetica" font-size="11" '
           f'fill="#B4536B">un solo rol (RI-12)</text>\n')
m.conecta("DBA", "comprende", "EVIDENCIA")
m.conecta("EVIDENCIA", "se dictamina", "EVIDENCIA_DICTAMEN")
m.conecta("EXPERIENCIA", "se ancla a", "DBA")
m.conecta("EVIDENCIA", "sobre", "EXPERIENCIA_EVIDENCIA")
m.conecta("DOCENTE", "crea", "EXPERIENCIA")
m.conecta("EXPERIENCIA", "incluye", "EXPERIENCIA_EVIDENCIA")
m.conecta("EXPERIENCIA_EVIDENCIA", "genera", "ITEM")
m.conecta("ITEM", "ofrece", "OPCION")
m.conecta("INSCRIPCION", "pertenece a", "EXPERIENCIA")
m.conecta("EXPERIENCIA_EVIDENCIA", "mide", "RESULTADO")
m.conecta("ESTUDIANTE", "realiza", "INSCRIPCION")
m.conecta("ITEM", "se presenta", "PRESENTACION")
m.conecta("INSCRIPCION", "arroja", "RESULTADO")
m.conecta("INSCRIPCION", "atiende", "PRESENTACION")
m.conecta("PRESENTACION", "registra", "RESPUESTA")
m.conecta_asoc("RESPUESTA", "RESPUESTA_OPCION", "OPCION")
# las dos derivadas, cortas, dentro del cuadro central
m.conecta("RESULTADO", "se agrega en", "REPORTE")
m.conecta("REPORTE", "resume", "EXPERIENCIA", off_b=22)

# ---------------------------------------------------------------- rotulo
NOTA = [
    f"MAPA COMPLETO · {N_ENTIDADES} entidades + Reporte (derivado) · {N_ATRIBUTOS} atributos · "
    f"{N_REL_REALES + N_REL_DERIVADAS} relaciones ({N_REL_REALES} propias + {N_REL_DERIVADAS} derivadas)",
    "Notación Chen estricta. Elipse negra = llave primaria. Subrayado punteado = llave parcial. "
    "Doble borde = entidad débil. Rombo doble = relación identificadora. Sin llaves foráneas: "
    "las deriva el modelo relacional de cada relación (H-8).",
    "Línea doble = participación total. (mín, máx) junto a cada entidad; razón de cardinalidad "
    "(1:1, 1:n, n:m) bajo cada rombo. Elipse punteada = derivado. Punteado {xor} = relaciones "
    "excluyentes. Rombo y caja punteados = derivados, no persisten.",
]
for i, linea in enumerate(NOTA):
    peso = "700" if i == 0 else "400"
    col = "#555555" if i == 0 else "#888888"
    esp = ' letter-spacing="1.5"' if i == 0 else ""
    m.body = (f'<text x="40" y="{46 + i * 20}" font-family="Helvetica" '
              f'font-size="13" font-weight="{peso}" fill="{col}"{esp}>'
              f'{linea}</text>\n') + m.body

MAPA = g.wrap_svg(4800, int(m.fondo_max + 70), m.body)

CAPTION = (
    "<b>El mapa completo y las siete vistas dicen exactamente lo mismo</b>: los dos "
    "salen de <code>datos_mer.py</code>, así que no pueden desalinearse. "
    f"<b>Los {N_ATRIBUTOS} atributos están todos aquí</b>, en elipses —notación Chen—. "
    "Cada entidad cuelga su columna corrida a un costado, del lado por donde no pasa "
    "ninguna línea. "
    "<b>CREDENCIAL ocupa un carril propio a la izquierda</b>, entre DOCENTE y "
    "ESTUDIANTE: una misma credencial accede como uno de los dos, nunca como ambos "
    "(RI-12). "
    "<b>REPORTE va al centro y con borde punteado</b>: no persiste, se calcula sobre "
    "RESULTADO por cada EXPERIENCIA, y por eso sus dos relaciones derivadas quedan "
    "cortas, dentro del cuadro que forman las cuatro entidades de las que depende.")

if __name__ == "__main__":
    open("mapa-chen.svg", "w", encoding="utf-8").write(MAPA)
    ids = {r.get("id", r["nombre"]) for r in RELACIONES}
    faltan = ids - {k[1:] for k in m.pos if k.startswith("◇")} - {"selecciona"}
    assert not faltan, f"relaciones sin dibujar en el mapa: {faltan}"
    cajas = [k for k in m.pos if not k.startswith("◇")]
    assert len(cajas) == len(ENTIDADES), "falta alguna entidad en el mapa"
    print(f"mapa-chen.svg — {len(cajas)} cajas ({N_ENTIDADES} entidades + Reporte derivado), "
          f"{N_ATRIBUTOS} atributos, {len(ids)} relaciones, ninguna sin dibujar")
