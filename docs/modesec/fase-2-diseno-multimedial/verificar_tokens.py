#!/usr/bin/env python3
"""Verifica que un spec de pantalla solo use valores del tokens.json.
Uso: python3 verificar_tokens.py <archivo.md>
Sale con codigo != 0 si encuentra un color o numero fuera de la lista aprobada.
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).parent
TOKENS = json.loads((HERE / "tokens.json").read_text(encoding="utf-8"))

colores_validos = {k.upper() for k in TOKENS["colores"].keys()}
anchos_layout = {int(k) for k in TOKENS["anchos_layout_px"].keys() if not k.startswith("_")}
lienzo = {int(k) for k in TOKENS["lienzo_figma_px"].keys() if not k.startswith("_")}
iconos_validos = set(TOKENS["iconos_px"])
espaciado_validos = set(TOKENS["espaciado_px"])
px_validos = set(
    TOKENS["espaciado_px"] + TOKENS["radios_px"] +
    TOKENS["alturas_control_px"] + TOKENS["iconos_px"] +
    TOKENS["grosores_borde_px"] +
    [t["size"] for t in TOKENS["tipografia"]] +
    [t["lh"] for t in TOKENS["tipografia"]]
) | anchos_layout | lienzo
pesos_validos = {t["peso"] for t in TOKENS["tipografia"]}

# Hueco encontrado 2026-08-29: un "20×20px" pasaba solo porque el
# primer numero (20) coincidia con ALGUNA categoria del pool combinado
# -- nunca se exigia que fuera especificamente un tamaño de icono
# valido, aunque la propia linea diga "icono". Se corrige exigiendo
# iconos_px (no el pool general) cuando el numero es la medida de un
# icono declarado como tal.
#
# Deteccion: la palabra "icono" aparece hasta 45 caracteres antes del
# match, en la misma linea. Ventana medida contra el corpus real
# (2026-08-29): las declaraciones genuinas de tamaño de icono quedan
# entre 7 y 38 caracteres despues de la palabra "icono" (ej. "Ícono
# `Users` (grupo de personas), `32×32px`" = 36); el unico falso
# positivo encontrado (una mencion de "iconos inactivos" en prosa,
# 03-tokens-diseno.md linea 146) queda a 300 caracteres del siguiente
# "NxNpx" real (un punto de leyenda, no un icono) -- 45 separa ambos
# casos con margen amplio. Si en el futuro aparece una declaracion de
# icono genuina fuera de ese rango, hay que revisar esta ventana, no
# ensancharla sin medir de nuevo.
ICONO_VENTANA = 45
ICONO_ANTES = re.compile(r"[ií]cono", re.IGNORECASE)

# Hueco encontrado 2026-08-29 (segundo, mismo dia que el de iconos): un
# "Gap `2px`" pasaba porque 2 coincide con grosores_borde_px, aunque 2px
# no es un valor de espaciado real (la escala es 4/8/12/16/24...). Se
# corrige exigiendo espaciado_px cuando el numero es directamente el
# valor de un Gap o Padding.
#
# A diferencia del caso de iconos, acá NO sirve una ventana de "la
# palabra aparece hasta N caracteres antes" -- las lineas de este
# corpus suelen traer varios numeros seguidos despues de "Gap"/
# "Padding" que no son el valor de ese Gap/Padding (ej. "Padding
# izq/der `24px`... texto `16px / 22px`" -- el 16 y el 22 son
# tipografia, no padding, y una ventana ancha los atraparia igual por
# error). Se resuelve capturando SOLO el primer numero que sigue
# inmediatamente a la palabra (maximo 20 caracteres sin otro digito de
# por medio) -- ese es gramaticalmente el valor real del Gap/Padding,
# nunca un numero mas adelante en la misma linea. Medido contra las 142
# apariciones reales de Gap/Padding del corpus (2026-08-29): las 142
# ya eran valores validos de espaciado_px, cero falsos positivos.
GAP_PADDING = re.compile(r"(?:Gap|Padding)[^\d]{0,20}?(\d+(?:\.\d+)?)\s*px", re.IGNORECASE)

# 03-tokens-diseno.md es la DOCUMENTACION de los tokens: ademas de los
# valores en uso, registra los que se RECHAZARON y por que. Acusarlo por
# contenerlos es acusarlo de hacer su trabajo -- mismo falso positivo
# estructural que tenia el detector de consistencia con decisiones.md.
#
# Se resuelve con una lista EXPLICITA y finita, no con un heuristico de
# prosa: un heuristico podria tapar un error real el dia de mañana; una
# lista cerrada solo perdona exactamente lo que ya se decidio rechazar.
RECHAZOS_DOCUMENTADOS = {
    "03-tokens-diseno.md": {
        # Los 4 pasteles del sistema anterior: fallaron la validacion de
        # conjunto categorico (croma bajo, ΔE 2.9 en deuteranopia).
        "#FFE59A", "#FFB5C1", "#B7E1D1", "#A9D3FF",
        # Paleta de estado antes de la revision de la Ventana 010:
        # demasiado vividos frente al resto del sistema.
        "#2A78D6", "#EB6834",
        # Tamaño viejo del Badge Label, subido a 12px por legibilidad.
        11.0,
    },
}


def verificar(path, estricto=True):
    text = Path(path).read_text(encoding="utf-8")
    lineas = text.splitlines()
    errores = []
    perdonados = RECHAZOS_DOCUMENTADOS.get(Path(path).name, set())
    ignorados = 0

    for i, linea in enumerate(lineas, start=1):
        # Colores hex
        for m in re.finditer(r"#[0-9a-fA-F]{6}\b", linea):
            hexval = m.group(0).upper()
            if hexval not in colores_validos:
                if hexval in perdonados:
                    ignorados += 1
                else:
                    errores.append(f"  Línea {i}: color {m.group(0)} NO está en tokens.json")

        # Posiciones cuyo valor es directamente un Gap/Padding -- se
        # calculan aparte porque exigen deteccion "adyacente", no de
        # ventana (ver comentario de GAP_PADDING arriba).
        spans_gap_padding = {m.start(1) for m in GAP_PADDING.finditer(linea)}

        # Valores en px — soporta decimales (1.5px) y pares "20 × 20px"
        for m in re.finditer(r"(?<![\d.])(\d+(?:\.\d+)?)\s*(×)?\s*(?:\d+(?:\.\d+)?\s*)?px", linea):
            val = float(m.group(1))
            val = int(val) if val.is_integer() else val
            es_par_wxh = m.group(2) is not None
            ventana = linea[max(0, m.start() - ICONO_VENTANA):m.start()]
            es_icono = es_par_wxh and ICONO_ANTES.search(ventana) is not None
            es_gap_padding = (not es_icono) and m.start(1) in spans_gap_padding
            if es_icono:
                pool, etiqueta = iconos_validos, "iconos_px"
            elif es_gap_padding:
                pool, etiqueta = espaciado_validos, "espaciado_px"
            else:
                pool, etiqueta = px_validos, None
            if val not in pool:
                if float(val) in perdonados:
                    ignorados += 1
                elif es_icono:
                    errores.append(f"  Línea {i}: valor {val}px declarado como tamaño de ícono, pero NO está en iconos_px {sorted(iconos_validos)}")
                elif es_gap_padding:
                    errores.append(f"  Línea {i}: valor {val}px declarado como Gap/Padding, pero NO está en espaciado_px {sorted(espaciado_validos)}")
                else:
                    errores.append(f"  Línea {i}: valor {val}px NO está en ningún token (espaciado/radio/altura/ícono/borde/layout/tipografía)")

    if errores:
        print(f"FALLO — {path}")
        for e in errores:
            print(e)
        return False
    else:
        extra = (f" ({ignorados} apariciones de valores documentados como "
                 f"RECHAZADOS, perdonadas a propósito)") if ignorados else ""
        print(f"OK — {path}: todos los colores y valores en px están en tokens.json{extra}")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 verificar_tokens.py <archivo.md> [archivo2.md ...]")
        sys.exit(1)
    resultados = [verificar(p) for p in sys.argv[1:]]
    sys.exit(0 if all(resultados) else 1)
