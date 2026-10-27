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
  * Lo que no es enunciado ni evidencia (ejemplos, textos de las
    imágenes, títulos) se ignora: el ejemplo está fuera de alcance (QA-011).

El texto se copia tal cual. Lo único que se normaliza es el espacio: los
saltos de línea pasan a un espacio y los espacios repetidos a uno. Un guion
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


def paginas_del_pdf(archivo):
    """[(ancho, palabras, huecos)] por página. Si la variable CATALOGO_CACHE
    nombra una carpeta, guarda ahí lo extraído para no volver a leer el PDF
    (solo sirve para desarrollar: el resultado es el mismo)."""
    cache = os.environ.get("CATALOGO_CACHE")
    ruta = os.path.join(cache, archivo + ".chars.json") if cache else None
    if ruta and os.path.exists(ruta):
        crudas = json.load(open(ruta, encoding="utf-8"))
    else:
        with pdfplumber.open(os.path.join(PDFS, archivo)) as pdf:
            crudas = [(p.width, [{k: c[k] for k in ("text", "x0", "x1", "top", "fontname", "size")}
                                 for c in p.chars]) for p in pdf.pages]
        if ruta:
            os.makedirs(cache, exist_ok=True)
            json.dump(crudas, open(ruta, "w", encoding="utf-8"))
    paginas = []
    for ancho, chars in crudas:
        huecos = []
        paginas.append((ancho, palabras_de(chars, huecos), huecos))
    return paginas


def leer_area(codigo, archivo):
    """Recorre el PDF y devuelve los DBA tal como aparecen, en orden."""
    dbas, observaciones, encabezados = [], [], {}
    actual = None           # DBA que se está leyendo
    estado = None           # 'enunciado' | 'evidencias' | 'ejemplo' | None
    ultima = None           # (pagina, columna, top) de la última línea de evidencia
    grado_anterior = None
    for n, (ancho, palabras, huecos) in enumerate(paginas_del_pdf(archivo), 1):
        grado, texto_enc = grado_de(palabras)
        sin_encabezado = False
        if grado is None:
            con_dba = any(es_avantgarde(w) and w["size"] > 20 and TOPE_ENCABEZADO < w["top"] < TOPE_PIE
                          and re.fullmatch(r"\d{1,2}\.", w["text"]) for w in palabras)
            if not (con_dba and grado_anterior):
                continue              # portada, presentación, créditos
            grado, sin_encabezado = grado_anterior, True
            texto_enc = ""
            observaciones.append(dict(pagina=n, tipo="página con DBA y sin encabezado de grado",
                                      texto=f"se toma el grado de la página anterior: {grado}"))
        grado_anterior = grado
        encabezados[n] = texto_enc
        for c, col in enumerate(lineas_por_columna(ancho, palabras)):
            for seg in col:
                k = clase(seg)
                top = seg[0]["top"]
                if k == "vineta":
                    texto = " ".join(x["text"] for x in seg[1:])
                else:
                    texto = " ".join(x["text"] for x in seg)
                if k == "numero":
                    actual = dict(numero=int(texto[:-1]), grado=grado, pagina=n,
                                  enunciado_lineas=[], evidencias=[],
                                  paginas=[n], sin_encabezado=sin_encabezado)
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
                    estado = "ejemplo"
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
                # el resto -- ejemplo, textos de imágenes -- se ignora
    return dbas, observaciones, encabezados


# ------------------------------------------------------------ correcciones
# Donde la CAPA DE TEXTO del PDF no dice lo que la página IMPRESA muestra, y
# ningún programa puede saberlo solo. Cada una se verificó mirando la página
# renderizada. Solo tocan espacios, saltos de línea o una ligadura que el PDF
# dibuja pero no declara como texto: nunca una palabra.
# (codigo_dba, campo, texto como sale del PDF, texto corregido, página, razón)
CORRECCIONES = [
    ("CS-06-05", "evidencia 1", "geográ cos", "geográficos", 31,
     "la ligadura «fi» está dibujada pero el PDF no la declara como texto: queda un hueco"),
    ("CS-07-07", "enunciado", "Co mprende", "Comprende", 36,
     "hueco de diagramación dentro de la palabra, sin carácter de espacio"),
    ("MAT-02-01", "evidencia 2", "? +b = c.", "? + b = c.", 15,
     "la página muestra «+ b», como «a + b» en la línea anterior; la capa de texto no trae ese espacio"),
    ("MAT-09-06", "evidencia 1", "bidimen-sionales", "bidimensionales", 69,
     "guion de partición al final de la línea (la palabra se corta en dos renglones)"),
]

# Lo que no se puede resolver con certeza: se deja como está en el PDF y se
# marca. El informe lo explica uno por uno.
DUDOSOS = {
    "CS-08-08": "el enunciado está impreso sin espacios en el PDF oficial "
                "(«Comprendelaimportanciadelasasociaciones,», p. 41). Se copia así; la lectura "
                "obvia es «Comprende la importancia de las asociaciones,». Decide el equipo.",
    "MAT-04-02": "el enunciado tiene una llamada a nota al pie en superíndice después de "
                 "«(fraccionarios)»; queda como «(fraccionarios)1». La nota está en la misma "
                 "página (p. 30) y no se copia: el catálogo no tiene campo para notas.",
}


def corregir(registro):
    """Aplica CORRECCIONES. Falla si el texto a corregir no aparece tal cual:
    así, si cambia la lectura del PDF, nadie corrige a ciegas."""
    hechas = []
    for cod, campo, mal, bien, pagina, razon in CORRECCIONES:
        if cod != registro["codigo_dba"]:
            continue
        if campo == "enunciado":
            assert registro["enunciado"].count(mal) == 1, (cod, campo, mal)
            registro["enunciado"] = registro["enunciado"].replace(mal, bien)
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
    corregidas = []
    usados = set()
    for codigo, nombre, area_vieja, archivo, version in AREAS:
        print(f"leyendo {archivo} ...", file=sys.stderr)
        dbas, obs, encabezados = leer_area(codigo, archivo)
        for o in obs:
            o["area"] = codigo
        observaciones += obs
        del_area = [(i, r) for i, r in enumerate(viejos) if r["area"] == area_vieja]
        registros = []
        for d in dbas:
            cod = f"{codigo}-{d['grado']:02d}-{d['numero']:02d}"
            registro = dict(
                codigo_dba=cod, codigo_area=codigo, area=nombre, grado=d["grado"],
                numero=d["numero"],
                enunciado=unir(d["enunciado_lineas"], guiones, f"{cod} enunciado"),
                evidencias=[unir(e["lineas"], guiones, f"{cod} evidencia {i}")
                            for i, e in enumerate(d["evidencias"], 1)],
                documento=dict(archivo=archivo, version=version),
                pagina=d["pagina"],
                paginas_evidencias=[e["pagina"] for e in d["evidencias"]],
                encabezado_pagina=espacios(encabezados[d["pagina"]]),
                dudoso=(["la página no tiene encabezado de grado: se toma el de la página "
                         "anterior y la numeración que sigue"] if d["sin_encabezado"] else []),
                id_anterior=None,
            )
            if cod in DUDOSOS:
                registro["dudoso"].append(DUDOSOS[cod])
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
    return catalogo, cambios, guiones, observaciones, sin_par, corregidas


# --------------------------------------------------------------- informe
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


def generar_informe(catalogo, cambios, guiones, observaciones, corregidas, viejos):
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
    w("**Encargo 02** (`docs/encargos/02-catalogo-curricular-corregido.md`). **Archivo generado** por")
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
            w(f"- **`{r['codigo_dba']}`** (p. {r['pagina']}): {d}")
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
    w("- **Guiones al final de un renglón:** se unen sin espacio a la línea siguiente. Tres son")
    w("  guiones reales (" + ", ".join(f"«{g['antes'].split()[-1]}{g['despues'].split()[0]}»"
                                     for g in guiones if "bidimen" not in g["antes"]) + ");")
    w("  el de «bidimen-sionales» es partición de palabra y se corrigió (3.3).")
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
    w("  documento. Al final introduce siete errores a propósito en copias en memoria y comprueba que")
    w("  los atrapa todos.")
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
    w("## 7. Notas para la auditoría completa (A12) — fuera de este encargo")
    w("")
    w("- **El ejemplo de cada DBA** no se copió (QA-011). Al leer los PDF se vio que muchos ejemplos")
    w("  dependen de una imagen, una tabla o una fórmula (por ejemplo, Matemáticas 9°, `MAT-09-03`, y")
    w("  10°, `MAT-10-07`; Ciencias Sociales, con fotografías y sus créditos). El JSON viejo pegaba")
    w("  parte de esos ejemplos al final de la última evidencia; aquí se quitaron porque no son")
    w("  evidencia.")
    w("- **Notas al pie:** hay llamadas a nota en algunos títulos «Ejemplo» de Matemáticas (páginas")
    w("  " + ", ".join(str(o["pagina"]) for o in observaciones if "Ejemplo" in o.get("texto", "")) + ")")
    w("  y en el enunciado de `MAT-04-02`. El catálogo no tiene dónde guardar notas.")
    w("- **Las direcciones del JSON viejo** apuntan a rutas de Colombia Aprende de 2022; las vigentes")
    w("  son las de ADR-033.")
    w("")
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
    catalogo, cambios, guiones, observaciones, sin_par, corregidas = construir()
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
        fh.write(generar_informe(catalogo, cambios, guiones, observaciones, corregidas, viejos))
    if os.environ.get("CATALOGO_CACHE"):        # para revisar a mano al desarrollar
        with open(os.path.join(os.environ["CATALOGO_CACHE"], "construccion.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(dict(cambios=cambios, guiones=guiones, observaciones=observaciones,
                           sin_par=sin_par, correcciones=corregidas), fh, ensure_ascii=False, indent=1)
    print(f"{len(catalogo)} DBA · {len(cambios)} con cambios respecto del JSON viejo · "
          f"{len(guiones)} guiones de fin de línea · {len(observaciones)} observaciones · "
          f"{len(sin_par)} sin pareja")
