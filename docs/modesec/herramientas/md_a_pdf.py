"""Convierte los entregables Markdown a PDF con el sistema de diseño del
proyecto.

POR QUE EXISTE
Los entregables se escriben en Markdown (versionable, diffeable, y es
donde viven los verificadores). La plataforma del curso pide PDF. Esta
herramienta hace la conversion sin intermediarios manuales: se corre y
los PDF quedan regenerados desde el Markdown vigente. Si el documento
cambia, el PDF se vuelve a generar -- no se edita el PDF.

COMO
Markdown -> HTML (conversor propio, sin dependencias externas: la
maquina no tiene pandoc ni weasyprint) -> PDF con Chrome headless, que
ya se usa en este proyecto para renderizar los diagramas.

TIPOGRAFIA
Inter, la misma que fija `03-tokens-diseno.md` para todo el sistema.
Colores tomados de `tokens.json`: #111111 tinta principal, #555555
secundario, #888888 atenuado, #E7E7E7 bordes, #F5F3EE superficie.

Uso:  python3 md_a_pdf.py
"""
import html
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..")
CHROME = "/usr/bin/google-chrome"


# ===================================================== Markdown -> HTML
def en_linea(t):
    """Formato dentro de una linea. El orden importa: el codigo primero,
    para que nada de adentro se reinterprete."""
    fragmentos = []

    def guardar(m):
        fragmentos.append(m.group(1))
        return f"\x00{len(fragmentos) - 1}\x00"

    t = re.sub(r"`([^`]+)`", guardar, t)
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    # <br> escrito a mano dentro de celdas de tabla
    t = t.replace("&lt;br&gt;", "<br>")
    for i, frag in enumerate(fragmentos):
        t = t.replace(f"\x00{i}\x00", f"<code>{html.escape(frag)}</code>")
    return t


def celdas(fila):
    """Parte una fila de tabla respetando los pipes escapados (\\|)."""
    fila = fila.strip().strip("|")
    partes, actual, i = [], "", 0
    while i < len(fila):
        if fila[i] == "\\" and i + 1 < len(fila) and fila[i + 1] == "|":
            actual += "|"
            i += 2
        elif fila[i] == "|":
            partes.append(actual)
            actual = ""
            i += 1
        else:
            actual += fila[i]
            i += 1
    partes.append(actual)
    return [p.strip() for p in partes]


def convertir(md):
    lineas = md.split("\n")
    out, i = [], 0
    clase_tabla = None
    while i < len(lineas):
        l = lineas[i]

        # bloque de codigo
        if l.startswith("```"):
            i += 1
            cuerpo = []
            while i < len(lineas) and not lineas[i].startswith("```"):
                cuerpo.append(html.escape(lineas[i]))
                i += 1
            i += 1
            out.append("<pre><code>" + "\n".join(cuerpo) + "</code></pre>")
            continue

        # marca de clase para la tabla siguiente: <!-- tabla:campos -->
        m = re.match(r"^\s*<!--\s*tabla:(\w+)\s*-->\s*$", l)
        if m:
            clase_tabla = m.group(1)
            i += 1
            continue

        # tabla
        if l.strip().startswith("|") and i + 1 < len(lineas) and \
                re.match(r"^\s*\|[\s:|-]+\|\s*$", lineas[i + 1]):
            cab = celdas(l)
            i += 2
            filas = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                filas.append(celdas(lineas[i]))
                i += 1
            cls = f' class="{clase_tabla}"' if clase_tabla else ""
            clase_tabla = None
            t = [f"<table{cls}><thead><tr>"]
            t += [f"<th>{en_linea(c)}</th>" for c in cab]
            t.append("</tr></thead><tbody>")
            for f in filas:
                t.append("<tr>" + "".join(
                    f"<td>{en_linea(c)}</td>" for c in f) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        # encabezados
        m = re.match(r"^(#{1,6})\s+(.*)$", l)
        if m:
            n = len(m.group(1))
            out.append(f"<h{n}>{en_linea(m.group(2))}</h{n}>")
            i += 1
            continue

        # regla horizontal
        if re.match(r"^\s*---+\s*$", l):
            out.append("<hr>")
            i += 1
            continue

        # cita
        if l.startswith(">"):
            cuerpo = []
            while i < len(lineas) and lineas[i].startswith(">"):
                cuerpo.append(lineas[i].lstrip(">").strip())
                i += 1
            out.append(f"<blockquote>{en_linea(' '.join(cuerpo))}</blockquote>")
            continue

        # listas
        if re.match(r"^\s*([-*]|\d+\.)\s+", l):
            ordenada = bool(re.match(r"^\s*\d+\.", l))
            items, nivel_base = [], len(l) - len(l.lstrip())
            while i < len(lineas) and (
                    re.match(r"^\s*([-*]|\d+\.)\s+", lineas[i]) or
                    (lineas[i].strip() and lineas[i].startswith("  ") and items)):
                if re.match(r"^\s*([-*]|\d+\.)\s+", lineas[i]):
                    sangria = len(lineas[i]) - len(lineas[i].lstrip())
                    txt = re.sub(r"^\s*([-*]|\d+\.)\s+", "", lineas[i])
                    items.append((sangria, txt))
                else:                       # continuacion del item anterior
                    items[-1] = (items[-1][0], items[-1][1] + " " + lineas[i].strip())
                i += 1
            tag = "ol" if ordenada else "ul"
            out.append(f"<{tag}>")
            anidado = False
            for sangria, txt in items:
                if sangria > nivel_base and not anidado:
                    out.append("<ul>")
                    anidado = True
                elif sangria <= nivel_base and anidado:
                    out.append("</ul>")
                    anidado = False
                out.append(f"<li>{en_linea(txt)}</li>")
            if anidado:
                out.append("</ul>")
            out.append(f"</{tag}>")
            continue

        # parrafo
        if l.strip():
            cuerpo = []
            while i < len(lineas) and lineas[i].strip() and \
                    not re.match(r"^(#{1,6}\s|```|\s*---+\s*$|>|\s*([-*]|\d+\.)\s)",
                                 lineas[i]) and \
                    not lineas[i].strip().startswith("|"):
                cuerpo.append(lineas[i].rstrip("\n"))
                i += 1
            # Salto de linea duro de Markdown: dos espacios al final.
            # Sin esto, varias lineas seguidas se funden en un parrafo --
            # correcto segun el estandar, pero indeseable en un bloque de
            # metadatos donde cada linea es un campo.
            unido = "<br>".join(x.rstrip() for x in cuerpo) if any(
                x.endswith("  ") for x in cuerpo[:-1]) else " ".join(
                x.strip() for x in cuerpo)
            out.append(f"<p>{en_linea(unido)}</p>")
            continue

        i += 1
    return "\n".join(out)


# ============================================================ plantilla
CSS = """
@page { size: %(tam)s; margin: 18mm 16mm 16mm 16mm; }
* { box-sizing: border-box; }
body { font-family: 'Inter', sans-serif; font-size: %(base)s;
       line-height: 1.6; color: #111111; margin: 0;
       -webkit-font-smoothing: antialiased; }

/* ---------------- portada ---------------- */
.portada { height: %(alto_portada)s; display: flex; flex-direction: column;
           justify-content: center; page-break-after: always; }
.portada .kicker { font-size: 9.5pt; font-weight: 700; color: #888888;
       text-transform: uppercase; letter-spacing: 0.12em;
       margin: 0 0 14px 0; }
.portada h1 { font-size: 30pt; font-weight: 700; line-height: 1.15;
       margin: 0 0 12px 0; letter-spacing: -0.02em; border: none;
       padding: 0; }
.portada .sub { font-size: 12.5pt; color: #555555; font-weight: 400;
       line-height: 1.5; margin: 0 0 40px 0; max-width: 135mm; }
.portada .meta { border-top: 2px solid #111111; padding-top: 18px;
       display: grid; grid-template-columns: 1fr 1fr; gap: 14px 32px;
       max-width: 135mm; }
.portada .meta div b { display: block; font-size: 8pt; color: #888888;
       text-transform: uppercase; letter-spacing: 0.08em;
       font-weight: 700; margin-bottom: 3px; }
.portada .meta div span { font-size: 10.5pt; color: #111111; }

/* ---------------- texto ---------------- */
h1 { font-size: 19pt; font-weight: 700; margin: 0 0 14px 0;
     letter-spacing: -0.01em; page-break-after: avoid; }
h2 { font-size: 14pt; font-weight: 700; margin: 26px 0 10px 0;
     padding-top: 10px; border-top: 1.5px solid #111111;
     page-break-after: avoid; }
h3 { font-size: 11.5pt; font-weight: 700; margin: 18px 0 7px 0;
     page-break-after: avoid; }
h4 { font-size: 10.5pt; font-weight: 700; color: #222222;
     margin: 14px 0 5px 0; page-break-after: avoid; }
p { margin: 0 0 9px 0; }
strong { font-weight: 700; }
em { font-style: italic; color: #333333; }
a { color: #111111; text-decoration: underline; }
hr { border: none; border-top: 1px solid #E7E7E7; margin: 20px 0; }
blockquote { margin: 12px 0; padding: 2px 0 2px 14px;
     border-left: 3px solid #E7E7E7; color: #555555; font-style: italic; }
ul, ol { margin: 0 0 10px 0; padding-left: 20px; }
li { margin-bottom: 4px; }
li > ul, li > ol { margin-top: 4px; }

code { font-family: 'DejaVu Sans Mono', monospace; font-size: 0.87em;
       background: #F5F3EE; padding: 1px 4px; border-radius: 3px;
       color: #111111; word-break: break-word; }
pre { background: #FAFAF8; border: 1px solid #E7E7E7; border-radius: 6px;
      padding: 11px 13px; margin: 0 0 12px 0; overflow: hidden;
      page-break-inside: avoid; }
pre code { background: none; padding: 0; font-size: 8.4pt;
       line-height: 1.5; white-space: pre-wrap; }

/* ---------------- tablas ---------------- */
table { border-collapse: collapse; width: 100%%; margin: 10px 0 16px 0;
        font-size: %(tabla)s; page-break-inside: auto; }
thead { display: table-header-group; }
tr { page-break-inside: avoid; }
th { text-align: left; font-weight: 700; font-size: 0.92em;
     color: #111111; border-bottom: 1.5px solid #111111;
     padding: 6px 8px 6px 0; vertical-align: bottom; }
td { padding: 6px 8px 6px 0; border-bottom: 1px solid #E7E7E7;
     vertical-align: top; line-height: 1.45; }
td code, th code { font-size: 0.88em; padding: 0 2px; }
table em { color: #555555; font-size: 0.94em; }

/* Un identificador partido a mitad de palabra (id_inscrip / cion) es
   ilegible. Estas dos clases dan a cada columna el ancho que necesita y
   prohiben el corte donde importa. */
table.campos td:first-child code { white-space: nowrap; }
table.campos td:nth-child(2) code { white-space: nowrap; }
table.campos th:nth-child(3), table.campos td:nth-child(3),
table.campos th:nth-child(4), table.campos td:nth-child(4),
table.campos th:nth-child(6), table.campos td:nth-child(6) {
     white-space: nowrap; }
table.fks td:nth-child(3) { white-space: nowrap; }
table.fks td:first-child code { word-break: normal; }
/* Un identificador corto en la primera columna (RNF-01, RF-12) no
   debe partirse en dos lineas. */
td:first-child > strong { white-space: nowrap; }
"""

PAGINA = """<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><title>%(titulo)s</title>
<style>%(css)s</style></head><body>
%(portada)s
%(cuerpo)s
</body></html>"""

PORTADA = """<section class="portada">
  <p class="kicker">%(kicker)s</p>
  <h1>%(titulo)s</h1>
  <p class="sub">%(sub)s</p>
  <div class="meta">
    <div><b>Proyecto</b><span>AdaptiveLearn</span></div>
    <div><b>Curso</b><span>DSE-2 · Diseño y Desarrollo de Software Educativo II</span></div>
    <div><b>Metodología</b><span>MODESEC · %(fase)s</span></div>
    <div><b>Fecha</b><span>%(fecha)s</span></div>
  </div>
</section>"""


def construir(md, titulo, sub, kicker, fase, fecha, apaisado=False):
    cuerpo = convertir(md)
    # el H1 del Markdown ya esta en la portada: se retira del cuerpo
    cuerpo = re.sub(r"^<h1>.*?</h1>\s*", "", cuerpo, count=1, flags=re.S)
    css = CSS % {
        "tam": "A4 landscape" if apaisado else "A4",
        "base": "9.5pt" if apaisado else "10pt",
        "tabla": "8pt" if apaisado else "8.6pt",
        # alto util = lado de la hoja menos los dos margenes verticales.
        # Con el valor de vertical (247mm) la portada desbordaba a una
        # segunda pagina en blanco al imprimir en apaisado.
        "alto_portada": "174mm" if apaisado else "247mm",
    }
    portada = PORTADA % {"kicker": kicker, "titulo": titulo, "sub": sub,
                         "fase": fase, "fecha": fecha}
    return PAGINA % {"titulo": titulo, "css": css, "portada": portada,
                     "cuerpo": cuerpo}


INTER = os.path.expanduser("~/.local/share/fonts/inter/Inter-Regular.otf")


def numerar(ruta, titulo):
    """Pone pie de pagina: titulo a la izquierda, 'n / total' a la derecha.

    Lo hace PyMuPDF y no Chrome a proposito: el pie que Chrome trae de
    fabrica incluye la ruta `file:///...` del archivo temporal, que no
    tiene nada que hacer en un entregable. Con `--no-pdf-header-footer`
    se quita esa linea, pero tambien el numero de pagina; asi que el
    numero se estampa aqui, con la tipografia y el gris del sistema.

    La portada se salta: una portada numerada se ve mal y ademas no
    cuenta como pagina de contenido.
    """
    import fitz
    doc = fitz.open(ruta)
    total = len(doc)
    gris = (0x88 / 255, 0x88 / 255, 0x88 / 255)     # #888888, token Muted
    usar_inter = os.path.exists(INTER)
    for n, pagina in enumerate(doc, start=1):
        if n == 1:
            continue
        ancho, alto = pagina.rect.width, pagina.rect.height
        y = alto - 28
        args = dict(fontsize=7.5, color=gris)
        if usar_inter:
            args.update(fontfile=INTER, fontname="Inter")
        pagina.insert_text((45, y), titulo, **args)
        etiqueta = f"{n - 1} / {total - 1}"
        ancho_txt = len(etiqueta) * 4.0
        pagina.insert_text((ancho - 45 - ancho_txt, y), etiqueta, **args)
    doc.saveIncr() if doc.can_save_incrementally() else doc.save(
        ruta, incremental=False, deflate=True)
    doc.close()


def a_pdf(html_txt, destino, titulo):
    tmp = destino.replace(".pdf", ".__tmp__.html")
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(html_txt)
    r = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
         "--no-pdf-header-footer", "--virtual-time-budget=12000",
         f"--print-to-pdf={destino}", f"file://{os.path.abspath(tmp)}"],
        capture_output=True, text=True, timeout=180)
    os.remove(tmp)
    if not os.path.exists(destino):
        raise RuntimeError(f"Chrome no genero el PDF:\n{r.stderr[-700:]}")
    numerar(destino, titulo)
    return os.path.getsize(destino)


# ======================================================= PDF de diagramas
CSS_DIAGRAMAS = """
@page { size: A4 landscape; margin: 14mm; }
* { box-sizing: border-box; }
body { font-family: 'Inter', sans-serif; color: #111111; margin: 0;
       font-size: 9.5pt; line-height: 1.55; }
.figura { height: 182mm; display: flex; flex-direction: column;
          page-break-after: always; }
.figura:last-child { page-break-after: auto; }
.figura .rotulo { font-size: 8pt; font-weight: 700; color: #888888;
       text-transform: uppercase; letter-spacing: 0.1em;
       margin: 0 0 6px 0; }
.lienzo { flex: 1; display: flex; align-items: center;
          justify-content: center; min-height: 0; }
.lienzo svg { max-width: 100%; max-height: 100%; height: auto;
              width: auto; }
.pie { font-size: 8.5pt; color: #333333; line-height: 1.5;
       border-top: 1px solid #E7E7E7; padding-top: 8px; margin-top: 8px; }
.pie b { color: #111111; }
.pie code { font-family: 'DejaVu Sans Mono', monospace; font-size: 0.87em;
       background: #F5F3EE; padding: 1px 3px; border-radius: 3px; }
"""


def pdf_diagramas(origen, destino, fecha, solo_mapa=False):
    """Arma el PDF de los diagramas Chen: una figura por pagina.

    Toma los SVG ya generados y verificados por `diagrama/`, no los
    vuelve a dibujar -- reusarlos es lo que garantiza que el PDF muestre
    exactamente lo que `_verificar_mapa.py` comprobo.
    """
    crudo = open(origen, encoding="utf-8").read()
    bloques = re.findall(
        r'<div class="bloque">(.*?)<p class="caption">(.*?)</p>\s*</div>',
        crudo, re.S)
    if not bloques:
        raise RuntimeError("no se encontraron figuras en " + origen)

    titulos = ["Leyenda de notación", "Mapa completo",
               "Vista 1 · Currículo oficial", "Vista 2 · Autoría de la experiencia",
               "Vista 3 · Banco de diagnóstico", "Vista 4 · Inscripción y entrega",
               "Vista 5 · Captura de la respuesta", "Vista 6 · Conclusión y reporte"]

    # El mapa completo mide 4200x3196: reducido a una hoja A4 sus rotulos
    # quedan ilegibles. Va en su propio PDF de formato grande (`solo_mapa`),
    # y se saca de aqui para no entregar una figura que no se puede leer.
    if solo_mapa:
        bloques = [bloques[1]]
        titulos = ["Mapa completo"]
    else:
        bloques = [b for i, b in enumerate(bloques) if i != 1]
        titulos = [x for i, x in enumerate(titulos) if i != 1]

    if solo_mapa:
        hoja, alto_fig, titulo_doc = "594mm 420mm", "372mm", "Mapa completo del MER"
        partes = []          # una sola lamina: sin portada, se imprime y se cuelga
    else:
        hoja, alto_fig, titulo_doc = "A4 landscape", "182mm", "Diagramas del MER"
        partes = [PORTADA % {
            "kicker": "Diseño Computacional · Anexo gráfico",
            "titulo": "Diagramas del MER",
            "sub": "Notación Chen. Leyenda y las seis vistas por ciclo de vida del "
                   "sistema. El mapa completo va aparte, en formato grande, porque "
                   "reducido a una hoja A4 sus rótulos no se leen.",
            "fase": "Fase III", "fecha": fecha}]

    for i, (svg, pie) in enumerate(bloques):
        rotulo = titulos[i] if i < len(titulos) else f"Figura {i + 1}"
        partes.append(
            f'<section class="figura"><p class="rotulo">{rotulo}</p>'
            f'<div class="lienzo">{svg.strip()}</div>'
            f'<div class="pie">{pie.strip()}</div></section>')

    css = (CSS % {"tam": hoja, "base": "9.5pt", "tabla": "8pt",
                  "alto_portada": alto_fig} + CSS_DIAGRAMAS
           + f"\n@page {{ size: {hoja}; }}\n.figura {{ height: {alto_fig}; }}\n")
    doc = PAGINA % {"titulo": titulo_doc, "css": css,
                    "portada": "", "cuerpo": "\n".join(partes)}
    return a_pdf(doc, destino, titulo_doc)


# =============================================================== catalogo
F3 = os.path.join(RAIZ, "fase-3-diseno-computacional")
SALIDA = os.path.join(F3, "entrega-pdf")

DOCUMENTOS = [
    dict(md=os.path.join(F3, "00-ENTREGA.md"),
         pdf="0-Entrega-Fase-III-indice.pdf",
         titulo="Entrega — Fase III",
         sub="Índice de la entrega, trazabilidad de los doce hallazgos de la "
             "revisión docente, y los vacíos que el modelo declara sin resolver.",
         kicker="Diseño Computacional", fase="Fase III"),
    dict(md=os.path.join(F3, "01-modelo-entidad-relacion.md"),
         pdf="1-Modelo-Entidad-Relacion.pdf",
         titulo="Modelo Entidad-Relación",
         sub="Quinta revisión. Catorce entidades y dieciocho relaciones, en "
             "notación Chen, con la trazabilidad de cada atributo a su fuente.",
         kicker="Diseño Computacional · Entregable 1", fase="Fase III"),
    dict(md=os.path.join(F3, "04-modelo-relacional.md"),
         pdf="2-Modelo-Relacional.pdf",
         titulo="Modelo Relacional",
         sub="Catorce tablas derivadas del MER por el algoritmo formal de mapeo: "
             "llaves, acciones referenciales, normalización y mecanismo de cada "
             "restricción de integridad.",
         kicker="Diseño Computacional · Entregable 2", fase="Fase III"),
    dict(md=os.path.join(F3, "06-diccionario-datos.md"),
         pdf="3-Diccionario-de-Datos.pdf",
         titulo="Diccionario de Datos",
         sub="Setenta y dos columnas con su tipo, tamaño, dominio, valor por "
             "defecto y la fuente de la que sale cada una. Motor objetivo: "
             "MariaDB 10.11.",
         kicker="Diseño Computacional · Entregable 3", fase="Fase III",
         apaisado=True),
    dict(md=os.path.join(F3, "05-triaje-revision-docente.md"),
         pdf="4-Triaje-de-la-revision-docente.pdf",
         titulo="Triaje de la revisión docente",
         sub="Los doce hallazgos del 1 de septiembre, clasificados en los que se "
             "aceptan, los que se disuelven y los que quedaron obsoletos — cada "
             "uno con su razón escrita.",
         kicker="Diseño Computacional · Anexo", fase="Fase III"),
]

FECHA = "19 de septiembre de 2026"

if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    fallas = []
    print("=" * 64)
    for d in DOCUMENTOS:
        nombre = os.path.basename(d["md"])
        if not os.path.exists(d["md"]):
            fallas.append(f"no existe: {nombre}")
            print(f"  FALTA   {nombre}")
            continue
        md = open(d["md"], encoding="utf-8").read()
        doc = construir(md, d["titulo"], d["sub"], d["kicker"], d["fase"],
                        FECHA, d.get("apaisado", False))
        destino = os.path.join(SALIDA, d["pdf"])
        try:
            kb = a_pdf(doc, destino, d["titulo"]) // 1024
            orient = "apaisado" if d.get("apaisado") else "vertical"
            print(f"  OK      {d['pdf']}  ({kb} KB, {orient})")
        except Exception as e:
            fallas.append(f"{d['pdf']}: {e}")
            print(f"  ERROR   {d['pdf']}: {e}")
    print("=" * 64)
    if fallas:
        print(f"{len(fallas)} problema(s)")
        sys.exit(1)
    print(f"{len(DOCUMENTOS)} PDF generados en fase-3-diseno-computacional/entrega-pdf/")
