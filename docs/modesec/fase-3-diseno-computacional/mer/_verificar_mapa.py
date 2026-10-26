"""Verifica GEOMETRICAMENTE un SVG del MER, en vez de revisarlo a ojo.

Detecta las tres fallas que aparecieron revisando a mano el mapa completo:

  1. una linea de conexion que atraviesa la caja de una entidad ajena
  2. una linea que atraviesa un rombo ajeno
  3. dos rotulos de texto encimados, o una linea que tacha un rotulo
  4. algo dibujado fuera del lienzo, que en el PNG sale recortado

Uso:  python3 _verificar_mapa.py mapa-chen.svg [vista1.svg ...]
Sin argumentos revisa el mapa completo y las siete vistas.
"""
import re
import sys

TOL = 3.0          # holgura: tocar el borde es legitimo, atravesar no
SOLAPE_TXT = 4.0   # px de traslape a partir del cual dos rotulos estorban


def _num(s):
    return float(s)


def leer(path):
    svg = open(path, encoding="utf-8").read()
    rects, lines, polys, texts = [], [], [], []
    mv = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg)
    lienzo = (_num(mv.group(1)), _num(mv.group(2))) if mv else None

    for m in re.finditer(r'<rect ([^>]*)/>', svg):
        a = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', m.group(1)))
        if "width" not in a or "x" not in a:
            continue
        # el fondo del lienzo (wrap_svg) no es una entidad: se descarta o
        # toda linea del diagrama figuraria como si lo atravesara
        if a.get("fill") == "#F3F5F8":
            continue
        x, y = _num(a["x"]), _num(a["y"])
        rects.append((x, y, x + _num(a["width"]), y + _num(a["height"])))

    for m in re.finditer(r'<line ([^>]*)/>', svg):
        a = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', m.group(1)))
        lines.append((_num(a["x1"]), _num(a["y1"]), _num(a["x2"]), _num(a["y2"])))

    for m in re.finditer(r'<polygon points="([^"]*)"', svg):
        pts = [tuple(map(_num, p.split(","))) for p in m.group(1).split()]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        polys.append((min(xs), min(ys), max(xs), max(ys)))

    for m in re.finditer(r'<text ([^>]*)>([^<]*)</text>', svg):
        a = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', m.group(1)))
        txt = m.group(2).strip()
        if not txt:
            continue
        size = _num(a.get("font-size", "13"))
        w = len(txt) * size * 0.58
        anchor = a.get("text-anchor", "start")
        x, y = _num(a["x"]), _num(a["y"])
        x0 = {"middle": x - w / 2, "end": x - w}.get(anchor, x)
        texts.append((x0, y - size * 0.8, x0 + w, y + size * 0.25, txt))

    return rects, lines, polys, texts, lienzo


def corta_caja(seg, caja):
    """True si el segmento entra al interior de la caja (encogida por TOL)."""
    x1, y1, x2, y2 = seg
    a, b, c, d = caja[0] + TOL, caja[1] + TOL, caja[2] - TOL, caja[3] - TOL
    if c <= a or d <= b:
        return False
    # recorte de Liang-Barsky
    t0, t1 = 0.0, 1.0
    dx, dy = x2 - x1, y2 - y1
    for p, q in ((-dx, x1 - a), (dx, c - x1), (-dy, y1 - b), (dy, d - y1)):
        if p == 0:
            if q < 0:
                return False
        else:
            r = q / p
            if p < 0:
                if r > t1:
                    return False
                t0 = max(t0, r)
            else:
                if r < t0:
                    return False
                t1 = min(t1, r)
    return t0 < t1


def solapan(a, b):
    ox = min(a[2], b[2]) - max(a[0], b[0])
    oy = min(a[3], b[3]) - max(a[1], b[1])
    return ox > SOLAPE_TXT and oy > SOLAPE_TXT


def revisar(path):
    rects, lines, polys, texts, lienzo = leer(path)
    fallas = []

    # 4. algo dibujado fuera del lienzo: se ve recortado en el PNG
    if lienzo:
        W, H = lienzo
        for t in texts:
            if t[0] < 0 or t[2] > W or t[1] < 0 or t[3] > H:
                fallas.append(f"el rotulo '{t[4]}' se sale del lienzo "
                              f"({int(t[0])}..{int(t[2])} de 0..{int(W)})")
        for caja in rects + polys:
            if caja[0] < 0 or caja[2] > W or caja[1] < 0 or caja[3] > H:
                fallas.append(f"figura fuera del lienzo: {tuple(map(int, caja))}")

    for seg in lines:
        for caja in rects:
            if corta_caja(seg, caja):
                fallas.append(f"linea {tuple(map(int, seg))} atraviesa caja "
                              f"{tuple(map(int, caja))}")
        for rombo in polys:
            if corta_caja(seg, rombo):
                fallas.append(f"linea {tuple(map(int, seg))} atraviesa rombo "
                              f"{tuple(map(int, rombo))}")

    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            if solapan(texts[i], texts[j]):
                fallas.append(f"rotulos encimados: '{texts[i][4]}' y '{texts[j][4]}' "
                              f"cerca de ({int(texts[i][0])},{int(texts[i][1])})")

    for seg in lines:
        for t in texts:
            if corta_caja(seg, t[:4]):
                fallas.append(f"la linea {tuple(map(int, seg))} tacha el rotulo "
                              f"'{t[4]}'")

    return fallas


if __name__ == "__main__":
    objetivos = sys.argv[1:] or (
        ["mapa-chen.svg"] + [f"vista{i}.svg" for i in range(1, 8)])
    total = 0
    for path in objetivos:
        fallas = revisar(path)
        total += len(fallas)
        estado = "OK" if not fallas else f"{len(fallas)} FALLA(S)"
        print(f"\n{path}: {estado}")
        for f in fallas:
            print(f"   · {f}")
    print("\n" + "=" * 62)
    print("GEOMETRIA LIMPIA" if not total else f"{total} problema(s) a revisar")
    sys.exit(1 if total else 0)
