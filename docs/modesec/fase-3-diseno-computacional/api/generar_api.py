"""Genera ../20-catalogo-endpoints.md desde datos_api.py.

Los endpoints, su CRUD y sus reglas salen de `datos_api.py`; en que diagrama
de secuencia aparece cada uno y que borra en cascada cada DELETE se calculan
(`calculos.py`). La coherencia con casos de uso, clases, matriz CRUD y
secuencias la comprueba `_verificar_api.py`.

Uso:  python generar_api.py
"""
import os

import calculos as K
from calculos import A, CU, ENDPOINTS, nombre

SALIDA = os.path.join(K.AQUI, "..", "20-catalogo-endpoints.md")
FECHA = "2026-10-22"
GENERADO = "**Archivo generado** por `api/generar_api.py`; no se edita a mano."
VERBO = {"C": "crea", "R": "lee", "U": "modifica", "D": "borra"}


def cel(t):
    return str(t).replace("|", "\\|")


def toca(crud):
    if not crud:
        return "nada guardado"
    return "; ".join(f"{ent} ({', '.join(VERBO[L] for L in letras)})"
                     for ent, letras in crud.items())


def cuenta(eps):
    return {k: sum(e["estado"] == k for e in eps) for k in A.ESTADOS}


def tabla(w, eps):
    # la marca da a la tabla la clase `endpoints` en el PDF (herramientas/md_a_pdf.py)
    w("<!-- tabla:endpoints -->")
    w("| N.º | Endpoint | Casos de uso | Operación | Quién | Estado |")
    w("|---|---|---|---|---|---|")
    for e in eps:
        w(f"| **{K.numero(e)}** | `{cel(nombre(e))}` | {'<br>'.join(e['cus'])} | `{e['op']}` | "
          f"{A.ACCESOS[e['acceso']][0]} | {A.ESTADOS[e['estado']]} |")
    w("")


def detalle(w, e):
    _, m = K.operacion(e["op"])
    clase = e["op"].split(".")[0]
    w(f"#### {K.numero(e)} · `{nombre(e)}`")
    w("")
    cus = " · ".join(f"{c} {CU.POR_ID[c]['nombre']}" for c in e["cus"])
    sec = K.secuencias(e)
    linea = f"{cus}. Operación: `{clase}.{m['firma']}`"
    if sec:
        linea += "; se ve en `15` " + " y ".join(f"§{s.split('-')[1]}" for s in sec)
    w(linea + f". **{A.ESTADOS[e['estado']]}.**")
    w("")
    w(f"- **Quién:** {A.ACCESOS[e['acceso']][0]}.")
    w(f"- **Recibe:** {e['recibe']}.")
    w(f"- **Responde:** {e['responde']}.")
    w(f"- **Toca:** {toca(e['crud'])}.")
    casc = K.cascada(e)
    if casc:
        w(f"- **Borra en cascada** (de las llaves foráneas de `17`): {', '.join(casc)}.")
    if e["reglas"]:
        w("- **Reglas y errores:**")
        for cod, txt in e["reglas"]:
            w(f"  - `{cod}` {txt}." if cod != "—" else f"  - {txt[0].upper() + txt[1:]}.")
    if e["nota"]:
        etiqueta = {"ajustar": "Qué ajustar", "opcional": "Por qué es opcional"}.get(
            e["estado"], "Nota")
        w(f"- **{etiqueta}:** {e['nota']}")
    w("")


def documento():
    L = []
    w = L.append
    tot = cuenta(ENDPOINTS)
    w("# 20. Catálogo de endpoints")
    w("")
    w("**Metodología:** MODESEC — Fase III, Diseño Computacional. Anexo: no es una sub-etapa de")
    w(f"MODESEC. **Fecha:** {FECHA}. {GENERADO}")
    w("")
    w("MODESEC cierra el diseño computacional con el modelado de la base de datos; no pide")
    w("describir lo que el frontend le pide al backend. Este anexo lo describe porque es lo primero")
    w("que hace falta para construir (Fase IV). Cada endpoint dice qué caso de uso atiende")
    w("(`12`), qué operación del diagrama de clases lo resuelve (`13`), en qué diagrama de")
    w("secuencia se ve (`15`), qué entidades crea, lee, modifica o borra —las mismas de la matriz")
    w("CRUD de `16` §7—, quién puede llamarlo y si ya existe en el backend del incremento I1.")
    w("")
    w("Es, casi literalmente, la lista de tareas de cada incremento: cada endpoint lleva un número,")
    w(f"de E-01 a E-{len(ENDPOINTS):02d}, para repartirlo.")
    w("")

    # -------------------------------------------------------------- 1
    w("## 1. En cifras")
    w("")
    w("| Incremento | Subsistemas | Endpoints | Hechos en I1 | Por ajustar | Faltan | Opcionales |")
    w("|---|---|---|---|---|---|---|")
    for inc, titulo in A.INCREMENTOS.items():
        eps = [e for e in ENDPOINTS if K.incremento(e) == inc]
        subs = sorted({e["sub"] for e in eps})
        c = cuenta(eps)
        w(f"| **{inc} — {titulo}** | {', '.join(subs)} | {len(eps)} | {c['hecho']} | "
          f"{c['ajustar']} | {c['falta']} | {c['opcional']} |")
    w(f"| **Total** | | **{len(ENDPOINTS)}** | **{tot['hecho']}** | **{tot['ajustar']}** | "
      f"**{tot['falta']}** | **{tot['opcional']}** |")
    w("")
    w(f"De los {len(ENDPOINTS)}, {tot['hecho'] + tot['ajustar']} ya existen en el backend I1")
    w("(`backend/` del repositorio): lo dice su código, revisado el 2026-10-26.")
    w(f"{tot['ajustar']} de ellos funcionan, pero el diseño les pide algo distinto. Los")
    w("incrementos I2, I3 e I4 están por construir.")
    w("")

    # -------------------------------------------------------------- 2
    w("## 2. Convenciones")
    w("")
    w("### 2.1 Quién puede llamar")
    w("")
    w("Todo token es un JWT en la cabecera `Authorization: Bearer`; su tipo va dentro. Quién")
    w("puede llamar sale del actor del caso de uso: un endpoint de un caso de uso del Docente no")
    w("lo llama un Estudiante, y el verificador lo comprueba.")
    w("")
    w("| Acceso | Quién |")
    w("|---|---|")
    for corto, largo in A.ACCESOS.values():
        w(f"| **{corto}** | {largo} |")
    w("")
    w("### 2.2 Errores")
    w("")
    w("| Código | Cuándo |")
    w("|---|---|")
    for cod, txt in A.ERRORES:
        w(f"| `{cod}` | {txt} |")
    w("")
    w("Un endpoint que no es del dueño responde `403`, no `404`, como ya lo hace I1. Los mensajes")
    w("de error van en español y nunca afirman certeza sobre el aprendizaje (RNF-02, RNF-04).")
    w("")
    w("### 2.3 Nombres")
    w("")
    w("Las rutas y los campos nuevos van en español, con los nombres del MER y del MR")
    w("(`experiencias`, `inscripciones`, `codigo_dba`, `certeza`): un mismo dato no cambia de")
    w("nombre entre la base, el backend y este catálogo. Las cuatro rutas que I1 heredó de la guía")
    w("del curso en inglés —`/auth/register`, `/auth/login`, `/auth/profile`, `/users/:id`—, y sus")
    w("campos `email`, `password` y `role`, se dejan como están: ya los usan el backend I1 y su")
    w("colección de pruebas. Unificarlas es una decisión del equipo; si se toma, se hace en un solo")
    w("cambio y se corrige aquí.")
    w("")
    w("En **Toca**, las entidades son las del MER (`16`): REPORTE no es una tabla, se calcula al")
    w("abrirlo (ADR-022).")
    w("")

    # -------------------------------------------------------- 3 a 6
    n = 3
    for inc, titulo in A.INCREMENTOS.items():
        eps = [e for e in ENDPOINTS if K.incremento(e) == inc]
        subs = list(dict.fromkeys(e["sub"] for e in eps))
        w(f"## {n}. {inc} — {titulo}")
        w("")
        if len(subs) == 1:
            tabla(w, eps)
            for e in eps:
                detalle(w, e)
        else:
            for i, sub in enumerate(subs, start=1):
                w(f"### {n}.{i} {sub} · {CU.SUBSISTEMAS[sub][0]}")
                w("")
                de_sub = [e for e in eps if e["sub"] == sub]
                tabla(w, de_sub)
                for e in de_sub:
                    detalle(w, e)
        n += 1

    # -------------------------------------------------------------- 7
    w(f"## {n}. En el backend I1, pero no del producto")
    w("")
    w("El backend I1 trae también rutas que vienen de la guía del curso (JWT). AdaptiveLearn")
    w("no tiene rol de administrador (`10` §2.2), así que no son del producto: se quitan antes de")
    w("entregarlo, o se dejan solo en desarrollo.")
    w("")
    w("| Ruta | Qué es |")
    w("|---|---|")
    for ruta, que in A.AJENOS_I1:
        w(f"| `{ruta}` | {que} |")
    w("")
    n += 1

    # -------------------------------------------------------------- 8
    w(f"## {n}. Adicionales que conviene agregar")
    w("")
    w("No los pide ningún requerimiento; ayudan a construir, a probar o a presentar. Ninguno cambia")
    w("lo que el sistema hace.")
    w("")
    w("| Qué | Para qué | Efecto en el MER |")
    w("|---|---|---|")
    for que, para, mer in A.ADICIONALES:
        w(f"| {cel(que)} | {cel(para)} | {cel(mer)} |")
    w("")
    n += 1

    # -------------------------------------------------------------- 9
    w(f"## {n}. Lo que no se debe agregar")
    w("")
    w("Contradice una decisión ya tomada. El verificador comprueba que ninguna ruta del catálogo lo")
    w("haga.")
    w("")
    w("| No agregar | Por qué |")
    w("|---|---|")
    for r in A.NO_AGREGAR:
        w(f"| {r['que']} | {r['fuente']} |")
    w("")
    n += 1

    # ------------------------------------------------------------- 10
    w(f"## {n}. Operaciones de servicio sin ruta propia")
    w("")
    w("Toda operación de una clase «servicio» del diagrama de clases tiene su endpoint, salvo estas:")
    w("")
    for op, razon in A.INTERNOS.items():
        w(f"- `{op}()`: {razon}")
    w("")
    n += 1

    # ------------------------------------------------------------- 11
    w(f"## {n}. Decisiones de este catálogo")
    w("")
    w("- **La foto viaja con el perfil**, en multipart/form-data, en `POST /auth/elegir-rol` y en")
    w("  `PATCH /users/:id`. CU-04 dice que el perfil se guarda al elegir el rol, y una ruta aparte")
    w("  para subir la foto no tendría ni operación ni caso de uso propios.")
    w("- **Las 4 áreas no tienen endpoint:** son fijas (CU-11 paso 1).")
    w("- **La siguiente pregunta es `POST`, no `GET`:** cada llamada puede crear una presentación.")
    w("  Un `GET` que escribe se repetiría solo con cualquier recarga o caché.")
    w("- **El diagrama de clases ganó tres operaciones** que la IGU necesita y no estaban:")
    w("  `ServicioAcceso.perfil()` (CU-09), `ServicioDiagnostico.misInscripciones()` (CU-21) y")
    w("  `ServicioDiagnostico.consultar()` (CU-23, CU-26). `ServicioExperiencias.consultar()`")
    w("  atiende también CU-13 y CU-15, como ya lo mostraban las secuencias 4 y 8 (`13`, `15`).")
    w("- **La matriz CRUD** registra que CU-23 también lee OPCION: presentar un ítem muestra sus")
    w("  opciones (`16` §7).")
    w("")
    n += 1

    # ------------------------------------------------------------- 12
    w(f"## {n}. Cómo se comprueba")
    w("")
    w("`python api/_verificar_api.py` comprueba:")
    w("")
    w("- **Trazabilidad:** todo caso de uso tiene al menos un endpoint. La operación de cada uno")
    w("  existe en una clase «servicio» y atiende uno de sus casos de uso. Toda operación de")
    w("  servicio tiene ruta, o está en la sección anterior. Toda llamada de la IGU en los")
    w("  diagramas de secuencia es un endpoint de aquí.")
    w("- **Datos:** lo que toca cada endpoint sale de la matriz CRUD de sus casos de uso, y todo lo")
    w("  que un caso de uso hace lo hace alguno de sus endpoints. `GET` solo lee, `DELETE` borra y")
    w("  `PATCH` modifica. Ningún endpoint modifica un hecho (RNF-10, RNF-11) ni borra lo que")
    w("  ningún flujo borra.")
    w("- **Acceso e incremento:** quien llama es el actor del caso de uso, y cada endpoint cae en")
    w("  un solo incremento. Solo I1 tiene endpoints hechos.")
    w("- **Rutas:** ninguna repetida, ninguna de la sección «Lo que no se debe agregar», y las")
    w("  nuevas en español.")
    w("")
    w("La secuencia en que se ve cada endpoint y lo que borra cada `DELETE` no se escriben a mano:")
    w("se calculan de `uml/datos_secuencias.py` y de las llaves foráneas del modelo relacional.")
    w("")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    with open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(documento())
    print(f"generado: 20-catalogo-endpoints.md ({sum(1 for _ in open(SALIDA, encoding='utf-8'))} líneas)")
