"""Las vistas del MER en notacion Chen -- version final de la Fase III (2026-10-21).

Todo el contenido sale de datos_mer.py; aca solo vive el LAYOUT (donde va
cada caja). La particion en vistas la verifica _verificar_vistas.py.

Convencion: una entidad muestra sus atributos solo en la vista donde se
presenta por primera vez. Cuando reaparece en otra vista es una COSTURA
--borde punteado, fondo de referencia, sin atributos-- para que nadie
cuente 20 entidades donde hay 14.
"""
import generador as g
from datos_mer import ENTIDADES, RELACIONES, VISTAS, DEBILES

ENT = {e[0]: e for e in ENTIDADES}
# Clave: 'id' si la relacion lo declara (dos relaciones pueden llamarse igual,
# como 'accede como' hacia DOCENTE y hacia ESTUDIANTE); si no, su nombre.
REL = {r.get("id", r["nombre"]): r for r in RELACIONES}

HALF_W, HALF_H = g.ENTIDAD_W / 2, g.ENTIDAD_H / 2


class Lienzo:
    def __init__(self):
        self.body = ""
        self.pos = {}          # nombre -> (cx, cy, half_w, half_h)
        self.fondo_max = 0

    # ---------------------------------------------------------- entidades
    def ent(self, nombre, cx, cy, dx=0, side="left", first_row=None, double=False,
            atributos=True, dashed=False):
        """Entidad primaria: caja + su columna de atributos.

        atributos=False la dibuja sin su columna de elipses -- lo que usa el
        mapa completo, donde 74 elipses en un solo lienzo no se leen."""
        _, cat, attrs = ENT[nombre]
        double = double or nombre in DEBILES        # debil -> doble borde
        svg, bb = g.entity_box(cx, cy, nombre, double=double, dashed=dashed)
        self.body += svg
        self.pos[nombre] = (cx, cy, (bb[2]-bb[0])/2, (bb[3]-bb[1])/2)
        if not atributos or not attrs:       # sin atributos propios: nada que colgar
            self.fondo_max = max(self.fondo_max, bb[3])
            return self
        fr = first_row if first_row is not None else cy + HALF_H + 130
        a_svg, bottom = g.attribute_stack(cx, bb[3], attrs, fr, side=side, column_dx=dx)
        self.body += a_svg
        self.fondo_max = max(self.fondo_max, bottom)
        return self

    def ref(self, nombre, cx, cy, vista_origen):
        """Costura: entidad ya presentada en otra vista."""
        svg, bb = g.entity_box(cx, cy, nombre, fill=g.REF_FILL, dashed=True,
                               double=nombre in DEBILES)
        svg += (f'<text x="{cx}" y="{bb[3] + 16}" text-anchor="middle" '
                f'font-family="Helvetica" font-size="11" fill="{g.GRIS_ATRIB}">'
                f'ya presentada · Vista {vista_origen}</text>\n')
        self.body += svg
        self.pos[nombre] = (cx, cy, (bb[2]-bb[0])/2, (bb[3]-bb[1])/2)
        self.fondo_max = max(self.fondo_max, cy + HALF_H + 30)
        return self

    def asoc(self, nombre, cx, cy, rel_nombre, dx=0, first_row=None,
             atributos=True, razon_lado="abajo", label_lado="arriba"):
        """Entidad asociativa: el rombo dentro del rectangulo."""
        _, cat, attrs = ENT[nombre]
        ra = REL[rel_nombre]
        svg, bb = g.associative_entity(
            cx, cy, nombre, rel_nombre,
            razon=g.razon_cardinalidad(ra["card_a"], ra["card_b"]),
            razon_lado=razon_lado, label_lado=label_lado)
        self.body += svg
        self.pos[nombre] = (cx, cy, (bb[2]-bb[0])/2, (bb[3]-bb[1])/2)
        self.fondo_max = max(self.fondo_max, bb[3] + 26)
        if not atributos or not attrs:
            return self
        fr = first_row if first_row is not None else bb[3] + 100
        a_svg, bottom = g.attribute_stack(cx, bb[3], attrs, fr, column_dx=dx)
        self.body += a_svg
        self.fondo_max = max(self.fondo_max, bottom)
        return self

    # --------------------------------------------------------- relaciones
    def rel(self, nombre, cx, cy, razon_lado="abajo"):
        r = REL[nombre]
        svg, _ = g.relation_diamond2(
            cx, cy, r["nombre"], ident=r.get("ident"), derivada=r.get("derivada"),
            razon=g.razon_cardinalidad(r["card_a"], r["card_b"]),
            razon_lado=razon_lado)
        self.body += svg
        hw = g.ROMBO_W / 2 + (7 if r.get("ident") else 0)
        hh = g.ROMBO_H / 2 + (7 if r.get("ident") else 0)
        self.pos["◇" + nombre] = (cx, cy, hw, hh)
        self.fondo_max = max(self.fondo_max, cy + hh + 26)
        return self

    def unir(self, entidad, relacion, card, total=False, derivada=False, off=0):
        """Une el borde de una entidad con el borde del rombo, por el eje
        que domine -- nunca una diagonal a angulo libre.

        off desplaza el punto de anclaje a lo largo de ese borde. Hace falta
        porque un rectangulo tiene 4 lados y EXPERIENCIA tiene 5 relaciones:
        sin desplazar, dos lineas salen del mismo punto y se pisan."""
        ex, ey, ehw, ehh = self.pos[entidad]
        rx, ry, rhw, rhh = self.pos["◇" + relacion]
        if abs(rx - ex) >= abs(ry - ey):                 # horizontal
            s = 1 if rx > ex else -1
            p1 = (ex + s * ehw, ey + off)
            p2 = (rx - s * rhw, ry)
        else:                                            # vertical
            s = 1 if ry > ey else -1
            p1 = (ex + off, ey + s * ehh)
            p2 = (rx, ry - s * rhh)
        self.body += g.link(p1[0], p1[1], p2[0], p2[1], card=card,
                            total=total, derivada=derivada)
        return self

    def conecta(self, a, relacion, b, off_a=0, off_b=0):
        """Une las dos puntas de una relacion leyendo cardinalidades y
        participacion de datos_mer.py -- no se escriben a mano aca. Junto a
        cada entidad va su (min,max); la razon (1:n) va bajo el rombo."""
        r = REL[relacion]
        d = r.get("derivada", False)
        self.unir(a, relacion, r["part_a"], r["total_a"], d, off=off_a)
        self.unir(b, relacion, r["part_b"], r["total_b"], d, off=off_b)
        return self

    def conecta_asoc(self, a, asociativa, b):
        """Las dos puntas de una relacion materializada como entidad
        asociativa: el rombo ya esta dentro del rectangulo, asi que las
        lineas van de cada entidad al borde de ese rectangulo. Las
        cardinalidades tambien salen de datos_mer.py."""
        r = REL[[k for k, v in REL.items()
                 if v.get("asociativa") == asociativa][0]]
        for ent_nombre, card, total in ((a, r["part_a"], r["total_a"]),
                                        (b, r["part_b"], r["total_b"])):
            ex, ey, ehw, ehh = self.pos[ent_nombre]
            ax, ay, ahw, ahh = self.pos[asociativa]
            if abs(ax - ex) >= abs(ay - ey):
                s = 1 if ax > ex else -1
                p1, p2 = (ex + s * ehw, ey), (ax - s * ahw, ay)
            else:
                s = 1 if ay > ey else -1
                p1, p2 = (ex, ey + s * ehh), (ax, ay - s * ahh)
            self.body += g.link(p1[0], p1[1], p2[0], p2[1], card=card, total=total)
        return self

    def rotulo(self, texto, x=40, y=44):
        self.body = (f'<text x="{x}" y="{y}" font-family="Helvetica" font-size="13" '
                     f'letter-spacing="1.5" fill="#888888">{texto}</text>\n'
                     + self.body)
        return self

    def titulo(self, n, x=40, y=44):
        t, sub = VISTAS[n]
        self.body = (f'<text x="{x}" y="{y}" font-family="Helvetica" font-size="13" '
                     f'letter-spacing="1.5" fill="#888888">VISTA {n} · {t.upper()}</text>\n'
                     + self.body)
        return self

    def svg(self, w):
        return g.wrap_svg(w, int(self.fondo_max + 60), self.body)
