"""Mapa completo del MER en notacion Chen -- Quinta revision.

Las 14 entidades (+ Reporte, derivado), sus 74 atributos y las 18
relaciones en un solo lienzo. Mismo contenido que las 6 vistas, porque
las dos cosas salen de datos_mer.py; lo unico que cambia es el layout.

Como se resolvio el problema de leer 74 elipses en un solo lienzo, sin
caer en cajas-tabla (que el docente Alexander no acepta):

  1. Cada entidad cuelga su columna de atributos DESPLAZADA a un costado,
     no centrada debajo. Asi la vertical que sale de la entidad --que es
     por donde pasan sus relaciones-- queda siempre libre.
  2. La reticula se separa lo necesario para que ninguna columna invada
     la fila siguiente. Un MER completo con atributos es grande: se lee
     ampliando, y eso es normal en un modelo de este tamano.
  3. El costado de cada columna (izquierda o derecha) no se eligio por
     estetica sino por trafico: va del lado por donde NO pasa una linea.

Todo esto lo comprueba _verificar_mapa.py por coordenadas, no a ojo.
"""
import generador as g
from vistas_chen import Lienzo
from datos_mer import RELACIONES, ENTIDADES

# --------------------------------------------------------------- reticula
C1, C2, C3, C4, C5 = 480, 1300, 2120, 2940, 3760      # columnas
F1, F2, F3, F4 = 170, 870, 1570, 2270                 # filas
F5 = 2850                                             # banda de lo derivado

DX = 195          # cuanto se corre la columna de atributos hacia el costado
CAIDA = 140       # cuanto baja el primer atributo respecto al centro de la caja

m = Lienzo()


def ent(nombre, cx, cy, lado="right", **kw):
    """Entidad con su columna de atributos corrida a un costado."""
    dx = DX if lado == "right" else -DX
    return m.ent(nombre, cx, cy, dx=dx, side=lado, first_row=cy + CAIDA, **kw)


# ---------------------------------------------- fila 1 - curriculo oficial
ent("DBA",                C2, F1)
ent("EVIDENCIA",          C3, F1)
ent("EVIDENCIA_DICTAMEN", C4, F1)

# ------------------------------------ fila 2 - autoria y banco de contenido
# DOCENTE cuelga a la IZQUIERDA: por su derecha pasa 'crea' y, mas abajo,
# la diagonal punteada de 'resume'.
ent("DOCENTE",               C1, F2, lado="left")
ent("EXPERIENCIA",           C2, F2)
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

# ------------------------------------------------- banda de lo derivado
# REPORTE no persiste, se calcula: borde punteado y fila propia, abajo.
ent("REPORTE", C1, F5, dashed=True)

# ------------------------------------------------------------ relaciones
m.rel("comprende",    1710, F1)
m.rel("se dictamina", 2530, F1)
m.rel("se ancla a",   C2,   520,  razon_lado="izq")
m.rel("sobre",        C3,   520,  razon_lado="izq")
m.rel("crea",          890, F2)
m.rel("incluye",      1710, F2)
m.rel("genera",       2530, F2)
m.rel("ofrece",       3350, F2)
m.rel("pertenece a",  C2,   1220, razon_lado="izq")
m.rel("mide",         C3,   1220, razon_lado="izq")
m.rel("realiza",       890, F3)
m.rel("arroja",       1710, F3)
m.rel("se presenta",  C4,   F3,   razon_lado="izq")
m.rel("atiende",      2050, 1950)
m.rel("registra",     3350, F4)
m.rel("resume",        170, F3,   razon_lado="izq")
m.rel("se agrega en", C2,   F5)

# ------------------------------------------------------------- conexiones
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

# EXPERIENCIA tiene 5 relaciones y un rectangulo tiene 4 lados: 'resume'
# comparte el lado izquierdo con 'crea' y se baja 22px para no pisarla.
m.conecta("RESULTADO", "se agrega en", "REPORTE")
m.conecta("REPORTE", "resume", "EXPERIENCIA", off_b=22)

# ---------------------------------------------------------------- rotulo
# El conteo dice lo mismo que 01-modelo-entidad-relacion.md: 14 entidades,
# porque Reporte no cuenta -- es vista derivada, no persiste.
N_ATTR = sum(len(e[2]) for e in ENTIDADES)
NOTA = [
    f"MAPA COMPLETO · 14 entidades + Reporte (derivado) · {N_ATTR} atributos · "
    "18 relaciones (16 propias + 2 derivadas)",
    "Notación Chen. Elipse negra = llave primaria. Doble borde = entidad débil. "
    "Rombo doble = relación identificadora.",
    "Línea doble = participación total. Punteado = derivado, no persiste. "
    "Junto a cada rombo, la razón de cardinalidad (1:1, 1:n, n:m).",
]
for i, linea in enumerate(NOTA):
    peso = "700" if i == 0 else "400"
    col = "#555555" if i == 0 else "#888888"
    esp = ' letter-spacing="1.5"' if i == 0 else ""
    m.body = (f'<text x="40" y="{46 + i * 20}" font-family="Helvetica" '
              f'font-size="13" font-weight="{peso}" fill="{col}"{esp}>'
              f'{linea}</text>\n') + m.body

MAPA = g.wrap_svg(4200, int(m.fondo_max + 70), m.body)

CAPTION = (
    "<b>El mapa completo y las seis vistas dicen exactamente lo mismo</b>: los dos "
    "salen de <code>datos_mer.py</code>, así que no pueden desalinearse. "
    "<b>Los 74 atributos están todos aquí</b>, en elipses —notación Chen—, no en "
    "cajas-tabla. Para que se lean, cada entidad cuelga su columna corrida a un "
    "costado en vez de centrada debajo: así la vertical que sale de la caja, que es "
    "por donde pasan sus relaciones, queda siempre libre. El costado de cada columna "
    "no se eligió por estética sino por tráfico: va del lado por donde no pasa "
    "ninguna línea. "
    "<b>El trazado tampoco es decorativo:</b> las 16 relaciones propias quedan "
    "ortogonales y sin un solo cruce. El único cruce del mapa cae sobre "
    "<i>se agrega en</i>, que es una relación <b>derivada</b> (punteada), y ahí es "
    "donde menos estorba: se lee como la capa calculada pasando por encima de la "
    "capa que sí se almacena, que es exactamente lo que es. "
    "<b>Reporte se dibuja aparte, abajo y con borde punteado</b>, por la misma "
    "razón: no persiste. Por eso el conteo dice <i>14 entidades + Reporte</i>.")

if __name__ == "__main__":
    open("mapa-chen.svg", "w", encoding="utf-8").write(MAPA)
    dibujadas = {r["nombre"] for r in RELACIONES}
    faltan = dibujadas - {k[1:] for k in m.pos if k.startswith("◇")} - {"selecciona"}
    assert not faltan, f"relaciones sin dibujar en el mapa: {faltan}"
    cajas = [k for k in m.pos if not k.startswith("◇")]
    assert len(cajas) == len(ENTIDADES), "falta alguna entidad en el mapa"
    print(f"mapa-chen.svg — {len(cajas)} cajas (14 entidades + Reporte derivado), "
          f"{N_ATTR} atributos, {len(dibujadas)} relaciones, ninguna sin dibujar")
