"""Primitivas para escribir dentro de las plantillas .docx del curso
sin reconstruirlas: se conserva todo el XML original y solo se agregan
parrafos/tablas debajo de cada etiqueta de las cajas de respuesta."""
import copy
import re
import zipfile
from lxml import etree

WNS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = "{%s}" % WNS
AZUL = "1F3864"


def el(tag, **attrs):
    e = etree.Element(W + tag)
    for k, v in attrs.items():
        e.set(W + k, str(v))
    return e


def sub(parent, tag, **attrs):
    e = el(tag, **attrs)
    parent.append(e)
    return e


# ------------------------------------------------------------------ runs
def run(texto, b=False, i=False, color="000000", sz=20, mono=False, resaltar=False):
    r = el("r")
    rpr = sub(r, "rPr")
    f = "Consolas" if mono else "Calibri"
    sub(rpr, "rFonts", ascii=f, hAnsi=f, cs=f, eastAsia=f)
    if b:
        sub(rpr, "b"); sub(rpr, "bCs")
    if i:
        sub(rpr, "i"); sub(rpr, "iCs")
    sub(rpr, "color", val=color)
    if resaltar:
        sub(rpr, "highlight", val="yellow")
    sub(rpr, "sz", val=sz); sub(rpr, "szCs", val=sz)
    t = sub(r, "t")
    t.text = texto
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    return r


def runs_inline(texto, sz=20, color="000000", base_i=False, resaltar=False):
    """**negrita**, *cursiva* y `codigo` dentro de una linea."""
    out = []
    for trozo in re.split(r"(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)", texto):
        if not trozo:
            continue
        if trozo.startswith("**"):
            out.append(run(trozo[2:-2], b=True, i=base_i, sz=sz, color=color, resaltar=resaltar))
        elif trozo.startswith("`"):
            out.append(run(trozo[1:-1], mono=True, sz=sz - 2, color=color, resaltar=resaltar))
        elif trozo.startswith("*"):
            out.append(run(trozo[1:-1], i=True, sz=sz, color=color, resaltar=resaltar))
        else:
            out.append(run(trozo, i=base_i, sz=sz, color=color, resaltar=resaltar))
    return out


def par(texto="", after=80, ind=0, hanging=0, sz=20, color="000000", i=False,
        resaltar=False, keep=False, jc=None):
    p = el("p")
    ppr = sub(p, "pPr")
    if keep:
        sub(ppr, "keepNext")
    sub(ppr, "spacing", before=0, after=after, line=264, lineRule="auto")
    if ind or hanging:
        sub(ppr, "ind", left=ind, hanging=hanging)
    if jc:
        sub(ppr, "jc", val=jc)
    for r in runs_inline(texto, sz=sz, color=color, base_i=i, resaltar=resaltar):
        p.append(r)
    return p


# ---------------------------------------------------------------- tablas
def tabla(cabecera, filas, ancho_total, pesos=None, sz=17):
    n = len(cabecera)
    pesos = pesos or [1] * n
    anchos = [int(ancho_total * p / sum(pesos)) for p in pesos]
    t = el("tbl")
    tpr = sub(t, "tblPr")
    sub(tpr, "tblW", w=sum(anchos), type="dxa")
    b = sub(tpr, "tblBorders")
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        sub(b, lado, val="single", sz=4, space=0, color="BFBFBF")
    sub(tpr, "tblLayout", type="fixed")
    m = sub(tpr, "tblCellMar")
    sub(m, "top", w=40, type="dxa"); sub(m, "left", w=70, type="dxa")
    sub(m, "bottom", w=40, type="dxa"); sub(m, "right", w=70, type="dxa")
    g = sub(t, "tblGrid")
    for a in anchos:
        sub(g, "gridCol", w=a)

    def fila(celdas, es_cab):
        tr = sub(t, "tr")
        trpr = sub(tr, "trPr")
        sub(trpr, "cantSplit")
        if es_cab:
            sub(trpr, "tblHeader")
        for a, c in zip(anchos, celdas):
            tc = sub(tr, "tc")
            tcpr = sub(tc, "tcPr")
            sub(tcpr, "tcW", w=a, type="dxa")
            if es_cab:
                sub(tcpr, "shd", val="clear", color="auto", fill="DCE3EE")
            lineas = c if isinstance(c, list) else [c]
            for ln in lineas:
                p = par(ln, after=20, sz=sz, color=AZUL if es_cab else "000000")
                if es_cab:
                    for r in p.findall(W + "r"):
                        rpr = r.find(W + "rPr")
                        rpr.insert(1, el("b"))
                tc.append(p)
    fila(cabecera, True)
    for f in filas:
        fila(f, False)
    return t


# ------------------------------------------------------------- bloques
def bloques(items, ancho):
    """Traduce una lista de items de contenido a elementos XML."""
    out = []
    for it in items:
        if isinstance(it, str):
            out.append(par(it))
        elif it[0] == "h":
            out.append(par("**" + it[1] + "**", after=40, color=AZUL, keep=True))
        elif it[0] == "ul":
            for x in it[1]:
                out.append(par("–\t" + x, after=40, ind=360, hanging=220))
        elif it[0] == "pend":
            out.append(par("Pendiente: " + it[1], resaltar=True, i=True))
        elif it[0] == "cita":
            out.append(par(it[1], i=True, ind=360, color="404040"))
        elif it[0] == "tbl":
            _, cab, filas, pesos = it
            out.append(tabla(cab, filas, ancho, pesos))
            out.append(par("", after=40))
        else:
            raise ValueError(it)
    return out


def _texto(p):
    return "".join(p.itertext()).strip()


def oscurecer_etiqueta(p):
    """Las etiquetas vienen en gris cursiva (texto de ayuda). La plantilla
    pide borrar el gris y conservar los titulos: quedan como subtitulo
    oscuro en negrita."""
    for r in p.findall(W + "r"):
        rpr = r.find(W + "rPr")
        if rpr is None:
            continue
        for tag in ("i", "iCs", "color", "b", "bCs"):
            for x in rpr.findall(W + tag):
                rpr.remove(x)
        rpr.insert(1, el("b"))
        rpr.insert(2, el("color", val=AZUL))


def ancho_celda(tc, defecto=9000):
    w = tc.find(W + "tcPr/" + W + "tcW")
    if w is not None and w.get(W + "type") == "dxa":
        return int(float(w.get(W + "w"))) - 300
    tbl = tc.getparent().getparent()
    cols = tbl.findall(W + "tblGrid/" + W + "gridCol")
    if cols:
        return int(sum(float(c.get(W + "w")) for c in cols)) - 300
    return defecto


def rellenar_caja(tbl, secciones, limpiar_vacios=True):
    """secciones: lista de (prefijo_de_etiqueta, items). Debajo de cada
    etiqueta encontrada se insertan los items."""
    tc = tbl.find(".//" + W + "tc")
    ancho = ancho_celda(tc)
    ps = tc.findall(W + "p")
    usados = set()
    for prefijo, items in secciones:
        objetivo = None
        for p in ps:
            if id(p) not in usados and _texto(p).startswith(prefijo):
                objetivo = p
                break
        if objetivo is None:
            raise KeyError("etiqueta no encontrada: %r" % prefijo)
        usados.add(id(objetivo))
        oscurecer_etiqueta(objetivo)
        ancla = objetivo
        for e in bloques(items, ancho):
            ancla.addnext(e)
            ancla = e
    if limpiar_vacios:
        for p in tc.findall(W + "p"):
            if not _texto(p) and p.find(".//" + W + "t") is None and p.getnext() is not None:
                tc.remove(p)
    # una celda debe terminar en parrafo
    if tc[-1].tag != W + "p":
        tc.append(par("", after=0))


def reemplazar_caja(tbl, items):
    """Para cajas sin etiquetas utiles ('[Escriba aqui]')."""
    tc = tbl.find(".//" + W + "tc")
    ancho = ancho_celda(tc)
    for p in tc.findall(W + "p"):
        tc.remove(p)
    for e in bloques(items, ancho):
        tc.append(e)
    if tc[-1].tag != W + "p":
        tc.append(par("", after=0))


def _poner_en_celda(tc, contenido, sz=18):
    ancho = ancho_celda(tc, 4000)
    for p in tc.findall(W + "p"):
        tc.remove(p)
    items = contenido if isinstance(contenido, list) else [contenido]
    for it in items:
        if isinstance(it, tuple) and it[0] == "pend":
            tc.append(par(it[1], after=20, sz=sz, resaltar=True, i=True))
        elif isinstance(it, str):
            tc.append(par(it, after=20, sz=sz))
        else:
            for e in bloques([it], ancho):
                tc.append(e)
    if tc[-1].tag != W + "p":
        tc.append(par("", after=0))


def rellenar_clave_valor(tbl, valores):
    """Tablas de 2 columnas cuya 1a columna es la etiqueta."""
    faltan = dict(valores)
    for tr in tbl.findall(W + "tr"):
        tcs = tr.findall(W + "tc")
        if len(tcs) < 2:
            continue
        clave = _texto(tcs[0])
        for k in list(faltan):
            if clave.startswith(k):
                _poner_en_celda(tcs[1], faltan.pop(k))
                break
    if faltan:
        raise KeyError("filas no encontradas: %s" % list(faltan))


def rellenar_grilla(tbl, filas, sz=17):
    """Cabecera + filas vacias. Clona la ultima si faltan; borra sobrantes."""
    trs = tbl.findall(W + "tr")
    cab, datos = trs[0], trs[1:]
    molde = datos[-1] if datos else cab
    while len(datos) < len(filas):
        nuevo = copy.deepcopy(molde)
        datos[-1].addnext(nuevo)
        datos.append(nuevo)
    for tr, valores in zip(datos, filas):
        for tc, v in zip(tr.findall(W + "tc"), valores):
            _poner_en_celda(tc, v, sz=sz)
    for tr in datos[len(filas):]:
        tbl.remove(tr)


def agregar_tras_etiqueta(raiz, prefijo, items):
    """Busca un parrafo por texto en cualquier parte de `raiz`."""
    for p in raiz.iter(W + "p"):
        if _texto(p).startswith(prefijo):
            oscurecer_etiqueta(p)
            tc = p.getparent()
            ancho = ancho_celda(tc) if tc.tag == W + "tc" else 9000
            ancla = p
            for e in bloques(items, ancho):
                ancla.addnext(e)
                ancla = e
            return
    raise KeyError(prefijo)


# ------------------------------------------------------------- archivo
def abrir(ruta):
    z = zipfile.ZipFile(ruta)
    arbol = etree.fromstring(z.read("word/document.xml"))
    return z, arbol


def guardar(z, arbol, destino):
    datos = etree.tostring(arbol, xml_declaration=True, encoding="UTF-8",
                           standalone=True)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as out:
        for item in z.infolist():
            if item.filename == "word/document.xml":
                out.writestr(item, datos)
            else:
                out.writestr(item, z.read(item.filename))
