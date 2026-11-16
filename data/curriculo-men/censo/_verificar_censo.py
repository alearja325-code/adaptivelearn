"""Verifica el censo de formato cerrado contra el catálogo y los criterios.

Encargo 05, Parte B.3. Comprueba:
  1. Hay exactamente un dictamen por cada evidencia del catálogo: ni falta ni
     sobra ninguna, ni hay dos para la misma, y el texto de la evidencia es el
     del catálogo.
  2. `formato` es nulo si y solo si la evidencia no aplica (RI-19), y cuando
     aplica es uno de los tres formatos de ADR-006.
  3. Toda justificación cita su regla: la que no aplica nombra su regla (N1 a
     N5), la que aplica nombra su formato; y `regla` dice lo mismo que
     `aplica` y `formato`.
  4. Un dictamen dudoso dice por qué; uno que no lo es, no.
  5. La cabecera dice el estado del censo (propuesto por IA o validado por
     muestreo), la fecha y la versión de los criterios, y esa versión es la del
     archivo de criterios de hoy.
  6. La muestra de `muestra_validacion.md` se puede volver a sacar igual con su
     semilla: las mismas evidencias, en el mismo orden, y todas las dudosas.
Al final introduce errores a propósito en copias en memoria y comprueba que
cada uno se detecta. Los archivos no se tocan.

Uso:  python3 _verificar_censo.py
"""
import copy
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from generar_censo import AREAS, muestra, version_criterios  # noqa: E402

CATALOGO = os.path.join(AQUI, "..", "catalogo", "catalogo_dba.json")
CENSO = os.path.join(AQUI, "censo_formato_cerrado.json")
MUESTRA = os.path.join(AQUI, "muestra_validacion.md")
FORMATOS = {"single_choice", "matching", "ordering"}
ESTADOS = {"propuesto-por-ia", "validado-por-muestreo"}


def claves_de_la_muestra(texto):
    """Las evidencias de muestra_validacion.md, en orden, y su semilla."""
    semilla = int(re.search(r"\*\*Semilla: `(\d+)`\*\*", texto).group(1))
    claves = [(m.group(1), int(m.group(2)))
              for m in re.finditer(r"^### \d+\. `((?:MAT|LEN|CN|CS)-\d{2}-\d{2})` #(\d+)$", texto, re.M)]
    return semilla, claves


def verificar(censo, catalogo, texto_muestra):
    hechas, fallas = [], []

    def chk(cond, msg):
        (hechas if cond else fallas).append(msg)

    d = censo["dictamenes"]
    meta = censo["_meta"]

    # ------------------------------------------------------------------ 1
    evidencias = {(r["codigo_dba"], i): e for r in catalogo for i, e in enumerate(r["evidencias"], 1)}
    claves = [(x["codigo_dba"], x["numero_evidencia"]) for x in d]
    repetidas = sorted({k for k in claves if claves.count(k) > 1}) if len(set(claves)) != len(claves) else []
    faltan = sorted(set(evidencias) - set(claves))
    sobran = sorted(set(claves) - set(evidencias))
    chk(not repetidas, f"ninguna evidencia tiene dos dictámenes{f' (repetidas: {repetidas[:3]})' if repetidas else ''}")
    chk(not faltan, f"toda evidencia del catálogo ({len(evidencias)}) tiene dictamen"
        + (f" (faltan {len(faltan)}: {faltan[:3]})" if faltan else ""))
    chk(not sobran, f"ningún dictamen es de una evidencia que no está en el catálogo"
        + (f" ({sobran[:3]})" if sobran else ""))
    distintas = [k for k, x in zip(claves, d) if k in evidencias and evidencias[k] != x["evidencia"]]
    chk(not distintas, "el texto de cada evidencia es el del catálogo"
        + (f" (distinto en {distintas[:3]})" if distintas else ""))

    # ------------------------------------------------------------------ 2
    for x in d:
        k = f"{x['codigo_dba']} #{x['numero_evidencia']}"
        chk(isinstance(x["aplica"], bool), f"{k}: aplica es verdadero o falso")
        chk((x["formato"] is None) == (not x["aplica"]),
            f"{k}: formato nulo si y solo si no aplica (RI-19)")
        if x["aplica"]:
            chk(x["formato"] in FORMATOS, f"{k}: el formato es uno de los de ADR-006")

    # ------------------------------------------------------------------ 3
    for x in d:
        k = f"{x['codigo_dba']} #{x['numero_evidencia']}"
        if x["aplica"]:
            chk(x["regla"].startswith(x["formato"] + " · «") and x["senal"] in x["regla"],
                f"{k}: la regla dice el formato y su señal")
            chk(x["formato"] in x["justificacion"], f"{k}: la justificación cita su formato ({x['formato']})")
        else:
            chk(re.fullmatch(r"N[1-5]", x["regla"] or "") is not None, f"{k}: la regla es una de N1 a N5")
            chk(re.search(rf"\b{x['regla']}\b", x["justificacion"]) is not None,
                f"{k}: la justificación cita su regla ({x['regla']})")
        chk(len(x["justificacion"]) >= 30 and "«" in x["justificacion"],
            f"{k}: la justificación cita la frase de la evidencia")

    # ------------------------------------------------------------------ 4
    for x in d:
        k = f"{x['codigo_dba']} #{x['numero_evidencia']}"
        chk(bool(x["motivo_dudoso"]) == x["dudoso"], f"{k}: un dudoso dice por qué, y solo un dudoso")

    # ------------------------------------------------------------------ 5
    chk(meta.get("estado") in ESTADOS, f"el estado del censo es uno de {sorted(ESTADOS)}")
    chk(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta.get("fecha") or "")), "la cabecera dice la fecha")
    chk(meta.get("criterios", {}).get("sha256") == version_criterios()["sha256"],
        "la versión de los criterios es la del archivo de criterios de hoy")
    chk(meta.get("total") == len(d) and meta.get("aplican") == sum(x["aplica"] for x in d),
        "los totales de la cabecera son los del censo")

    # ------------------------------------------------------------------ 6
    semilla, en_archivo = claves_de_la_muestra(texto_muestra)
    al_azar, dudosas = muestra(d, semilla)
    chk(semilla == censo["_meta"]["validacion"]["semilla"], "la semilla del archivo es la de la cabecera")
    chk(en_archivo == al_azar + dudosas,
        "la muestra se vuelve a sacar igual con su semilla (las mismas evidencias, en el mismo orden)")
    chk(all(sum(1 for c, _ in al_azar if c.startswith(a + "-")) == 10 for a, _ in AREAS),
        "la muestra tiene 10 evidencias al azar por área")
    chk({(x["codigo_dba"], x["numero_evidencia"]) for x in d if x["dudoso"]} <= set(en_archivo),
        "la muestra incluye todas las dudosas")
    return hechas, fallas


def errores_a_proposito(censo, texto_muestra):
    casos = []

    def caso(nombre, cambio, se_espera):
        c, t = copy.deepcopy(censo), texto_muestra
        t = cambio(c["dictamenes"], c["_meta"]) or t
        casos.append((nombre, c, t, se_espera))

    def falta(d, meta):
        d.pop(100)
    caso("un dictamen que falta", falta, "toda evidencia del catálogo")

    def doble(d, meta):
        d.append(copy.deepcopy(d[5]))
    caso("una evidencia con dos dictámenes", doble, "dos dictámenes")

    def formato_sin_aplicar(d, meta):
        x = next(x for x in d if not x["aplica"])
        x["formato"] = "single_choice"
    caso("un formato en una evidencia que no aplica (rompe RI-19)", formato_sin_aplicar, "RI-19")

    def sin_regla(d, meta):
        x = next(x for x in d if x["regla"] == "N3")
        x["justificacion"] = x["justificacion"].replace("(N3)", "").replace("N3", "")
    caso("una justificación que no cita su regla", sin_regla, "cita su regla")

    def regla_cambiada(d, meta):
        x = next(x for x in d if x["aplica"] and x["formato"] == "single_choice")
        x["aplica"], x["formato"], x["regla"] = False, None, "N2"
    caso("un dictamen cambiado sin cambiar su justificación", regla_cambiada, "cita su regla")

    def texto(d, meta):
        d[0]["evidencia"] = d[0]["evidencia"].replace("e", "a", 1)
    caso("el texto de una evidencia cambiado", texto, "el texto de cada evidencia")

    def estado(d, meta):
        meta["estado"] = "validado"
    caso("un estado del censo que no existe", estado, "el estado del censo")

    def muestra_cambiada(d, meta):
        t = texto_muestra
        primero = re.search(r"^### 1\. `([^`]+)` #(\d+)$", t, re.M)
        return t.replace(primero.group(0), "### 1. `MAT-01-01` #1", 1)
    caso("una evidencia de la muestra cambiada", muestra_cambiada, "la muestra se vuelve a sacar igual")
    return casos


def main():
    censo = json.load(open(CENSO, encoding="utf-8"))
    catalogo = json.load(open(CATALOGO, encoding="utf-8"))["dba"]
    texto_muestra = open(MUESTRA, encoding="utf-8").read()
    print("=" * 70)
    print(f"Censo de formato cerrado — {len(censo['dictamenes'])} dictámenes ({censo['_meta']['estado']})")
    print("=" * 70)
    hechas, fallas = verificar(censo, catalogo, texto_muestra)
    print(f"   {len(hechas)} comprobaciones correctas")
    for f in fallas:
        print(f"   FALLA {f}")
    print()
    print("=" * 70)
    print("¿El verificador atrapa errores? Se introducen a propósito, en memoria")
    print("=" * 70)
    atrapados = 0
    casos = errores_a_proposito(censo, texto_muestra)
    for nombre, copia, texto, se_espera in casos:
        _, f = verificar(copia, catalogo, texto)
        f = [x for x in f if x not in fallas]
        ok = any(se_espera in x for x in f)
        atrapados += ok
        print(f"   {'ATRAPADO ' if ok else 'NO ATRAPADO'} {nombre}")
        for x in [x for x in f if se_espera in x][:1]:
            print(f"             ↳ {x[:100]}")
    print("   (los archivos en disco no se modificaron)")
    print()
    print("=" * 70)
    if fallas or atrapados != len(casos):
        print(f"RESULTADO: {len(fallas)} FALLAS; {atrapados} de {len(casos)} errores a propósito atrapados")
        sys.exit(1)
    print(f"RESULTADO: {len(hechas)} comprobaciones, todas correctas; "
          f"{atrapados} de {len(casos)} errores a propósito atrapados.")
    print("=" * 70)


if __name__ == "__main__":
    main()
