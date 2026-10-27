"""Genera ../17-modelo-relacional.md desde datos_mr.py.

El esquema que el documento describe -- tablas, llaves, acciones
referenciales, UNIQUE y CHECK -- sale de la misma fuente que el SQL que se
probo contra MySQL. La prosa (por que cada decision) vive aqui.

Uso:  python documento_mr.py
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from datos_mr import TABLAS, FKS, UNICOS, CHECKS, pk_de, N_TABLAS, N_CAMPOS, N_FKS  # noqa: E402
from generar import indices_extra, expr_de                                         # noqa: E402
from pruebas_mr import PRUEBAS                                                     # noqa: E402
from collections import Counter                                                    # noqa: E402

N_PRUEBA = Counter(p[0] for p in PRUEBAS)
# lo que cuentan los dos verificadores: bloques A y C fijos, mas semilla y bateria
N_SQLITE = 9 + 1 + len(PRUEBAS) + 3
N_MYSQL = 4 + 1 + len(PRUEBAS)

SALIDA = os.path.join(AQUI, "..", "17-modelo-relacional.md")


def esquema(t):
    """Notacion clasica: tabla(PK subrayada, FK en cursiva con su destino)."""
    pk = pk_de(t["tabla"])
    fk_cols = {}
    for o, cols, dest, *_ in FKS:
        if o == t["tabla"]:
            for c in cols:
                fk_cols.setdefault(c, []).append(dest)
    partes = []
    for f in t["campos"]:
        n = f["nombre"]
        s = f"<u>{n}</u>" if n in pk else n
        if n in fk_cols:
            s = f"*{s}* → {', '.join(dict.fromkeys(fk_cols[n]))}"
        partes.append(s)
    return f"**{t['tabla']}**({', '.join(partes)})"


def documento():
    L = []
    w = L.append
    w("# 17. Modelo Relacional — AdaptiveLearn")
    w("")
    w("**Metodología:** MODESEC — Fase III, Diseño Computacional, modelado de la base de datos.")
    w("**Fecha:** 2026-10-21. **Archivo generado** por `modelo-relacional/documento_mr.py` desde")
    w("`modelo-relacional/datos_mr.py`; no se edita a mano.")
    w("")
    w("**Actualizado el 2026-10-26** por la revisión del docente del 2026-10-22: tablas `area`,")
    w("`grado` y `documento_oficial`, código del DBA `ÁREA-GG-NN` (ADR-036) y")
    w("`credencial.estado_verificacion` (ADR-037). Ver la sección 5.6 y la tabla de cambios (10).")
    w("")
    w("MODESEC pide *«un MR (Modelo relacional) basado en el MER»*. La base es")
    w("`16-modelo-entidad-relacion.md`; `modelo-relacional/_verificar_mr_mer.py` comprueba en cada")
    w("corrida que este modelo no se aparte de él, entidad por entidad y atributo por atributo.")
    w("")
    w("**Motor: MySQL 8** (RNF-14, *«NestJS y MySQL»*). El esquema ejecutable es")
    w("`modelo-relacional/mr_mysql.sql`, y **se probó contra MySQL real** —8.4 y 8.0— (sección 9). No usa")
    w("nada que MariaDB 10.11 no tenga —el backend de I1 hoy corre sobre MariaDB—, pero en MariaDB")
    w("no se ejecutó: queda como prueba pendiente al integrar.")
    w("")
    w("## 1. Resumen")
    w("")
    w("| Tablas | Columnas | Llaves foráneas | UNIQUE | CHECK |")
    w("|---|---|---|---|---|")
    w(f"| {N_TABLAS} | {N_CAMPOS} | {N_FKS} | {len(UNICOS)} | {len(CHECKS)} |")
    w("")
    w("Una tabla por entidad del MER; Reporte no tiene tabla (sección 5). Los tipos, tamaños y")
    w("dominios de cada columna están en `18-diccionario-datos.md`.")
    w("")
    w("## 2. Esquema")
    w("")
    w("Llave primaria <u>subrayada</u>; llave foránea en *cursiva*, con la tabla a la que apunta.")
    w("")
    for t in TABLAS:
        w(f"- {esquema(t)}")
    w("")
    w("Diagrama del esquema: pegar `modelo-relacional/mr_adaptivelearn.dbml` en dbdiagram.io.")
    w("")
    w("## 3. Convención de nombres")
    w("")
    w("- Tablas y columnas en `snake_case`, en singular y sin tildes: `inscripcion`, `opcion`.")
    w("- Llaves sustitutas `id_<tabla>`, `INT UNSIGNED AUTO_INCREMENT`. Las llaves naturales son las")
    w("  del catálogo: `codigo_dba`, `codigo_area` y el `numero` del grado (ADR-036).")
    w("- Una llave foránea se llama igual que la columna a la que apunta, con una excepción:")
    w("  `dba.numero_grado` apunta a `grado.numero`, para no confundirla con el número del DBA.")
    w("- Restricciones con nombre: `fk_<tabla>_<n>`, `uq_<tabla>_<n>`, `ck_<tabla>_<n>`. Un error")
    w("  del motor dice qué regla se rompió.")
    w("")
    w("## 4. Llaves foráneas y política de borrado")
    w("")
    w("**Esto cierra el vacío V-11** que el análisis de requerimientos dejó abierto en RF-02-07")
    w("(eliminar una experiencia) y RF-04-12 (salir de una): borrar una experiencia o una")
    w("inscripción borra **en cascada** todo lo que depende de ella. Las raíces que ningún flujo")
    w("borra —credencial, docente, estudiante, el catálogo (área, grado, documento, DBA) y evidencia—")
    w("quedan en `RESTRICT`, como seguro. `ON UPDATE CASCADE` en todas, salvo las de `credencial` y")
    w("las del catálogo hacia `area`, `grado` y `documento_oficial` (abajo).")
    w("")
    w("| Tabla | Columnas | Referencia | ON DELETE | ON UPDATE | Por qué |")
    w("|---|---|---|---|---|---|")
    for o, cols, dest, cols_d, od, razon, ou in FKS:
        w(f"| {o} | `{', '.join(cols)}` | `{dest}({', '.join(cols_d)})` | {od} | {ou} | {razon} |")
    w("")
    w("**Por qué las de `credencial` no llevan `ON UPDATE CASCADE`:** MySQL no admite una")
    w("restricción CHECK sobre una columna que participa en una acción referencial, y")
    w("`id_docente` / `id_estudiante` tienen el CHECK de RI-12. Como son llaves sustitutas que nunca")
    w("se actualizan, `RESTRICT` no cuesta nada. **Lo mismo en las del catálogo:** el CHECK de RI-21")
    w("lee `dba.codigo_area` y `dba.numero_grado`, y un código del catálogo no cambia.")
    w("")
    w("**Lo que la cascada nunca toca:** una cuenta, ni el currículo. La prueba de la sección 9")
    w("elimina una experiencia con un inscrito que respondió y cuenta, tabla por tabla, lo que queda.")
    w("")
    w("## 5. Decisiones de este modelo")
    w("")
    w("### 5.1 `id_experiencia` en `presentacion` y en `resultado` (RI-13)")
    w("")
    w("El MER dejó esta decisión al modelo relacional: *«que esa deducción se resuelva con una")
    w("columna redundante o con una regla, lo decide el Modelo Relacional»*. Se resuelve con la")
    w("columna, en las dos tablas. `id_experiencia` participa en **dos llaves foráneas compuestas**")
    w("a la vez —hacia `inscripcion(id_inscripcion, id_experiencia)` y hacia")
    w("`item(id_item, id_experiencia)` en `presentacion`; hacia `inscripcion` y hacia")
    w("`experiencia_evidencia` en `resultado`—, así que el motor rechaza una presentación de un ítem")
    w("de otra experiencia, o un resultado de una evidencia que la experiencia no incluye, sin")
    w("triggers. Para que esas FK sean posibles, `inscripcion` e `item` declaran un UNIQUE sobre")
    w("`(id, id_experiencia)`.")
    w("")
    w("El borrador del MR había resuelto esto solo en `resultado` y dejó declarado el hueco en")
    w("`presentacion`. Ya no está: la batería de pruebas intenta las dos combinaciones posibles de")
    w("presentar un ítem ajeno y el motor rechaza ambas.")
    w("")
    w("### 5.2 Los ciclos C1 y C4 del MER, cerrados con la misma técnica (RI-18, RI-6)")
    w("")
    w("El MER declara sus seis ciclos y qué cierra cada uno (`16`, sección 6). Dos estaban abiertos, y")
    w("el motor aceptaba los datos que los rompen; las pruebas de `pruebas_mr.py` lo demostraron:")
    w("")
    w("- **C1, RI-18.** Una experiencia podía incluir una evidencia de **otro DBA**. Ahora la FK de")
    w("  `experiencia_evidencia` hacia `experiencia` es compuesta, `(id_experiencia, codigo_dba)`, y")
    w("  `experiencia` declara `UNIQUE(id_experiencia, codigo_dba)` para poder ser su destino.")
    w("- **C4, RI-6.** Una respuesta podía elegir una opción de **otro ítem**. Ahora `respuesta_opcion`")
    w("  lleva `id_item` dentro de sus dos FK compuestas —hacia `respuesta(id_respuesta, id_item)` y")
    w("  hacia `opcion(id_opcion, id_item)`—, igual que `id_experiencia` en `presentacion`.")
    w("")
    w("### 5.3 El servicio de IA se guarda en la experiencia, no en cada ítem (RI-17)")
    w("")
    w("Un banco sale entero de un solo servicio (RF-03-02). Guardar `servicio_ia` y `modelo_ia` en")
    w("cada ítem repetía el mismo valor una vez por ítem y, peor, dejaba que un banco mezclara")
    w("servicios. Van en `experiencia`, una sola vez y `NOT NULL` (toda experiencia tiene banco: el")
    w("«todo o nada» de ADR-027). El servicio de un ítem de origen `ia` o `editado_docente` es el de su")
    w("experiencia; uno `creado_docente` no se atribuye a la IA. Así RF-03-03 —saber qué servicio y")
    w("modelo generó cada ítem— se cumple sin repetir el dato.")
    w("")
    w("### 5.4 Docente y Estudiante, cada uno con su tabla; Usuario sin tabla")
    w("")
    w("El diagrama de clases generaliza a los dos en `Usuario` (abstracta). En la base, cada")
    w("subclase concreta tiene su tabla con los atributos heredados: no hay usuarios sin rol, y")
    w("Docente y Estudiante son tipos separados (RF-01-06). La credencial apunta a uno **o** al otro")
    w("(CHECK de RI-12), y el correo, en `credencial`, es único entre los dos.")
    w("")
    w("### 5.5 Reporte no es una tabla")
    w("")
    w("Se calcula sobre `resultado` cada vez que el docente lo abre (ADR-022): estado general por")
    w("estudiante y clasificación por evidencia. Guardarlo crearía un segundo lugar donde el mismo")
    w("dato podría quedar viejo.")
    w("")
    w("### 5.6 El catálogo normalizado: ciclo C6 y código del DBA (ADR-036, RI-20, RI-21)")
    w("")
    w("- **C6, RI-20.** El documento del que se copió un DBA tiene que ser de su misma área. Se")
    w("  cierra con la técnica de C1 y C4: la FK de `dba` hacia `documento_oficial` es compuesta,")
    w("  `(id_documento, codigo_area)`, y `documento_oficial` declara `UNIQUE(id_documento, codigo_area)`")
    w("  para poder ser su destino. La prueba «un DBA de Matemáticas copiado del documento de")
    w("  Lenguaje» lo intenta y el motor lo rechaza.")
    w("- **RI-21.** Un CHECK arma el código esperado con el área y el grado de la misma fila y lo")
    w("  compara con `codigo_dba`: `MAT-08-01` solo entra con `codigo_area = 'MAT'` y")
    w("  `numero_grado = 8`. Así el código no puede contradecir las llaves foráneas.")
    w("- **Decisión de esta sesión, para que el equipo la confirme:** las columnas de código")
    w("  (`codigo_dba`, `codigo_area` y sus copias en otras tablas) son `CHARACTER SET ascii COLLATE")
    w("  ascii_bin`. ADR-036 pide códigos sin tildes; con ASCII, el motor ni siquiera puede guardar")
    w("  una tilde, y con el cotejamiento binario `mat` no es igual a `MAT`. El resto de la base sigue")
    w("  en `utf8mb4_unicode_ci`.")
    w("- **De dónde se cargan los DBA.** De `data/curriculo-men/catalogo/catalogo_dba.json` (343 DBA,")
    w("  códigos únicos, verificado contra los PDF; encargo 02, pendientes A12), **no** de")
    w("  `curriculo_men_normalizado.json`: ese tenía 342 DBA y solo 329 códigos distintos (16 §4, DBA),")
    w("  y cargarlo fallaría por llave duplicada en 13, que es lo correcto: `codigo_dba` es llave primaria.")
    w("")
    w("## 6. Análisis de normalización")
    w("")
    w("**Todas las tablas están en tercera forma normal, con tres excepciones deliberadas y")
    w("controladas.** En las de llave sustituta simple no hay dependencias parciales posibles; se")
    w("revisó que ningún atributo no clave dependa de otro no clave. En las de llave compuesta")
    w("(`evidencia`, `evidencia_dictamen`, `experiencia_evidencia`, `presentacion`,")
    w("`respuesta_opcion`, `resultado`), cada atributo no clave depende de la llave entera, salvo:")
    w("")
    w("| Dónde | Dependencia | Por qué se acepta |")
    w("|---|---|---|")
    w("| `presentacion.id_experiencia`, `resultado.id_experiencia`, `respuesta_opcion.id_item` | Dependen solo de una parte de la llave (`id_inscripcion`, `id_respuesta`): dependencia parcial, que viola la 2FN en sentido estricto. | Es la redundancia de 5.1 y 5.2. No puede quedar inconsistente: las FK compuestas la obligan a coincidir. A cambio, RI-13 y RI-6 son estructurales. |")
    w("| `experiencia.modelo_ia` → `experiencia.servicio_ia` | Un modelo pertenece a un solo servicio (dependencia transitiva). | Los dos son el registro de lo que ocurrió al generar el banco (RF-03-03), no datos que se editen. Normalizar exigiría una tabla de modelos sin ningún otro uso. Pasarlos de `item` a `experiencia` (5.3) ya quitó la repetición mayor. |")
    w("| `respuesta.correcta`, `resultado.estado` | Derivados de otras filas. | ADR-021: se guardan a propósito, como fotografía del momento (RNF-11). RI-11 exige que coincidan con el recálculo. |")
    w("")
    w("## 7. Restricciones de integridad: quién hace cumplir cada una")
    w("")
    w("Una restricción que la base puede hacer cumplir, la hace cumplir la base. Las demás")
    w("dependen de datos de otra tabla —un CHECK de MySQL no puede consultarlas— o del momento en")
    w("que ocurre algo, y las hace cumplir el servicio de la capa NestJS que se nombra; no se usan")
    w("triggers, para que cada regla de negocio viva en un solo lugar y se pueda probar.")
    w("")
    w("| RI | Mecanismo | Dónde |")
    w("|---|---|---|")
    for ri, mec, donde in RI_MECANISMO:
        w(f"| {ri} | {mec} | {donde} |")
    w("")
    w("**Restricciones de dominio (CHECK)** — expresión de MySQL:")
    w("")
    for i, (t, expr, desc, fuente) in enumerate(CHECKS):
        w(f"- `{t}`: `{expr_de(expr, 'mysql')}` — {desc}. *{fuente}*")
    w("")
    w("Además, cada columna `ENUM` restringe su dominio, y el modo estricto de MySQL (activo por")
    w("defecto) rechaza un valor fuera de él en vez de truncarlo.")
    w("")
    w("**UNIQUE:**")
    w("")
    for t, cols, razon in UNICOS:
        w(f"- `{t}({', '.join(cols)})` — {razon}")
    w("")
    w("## 8. Índices")
    w("")
    w("Toda llave primaria y todo UNIQUE ya es un índice. Se agrega uno por cada llave foránea cuyas")
    w("columnas no encabezan ya alguno de ellos:")
    w("")
    for t in TABLAS:
        for cols in indices_extra(t["tabla"]):
            w(f"- `{t['tabla']}({', '.join(cols)})`")
    w("")
    w(VERIFICACION.format(N_SQLITE=N_SQLITE, N_MYSQL=N_MYSQL, N_FALLA=N_PRUEBA["FALLA"],
                          N_PASA=N_PRUEBA["PASA"], N_QUEDA=N_PRUEBA["QUEDA"]))
    w(CAMBIOS)
    return "\n".join(L) + "\n"


RI_MECANISMO = [
    ("RI-1", "Motor: `UNIQUE(id_estudiante, id_experiencia)`", "`inscripcion`"),
    ("RI-2", "Motor: la llave primaria de la entidad débil", "`resultado`"),
    ("RI-3", "Motor: `UNIQUE(correo)` con cotejamiento sin mayúsculas; `UNIQUE(codigo_invitacion)` y CHECK del alfabeto", "`credencial`, `experiencia`"),
    ("RI-4", "Servicio: depende del formato, que está en otra tabla", "`Item.esValido()` (CU-16, CU-18, CU-20)"),
    ("RI-5", "Servicio: al crear la experiencia, solo entran las evidencias admitidas", "`DBA.evidenciasAdmitidas()` (CU-11, CU-16)"),
    ("RI-6", "Motor: que la opción sea del ítem presentado, con `id_item` en las dos FK compuestas de `respuesta_opcion` (sección 5.2). Servicio: al menos una opción, y exactamente una en selección única", "`respuesta_opcion` · `ServicioDiagnostico.responder()`, `Item.evaluar()` (CU-24)"),
    ("RI-7", "Servicio: al unirse", "`ServicioDiagnostico.unirse()` (CU-22)"),
    ("RI-8", "Motor: `UNIQUE(id_inscripcion, orden_presentacion)` y `CHECK(orden_presentacion > 0)`", "`presentacion`"),
    ("RI-9", "Servicio: la regla no presenta más de 6", "`ReglaAdaptativa` (CU-25)"),
    ("RI-10", "Servicio: el banco solo se edita en Borrador", "`Experiencia.bancoEditable()` (CU-17 a CU-20)"),
    ("RI-11", "Servicio: se calcula al escribir; verificable recalculando", "`Item.evaluar()`, `ReglaAdaptativa.concluir()`"),
    ("RI-12", "Motor: `CHECK(id_docente IS NULL OR id_estudiante IS NULL)` y UNIQUE sobre cada una", "`credencial`"),
    ("RI-13", "Motor: llaves foráneas compuestas con `id_experiencia` (sección 5.1)", "`presentacion`, `resultado`"),
    ("RI-14", "Servicio: al publicar, se comprueba otra vez", "`Experiencia.puedePublicarse()` (CU-13)"),
    ("RI-15", "Motor: CHECK, con `estado_verificacion = 'verificado'` (ADR-037)", "`credencial`"),
    ("RI-16", "Motor: CHECK", "`experiencia`"),
    ("RI-17", "Motor: un solo `servicio_ia` y un solo `modelo_ia`, NOT NULL, por experiencia: un banco no puede mezclar servicios", "`experiencia`"),
    ("RI-18", "Motor: FK compuesta `(id_experiencia, codigo_dba)` de `experiencia_evidencia` hacia `experiencia` (sección 5.2)", "`experiencia_evidencia`"),
    ("RI-20", "Motor: FK compuesta `(id_documento, codigo_area)` de `dba` hacia `documento_oficial` (sección 5.6)", "`dba`"),
    ("RI-21", "Motor: CHECK que arma `ÁREA-GG-NN` con el área y el grado de la fila; CHECK del formato de `codigo_area`; columnas ASCII binarias (sección 5.6)", "`dba`, `area`"),
    ("RI-19", "Motor: CHECK de que el dictamen que admite formato cerrado diga cuál. Servicio: el ítem usa el formato del dictamen al generarse y al crearse", "`evidencia_dictamen` · `GeneradorBanco`, `ServicioBanco.agregarItem()` (CU-16, CU-20)"),
]

VERIFICACION = """## 9. Verificación mecánica

Cuatro scripts, de menor a mayor fuerza. Desde `fase-3-diseno-computacional/modelo-relacional/`:

```bash
python generar.py
python _verificar_mr_mer.py
python verificar_mr.py
python probar_mysql.py --cnf RUTA_DEL_ARCHIVO_DE_OPCIONES --mysql RUTA_DE_mysql
```

| Script | Qué comprueba |
|---|---|
| `generar.py` | Escribe el diccionario (18), el DBML y los dos SQL desde la fuente. |
| `_verificar_mr_mer.py` | Que cada entidad del MER tenga su tabla y cada atributo su columna, con las mismas llaves primarias; que toda FK apunte a una PK o a un UNIQUE; que toda columna que el MER no declara tenga su justificación escrita (`EXTRA_JUSTIFICADAS`). |
| `verificar_mr.py` | Contra SQLite en memoria: que el esquema cargue, la batería de pruebas de `pruebas_mr.py`, y que el DBML y el SQL describan lo mismo. **{N_SQLITE} comprobaciones.** |
| `probar_mysql.py` | La **misma batería** contra un MySQL real: crea una base de prueba, carga `mr_mysql.sql` tal cual, corre cada prueba dentro de una transacción que se deshace, y borra la base al terminar. |

**La batería** (`pruebas_mr.py`) tiene tres clases de prueba: datos que rompen una regla y el
motor *debe rechazar* ({N_FALLA}), datos raros pero válidos que *debe aceptar* ({N_PASA}), y borrados tras
los que se cuenta qué *queda* en cada tabla ({N_QUEDA}: eliminar una experiencia, salir de una,
descartar un ítem). En MySQL, además, cada rechazo tiene que venir **de la restricción que la
prueba nombra** (`MOTIVO_MYSQL`): rechazar por otra razón cuenta como falla.

**Resultado del 2026-10-26, contra MySQL 8.0.46** (modo estricto por defecto), con el catálogo
normalizado y el estado de verificación: {N_MYSQL} comprobaciones, todas correctas. La salida
completa está en `modelo-relacional/salida_probar_mysql.txt`. La versión anterior del esquema
se había probado el 2026-10-22 contra MySQL 8.4.11; esta todavía no se corrió en 8.4 ni en
MariaDB.

**Lo que encontró.** La primera corrida contra MySQL mostró que la prueba «resultado cuya
experiencia no es la de su inscripción» pasaba **por la razón equivocada**: el motor rechazaba
la fila por llave primaria duplicada, no por la FK de RI-13. SQLite no lo podía mostrar, porque
no nombra la restricción rota. Se corrigió la prueba y desde entonces cada rechazo se exige con
su restricción.
"""

CAMBIOS = """
## 10. Cambios respecto del borrador del MR (2026-09-19)

| Cambio | Fuente |
|---|---|
| Tabla nueva `credencial`, con los contadores de intentos y el bloqueo que el backend de I1 ya usa. | V-8 · MER (Credencial) · backend I1 |
| `docente` / `estudiante`: `nombres` y `apellidos`; sin `correo`. | MER |
| `item`: `origen` con tres valores; sin `estado_revision` (el único dominio abierto del borrador, V-7). | MER |
| `experiencia`: `servicio_ia` y `modelo_ia`, los del banco entero (5.3). | RI-17 · RF-03-02 |
| `evidencia_dictamen`: `formato`, con su CHECK. | RI-19 · RF-03-01 |
| `experiencia_evidencia` y `respuesta_opcion`: FK compuestas que cierran los ciclos C1 y C4 del MER (5.2). | RI-18 · RI-6 |
| `experiencia_evidencia`: sin `incluida`. | MER |
| `presentacion`: `id_experiencia` y FK compuestas — cierra el hueco declarado. | RI-13 |
| Política de borrado en cascada desde `experiencia` e `inscripcion`; `presentacion → item` y `respuesta_opcion → opcion` pasan de RESTRICT a CASCADE, para que eliminar una experiencia con respuestas sea posible (RF-02-07). | V-11 |
| CHECK escritos como expresiones SQL reales, con nombre (antes eran prosa). | — |
| Motor objetivo MySQL 8 (antes MariaDB 10.11), con un DDL propio y probado. | RNF-14 |
| *(2026-10-26)* Tablas nuevas `area`, `grado` y `documento_oficial`; `dba` pierde `area` y `grado` como texto y gana `codigo_area`, `numero_grado` e `id_documento`, con una FK compuesta que cierra el ciclo C6 (RI-20). `codigo_dba` pasa a `ÁREA-GG-NN`, con su CHECK (RI-21), en ASCII binario en todas las tablas que lo usan (5.6). | ADR-036 · revisión del docente del 2026-10-22 (R1) |
| *(2026-10-26)* `credencial`: `email_verificado` pasa a `estado_verificacion` (`procesando` / `verificado`, por defecto `procesando`); el CHECK de RI-15 usa el estado. `codigo_expira_en` y `codigo_ultimo_envio` siguen, a la espera de la pregunta P2. | ADR-037 · revisión del docente del 2026-10-22 (R3, R4) |
"""

if __name__ == "__main__":
    txt = documento()
    with open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(txt)
    print(f"generado: 17-modelo-relacional.md ({len(txt.splitlines())} líneas)")
