"""Genera el diccionario de datos, el DBML y los dos SQL desde `datos_mr.py`.

Los cuatro salen de la misma fuente para que no puedan contradecirse —
que es exactamente lo que paso entre el MER y el MR antes del
2026-09-19.

  ../18-diccionario-datos.md   el entregable de MODESEC
  mr_adaptivelearn.dbml        para dibujar el MR en dbdiagram.io
  mr_esquema.sql               SQLite: lo usa verificar_mr.py
  mr_mysql.sql                 MySQL 8 (y MariaDB 10.11): el esquema real
  backend/sql/001_esquema.sql  el mismo esquema, solo con las tablas que el
                               backend usa hoy (TABLAS_BACKEND): asi la base
                               del backend no puede apartarse del MR

Uso:  python generar.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datos_mr import (TABLAS, FKS, UNICOS, CHECKS, campos_de, pk_de,   # noqa
                      N_TABLAS, N_CAMPOS, N_FKS)

AQUI = os.path.dirname(os.path.abspath(__file__))
FASE3 = os.path.join(AQUI, "..")
RAIZ = os.path.normpath(os.path.join(FASE3, "..", "..", ".."))
SQL_BACKEND = os.path.join(RAIZ, "backend", "sql", "001_esquema.sql")

# Las tablas de la etapa del backend del encargo 03: el acceso y el catalogo
# curricular, hasta el Paso 3 de crear experiencia (sin crear la
# experiencia). Tiene que ser cerrada: toda FK de una de ellas apunta a otra.
TABLAS_BACKEND = ["credencial", "codigo_verificacion", "docente", "estudiante",
                  "area", "grado", "documento_oficial", "dba", "evidencia",
                  "evidencia_dictamen"]

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


def expr_de(expr, dialecto):
    return expr[dialecto] if isinstance(expr, dict) else expr


def nombre_ck(tabla, i):
    return f"ck_{tabla}_{i}"


def indices_extra(tabla):
    """FK cuyas columnas no encabezan ya la PK ni un UNIQUE: necesitan indice."""
    pk = pk_de(tabla)
    unicos = [u[1] for u in unicos_de(tabla)]
    for fk in fks_de(tabla):
        cols = fk[1]
        cubierta = (pk[:len(cols)] == cols or
                    any(u[:len(cols)] == cols for u in unicos))
        if not cubierta:
            yield cols


def orden_creacion():
    """Tablas en un orden en que cada FK apunta a una tabla ya creada.

    SQLite resuelve las FK al usarlas y no le importa el orden; MySQL las
    resuelve al crear la tabla. `credencial` va primera en el MER (es por
    donde se entra al sistema) pero apunta a `docente` y `estudiante`."""
    pendientes = [t["tabla"] for t in TABLAS]
    hechas = []
    while pendientes:
        for t in pendientes:
            destinos = {fk[2] for fk in fks_de(t)} - {t}
            if destinos <= set(hechas):
                hechas.append(t)
                pendientes.remove(t)
                break
        else:
            raise ValueError(f"ciclo de FK entre {pendientes}")
    return hechas


# ============================================================ DICCIONARIO
def diccionario():
    L = []
    w = L.append
    w("# 18. Diccionario de Datos — AdaptiveLearn")
    w("")
    w("**Metodología:** MODESEC — Fase III, Diseño Computacional. Último")
    w("entregable del modelado de la base de datos. MODESEC lo pide")
    w("textualmente: *«un diccionario de datos para los metadatos (como tipos,")
    w("tamaños, y otras cualidades de los campos de datos)»*")
    w("(`MODESEC_TISE2009.txt`).")
    w("")
    w("**Base:** `17-modelo-relacional.md`, que deriva de")
    w("`16-modelo-entidad-relacion.md` — el MER final de la Fase III, hecho")
    w("con la Fase II cerrada y el análisis de requerimientos")
    w("(`11-analisis-requerimientos.md`) como fuente.")
    w("")
    w("**Motor objetivo: MySQL 8** (RNF-14: *«NestJS y MySQL»*). Los tipos de")
    w("este documento son los de ese motor, y no usan nada que MariaDB 10.11")
    w("no tenga: el backend del incremento I1 hoy corre sobre MariaDB y debe")
    w("aceptarlo igual. El esquema ejecutable es")
    w("`modelo-relacional/mr_mysql.sql`, **probado contra MySQL 8 real** (8.4 y 8.0)")
    w("(ver `17-modelo-relacional.md`, «Verificación mecánica»). La columna")
    w("equivalente en SQLite vive en `modelo-relacional/mr_esquema.sql`, que")
    w("se usa solo para la verificación automática.")
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
    w("| Tablas | Columnas | Llaves foráneas | UNIQUE | CHECK |")
    w("|---|---|---|---|---|")
    w(f"| {N_TABLAS} | {N_CAMPOS} | {N_FKS} | {len(UNICOS)} | {len(CHECKS)} |")
    w("")
    w("Reporte no aparece: no es una tabla. Se calcula sobre `resultado` cada")
    w("vez que el docente lo abre, sin llave ni persistencia propia — así lo")
    w("declara el MER y así lo implementa el MR.")
    w("")
    w("## Cómo leer cada ficha")
    w("")
    # Cada fila de tabla va en UNA sola linea: partirla rompe el
    # renderizado de Markdown.
    w("| Columna | Qué dice |")
    w("|---|---|")
    w("| **Campo** | Nombre exacto en el esquema. |")
    w("| **Tipo (MySQL)** | Tipo y tamaño concretos. El tamaño no es arbitrario: ver «Convenciones fijadas aquí» al final. |")
    w("| **Nulo** | Si admite `NULL`. «No» significa `NOT NULL`. |")
    w("| **Llave** | PK, FK, o UNIQUE. |")
    w("| **Dominio** | Valores admitidos, cuando están restringidos. |")
    w("| **Defecto** | Valor por defecto, si existe. |")
    w("| **Descripción y fuente** | Qué significa y de qué RF, ADR o spec sale. |")
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
        w("| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |")
        w("|---|---|---|---|---|---|---|")
        for f in t["campos"]:
            nulo = "Sí" if f["nulo"] else "No"
            llave = f["llave"] or "—"
            dom = cel(f["dominio"]) or "—"
            det = cel(f["defecto"]) or "—"
            desc = cel(f"{f['desc']}<br>*Fuente: {f['fuente']}*")
            w(f"| `{f['nombre']}` | `{cel(f['mysql'])}` | {nulo} | {llave} | "
              f"{dom} | {det} | {desc} |")
        w("")

        fks = fks_de(t["tabla"])
        if fks:
            w("**Llaves foráneas**")
            w("")
            w('<!-- tabla:fks -->')
            w("| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |")
            w("|---|---|---|---|---|")
            for _, cols, dest, cols_d, od, razon, ou in fks:
                w(f"| `{', '.join(cols)}` | `{dest}({', '.join(cols_d)})` | "
                  f"`{od}` | `{ou}` | {razon} |")
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
            for _, expr, desc, fuente in ch:
                w(f"- `{expr_de(expr, 'mysql')}` — {desc}. *{fuente}*")
            w("")

    w("---")
    w("")
    w("## Lo que este diccionario declara como no resuelto")
    w("")
    w("Un diccionario que inventa un valor para un dato que todavía no se")
    w("tiene afirma más de lo que el proyecto sostiene. Estos casos quedan")
    w("marcados, no rellenados:")
    w("")
    w("| Campo | Qué falta | Dónde está declarado |")
    w("|---|---|---|")
    w("| `evidencia_dictamen.aplica_formato_cerrado` | El tipo está cerrado; **los valores no**: dependen del censo QA-014, que no ha corrido. Hasta entonces RI-5 no se puede evaluar contra datos reales. | **V-6**, MER |")
    w("| `dba.codigo_dba` | El formato `ÁREA-GG-NN` está cerrado (RI-21), y los datos lo cumplen como llave desde el catálogo corregido (`data/curriculo-men/catalogo/catalogo_dba.json`, 343 DBA, encargo 02). El JSON viejo, `curriculo_men_normalizado.json`, tenía 342 DBA y solo 329 códigos distintos; cargarlo falla por llave duplicada en 13, y eso es lo correcto: se corrigió en los datos, no en el modelo. | **Pendientes, A12** · ADR-036 |")
    w("| `dba.ejemplo` | Admite `NULL` porque el campo todavía no existe en la normalización del currículo. No es opcionalidad de diseño, es un dato que falta. | **QA-011** |")
    w("")
    w("**Cerrados desde el borrador anterior** (para no perder el rastro):")
    w("`item.estado_revision` sale del modelo (V-7: tras ADR-026 revisar el")
    w("banco no es requisito de nada); la función que calcula")
    w("`resultado.estado` quedó definida en RF-04-07 (V-5); la credencial ya")
    w("tiene tabla (V-8); y la política de borrado está en las FK (V-11).")
    w("")
    w("## Convenciones fijadas aquí")
    w("")
    w("- **Identificadores:** `INT UNSIGNED AUTO_INCREMENT`. Un `INT UNSIGNED`")
    w("  llega a 4.294.967.295 filas — muy por encima de cualquier escala")
    w("  realista de este sistema, y ocupa la mitad que un `BIGINT`.")
    w("- **`VARCHAR(254)` para correo:** es el máximo que admite una dirección")
    w("  de correo según RFC 5321. No es un número redondeado a ojo.")
    w("- **`CHAR(6)` para el código de invitación y el de verificación:**")
    w("  longitud fija y conocida (`08-spec-unirse-codigo.md` §2.3,")
    w("  RF-01-03). `CHAR` y no `VARCHAR` porque nunca varía.")
    w("- **`TINYINT UNSIGNED` para `certeza`, `numero_evidencia`,")
    w("  `orden_presentacion`, `orden`, `valor_dado`, el número del grado y los")
    w("  contadores de intentos:** ninguno pasa de 255 por definición (la escala")
    w("  CRI llega a 5; el tope de ítems por evidencia es 6, ADR-016; los grados,")
    w("  a 11). `SMALLINT UNSIGNED` para el año y las páginas de un documento.")
    w("- **`TEXT` para todo enunciado:** los textos del MEN no tienen longitud")
    w("  acotada conocida, y truncarlos sería alterar contenido oficial.")
    w("- **`DATETIME` y no `TIMESTAMP`:** `TIMESTAMP` tiene el límite del año")
    w("  2038 y conversión automática de zona horaria; ninguna de las dos")
    w("  cosas se necesita aquí.")
    w("- **`ENUM` donde el dominio está cerrado y decidido.** Desde que V-7 se")
    w("  cerró ya no queda ningún dominio abierto; en SQLite, que no tiene")
    w("  `ENUM`, cada uno se vuelve un `CHECK ... IN (...)`.")
    w("- **`utf8mb4` con cotejamiento `utf8mb4_unicode_ci`:** acentos y eñes")
    w("  sin pérdida, y comparación sin distinguir mayúsculas — por eso")
    w("  `correo` y `codigo_invitacion` son únicos sin importar cómo se")
    w("  escriban (RF-01-04, `08-spec-unirse-codigo.md`). Se elige ese")
    w("  cotejamiento y no el `utf8mb4_0900_ai_ci` por defecto de MySQL 8")
    w("  porque MariaDB no lo tiene.")
    w("- **Códigos del catálogo en ASCII con cotejamiento binario**")
    w("  (`CHARACTER SET ascii COLLATE ascii_bin`): `codigo_dba` y `codigo_area`, y")
    w("  toda columna que los repite como llave foránea. ADR-036 pide códigos sin")
    w("  tildes: con ASCII, una tilde no se puede guardar; con el cotejamiento")
    w("  binario, `mat` no es igual a `MAT`. Las dos cosas existen igual en MySQL 8 y")
    w("  en MariaDB. Es una decisión de este modelo, no de una ADR: va declarada en")
    w("  `17-modelo-relacional.md` para que el equipo la confirme.")
    w("- **`VARCHAR(9)` para `codigo_dba`:** `ÁREA-GG-NN` mide 8 o 9 caracteres")
    w("  (`CN-01-01`, `MAT-01-01`).")
    w("- **Nombres de restricción** `ck_<tabla>_<n>`, `fk_<tabla>_<n>` y")
    w("  `uq_<tabla>_<n>`: un error del motor nombra la regla rota, y con el")
    w("  número se encuentra aquí.")
    w("")
    return "\n".join(L) + "\n"


# =================================================================== DBML
def dbml():
    L = []
    w = L.append
    w("// Modelo Relacional — AdaptiveLearn")
    w("// GENERADO por modelo-relacional/generar.py — no editar a mano.")
    w("// Fuente: datos_mr.py · Base: MER final de la Fase III (2026-10-21)")
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
            if "AUTO_INCREMENT" in f["mysql"]:
                attrs.append("increment")
            # DBML no tiene juego de caracteres por columna: va solo el tipo
            tipo = f["mysql"].replace(" AUTO_INCREMENT", "").split(" CHARACTER SET")[0].lower()
            if tipo.startswith("enum"):
                tipo = "varchar"
            if " " in tipo:                  # DBML exige comillas: "int unsigned"
                tipo = f'"{tipo}"'
            a = " [" + ", ".join(attrs) + "]" if attrs else ""
            w(f"  {f['nombre']} {tipo}{a}")
        compuestos = [u for u in unicos_de(t["tabla"]) if len(u[1]) > 1]
        if len(pk) > 1 or compuestos:
            w("  indexes {")
            if len(pk) > 1:
                w(f"    ({', '.join(pk)}) [pk]")
            for _, cols, _ in compuestos:
                w(f"    ({', '.join(cols)}) [unique]")
            w("  }")
        w("}")
        w("")
    w("// ---- referencias ----")
    for origen, cols, dest, cols_d, od, _, ou in FKS:
        c = cols[0] if len(cols) == 1 else f"({', '.join(cols)})"
        d = cols_d[0] if len(cols_d) == 1 else f"({', '.join(cols_d)})"
        w(f"Ref: {origen}.{c} > {dest}.{d} "
          f"[delete: {od.lower()}, update: {ou.lower()}]")
    return "\n".join(L) + "\n"


# ============================================================= SQL SQLite
def sql():
    L = []
    w = L.append
    w("-- Esquema ejecutable — AdaptiveLearn")
    w("-- GENERADO por modelo-relacional/generar.py — no editar a mano.")
    w("-- Dialecto: SQLite, solo para la verificacion mecanica (verificar_mr.py).")
    w("-- El esquema real (MySQL 8) es mr_mysql.sql.")
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
                if "AUTO_INCREMENT" in f["mysql"]:
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
            if len(cols) > 1 or not any(f["nombre"] == cols[0] and f["llave"] == "UNIQUE"
                                        for f in t["campos"]):
                lineas.append(f"  UNIQUE ({', '.join(cols)})")
        # dominios cerrados -> CHECK (SQLite no tiene ENUM)
        for f in t["campos"]:
            if f["mysql"].startswith("ENUM"):
                vals = f["mysql"][5:-1]
                lineas.append(f"  CHECK ({f['nombre']} IN ({vals}))")
        for _, expr, _, _ in checks_de(t["tabla"]):
            lineas.append(f"  CHECK ({expr_de(expr, 'sqlite')})")
        for _, cols, dest, cols_d, od, _, ou in fks_de(t["tabla"]):
            lineas.append(
                f"  FOREIGN KEY ({', '.join(cols)}) "
                f"REFERENCES {dest}({', '.join(cols_d)}) "
                f"ON DELETE {od} ON UPDATE {ou}")
        w(",\n".join(lineas))
        w(");")
        w("")
    w("-- ---- indices sobre FK no cubiertas por una llave existente ----")
    for t in TABLAS:
        for cols in indices_extra(t["tabla"]):
            w(f"CREATE INDEX idx_{t['tabla']}_{'_'.join(cols)} "
              f"ON {t['tabla']}({', '.join(cols)});")
    return "\n".join(L) + "\n"


# ============================================================== SQL MySQL
def sql_mysql(tablas=None):
    """El DDL de MySQL. Con `tablas`, solo esas (en orden de creacion)."""
    L = []
    w = L.append
    if tablas is None:
        w("-- Esquema de produccion — AdaptiveLearn")
        w("-- GENERADO por modelo-relacional/generar.py — no editar a mano.")
    else:
        fuera = {fk[2] for t in tablas for fk in fks_de(t)} - set(tablas)
        if fuera:
            raise ValueError(f"TABLAS_BACKEND no es cerrada: falta {sorted(fuera)}")
        w("-- Esquema del backend — AdaptiveLearn")
        w("-- GENERADO por docs/modesec/fase-3-diseno-computacional/modelo-relacional/")
        w("-- generar.py desde datos_mr.py — no editar a mano: cambiar el MR y regenerar.")
        w("-- Es mr_mysql.sql, solo con las tablas que el backend usa hoy (encargo 03):")
        w("-- " + ", ".join(tablas) + ".")
    w("-- Dialecto: MySQL 8.0.16 o posterior (RNF-14). Tambien corre en")
    w("-- MariaDB 10.11: no usa nada que ese motor no tenga.")
    w("-- Ejecutar dentro de una base de datos VACIA, ya seleccionada con USE.")
    w("-- Los CHECK se hacen cumplir desde MySQL 8.0.16; antes se ignoraban.")
    w("SET NAMES utf8mb4;")
    w("")
    por_nombre = {t["tabla"]: t for t in TABLAS}
    for nombre in orden_creacion():
        if tablas is not None and nombre not in tablas:
            continue
        t = por_nombre[nombre]
        w(f"CREATE TABLE {nombre} (")
        lineas = []
        pk = pk_de(nombre)
        for f in t["campos"]:
            partes = [f"  {f['nombre']}", f["mysql"]]
            partes.append("NULL" if f["nulo"] else "NOT NULL")
            d = f["defecto"]
            if d and d != "NULL":
                partes.append(f"DEFAULT {d}")
                if f["nombre"] == "actualizado_en":
                    partes.append("ON UPDATE CURRENT_TIMESTAMP")
            lineas.append(" ".join(partes))
        lineas.append(f"  PRIMARY KEY ({', '.join(pk)})")
        for i, (_, cols, _) in enumerate(unicos_de(nombre), 1):
            lineas.append(f"  CONSTRAINT uq_{nombre}_{i} UNIQUE ({', '.join(cols)})")
        for cols in indices_extra(nombre):
            lineas.append(f"  KEY idx_{nombre}_{'_'.join(cols)} ({', '.join(cols)})")
        for i, (_, expr, _, _) in enumerate(checks_de(nombre), 1):
            lineas.append(f"  CONSTRAINT {nombre_ck(nombre, i)} "
                          f"CHECK ({expr_de(expr, 'mysql')})")
        for i, (_, cols, dest, cols_d, od, _, ou) in enumerate(fks_de(nombre), 1):
            lineas.append(
                f"  CONSTRAINT fk_{nombre}_{i} FOREIGN KEY ({', '.join(cols)}) "
                f"REFERENCES {dest}({', '.join(cols_d)}) "
                f"ON DELETE {od} ON UPDATE {ou}")
        w(",\n".join(lineas))
        w(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
        w("")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    salidas = [
        (os.path.join(FASE3, "18-diccionario-datos.md"), diccionario()),
        (os.path.join(AQUI, "mr_adaptivelearn.dbml"), dbml()),
        (os.path.join(AQUI, "mr_esquema.sql"), sql()),
        (os.path.join(AQUI, "mr_mysql.sql"), sql_mysql()),
        (SQL_BACKEND, sql_mysql(TABLAS_BACKEND)),
    ]
    for ruta, contenido in salidas:
        with open(ruta, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(contenido)
        print(f"generado: {os.path.relpath(ruta, FASE3)}  "
              f"({len(contenido.splitlines())} lineas)")
    print(f"\n{N_TABLAS} tablas · {N_CAMPOS} columnas · {N_FKS} llaves foraneas · "
          f"{len(UNICOS)} UNIQUE · {len(CHECKS)} CHECK")
