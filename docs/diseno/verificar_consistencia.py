#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detector de inconsistencias entre documentos de AdaptiveLearn.

Motivo: la causa raiz de casi todas las inconsistencias de este proyecto
es siempre la misma -- un ADR reemplaza a otro, y los documentos que
citaban la decision vieja nunca se actualizan. Eso NO se encuentra
releyendo (ya se comprobo varias veces); se encuentra rastreando, para
cada reemplazo, los terminos concretos que quedaron obsoletos.

Barre .md y .docx en:
  diseno/ · fase-1-diseño-educativo/ · fase-2-diseno-multimedial/

No decide por su cuenta: reporta candidatos con archivo:linea para que
un humano triage. Marca [hist] las lineas que parecen contexto
historico legitimo ("antes decia...", "se retira", "reemplaza a").
"""
import os, re, sys, zipfile, io

# Rutas relativas al propio script (2026-10-24): antes eran absolutas
# (/home/alejandro/Documents/AdaptiveLearn-V3) y solo funcionaban en un
# computador. RAIZ = raiz del repositorio; DOCS = su carpeta docs/.
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = os.path.join(RAIZ, "docs")
CARPETAS = [
    os.path.join(DOCS, "diseno"),
    os.path.join(DOCS, "modesec", "fase-1-diseño-educativo"),
    os.path.join(DOCS, "modesec", "fase-2-diseno-multimedial"),
]

# Terminos que un ADR posterior dejo obsoletos.
# (patron, por_que, adr_que_lo_reemplaza)
OBSOLETOS = [
    (r"brecha\s+extendida",           "categoria eliminada", "ADR-017"),
    (r"brecha\s+aislada",             "categoria eliminada", "ADR-017"),
    (r"brecha\s+detectada",           "nombre descartado por afirmar certeza", "ADR-017"),
    (r"umbrales?.{0,40}(ajusta|define|decide)\s+el\s+docente",
                                      "los umbrales los fija el SISTEMA", "ADR-013"),
    (r"nunca\s+en\s+un\s+veredicto",  "ADR-018 SI calcula un veredicto por DBA", "ADR-018"),
    (r"base\s+de\s+6\b|6\s+items?\s+por\s+evidencia|banco.{0,20}\b6\b",
                                      "el banco subio de 6 a 12", "ADR-016"),
    (r"tope:?\s*3\s+items?|hasta\s+1\s+item\s+mas",
                                      "la regla es minimo 4 / tope 6", "ADR-016"),
    (r"(el\s+)?docente\s+decide.{0,40}cu[aá]nt[oa]s\s+[ií]tems",
                                      "lo decide el SISTEMA", "ADR-016"),
    (r"target_solo|taxonom[ií]a\s+SOLO",
                                      "SOLO fue retirado", "ADR-002"),
    (r"punto\s+de\s+aprendizaje",     "renombrado a 'evidencia'", "glosario"),
    (r"Resultados\s+generales",       "renombrado a 'Estado general'", "ADR-022"),
    (r"Resultados\s+por\s+evidencia", "renombrado a 'Estado por evidencia'", "ADR-022"),
    (r"[Íi]tem.{0,15}\bdistractor\b", "el distractor vive en Opcion", "ADR-020"),
    (r"tres\s+estados|3\s+estados",   "ahora son 4 (con 'sin concluir')", "ADR-022"),
    (r"no\s+concluyente\s+en\s+los\s+dem[aá]s\s+casos",
                                      "'los demas casos' ahora se parte en 2", "ADR-022"),
]

# Lineas que suenan a historial legitimo -> se marcan, no se acusan.
HISTORICO = re.compile(
    r"antes\b|reemplaza|se\s+retir|ya\s+no\b|descartad|obsolet|"
    r"correcci[oó]n|hist[oó]ric|super[aá]|se\s+fusion|versi[oó]n\s+anterior|"
    r"primer\s+borrador|dej[oó]\s+de|se\s+elimin|se\s+cambi|pas[oó]\s+de",
    re.I)

# Hueco encontrado 2026-10-21: estos dos maximos estaban escritos a mano
# (25, 16). Al agregar ADR-026/027 el chequeo las marco como
# "inexistentes" -- el error era del script, no de los documentos. Se
# leen ahora de los encabezados reales de cada archivo.
def _ultimo(archivo, prefijo):
    with open(os.path.join(DOCS, "diseno", archivo), encoding="utf-8") as f:
        nums = re.findall(r"^## %s-(\d{3})" % prefijo, f.read(), re.M)
    return max(int(n) for n in nums)

MAX_ADR = _ultimo("decisiones.md", "ADR")
MAX_QA = _ultimo("preguntas-abiertas.md", "QA")

# ADRs reemplazados: citarlos como fuente VIGENTE (sin nombrar al que los
# reemplaza) es un error, aunque el texto no use ninguna palabra obsoleta.
REEMPLAZADOS = {
    "ADR-009": ("ADR-016", "la cantidad de items la fija el sistema, no el docente; banco 6->12"),
    "ADR-018": ("ADR-022", "agrega el 4.o estado 'sin concluir', con precedencia"),
    # ADR-013 y ADR-014 se dejan FUERA a proposito: fueron reemplazados solo
    # en un punto (categorias / distractor) y siguen siendo la autoridad del
    # resto de su contenido, asi que citarlos no es un error por si mismo.
}


# Excepciones VERIFICADAS a mano el 2026-08-26. No es "bajar el liston":
# cada una se comprobo leyendo el contexto real y se documenta por que es
# legitima. Si mañana aparece un caso nuevo, salta -- solo se perdona lo
# que ya se reviso.
#   (archivo, motivo_que_dispara) -> por que es correcto que aparezca
EXCEPCIONES = {
    ("glosario.md", "renombrado a 'evidencia'"):
        "la entrada Evidencia explica su propia etimologia: 'se llamo punto "
        "de aprendizaje mientras...'. Es historia legitima del termino.",
    ("preguntas-abiertas.md", "renombrado a 'evidencia'"):
        "'Surgio en: definicion de punto de aprendizaje' es el registro de "
        "CUANDO nacio cada pregunta. Reescribirlo falsearia el historial.",
    ("preguntas-abiertas.md", "SOLO fue retirado"):
        "QA-007 trata SOBRE target_solo y ya esta marcada 'sin objeto'. El "
        "termino es su tema, no una afirmacion vigente.",
    ("06-diseno-contenidos.docx", "renombrado a 'evidencia'"):
        "dice 'renombrada de Punto de aprendizaje el 2026-08-07' -- etimologia.",
    ("06-diseno-contenidos.docx", "ahora son 4 (con 'sin concluir')"):
        "la fila es 'Resultado de evidencia': POR EVIDENCIA siguen siendo 3 "
        "estados. El 4.o (sin concluir) solo existe a nivel de DBA completo "
        "(ADR-022). Verificado leyendo la fila entera de la tabla.",
    ("08-diseno-aprendizaje.docx", "ahora son 4 (con 'sin concluir')"):
        "igual que el anterior: habla del resultado por evidencia y por "
        "estudiante, donde 3 es correcto.",
    ("01-analisis-necesidad-educativa.docx", "SOLO fue retirado"):
        "menciona los pivotes previos del proyecto como contexto historico.",
    ("13-spec-modal-reporte.md", "renombrado a 'Estado general'"):
        "aparece en 'Correcciones posteriores', el log de cambios del propio "
        "spec: registra el nombre viejo al documentar el renombrado.",
    ("13-spec-modal-reporte.md", "renombrado a 'Estado por evidencia'"):
        "misma razon que el anterior.",
    ("13-spec-modal-reporte.md", "categoria eliminada"):
        "'Correcciones posteriores' #9 documenta la fusion de ADR-017.",
    ("11-spec-vista-interna-materiales.md", "renombrado a 'Estado general'"):
        "nota de correccion que documenta el cambio.",
    ("11-spec-vista-interna-materiales.md", "categoria eliminada"):
        "nota de correccion: 'brecha extendida ya no existe (ADR-017...)'.",
    ("03-tokens-diseno.md", "categoria eliminada"):
        "la seccion 'Resuelto' cita los nombres viejos al explicar que se "
        "fusionaron. Es el registro del cambio.",
    ("03-tokens-diseno.md", "ahora son 4 (con 'sin concluir')"):
        "'se reemplazan por los 3 estados reales que si definimos hoy' habla "
        "de los 4 pasteles rechazados del sistema anterior.",
    ("11-spec-vista-interna-materiales.md", "ADR-018 reemplazado"):
        "esta en 'Correccion posterior 2': registra que el texto viejo no "
        "mencionaba la seccion 2.2. Es el log del cambio, no una afirmacion.",
    ("13-spec-modal-reporte.md", "ADR-018 reemplazado"):
        "esta en 'Correcciones posteriores' #13: documenta que ADR-018 "
        "formalizo el mecanismo en su momento. Historial, no vigencia.",
    ("modelo-conceptual.md", "el banco subio de 6 a 12"):
        "la fila YA dice 'base de 12 ... revisado desde 6' -- menciona el 6 "
        "justamente para dejar constancia del cambio.",
    ("04-spec-dashboard.md", "ahora son 4 (con 'sin concluir')"):
        "falso positivo del heuristico: los '3 estados' de esas 2 lineas son "
        "el Status Badge de progreso del Estudiante (No iniciado/En curso/"
        "Completado, agregado 2026-09-12) -- no tiene relacion con los 4 "
        "estados de Reporte que cubre ADR-022.",
    ("23-spec-toma-diagnostico.md", "ahora son 4 (con 'sin concluir')"):
        "falso positivo del heuristico, misma razon que el de "
        "04-spec-dashboard.md: los '3 estados' de esa nota son los de la "
        "pantalla de inicio de Toma del diagnostico (No iniciada/En curso/"
        "Completada, mismo Badge del Dashboard) -- no tiene relacion con los "
        "4 estados de Reporte que cubre ADR-022.",
}


def leer(ruta):
    if ruta.endswith(".md"):
        return io.open(ruta, encoding="utf-8", errors="ignore").read()
    if ruta.endswith(".docx"):
        try:
            xml = zipfile.ZipFile(ruta).read("word/document.xml").decode("utf-8", "ignore")
            xml = re.sub(r"</w:p>", "\n", xml)
            return re.sub(r"<[^>]+>", " ", xml)
        except Exception:
            return ""
    return ""


def archivos():
    for carpeta in CARPETAS:
        if not os.path.isdir(carpeta):
            print(f"  !! carpeta no encontrada: {carpeta}")
            continue
        for n in sorted(os.listdir(carpeta)):
            if n.endswith((".md", ".docx")) and not n.startswith("~$"):
                yield os.path.join(carpeta, n)


def rel(p):
    return os.path.relpath(p, RAIZ)


docs = list(archivos())
print(f"Documentos barridos: {len(docs)}")
for d in docs:
    print("   ", rel(d))

errores, avisos = [], []

# --- 1. terminos obsoletos ---
print("\n" + "=" * 66)
print("1. TERMINOS QUE UN ADR POSTERIOR DEJO OBSOLETOS")
print("=" * 66)
hits = 0
# decisiones.md es el REGISTRO historico de ADRs: su regla propia es
# "nunca se edita una decision vieja", asi que contiene los terminos
# obsoletos por diseño. Excluirlo no es bajar el liston, es no acusar
# al archivo cuyo trabajo es justamente conservar lo viejo.
SIN_CHEQUEO_TERMINOS = {"decisiones.md", "pendientes.md",
                        "verificar_consistencia.py"}
for ruta in docs:
    if os.path.basename(ruta) in SIN_CHEQUEO_TERMINOS:
        continue
    texto = leer(ruta)
    lineas = texto.splitlines()
    for i in range(len(lineas)):
        # ventana de 3 lineas: una frase partida por saltos de linea
        # tambien tiene que ser visible
        linea = " ".join(l.strip() for l in lineas[i:i+3])
        if not linea.strip():
            continue
        i_real = i + 1
        for patron, motivo, adr in OBSOLETOS:
            if re.search(patron, linea, re.I) and not re.search(patron, " ".join(l.strip() for l in lineas[max(0,i-1):i+2]), re.I):
                if (os.path.basename(ruta), motivo) in EXCEPCIONES:
                    break  # verificada a mano, ver EXCEPCIONES
                hist = bool(HISTORICO.search(linea))
                marca = "[hist]" if hist else "[!!!] "
                frag = re.sub(r"\s+", " ", linea.strip())[:96]
                print(f"{marca} {rel(ruta)}:{i_real}")
                print(f"        {frag}")
                print(f"        -> {motivo} ({adr})")
                (avisos if hist else errores).append((rel(ruta), i_real, motivo, adr))
                hits += 1
                break
if not hits:
    print("  (sin coincidencias)")

# --- 2. citas a ADR / QA inexistentes ---
print("\n" + "=" * 66)
print("2. CITAS A ADR / QA QUE NO EXISTEN")
print("=" * 66)
rotas = 0
for ruta in docs:
    texto = leer(ruta)
    for i, linea in enumerate(texto.splitlines(), 1):
        for m in re.finditer(r"ADR-(\d{3})", linea):
            if int(m.group(1)) > MAX_ADR or int(m.group(1)) == 0:
                print(f"[!!!]  {rel(ruta)}:{i} -> {m.group(0)} (el ultimo es ADR-{MAX_ADR:03d})")
                errores.append((rel(ruta), i, "ADR inexistente", m.group(0))); rotas += 1
        for m in re.finditer(r"QA-(\d{3})", linea):
            if int(m.group(1)) > MAX_QA or int(m.group(1)) == 0:
                print(f"[!!!]  {rel(ruta)}:{i} -> {m.group(0)} (el ultimo es QA-{MAX_QA:03d})")
                errores.append((rel(ruta), i, "QA inexistente", m.group(0))); rotas += 1
if not rotas:
    print("  (todas las citas resuelven)")

# --- 3. referencias a archivos ---
print("\n" + "=" * 66)
print("3. REFERENCIAS A ARCHIVOS QUE NO EXISTEN")
print("=" * 66)
# HUECO CORREGIDO: antes solo se indexaban las 3 carpetas de documentos,
# asi que TODA referencia a un archivo del backend o de fase-3 salia como
# "inexistente" -- 9 falsos positivos. Ahora se indexa el repo entero.
# 'NN-nombre.md' es un marcador de patron usado al DESCRIBIR el problema
# de referencias rotas, no una referencia real.
#
# 2026-09-17: V3 se separo de V2 (ver vision.md, "Historia de
# versiones") -- RAIZ ya no incluye AdaptiveLearn/mvp/. Las 3 lineas de
# abajo citan archivos que viven ahi a proposito (auditoria de V2 en
# ADR-012/QA-006/QA-007/QA-013, documentacion historica real, no un
# vinculo que deba seguir funcionando). No se ensancha RAIZ para volver
# a incluir mvp/ -- eso recuplaria V3 a la ubicacion de V2, justo lo que
# la separacion evito.
HISTORICOS_V2 = {
    "interaction_evidence_planner.py",  # mvp/backend/ -- QA-006/ADR-012
    "intervention_path.py",             # mvp/backend/ -- QA-007
    "ia_service.py",                    # mvp/backend/ -- ADR-012
    "curriculo_men_normalizado.json",   # mvp/backend/data/men_sources/normalized/ -- QA-007/QA-013
    "dba_matematicas_v2.txt",           # mvp/backend/data/men_sources/text/ -- cita textual del MEN
                                         # (ADR-018). Dato curricular, no codigo de V2 -- candidato a
                                         # copiarse dentro de V3 mas adelante para no depender de la
                                         # ubicacion de mvp/; no se hace ahora, fuera de alcance de hoy.
}
existentes = {"NN-nombre.md"} | HISTORICOS_V2
for base, dirs, files in os.walk(RAIZ):
    dirs[:] = [d for d in dirs if d not in
               {"venv", "node_modules", ".git", "__pycache__", ".respaldo-2026-08-26"}]
    existentes.update(files)
rotas_f = 0
for ruta in docs:
    texto = leer(ruta)
    for i, linea in enumerate(texto.splitlines(), 1):
        for m in re.finditer(r"`([\w\-\.ñáéíóú]+\.(?:md|json|py|txt))`", linea):
            if m.group(1) not in existentes:
                print(f"[!!!]  {rel(ruta)}:{i} -> {m.group(1)}")
                errores.append((rel(ruta), i, "archivo inexistente", m.group(1))); rotas_f += 1
if not rotas_f:
    print("  (todas las referencias resuelven)")

# --- 4. citas a ADR reemplazados, sin mencionar al sucesor ---
print("\n" + "=" * 66)
print("4. ADR REEMPLAZADOS, CITADOS COMO SI FUERAN VIGENTES")
print("=" * 66)
malas = 0
for ruta in docs:
    if os.path.basename(ruta) in ("decisiones.md", "pendientes.md",
                                  "verificar_consistencia.py"):
        continue
    lineas_r = leer(ruta).splitlines()
    for i in range(len(lineas_r)):
        # ventana de 3 lineas: el sucesor suele citarse en la linea siguiente
        linea = " ".join(l.strip() for l in lineas_r[max(0, i - 1):i + 2])
        i_r = i + 1
        for viejo_adr, (nuevo_adr, motivo) in REEMPLAZADOS.items():
            if viejo_adr not in lineas_r[i]:
                continue
            # si la misma linea nombra al sucesor o dice que fue reemplazado,
            # es narrativa historica legitima
            sucesores = re.findall(r"ADR-\d{3}", nuevo_adr)
            if any(x in linea for x in sucesores) or re.search(
                    r"reemplaz|revisad|super[aá]|ya no|antes\b|correcci[oó]n",
                    linea, re.I):
                continue
            # las excepciones verificadas a mano tambien valen para este chequeo
            if (os.path.basename(ruta), f"{viejo_adr} reemplazado") in EXCEPCIONES:
                continue
            frag = re.sub(r"\s+", " ", linea.strip())[:96]
            print(f"[!!!]  {rel(ruta)}:{i_r}")
            print(f"        {frag}")
            print(f"        -> {viejo_adr} fue reemplazado por {nuevo_adr}: {motivo}")
            errores.append((rel(ruta), i_r, f"{viejo_adr} reemplazado", nuevo_adr))
            malas += 1
if not malas:
    print("  (ninguna cita a un ADR reemplazado sin nombrar a su sucesor)")

# --- resumen ---
print("\n" + "=" * 66)
print(f"RESUMEN: {len(errores)} a revisar  ·  {len(avisos)} marcados como historial")
print("=" * 66)
if errores:
    print("\nA revisar, agrupado por archivo:")
    porarch = {}
    for a, i, motivo, ref in errores:
        porarch.setdefault(a, []).append((i, motivo, ref))
    for a in sorted(porarch):
        print(f"\n  {a}")
        for i, motivo, ref in porarch[a]:
            print(f"    linea {i}: {motivo} ({ref})")
sys.exit(0)
