"""Diagramas de secuencia, trazados desde `datos_secuencias.py`.

El ancho entre lineas de vida no es fijo: se abre lo necesario para que
el rotulo de cada mensaje quepa entre sus dos extremos. Los fragmentos
(alt, opt, loop) se ajustan a los participantes que tocan sus mensajes,
y un fragmento anidado queda siempre dentro del que lo contiene.
"""
from lienzo import (Lienzo, ancho_texto, partir, NEGRO, GRIS, GRIS_CLARO, BLANCO, CREMA,
                    AZUL_FILL, AMBAR_FILL, AMBAR_STROKE)
from datos_secuencias import SECUENCIAS

T = 12            # tamano de los rotulos de mensaje
TOP = 70          # y de la cabecera de los participantes
H_CAB = 46


def rotulo_cab(p):
    pid, rot, clase, tipo = p
    return rot


def ancho_cab(p):
    pid, rot, clase, tipo = p
    if tipo == "actor":
        return max(90, ancho_texto(rot, 13, True) + 10)
    extra = ancho_texto("«IGU»", 11) if tipo == "igu" else 0
    return max(130, ancho_texto(rot, 13, True) + 26, extra)


def numerar(pasos):
    n, salida = 0, []
    for p in pasos:
        if p[0] in ("m", "c", "s"):
            n += 1
            salida.append((p, f"{n}: "))
        else:
            salida.append((p, ""))
    return salida


def posiciones(sec):
    parts = sec["participantes"]
    idx = {p[0]: i for i, p in enumerate(parts)}
    w = [ancho_cab(p) for p in parts]
    gaps = [max(w[i] / 2 + w[i + 1] / 2 + 46, 170) for i in range(len(parts) - 1)]
    req = []                                   # (i, j, distancia minima)
    for paso, num in numerar(sec["pasos"]):
        k = paso[0]
        if k in ("m", "r", "c"):
            i, j = idx[paso[1]], idx[paso[2]]
            a, b = min(i, j), max(i, j)
            lw = ancho_texto(num + paso[3], T) + 36
            if k == "c":
                lw += w[idx[paso[2]]] / 2
            req.append((a, b, lw))
        elif k == "s":
            i = idx[paso[1]]
            if i + 1 < len(parts):
                req.append((i, i + 1, 56 + ancho_texto(num + paso[2], T) + 24))
    for _ in range(100):
        cambio = False
        for a, b, d in req:
            actual = sum(gaps[a:b])
            if actual < d:
                gaps[b - 1] += d - actual
                cambio = True
        if not cambio:
            break
    xs = [100 + w[0] / 2]
    for g in gaps:
        xs.append(xs[-1] + g)
    return idx, w, xs


def cabecera(L, p, x, y, w):
    pid, rot, clase, tipo = p
    if tipo == "actor":
        L.crudo(f'<circle cx="{x}" cy="{y + 8}" r="8" fill="{BLANCO}" stroke="{NEGRO}" stroke-width="1.5"/>'
                f'<line x1="{x}" y1="{y + 16}" x2="{x}" y2="{y + 32}" stroke="{NEGRO}" stroke-width="1.5"/>'
                f'<line x1="{x - 12}" y1="{y + 22}" x2="{x + 12}" y2="{y + 22}" stroke="{NEGRO}" stroke-width="1.5"/>'
                f'<line x1="{x}" y1="{y + 32}" x2="{x - 10}" y2="{y + 44}" stroke="{NEGRO}" stroke-width="1.5"/>'
                f'<line x1="{x}" y1="{y + 32}" x2="{x + 10}" y2="{y + 44}" stroke="{NEGRO}" stroke-width="1.5"/>')
        L.cajas[pid] = (x - 14, y, x + 14, y + 45)
        L.texto(x, y + 60, rot, tam=13, peso=700, anchor="middle", dueno=pid)
        return y + 66
    fill = {"igu": AMBAR_FILL, "objeto": AZUL_FILL, "externo": BLANCO, "bd": "#ECEEF1"}[tipo]
    stroke = AMBAR_STROKE if tipo == "igu" else NEGRO
    dash = "6,4" if tipo == "externo" else None
    L.rect(x - w / 2, y, w, H_CAB, fill=fill, stroke=stroke, sw=1.5, dash=dash, id=pid)
    sub = {"igu": "«IGU»", "externo": "«interfaz externa»", "bd": "«persistencia»"}.get(tipo)
    if sub:
        L.texto(x, y + 17, sub, tam=10.5, color=GRIS, anchor="middle", dueno=pid)
        L.texto(x, y + 35, rot, tam=13, peso=700, anchor="middle", dueno=pid,
                subrayado=tipo == "objeto")
    else:
        L.texto(x, y + 28, rot, tam=13, peso=700, anchor="middle", dueno=pid,
                subrayado=tipo == "objeto")
    return y + H_CAB


def dibujar(sec):
    parts = sec["participantes"]
    idx, w, xs = posiciones(sec)
    creados = {p[2] for p in sec["pasos"] if p[0] == "c"}
    # --- primera pasada: alturas y fragmentos
    y = TOP + 66 + 26
    eventos = []          # (paso, num, y)
    pila, fragmentos = [], []
    for paso, num in numerar(sec["pasos"]):
        k = paso[0]
        if k in ("m", "r"):
            y += 32
        elif k == "c":
            y += 50
        elif k == "s":
            y += 34
        elif k == "ini":
            y += 14
            fr = dict(op=paso[1], guarda=paso[2], top=y, ramas=[], parts=set(), hijos=[],
                      extra_der=0)
            if pila:
                pila[-1]["hijos"].append(fr)
            else:
                fragmentos.append(fr)
            pila.append(fr)
            y += 22
        elif k == "sino":
            y += 14
            pila[-1]["ramas"].append((y, paso[1]))
            y += 22
        elif k == "fin":
            y += 12
            fr = pila.pop()
            fr["bot"] = y
            y += 4
        elif k == "nota":
            lineas = partir(paso[2], 52)
            y += 16 + 15 * len(lineas) + 12
            # una nota dentro de un fragmento lo ensancha hasta cubrirla
            der = xs[idx[paso[1]]] + 16 + max(ancho_texto(t, 11.5) for t in lineas) + 22
            for fr in pila:
                fr["extra_der"] = max(fr["extra_der"], der)
        eventos.append((paso, num, y))
        if k in ("m", "r", "c") and pila:
            for fr in pila:
                fr["parts"] |= {idx[paso[1]], idx[paso[2]]}
        if k in ("s",) and pila:
            for fr in pila:
                fr["parts"].add(idx[paso[1]])
                fr["extra_der"] = max(fr["extra_der"],
                                      xs[idx[paso[1]]] + 56 + ancho_texto(num + paso[2], T))
    alto = y + 70
    ancho_der = max([xs[-1] + w[-1] / 2] + [xs[idx[p[1]]] + 60 + ancho_texto(n + p[2], T)
                                              for p, n in numerar(sec["pasos"]) if p[0] == "s"]
                    + [xs[idx[p[1]]] + 30 + 380 for p, _ in numerar(sec["pasos"]) if p[0] == "nota"])
    L = Lienzo(max(int(ancho_der + 70), 1320), int(alto))
    L.texto(32, 40, f"Diagrama de secuencia {sec['id'][-1]} · {sec['titulo']}", tam=16, peso=700,
            color="#333333")
    L.texto(L.ancho - 32, 40, "Casos de uso: " + ", ".join(sec["cus"]), tam=12, color=GRIS,
            anchor="end")

    # --- fragmentos (debajo de todo lo demas)
    def rango(fr, prof):
        xs_f = [xs[i] for i in fr["parts"]] or [xs[0]]
        x0, x1 = min(xs_f) - 64 + prof * 8, max(xs_f) + 64 - prof * 8
        if fr["extra_der"]:
            x1 = max(x1, fr["extra_der"] + 14)
        for h in fr["hijos"]:
            hx0, hx1 = rango(h, prof + 1)
            x0, x1 = min(x0, hx0 - 10), max(x1, hx1 + 10)
        fr["x0"], fr["x1"], fr["prof"] = x0, x1, prof
        return x0, x1

    def pintar(fr):
        x0, x1 = fr["x0"], fr["x1"]
        L.rect(x0, fr["top"], x1 - x0, fr["bot"] - fr["top"], fill="none", stroke=GRIS, sw=1.2)
        tw = ancho_texto(fr["op"], 12, True) + 16
        L.crudo(f'<path d="M{x0},{fr["top"]} L{x0 + tw},{fr["top"]} L{x0 + tw},{fr["top"] + 12} '
                f'L{x0 + tw - 7},{fr["top"] + 20} L{x0},{fr["top"] + 20} Z" fill="{BLANCO}" '
                f'stroke="{GRIS}" stroke-width="1.2"/>')
        L.texto(x0 + 6, fr["top"] + 15, fr["op"], tam=12, peso=700, dueno="frag")
        L.texto(x0 + tw + 8, fr["top"] + 15, f"[{fr['guarda']}]", tam=12, color=GRIS,
                cursiva=True, dueno="frag")
        for yy, guarda in fr["ramas"]:
            L.crudo(f'<line x1="{x0}" y1="{yy}" x2="{x1}" y2="{yy}" stroke="{GRIS}" '
                    f'stroke-width="1.1" stroke-dasharray="6,4"/>')
            L.texto(x0 + 8, yy + 15, f"[{guarda}]", tam=12, color=GRIS, cursiva=True, dueno="frag")
        for h in fr["hijos"]:
            pintar(h)
    for fr in fragmentos:
        rango(fr, 0)
        pintar(fr)

    # --- cabeceras y lineas de vida
    y_cab = {}
    for i, p in enumerate(parts):
        if p[0] in creados:
            continue
        y_cab[p[0]] = cabecera(L, p, xs[i], TOP, w[i])
    for paso, num, yy in eventos:
        if paso[0] == "c":
            i = idx[paso[2]]
            cabecera(L, parts[i], xs[i], yy - H_CAB / 2, w[i])
            y_cab[paso[2]] = yy + H_CAB / 2
    for i, p in enumerate(parts):
        L.crudo(f'<line x1="{xs[i]}" y1="{y_cab[p[0]]}" x2="{xs[i]}" y2="{alto - 40}" '
                f'stroke="{GRIS_CLARO}" stroke-width="1.2" stroke-dasharray="5,5"/>')

    # --- mensajes
    for paso, num, yy in eventos:
        k = paso[0]
        if k in ("m", "r", "c"):
            a, b = idx[paso[1]], idx[paso[2]]
            xa, xb = xs[a], xs[b]
            if k == "c":
                xb = xb - w[b] / 2 if xb > xa else xb + w[b] / 2
            L.linea([(xa, yy), (xb, yy)], color=NEGRO, sw=1.3,
                    dash="6,4" if k in ("r", "c") else None,
                    fin="lleno" if k == "m" else "abierta", desc=f"mensaje {num or paso[3]}")
            texto = num + paso[3]
            cx = (xa + xb) / 2
            L.texto(cx, yy - 7, texto, tam=T, anchor="middle", color=NEGRO if k != "r" else GRIS,
                    cursiva=k == "r")
        elif k == "s":
            x = xs[idx[paso[1]]]
            L.linea([(x, yy - 14), (x + 40, yy - 14), (x + 40, yy + 6), (x + 2, yy + 6)],
                    color=NEGRO, sw=1.3, fin="lleno", desc=f"mensaje {num}")
            L.texto(x + 48, yy, num + paso[2], tam=T)
        elif k == "nota":
            x = xs[idx[paso[1]]] + 16
            lineas = partir(paso[2], 52)
            h = 10 + 15 * len(lineas)
            y0 = yy - h - 6
            ancho = max(ancho_texto(s, 11.5) for s in lineas) + 22
            L.crudo(f'<path d="M{x},{y0} L{x + ancho - 10},{y0} L{x + ancho},{y0 + 10} '
                    f'L{x + ancho},{y0 + h} L{x},{y0 + h} Z" fill="#FFFBEA" stroke="{GRIS_CLARO}" '
                    f'stroke-width="1.1"/>')
            for j, s in enumerate(lineas):
                L.texto(x + 10, y0 + 16 + 15 * j, s, tam=11.5, color="#5A4A1A")
    L.texto(32, alto - 16, "Flecha llena: mensaje (si es una llamada, es una operación del diagrama de "
            "clases). Punteada: respuesta o «create». Recuadros alt / opt / loop: alternativas, "
            "opcional y repetición, con su condición entre corchetes.", tam=11.5, color=GRIS_CLARO)
    return L


def todos():
    return [(s["archivo"], s["titulo"], dibujar(s)) for s in SECUENCIAS]
