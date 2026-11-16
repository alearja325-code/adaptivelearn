"""Arma el censo de formato cerrado (QA-014) a partir de los dictámenes.

Encargo 05, Parte B. Los criterios son `docs/diseno/criterios-censo-formato-cerrado.md`
(aceptados, ADR-042). El juicio está en `dictamenes/*.txt`: una línea por evidencia,
escrita por la sesión de Claude del encargo 05 leyendo cada evidencia. Este script
NO juzga nada: lee esas líneas, las cruza con el catálogo y escribe

  censo_formato_cerrado.json   el dictamen de cada evidencia (lo carga el backend)
  informe-censo.md             las cifras, por área, grado, formato y regla
  muestra_validacion.md        la muestra para los dos validadores (criterios §5)

Ninguno de los tres se edita a mano: si un dictamen cambia, se cambia su línea en
`dictamenes/` y se vuelve a correr este script.

Formato de una línea de `dictamenes/`:
  CÓDIGO NÚMERO | DICTAMEN | SEÑAL | JUSTIFICACIÓN [| dudoso: RAZÓN]
DICTAMEN es SC (single_choice), MT (matching) u OR (ordering) si aplica, o N1 a
N5 si no aplica. SEÑAL es el verbo o la frase que decide.

Uso:  python3 generar_censo.py
"""
import collections
import hashlib
import json
import os
import random
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..", "..", "..")
CATALOGO = os.path.join(AQUI, "..", "catalogo", "catalogo_dba.json")
CRITERIOS = os.path.join(RAIZ, "docs", "diseno", "criterios-censo-formato-cerrado.md")
DICTAMENES = os.path.join(AQUI, "dictamenes")

AREAS = [("MAT", "Matemáticas"), ("LEN", "Lenguaje"), ("CN", "Ciencias Naturales"),
         ("CS", "Ciencias Sociales")]
FORMATOS = {"SC": "single_choice", "MT": "matching", "OR": "ordering"}
REGLAS = {
    "N1": "producir",
    "N2": "comunicar en vivo",
    "N3": "sostener una postura propia",
    "N4": "actuar en el mundo",
    "N5": "una actitud o disposición",
}
FECHA = "2026-11-10"
ESTADO = "propuesto-por-ia"     # pasa a "validado-por-muestreo" cuando el equipo valide (criterios §5)

# La muestra de validación (criterios §5): 10 evidencias al azar por área, con
# esta semilla, más todas las dudosas. Cambiar la semilla cambia la muestra:
# no se cambia después de que los validadores empiecen.
SEMILLA = 2026111005
POR_AREA = 10

# Las 20 evidencias que los criterios ya clasificaron a mano (§7): su dictamen,
# para compararlo con el del censo. Copiado de la tabla de §7.
PRUEBA_CRITERIOS = {
    ("MAT-04-11", 4): "SC", ("MAT-09-04", 1): "SC", ("MAT-03-05", 1): "SC",
    ("MAT-08-04", 4): "SC", ("MAT-11-09", 2): "N1",
    ("LEN-08-07", 3): "N1", ("LEN-07-01", 2): "SC", ("LEN-06-02", 1): "N1",
    ("LEN-03-07", 1): "N2", ("LEN-10-04", 2): "SC",
    ("CN-05-04", 3): "SC", ("CN-04-03", 3): "N4", ("CN-09-02", 1): "SC",
    ("CN-09-03", 1): "SC", ("CN-07-01", 3): "SC",
    ("CS-09-05", 2): "SC", ("CS-03-02", 4): "SC", ("CS-06-06", 1): "SC",
    ("CS-10-04", 4): "N3", ("CS-08-02", 2): "SC",
}


def leer_dictamenes():
    """[(codigo, numero, dictamen, señal, justificación, razón_dudoso o None, archivo, línea)]"""
    salida = []
    for codigo, _ in AREAS:
        ruta = os.path.join(DICTAMENES, f"{codigo}.txt")
        for n, linea in enumerate(open(ruta, encoding="utf-8"), 1):
            linea = linea.rstrip("\n")
            if not linea.strip() or linea.lstrip().startswith("#"):
                continue
            partes = [p.strip() for p in linea.split(" | ")]
            if len(partes) not in (4, 5):
                sys.exit(f"{codigo}.txt:{n}: se esperaban 4 o 5 campos separados por « | »")
            m = re.fullmatch(r"((?:MAT|LEN|CN|CS)-\d{2}-\d{2}) (\d{1,2})", partes[0])
            if not m:
                sys.exit(f"{codigo}.txt:{n}: «{partes[0]}» no es «CÓDIGO NÚMERO»")
            dictamen = partes[1]
            if dictamen not in FORMATOS and dictamen not in REGLAS:
                sys.exit(f"{codigo}.txt:{n}: dictamen «{dictamen}» desconocido")
            dudoso = None
            if len(partes) == 5:
                if not partes[4].startswith("dudoso: "):
                    sys.exit(f"{codigo}.txt:{n}: el quinto campo empieza con «dudoso: »")
                dudoso = partes[4][len("dudoso: "):]
            salida.append((m.group(1), int(m.group(2)), dictamen, partes[2], partes[3], dudoso,
                           f"{codigo}.txt", n))
    return salida


def version_criterios():
    contenido = open(CRITERIOS, "rb").read()
    return dict(archivo="docs/diseno/criterios-censo-formato-cerrado.md",
                estado="aceptados por Alejandro el 2026-11-10 (ADR-042)",
                sha256=hashlib.sha256(contenido).hexdigest())


def construir():
    catalogo = json.load(open(CATALOGO, encoding="utf-8"))["dba"]
    evidencias = {(r["codigo_dba"], i): (r, e) for r in catalogo
                  for i, e in enumerate(r["evidencias"], 1)}
    vistos, registros = set(), []
    for cod, num, dic, senal, just, dudoso, archivo, n in leer_dictamenes():
        if (cod, num) not in evidencias:
            sys.exit(f"{archivo}:{n}: {cod} #{num} no está en el catálogo")
        if (cod, num) in vistos:
            sys.exit(f"{archivo}:{n}: {cod} #{num} ya tiene dictamen")
        vistos.add((cod, num))
        r, texto = evidencias[(cod, num)]
        aplica = dic in FORMATOS
        registros.append(dict(
            codigo_dba=cod, numero_evidencia=num, area=r["codigo_area"], grado=r["grado"],
            evidencia=texto,
            aplica=aplica,
            formato=FORMATOS.get(dic),
            regla=f"{FORMATOS[dic]} · «{senal}»" if aplica else dic,
            senal=senal,
            justificacion=just,
            dudoso=dudoso is not None,
            motivo_dudoso=dudoso,
        ))
    faltan = sorted(set(evidencias) - vistos)
    if faltan:
        sys.exit(f"faltan {len(faltan)} evidencias sin dictamen, por ejemplo {faltan[:3]}")
    orden = {c: i for i, (c, _) in enumerate(AREAS)}
    registros.sort(key=lambda x: (orden[x["area"]], x["grado"], x["codigo_dba"], x["numero_evidencia"]))
    return catalogo, registros


def muestra(registros, semilla=SEMILLA, por_area=POR_AREA):
    """(al azar, dudosas): las claves (código, número) de la muestra de validación.
    10 al azar por área, de todas las evidencias del área, en el orden del censo;
    y aparte, todas las dudosas que no salieron al azar."""
    rnd = random.Random(semilla)
    al_azar = []
    for codigo, _ in AREAS:
        del_area = [(x["codigo_dba"], x["numero_evidencia"]) for x in registros if x["area"] == codigo]
        al_azar += sorted(rnd.sample(del_area, por_area))
    dudosas = [(x["codigo_dba"], x["numero_evidencia"]) for x in registros
               if x["dudoso"] and (x["codigo_dba"], x["numero_evidencia"]) not in al_azar]
    return al_azar, dudosas


# ------------------------------------------------------------------ salidas
def pct(a, b):
    return f"{100 * a / b:.0f} %" if b else "—"


def celda(t):
    return str(t).replace("|", "\\|").replace("\n", " ")


def escribir_json(registros):
    cabecera = dict(
        generado_por="data/curriculo-men/censo/generar_censo.py",
        fuente="Los dictámenes de data/curriculo-men/censo/dictamenes/ (una línea por evidencia), "
               "escritos por la sesión de Claude del encargo 05 aplicando los criterios a cada "
               "evidencia (ADR-042). El texto de la evidencia es el del catálogo.",
        estado=ESTADO,
        fecha=FECHA,
        criterios=version_criterios(),
        validacion=dict(muestra="muestra_validacion.md", semilla=SEMILLA, por_area=POR_AREA,
                        validadores=None, fecha=None),
        total=len(registros),
        aplican=sum(x["aplica"] for x in registros),
        dudosos=sum(x["dudoso"] for x in registros),
    )
    with open(os.path.join(AQUI, "censo_formato_cerrado.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(dict(_meta=cabecera, dictamenes=registros), fh, ensure_ascii=False, indent=1)
        fh.write("\n")


# Para el informe: los motivos de duda, agrupados (el primero que coincide)
GRUPOS_DUDA = [
    (r"contexto propio", "contexto propio: la respuesta depende de la vida del estudiante (su familia, su municipio)"),
    (r"justific", "«justifica»: entre «explica» (aplica) y «argumenta» (N3)"),
    (r"ortografía|puntuación|concordancia", "ortografía, puntuación y concordancia: elegir la forma correcta es reconocer, no escribir"),
    (r"ítem tendría que|propio estudiante|depende del estudiante|no fija sobre qué",
     "lo que se evalúa es del propio estudiante (sus hipótesis, sus ideas): la pregunta tendría que darlo"),
    (r"toma decisiones|«decide»", "«toma decisiones» o «decide» (señal de N3) con una respuesta correcta"),
    (r"proceso|método|algoritmo|exploración|indagación|gestos y dibujos",
     "la evidencia habla de un proceso o un método que la pregunta no observa; solo ve el resultado"),
    (r"escucha|oír", "escucha: hay que oír algo, y la pregunta es escrita"),
    (r"modelo", "«plantea modelos» o «modela»: cercano a «representa»"),
    (r"hábito", "buscar o consultar fuentes: una acción (N4) o un hábito (N5)"),
    (r"N3|valoración|propone", "cerca de N3: «propone» un valor, «evalúa», «análisis crítico», razones sobre un valor"),
    (r"comunica|indicaciones", "«comunica», «da orientaciones», «utiliza señales»: producir o elegir"),
    (r"sí aplicaría|sí se puede preguntar|que sí aplica|sí se podría",
     "evidencia compuesta: una parte aplicaría y otra no"),
]


def motivo_agrupado(motivo):
    for patron, grupo in GRUPOS_DUDA:
        if re.search(patron, motivo):
            return grupo
    return "otros (cada uno con su razón en el JSON)"


def escribir_informe(catalogo, registros):
    L = []
    w = L.append
    nombres = dict(AREAS)
    tot = len(registros)
    ap = [x for x in registros if x["aplica"]]
    por_area = {c: [x for x in registros if x["area"] == c] for c, _ in AREAS}

    w("# Informe del censo de formato cerrado (QA-014)")
    w("")
    w("**Encargo 05**, Parte B. **Archivo generado** por `generar_censo.py`: no se edita a mano.")
    w(f"**Estado: propuesto por IA, sin validar** (`{ESTADO}`, ADR-042). Fecha: {FECHA}.")
    w("Criterios aplicados: `docs/diseno/criterios-censo-formato-cerrado.md`, aceptados el 2026-11-10")
    w(f"(huella sha256 `{version_criterios()['sha256'][:16]}…`, en la cabecera del JSON).")
    w("")
    w("## 1. En una frase")
    w("")
    w(f"De las **{tot} evidencias** del catálogo, **{len(ap)} ({pct(len(ap), tot)}) se pueden diagnosticar")
    w(f"con una pregunta cerrada** y {tot - len(ap)} no. Por área: " + "; ".join(
        f"{nombres[c]} {sum(x['aplica'] for x in xs)} de {len(xs)} ({pct(sum(x['aplica'] for x in xs), len(xs))})"
        for c, xs in por_area.items()) + ".")
    w("")
    w("Es un juicio de IA, no del equipo: lo hizo la sesión de Claude del encargo 05, leyendo cada")
    w("evidencia y escribiendo su razón (`dictamenes/`). Antes de usarlo como dato del proyecto, dos")
    w("integrantes validan la muestra de `muestra_validacion.md` (criterios §5).")
    w("")
    w("## 2. La respuesta a QA-014: ¿alcanza el formato cerrado?")
    w("")
    bajas = [c for c, xs in por_area.items() if sum(x["aplica"] for x in xs) / len(xs) < 0.6]
    w("| Área | Evidencias | Aplican | % | No aplican |")
    w("|---|---|---|---|---|")
    for c, xs in por_area.items():
        a = sum(x["aplica"] for x in xs)
        w(f"| {nombres[c]} | {len(xs)} | {a} | **{pct(a, len(xs))}** | {len(xs) - a} |")
    w(f"| **Total** | {tot} | {len(ap)} | **{pct(len(ap), tot)}** | {tot - len(ap)} |")
    w("")
    w("**Respuesta:** en Matemáticas, Ciencias Naturales y Ciencias Sociales el formato cerrado")
    w("alcanza a la mayoría de las evidencias. **En Lenguaje la proporción es baja: algo más de la")
    w("mitad.** Casi la mitad de las evidencias de Lenguaje piden hablar, escuchar o escribir, y una")
    w("pregunta cerrada no las observa. Es lo que ADR-002 anticipaba. Consecuencia para el diseño:")
    w("en Lenguaje el diagnóstico automático cubre sobre todo la comprensión (leer, identificar,")
    w("inferir) y deja fuera la producción oral y escrita, que es una parte central del área. El")
    w("sistema no lo esconde: el Paso 2 muestra esas evidencias tachadas (`06-spec` §2.4), y qué hacer")
    w("con ellas en otra versión es QA-017.")
    if bajas:
        w("")
        w("Áreas por debajo del 60 %: " + ", ".join(nombres[c] for c in bajas) + ".")
    w("")
    w("### 2.1 Por grado")
    w("")
    w("Cuántas aplican de las que hay, por área y grado:")
    w("")
    w("| Área | " + " | ".join(f"{g}°" for g in range(1, 12)) + " |")
    w("|---|" + "---|" * 11)
    for c, xs in por_area.items():
        fila = []
        for g in range(1, 12):
            gx = [x for x in xs if x["grado"] == g]
            a = sum(x["aplica"] for x in gx)
            fila.append(f"{a}/{len(gx)}" if gx else "—")
        w(f"| {nombres[c]} | " + " | ".join(fila) + " |")
    w("")
    w("En los primeros grados de Ciencias Sociales muchas evidencias piden saber algo de la vida del")
    w("propio estudiante (su familia, su casa, su municipio): ver la sección 6.")
    w("")
    w("## 3. Con qué formato")
    w("")
    w("| Área | single_choice | matching | ordering |")
    w("|---|---|---|---|")
    for c, xs in por_area.items():
        f = collections.Counter(x["formato"] for x in xs if x["aplica"])
        w(f"| {nombres[c]} | {f['single_choice']} | {f['matching']} | {f['ordering']} |")
    f = collections.Counter(x["formato"] for x in ap)
    w(f"| **Total** | {f['single_choice']} | {f['matching']} | {f['ordering']} |")
    w("")
    w("`matching` y `ordering` son minoría, como esperaban los criterios (§7): se usan solo cuando la")
    w("evidencia nombra explícitamente dos conjuntos que emparejar (clasifica, diferencia… de…,")
    w("relaciona X con Y) o un orden (ordena, el orden de los eventos). Ante la duda, `single_choice`.")
    w("")
    w("## 4. Por qué no aplican: cada regla")
    w("")
    w("| Regla | Qué pide la evidencia | " + " | ".join(nombres[c] for c, _ in AREAS) + " | Total |")
    w("|---|---|" + "---|" * (len(AREAS) + 1))
    for regla, desc in REGLAS.items():
        cifras = [sum(1 for x in xs if x["regla"] == regla) for xs in por_area.values()]
        w(f"| **{regla}** | {desc} | " + " | ".join(map(str, cifras)) + f" | {sum(cifras)} |")
    w("")
    w("- **N1 (producir)** es la regla más usada en Matemáticas y Lenguaje: construir tablas y")
    w("  gráficas, proponer estrategias, escribir textos.")
    w("- **N2 (comunicar en vivo)** es casi toda de Lenguaje: hablar, leer en voz alta, conversar y")
    w("  **escuchar**. Las evidencias sobre lo que el estudiante escucha (un discurso, una voz) se")
    w("  dictaminaron N2 porque la pregunta del sistema es escrita: leer un texto cambia lo que la")
    w("  evidencia pide (ver la propuesta 7.2).")
    w("- **N3 (postura propia)** es sobre todo de Ciencias Sociales: «argumenta» (que los criterios")
    w("  fijan como no aplica), «propone acciones», «expresa sus opiniones».")
    w("- **N4 (actuar en el mundo)** incluye medir, experimentar y observar, y en Ciencias Sociales las")
    w("  evidencias de contexto propio (sección 6).")
    w("")
    w("## 5. DBA sin ninguna evidencia que aplique")
    w("")
    sin = []
    for r in catalogo:
        xs = [x for x in registros if x["codigo_dba"] == r["codigo_dba"]]
        if not any(x["aplica"] for x in xs):
            sin.append(r)
    w(f"**{len(sin)} DBA** quedan sin ninguna evidencia que admita pregunta cerrada. Según QA-012, **no")
    w("se pueden usar para crear una experiencia en esta versión**: el banco no tendría de dónde")
    w("generar preguntas. (Qué muestra la pantalla en ese caso es el vacío V-12.)")
    w("")
    w("| DBA | Enunciado | Evidencias | Reglas |")
    w("|---|---|---|---|")
    for r in sin:
        xs = [x for x in registros if x["codigo_dba"] == r["codigo_dba"]]
        reglas = ", ".join(f"{k} ×{v}" if v > 1 else k for k, v in
                           sorted(collections.Counter(x["regla"] for x in xs).items()))
        w(f"| `{r['codigo_dba']}` | {celda(r['enunciado'])} | {len(xs)} | {reglas} |")
    w("")
    por_area_sin = collections.Counter(r["codigo_area"] for r in sin)
    w("Por área: " + ", ".join(f"{nombres[c]} {por_area_sin[c]}" for c, _ in AREAS) + ".")
    w("")
    w("## 6. Dudosas")
    w("")
    dud = [x for x in registros if x["dudoso"]]
    w(f"**{len(dud)} evidencias** quedaron dictaminadas pero marcadas `dudoso`, con su razón. Van todas")
    w("a la validación (criterios §5). Por motivo:")
    w("")
    grupos = collections.Counter()
    for x in dud:
        grupos[motivo_agrupado(x["motivo_dudoso"])] += 1
    for k, v in grupos.most_common():
        w(f"- {k}: **{v}**")
    w("")
    w("### 6.1 Contexto propio (Ciencias Sociales, sobre todo 1° a 3°)")
    w("")
    w("Varias evidencias piden algo que solo sabe el estudiante: los cumpleaños de sus padres, de dónde")
    w("vino su familia, el croquis de su municipio, el manual de convivencia de su colegio. Una pregunta")
    w("generada para cualquier estudiante no conoce esa respuesta. Los criterios no tienen una regla")
    w("para esto: se dictaminaron **N4** (requieren observar o consultar su entorno) y se marcaron")
    w("dudosas. Ver la propuesta 7.1.")
    w("")
    w("## 7. Propuestas de ajuste a los criterios")
    w("")
    w("No se cambiaron los criterios (encargo 05, B.2). Estos patrones no quedan bien cubiertos y se")
    w("proponen para que el equipo decida:")
    w("")
    w("1. **Contexto propio.** Agregar una regla (por ejemplo **N6, contexto propio**: la respuesta")
    w("   depende de la vida o el lugar del estudiante) o decir que, si el docente escribe ese contexto")
    w("   al crear la experiencia (el municipio, el manual), aplica. Hoy se dictaminan N4 y dudosas.")
    w("2. **Escuchar.** Decidir si el sistema tendrá preguntas con audio. Si no, las evidencias de")
    w("   escucha son N2 (así quedaron). Si sí, varias pasarían a `single_choice`. Lo mismo, en menor")
    w("   medida, con las evidencias que necesitan una imagen en la pregunta (caricaturas, mapas,")
    w("   afiches): se dictaminaron como aplican, pero el banco solo puede generarlas si la pregunta")
    w("   puede llevar una imagen.")
    w("3. **«Justifica».** Nombrarlo en los criterios: como «explica» (aplica) cuando lo que se justifica")
    w("   es un hecho o un procedimiento matemático, o como «argumenta» (N3). Hoy aplica y queda dudoso.")
    w("4. **«Propone».** Los criterios lo ponen como señal de N3. En la práctica tiene tres usos: proponer")
    w("   un método propio (estrategias, procedimientos, patrones: se dictaminó **N1**), proponer una")
    w("   acción o una solución a un problema social (**N3**), y proponer un valor que se comprueba")
    w("   («propone números que satisfacen una igualdad»: aplica, dudoso). Conviene escribir los tres.")
    w("5. **Ortografía y puntuación.** Decidir si «escribe con la ortografía correcta» se puede observar")
    w("   eligiendo la palabra bien escrita (práctica común en pruebas como Saber) o si eso es solo")
    w("   reconocer (N1, como quedó).")
    w("6. **Orden de las reglas frente al ejemplo de N5.** Por el orden de revisión, «asume una postura")
    w("   crítica y respetuosa» sería N3; los criterios la ponen como ejemplo de N5. Se siguió el")
    w("   ejemplo. Conviene aclarar cuál manda.")
    w("7. **Evidencias compuestas con «argumenta» en segundo lugar** («Conjetura y argumenta», «Compara")
    w("   y argumenta»). Se aplicó §4: decide la acción principal y se aplica; «argumenta» queda sin")
    w("   cubrir y se dice en la justificación. Si el equipo prefiere que «argumenta» decida siempre,")
    w("   cambian unas 10.")
    w("")
    w("## 8. Frente a la prueba de los criterios (§7)")
    w("")
    w("Las 20 evidencias que los criterios clasificaron a mano se volvieron a leer y dictaminar, sin")
    w("copiar la tabla.")
    w("")
    distintas = []
    for (cod, num), esperado in PRUEBA_CRITERIOS.items():
        x = next(x for x in registros if (x["codigo_dba"], x["numero_evidencia"]) == (cod, num))
        obtenido = next(k for k, v in FORMATOS.items() if v == x["formato"]) if x["aplica"] else x["regla"]
        if obtenido != esperado:
            distintas.append((cod, num, esperado, obtenido, x))
    if not distintas:
        w("**Coinciden las 20.** El censo da el mismo dictamen que la tabla en todas, incluido")
        w("`LEN-06-02` #1 como N1 dudoso.")
    else:
        w(f"Coinciden {20 - len(distintas)} de 20. Las que difieren:")
        w("")
        for cod, num, esperado, obtenido, x in distintas:
            w(f"- `{cod}` #{num}: la tabla dice {esperado}, el censo {obtenido}. {x['justificacion']}")
    w("")
    w("## 9. Cómo se hizo y cómo se comprueba")
    w("")
    w("- **El juicio** está en `dictamenes/MAT.txt`, `LEN.txt`, `CN.txt` y `CS.txt`: una línea por")
    w("  evidencia, con el dictamen, la señal (el verbo o la frase que decide) y la justificación, que")
    w("  cita esa señal y la regla. Se escribió área por área, grado por grado, leyendo cada evidencia")
    w("  con el enunciado de su DBA. No se usó ninguna API de IA externa. Las decisiones de aplicación")
    w("  que se repiten (escuchar, contexto propio, experimentos como contexto) están anotadas al")
    w("  comienzo de cada archivo.")
    w("- **El script** `generar_censo.py` no juzga: cruza las líneas con el catálogo y escribe el JSON,")
    w("  este informe y la muestra.")
    w("- **El verificador** `_verificar_censo.py` comprueba que hay exactamente un dictamen por cada")
    w("  evidencia del catálogo, que `formato` es nulo si y solo si no aplica (RI-19), que toda")
    w("  justificación cita su regla, y que la muestra se puede volver a sacar igual con su semilla. Al")
    w("  final introduce errores a propósito y comprueba que los atrapa.")
    w("- **Lo que no garantiza nada de esto:** que el juicio sea correcto. Eso solo lo dice la")
    w("  validación del equipo (criterios §5).")
    w("")
    with open(os.path.join(AQUI, "informe-censo.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L))


def escribir_muestra(registros):
    al_azar, dudosas = muestra(registros)
    por_clave = {(x["codigo_dba"], x["numero_evidencia"]): x for x in registros}
    L = []
    w = L.append
    w("# Muestra de validación del censo de formato cerrado")
    w("")
    w("**Archivo generado** por `generar_censo.py`: no se edita a mano. Para marcar el acuerdo, copiar")
    w("este archivo (por ejemplo, `muestra_validacion-alejandro.md`) y marcar ahí.")
    w("")
    w("**Cómo se valida** (criterios §5): dos integrantes del equipo (propuestos: Alejandro y Jose),")
    w("**por separado**, leen cada evidencia y dicen si están de acuerdo con el dictamen: si aplica o")
    w("no, y con qué formato. **Si discrepan con más de 6 de las 40 al azar (15 %)**, los criterios se")
    w("corrigen y el censo se vuelve a correr. Si no, el censo pasa a «validado por muestreo». Las")
    w("dudosas se revisan todas, pero no cuentan para el umbral.")
    w("")
    w(f"**Semilla: `{SEMILLA}`**. Con ella, `generar_censo.py` saca siempre la misma muestra: "
      f"{POR_AREA} al azar por área (`random.Random({SEMILLA}).sample`, área por área en el orden")
    w("MAT, LEN, CN, CS, sobre las evidencias en el orden del censo). `_verificar_censo.py` lo comprueba.")
    w("")

    def bloque(clave, k):
        x = por_clave[clave]
        dic = f"aplica · `{x['formato']}`" if x["aplica"] else f"no aplica · {x['regla']}"
        w(f"### {k}. `{x['codigo_dba']}` #{x['numero_evidencia']}")
        w("")
        w(f"> {x['evidencia']}")
        w("")
        w(f"**Dictamen:** {dic}" + (" · **dudoso**" if x["dudoso"] else ""))
        w("")
        w(f"**Justificación:** {x['justificacion']}")
        if x["dudoso"]:
            w("")
            w(f"**Por qué es dudoso:** {x['motivo_dudoso']}")
        w("")
        w("- [ ] Validador 1 de acuerdo · si no, ¿qué dictamen?: ______")
        w("- [ ] Validador 2 de acuerdo · si no, ¿qué dictamen?: ______")
        w("")

    w(f"## 1. Las {len(al_azar)} al azar ({POR_AREA} por área)")
    w("")
    for k, clave in enumerate(al_azar, 1):
        bloque(clave, k)
    w(f"## 2. Las dudosas que no salieron al azar ({len(dudosas)})")
    w("")
    for k, clave in enumerate(dudosas, len(al_azar) + 1):
        bloque(clave, k)
    w("## 3. Resultado")
    w("")
    w("| | Validador 1 | Validador 2 |")
    w("|---|---|---|")
    w("| Nombre | | |")
    w("| Fecha | | |")
    w("| Desacuerdos en las 40 al azar | | |")
    w("| Desacuerdos en las dudosas | | |")
    w("")
    with open(os.path.join(AQUI, "muestra_validacion.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L))


if __name__ == "__main__":
    catalogo, registros = construir()
    escribir_json(registros)
    escribir_informe(catalogo, registros)
    escribir_muestra(registros)
    ap = sum(x["aplica"] for x in registros)
    print(f"{len(registros)} dictámenes · {ap} aplican · {sum(x['dudoso'] for x in registros)} dudosos")
