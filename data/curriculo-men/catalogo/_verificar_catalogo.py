"""Verifica catalogo_dba.json contra los PDF oficiales del MEN.

Encargo 02, sección 5. Para que la comprobación no dependa del programa que
armó el catálogo, este verificador NO usa su lector: lee las páginas con
`pdftotext` (poppler), otro programa distinto de pdfplumber.

Comprueba:
  1. Cada codigo_dba es único, tiene el formato ÁREA-GG-NN (RI-21) y dice el
     área, el grado y el número que el registro dice.
  2. En cada área y grado, los números van del 01 al N, sin huecos ni repetidos.
  3. El enunciado y cada evidencia aparecen LITERALMENTE en la página que el
     registro dice. Se comparan las letras en orden, sin los espacios: así
     cualquier palabra cambiada, agregada o quitada se detecta, y no se
     confunde un error de texto con uno de espaciado (en algunas páginas el
     PDF separa las palabras solo por posición, sin carácter de espacio, y
     cada programa lo lee distinto). Aparte, como nota, cuenta dónde el
     espaciado no coincide con el de poppler.
     Las correcciones declaradas en construir_catalogo.py (CORRECCIONES) se
     comprueban al revés: el texto "como sale del PDF" tiene que estar en la
     página, y el corregido en el catálogo.
  4. El grado de cada DBA es el del encabezado de su página.
  5. Cada evidencia pertenece a un solo DBA.
  6. (además) Todo DBA del PDF está en el catálogo, y nada más: los números
     grandes de cada página son exactamente los DBA que el catálogo pone ahí.
  7. (además) El documento y la versión de cada área son los de ADR-033.

Lo que no pasa pero está explicado como dudoso en el registro (campo
`dudoso`) se informa como observación, no como falla.

Al final se demuestra que el verificador SÍ atrapa errores: se introducen
errores a propósito en copias en memoria del catálogo y se comprueba que
cada uno se detecta. El archivo no se toca.

Uso:  python3 _verificar_catalogo.py
"""
import copy
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from construir_catalogo import CORRECCIONES        # noqa: E402  (solo los datos)

PDFS = os.path.join(AQUI, "..", "pdfs")
CATALOGO = os.path.join(AQUI, "catalogo_dba.json")

# ADR-033: la versión se lee del documento, no del nombre del archivo
DOCUMENTOS = {"MAT": ("dba_matematicas_v2.pdf", "V.2"), "LEN": ("dba_lenguaje_v2.pdf", "V.2"),
              "CN": ("dba_ciencias_naturales_v1.pdf", "V.1"),
              "CS": ("dba_ciencias_sociales_v2.pdf", "V.1")}

_cache = {}


def poppler(archivo, pagina, *opciones):
    clave = (archivo, pagina, opciones)
    if clave not in _cache:
        r = subprocess.run(["pdftotext", *opciones, "-f", str(pagina), "-l", str(pagina),
                            "-enc", "UTF-8", os.path.join(PDFS, archivo), "-"],
                           capture_output=True, text=True, check=True)
        _cache[clave] = r.stdout
    return _cache[clave]


def sin_espacios(texto):
    return re.sub(r"\s+", "", texto)


def espacios(texto):
    # un guion al final de una línea se une sin espacio a la siguiente
    return re.sub(r"\s+", " ", re.sub(r"(?<=\w)-\s+(?=\w)", "-", texto)).strip()


def texto_pagina(archivo, pagina):
    """Las dos lecturas de poppler: por posición (la normal) y en el orden en
    que el PDF guarda el texto (-raw). Una línea guardada al revés solo se lee
    bien por posición; un texto partido entre columnas, en orden."""
    return [poppler(archivo, pagina), poppler(archivo, pagina, "-raw")]


def grado_encabezado(archivo, pagina):
    t = sin_espacios(poppler(archivo, pagina, "-x", "0", "-y", "0", "-W", "700", "-H", "85", "-raw"))
    m = re.search(r"Grado(\d{1,2})[º°o]", t)
    return int(m.group(1)) if m else None


def numeros_grandes(archivo, pagina):
    """Los números de DBA: palabras "N." de más de 18 puntos de alto."""
    salida = []
    for m in re.finditer(r'<word xMin="[\d.]+" yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)">'
                         r'(\d{1,2})\.</word>', poppler(archivo, pagina, "-bbox")):
        if float(m.group(2)) - float(m.group(1)) > 18:
            salida.append(int(m.group(3)))
    return sorted(salida)


def renglones(texto):
    """El texto de una página sin espacios, y dónde empieza cada renglón."""
    juntos, cortes = "", {0}
    for ln in texto.split("\n"):
        juntos += sin_espacios(ln)
        cortes.add(len(juntos))
    return juntos, cortes


def partido(buscado, lecturas_a, lecturas_b):
    """¿Está el texto partido en dos trozos: el primero termina al final de un
    renglón de la página (lecturas_a) y el segundo empieza al principio de un
    renglón de la misma página o de la siguiente (lecturas_b)? Así se lee una
    evidencia que sigue en la otra columna o en la otra página. Exigir el
    corte justo en el borde de renglón impide que una palabra quitada en el
    medio pase inadvertida."""
    s = sin_espacios(buscado)
    for ta in lecturas_a:
        ja, ca = renglones(ta)
        for tb in lecturas_b:
            jb, cb = renglones(tb)
            for k in range(8, len(s) - 7):
                a, b = s[:k], s[k:]
                i = ja.find(a)
                fin_ok = False
                while i >= 0:
                    if i + k in ca:
                        fin_ok = True
                        break
                    i = ja.find(a, i + 1)
                if not fin_ok:
                    continue
                j = jb.find(b)
                while j >= 0:
                    if j in cb:
                        return True
                    j = jb.find(b, j + 1)
    return False


def correcciones_de(cod):
    return [c for c in CORRECCIONES if c[0] == cod]


def como_en_el_pdf(registro, campo, texto):
    """Deshace las correcciones declaradas: lo que se busca en la página es el
    texto tal como lo trae el PDF."""
    for cod, c_campo, mal, bien, *_ in correcciones_de(registro["codigo_dba"]):
        if c_campo == campo:
            texto = texto.replace(bien, mal)
    return texto


def paginas_de(archivo):
    if ("pdfinfo", archivo) not in _cache:
        _cache[("pdfinfo", archivo)] = int(re.search(r"Pages:\s+(\d+)", subprocess.run(
            ["pdfinfo", os.path.join(PDFS, archivo)], capture_output=True, text=True).stdout).group(1))
    return _cache[("pdfinfo", archivo)]


def verificar(catalogo):
    """Devuelve (comprobaciones, fallas, observaciones, notas)."""
    hechas, fallas, observaciones, notas = [], [], [], []

    def chk(cond, msg, registro=None, motivo=None):
        """Una comprobación. Si falla pero el registro lo explica como dudoso
        (motivo aparece en su campo `dudoso`), es observación, no falla."""
        if cond:
            hechas.append(msg)
        elif registro and motivo and any(motivo in d for d in registro.get("dudoso", [])):
            observaciones.append(f"{msg} — explicado como dudoso en el registro")
        else:
            fallas.append(msg)

    dba = catalogo["dba"]

    # ------------------------------------------------------------------ 1
    formato = re.compile(r"(MAT|LEN|CN|CS)-(0[1-9]|1[01])-(0[1-9]|[1-9]\d)")
    codigos = Counter(r["codigo_dba"] for r in dba)
    for r in dba:
        cod = r["codigo_dba"]
        m = formato.fullmatch(cod)
        chk(m is not None, f"{cod}: formato ÁREA-GG-NN (RI-21)")
        if m:
            chk((m.group(1), int(m.group(2)), int(m.group(3))) ==
                (r["codigo_area"], r["grado"], r["numero"]),
                f"{cod}: el código dice el área, el grado y el número del registro")
        chk(codigos[cod] == 1, f"{cod}: código único")

    # ------------------------------------------------------------------ 2
    por_grado = defaultdict(list)
    for r in dba:
        por_grado[(r["codigo_area"], r["grado"])].append(r["numero"])
    for (area, grado), nums in sorted(por_grado.items()):
        chk(sorted(nums) == list(range(1, len(nums) + 1)),
            f"{area} {grado}°: números del 01 al {len(nums):02d}, sin huecos ni repetidos "
            f"(hay {sorted(nums)})")

    # ------------------------------------------------------------------ 3
    for r in dba:
        archivo = r["documento"]["archivo"]
        partes = [("enunciado", r["enunciado"], r["pagina"])]
        partes += [(f"evidencia {i}", e, p) for i, (e, p)
                   in enumerate(zip(r["evidencias"], r["paginas_evidencias"]), 1)]
        for campo, texto, pagina in partes:
            buscado = como_en_el_pdf(r, campo, texto)
            lecturas = texto_pagina(archivo, pagina)
            seguido = any(sin_espacios(buscado) in sin_espacios(t) for t in lecturas)
            en_dos = False
            if not seguido:
                siguiente = texto_pagina(archivo, pagina + 1) if pagina + 1 <= paginas_de(archivo) else []
                seguido = en_dos = partido(buscado, lecturas, lecturas + siguiente)
                if en_dos:
                    notas.append(f"{r['codigo_dba']} {campo}: sigue en la otra columna o la otra página")
            chk(seguido, f"{r['codigo_dba']} {campo}: aparece literal en la página {pagina}")
            if not en_dos and not any(espacios(buscado) in espacios(t) for t in lecturas):
                notas.append(f"{r['codigo_dba']} {campo}: mismas letras, distinto espaciado que poppler")
        for cod, campo, mal, bien, pagina, razon in correcciones_de(r["codigo_dba"]):
            texto = r["enunciado"] if campo == "enunciado" else r["evidencias"][int(campo.split()[1]) - 1]
            chk(bien in texto and mal not in texto,
                f"{cod} {campo}: corrección declarada aplicada («{mal}» → «{bien}»)")
            chk(any(sin_espacios(mal) in sin_espacios(t) for t in texto_pagina(archivo, pagina)),
                f"{cod} {campo}: lo que se corrigió («{mal}») está así en la página {pagina}")

    # ------------------------------------------------------------------ 4
    for r in dba:
        g = grado_encabezado(r["documento"]["archivo"], r["pagina"])
        dice = f"{g}°" if g else "ninguno, la página no tiene encabezado"
        chk(g == r["grado"], f"{r['codigo_dba']}: grado del encabezado de la página {r['pagina']}: "
            f"{dice}", r, "encabezado")

    # ------------------------------------------------------------------ 5
    # El MEN repite a veces la misma evidencia, con las mismas palabras, en
    # DBA distintos. Eso es válido si el PDF la imprime bajo cada uno: en cada
    # página tiene que aparecer al menos tantas veces como DBA la reclaman
    # ahí. Si no, una evidencia de un DBA se copió a otro: falla.
    dueno = defaultdict(list)
    for r in dba:
        for e, p in zip(r["evidencias"], r["paginas_evidencias"]):
            dueno[sin_espacios(e)].append((r["codigo_dba"], r["documento"]["archivo"], p))
    mal_repetidas, repetidas = [], []
    for e, lugares in dueno.items():
        if len(lugares) < 2:
            continue
        repetidas.append(sorted(c for c, _, _ in lugares))
        for (archivo, p), n in Counter((a, p) for _, a, p in lugares).items():
            veces = max(sin_espacios(t).count(e) for t in texto_pagina(archivo, p))
            if veces < n:
                mal_repetidas.append(sorted(c for c, a, q in lugares if (a, q) == (archivo, p)))
    chk(not mal_repetidas, f"cada evidencia pertenece a un solo DBA ({len(dueno)} evidencias"
        + (f"; puestas en más de un DBA sin que el PDF las repita: {mal_repetidas}"
           if mal_repetidas else "") + ")")
    for grupo in repetidas:
        notas.append(f"evidencia que el PDF repite, igual, en {', '.join(grupo)}")
    for r in dba:
        chk(len(set(map(sin_espacios, r["evidencias"]))) == len(r["evidencias"]) and r["evidencias"],
            f"{r['codigo_dba']}: tiene evidencias, sin repetir")

    # ------------------------------------------------------------------ 6
    por_pagina = defaultdict(list)
    for r in dba:
        por_pagina[(r["documento"]["archivo"], r["pagina"])].append(r["numero"])
    for area, (archivo, _) in DOCUMENTOS.items():
        n = paginas_de(archivo)
        en_pdf = {p: numeros_grandes(archivo, p) for p in range(1, n + 1)}
        en_pdf = {p: v for p, v in en_pdf.items() if v}
        en_cat = {p: sorted(v) for (a, p), v in por_pagina.items() if a == archivo}
        dif = {p: (en_pdf.get(p), en_cat.get(p)) for p in set(en_pdf) | set(en_cat)
               if en_pdf.get(p) != en_cat.get(p)}
        chk(not dif, f"{area}: los {sum(map(len, en_pdf.values()))} números de DBA del PDF son "
            f"exactamente los del catálogo, página por página"
            + (f" (difieren, página: (PDF, catálogo): {dif})" if dif else ""))

    # ------------------------------------------------------------------ 7
    for r in dba:
        chk((r["documento"]["archivo"], r["documento"]["version"]) == DOCUMENTOS[r["codigo_area"]],
            f"{r['codigo_dba']}: documento y versión de ADR-033")

    return hechas, fallas, observaciones, notas


# ---------------------------------------------------------------- errores
def errores_a_proposito(catalogo):
    """Copias del catálogo, cada una con un error distinto, y la comprobación
    que tiene que atraparlo."""
    casos = []

    def caso(nombre, cambio, se_espera):
        c = copy.deepcopy(catalogo)
        cambio(c["dba"])
        casos.append((nombre, c, se_espera))

    def por_codigo(lista, cod):
        return next(r for r in lista if r["codigo_dba"] == cod)

    def palabra(lista):
        r = por_codigo(lista, "MAT-03-01")
        r["evidencias"][0] = r["evidencias"][0].replace("diagramas", "dibujos", 1)
    caso("una palabra cambiada en una evidencia (MAT-03-01: «diagramas» → «dibujos»)",
         palabra, "aparece literal")

    def quita(lista):
        r = por_codigo(lista, "LEN-05-02")
        r["enunciado"] = r["enunciado"].replace(" no ", " ", 1) if " no " in r["enunciado"] \
            else " ".join(r["enunciado"].split()[:-2] + r["enunciado"].split()[-1:])
    caso("una palabra quitada del enunciado (LEN-05-02)", quita, "aparece literal")

    def grado(lista):
        r = por_codigo(lista, "CN-02-01")         # el que el JSON viejo ponía en 1°
        r["grado"], r["codigo_dba"] = 1, "CN-01-05"
    caso("un DBA devuelto al grado equivocado (CN-02-01 → 1°, como en el JSON viejo)",
         grado, "grado del encabezado")

    def duplicada(lista):
        a, b = por_codigo(lista, "CS-04-01"), por_codigo(lista, "CS-04-02")
        b["evidencias"].append(a["evidencias"][0])
        b["paginas_evidencias"].append(a["paginas_evidencias"][0])
    caso("una evidencia puesta también en otro DBA (CS-04-01 → CS-04-02)",
         duplicada, "cada evidencia pertenece a un solo DBA")

    def codigo(lista):
        por_codigo(lista, "MAT-07-03")["codigo_dba"] = "MAT-7-3"
    caso("un código mal formado (MAT-7-3)", codigo, "formato ÁREA-GG-NN")

    def hueco(lista):
        lista.remove(por_codigo(lista, "LEN-09-04"))
    caso("un DBA que falta (sin LEN-09-04)", hueco, "sin huecos")

    def version(lista):
        for r in lista:
            if r["codigo_area"] == "CS":
                r["documento"]["version"] = "V.2"   # el error que corrigió ADR-033
    caso("Ciencias Sociales con la versión del nombre del archivo (V.2)", version,
         "documento y versión de ADR-033")
    return casos


def main():
    catalogo = json.load(open(CATALOGO, encoding="utf-8"))
    print("=" * 70)
    print(f"Catálogo de DBA contra los PDF — {len(catalogo['dba'])} DBA")
    print("=" * 70)
    hechas, fallas, observaciones, notas = verificar(catalogo)
    print(f"   {len(hechas)} comprobaciones correctas")
    for o in observaciones:
        print(f"   OBSERVACIÓN {o}")
    for f in fallas:
        print(f"   FALLA {f}")
    esp = [n for n in notas if "espaciado" in n]
    rep = [n for n in notas if "repite" in n]
    dos = [n for n in notas if "sigue en" in n]
    print(f"   nota: {len(dos)} textos siguen en la otra columna o la otra página "
          f"(se aceptan solo si el corte cae justo en un borde de renglón)")
    print(f"   nota: en {len(esp)} textos el espaciado no coincide con el de poppler "
          f"(mismas letras en el mismo orden; ver el informe)")
    print(f"   nota: {len(rep)} evidencias que el PDF repite, con las mismas palabras, en "
          f"DBA distintos (cada vez impresa bajo su DBA)")

    print()
    print("=" * 70)
    print("¿El verificador atrapa errores? Se introducen a propósito, en memoria")
    print("=" * 70)
    atrapados = 0
    casos = errores_a_proposito(catalogo)
    for nombre, copia, se_espera in casos:
        _, f, _, _ = verificar(copia)
        ok = any(se_espera in x for x in f)
        atrapados += ok
        print(f"   {'ATRAPADO ' if ok else 'NO ATRAPADO'} {nombre}")
        for x in [x for x in f if se_espera in x][:1]:
            print(f"             ↳ {x[:110]}")
    if atrapados != len(casos):
        fallas.append(f"el verificador no atrapó {len(casos) - atrapados} errores a propósito")
    print("   (el catálogo en disco no se modificó)")

    print()
    print("=" * 70)
    if fallas:
        print(f"RESULTADO: {len(hechas)} correctas, {len(fallas)} FALLAS, "
              f"{len(observaciones)} observaciones explicadas como dudosas")
        sys.exit(1)
    print(f"RESULTADO: {len(hechas)} comprobaciones, todas correctas; "
          f"{len(observaciones)} observaciones explicadas como dudosas; "
          f"{atrapados} de {len(casos)} errores a propósito atrapados.")
    print("=" * 70)


if __name__ == "__main__":
    main()
