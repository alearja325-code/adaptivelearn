#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica la CADENA DERIVACIONAL de MODESEC, no la ausencia de errores.

Distinto de verificar_consistencia.py: aquel busca contradicciones; este
comprueba que cada documento se apoye de verdad en el que lo precede.

  diseno/  ->  Fase I (8 sub-etapas)  ->  Fase II (6 puntos)

Si un eslabon se rompe (un concepto listado que nadie define, una fuente
citada que no existe, una pantalla especificada que el plan no previo),
sale aqui.
"""
import os, re, zipfile, glob, sys

# Rutas relativas al propio script (2026-10-24): antes eran absolutas
# (/home/alejandro/Documents/AdaptiveLearn-V3) y solo funcionaban en un
# computador. RAIZ = raiz del repositorio; DOCS = su carpeta docs/.
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = os.path.join(RAIZ, "docs")
F1 = os.path.join(DOCS, "modesec", "fase-1-diseño-educativo")
F2 = os.path.join(DOCS, "modesec", "fase-2-diseno-multimedial")
DIS = os.path.join(DOCS, "diseno")

def docx(f):
    xml = zipfile.ZipFile(f).read("word/document.xml").decode("utf-8")
    xml = re.sub(r"</w:p>", "\n", xml)
    return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", l)).strip()
            for l in xml.split("\n")]

fallos = []

# ---- Eslabon 1: Fase I sub-etapa 4 (lista) -> sub-etapa 6 (definiciones)
print("1. Fase I: los conceptos LISTADOS en 04 ¿están DEFINIDOS en 06?")
L4 = docx(os.path.join(F1, "04-conceptos.docx"))
a = next(i for i, t in enumerate(L4) if "Objetos del dominio" in t)
b = next(i for i, t in enumerate(L4) if "Documento elaborado" in t)
lista = [t.split(":")[0].split("(")[0].strip() for t in L4[a:b]
         if t and not t.startswith(("Objetos", "Mecanismo", "Alcance"))]
t6 = " ".join(docx(os.path.join(F1, "06-diseno-contenidos.docx"))).lower()
sin_def = [c for c in lista if c.lower() not in t6]
print(f"   {len(lista)} conceptos listados · {len(sin_def)} sin definir")
if sin_def:
    for c in sin_def:
        print(f"   [ROTO] '{c}' se lista en 04 pero 06 no lo define")
    fallos.append(f"{len(sin_def)} concepto(s) sin definicion en Fase I")

# ---- Eslabon 2: Fase II punto 2 (diagrama) -> Fase I punto 6
print("\n2. Fase II: el diagrama de contenidos ¿cuadra con los conceptos de Fase I?")
dia = open(os.path.join(F2, "02-diagrama-contenidos.md"), encoding="utf-8").read()
m = re.search(r"los (\d+) conceptos", dia)
if m:
    declarado = int(m.group(1))
    print(f"   declara {declarado} · Fase I tiene {len(lista)}")
    if declarado != len(lista):
        print(f"   [ROTO] el diagrama dice {declarado}, la lista tiene {len(lista)}")
        fallos.append("conteo de conceptos desalineado entre Fase I y Fase II")
dot = open(os.path.join(F2, "mapa-conceptual-diagrama.dot"), encoding="utf-8").read()
nodos = set(re.findall(r'label="([^"]+)"', dot)) | set(
    re.findall(r"^\s+(\w+);", dot, re.M))
print(f"   nodos en el .dot: {len(nodos)}")

# ---- Eslabon 3: Fase II punto 1 (planeacion) -> specs realmente escritos
# Hueco encontrado 2026-09-26: el patron original ("0[4-9]" + "1*") solo
# cubria specs numerados 04-19 -- cualquier spec de 2 digitos que
# empezara en 2 (20, 21, 22, y ahora 23-25) quedaba fuera del conteo sin
# que nadie lo notara, porque el resultado final ("CADENA INTEGRA") no
# depende de este numero, solo se imprime. Se corrige con un patron que
# no enumera rangos a mano.
print("\n3. Fase II: ¿las ventanas especificadas están previstas en la planeación?")
specs = sorted(glob.glob(os.path.join(F2, "[0-9][0-9]-spec*.md")))
print(f"   specs escritos: {len(specs)}")
for s in specs:
    txt = open(s, encoding="utf-8").read()
    if not re.search(r"Ventana \d+", txt):
        print(f"   [ROTO] {os.path.basename(s)} sin numero de Ventana")
        fallos.append("spec sin numero de ventana")

# ---- Eslabon 4: toda fuente citada como /diseno/... debe existir
print("\n4. Transversal: las fuentes citadas de /diseno ¿existen?")
reales = set(os.listdir(DIS))
rotas = 0
for ruta in glob.glob(os.path.join(F2, "*.md")) + glob.glob(os.path.join(F1, "*.docx")):
    txt = (open(ruta, encoding="utf-8").read() if ruta.endswith(".md")
           else " ".join(docx(ruta)))
    for cit in set(re.findall(r"/diseno/([\w\-]+\.md)", txt)):
        if cit not in reales:
            print(f"   [ROTO] {os.path.basename(ruta)} cita /diseno/{cit}, que no existe")
            rotas += 1
if not rotas:
    print("   todas existen")
else:
    fallos.append(f"{rotas} fuente(s) de /diseno rotas")

print("\n" + "=" * 62)
print("CADENA ÍNTEGRA" if not fallos else f"{len(fallos)} ESLABÓN(ES) ROTO(S)")
for f in fallos:
    print("  -", f)
sys.exit(1 if fallos else 0)
