"""Genera el diccionario de datos, el DBML y el SQL desde `datos_mr.py`.

Los tres salen de la misma fuente para que no puedan contradecirse —
que es exactamente lo que paso entre el MER y el MR antes del
2026-09-19.

Uso:  python3 generar.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datos_mr import (TABLAS, FKS, UNICOS, CHECKS, campos_de, pk_de,   # noqa
                      N_TABLAS, N_CAMPOS, N_FKS)

AQUI = os.path.dirname(os.path.abspath(__file__))
FASE3 = os.path.join(AQUI, "..")

CLASES = {
    "propia": "Propia",
    "men": "Externa (MEN)",
    "men debil": "Externa (MEN), débil",
    "propia debil": "Propia, débil",
    "asociativa": "Asociativa",
}


def cel(texto):
    """Escapa el contenido de una celda de tabla Markdown.

    Sin esto, un dominio como `muestra | no_muestra | no_concluyente`
    parte la fila en columnas extra y descuadra la tabla entera. Salio
    justo asi en la primera generacion.
    """
    return str(texto).replace("|", "\\|")


def fks_de(tabla):
    return [f for f in FKS if f[0] == tabla]


def unicos_de(tabla):
    return [u for u in UNICOS if u[0] == tabla]


def checks_de(tabla):
    return [c for c in CHECKS if c[0] == tabla]


# ============================================================ DICCIONARIO
def diccionario():
    L = []
    w = L.append
    w("# 6. Diccionario de Datos — AdaptiveLearn")
    w("")
    w('> **⚠ BORRADOR ANTERIOR AL CIERRE DE LA FASE II — no es fuente de verdad.**')
    w('> Se hizo entre agosto y septiembre de 2026, mientras la Fase II seguía')
    w('> abierta. Después cambiaron decisiones que lo afectan (ADR-026 a')
    w('> ADR-029, entre otras). La fuente de verdad es la Fase I, la Fase II y')
    w('> `diseno/decisiones.md`; la Fase III se rehace en orden desde')
    w('> `10-proceso-desarrollo.md`, y este documento se usa como insumo, no como')
    w('> base. Lo que el modelo nuevo debe recibir está en `diseno/pendientes.md`,')
    w('> sección "Entrada a Fase III". *(Aviso agregado el 2026-10-21, decisión')
    w('> de Alejandro.)*')
    w("")
    w("**Metodología:** MODESEC — Fase III, Diseño Computacional, tercer")
    w("entregable. MODESEC lo pide textualmente: *«un diccionario de datos")
    w("para los metadatos (como tipos, tamaños, y otras cualidades de los")
    w("campos de datos)»* (`MODESEC_TISE2009.txt`).")
    w("")
    w("**Base:** `04-modelo-relacional.md`, que a su vez deriva de")
    w("`01-modelo-entidad-relacion.md` — **Quinta revisión (2026-09-08)**,")
    w("la que responde a la revisión del docente del 2026-09-01.")
    w("")
    w("**Motor objetivo: MariaDB 10.11.** Los tipos concretos de este")
    w("documento son los de ese motor, que es el que el curso DSE-2 pide para")
    w("el backend. La columna equivalente en SQLite existe en")
    w("`modelo-relacional/mr_esquema.sql`, que se usa solo para la")
    w("verificación mecánica.")
    w("")
    w("**Generado, no escrito a mano.** Este documento sale de")
    w("`modelo-relacional/datos_mr.py` mediante `generar.py`. No se edita")
    w("directamente: se edita la fuente y se regenera. La razón es concreta —")
    w("el 2026-09-19 se descubrió que el Modelo Relacional llevaba dos")
    w("revisiones de atraso respecto al MER sin que nadie lo notara, porque")
    w("eran dos documentos escritos a mano por separado. `_verificar_mr_mer.py`")
    w("comprueba en cada corrida que esta fuente no se aparte del MER.")
    w("")
    w("---")
    w("")
    w("## Resumen")
    w("")
    w(f"| Tablas | Columnas | Llaves foráneas |")
    w(f"|---|---|---|")
    w(f"| {N_TABLAS} | {N_CAMPOS} | {N_FKS} |")
    w("")
    w("Reporte no aparece: no es una tabla. Es un conjunto de vistas")
    w("calculadas sobre `resultado`, sin llave ni persistencia propia —")
    w("confirmado en el MER y en el MR.")
    w("")
    w("## Cómo leer cada ficha")
    w("")
    # Cada fila de tabla va en UNA sola linea: partirla rompe el
    # renderizado de Markdown.
    w("| Columna | Qué dice |")
    w("|---|---|")
    w("| **Campo** | Nombre exacto en el esquema. |")
    w("| **Tipo (MariaDB)** | Tipo y tamaño concretos. El tamaño no es arbitrario: ver «Convenciones fijadas aquí» al final. |")
    w("| **Nulo** | Si admite `NULL`. «No» significa `NOT NULL`. |")
    w("| **Llave** | PK, FK, o UNIQUE. |")
    w("| **Dominio** | Valores admitidos, cuando están restringidos. |")
    w("| **Defecto** | Valor por defecto, si existe. |")
    w("| **Descripción y fuente** | Qué significa y de qué ADR o spec sale. |")
    w("")
    w("---")
    w("")

    for i, t in enumerate(TABLAS, 1):
        w(f"## {i}. `{t['tabla']}`")
        w("")
        w(f"**Entidad del MER:** {t['entidad']} · "
          f"**Clasificación:** {CLASES[t['clase']]}")
        w("")
        w(t["desc"])
        w("")
        # La clase la usa el conversor a PDF para que los identificadores
        # no se partan a mitad de palabra (`id_inscrip` / `cion`).
        w('<!-- tabla:campos -->')
        w("| Campo | Tipo (MariaDB) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |")
        w("|---|---|---|---|---|---|---|")
        for f in t["campos"]:
            nulo = "Sí" if f["nulo"] else "No"
            llave = f["llave"] or "—"
            dom = cel(f["dominio"]) or "—"
            det = cel(f["defecto"]) or "—"
            desc = cel(f"{f['desc']}<br>*Fuente: {f['fuente']}*")
            w(f"| `{f['nombre']}` | `{cel(f['mariadb'])}` | {nulo} | {llave} | "
              f"{dom} | {det} | {desc} |")
        w("")

        fks = fks_de(t["tabla"])
        if fks:
            w("**Llaves foráneas**")
            w("")
            w('<!-- tabla:fks -->')
            w("| Columnas | Referencia | ON DELETE | Por qué esa acción |")
            w("|---|---|---|---|")
            for _, cols, dest, cols_d, od, razon in fks:
                w(f"| `{', '.join(cols)}` | `{dest}({', '.join(cols_d)})` | "
                  f"`{od}` | {razon} |")
            w("")
            w("*`ON UPDATE CASCADE` en todas, sin excepción — ver el Modelo")
            w("Relacional para el porqué.*")
            w("")

        un = unicos_de(t["tabla"])
        if un:
            w("**Unicidad**")
            w("")
            for _, cols, razon in un:
                w(f"- `UNIQUE({', '.join(cols)})` — {razon}")
            w("")

        ch = checks_de(t["tabla"])
        if ch:
            w("**Restricciones de dominio (CHECK)**")
            w("")
            for _, expr, fuente in ch:
                w(f"- `{expr}` — {fuente}")
            w("")

    w("---")
    w("")
    w("## Lo que este diccionario declara como no resuelto")
    w("")
    w("Un diccionario que inventa un tipo para un campo cuyo dominio todavía")
    w("no se decidió afirma más de lo que el proyecto sostiene. Estos casos")
    w("quedan marcados, no rellenados:")
    w("")
    w("| Campo | Qué falta | Dónde está declarado |")
    w("|---|---|---|")
    w("| `item.estado_revision` | El vocabulario exacto de estados. Por eso el tipo es `VARCHAR(30)` y **no** un `ENUM`: poner un ENUM aquí sería fijar por la puerta de atrás una decisión que nadie tomó. | **V-7**, MER |")
    w("| `resultado.estado` | El tipo sí está cerrado, pero **la función que lo calcula no**: qué combinación exacta de `correcta` × `certeza` cuenta como señal fuerte. | **V-5**, MER (hallazgo H-7 del docente) |")
    w("| `dba.ejemplo` | Admite `NULL` porque el campo todavía no existe en la normalización del currículo. No es opcionalidad de diseño, es un dato que falta. | **QA-011** |")
    w("")
    w("## Convenciones fijadas aquí")
    w("")
    w("- **Identificadores:** `INT UNSIGNED AUTO_INCREMENT`. Un `INT UNSIGNED`")
    w("  llega a 4.294.967.295 filas — muy por encima de cualquier escala")
    w("  realista de este sistema, y ocupa la mitad que un `BIGINT`.")
    w("- **`VARCHAR(254)` para correo:** es el máximo que admite una dirección")
    w("  de correo según RFC 5321. No es un número redondeado a ojo.")
    w("- **`CHAR(6)` para el código de invitación:** longitud fija y conocida")
    w("  (`08-spec-unirse-codigo.md` §2.3). `CHAR` y no `VARCHAR` porque nunca")
    w("  varía.")
    w("- **`TINYINT UNSIGNED` para `certeza`, `numero_evidencia`,")
    w("  `orden_presentacion`, `orden` y `valor_dado`:** ninguno pasa de 255")
    w("  por definición (la escala CRI llega a 5; el tope de ítems por")
    w("  evidencia es 6, ADR-016).")
    w("- **`TEXT` para todo enunciado:** los textos del MEN no tienen longitud")
    w("  acotada conocida, y truncarlos sería alterar contenido oficial.")
    w("- **`DATETIME` y no `TIMESTAMP`:** `TIMESTAMP` en MariaDB tiene el")
    w("  límite del año 2038 y conversión automática de zona horaria; ninguna")
    w("  de las dos cosas se necesita aquí.")
    w("- **`ENUM` donde el dominio está cerrado y decidido**; `VARCHAR` con")
    w("  `CHECK` donde no lo está (ver la tabla de arriba).")
    w("")
    return "\n".join(L) + "\n"


# =================================================================== DBML
def dbml():
    L = []
    w = L.append
    w("// Modelo Relacional — AdaptiveLearn")
    w("// GENERADO por modelo-relacional/generar.py — no editar a mano.")
    w("// Fuente: datos_mr.py · Base: MER Quinta revision (2026-09-08)")
    w("// Pegar en https://dbdiagram.io para el diagrama.")
    w("")
    for t in TABLAS:
        w(f"Table {t['tabla']} {{")
        pk = pk_de(t["tabla"])
        for f in t["campos"]:
            attrs = []
            if len(pk) == 1 and f["nombre"] in pk:
                attrs.append("pk")
            if not f["nulo"]:
                attrs.append("not null")
            if f["llave"] == "UNIQUE":
                attrs.append("unique")
            tipo = f["mariadb"].replace(" AUTO_INCREMENT", "")
            if tipo.startswith("ENUM"):
                tipo = "varchar"
            a = " [" + ", ".join(attrs) + "]" if attrs else ""
            w(f"  {f['nombre']} {tipo.lower()}{a}")
        if len(pk) > 1:
            w("  indexes {")
            w(f"    ({', '.join(pk)}) [pk]")
            w("  }")
        w("}")
        w("")
    w("// ---- referencias ----")
    for origen, cols, dest, cols_d, od, _ in FKS:
        c = cols[0] if len(cols) == 1 else f"({', '.join(cols)})"
        d = cols_d[0] if len(cols_d) == 1 else f"({', '.join(cols_d)})"
        w(f"Ref: {origen}.{c} > {dest}.{d} "
          f"[delete: {od.lower()}, update: cascade]")
    return "\n".join(L) + "\n"


# ==================================================================== SQL
def sql():
    L = []
    w = L.append
    w("-- Esquema ejecutable — AdaptiveLearn")
    w("-- GENERADO por modelo-relacional/generar.py — no editar a mano.")
    w("-- Dialecto: SQLite, solo para la verificacion mecanica.")
    w("-- Los tipos de produccion (MariaDB) estan en 06-diccionario-datos.md")
    w("PRAGMA foreign_keys = ON;")
    w("")
    for t in TABLAS:
        w(f"CREATE TABLE {t['tabla']} (")
        lineas = []
        pk = pk_de(t["tabla"])
        for f in t["campos"]:
            partes = [f"  {f['nombre']}", f["sqlite"]]
            if len(pk) == 1 and f["nombre"] in pk:
                partes.append("PRIMARY KEY")
                if "AUTO_INCREMENT" in f["mariadb"]:
                    partes.append("AUTOINCREMENT")
            if not f["nulo"]:
                partes.append("NOT NULL")
            if f["llave"] == "UNIQUE":
                partes.append("UNIQUE")
            if f["defecto"] and f["defecto"] not in ("NULL", ""):
                d = f["defecto"]
                d = {"TRUE": "1", "FALSE": "0"}.get(d, d)
                partes.append(f"DEFAULT {d}")
            lineas.append(" ".join(partes))
        if len(pk) > 1:
            lineas.append(f"  PRIMARY KEY ({', '.join(pk)})")
        for _, cols, razon in unicos_de(t["tabla"]):
            lineas.append(f"  UNIQUE ({', '.join(cols)})")
        # dominios cerrados -> CHECK (SQLite no tiene ENUM)
        for f in t["campos"]:
            if f["mariadb"].startswith("ENUM"):
                vals = f["mariadb"][5:-1]
                lineas.append(f"  CHECK ({f['nombre']} IN ({vals}))")
        for _, expr, _ in checks_de(t["tabla"]):
            if "BETWEEN" in expr or ">" in expr:
                lineas.append(f"  CHECK ({expr})")
        cod = [f for f in t["campos"] if f["nombre"] == "codigo_invitacion"]
        if cod:
            pos = " AND ".join(
                f"substr(codigo_invitacion,{i},1) "
                f"GLOB '[ABCDEFGHJKMNPQRSTUVWXYZ23456789]'" for i in range(1, 7))
            lineas.append(f"  CHECK (length(codigo_invitacion) = 6 AND {pos})")
        for _, cols, dest, cols_d, od, _ in fks_de(t["tabla"]):
            lineas.append(
                f"  FOREIGN KEY ({', '.join(cols)}) "
                f"REFERENCES {dest}({', '.join(cols_d)}) "
                f"ON DELETE {od} ON UPDATE CASCADE")
        w(",\n".join(lineas))
        w(");")
        w("")
    w("-- ---- indices sobre FK no cubiertas por una llave existente ----")
    for origen, cols, dest, _, _, _ in FKS:
        pk = pk_de(origen)
        unicos = [u[1] for u in unicos_de(origen)]
        cubierta = (pk[:len(cols)] == cols or
                    any(u[:len(cols)] == cols for u in unicos))
        if not cubierta:
            w(f"CREATE INDEX idx_{origen}_{'_'.join(cols)} "
              f"ON {origen}({', '.join(cols)});")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    salidas = [
        (os.path.join(FASE3, "06-diccionario-datos.md"), diccionario()),
        (os.path.join(AQUI, "mr_adaptivelearn.dbml"), dbml()),
        (os.path.join(AQUI, "mr_esquema.sql"), sql()),
    ]
    for ruta, contenido in salidas:
        with open(ruta, "w", encoding="utf-8") as fh:
            fh.write(contenido)
        print(f"generado: {os.path.relpath(ruta, FASE3)}  "
              f"({len(contenido.splitlines())} lineas)")
    print(f"\n{N_TABLAS} tablas · {N_CAMPOS} columnas · {N_FKS} llaves foraneas")
