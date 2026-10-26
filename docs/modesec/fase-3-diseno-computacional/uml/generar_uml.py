"""Genera los diagramas UML y los documentos 12 a 15 de la Fase III.

  svg/*.svg                      los 19 diagramas
  ../12-casos-de-uso.md
  ../13-diagrama-clases.md
  ../14-diagrama-objetos.md
  ../15-diagramas-secuencia.md
  uml-fase3.html                 todos los diagramas en una pagina, para presentar

Todo sale de los `datos_*.py` de esta carpeta. Un diagrama con un problema
de geometria (texto encaramado, linea que atraviesa una caja) no se escribe:
el generador se detiene y dice cual. La coherencia con el MR, el MER y el
analisis de requerimientos la comprueba `_verificar_uml.py`.

Uso:  python generar_uml.py
"""
import os
import re
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
FASE3 = os.path.join(AQUI, "..")
sys.path.insert(0, AQUI)

import diagramas_cu                                             # noqa: E402
import diagramas_clases                                         # noqa: E402
import diagramas_objetos                                        # noqa: E402
import diagramas_secuencia                                      # noqa: E402
import datos_casos_uso as CU                                    # noqa: E402
import datos_clases as CL                                       # noqa: E402
import datos_objetos as OB                                      # noqa: E402
import datos_secuencias as SQ                                   # noqa: E402

FECHA = "2026-10-21"
GENERADO = "**Archivo generado** por `uml/generar_uml.py`; no se edita a mano."


def cel(t):
    return str(t).replace("|", "\\|")


def img(archivo, alt):
    return f"![{alt}](uml/svg/{archivo})"


# ============================================================ diagramas
def diagramas():
    todos = (diagramas_cu.todos() + diagramas_clases.todos() + diagramas_objetos.todos()
             + diagramas_secuencia.todos())
    malos = []
    for archivo, _, L in todos:
        p = L.verificar()
        if p:
            malos.append((archivo, p))
    if malos:
        for archivo, p in malos:
            print(f"GEOMETRIA: {archivo}")
            for x in p:
                print(f"   · {x}")
        sys.exit(1)
    os.makedirs(os.path.join(AQUI, "svg"), exist_ok=True)
    for archivo, _, L in todos:
        with open(os.path.join(AQUI, "svg", archivo), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(L.svg())
    return todos


# ============================================================ 12 · CU
def doc_casos_uso():
    L = []
    w = L.append
    w("# 12. Casos de uso")
    w("")
    w("**Metodología:** MODESEC — Fase III, Diseño Computacional, tercera sub-etapa.")
    w(f"**Fecha:** {FECHA}. {GENERADO}")
    w("")
    w("MODESEC define el caso de uso como la especificación del *«comportamiento de un sistema o")
    w("de una parte del mismo»*, una *«descripción de un conjunto de secuencias de acciones,")
    w("incluyendo variantes, que ejecuta un sistema para producir un resultado observable de")
    w("valor para un actor»*, y les pide dos objetivos: *«Definir los requisitos funcionales del")
    w("sistema y proporcionar una base para la validación de las pruebas»*. Por eso cada caso de")
    w("uso de este documento dice qué requerimientos de `11-analisis-requerimientos.md` cubre, y")
    w("trae una **prueba de aceptación**: un caso concreto que, al construir el incremento, dice")
    w("si quedó bien hecho.")
    w("")
    n_rf = len({r for c in CU.CASOS for r in c["rf"] if r.startswith("RF")})
    w(f"**{len(CU.CASOS)} casos de uso** en **7 diagramas** (uno general y uno por subsistema). "
      f"Cubren los **{n_rf} requerimientos funcionales** del análisis, sin excepción.")
    w("")
    w("## 1. Actores")
    w("")
    w("| Actor | Quién es |")
    w("|---|---|")
    for a, d in CU.ACTORES.items():
        w(f"| **{a}** | {d} |")
    w("")
    w("## 2. Cómo leer los diagramas")
    w("")
    w("- **Elipse:** un caso de uso. **Monigote:** un actor. **Rectángulo «AdaptiveLearn»:** el límite del sistema.")
    w("- **«include»** (flecha punteada): el caso de origen **siempre** ejecuta al de destino — por ejemplo, registrarse siempre incluye verificar el correo.")
    w("- **«extend»** (flecha punteada): el caso de origen se agrega al de destino **solo bajo la condición** entre corchetes — por ejemplo, completar perfil extiende a entrar con Google solo si la cuenta es nueva.")
    w("- **Elipse punteada y crema:** un caso de uso de otro diagrama, dibujado por referencia para mostrar un «include» o un «extend». Cada caso de uso es *propio* de un solo diagrama: misma regla de las costuras del MER.")
    w("- **Triángulo hueco:** generalización entre actores. Docente y Estudiante son Usuarios.")
    w("")
    w("## 3. Diagramas")
    w("")
    for archivo, titulo, _ in diagramas_cu.todos():
        w(f"### {titulo}")
        w("")
        w(img(archivo, titulo))
        w("")
    w("## 4. Resumen por subsistema")
    w("")
    w("| Subsistema | Incremento | Casos de uso |")
    w("|---|---|---|")
    por_sub = defaultdict(list)
    for c in CU.CASOS:
        por_sub[c["sub"]].append(c["id"])
    for sub, (nombre, inc) in CU.SUBSISTEMAS.items():
        w(f"| **{sub}** {nombre} | {inc} | {', '.join(sorted(por_sub[sub]))} |")
    w("")
    w("## 5. Especificación de cada caso de uso")
    w("")
    for sub, (nombre, inc) in CU.SUBSISTEMAS.items():
        w(f"### {sub} — {nombre}")
        w("")
        for c in sorted((c for c in CU.CASOS if c["sub"] == sub), key=lambda c: c["id"]):
            w(f"#### {c['id']} — {c['nombre']}")
            w("")
            w("| Actor | Actores secundarios | Requerimientos | Ventanas | Incremento |")
            w("|---|---|---|---|---|")
            w(f"| {c['actor']} | {', '.join(c['secundarios']) or '—'} | {', '.join(c['rf'])} | "
              f"{', '.join(c['ventanas'])} | {inc} |")
            w("")
            rel = [f"«{t}» {d}" + (f" [{g}]" if g else "") for o, t, d, g in CU.RELACIONES if o == c["id"]]
            rel += [f"lo {'incluye' if t == 'include' else 'extiende'} {o}"
                    for o, t, d, g in CU.RELACIONES if d == c["id"]]
            if rel:
                w(f"**Relaciones:** {'; '.join(rel)}.")
                w("")
            w(f"**Precondición:** {c['pre']}")
            w("")
            w("**Flujo principal**")
            w("")
            for i, paso in enumerate(c["flujo"], 1):
                w(f"{i}. {paso}")
            w("")
            if c["alternos"]:
                w("**Flujos alternos**")
                w("")
                for a in c["alternos"]:
                    w(f"- {a}")
                w("")
            w(f"**Postcondición:** {c['post']}")
            w("")
            w(f"**Prueba de aceptación:** {c['prueba']}")
            w("")
            for n in c["notas"]:
                w(f"> {n}")
                w("")
    w("## 6. Trazabilidad: requerimiento → casos de uso")
    w("")
    w("| Requerimiento | Casos de uso |")
    w("|---|---|")
    traza = defaultdict(list)
    for c in CU.CASOS:
        for r in c["rf"]:
            traza[r].append(c["id"])
    for r in sorted(traza, key=lambda r: (r.startswith("RNF"), r)):
        w(f"| {r} | {', '.join(sorted(traza[r]))} |")
    w("")
    w("Los requerimientos no funcionales no se convierten en casos de uso: condicionan a varios a")
    w("la vez. Aparecen citados donde un caso de uso los hace cumplir (por ejemplo RNF-07 en")
    w("CU-07, RNF-12 en CU-11).")
    w("")
    w("## 7. Decisiones y vacíos que este documento declara")
    w("")
    w("Lo que los requerimientos no decían y hacía falta para escribir un flujo completo. No se")
    w("rellenó en silencio: queda aquí, para que el equipo lo confirme o lo cambie.")
    w("")
    w("| Dónde | Qué | Tipo |")
    w("|---|---|---|")
    w("| CU-06, alterno 3a | Una credencial sin rol (registro sin terminar) que inicia sesión retoma el registro en completar perfil. | Decisión |")
    w("| CU-16, alterno 4a | Un ítem generado que no pasa la validación se trata como falla de ese servicio: se pasa al de respaldo. Mantiene el «todo o nada» de ADR-027. | Decisión |")
    w("| CU-31, nota | Qué muestra la pantalla si **ninguna** evidencia de un DBA admite formato cerrado. Depende del censo QA-014. | Vacío nuevo: **V-12** |")
    w("| CU-15 y CU-26 | Qué pasa con los datos al eliminar o salir de una experiencia: se borran en cascada. | **Cierra V-11** (en el modelo relacional) |")
    w("")
    w("## 8. Verificación")
    w("")
    w("`python uml/_verificar_uml.py`, bloque A: los 44 RF cubiertos; ningún RF, RNF ni ventana")
    w("citado que no exista en `11`; cada caso de uso en el subsistema de sus RF y dibujado como")
    w("propio en exactamente un diagrama; y cada «se incluye CU-xx» de un flujo dibujado como")
    w("«include», y al revés.")
    w("")
    return "\n".join(L) + "\n"


# ========================================================== 13 · clases
def doc_clases():
    L = []
    w = L.append
    w("# 13. Diagrama de clases")
    w("")
    w("**Metodología:** MODESEC — Fase III, Diseño Computacional, cuarta sub-etapa.")
    w(f"**Fecha:** {FECHA}. {GENERADO}")
    w("")
    w("MODESEC: los diagramas de clases *«se utilizan para modelar la vista de diseño estático de")
    w("un sistema»*, *«resultan de la composición de los casos de uso»* y deben expresar *«detalles")
    w("de los objetos que existen en el área de enfoque»*, con *«atributos y métodos de cada una de")
    w("las clases»*. Las dos mitades de cada clase tienen, por eso, una fuente cada una:")
    w("")
    w("- **Atributos:** los del modelo relacional (`17-modelo-relacional.md`) **menos las columnas")
    w("  de llave foránea**: en un modelo de objetos, esas columnas son las asociaciones. Llevan")
    w("  los mismos nombres del MER y del MR, a propósito: un dato no cambia de nombre entre")
    w("  documentos.")
    w("- **Métodos:** cada uno sale de uno o más casos de uso de `12-casos-de-uso.md`, y lo dice.")
    w("  Todo caso de uso aporta al menos un método.")
    w("")
    n_dom = len(CL.CLASES)
    w(f"Dos diagramas: el **dominio** ({n_dom} clases, {len(CL.ENUMERACIONES)} enumeraciones,"
      f" {len(CL.ASOCIACIONES)} asociaciones) y los **servicios** ({len(CL.SERVICIOS)} clases de"
      f" control e interfaces), que son los objetos que aparecen en los diagramas de secuencia.")
    w("")
    w("## 1. Decisiones de diseño")
    w("")
    w("| Decisión | Por qué |")
    w("|---|---|")
    w("| **Usuario**, abstracta, generaliza a Docente y Estudiante | Tienen los mismos datos de perfil y la misma edición (CU-09). Es abstracta porque no hay usuarios sin rol, y en la base no tiene tabla: Docente y Estudiante son tipos separados (RF-01-06), cada uno con la suya. |")
    w("| **RespuestaOpcion** es clase asociación de «selecciona» | Una respuesta elige varias opciones, y en emparejar y ordenar cada elección lleva un valor (`valor_dado`). Es la entidad asociativa del MER. |")
    w("| **Reporte** es «calculada» | No persiste (ADR-022): sus atributos son derivados (`/`) y sus asociaciones también. |")
    w("| La regla adaptativa vive en **ReglaAdaptativa**, no en Resultado | Un resultado es una fotografía (RNF-11): no se recalcula a sí mismo. Quien decide es un servicio, y el resultado guarda lo que decidió. |")
    w("| `servicio_ia` y `modelo_ia` son de **Experiencia**, no de Item | Un banco sale entero de un solo servicio (RF-03-02): guardarlo en cada ítem lo repetía y dejaba que un banco mezclara servicios. El servicio de un ítem generado o editado es el de su experiencia (RF-03-03, RI-17). |")
    w("| **Usuario** existe aquí y no en el MER | Es una abstracción de diseño de objetos: agrupa lo que Docente y Estudiante hacen igual. En el MER y en la base siguen siendo dos entidades separadas, por la decisión del equipo de que la estructura impida asignar un estudiante como creador (ver `16`, «El MER y el diagrama de clases»). |")
    w("| **GeneradorBanco** depende de la interfaz **ServicioGeneracion** | Gemini y DeepSeek la realizan; cuál es el principal y cuál el respaldo es configuración (RF-03-02, ADR-030), no código. |")
    w("")
    w("## 2. Diagrama 1 · Dominio")
    w("")
    w(img("clases-1-dominio.svg", "Diagrama de clases del dominio"))
    w("")
    w("## 3. Diagrama 2 · Servicios")
    w("")
    w(img("clases-2-servicios.svg", "Diagrama de clases de los servicios"))
    w("")
    w("## 4. Clases del dominio")
    w("")
    for c in CL.CLASES:
        est = f" «{c['estereotipo']}»" if c["estereotipo"] else ""
        abst = " {abstracta}" if c["abstracta"] else ""
        w(f"### {c['nombre']}{est}{abst}")
        w("")
        origen = (f"Tabla `{c['tabla']}` · entidad {c['entidad']} del MER" if c["tabla"] else
                  "Sin tabla" + (f" · entidad {c['entidad']} del MER" if c["entidad"] else ""))
        w(f"*{origen}.* {c['desc']}")
        w("")
        if c["atributos"]:
            w("| Atributo | Tipo |")
            w("|---|---|")
            for a, t in c["atributos"]:
                w(f"| `{a}` | {cel(t)} |")
            w("")
        if c["metodos"]:
            w("| Método | Casos de uso |")
            w("|---|---|")
            for m in c["metodos"]:
                w(f"| `{cel(m['firma'])}` | {', '.join(m['cus'])} |")
            w("")
    w("## 5. Asociaciones")
    w("")
    w("Cada una es una relación del MER, con su mismo nombre. El verificador exige que estén")
    w("todas y ninguna más.")
    w("")
    w("| Clase A | Asociación | Clase B | Mult. A | Mult. B | Tipo |")
    w("|---|---|---|---|---|---|")
    for a, b, n, ma, mb, t in CL.ASOCIACIONES:
        w(f"| {a} | *{'/' if t == 'derivada' else ''}{n}* | {b} | {ma} | {mb} | {t} |")
    w("")
    w("Generalizaciones: " + "; ".join(f"{h} → {p}" for h, p in CL.GENERALIZACIONES) + ".")
    w("")
    w("## 6. Enumeraciones")
    w("")
    w("| Enumeración | Valores | Origen |")
    w("|---|---|---|")
    for n, vals, origen in CL.ENUMERACIONES:
        o = f"ENUM de `{origen[0]}.{origen[1]}`" if origen else "valor calculado, no se guarda"
        w(f"| {n} | {', '.join(vals)} | {o} |")
    w("")
    w("## 7. Servicios e interfaces")
    w("")
    for c in CL.SERVICIOS:
        est = f" «{c['estereotipo']}»" if c["estereotipo"] else ""
        w(f"### {c['nombre']}{est}")
        w("")
        if c["atributos"]:
            w("Atributos: " + ", ".join(f"`{a}: {t}`" for a, t in c["atributos"]) + ".")
            w("")
        w("| Operación | Casos de uso |")
        w("|---|---|")
        for m in c["metodos"]:
            w(f"| `{cel(m['firma'])}` | {', '.join(m['cus'])} |")
        w("")
    w("Dependencias: " + "; ".join(f"{a} «{t}» {b}" for a, b, t in CL.DEPENDENCIAS) + ".")
    w("")
    w("## 8. Verificación")
    w("")
    w("`python uml/_verificar_uml.py`, bloque B: los atributos de cada clase son exactamente las")
    w("columnas de su tabla sin las de llave foránea; cada tabla del MR tiene su clase; cada")
    w("enumeración es el ENUM de su columna, valor por valor; las asociaciones son las relaciones")
    w("del MER con las mismas entidades; y todo caso de uso aporta al menos un método. El bloque E")
    w("comprueba que toda operación que un diagrama de secuencia invoca esté declarada aquí.")
    w("")
    return "\n".join(L) + "\n"


# ========================================================= 14 · objetos
def doc_objetos():
    L = []
    w = L.append
    w("# 14. Diagrama de objetos")
    w("")
    w("**Metodología:** MODESEC — Fase III, Diseño Computacional, quinta sub-etapa.")
    w(f"**Fecha:** {FECHA}. {GENERADO}")
    w("")
    w("MODESEC: *«Un diagrama de objetos es un diagrama que representa un conjunto de objetos y")
    w("sus relaciones en un momento concreto.»* El momento elegido es el que más reglas pone a")
    w("prueba a la vez:")
    w("")
    w("> **Martes 4 de noviembre de 2026, 09:06.** Luis está respondiendo la experiencia que Ana")
    w("> publicó el día anterior. Ya concluyó la evidencia 1 —*Muestra*, en la 4.ª respuesta— y")
    w("> acaba de ver la primera pregunta de la evidencia 2, pero cerró la página sin responderla.")
    w("")
    w("Se dibuja en **dos vistas del mismo momento**, como el MER: la experiencia publicada (lo")
    w("que hizo Ana) y el diagnóstico de Luis (lo que hizo Luis). Un objeto que la segunda vista")
    w("necesita se dibuja allí como costura, sin repetir sus valores.")
    w("")
    w("## 1. Vista 1 · La experiencia publicada")
    w("")
    w(img("objetos-1-experiencia.svg", "Diagrama de objetos, vista 1"))
    w("")
    w("## 2. Vista 2 · El diagnóstico de Luis, en curso")
    w("")
    w(img("objetos-2-diagnostico.svg", "Diagrama de objetos, vista 2"))
    w("")
    w("## 3. Qué regla se ve en cada parte")
    w("")
    w("| Lo que muestra | Regla |")
    w("|---|---|")
    w("| `c1` tiene contraseña cifrada; `c2`, que entró con Google, no tiene contraseña, sí identificador del proveedor, y el correo verificado. | RI-15 · RF-01-02 |")
    w("| Cada credencial da acceso a un solo rol. | RI-12 |")
    w("| `exp3` está Publicada y tiene fecha de publicación; Luis se unió después. | RI-16 · RI-7 |")
    w("| Las dos evidencias del DBA tienen dictamen que admite formato cerrado, y por eso las dos están incluidas. | RI-5 · RF-06-02 |")
    w("| El servicio y el modelo de IA están en `exp3`, no en cada ítem: un banco sale entero de un solo servicio. `it12`, que editó Ana, sigue siendo de Gemini; `it21`, que creó Ana, no se le atribuye a la IA. | RI-17 · RF-03-02 · RF-03-03 |")
    w("| Las dos evidencias incluidas son del DBA al que se ancla `exp3`. | RI-18 (ciclo C1) |")
    w("| `d1` y `d2` fijan el formato `single_choice`, y los ítems de esas evidencias lo usan. | RI-19 · RF-03-01 |")
    w("| Las cinco presentaciones tienen órdenes 1 a 5, sin repetir, y cada ítem es de la experiencia de la inscripción. | RI-8 · RI-13 (ciclo C2) |")
    w("| `ro1` elige `op1`, que es una opción de `it11`: el ítem que se le presentó en `p1`. | RI-6 (ciclo C4) |")
    w("| Las preguntas de la evidencia 1 van antes que la de la evidencia 2. | ADR-024 |")
    w("| `p5` no tiene respuesta: es la que Luis verá al volver. | ADR-031 · RF-04-09 |")
    w("| `res1` dice *muestra*: con las certezas 4, 5, 1 y 3 (la tercera incorrecta), hay 3 señales fuertes de «muestra» en 4 respuestas. | RF-04-07 |")
    w("| No hay resultado de la evidencia 2: el estado general de Luis es *Sin concluir*, y no se guarda. | ADR-022 · RF-05-01 |")
    w("")
    w("## 4. Los objetos")
    w("")
    w("| Objeto | Clase | Valores en este momento |")
    w("|---|---|---|")
    for oid, (clase, valores) in OB.OBJETOS.items():
        vals = "; ".join(f"`{k} = {v}`" for k, v in valores) or "— (sin atributos propios)"
        w(f"| `{oid}` | {clase} | {cel(vals)} |")
    w("")
    w("Nombres, correos, códigos y el modelo de IA son **ilustrativos**. Lo que no es ilustrativo")
    w("es la estructura y que cada valor cumpla las reglas.")
    w("")
    w("## 5. Verificación: la fotografía se carga en el esquema real")
    w("")
    w("`python uml/_verificar_uml.py`, bloques C y D. Además de comprobar que cada atributo exista")
    w("en su clase y cada enlace sea una asociación del diagrama de clases, el verificador **carga")
    w("los objetos en `modelo-relacional/mr_esquema.sql`**: convierte cada objeto en una fila y cada")
    w("enlace en su llave foránea, y los inserta. Si la fotografía violara una sola restricción")
    w("—un ítem de otra experiencia, una credencial de Google con contraseña, un orden repetido—")
    w("el motor la rechazaría. Y recalcula el resultado de la evidencia 1 con la regla de RF-04-07")
    w("(`uml/regla.py`): tiene que dar *muestra* en la 4.ª respuesta, que es lo que dice `res1`.")
    w("")
    return "\n".join(L) + "\n"


# ======================================================= 15 · secuencias
def doc_secuencias():
    L = []
    w = L.append
    w("# 15. Diagramas de secuencia")
    w("")
    w("**Metodología:** MODESEC — Fase III, Diseño Computacional, sexta sub-etapa.")
    w(f"**Fecha:** {FECHA}. {GENERADO}")
    w("")
    w("MODESEC: *«Los Diagramas de Secuencia representan una interacción entre objetos de manera")
    w("secuencial en el tiempo […] El responsable o actor es quien inicia el ciclo interactuando")
    w("inicialmente con la interfaz de usuario (IGU); en seguida se inician todos los objetos que")
    w("intervienen en el funcionamiento del aplicativo.»* Cada diagrama, por eso, empieza en un")
    w("actor, pasa por la IGU —la ventana de la Fase II que corresponde— y de ahí a los servicios y")
    w("a las clases del dominio de `13-diagrama-clases.md`.")
    w("")
    w(f"**{len(SQ.SECUENCIAS)} diagramas**, elegidos por ser los flujos con más decisiones: los que")
    w("tienen ramas, repeticiones o reglas que el código tendrá que respetar al pie de la letra.")
    w("")
    w("| # | Diagrama | Casos de uso | Ventanas |")
    w("|---|---|---|---|")
    for s in SQ.SECUENCIAS:
        w(f"| {s['id'][-1]} | {s['titulo']} | {', '.join(s['cus'])} | {', '.join(s['ventanas'])} |")
    w("")
    w("**Cómo leerlos.** Flecha llena: un mensaje; si está escrito como llamada —`publicar(id)`—")
    w("es una operación declarada en el diagrama de clases, y el verificador lo comprueba. Flecha")
    w("punteada: una respuesta, o «create» (el objeto nace ahí: su cabecera aparece a esa altura).")
    w("Recuadros **alt** (alternativas), **opt** (opcional) y **loop** (repetición), con su condición")
    w("entre corchetes.")
    w("")
    for s in SQ.SECUENCIAS:
        w(f"## {s['id'][-1]}. {s['titulo']}")
        w("")
        w(SQ.EXPLICACION[s["id"]])
        w("")
        w(img(s["archivo"], s["titulo"]))
        w("")
        clase_de = {p[0]: p[2] for p in s["participantes"]}
        usadas = []
        for paso in s["pasos"]:
            if paso[0] in ("m", "s"):
                rec = paso[2] if paso[0] == "m" else paso[1]
                txt = paso[3] if paso[0] == "m" else paso[2]
                m = re.fullmatch(r"([a-zA-Z]+)\(.*\)", txt)
                if m and clase_de.get(rec):
                    op = f"{clase_de[rec]}.{m.group(1)}()"
                    if op not in usadas:
                        usadas.append(op)
        w("Operaciones del diagrama de clases que usa: " + ", ".join(f"`{u}`" for u in usadas) + ".")
        w("")
    w("## Verificación")
    w("")
    w("`python uml/_verificar_uml.py`, bloque E: toda llamada de estos diagramas es una operación")
    w("declarada en la clase de su receptor (heredadas incluidas), todo «create» es de una clase")
    w("que existe, y todo caso de uso y ventana citados existen.")
    w("")
    return "\n".join(L) + "\n"


# =============================================================== visor
def visor(todos):
    secciones = [
        ("Casos de uso", [a for a, *_ in diagramas_cu.todos()], "12-casos-de-uso.md"),
        ("Diagrama de clases", [a for a, *_ in diagramas_clases.todos()], "13-diagrama-clases.md"),
        ("Diagrama de objetos", [a for a, *_ in diagramas_objetos.todos()], "14-diagrama-objetos.md"),
        ("Diagramas de secuencia", [s["archivo"] for s in SQ.SECUENCIAS], "15-diagramas-secuencia.md"),
    ]
    explic = {s["archivo"]: SQ.EXPLICACION[s["id"]] for s in SQ.SECUENCIAS}
    partes = []
    indice = []
    for nombre, archivos, doc in secciones:
        ancla = nombre.lower().replace(" ", "-")
        indice.append(f'<a href="#{ancla}">{nombre}</a>')
        partes.append(f'<h2 id="{ancla}">{nombre} <span>· {doc}</span></h2>')
        for a in archivos:
            svg = open(os.path.join(AQUI, "svg", a), encoding="utf-8").read()
            cap = explic.get(a, "")
            # el titulo ya va dentro de cada SVG: no se repite como figcaption
            partes.append(f'<figure id="{a[:-4]}">{svg}'
                          + (f'<p>{cap}</p>' if cap else "") + "</figure>")
    html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Diagramas UML — Fase III</title>
<style>
  body {{ margin:0; padding:32px 40px; background:#FFFFFF; color:#111111; font-family:Helvetica,Arial,sans-serif; }}
  h1 {{ font-size:22px; margin:0 0 4px 0; }}
  p.sub {{ font-size:13px; color:#555555; margin:0 0 12px 0; }}
  nav {{ position:sticky; top:0; background:#FFFFFF; padding:10px 0; border-bottom:1px solid #E7E7E7; z-index:1; }}
  nav a {{ font-size:13px; color:#3B7DD8; margin-right:18px; text-decoration:none; }}
  h2 {{ font-size:18px; margin:40px 0 12px 0; }}
  h2 span {{ font-size:13px; color:#888888; font-weight:400; }}
  figure {{ margin:0 0 36px 0; }}
  figure svg {{ display:block; max-width:100%; height:auto; }}
  figure p {{ font-size:13px; color:#555555; max-width:1100px; margin:8px 4px 0 4px; }}
</style></head><body>
<h1>Diagramas UML — AdaptiveLearn, Fase III</h1>
<p class="sub">MODESEC, Diseño Computacional. Generado por <code>uml/generar_uml.py</code> desde las mismas fuentes que los documentos 12 a 15.</p>
<nav>{"".join(indice)}</nav>
{"".join(partes)}
</body></html>
"""
    with open(os.path.join(AQUI, "uml-fase3.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)


if __name__ == "__main__":
    todos = diagramas()
    print(f"{len(todos)} diagramas, geometría limpia")
    for nombre, contenido in [("12-casos-de-uso.md", doc_casos_uso()),
                              ("13-diagrama-clases.md", doc_clases()),
                              ("14-diagrama-objetos.md", doc_objetos()),
                              ("15-diagramas-secuencia.md", doc_secuencias())]:
        with open(os.path.join(FASE3, nombre), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(contenido)
        print(f"generado: {nombre}  ({len(contenido.splitlines())} líneas)")
    visor(todos)
    print("generado: uml/uml-fase3.html")
