"""Arma el catálogo de DBA leyendo los cuatro PDF oficiales del MEN.

Encargo 02 (`docs/encargos/02-catalogo-curricular-corregido.md`). La
verdad es el PDF (ADR-033); el JSON heredado de la V2
(`../normalized/curriculo_men_normalizado.json`) solo se usa para decir,
por cada DBA, qué identificador tenía y qué cambió. No se modifica.

Cómo lee cada página:
  * Las palabras se arman siguiendo el ORDEN en que el PDF guarda los
    caracteres y con los espacios que el PDF trae (no adivinándolos por la
    distancia entre letras, que daba "instrume n tos"). Donde el PDF separa
    solo por posición, un hueco del ancho de un espacio también separa.
    Las líneas guardadas al revés se enderezan.
  * El GRADO sale del encabezado de la página ("Matemáticas • Grado 3º"),
    no de la posición del DBA en el documento.
  * La página tiene dos columnas. Se leen de arriba abajo, primero la
    izquierda y después la derecha, y las páginas en orden: un DBA puede
    empezar abajo en la izquierda y seguir arriba en la derecha.
  * Cada parte se reconoce por su tamaño de letra y su posición, que son
    los mismos en los cuatro documentos: el número del DBA (AvantGarde,
    ~26 pt), el enunciado (11 pt, justo debajo del número), los títulos
    "Evidencias de aprendizaje" y "Ejemplo" (11 pt), cada evidencia empieza
    con una viñeta (Wingdings, 10 pt) y sigue en 10 pt. No se usa la
    variante (Medium o Book): en algunas páginas de Ciencias Sociales el PDF
    marca todo como Book, aunque el enunciado se vea en negrita.
  * Una página sin encabezado de grado pero con DBA (solo la 86 de
    Matemáticas) toma el grado de la página anterior, y sus DBA quedan
    marcados como dudosos.
  * El EJEMPLO (encargo 05, QA-011) es lo que sigue al título "Ejemplo"
    hasta el número del DBA siguiente, aunque siga en la otra columna o la
    otra página. Se copia su texto corrido: letra de 10 u 11 pt que empieza
    en el margen de la columna (o en el de las viñetas). Lo demás no se
    copia, porque es parte de una figura o la acompaña: las tablas, las
    fórmulas en renglón aparte y los rótulos de un dibujo (fuera del margen
    o en otro tamaño de letra), el texto que está dentro de una imagen, y
    las notas de 9 pt o menos (de dónde se tomó un texto o una foto, notas
    al pie). Cada ejemplo se marca con ejemplo_tiene_imagen si incluye una
    figura: una imagen, un dibujo, una tabla o una fórmula en renglón
    aparte. La marca la propone el programa (hay una imagen en la zona del
    ejemplo, o se dejó texto de una figura sin copiar) y se revisó mirando
    cada página renderizada: lo que la revisión cambió está en
    EJEMPLO_AJUSTES e IMAGEN_REVISADA, con su razón.
  * Ciencias Sociales (V.1) casi no trae título "Ejemplo": la mayoría de sus
    DBA solo tienen una ilustración sin texto. Sin título, no hay ejemplo
    (null): no se adivina.
  * Lo demás (textos de las ilustraciones sin título, títulos) se ignora.

El texto se copia tal cual. Lo único que se normaliza es el espacio: los
saltos de línea pasan a un espacio y los espacios repetidos a uno (en el
ejemplo, un cambio de párrafo o de viñeta se guarda como un salto de línea,
para que se pueda leer). Un guion
al final de una línea se conserva y se une sin espacio a la línea
siguiente; cada caso queda listado en el informe para revisarlo.

Lo que la capa de texto del PDF no dice como la página impresa (una ligadura
"fi" sin declarar, un hueco dentro de una palabra) no se adivina: va en
CORRECCIONES, cada una verificada mirando la página. Lo que no se puede
resolver con certeza va en DUDOSOS.

Uso:  python3 construir_catalogo.py      (unos 7 minutos: leer los PDF es lento)
Escribe catalogo_dba.json e informe-correccion.md. Con la variable
CATALOGO_CACHE apuntando a una carpeta, guarda ahí lo leído de los PDF y las
corridas siguientes tardan segundos; el resultado es el mismo.
"""
import collections
import difflib
import json
import os
import re
import sys
import unicodedata

import pdfplumber

AQUI = os.path.dirname(os.path.abspath(__file__))
PDFS = os.path.join(AQUI, "..", "pdfs")
JSON_VIEJO = os.path.join(AQUI, "..", "normalized", "curriculo_men_normalizado.json")

# (codigo, nombre, area en el JSON viejo, archivo, version leida del documento: ADR-033)
AREAS = [
    ("MAT", "Matemáticas", "matemáticas", "dba_matematicas_v2.pdf", "V.2"),
    ("LEN", "Lenguaje", "lenguaje", "dba_lenguaje_v2.pdf", "V.2"),
    ("CN", "Ciencias Naturales", "ciencias naturales", "dba_ciencias_naturales_v1.pdf", "V.1"),
    ("CS", "Ciencias Sociales", "ciencias sociales", "dba_ciencias_sociales_v2.pdf", "V.1"),
]

TOPE_ENCABEZADO = 80      # el encabezado de grado está por encima
TOPE_PIE = 800            # por debajo, solo el pie de imprenta
ZONA_NUMERO_PAGINA = 755  # el número de página (solo cifras) cae más abajo
TOL_LINEA = 1.5           # palabras a esta distancia vertical: misma línea (las dos
                          # columnas pueden quedar a 3 puntos: no deben mezclarse)
SALTO_PARRAFO = 22        # más que esto entre dos líneas: otro bloque


def espacios(texto):
    """La única normalización permitida: espacios y saltos de línea."""
    return re.sub(r"\s+", " ", texto).strip()


def fuente(w):
    return w["fontname"].split("+")[-1]


def es_vineta(w):
    return "Wingdings" in fuente(w) and 9 <= w["size"] <= 11


def es_vineta_ejemplo(w):
    return "Wingdings" in fuente(w) and w["size"] < 9


def grado_de(palabras):
    """Grado del encabezado: 'Matemáticas • Grado 3º' viene letra a letra, en
    AvantGarde de ~13 pt. En algunas páginas de Ciencias Sociales va en Book y
    no en Medium, y unos puntos más abajo: por eso no se mira la variante."""
    texto = "".join(w["text"] for w in palabras
                    if w["top"] < TOPE_ENCABEZADO and "AvantGarde" in fuente(w)
                    and 12.5 <= w["size"] <= 14.5)
    m = re.search(r"Grado(\d{1,2})", texto.replace(" ", ""))
    return (int(m.group(1)), texto) if m else (None, texto)


def lineas_por_columna(ancho, palabras):
    """Agrupa las palabras del cuerpo en líneas, y las líneas en dos columnas."""
    cuerpo = [w for w in palabras
              if TOPE_ENCABEZADO + 30 < w["top"] < TOPE_PIE and w["size"] >= 7
              and ("AvantGarde" in fuente(w) or "Wingdings" in fuente(w))
              and not (w["top"] > ZONA_NUMERO_PAGINA and w["text"].isdigit())]
    cuerpo.sort(key=lambda w: (w["top"], w["x0"]))
    filas = []
    for w in cuerpo:
        if filas and abs(filas[-1][0]["top"] - w["top"]) <= TOL_LINEA:
            filas[-1].append(w)
        else:
            filas.append([w])
    # Cada palabra va a la columna de la izquierda si empieza antes de la
    # mitad de la página. No se decide por tramos: en una línea justificada
    # la última palabra de la columna izquierda puede quedar lejos de las
    # demás ("personas      con", CS 8°, p. 41) y no por eso es de la derecha.
    mitad = ancho * 0.5
    columnas = ([], [])
    for fila in filas:
        for lado in (0, 1):
            seg = sorted((w for w in fila if (w["x0"] >= mitad) == bool(lado)),
                         key=lambda w: w["x0"])
            if seg:
                columnas[lado].append(seg)
    for i, col in enumerate(columnas):
        # una viñeta (Wingdings) puede quedar uno o dos puntos más arriba que
        # su texto, y por eso en otra "línea": se pega al texto que tiene a
        # su derecha
        sueltas = [sg for sg in col if len(sg) == 1 and "Wingdings" in sg[0]["fontname"]]
        for v in sueltas:
            junto = [sg for sg in col if sg is not v and abs(sg[0]["top"] - v[0]["top"]) <= 4
                     and 0 <= sg[0]["x0"] - v[0]["x1"] <= 20]
            if junto:
                junto[0].insert(0, v[0])
                col.remove(v)
        # el número grande ("2.") está unos puntos más abajo que la primera
        # línea de su enunciado: se le adelanta para que la abra
        col.sort(key=lambda s: s[0]["top"] - (10 if s[0]["size"] > 20 else 0))
    return columnas


def es_avantgarde(w):
    return "AvantGarde" in fuente(w)


def clase(seg):
    w = seg[0]
    texto = " ".join(x["text"] for x in seg)
    if es_avantgarde(w) and w["size"] > 20 and re.fullmatch(r"\d{1,2}\.", texto):
        return "numero"
    if es_avantgarde(w) and 10.5 <= w["size"] <= 11.5:
        # sin espacios: en la página 41 de Ciencias Sociales el espaciado
        # parte la palabra ("Evidencias d e aprendizaje")
        # (y a veces con una llamada a nota pegada: "Ejemplo2", "Ejemplo[1]")
        titulo = re.sub(r"[\[\]\d]+$", "", texto.replace(" ", ""))
        if titulo == "Evidenciasdeaprendizaje":
            return "titulo_evidencias"
        if titulo == "Ejemplo":
            return "titulo_ejemplo"
        return "enunciado"
    if es_vineta(w):
        return "vineta"
    if es_vineta_ejemplo(w):
        return "vineta_ejemplo"
    if es_avantgarde(w) and 9.5 <= w["size"] <= 10.5:
        return "texto"
    return "otro"


def unir(lineas, guiones, donde):
    """Une líneas con un espacio. Un guion final pegado a una letra se une
    sin espacio a la línea siguiente (y se anota)."""
    texto = ""
    for ln in lineas:
        ln = espacios(ln)
        if texto.endswith("-") and re.search(r"\w-$", texto) and ln[:1].isalpha():
            guiones.append(dict(donde=donde, antes=texto[-25:], despues=ln[:25]))
            texto += ln
        else:
            texto = f"{texto} {ln}" if texto else ln
    return texto


def enderezar(chars):
    """Algunas líneas vienen guardadas al revés, de derecha a izquierda (en
    Ciencias Sociales 6°, p. 31, la línea con letras espaciadas "Compara la
    estructura social, política y" está como "y acitílop ,laicos ..."). Se
    parte el flujo en tramos de una misma altura y se invierte el tramo en el
    que la mayoría de los pasos van hacia la izquierda."""
    tramos, actual = [], []
    for ch in chars:
        if actual and abs(ch["top"] - actual[-1]["top"]) > 0.5 * max(ch["size"], 1):
            tramos.append(actual)
            actual = []
        actual.append(ch)
    if actual:
        tramos.append(actual)
    salida = []
    for t in tramos:
        letras = [c for c in t if not c["text"].isspace()]
        pasos = [b["x0"] - a["x0"] for a, b in zip(letras, letras[1:])]
        if len(pasos) >= 3 and sum(p < 0 for p in pasos) > 0.7 * len(pasos):
            # se invierte el orden, no se ordena por posición: en esos tramos
            # los espacios están mal ubicados, pero bien en la secuencia
            t = t[::-1]
        # espaciado típico entre letras de este tramo: en una línea con letras
        # espaciadas, un hueco "de espacio" tiene que ser bastante mayor
        letras = [c for c in t if not c["text"].isspace()]
        huecos = sorted(b["x0"] - a["x1"] for a, b in zip(letras, letras[1:])
                        if 0 < b["x0"] - a["x1"] < 20)
        tipico = huecos[len(huecos) // 2] if huecos else 0
        tamano = max((c["size"] for c in letras), default=10)
        if tipico < 0.15 * tamano:
            tipico = 0              # línea normal: rige el umbral general
        salida += [dict(c, tipico=tipico) for c in t]
    return salida


def palabras_de(chars, huecos):
    """Arma las palabras siguiendo el ORDEN en que el PDF guarda los
    caracteres, cortando donde el PDF pone un espacio o donde el texto salta
    de línea. Así se respetan los espacios que puso quien diagramó el
    documento, en vez de adivinarlos por la distancia entre letras. Los
    subíndices y superíndices (dm3, H2O) quedan pegados a su palabra.

    `huecos` recibe los saltos sin carácter dentro de una palabra: ahí el PDF
    dibuja una ligadura ("fi") que no declara como texto."""
    palabras, actual = [], None
    chars = enderezar(chars)

    def cerrar():
        nonlocal actual
        if actual:
            normales = [c for c in actual["chars"] if c["size"] >= 7] or actual["chars"]
            base = max(normales, key=lambda c: c["size"])
            palabras.append(dict(
                text="".join(c["text"] for c in actual["chars"]),
                x0=actual["chars"][0]["x0"], x1=actual["chars"][-1]["x1"],
                top=min(c["top"] for c in normales), fontname=base["fontname"],
                size=base["size"]))
        actual = None

    for ch in chars:
        f = ch["fontname"].split("+")[-1]
        if not ("AvantGarde" in f or "Wingdings" in f):
            continue                  # marcas de corte (Times), pie (Helvetica), imágenes
        if ch["text"].isspace() or ch["text"] == "":
            cerrar()
            continue
        if actual:
            prev = actual["chars"][-1]
            otra_linea = (ch["x0"] < prev["x1"] - 2
                          or abs(ch["top"] - prev["top"]) > max(ch["size"], prev["size"]))
            hueco = ch["x0"] - prev["x1"]
            # el número del DBA ("1.") viene pegado a su enunciado, sin espacio:
            # se corta donde cambia el tamaño de letra (no en sub/superíndices)
            otro_tamano = (ch["size"] >= 7 and prev["size"] >= 7
                           and max(ch["size"], prev["size"]) > 1.3 * min(ch["size"], prev["size"]))
            # un hueco del ancho de un espacio, sin carácter de espacio, también
            # separa palabras: el PDF a veces ubica la palabra siguiente solo
            # por posición ("o multiplicativas")
            # (dentro de una palabra el hueco es casi siempre < 0,13 del tamaño
            # de letra; los espacios "por posición" pasan de 0,2)
            espacio = hueco > max(0.2 * min(ch["size"], prev["size"]), 3 * ch["tipico"])
            if (otra_linea or otro_tamano or espacio
                    or "Wingdings" in f or "Wingdings" in prev["fontname"]):
                if espacio and not otra_linea and not otro_tamano and ch["size"] >= 7:
                    # se anota: el informe los lista para revisarlos. Uno
                    # ancho entre dos letras puede ser también una ligadura
                    # ("fi") que el PDF dibuja pero no declara como texto
                    huecos.append(dict(antes="".join(c["text"] for c in actual["chars"]),
                                       despues=ch["text"], hueco=round(hueco / ch["size"], 2),
                                       top=round(ch["top"]), x=round(ch["x0"])))
                cerrar()
        if actual is None:
            actual = dict(chars=[])
        actual["chars"].append(ch)
    cerrar()
    return palabras


def leer_pdf(archivo):
    """Lo que se usa de cada página: su ancho, sus caracteres y los recuadros
    de sus imágenes (fotos, dibujos pegados como imagen). Si la variable
    CATALOGO_CACHE nombra una carpeta, guarda ahí lo extraído para no volver a
    leer el PDF (solo sirve para desarrollar: el resultado es el mismo)."""
    cache = os.environ.get("CATALOGO_CACHE")
    ruta = os.path.join(cache, archivo + ".chars.json") if cache else None
    ruta_img = os.path.join(cache, archivo + ".imagenes.json") if cache else None
    if ruta and os.path.exists(ruta) and os.path.exists(ruta_img):
        crudas = json.load(open(ruta, encoding="utf-8"))
        imagenes = json.load(open(ruta_img, encoding="utf-8"))
    else:
        with pdfplumber.open(os.path.join(PDFS, archivo)) as pdf:
            crudas, imagenes = [], []
            for p in pdf.pages:
                crudas.append((p.width, [{k: c[k] for k in ("text", "x0", "x1", "top", "fontname", "size")}
                                         for c in p.chars]))
                imagenes.append([[round(i[k], 1) for k in ("x0", "top", "x1", "bottom")]
                                 for i in p.images])
        if ruta:
            os.makedirs(cache, exist_ok=True)
            json.dump(crudas, open(ruta, "w", encoding="utf-8"))
            json.dump(imagenes, open(ruta_img, "w", encoding="utf-8"))
    return crudas, imagenes


def de_figura(ch):
    """Una letra que no es del texto del documento ni de su marco: el cuerpo
    va en AvantGarde (y las viñetas en Wingdings), el pie de imprenta en
    Helvetica y las marcas de corte en Times. Lo demás (Arial, Myriad,
    Symbol…), y la letra de menos de 7 pt, es texto de una figura: un
    rótulo, una tabla, una fórmula."""
    f = ch["fontname"].split("+")[-1]
    if ch["text"].isspace() or ch["top"] > ZONA_NUMERO_PAGINA:
        return False
    if "AvantGarde" in f:
        return ch["size"] < 7
    return "Wingdings" not in f and f != "Helvetica" and not f.startswith("Times")


def paginas_del_pdf(archivo):
    """[(ancho, palabras, huecos, imagenes, letras de figura)] por página."""
    crudas, imagenes = leer_pdf(archivo)
    paginas = []
    for (ancho, chars), imgs in zip(crudas, imagenes):
        huecos = []
        figura = [(round(c["x0"], 1), round(c["top"], 1)) for c in chars if de_figura(c)]
        paginas.append((ancho, palabras_de(chars, huecos), huecos, imgs, figura))
    return paginas


def leer_area(codigo, archivo):
    """Recorre el PDF y devuelve los DBA tal como aparecen, en orden."""
    dbas, observaciones, encabezados, imagenes_de = [], [], {}, {}
    actual = None           # DBA que se está leyendo
    estado = None           # 'enunciado' | 'evidencias' | 'ejemplo' | None
    ultima = None           # (pagina, columna, top) de la última línea de evidencia
    grado_anterior = None
    for n, (ancho, palabras, huecos, imagenes, figura) in enumerate(paginas_del_pdf(archivo), 1):
        grado, texto_enc = grado_de(palabras)
        sin_encabezado = False
        if grado is None:
            con_dba = any(es_avantgarde(w) and w["size"] > 20 and TOPE_ENCABEZADO < w["top"] < TOPE_PIE
                          and re.fullmatch(r"\d{1,2}\.", w["text"]) for w in palabras)
            if not (con_dba and grado_anterior):
                estado = None         # el ejemplo no sigue en la página final de comentarios
                continue              # portada, presentación, créditos
            grado, sin_encabezado = grado_anterior, True
            texto_enc = ""
            observaciones.append(dict(pagina=n, tipo="página con DBA y sin encabezado de grado",
                                      texto=f"se toma el grado de la página anterior: {grado}"))
        grado_anterior = grado
        encabezados[n] = texto_enc
        imagenes_de[n] = (imagenes, figura)
        for c, col in enumerate(lineas_por_columna(ancho, palabras)):
            if estado == "ejemplo":
                # el ejemplo sigue arriba en esta columna: su zona empieza ahí
                actual["ejemplo_zonas"].append([n, c, TOPE_ENCABEZADO + 30, TOPE_PIE])
            for seg in col:
                k = clase(seg)
                top = seg[0]["top"]
                if k == "vineta":
                    texto = " ".join(x["text"] for x in seg[1:])
                else:
                    texto = " ".join(x["text"] for x in seg)
                if estado == "ejemplo" and k in ("numero", "titulo_evidencias", "titulo_ejemplo"):
                    actual["ejemplo_zonas"][-1][3] = top    # ahí termina la zona del ejemplo
                if estado == "ejemplo" and k not in ("numero", "titulo_evidencias", "titulo_ejemplo"):
                    vineta = k in ("vineta", "vineta_ejemplo")
                    actual["ejemplo_lineas"].append(dict(
                        pagina=n, columna=c, top=round(top, 1), x1=round(max(x["x1"] for x in seg), 1),
                        x0=round(seg[1 if vineta and len(seg) > 1 else 0]["x0"], 1),
                        x_vineta=round(seg[0]["x0"], 1) if vineta else None,
                        tamano=round(max(x["size"] for x in (seg[1:] if vineta and len(seg) > 1 else seg)), 1),
                        fuente=fuente(seg[-1]), clase=k,
                        texto=" ".join(x["text"] for x in seg[1:]) if vineta else texto))
                    continue
                if k == "numero":
                    actual = dict(numero=int(texto[:-1]), grado=grado, pagina=n,
                                  enunciado_lineas=[], evidencias=[],
                                  paginas=[n], sin_encabezado=sin_encabezado,
                                  ejemplo_titulo=None, ejemplo_lineas=[], ejemplo_zonas=[])
                    dbas.append(actual)
                    estado = "enunciado"
                    ultima = (n, c, top)
                elif k == "enunciado":
                    pegado = ultima and ultima[:2] == (n, c) and top - ultima[2] <= SALTO_PARRAFO
                    if estado == "enunciado" and actual is not None and pegado:
                        actual["enunciado_lineas"].append(texto)
                        ultima = (n, c, top)
                    elif estado in ("enunciado", "evidencias"):
                        observaciones.append(dict(pagina=n, tipo="negrita fuera de un enunciado",
                                                  texto=texto))
                elif k == "titulo_evidencias":
                    if actual is None or actual["evidencias"]:
                        observaciones.append(dict(pagina=n, tipo="título de evidencias sin DBA abierto",
                                                  texto=texto))
                    estado = "evidencias" if actual is not None else None
                elif k == "titulo_ejemplo":
                    if actual is not None and actual["ejemplo_titulo"] is None:
                        estado = "ejemplo"
                        actual["ejemplo_titulo"] = n
                        actual["ejemplo_zonas"].append([n, c, top, TOPE_PIE])
                    else:
                        estado = None
                        observaciones.append(dict(pagina=n, tipo="título de ejemplo sin DBA abierto",
                                                  texto=texto))
                elif k == "vineta" and estado == "evidencias":
                    actual["evidencias"].append(dict(lineas=[texto], pagina=n))
                    if n not in actual["paginas"]:
                        actual["paginas"].append(n)
                    ultima = (n, c, top)
                elif k == "texto" and estado == "evidencias" and actual["evidencias"]:
                    ev = actual["evidencias"][-1]
                    cerca = ultima and ultima[:2] == (n, c) and top - ultima[2] <= SALTO_PARRAFO
                    # sigue en otra columna u otra página: solo si la
                    # evidencia no había terminado con punto
                    sigue = (ultima and ultima[:2] != (n, c)
                             and not espacios(" ".join(ev["lineas"])).endswith("."))
                    if cerca or sigue:
                        ev["lineas"].append(texto)
                        if n not in actual["paginas"]:
                            actual["paginas"].append(n)
                        ultima = (n, c, top)
                    else:
                        estado = None
                elif k == "vineta" and estado != "ejemplo":
                    observaciones.append(dict(pagina=n, tipo="viñeta fuera de una lista de evidencias",
                                              texto=texto))
                # el resto -- textos de imágenes, títulos -- se ignora
    return dbas, observaciones, encabezados, imagenes_de


# ---------------------------------------------------------------- ejemplo
# Dónde empieza el texto corrido en cada columna: el margen de las viñetas o
# el del texto (medidos en las evidencias). Matemáticas, Lenguaje y Ciencias
# Naturales tienen la misma diagramación; Ciencias Sociales, dos.
BANDAS = {
    "MAT": {0: [(82, 112)], 1: [(354, 384)]},
    "LEN": {0: [(82, 112)], 1: [(354, 384)]},
    "CN": {0: [(82, 112)], 1: [(354, 384)]},
    "CS": {0: [(61, 90), (94, 124)], 1: [(333, 366), (367, 392)]},
}
# (en Ciencias Sociales la página 41 está corrida unos puntos: su columna
# derecha empieza en 364)
SALTO_EJEMPLO = 20        # más que esto entre dos renglones del ejemplo: otro párrafo
# Dónde termina el renglón lleno, por columna (en Ciencias Sociales, según el
# margen en que empieza). Un renglón que termina 20 puntos antes cierra su
# párrafo (o su verso, en un poema): el siguiente va en otra línea.
DERECHA = {"MAT": (316, 588), "LEN": (316, 588), "CN": (316, 588), "CS": ((296, 329), 568)}
AREA_MIN_IMAGEN = 1500    # puntos²: menos que esto es un adorno, no una figura

# Lo que la revisión de cada página renderizada cambió de la propuesta del
# programa. (codigo_dba, "quitar" | "poner", página, comienzo del renglón,
# razón). "quitar": el programa lo toma por texto corrido y es parte de una
# figura (una tabla, una fórmula). "poner": el programa lo deja y es texto
# corrido. Nunca agrega palabras: solo decide qué renglones del PDF se copian.
TABLA = "es parte de una tabla del ejemplo, no texto corrido"
ROTULO = "es un rótulo de la figura, no texto corrido"
EJEMPLO_AJUSTES = [
    ("MAT-01-06", "quitar", 11, "Mariposa Pingüino", ROTULO),
    ("MAT-02-10", "quitar", 20, "Candidato 1", ROTULO),
    ("MAT-02-10", "quitar", 20, "Candidato 2", ROTULO),
    ("MAT-02-10", "quitar", 20, "Candidato 3", ROTULO),
    ("MAT-02-10", "quitar", 20, "Candidato 4", ROTULO),
    ("MAT-02-10", "quitar", 20, "Cada Equivale", "es la leyenda del pictograma (un ícono de estrella entre «Cada» y «Equivale»)"),
    ("MAT-03-10", "quitar", 28, "Caminando 10", TABLA),
    ("MAT-03-10", "quitar", 28, "Carro particular 12", TABLA),
    ("MAT-06-08", "quitar", 49, "Empresa A", TABLA),
    ("MAT-06-08", "quitar", 49, "Hasta 300", TABLA),
    ("MAT-06-08", "quitar", 49, "kilos para", TABLA),
    ("MAT-06-08", "quitar", 49, "pesos. 250.000", TABLA),
    ("MAT-06-08", "quitar", 49, "pesos más", TABLA),
    ("MAT-06-08", "quitar", 49, "de más.", TABLA),
    ("MAT-11-08", "quitar", 85, "dy", "es una fracción (dy/dx) escrita en dos renglones, parte de una fórmula"),
    ("MAT-11-08", "quitar", 85, "dx", "es una fracción (dy/dx) escrita en dos renglones, parte de una fórmula"),
    ("MAT-11-10", "quitar", 86, "TOTAL 183", TABLA),
    ("CN-04-05", "quitar", 17, "Agua - Sal", "es una fila de la tabla «Mezcla» del ejemplo, no texto corrido"),
    ("CN-04-05", "quitar", 17, "Trozos de banano", "es una fila de la tabla «Mezcla» del ejemplo, no texto corrido"),
    ("CN-04-05", "quitar", 17, "Agua – Azúcar", "es una fila de la tabla «Mezcla» del ejemplo, no texto corrido"),
    ("CN-04-05", "quitar", 17, "Agua - Arena", "es una fila de la tabla «Mezcla» del ejemplo, no texto corrido"),
]

# Ejemplos cuya marca de imagen la revisión cambió: {codigo_dba: (valor, razón)}
DIBUJO = "la figura está dibujada con trazos (no es una imagen pegada), y el programa no la ve"
IMAGEN_REVISADA = {
    "MAT-01-05": (True, "las tiras de colores son un dibujo; el texto nombra tiras por su color dibujado"),
    "MAT-02-07": (True, "el mapa es un dibujo: " + DIBUJO),
    "MAT-02-09": (True, "la niña y su globo de pensamiento son un dibujo: " + DIBUJO),
    "MAT-05-01": (True, "el plano de la finca es un dibujo: " + DIBUJO),
    "MAT-05-07": (True, "el mapa del barrio es un dibujo: " + DIBUJO),
    "MAT-05-10": (True, "los gráficos de barras y circular: " + DIBUJO),
    "MAT-06-03": (True, "las tres balanzas: " + DIBUJO),
    "MAT-07-03": (True, "la calculadora: " + DIBUJO),
    "MAT-07-07": (True, "las balanzas con gallinas: " + DIBUJO),
    "MAT-07-09": (True, "el menú del almuerzo: " + DIBUJO),
    "MAT-08-07": (True, "los rompecabezas sobre la cuadrícula: " + DIBUJO),
    "MAT-08-12": (True, "la tabla «Rango de edades» está dibujada, sin texto que el programa lea"),
    "MAT-09-10": (True, "los diagramas de caja y bigote: " + DIBUJO),
    "MAT-10-01": (True, "los triángulos: " + DIBUJO),
    "MAT-10-04": (True, "el disco de colores: " + DIBUJO),
    "LEN-03-04": (True, "el plan textual es un organizador dibujado (cuadros y flechas), no una imagen pegada"),
    "LEN-08-04": (True, "el poema está escrito sobre el dibujo de una hoja"),
    "LEN-09-08": (True, "la lista de recomendaciones está manuscrita en el dibujo de una hoja"),
    "LEN-11-03": (True, "las preguntas están manuscritas en el dibujo de un cuaderno"),
    "LEN-11-08": (True, "las indicaciones están escritas en el dibujo de un tablero"),
}

# Ejemplos que la revisión no pudo resolver con certeza: {codigo_dba: razón}
FORMULA = "una fórmula escrita dentro de la frase (fracción en dos pisos o símbolo especial) no se lee completa"
EJEMPLO_DUDOSO = {
    "MAT-05-03": FORMULA + ": las fracciones 9/5 y 11/6 quedan como «9 … 11» y «5 6»",
    "MAT-08-02": FORMULA + ": los símbolos del triángulo y el cuadrado faltan («en las casillas y y»)",
    "MAT-09-01": FORMULA + ": D/d y 4/3 π(d/2)³ quedan como «tablero:dd», «=√5» y «4 π(d)3»",
    "MAT-10-02": FORMULA + ": «Conjunto 1: 1, 1 , 1» (faltan los denominadores 10, 100 y 1000)",
    "MAT-10-04": FORMULA + ": «posición de inicio =0°» (falta la letra α)",
    "MAT-10-10": FORMULA + ": «aproximadamente 1» y «haya sido 1» (falta el denominador 2 de 1/2)",
    "MAT-11-08": FORMULA + ": faltan dy/dx y los denominadores de y(x)",
}


def en_banda(area, columna, x):
    return any(a <= x <= b for a, b in BANDAS[area][columna])


def corto(area, ln, imgs):
    """¿El renglón termina antes del borde derecho? Si a su derecha hay una
    imagen, el texto la rodea: el borde es el comienzo de la imagen."""
    borde = DERECHA[area][ln["columna"]]
    if isinstance(borde, tuple):
        borde = borde[0] if ln["x0"] < BANDAS[area][0][1][0] else borde[1]
    for pagina, x0, top, x1, bottom in imgs:
        if pagina == ln["pagina"] and x0 > ln["x0"] and top - 4 <= ln["top"] <= bottom + 4:
            borde = min(borde, x0)
    return ln["x1"] < borde - 20


def dentro_de(linea, img):
    """El renglón entero está dentro del recuadro de la imagen (no basta con
    rozarlo: un pie de imagen puede empezar un punto antes de su borde)."""
    x0, top, x1, bottom = img
    return (x0 - 2 <= linea["x0"] and linea["x1"] <= x1 + 2
            and top - 2 <= linea["top"] and linea["top"] + linea["tamano"] <= bottom + 2)


def imagenes_del_ejemplo(d, imagenes_de, ancho=612):
    """Las imágenes (fotos, dibujos pegados como imagen) que caen en la zona
    del ejemplo: misma página, misma columna, entre el título (o el comienzo
    de la columna) y el DBA siguiente."""
    halladas = []
    for pagina, col, desde, hasta in d["ejemplo_zonas"]:
        for img in imagenes_de.get(pagina, ([], []))[0]:
            x0, top, x1, bottom = img
            if (x1 - x0) * (bottom - top) < AREA_MIN_IMAGEN:
                continue
            centro_x, centro_y = (x0 + x1) / 2, (top + bottom) / 2
            if (centro_x >= ancho / 2) == bool(col) and desde <= centro_y <= hasta:
                halladas.append([pagina] + img)
    return halladas


def letras_de_figura(d, imagenes_de, ancho=612):
    """Cuántas letras de figura (de_figura) caen en la zona del ejemplo."""
    return sum(1 for pagina, col, desde, hasta in d["ejemplo_zonas"]
               for x, top in imagenes_de.get(pagina, ([], []))[1]
               if (x >= ancho / 2) == bool(col) and desde <= top <= hasta)


def armar_ejemplo(cod, area, d, imagenes_de, guiones):
    """El ejemplo de un DBA: (texto o None, páginas, tiene_imagen, renglones
    con la decisión de cada uno, imágenes halladas). El texto es el de los
    renglones que se copian, unidos como el enunciado; cada párrafo o viñeta,
    en su propia línea."""
    if d["ejemplo_titulo"] is None:
        return None, [], False, [], []
    imgs = imagenes_del_ejemplo(d, imagenes_de)
    lineas = [dict(ln) for ln in d["ejemplo_lineas"]]
    for ln in lineas:
        x = ln["x_vineta"] if ln["x_vineta"] is not None else ln["x0"]
        if not 9.5 <= ln["tamano"] <= 11.5:
            ln["copia"], ln["por"] = False, f"letra de {ln['tamano']:g} pt"
        elif not en_banda(area, ln["columna"], x):
            ln["copia"], ln["por"] = False, "fuera del margen del texto"
        elif any(dentro_de(ln, img[1:]) for img in imgs if img[0] == ln["pagina"]):
            ln["copia"], ln["por"] = False, "dentro de una imagen"
        else:
            ln["copia"], ln["por"] = True, "texto corrido"
    for c, accion, pagina, comienzo, razon in EJEMPLO_AJUSTES:
        if c != cod:
            continue
        # entre los renglones cuya decisión cambia (si "quitar", los que se copiaban)
        cuales = [ln for ln in lineas if ln["pagina"] == pagina and ln["texto"].startswith(comienzo)
                  and ln["copia"] == (accion == "quitar")]
        assert len(cuales) == 1, (cod, accion, pagina, comienzo, len(cuales))
        cuales[0]["copia"], cuales[0]["por"] = accion == "poner", f"revisión: {razon}"
    # una figura deja rastro: una imagen, o texto que no se copió y no es una
    # nota (las notas de 9 pt: de dónde se tomó un texto o una foto)
    nota = lambda ln: ln["tamano"] <= 9.2 and "Medium" not in ln["fuente"] and en_banda(
        area, ln["columna"], ln["x0"])
    tiene_imagen = (bool(imgs) or any(not ln["copia"] and not nota(ln) for ln in lineas)
                    or letras_de_figura(d, imagenes_de) >= 3)
    if cod in IMAGEN_REVISADA:
        tiene_imagen = IMAGEN_REVISADA[cod][0]
    parrafos, previa = [], None
    copiadas = [ln for ln in lineas if ln["copia"]]
    for k, ln in enumerate(copiadas):
        texto = espacios(ln["texto"])
        # cada inciso de una lista ("a) …", "b. …") empieza su propia línea
        inciso = re.match(r"[a-h][).]\s", texto)
        # un renglón corto cierra su párrafo, salvo que el anterior termine en
        # el mismo punto: entonces el texto es angosto porque rodea una imagen
        justificado = previa is not None and k >= 2 and abs(copiadas[k - 2]["x1"] - previa["x1"]) <= 1
        if (previa is None or ln["clase"] in ("vineta", "vineta_ejemplo") or inciso
                or (corto(area, previa, imgs) and not justificado)):
            nuevo = True
        elif (ln["pagina"], ln["columna"]) == (previa["pagina"], previa["columna"]):
            nuevo = ln["top"] - previa["top"] > SALTO_EJEMPLO
        else:
            nuevo = False
        if nuevo:
            parrafos.append([texto])
        else:
            parrafos[-1].append(texto)
        previa = ln
    texto = "\n".join(unir(p, guiones, f"{cod} ejemplo") for p in parrafos) or None
    paginas = sorted({ln["pagina"] for ln in lineas if ln["copia"]})
    return texto, paginas, tiene_imagen, lineas, imgs


# ------------------------------------------------------------ correcciones
# Donde la CAPA DE TEXTO del PDF no dice lo que la página IMPRESA muestra, y
# ningún programa puede saberlo solo. Cada una se verificó mirando la página
# renderizada. Solo tocan espacios, saltos de línea, una ligadura que el PDF
# dibuja pero no declara como texto, o una llamada a nota al pie: nunca una
# palabra. (Las dos últimas, CS-08-08 y MAT-04-02, las decidió el equipo el
# 2026-10-26 al revisar el PR #2: antes estaban como dudosas.)
# (codigo_dba, campo, texto como sale del PDF, texto corregido, página, razón)
PARTICION = "guion de partición al final de la línea (la palabra se corta en dos renglones)"
CORRECCIONES = [
    ("CS-06-05", "evidencia 1", "geográ cos", "geográficos", 31,
     "la ligadura «fi» está dibujada pero el PDF no la declara como texto: queda un hueco"),
    ("CS-07-07", "enunciado", "Co mprende", "Comprende", 36,
     "hueco de diagramación dentro de la palabra, sin carácter de espacio"),
    ("MAT-02-01", "evidencia 2", "? +b = c.", "? + b = c.", 15,
     "la página muestra «+ b», como «a + b» en la línea anterior; la capa de texto no trae ese espacio"),
    ("MAT-09-06", "evidencia 1", "bidimen-sionales", "bidimensionales", 69,
     "guion de partición al final de la línea (la palabra se corta en dos renglones)"),
    ("CS-08-08", "enunciado", "Comprendelaimportanciadelasasociaciones,",
     "Comprende la importancia de las asociaciones,", 41,
     "el PDF oficial imprime esas palabras sin espacios (se ve así en la página): solo se agregan los espacios"),
    ("MAT-04-02", "enunciado", "(fraccionarios)1", "(fraccionarios)", 30,
     "el «1» es la llamada en superíndice a una nota al pie de la misma página, no parte del enunciado"),
    # ejemplos (encargo 05): el mismo criterio
    ("MAT-04-05", "ejemplo", "personas es1", "personas es", 33,
     "el «1» (de 6 pt) es la llamada a la nota al pie que dice de dónde se tomó la receta"),
    ("MAT-01-03", "ejemplo", "dife-rente", "diferente", 9, PARTICION),
    ("MAT-01-05", "ejemplo", "tama-ños", "tamaños", 10, PARTICION),
    ("MAT-04-01", "ejemplo", "preparar limona-das", "preparar limonadas", 30, PARTICION),
    ("MAT-04-01", "ejemplo", "dife-rentes", "diferentes", 30, PARTICION),
    ("CS-07-06", "ejemplo", "histó-rico", "histórico", 36, PARTICION),
]

# Lo que no se puede resolver con certeza: se deja como está en el PDF y se
# marca. El informe lo explica uno por uno.
DUDOSOS = {}


def corregir(registro):
    """Aplica CORRECCIONES. Falla si el texto a corregir no aparece tal cual:
    así, si cambia la lectura del PDF, nadie corrige a ciegas."""
    hechas = []
    for cod, campo, mal, bien, pagina, razon in CORRECCIONES:
        if cod != registro["codigo_dba"]:
            continue
        if campo in ("enunciado", "ejemplo"):
            assert registro[campo].count(mal) == 1, (cod, campo, mal)
            registro[campo] = registro[campo].replace(mal, bien)
        else:
            i = int(campo.split()[1]) - 1
            assert registro["evidencias"][i].count(mal) == 1, (cod, campo, mal)
            registro["evidencias"][i] = registro["evidencias"][i].replace(mal, bien)
        hechas.append(dict(codigo_dba=cod, campo=campo, pdf=mal, corregido=bien,
                           pagina=pagina, razon=razon))
    return hechas


def clave(texto):
    """Para emparejar con el JSON viejo: sin tildes, sin mayúsculas y sin
    puntuación. SOLO para buscar; nunca para guardar texto."""
    t = unicodedata.normalize("NFKD", texto)
    t = "".join(ch for ch in t if not unicodedata.combining(ch)).lower()
    return re.sub(r"[^a-z0-9ñ]+", "", t)


def construir():
    viejos = [r for r in json.load(open(JSON_VIEJO, encoding="utf-8"))["records"]
              if r["tipo"] == "DBA"]
    catalogo, cambios, guiones, observaciones, sin_par = [], [], [], [], []
    corregidas, revision = [], []
    usados = set()
    for codigo, nombre, area_vieja, archivo, version in AREAS:
        print(f"leyendo {archivo} ...", file=sys.stderr)
        dbas, obs, encabezados, imagenes_de = leer_area(codigo, archivo)
        for o in obs:
            o["area"] = codigo
        observaciones += obs
        del_area = [(i, r) for i, r in enumerate(viejos) if r["area"] == area_vieja]
        registros = []
        for d in dbas:
            cod = f"{codigo}-{d['grado']:02d}-{d['numero']:02d}"
            ejemplo, pag_ejemplo, con_imagen, renglones, imgs = armar_ejemplo(
                cod, codigo, d, imagenes_de, guiones)
            revision.append(dict(codigo_dba=cod, titulo=d["ejemplo_titulo"], zonas=d["ejemplo_zonas"],
                                 renglones=renglones, imagenes=imgs, tiene_imagen=con_imagen))
            registro = dict(
                codigo_dba=cod, codigo_area=codigo, area=nombre, grado=d["grado"],
                numero=d["numero"],
                enunciado=unir(d["enunciado_lineas"], guiones, f"{cod} enunciado"),
                evidencias=[unir(e["lineas"], guiones, f"{cod} evidencia {i}")
                            for i, e in enumerate(d["evidencias"], 1)],
                documento=dict(archivo=archivo, version=version),
                pagina=d["pagina"],
                paginas_evidencias=[e["pagina"] for e in d["evidencias"]],
                ejemplo=ejemplo,
                ejemplo_paginas=pag_ejemplo,
                ejemplo_tiene_imagen=con_imagen,
                encabezado_pagina=espacios(encabezados[d["pagina"]]),
                dudoso=(["la página no tiene encabezado de grado: se toma el de la página "
                         "anterior y la numeración que sigue"] if d["sin_encabezado"] else []),
                id_anterior=None,
            )
            if cod in DUDOSOS:
                registro["dudoso"].append(DUDOSOS[cod])
            if cod in EJEMPLO_DUDOSO:
                registro["dudoso"].append(f"ejemplo: {EJEMPLO_DUDOSO[cod]}")
            corregidas += corregir(registro)
            registros.append(registro)
        # Pareja en el JSON viejo, para decir qué cambió. Primero por el mismo
        # enunciado; después, a los que quedan, por parecido: en el JSON hay
        # enunciados con basura de las marcas de corte ("150 S") o con el
        # ejemplo pegado, y otros con palabras perdidas.
        pares = {}
        for k, reg in enumerate(registros):
            for i, r in del_area:
                if i not in usados and clave(r["referente"]) == clave(reg["enunciado"]):
                    pares[k] = (r, "mismo enunciado")
                    usados.add(i)
                    break
        for k, reg in enumerate(registros):
            if k in pares:
                continue
            candidatos = [(difflib.SequenceMatcher(None, clave(r["referente"]),
                                                   clave(reg["enunciado"])).ratio(), i, r)
                          for i, r in del_area if i not in usados]
            candidatos += [(1.0, i, r) for i, r in del_area if i not in usados
                           and clave(r["referente"]).startswith(clave(reg["enunciado"]))]
            if candidatos:
                razon, i, r = max(candidatos, key=lambda x: x[0])
                if razon >= 0.85:
                    pares[k] = (r, "enunciado parecido")
                    usados.add(i)
        for k, registro in enumerate(registros):
            catalogo.append(registro)
            cod = registro["codigo_dba"]
            if k not in pares:
                sin_par.append(cod)
                continue
            viejo, como = pares[k]
            registro["id_anterior"] = viejo["id"]
            g_viejo = int(viejo["grado"].rstrip("°"))
            c = dict(codigo_dba=cod, id_anterior=viejo["id"], pagina=registro["pagina"],
                     encabezado=registro["encabezado_pagina"], pareja=como)
            if g_viejo != registro["grado"]:
                c["grado"] = (g_viejo, registro["grado"])
            if int(viejo["numero"]) != registro["numero"]:
                c["numero"] = (int(viejo["numero"]), registro["numero"])
            if viejo["referente"] != registro["enunciado"]:
                c["enunciado"] = (viejo["referente"], registro["enunciado"])
            ev_v = [espacios(e) for e in viejo["evidencias"]]
            if ev_v != registro["evidencias"]:
                c["evidencias"] = (ev_v, registro["evidencias"])
            if len(c) > 5:
                cambios.append(c)
        for i, r in del_area:
            if i not in usados:
                sin_par.append(f"JSON viejo sin DBA en el PDF: {r['id']} ({r['grado']})")
    hechas = {(c["codigo_dba"], c["campo"]) for c in corregidas}
    faltan = [c[:2] for c in CORRECCIONES if c[:2] not in hechas]
    assert not faltan, f"correcciones que no se aplicaron: {faltan}"
    for tabla, nombre in ((EJEMPLO_AJUSTES, "EJEMPLO_AJUSTES"), (IMAGEN_REVISADA, "IMAGEN_REVISADA"),
                          (EJEMPLO_DUDOSO, "EJEMPLO_DUDOSO")):
        cods = {x[0] for x in tabla} if isinstance(tabla, list) else set(tabla)
        assert cods <= {r["codigo_dba"] for r in catalogo if r["ejemplo"] or r["ejemplo_tiene_imagen"]
                        or r["codigo_dba"] in {v["codigo_dba"] for v in revision if v["titulo"]}}, nombre
    return catalogo, cambios, guiones, observaciones, sin_par, corregidas, revision


# --------------------------------------------------------------- informe
def informe_ejemplos(w, catalogo, revision, nombres):
    """Sección 8: el ejemplo de cada DBA (encargo 05)."""
    rev = {v["codigo_dba"]: v for v in revision}
    w("## 8. El ejemplo de cada DBA (encargo 05, QA-011)")
    w("")
    w("Cada DBA del MEN tiene, además del enunciado y las evidencias, un **ejemplo**: una situación")
    w("concreta que muestra lo que el estudiante debe poder hacer. El catálogo lo trae ahora en el")
    w("campo `ejemplo`, con las páginas de donde se copió (`ejemplo_paginas`) y la marca")
    w("`ejemplo_tiene_imagen`. El texto se copia exacto, como el enunciado; cada párrafo, viñeta o")
    w("verso va en su propia línea.")
    w("")
    w("| Área | DBA | Con ejemplo (texto) | Incluye una figura | Solo figura, sin texto | Sin ejemplo | Dudosos |")
    w("|---|---|---|---|---|---|---|")
    for cod, nombre in nombres.items():
        rs = [r for r in catalogo if r["codigo_area"] == cod]
        w(f"| {nombre} | {len(rs)} | {sum(1 for r in rs if r['ejemplo'])} | "
          f"{sum(1 for r in rs if r['ejemplo_tiene_imagen'])} | "
          f"{sum(1 for r in rs if r['ejemplo_tiene_imagen'] and not r['ejemplo'])} | "
          f"{sum(1 for r in rs if not r['ejemplo'] and not r['ejemplo_tiene_imagen'])} | "
          f"{sum(1 for r in rs if any(d.startswith('ejemplo:') for d in r['dudoso']))} |")
    rs = catalogo
    w(f"| **Total** | {len(rs)} | {sum(1 for r in rs if r['ejemplo'])} | "
      f"{sum(1 for r in rs if r['ejemplo_tiene_imagen'])} | "
      f"{sum(1 for r in rs if r['ejemplo_tiene_imagen'] and not r['ejemplo'])} | "
      f"{sum(1 for r in rs if not r['ejemplo'] and not r['ejemplo_tiene_imagen'])} | "
      f"{sum(1 for r in rs if any(d.startswith('ejemplo:') for d in r['dudoso']))} |")
    w("")
    w("**«Incluye una figura»** quiere decir que en la zona del ejemplo hay una imagen, un dibujo, una")
    w("tabla o una fórmula en renglón aparte. El texto que la acompaña se copió; el texto que está")
    w("**dentro** de la figura (rótulos, celdas de una tabla, letreros de un dibujo) y las notas de")
    w("dónde se tomó (créditos, de 9 pt) no. En el Paso 2 esos ejemplos muestran el aviso *«Este")
    w("ejemplo incluye una imagen que no se muestra en esta versión.»* (`06-spec` §2.4).")
    w("")
    w("**Esto corrige una cifra de ADR-011.** ADR-011 estimó que las figuras eran «rara excepción (2 a 8")
    w("casos)» por área, contando las menciones a una figura en el texto. Mirando las páginas, casi")
    w("todos los ejemplos de Matemáticas, Lenguaje y Ciencias Naturales traen una figura: muchas son")
    w("ilustraciones que acompañan un texto completo, pero en otras el texto no se entiende sin la")
    w("figura (una tabla de datos, una gráfica). La decisión de ADR-011 (el ejemplo como escenario para")
    w("generar preguntas) no cambia, pero el ejemplo llega a la IA sin su figura en la mayoría de los")
    w("casos. Ver el informe del encargo 05.")
    w("")
    w("**Ciencias Sociales** (V.1) casi no trae ejemplos: de sus 82 DBA, solo")
    w(f"{sum(1 for r in catalogo if r['codigo_area'] == 'CS' and rev[r['codigo_dba']]['titulo'])} tienen el título «Ejemplo».")
    w("Los demás solo tienen una ilustración sin título ni texto, y quedan sin ejemplo (`null`).")
    w("**Ciencias Naturales:** 28 ejemplos son solo una figura (una infografía, un esquema) con el")
    w("texto dentro de la imagen: quedan con `ejemplo` vacío y la marca de figura.")
    w(f"**Lenguaje:** `{', '.join(r['codigo_dba'] for r in catalogo if r['codigo_area'] == 'LEN' and not rev[r['codigo_dba']]['titulo'])}`")
    w("no tiene título «Ejemplo» (solo una ilustración).")
    w("")
    w("### 8.1 Cómo se decidió qué se copia y qué es figura")
    w("")
    w("El programa propone; la revisión de cada página renderizada (todas las páginas con ejemplo, de")
    w("los cuatro documentos) confirma o corrige. Lo que la revisión cambió está escrito en el script")
    w("(`EJEMPLO_AJUSTES`, `IMAGEN_REVISADA`, `EJEMPLO_DUDOSO`), con su razón:")
    w("")
    w("| DBA | Qué cambió la revisión | Razón |")
    w("|---|---|---|")
    for cod, accion, pagina, comienzo, razon in EJEMPLO_AJUSTES:
        w(f"| `{cod}` | {accion} el renglón «{celda(comienzo)}…» (p. {pagina}) | {celda(razon)} |")
    for cod, (valor, razon) in IMAGEN_REVISADA.items():
        w(f"| `{cod}` | {'con' if valor else 'sin'} figura | {celda(razon)} |")
    w("")
    w("Las correcciones de texto del ejemplo (guiones de partición y una llamada a nota) están en la")
    w("tabla de la sección 3.3, con las del enunciado y las evidencias.")
    w("")
    w("### 8.2 Ejemplos dudosos")
    w("")
    w("Se copiaron tal cual y se marcaron en el campo `dudoso` del DBA. En todos, el problema es una")
    w("fórmula escrita dentro de la frase: la capa de texto del PDF no la trae completa, y escribirla")
    w("a mano sería agregar texto que no se leyó del documento.")
    w("")
    for cod, razon in EJEMPLO_DUDOSO.items():
        w(f"- **`{cod}`**: {razon}.")
    w("")



def tipo_de_cambio(viejo, nuevo):
    """En palabras simples, qué le pasaba al texto del JSON viejo."""
    a, b = re.sub(r"\s+", "", viejo), re.sub(r"\s+", "", nuevo)
    if a == b:
        return "solo espacios (palabras pegadas o separadas)"
    if b in a:
        return "tenía texto de más (basura de la página)"
    if a in b:
        return "estaba cortado: le faltaba el final"
    return "palabras distintas"


def diferencia(viejo, nuevo, ancho=20):
    if re.sub(r"\s+", "", viejo) == re.sub(r"\s+", "", nuevo):
        i = next(k for k, (x, y) in enumerate(zip(viejo, nuevo)) if x != y)
        return (f"solo espacios: «…{viejo[max(0, i - ancho):i + 2 * ancho]}…» → "
                f"«…{nuevo[max(0, i - ancho):i + 2 * ancho]}…»")
    sm = difflib.SequenceMatcher(None, viejo, nuevo, autojunk=False)
    partes = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            partes.append(f"«…{viejo[max(0, i1 - ancho):i2 + ancho]}…» → «…{nuevo[max(0, j1 - ancho):j2 + ancho]}…»")
    return " · ".join(partes[:2]) + (" · (y más)" if len(partes) > 2 else "")


def celda(t):
    return str(t).replace("|", "\\|").replace("\n", " ")


def generar_informe(catalogo, cambios, guiones, observaciones, corregidas, viejos, revision):
    L = []
    w = L.append
    nombres = {a[0]: a[1] for a in AREAS}
    ids_viejos = collections.Counter(r["id"] for r in viejos)
    por_area_grado = collections.Counter((r["codigo_area"], r["grado"]) for r in catalogo)
    area_vieja = {a[2]: a[0] for a in AREAS}
    viejo_ag = collections.Counter((area_vieja[r["area"]], int(r["grado"].rstrip("°"))) for r in viejos)
    de_grado = [c for c in cambios if "grado" in c]
    repetidos = [c for c in de_grado if ids_viejos[c["id_anterior"]] > 1]
    nuevos = [r for r in catalogo if r["id_anterior"] is None]
    cambio_ev = [c for c in cambios if "evidencias" in c]
    n_ev_viejo = sum(len(r["evidencias"]) for r in viejos)
    n_ev_nuevo = sum(len(r["evidencias"]) for r in catalogo)
    dudosos = [r for r in catalogo if r["dudoso"]]

    w("# Informe de corrección del catálogo de DBA")
    w("")
    w("**Encargos 02 y 05** (`docs/encargos/02-catalogo-curricular-corregido.md`, `05-ejemplos-y-censo.md`).")
    w("**Archivo generado** por")
    w("`construir_catalogo.py`: no se edita a mano. Las cifras y las tablas salen del catálogo que ese")
    w("script arma leyendo los cuatro PDF oficiales del MEN (`../pdfs/`).")
    w("")
    w("## 1. En una frase")
    w("")
    w(f"El catálogo nuevo, `catalogo_dba.json`, tiene **{len(catalogo)} DBA y {n_ev_nuevo} evidencias**, cada")
    w("uno con la página del PDF de donde se copió. Frente al JSON heredado de la versión 2")
    w(f"({len(viejos)} DBA, {n_ev_viejo} evidencias): **{len(de_grado)} DBA estaban en el grado equivocado**,")
    w(f"**{len(nuevos)} faltaba**, y **{len(cambios) - len(de_grado) + sum(1 for c in de_grado if len(c) > 6)}**")
    w("tenían errores en el texto del enunciado o de las evidencias. El JSON original no se tocó.")
    w("")
    w("## 2. Qué estaba mal en el JSON viejo")
    w("")
    w(f"- **DBA en el grado equivocado: {len(de_grado)}.** La extracción de la V2 asignó al grado")
    w("  anterior el primer DBA (a veces los dos primeros) de la primera página de muchos grados. En")
    w(f"  {len(repetidos)} casos eso produjo un identificador repetido (por ejemplo, dos")
    w("  `matemáticas_2_dba_1`): son los 13 pares que ya se conocían (pendientes, A12). En los otros")
    w(f"  {len(de_grado) - len(repetidos)} el número no chocaba con nada, y por eso el error no se veía.")
    w("  Consecuencia: el docente vería en un grado DBA de otro, y a algunos grados les faltaban.")
    w(f"- **DBA que faltaba: {', '.join(r['codigo_dba'] for r in nuevos)}.** Está en el PDF (página "
      f"{', '.join(str(r['pagina']) for r in nuevos)}) y no en el JSON.")
    w(f"- **Evidencias perdidas o pegadas: en {sum(1 for c in cambio_ev if len(c['evidencias'][0]) != len(c['evidencias'][1]))} DBA**")
    w("  el JSON tenía menos evidencias que el PDF: a veces se perdió la primera o la última, a veces")
    w("  dos venían pegadas en una (se ve una «m» suelta en medio del texto: es la viñeta).")
    w("- **Textos con basura o incompletos.** Números de las marcas de corte de la imprenta pegados al")
    w("  final («… vereda o lugar donde vive. 6 5 0 1 12»), el pie de página o el encabezado")
    w("  («Ciencias Naturales • Grado 6°»), el ejemplo o una tabla pegados a la última evidencia,")
    w("  palabras perdidas o fuera de lugar en algunas páginas de Ciencias Sociales, y frases cortadas.")
    w("- **Palabras pegadas** («Reconoceelsignoigualcomo…»): en esas páginas el PDF separa las palabras")
    w("  solo por su posición, sin carácter de espacio, y la extracción vieja no lo notó.")
    w("")
    w("## 3. Qué se corrigió")
    w("")
    w("### 3.1 DBA que cambian de grado")
    w("")
    w("La prueba es el encabezado de la página del PDF donde está el DBA.")
    w("")
    w("| DBA nuevo | Identificador viejo | Grado viejo → nuevo | Página | Encabezado de la página |")
    w("|---|---|---|---|---|")
    for c in de_grado:
        rep = " (repetido en el JSON)" if ids_viejos[c["id_anterior"]] > 1 else ""
        w(f"| `{c['codigo_dba']}` | `{c['id_anterior']}`{rep} | {c['grado'][0]}° → {c['grado'][1]}° | "
          f"{c['pagina']} | {celda(c['encabezado'])} |")
    w("")
    w("### 3.2 DBA cuyo texto cambia")
    w("")
    w("Cada fila dice qué le pasaba al texto del JSON viejo. «Basura de la página» son los números")
    w("de las marcas de corte, el pie o el encabezado, o el ejemplo o una tabla pegados al final. Si")
    w("el DBA también cambió de grado, está además en la tabla anterior. El detalle de cada")
    w("diferencia está en el anexo.")
    w("")
    w("| DBA | Página | Enunciado | Evidencias |")
    w("|---|---|---|---|")
    for c in cambios:
        if "enunciado" not in c and "evidencias" not in c:
            continue
        enun = tipo_de_cambio(*c["enunciado"]) if "enunciado" in c else "—"
        if "evidencias" in c:
            v, n = c["evidencias"]
            if len(v) != len(n):
                ev = f"el JSON tenía {len(v)}, el PDF tiene {len(n)}"
            else:
                tipos = sorted({tipo_de_cambio(a, b) for a, b in zip(v, n) if a != b})
                ev = "; ".join(tipos)
        else:
            ev = "—"
        w(f"| `{c['codigo_dba']}` | {c['pagina']} | {celda(enun)} | {celda(ev)} |")
    w("")
    w("### 3.3 Donde el texto del PDF no dice lo que la página muestra")
    w("")
    w("En estos casos la capa de texto del PDF (lo que un programa puede leer) no coincide con la")
    w("página impresa, y se corrigió mirando la página. Solo tocan espacios, un salto de línea o una")
    w("ligadura: ninguna palabra. Están escritas en `CORRECCIONES`, dentro del script, y el verificador")
    w("comprueba cada una.")
    w("")
    w("| DBA | Dónde | El PDF trae | Se copia | Página | Por qué |")
    w("|---|---|---|---|---|---|")
    for c in corregidas:
        w(f"| `{c['codigo_dba']}` | {c['campo']} | «{celda(c['pdf'])}» | «{celda(c['corregido'])}» | "
          f"{c['pagina']} | {celda(c['razon'])} |")
    w("")
    w("## 4. Qué quedó dudoso")
    w("")
    w("No se adivinó. Cada uno está marcado en el registro (campo `dudoso`):")
    w("")
    for r in dudosos:
        for d in r["dudoso"]:
            if not d.startswith("ejemplo:"):
                w(f"- **`{r['codigo_dba']}`** (p. {r['pagina']}): {d}")
    w("")
    w("Los ejemplos dudosos están en la sección 8.")
    w("")
    w("Además, cosas del propio PDF que se copiaron tal cual y conviene que el equipo conozca:")
    w("")
    w("- **Erratas del documento oficial**, conservadas: «dados en en América» (`CS-07-06`) y «con")
    w("  los se cuenta» (`CS-08-08`, evidencia 2). Copiar exacto incluye sus errores.")
    w("- **Superíndices y subíndices** quedan como un carácter normal pegado a su palabra: «dm3»")
    w("  (decímetro cúbico, `MAT-08-05`) y «H2O» (`CN-06-03`). Mostrarlos como ³ y ₂ es una")
    w("  decisión de presentación para la interfaz.")
    w("- **Evidencias repetidas por el MEN:** algunas evidencias tienen las mismas palabras en DBA")
    w("  distintos (sobre todo en Matemáticas). El verificador comprueba que el PDF las imprime bajo")
    w("  cada uno: no es un error de extracción.")
    particion = [c[2] for c in CORRECCIONES if c[5] == PARTICION]
    reales = [g for g in guiones if not any(p.split("-")[0] in g["antes"] and p.split("-")[1][:3]
                                            in g["despues"][:6] for p in particion)]
    w("- **Guiones al final de un renglón:** se unen sin espacio a la línea siguiente. Son")
    w("  guiones reales (" + ", ".join(f"«{g['antes'].split()[-1]}{g['despues'].split()[0]}»"
                                     for g in reales) + ");")
    w("  los de partición de palabra («" + "», «".join(particion) + "») se corrigieron (3.3).")
    w("")
    w("## 5. Conteos finales, según el PDF")
    w("")
    w("No se forzó que sumaran 342: es lo que hay en los documentos.")
    w("")
    w("| Área | " + " | ".join(f"{g}°" for g in range(1, 12)) + " | Total |")
    w("|---|" + "---|" * 12)
    for a in AREAS:
        fila = [por_area_grado[(a[0], g)] for g in range(1, 12)]
        w(f"| {a[1]} ({a[0]}) | " + " | ".join(map(str, fila)) + f" | **{sum(fila)}** |")
    w(f"| **Total** | " + " | ".join(str(sum(por_area_grado[(a[0], g)] for a in AREAS))
                                     for g in range(1, 12)) + f" | **{len(catalogo)}** |")
    w("")
    w("Como estaban en el JSON viejo, para comparar:")
    w("")
    w("| Área | " + " | ".join(f"{g}°" for g in range(1, 12)) + " | Total |")
    w("|---|" + "---|" * 12)
    for a in AREAS:
        fila = [viejo_ag[(a[0], g)] for g in range(1, 12)]
        w(f"| {a[1]} | " + " | ".join(map(str, fila)) + f" | {sum(fila)} |")
    w("")
    w("Documentos (ADR-033): " + "; ".join(f"{a[1]} **{a[4]}** (`{a[3]}`)" for a in AREAS) + ".")
    w("")
    w("## 6. Cómo se hizo y cómo se comprueba")
    w("")
    w("- **Cómo se lee el PDF** (`construir_catalogo.py`). El grado sale del encabezado de cada")
    w("  página. Las palabras se arman siguiendo el orden en que el PDF guarda los caracteres, con los")
    w("  espacios que el PDF trae; donde no los trae, un hueco del ancho de un espacio también separa.")
    w("  Cada parte del DBA se reconoce por su tamaño de letra: el número (~26 pt), el enunciado")
    w("  (11 pt), los títulos «Evidencias de aprendizaje» y «Ejemplo», y cada evidencia por su viñeta.")
    w("  Una evidencia puede seguir en la otra columna o en la página siguiente.")
    w("- **Cómo se comprueba** (`_verificar_catalogo.py`). Con otro programa (`pdftotext`, de")
    w("  poppler), para no depender del lector que armó el catálogo: formato y unicidad del código,")
    w("  numeración sin huecos, enunciado y evidencias literales en su página (las letras en orden, sin")
    w("  los espacios), grado igual al del encabezado, cada evidencia en un solo DBA, que los números")
    w("  de DBA impresos en cada página sean exactamente los del catálogo, y la versión de cada")
    w("  documento. Desde el encargo 05, también el ejemplo: cada párrafo tiene que estar en sus")
    w("  páginas como renglones completos (así se salta las figuras sin dejar pasar una palabra")
    w("  cambiada). Al final introduce nueve errores a propósito en copias en memoria (dos sobre")
    w("  ejemplos: una palabra cambiada y el ejemplo de otro DBA) y comprueba que los atrapa todos.")
    w("- **Lo que el verificador anota sin que sea falla:** textos que siguen en la otra columna o")
    w("  en la página siguiente (se aceptan solo si el corte cae justo en un borde de renglón);")
    w("  textos cuyo espaciado no coincide con el de poppler, que lee distinto las palabras que el")
    w("  PDF separa solo por posición (son los de 3.3 y casos como «mujeres, derechos», donde el PDF")
    w("  sí trae el espacio); y las evidencias que el MEN repite en varios DBA. Las dos observaciones")
    w("  que reporta son `MAT-11-09` y `MAT-11-10`, sin encabezado de grado (sección 4).")
    w("- **Lo que el verificador no puede ver:** una palabra que esté en la capa de texto del PDF pero")
    w("  no impresa en la página (pasó una vez: un «con» de una columna aparecía en la otra; se")
    w("  encontró comparando con la página impresa y con el JSON viejo, y se corrigió el lector). Las")
    w("  diferencias con el JSON viejo se revisaron una por una, y las de Ciencias Sociales 3°, 6°, 7°")
    w("  y 8° se confirmaron mirando la página renderizada.")
    w("")
    w("## 7. Notas para la auditoría completa (A12)")
    w("")
    w("- **El ejemplo de cada DBA** se copió en el encargo 05: sección 8.")
    w("- **Notas al pie:** hay llamadas a nota en algunos títulos «Ejemplo» de Matemáticas (páginas")
    w("  " + ", ".join(str(o["pagina"]) for o in observaciones if "Ejemplo" in o.get("texto", "")) + ")")
    w("  y en el enunciado de `MAT-04-02`. El catálogo no tiene dónde guardar notas.")
    w("- **Las direcciones del JSON viejo** apuntan a rutas de Colombia Aprende de 2022; las vigentes")
    w("  son las de ADR-033.")
    w("")
    informe_ejemplos(w, catalogo, revision, nombres)
    w("## Anexo · cada diferencia de texto con el JSON viejo")
    w("")
    w("Formato: «…texto del JSON…» → «…texto del PDF…». Solo el primer par de diferencias de cada")
    w("texto; el resto, en el catálogo.")
    w("")
    for c in cambios:
        if "enunciado" in c:
            w(f"- `{c['codigo_dba']}` enunciado: {celda(diferencia(*c['enunciado']))}")
        if "evidencias" in c:
            v, n = c["evidencias"]
            if len(v) != len(n):
                w(f"- `{c['codigo_dba']}` evidencias: el JSON tenía {len(v)}, el PDF tiene {len(n)}.")
            else:
                for k, (a, b) in enumerate(zip(v, n), 1):
                    if a != b:
                        w(f"- `{c['codigo_dba']}` evidencia {k}: {celda(diferencia(a, b))}")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    catalogo, cambios, guiones, observaciones, sin_par, corregidas, revision = construir()
    catalogo.sort(key=lambda r: ([a[0] for a in AREAS].index(r["codigo_area"]),
                                 r["grado"], r["numero"]))
    cabecera = dict(
        generado_por="data/curriculo-men/catalogo/construir_catalogo.py",
        fuente="Los PDF oficiales de data/curriculo-men/pdfs/ (ADR-033). El texto se copia "
               "tal cual; solo se normalizan espacios y saltos de línea.",
        documentos=[dict(codigo_area=a[0], area=a[1], archivo=a[3], version=a[4]) for a in AREAS],
        total_dba=len(catalogo),
    )
    with open(os.path.join(AQUI, "catalogo_dba.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(dict(_meta=cabecera, dba=catalogo), fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    viejos = [r for r in json.load(open(JSON_VIEJO, encoding="utf-8"))["records"] if r["tipo"] == "DBA"]
    with open(os.path.join(AQUI, "informe-correccion.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(generar_informe(catalogo, cambios, guiones, observaciones, corregidas, viejos, revision))
    if os.environ.get("CATALOGO_CACHE"):        # para revisar a mano al desarrollar
        with open(os.path.join(os.environ["CATALOGO_CACHE"], "construccion.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(dict(cambios=cambios, guiones=guiones, observaciones=observaciones,
                           sin_par=sin_par, correcciones=corregidas, revision_ejemplos=revision),
                      fh, ensure_ascii=False, indent=1)
    print(f"{len(catalogo)} DBA · {len(cambios)} con cambios respecto del JSON viejo · "
          f"{len(guiones)} guiones de fin de línea · {len(observaciones)} observaciones · "
          f"{len(sin_par)} sin pareja")
