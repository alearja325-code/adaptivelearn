"""Lienzo SVG para los diagramas UML de la Fase III.

Mismas reglas que los diagramas del MER (`../mer/generador.py`): todo se
ubica por coordenadas calculadas, nada a ojo, y la paleta es la misma
para que los entregables se vean como un solo trabajo.

Ademas de dibujar, el lienzo REGISTRA lo que dibuja -- cajas, textos y
tramos de linea -- y `verificar()` revisa la geometria por coordenadas:
dos textos que se encaraman, una linea que atraviesa un texto o una caja
que no es la suya, algo que se sale del lienzo. Es la misma idea de
`../mer/_verificar_mapa.py`, aplicada aqui al momento de generar: un
diagrama con un problema no se escribe.
"""
from html import escape

FUENTE = "Helvetica, Arial, sans-serif"
NEGRO = "#111111"
GRIS = "#555555"
GRIS_CLARO = "#888888"
AZUL_FILL, AZUL_STROKE, AZUL_TEXTO = "#DCE8FA", "#3B7DD8", "#1C3A5E"
CREMA = "#F5F3EE"
BLANCO = "#FFFFFF"
FONDO, FONDO_BORDE = "#F3F5F8", "#E3E7ED"
VERDE_FILL, VERDE_STROKE = "#E3F2E6", "#3C8D50"
AMBAR_FILL, AMBAR_STROKE = "#FFF4DC", "#C08A1E"


def ancho_texto(s, tam, negrita=False):
    """Estimacion conservadora del ancho de un texto en Helvetica.

    Por exceso a proposito: el verificador trabaja con esta medida, y es
    mejor que vea un choque que no hay a que deje pasar uno que si."""
    factor = 0.60 if negrita else 0.555
    anchos = sum(1.25 if c in "MWmw@%" else 0.62 if c in "il.,:;!|'()[] " else 1.0
                 for c in s)
    return anchos * tam * factor


def partir(s, max_chars):
    """Parte un texto en lineas de a lo sumo max_chars, por palabras."""
    lineas, actual = [], ""
    for palabra in s.split():
        prueba = f"{actual} {palabra}".strip()
        if len(prueba) <= max_chars or not actual:
            actual = prueba
        else:
            lineas.append(actual)
            actual = palabra
    if actual:
        lineas.append(actual)
    return lineas


def _caja_cruza(a, b, holgura=0.0):
    return not (a[2] <= b[0] + holgura or b[2] <= a[0] + holgura or
                a[3] <= b[1] + holgura or b[3] <= a[1] + holgura)


def _segmento_cruza(p, q, r, margen=1.5):
    """True si el segmento p-q entra al interior del rectangulo r (encogido)."""
    x0, y0, x1, y1 = r[0] + margen, r[1] + margen, r[2] - margen, r[3] - margen
    if x0 >= x1 or y0 >= y1:
        return False
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pk, qk in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pk == 0:
            if qk < 0:
                return False
        else:
            t = qk / pk
            if pk < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return t1 - t0 > 1e-6


class Lienzo:
    def __init__(self, ancho, alto):
        self.ancho, self.alto = ancho, alto
        self.partes = []
        self.textos = []      # (bbox, texto, id_dueno)
        self.cajas = {}       # id -> bbox (obstaculo para las lineas)
        self.tramos = []      # (p, q, ids permitidos, descripcion)

    # ------------------------------------------------------------ texto
    def texto(self, x, y, s, tam=13, peso=400, color=NEGRO, anchor="start",
              cursiva=False, subrayado=False, dueno=None, registrar=True):
        s = str(s)
        w = ancho_texto(s, tam, peso >= 600)
        x0 = x if anchor == "start" else x - w / 2 if anchor == "middle" else x - w
        if registrar:
            self.textos.append(((x0, y - 0.78 * tam, x0 + w, y + 0.24 * tam), s, dueno))
        extra = ' font-style="italic"' if cursiva else ""
        extra += ' text-decoration="underline"' if subrayado else ""
        self.partes.append(
            f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
            f'font-family="{FUENTE}" font-size="{tam}" font-weight="{peso}" '
            f'fill="{color}"{extra}>{escape(s)}</text>')
        return w

    # ----------------------------------------------------------- formas
    def rect(self, x, y, w, h, fill=BLANCO, stroke=NEGRO, sw=1.5, rx=0,
             dash=None, id=None, obstaculo=True):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.partes.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx}" ry="{rx}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}"{d}/>')
        if id and obstaculo:
            self.cajas[id] = (x, y, x + w, y + h)
        return (x, y, x + w, y + h)

    def elipse(self, cx, cy, rx, ry, fill=BLANCO, stroke=NEGRO, sw=1.5,
               dash=None, id=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.partes.append(
            f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
        if id:
            # el obstaculo es el rectangulo inscrito: una linea que solo
            # roza la esquina de la caja envolvente no toca la elipse
            k = 0.70
            self.cajas[id] = (cx - rx * k, cy - ry * k, cx + rx * k, cy + ry * k)

    def poligono(self, pts, fill=BLANCO, stroke=NEGRO, sw=1.5):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.partes.append(f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" '
                           f'stroke-width="{sw}"/>')

    def crudo(self, svg):
        self.partes.append(svg)

    # ----------------------------------------------------------- lineas
    def linea(self, pts, color=GRIS, sw=1.4, dash=None, fin=None, inicio=None,
              permitidos=(), desc="", registrar=True):
        """Polilinea. fin/inicio: nombre de marcador (ver MARCADORES)."""
        d = f' stroke-dasharray="{dash}"' if dash else ""
        me = f' marker-end="url(#{fin})"' if fin else ""
        ms = f' marker-start="url(#{inicio})"' if inicio else ""
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.partes.append(f'<polyline points="{p}" fill="none" stroke="{color}" '
                           f'stroke-width="{sw}"{d}{me}{ms}/>')
        if registrar:
            for a, b in zip(pts, pts[1:]):
                self.tramos.append((a, b, set(permitidos), desc))

    # ------------------------------------------------------- verificar
    def verificar(self):
        problemas = []
        T = self.textos
        for i in range(len(T)):
            for j in range(i + 1, len(T)):
                if _caja_cruza(T[i][0], T[j][0], 0.5):
                    problemas.append(f"textos encaramados: «{T[i][1]}» / «{T[j][1]}»")
        for p, q, perm, desc in self.tramos:
            for bbox, s, dueno in T:
                if dueno is not None and dueno in perm:
                    continue
                if _segmento_cruza(p, q, bbox, 0.8):
                    problemas.append(f"la linea {desc} tacha el texto «{s}»")
            for id_, bbox in self.cajas.items():
                if id_ in perm:
                    continue
                if _segmento_cruza(p, q, bbox):
                    problemas.append(f"la linea {desc} atraviesa la caja {id_}")
        ids = list(self.cajas)
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                if _caja_cruza(self.cajas[ids[i]], self.cajas[ids[j]]):
                    problemas.append(f"cajas encimadas: {ids[i]} / {ids[j]}")
        for bbox, s, _ in T:
            if bbox[0] < 0 or bbox[1] < 0 or bbox[2] > self.ancho or bbox[3] > self.alto:
                problemas.append(f"texto fuera del lienzo: «{s}»")
        for id_, b in self.cajas.items():
            if b[0] < 0 or b[1] < 0 or b[2] > self.ancho or b[3] > self.alto:
                problemas.append(f"caja fuera del lienzo: {id_}")
        return problemas

    # ------------------------------------------------------------- svg
    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.ancho} '
                f'{self.alto}" width="{self.ancho}" height="{self.alto}">\n'
                f'{MARCADORES}\n'
                f'<rect x="0" y="0" width="{self.ancho}" height="{self.alto}" '
                f'fill="{FONDO}" rx="20" ry="20" stroke="{FONDO_BORDE}"/>\n'
                + "\n".join(self.partes) + "\n</svg>\n")


MARCADORES = f"""<defs>
  <marker id="lleno" viewBox="0 0 12 10" refX="11.5" refY="5" markerWidth="12" markerHeight="10" markerUnits="userSpaceOnUse" orient="auto">
    <path d="M0,0 L12,5 L0,10 z" fill="{NEGRO}"/></marker>
  <marker id="abierta" viewBox="0 0 12 10" refX="11.5" refY="5" markerWidth="12" markerHeight="10" markerUnits="userSpaceOnUse" orient="auto">
    <path d="M0,0 L12,5 L0,10" fill="none" stroke="{NEGRO}" stroke-width="1.4"/></marker>
  <marker id="abierta_gris" viewBox="0 0 12 10" refX="11.5" refY="5" markerWidth="12" markerHeight="10" markerUnits="userSpaceOnUse" orient="auto">
    <path d="M0,0 L12,5 L0,10" fill="none" stroke="{GRIS}" stroke-width="1.4"/></marker>
  <marker id="herencia" viewBox="0 0 18 16" refX="17" refY="8" markerWidth="18" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto">
    <path d="M0,0 L17,8 L0,16 z" fill="{BLANCO}" stroke="{NEGRO}" stroke-width="1.4"/></marker>
  <marker id="rombo" viewBox="0 0 22 12" refX="1" refY="6" markerWidth="22" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto">
    <path d="M1,6 L11,1 L21,6 L11,11 z" fill="{NEGRO}" stroke="{NEGRO}" stroke-width="1"/></marker>
</defs>"""
