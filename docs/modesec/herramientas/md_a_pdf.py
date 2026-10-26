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

DIAGRAMAS
Una imagen sola en su linea -- ![pie](ruta.svg) -- va en su propia hoja A4
apaisada: los diagramas son mas anchos que altos, y al ancho de una hoja
vertical sus rotulos no se leen. El SVG entra como vector, asi que se
amplia sin perder nitidez. Las laminas que ni asi se leen (el MER entero)
van ademas en un PDF aparte de formato A1.

Uso:  python3 md_a_pdf.py      (en Windows: python md_a_pdf.py)
"""
import html
import os
import pathlib
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..")
# Chrome en Linux, como se escribio; en Windows sirven Chrome o Edge, que
# imprimen igual (los dos son Chromium). Se usa el primero que exista.
NAVEGADORES = ["/usr/bin/google-chrome",
               r"C:\Program Files\Google\Chrome\Application\chrome.exe",
               r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]
CHROME = next((n for n in NAVEGADORES if os.path.exists(n)), NAVEGADORES[0])


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
    # Un identificador largo (ServicioExperiencias.codigoInvitacion,
    # /auth/recuperar-contrasena/verificar) que no cabe se corta despues de
    # un punto o una barra, no a mitad de palabra.
    for i, frag in enumerate(fragmentos):
        cod = html.escape(frag).replace(".", ".<wbr>").replace("/", "/<wbr>")
        t = t.replace(f"\x00{i}\x00", f"<code>{cod}</code>")
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


def convertir(md, base="."):
    """`base`: la carpeta del .md, de la que cuelgan las rutas de sus imagenes."""
    lineas = md.split("\n")
    out, i = [], 0
    clase_tabla = None
    while i < len(lineas):
        l = lineas[i]

        # diagrama: ![pie](ruta), solo en su linea. Va en su hoja apaisada
        # (pagina con nombre `lamina`). Si el archivo no existe, se detiene:
        # un PDF al que le falta una figura no se entrega.
        m = re.match(r"^\s*!\[([^\]]*)\]\(([^)\s]+)\)\s*$", l)
        if m:
            ruta = os.path.join(base, m.group(2))
            if not os.path.exists(ruta):
                raise FileNotFoundError(f"la imagen no existe: {m.group(2)}")
            src = pathlib.Path(ruta).resolve().as_uri()
            # un titulo que va justo antes del diagrama se lleva a su hoja:
            # si no, queda solo en una hoja vertical entre dos apaisadas
            titulo = out.pop() if out and re.match(r"^<h[2-6]>", out[-1]) else ""
            out.append(f'<figure class="lamina">{titulo}<figcaption>{en_linea(m.group(1))}'
                       f'</figcaption><img src="{src}" alt="{html.escape(m.group(1))}"></figure>')
            i += 1
            continue

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
                    not re.match(r"^(#{1,6}\s|```|\s*---+\s*$|>|\s*([-*]|\d+\.)\s|\s*!\[)",
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
body { font-family: 'Inter', 'Segoe UI', sans-serif; font-size: %(base)s;
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

code { font-family: 'DejaVu Sans Mono', Consolas, monospace; font-size: 0.87em;
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
/* catalogo de endpoints: los casos de uso, uno por linea y enteros */
table.endpoints td:nth-child(3) { white-space: nowrap; }
table.endpoints code { word-break: normal; }
table.fks td:first-child code { word-break: normal; }
/* Un identificador corto en la primera columna (RNF-01, RF-12) no
   debe partirse en dos lineas. */
td:first-child > strong { white-space: nowrap; }

/* ---------------- diagramas: una hoja apaisada cada uno ---------------- */
@page lamina { size: A4 landscape; margin: 12mm 14mm 16mm 14mm; }
figure.lamina { page: lamina; height: 178mm; margin: 0; display: flex;
       flex-direction: column; break-before: page; break-after: page; }
figure.lamina > h2, figure.lamina > h3, figure.lamina > h4 { margin: 0 0 6px 0; }
figure.lamina figcaption { font-size: 8pt; font-weight: 700; color: #888888;
       text-transform: uppercase; letter-spacing: 0.1em; margin: 0 0 6px 0; }
figure.lamina img { flex: 1; min-height: 0; width: 100%%; object-fit: contain; }
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


def construir(md, titulo, sub, kicker, fase, fecha, apaisado=False, base="."):
    cuerpo = convertir(md, base)
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


def numerar(ruta, titulo, con_portada=True):
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
    salto = 1 if con_portada else 0
    for n, pagina in enumerate(doc, start=1):
        if n <= salto:
            continue
        ancho, alto = pagina.rect.width, pagina.rect.height
        y = alto - 28
        args = dict(fontsize=7.5, color=gris)
        if usar_inter:
            args.update(fontfile=INTER, fontname="Inter")
        pagina.insert_text((45, y), titulo, **args)
        etiqueta = f"{n - salto} / {total - salto}"
        ancho_txt = len(etiqueta) * 4.0
        pagina.insert_text((ancho - 45 - ancho_txt, y), etiqueta, **args)
    doc.saveIncr() if doc.can_save_incrementally() else doc.save(
        ruta, incremental=False, deflate=True)
    doc.close()


def a_pdf(html_txt, destino, titulo, con_portada=True):
    tmp = destino.replace(".pdf", ".__tmp__.html")
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(html_txt)
    r = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
         "--no-pdf-header-footer", "--virtual-time-budget=12000",
         # as_uri() arma file:///C:/... en Windows y file:///home/... en Linux
         f"--print-to-pdf={destino}", pathlib.Path(tmp).resolve().as_uri()],
        capture_output=True, text=True, timeout=180)
    os.remove(tmp)
    if not os.path.exists(destino):
        raise RuntimeError(f"Chrome no genero el PDF:\n{r.stderr[-700:]}")
    numerar(destino, titulo, con_portada)
    return os.path.getsize(destino)


# ======================================================== laminas grandes
CSS_LAMINAS = """
@page { size: %(hoja)s; margin: 14mm; }
* { box-sizing: border-box; }
body { font-family: 'Inter', 'Segoe UI', sans-serif; color: #111111; margin: 0; }
.figura { height: %(alto)s; display: flex; flex-direction: column;
          page-break-after: always; }
.figura:last-child { page-break-after: auto; }
.figura .rotulo { font-size: 11pt; font-weight: 700; color: #888888;
       text-transform: uppercase; letter-spacing: 0.1em; margin: 0 0 8px 0; }
.figura img { flex: 1; min-height: 0; width: 100%%; object-fit: contain; }
"""


def pdf_laminas(laminas, destino, titulo_doc, hoja="841mm 594mm", alto="560mm"):
    """Las laminas que en A4 no se leen, una por hoja de formato grande (A1
    apaisado por defecto) y sin portada: se imprimen en plotter o se ven con
    zoom. Toma los SVG ya generados y verificados, no los vuelve a dibujar --
    reusarlos es lo que garantiza que el PDF muestre lo que se comprobo.

    Reemplaza a `pdf_diagramas`, que leia las figuras de un HTML de vistas
    con la estructura de la quinta revision del MER, que ya no existe.
    """
    partes = []
    for ruta, rotulo in laminas:
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"la lamina no existe: {ruta}")
        src = pathlib.Path(ruta).resolve().as_uri()
        partes.append(f'<section class="figura"><p class="rotulo">{html.escape(rotulo)}</p>'
                      f'<img src="{src}" alt="{html.escape(rotulo)}"></section>')
    css = CSS_LAMINAS % {"hoja": hoja, "alto": alto}
    doc = PAGINA % {"titulo": titulo_doc, "css": css, "portada": "",
                    "cuerpo": "\n".join(partes)}
    return a_pdf(doc, destino, titulo_doc, con_portada=False)


# =============================================================== catalogo
F3 = os.path.join(RAIZ, "fase-3-diseno-computacional")
SALIDA = os.path.join(F3, "entrega-pdf")
KICKER = "Diseño Computacional"

DOCUMENTOS = [
    dict(md="19-entrega-fase-3.md", pdf="00-Entrega-Fase-III-indice.pdf",
         titulo="Entrega — Fase III",
         sub="Índice de la fase: qué pide MODESEC, en qué documento está, cómo se comprueba "
             "y qué queda abierto, declarado.",
         kicker=KICKER + " · Índice"),
    dict(md="10-proceso-desarrollo.md", pdf="10-Proceso-de-desarrollo.pdf",
         titulo="Descripción del proceso de desarrollo",
         sub="Ciclo de vida incremental en cuatro incrementos, y la descripción funcional del "
             "sistema: actores, subsistemas, lo que no hace y lo que condiciona el diseño.",
         kicker=KICKER + " · Sub-etapa 1"),
    dict(md="11-analisis-requerimientos.md", pdf="11-Analisis-de-requerimientos.pdf",
         titulo="Análisis de requerimientos",
         sub="Cincuenta y ocho requerimientos —44 funcionales y 14 no funcionales—, por "
             "subsistema, con su fuente y la trazabilidad de cada ventana de la Fase II.",
         kicker=KICKER + " · Sub-etapa 2"),
    dict(md="12-casos-de-uso.md", pdf="12-Casos-de-uso.pdf",
         titulo="Diagrama de casos de uso",
         sub="Treinta y un casos de uso en siete diagramas, cada uno con su flujo, sus "
             "alternos y su prueba de aceptación. Cubren los 44 requerimientos funcionales.",
         kicker=KICKER + " · Sub-etapa 3"),
    dict(md="13-diagrama-clases.md", pdf="13-Diagrama-de-clases.pdf",
         titulo="Diagrama de clases",
         sub="Las clases del dominio, con los atributos del modelo relacional, y las de "
             "servicio, con cada método trazado al caso de uso del que sale.",
         kicker=KICKER + " · Sub-etapa 4"),
    dict(md="14-diagrama-objetos.md", pdf="14-Diagrama-de-objetos.pdf",
         titulo="Diagrama de objetos",
         sub="Una fotografía del sistema en un momento dado, que se carga en el esquema real "
             "sin violar ninguna restricción.",
         kicker=KICKER + " · Sub-etapa 5"),
    dict(md="15-diagramas-secuencia.md", pdf="15-Diagramas-de-secuencia.pdf",
         titulo="Diagramas de secuencia",
         sub="Los ocho flujos con más decisiones, del actor a la interfaz, a los servicios y "
             "a las clases del dominio.",
         kicker=KICKER + " · Sub-etapa 6"),
    dict(md="16-modelo-entidad-relacion.md", pdf="16-Modelo-Entidad-Relacion.pdf",
         titulo="Modelo Entidad-Relación",
         sub="Notación Chen estricta: entidades, relaciones con su (mín, máx), los ciclos del "
             "modelo y qué regla cierra cada uno, la matriz CRUD y la respuesta a cada "
             "hallazgo de la revisión docente. La lámina completa va aparte, en A1.",
         kicker=KICKER + " · Sub-etapa 7 · Base de datos"),
    dict(md="17-modelo-relacional.md", pdf="17-Modelo-Relacional.pdf",
         titulo="Modelo Relacional",
         sub="Las tablas derivadas del MER: llaves, acciones referenciales, normalización y "
             "el mecanismo de cada restricción de integridad, probado contra MySQL 8.4.",
         kicker=KICKER + " · Sub-etapa 7 · Base de datos"),
    dict(md="18-diccionario-datos.md", pdf="18-Diccionario-de-Datos.pdf",
         titulo="Diccionario de Datos",
         sub="Cada columna con su tipo, nulidad, llave, dominio, valor por defecto y la fuente "
             "de la que sale. Motor objetivo: MySQL 8.",
         kicker=KICKER + " · Sub-etapa 7 · Base de datos", apaisado=True),
    dict(md="20-catalogo-endpoints.md", pdf="20-Catalogo-de-endpoints.pdf",
         titulo="Catálogo de endpoints",
         sub="El puente hacia la construcción: cada endpoint por incremento, con su caso de "
             "uso, la operación que lo resuelve, las entidades que toca y quién puede llamarlo.",
         kicker=KICKER + " · Anexo"),
]

# El MER entero: en A4 sus rotulos no se leen.
LAMINAS = dict(pdf="16-MER-laminas-A1.pdf", titulo="Modelo Entidad-Relación · láminas",
               figuras=[("mer/mer-cajas.svg", "Vista de conjunto del MER"),
                        ("mer/mapa-chen.svg", "Mapa completo del MER, notación Chen")])

FECHA = "22 de octubre de 2026"

if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    fallas = []
    print(f"Navegador: {CHROME}")
    print("=" * 64)
    for d in DOCUMENTOS:
        origen = os.path.join(F3, d["md"])
        if not os.path.exists(origen):
            fallas.append(f"no existe: {d['md']}")
            print(f"  FALTA   {d['md']}")
            continue
        destino = os.path.join(SALIDA, d["pdf"])
        try:
            md = open(origen, encoding="utf-8").read()
            doc = construir(md, d["titulo"], d["sub"], d["kicker"], "Fase III",
                            FECHA, d.get("apaisado", False), base=F3)
            kb = a_pdf(doc, destino, d["titulo"]) // 1024
            orient = "apaisado" if d.get("apaisado") else "vertical"
            print(f"  OK      {d['pdf']}  ({kb} KB, {orient})")
        except Exception as e:
            fallas.append(f"{d['pdf']}: {e}")
            print(f"  ERROR   {d['pdf']}: {e}")
    try:
        kb = pdf_laminas([(os.path.join(F3, r), t) for r, t in LAMINAS["figuras"]],
                         os.path.join(SALIDA, LAMINAS["pdf"]), LAMINAS["titulo"]) // 1024
        print(f"  OK      {LAMINAS['pdf']}  ({kb} KB, A1 apaisado)")
    except Exception as e:
        fallas.append(f"{LAMINAS['pdf']}: {e}")
        print(f"  ERROR   {LAMINAS['pdf']}: {e}")
    print("=" * 64)
    if fallas:
        print(f"{len(fallas)} problema(s)")
        sys.exit(1)
    print(f"{len(DOCUMENTOS) + 1} PDF generados en fase-3-diseno-computacional/entrega-pdf/")
