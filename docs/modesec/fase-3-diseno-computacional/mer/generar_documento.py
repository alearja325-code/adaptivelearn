"""Genera ../16-modelo-entidad-relacion.md desde datos_mer.py.

Las tablas de entidades, relaciones y ciclos salen de la misma fuente que
los diagramas (`mapa_chen.py`, `construir_vistas.py`, `mapa_cajas.py`); la
matriz CRUD, de `../uml/datos_crud.py`, con el borrado en cascada calculado
de las llaves foraneas del modelo relacional. Asi el documento no puede
contar algo distinto de lo que esta dibujado o de lo que el esquema hace.
La prosa -- de donde sale cada cosa y por que -- vive aqui, junto a los
datos que explica.

Uso:  python generar_documento.py
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "uml"))
sys.path.insert(0, os.path.join(AQUI, "..", "modelo-relacional"))

from datos_mer import (ENTIDADES, RELACIONES, VISTAS, DEBILES, CICLOS,  # noqa: E402
                       N_ENTIDADES, N_REL_REALES, N_REL_DERIVADAS, N_ATRIBUTOS)
import datos_crud as CR                                              # noqa: E402
import datos_mr as MR                                                # noqa: E402

SALIDA = os.path.join(AQUI, "..", "16-modelo-entidad-relacion.md")
N_RI = 21

TIPO = {"propia": "Propia", "men": "Externa (MEN)", "asociativa": "Asociativa",
        "debil": "Débil", "derivada": "Derivada — no persiste"}
MARCA = {"PK": " (PK)", "PD": " (llave parcial)", "D": " (derivado, se guarda)",
         "C": " (calculado, no se guarda)", "": ""}

# ----------------------------------------------------------------- entidades
FICHA = {
    "CREDENCIAL": (
        "**Nueva en esta versión (cierra V-8).** La cuenta de acceso: con qué correo y qué método "
        "se entra, la verificación del correo y a qué rol da acceso. Existe desde «Crear cuenta», "
        "*antes* de que exista el docente o el estudiante: hace falta para guardar el código de "
        "verificación (RF-01-03), y el docente o el estudiante se crea recién al elegir el rol "
        "(RF-01-05, RF-01-06). El correo vive aquí y no en Docente/Estudiante: es el correo de la "
        "cuenta, y así su unicidad vale **entre los dos roles** (RF-01-04), cosa que dos UNIQUE "
        "separados no garantizan. Accede como docente **o** como estudiante, nunca como los dos "
        "({xor}, RI-12). Es la tabla que el incremento I1 ya construyó (`backend/sql/001_esquema_auth.sql`). "
        "**Cambia el 2026-10-26 (ADR-037):** el sí/no `email_verificado` pasa a "
        "**`estado_verificacion`**, con dos valores: `procesando` (se envió el código y no se ha "
        "confirmado) y `verificado`. Una credencial de Google o Microsoft nace `verificado` (RI-15). "
        "`codigo_expira_en` y `codigo_ultimo_envio` siguen: quitarlos (nota R4 del docente) espera "
        "su respuesta a la pregunta P2 (`21-revision-docente-2026-10-22.md`).",
        "Ventanas 014 a 019 · RF-01-01 a RF-01-09 · backend I1 · ADR-037"),
    "DOCENTE": (
        "Quien crea y publica experiencias. Separado de Estudiante como entidad propia (decisión "
        "del borrador, que se mantiene): la relación de cada uno con Experiencia es distinta "
        "—creador y miembro— y separarlos hace que la estructura impida asignar un estudiante "
        "como creador. **Cambia:** `nombre` pasa a `nombres` + `apellidos` y sale `correo`.",
        "04-spec-dashboard · 19-spec-auth-completa-perfil · 26-spec-modal-mi-perfil · RF-01-05, RF-01-11"),
    "ESTUDIANTE": (
        "Quien se une con un código y responde el diagnóstico. Solo los datos mínimos (ADR-029): "
        "nombres, apellidos y foto opcional; el correo está en su credencial. Mismo cambio que "
        "Docente.",
        "ADR-029 · RF-01-05 · RNF-05"),
    "EXPERIENCIA": (
        "Un diagnóstico anclado a un único DBA, creado por un docente. Se guarda solo si su banco "
        "se generó completo (ADR-027). `estado`: Borrador o Publicada, sin vuelta atrás (ADR-026). "
        "`fecha_publicacion` es nula mientras esté en Borrador (RI-16). `codigo_invitacion` se "
        "genera al crearla y se muestra solo publicada (RF-02-06). **`servicio_ia` y `modelo_ia`** "
        "dicen con qué servicio y modelo se generó su banco: un banco sale entero de un solo "
        "servicio (RF-03-02), así que es un dato de la experiencia y no de cada ítem (RI-17). "
        "Área y grado no son atributos: se derivan del DBA.",
        "07-spec-crear-experiencia-paso3 · 15-spec-modal-confirmar-publicar · 08-spec-unirse-codigo · "
        "ADR-026, ADR-027, ADR-030 · RF-03-02, RF-03-03"),
    "AREA": (
        "**Nueva (ADR-036).** Área del currículo con DBA en esta versión: Matemáticas (`MAT`), "
        "Lenguaje (`LEN`), Ciencias Naturales (`CN`) y Ciencias Sociales (`CS`), las cuatro de "
        "ADR-033. Antes era un texto suelto dentro de cada DBA, que nada impedía escribir mal. "
        "`codigo_area` no lleva tildes y encabeza el código de cada DBA (RI-21). Dato de "
        "referencia, de solo lectura.",
        "ADR-036 · ADR-033 · revisión del docente del 2026-10-22, R1"),
    "GRADO": (
        "**Nueva (ADR-036).** Grado escolar, de 1° a 11°, con su `nombre` (Primero a Undécimo) y su "
        "`nivel` de la educación formal: básica primaria (1° a 5°), básica secundaria (6° a 9°) o "
        "media (10° y 11°), según la Ley 115 de 1994. Sin Transición (ADR-033). En el modelo "
        "relacional, un CHECK ata el nivel al número.",
        "ADR-036 · ADR-033 · Ley 115 de 1994 · revisión del docente del 2026-10-22, R1"),
    "DOCUMENTO_OFICIAL": (
        "**Nueva (ADR-036).** El PDF del MEN del que se copiaron los DBA de un área: título, "
        "versión, año, páginas y dirección oficial. Uno por área en esta versión, con los datos "
        "que ADR-033 verificó contra los archivos oficiales: Matemáticas V.2 (88 páginas), "
        "Lenguaje V.2 (56), Ciencias Naturales V.1 (44) y Ciencias Sociales **V.1** (52), los "
        "cuatro de 2016. **La versión se lee del documento, nunca del nombre del archivo:** el de "
        "Ciencias Sociales se llama «v2» y su portada dice V.1 (ADR-033). Deja trazable que nada "
        "del catálogo se inventó. El documento de un DBA es de su misma área (RI-20, ciclo C6).",
        "ADR-036 · ADR-033"),
    "DBA": (
        "Derecho Básico de Aprendizaje oficial del MEN: dato externo, referenciado, de solo lectura "
        "(SUB-06). **Cambia el 2026-10-26 (ADR-036):** salen `area` y `grado` como texto; ahora "
        "*pertenece a* un ÁREA, *corresponde a* un GRADO y *se copia de* un DOCUMENTO_OFICIAL. "
        "**`codigo_dba` tiene el formato `ÁREA-GG-NN`**, con ceros a la izquierda y sin tildes "
        "(`MAT-01-01`, `CS-11-05`, RI-21): se arma con el código del área, el grado y el `numero` "
        "de cada DBA. Equivale al identificador viejo "
        "así: `matemáticas_1_dba_1` → `MAT-01-01`, `ciencias_naturales_2_dba_3` → `CN-02-03`. "
        "**Los DBA se cargan de `data/curriculo-men/catalogo/catalogo_dba.json`**, no de "
        "`curriculo_men_normalizado.json`: ese JSON viejo tenía 342 DBA y solo 329 identificadores "
        "distintos, porque la normalización de la V2 asignó al grado anterior el primer DBA de "
        "algunas páginas. El catálogo corregido (encargo 02, 2026-10-26; pendientes, A12) tiene "
        "343 DBA, cada uno en el grado del encabezado de su página y con código único. "
        "`codigo_dba` es llave única: el defecto se corrigió en los datos, no relajando el "
        "modelo. `ejemplo` se usa como contexto al generar el banco (ADR-011) y "
        "todavía falta en la normalización (QA-011).",
        "Glosario «DBA» · ADR-005, ADR-011, ADR-036 · RF-06-01"),
    "EVIDENCIA": (
        "Evidencia de aprendizaje de un DBA. **Débil**: sin su DBA no tiene identidad. Se "
        "identifica por la llave de su DBA (relación identificadora *comprende*) más su **llave "
        "parcial** `numero_evidencia`: su posición en la lista del MEN, que es también el orden "
        "oficial en que se diagnostica (ADR-024). Dato del MEN, sin juicio nuestro.",
        "Glosario «Evidencia» · curriculo_men_normalizado.json · ADR-024"),
    "EVIDENCIA_DICTAMEN": (
        "Nuestro juicio sobre una evidencia del MEN: si admite formato cerrado y **cuál** "
        "(`formato`). Separada de Evidencia a propósito (hallazgo H-6 del docente) para no mezclar "
        "contenido oficial con criterio propio. `formato` entra en esta versión: «el formato de los "
        "ítems lo determina la evidencia» (RF-03-01) y una pregunta propia «se crea con el formato "
        "de esa evidencia» (RF-03-07), y antes no había dónde guardarlo (RI-19). Débil y 1:1 con su "
        "evidencia: la identifica la evidencia misma, así que no necesita llave parcial. Sus "
        "valores dependen del censo QA-014 (V-6, abierto).",
        "H-6 · ADR-006 · RF-06-02 · RF-03-01 · RF-03-07"),
    "EXPERIENCIA_EVIDENCIA": (
        "Las evidencias que diagnostica *esta* experiencia (hallazgo H-4 del docente). Hace que Ítem "
        "y Resultado cuelguen de un solo camino al currículo. **No tiene atributos propios**: su "
        "identidad es el par (experiencia, evidencia) que le dan sus dos relaciones, *incluye* y "
        "*sobre* — y la evidencia tiene que ser del DBA de la experiencia (RI-18, ciclo C1). "
        "**Cambia:** sale `incluida`. El docente no elige evidencias (QA-010) y solo entran las que "
        "el dictamen admite (RF-03-01): una fila de esta entidad **es** una evidencia incluida, y "
        "un booleano siempre verdadero no dice nada.",
        "H-4 · QA-010 · RF-03-01"),
    "INSCRIPCION": (
        "Un estudiante unido a una experiencia. Asociativa con llave propia, para que Presentación "
        "y Resultado no arrastren llave doble. De aquí sale el contador de estudiantes. "
        "**`progreso`** —No iniciada, En curso o Completada (RF-04-01)— va en elipse punteada: se "
        "calcula de sus presentaciones y resultados y no se guarda (ADR-022). Es lo que la v3 del "
        "docente llamaba `estado_avance`.",
        "08-spec-unirse-codigo · RF-04-01 · RF-04-02 · ADR-022"),
    "ITEM": (
        "Pregunta del banco. La IA genera 12 por evidencia incluida al crear la experiencia "
        "(RF-03-01); el docente puede editar, descartar (`excluido`) y agregar las suyas mientras "
        "esté en Borrador (ADR-026). Ninguno se borra, por eso *genera* es (12,N). **Cambia:** "
        "`origen` admite tres valores —`ia`, `editado_docente`, `creado_docente`—; el servicio y el "
        "modelo que lo generaron son los de su experiencia. `formato` es el que fija el dictamen de "
        "su evidencia (RI-19). **Sale `estado_revision`** (cierra V-7): tras ADR-026 revisar el "
        "banco no es requisito de nada y ningún requerimiento lo usa; lo que habilita a publicar es "
        "tener al menos 6 activos por evidencia (RF-02-05).",
        "ADR-005, ADR-006, ADR-014, ADR-015, ADR-016, ADR-026, ADR-030 · RF-03-01 a RF-03-08"),
    "OPCION": (
        "Opción de respuesta de un ítem. Qué columnas aplican depende del formato (RI-4). "
        "`hipotesis_error` existe pero nunca se muestra ni se reporta (ADR-008, ADR-020).",
        "ADR-014 · ADR-020"),
    "PRESENTACION": (
        "El hecho de **haber mostrado** un ítem a un estudiante, distinto del de haberlo respondido "
        "(hallazgos H-2 y H-3). Débil, sin llave parcial: la identifican a la vez la inscripción y "
        "el ítem (*atiende* y *se presenta*, las dos identificadoras), y el ítem tiene que ser de la "
        "experiencia de la inscripción (RI-13, ciclo C2). Una presentación sin respuesta es la "
        "pregunta que el estudiante verá otra vez al retomar (ADR-031). Con `orden_presentacion` y "
        "`fecha_presentacion` la secuencia adaptativa se puede reconstruir.",
        "H-2, H-3 · ADR-016 · ADR-031 · RF-04-04"),
    "RESPUESTA": (
        "Lo que el estudiante respondió a un ítem que se le presentó, con su certeza (CRI, 0 a 5). "
        "Cuelga de Presentación, no de Ítem e Inscripción por separado: no hay respuesta sin "
        "presentación. `correcta` es derivado y **se guarda** al responder (ADR-021). **Pasa a "
        "propia** (antes figuraba como asociativa): desde H-3 cuelga de una sola entidad y no "
        "resuelve ninguna N:M — la asociativa de esta parte es Respuesta_Opción.",
        "ADR-008, ADR-019, ADR-021 · RF-04-05, RF-04-06"),
    "RESPUESTA_OPCION": (
        "Qué opción u opciones eligió el estudiante, no solo si acertó; sin esto, emparejar y "
        "ordenar no son representables. `valor_dado`: la posición (ordenar) o el número de pareja "
        "(emparejar). La opción elegida tiene que ser del ítem que se presentó (RI-6, ciclo C4).",
        "ADR-019"),
    "RESULTADO": (
        "Lo que las respuestas de un estudiante permiten concluir sobre una evidencia de esta "
        "experiencia. Débil, sin llave parcial: la identifican la inscripción (*arroja*) y la "
        "evidencia de la experiencia (*mide*), que tienen que ser de la misma experiencia (RI-13, "
        "ciclo C3). `estado` es derivado y se guarda, con la regla de RF-04-07 —que **cierra "
        "V-5**—, como fotografía del momento (RNF-11), con `fecha_calculo`.",
        "ADR-008, ADR-016, ADR-021 · RF-04-07"),
    "REPORTE": (
        "No persiste: se calcula sobre Resultado, por experiencia, cada vez que se abre. El "
        "*estado general* de cada estudiante tiene cuatro valores con precedencia (ADR-022); el "
        "*estado por evidencia* se clasifica en Datos insuficientes, Brecha aparente o Sin brecha "
        "aparente, con umbrales fijos (ADR-013, ADR-017, ADR-023). No cuenta entre las entidades.",
        "ADR-010, ADR-013, ADR-017, ADR-018, ADR-022, ADR-023 · RF-05-01, RF-05-02"),
}

FUENTE_REL = {
    "accede_docente": "RF-01-06 · 20-spec-auth-elige-rol · RI-12", "accede_estudiante": "RF-01-06 · RI-12",
    "pertenece_area": "ADR-036", "corresponde a": "ADR-036", "se copia de": "ADR-036 · ADR-033",
    "es de": "ADR-036 · RI-20",
    "comprende": "modelo conceptual (rango no confiable: QA-013)", "se dictamina": "H-6",
    "crea": "glosario «Experiencia»", "se ancla a": "modelo conceptual · RF-02-02",
    "incluye": "H-4 · RF-03-01", "sobre": "H-4",
    "genera": "ADR-005 · RF-03-01 (12 por evidencia; ninguno se borra)", "ofrece": "ADR-014 · RI-4 (4 en matching)",
    "realiza": "08-spec-unirse-codigo", "pertenece a": "modelo conceptual",
    "atiende": "H-2", "se presenta": "H-2", "registra": "H-3",
    "selecciona": "ADR-019 · RI-6", "arroja": "ADR-008", "mide": "ADR-008 · H-4",
    "se agrega en": "ADR-010, ADR-018", "resume": "ADR-010, ADR-018",
}


def lista_cus(cus):
    return ", ".join(sorted(cus)) if cus else "—"


def documento():
    L = []
    w = L.append
    w("# 16. Modelo Entidad-Relación — AdaptiveLearn")
    w("")
    w("**Metodología:** MODESEC — Fase III, Diseño Computacional, modelado de la base de datos.")
    w("**Fecha:** 2026-10-21. **Estado:** versión final de la Fase III. **Archivo generado** por")
    w("`mer/generar_documento.py` desde `mer/datos_mer.py`, la misma fuente de los diagramas; no se")
    w("edita a mano.")
    w("")
    w("**Actualizado el 2026-10-26** por la revisión del docente del 2026-10-22")
    w("(`21-revision-docente-2026-10-22.md`): catálogo curricular normalizado —ÁREA, GRADO y")
    w("DOCUMENTO_OFICIAL, código del DBA sin tildes— (ADR-036) y estado de verificación del correo")
    w("(ADR-037). Ver la sección 10 y la tabla de cambios (13).")
    w("")
    w("MODESEC: *«En esta etapa se recomienda la utilización de bases de datos relacionales […] Si")
    w("la opción es la primera, se deberá crear un MER (Modelo Entidad Relación), un MR (Modelo")
    w("relacional) basado en el MER y un diccionario de datos para los metadatos»*. Este documento")
    w("es el primero de los tres; el MR es `17-modelo-relacional.md` y el diccionario,")
    w("`18-diccionario-datos.md`.")
    w("")
    w("**Este es el MER vigente del proyecto.** Parte de la *Quinta revisión* (2026-09-08), el")
    w("borrador que respondió a la revisión del docente del 2026-09-01 con la Fase II todavía")
    w("abierta, y lo lleva a lo que la Fase II cerrada y el análisis de requerimientos (`11`)")
    w("exigen. Para leerlo:")
    w("")
    w("- **Qué hay:** las entidades (sección 4) y cómo se relacionan (5).")
    w("- **Cómo encaja todo:** los ciclos del modelo y la regla que cierra cada uno (6), quién crea,")
    w("  lee, modifica y borra cada entidad (7), y un recorrido de la cuenta al reporte (8).")
    w("- **Con el resto de la fase:** el diagrama de clases (9) y la revisión del docente, hallazgo")
    w("  por hallazgo (10).")
    w("- **Lo que el diagrama no puede decir:** las restricciones (11), los vacíos (12) y qué cambió")
    w("  respecto del borrador (13).")
    w("")
    w("## 1. Conteo")
    w("")
    w("| Entidades | Relaciones | Atributos | Ciclos | Restricciones de integridad | Vacíos abiertos |")
    w("|---|---|---|---|---|---|")
    w(f"| **{N_ENTIDADES}** (+ Reporte, derivado) | **{N_REL_REALES}** (+ {N_REL_DERIVADAS} derivadas) "
      f"| **{N_ATRIBUTOS}** | **{len(CICLOS)}**, todos cerrados | **{N_RI}** | **2** (V-6, V-9) + 1 nuevo (V-12) |")
    w("")
    w("## 2. Notación")
    w("")
    w("**Chen estricta**, como decidió la Quinta revisión para cerrar el hallazgo H-8:")
    w("")
    w("| Símbolo | Significa |")
    w("|---|---|")
    w("| Rectángulo · doble borde | Entidad · entidad débil |")
    w("| Rombo · rombo doble | Relación · relación identificadora |")
    w("| Elipse · elipse negra · subrayado punteado | Atributo · llave primaria · llave parcial de una débil |")
    w("| **Elipse punteada** | Atributo derivado: «se guarda» (ADR-021) o «calculado» (no se guarda) |")
    w("| Línea simple · **línea doble** | Participación parcial · total |")
    w("| **(mín, máx) junto a cada entidad** | Cuántas veces participa un ejemplar suyo en la relación — la notación de la tabla de la v3 del docente |")
    w("| Razón bajo el rombo (1:1, 1:n, n:m) | El tipo de la relación |")
    w("| **{xor} punteado entre dos relaciones** | Son excluyentes: un ejemplar participa en una o en la otra |")
    w("| Rombo y caja punteados | Derivados: se calculan, no persisten |")
    w("")
    w("**Las llaves foráneas no se dibujan.** Es exactamente lo que señaló H-8: *«la FK es")
    w("precisamente lo que la derivación al MR produce a partir de la relación ya dibujada»*. Cada")
    w("entidad muestra solo sus atributos; las FK aparecen en `17-modelo-relacional.md`, y")
    w("`modelo-relacional/_verificar_mr_mer.py` comprueba que cada una salga de una relación de")
    w("este modelo, y que cada relación tenga la FK que la realiza.")
    w("")
    w("![Leyenda de la notación](mer/leyenda.svg)")
    w("")
    w("## 3. Diagramas")
    w("")
    w("La **vista de conjunto**, el **mapa completo** y las **siete vistas** no son tres modelos:")
    w("salen de `mer/datos_mer.py`. Las vistas se cortan por el ciclo de vida del sistema, y cada")
    w("relación se dibuja en **exactamente una** vista (lo comprueba `mer/_verificar_vistas.py`);")
    w("una entidad que reaparece en otra vista se dibuja como costura, sin atributos. La geometría")
    w("—líneas que atraviesan cajas, rótulos encimados— la revisan `mer/_verificar_mapa.py` y el")
    w("verificador de `mer/mapa_cajas.py`, por coordenadas.")
    w("")
    w("### Vista de conjunto, con la estructura de la v3 del docente")
    w("")
    w("El modelo entero en una sola lámina, con la estructura con que el docente presentó su")
    w("modelo v3: cajas de color por tipo de entidad, rombos verdes, línea doble para la")
    w("participación total, (mín, máx) en cada extremo y leyenda abajo. Para mirarlo de un vistazo")
    w("muestra también las llaves (PK y FK), calculadas del modelo relacional, así que no puede")
    w("contradecirlo. `mer/mer-pantalla-completa.html` la abre a pantalla completa, con zoom.")
    w("")
    w("![Vista de conjunto del MER](mer/mer-cajas.svg)")
    w("")
    w("### Mapa completo, en Chen")
    w("")
    w("![Mapa completo del MER](mer/mapa-chen.svg)")
    w("")
    for n, (titulo, sub) in VISTAS.items():
        w(f"### Vista {n} · {titulo}")
        w("")
        w(f"{sub}")
        w("")
        w(f"![Vista {n}: {titulo}](mer/vista{n}.svg)")
        w("")
    w("## 4. Entidades")
    w("")
    for nombre, tipo, attrs in ENTIDADES:
        debil = " · débil" if nombre in DEBILES and tipo != "debil" else ""
        w(f"### {nombre}")
        w("")
        lista = (", ".join(f"`{a.split(' ')[0]}`" + MARCA[m] + (" (U)" if "(U)" in a else "")
                           for a, m in attrs) if attrs else "ninguno propio")
        w(f"**Tipo:** {TIPO[tipo]}{debil}. **Atributos:** {lista}.")
        w("")
        texto, fuente = FICHA[nombre]
        w(texto)
        w("")
        w(f"*Fuente: {fuente}.*")
        w("")
    w("## 5. Relaciones")
    w("")
    w("| Entidad A | Relación | Entidad B | Razón | (mín, máx) de A | (mín, máx) de B | Identificadora | Vista | Fuente |")
    w("|---|---|---|---|---|---|---|---|---|")
    for r in RELACIONES:
        clave = r.get("id", r["nombre"])
        nombre = r["nombre"] + (" *(derivada)*" if r.get("derivada") else "")
        if r.get("asociativa"):
            nombre += f" — vía {r['asociativa']}"
        if r.get("xor"):
            nombre += " {xor}"
        razon = f"{r['card_a']}:{r['card_b']}".replace("N:M", "N:M")
        w(f"| {r['a']} | {nombre} | {r['b']} | {razon} | {r['part_a']} | {r['part_b']} | "
          f"{'sí' if r['ident'] else '—'} | {r['vista']} | {FUENTE_REL[clave]} |")
    w("")
    w("Cómo se lee una fila: en *crea*, DOCENTE (0,N) y EXPERIENCIA (1,1) dicen que un docente crea")
    w("cero o más experiencias, y que cada experiencia la crea exactamente un docente. Un mínimo de")
    w("1 es participación total (línea doble) y decide `NOT NULL` en la llave foránea del modelo")
    w("relacional; `_verificar_mer.py` comprueba que las dos cosas coincidan. Tres mínimos merecen")
    w("nota: **(12,N)** en *genera*, porque la IA genera 12 ítems por evidencia y ninguno se borra")
    w("(descartar solo excluye); **(2,N)** en *ofrece*, que en emparejamiento sube a 4 (RI-4); y")
    w("**(1,N)** de ÁREA, GRADO y DOCUMENTO_OFICIAL en las relaciones del catálogo, porque el")
    w("catálogo se carga completo y uno de ellos sin ningún DBA no tendría nada que ofrecer; y")
    w("**(0,1)** de CREDENCIAL en las dos *accede como*, porque mientras el registro está en curso la")
    w("credencial todavía no tiene rol. Las dos *accede como* llevan **{xor}**: una credencial da")
    w("acceso a un solo rol (RI-12).")
    w("")
    ciclos(w)
    crud(w)
    w(RECORRIDO)
    w(CLASES.replace("__N_REL__", str(len(RELACIONES))))
    w(RESPUESTA)
    w(RESTRICCIONES)
    w(VACIOS)
    w(CAMBIOS)
    w(VERIFICACION)
    return "\n".join(L) + "\n"


def ciclos(w):
    aristas = sum(2 if r.get("asociativa") else 1 for r in RELACIONES if not r.get("derivada"))
    w("## 6. Ciclos del modelo, y qué cierra cada uno")
    w("")
    w("Un ciclo es un camino de relaciones que vuelve a la entidad de la que salió. Si al volver")
    w("algo tiene que coincidir —que la evidencia incluida sea del DBA de la experiencia, por")
    w("ejemplo—, el diagrama no lo puede decir y hace falta una regla que lo cierre. Es el")
    w("argumento del hallazgo H-4: *«un ciclo que hay que restringir con una regla externa suele")
    w("indicar que falta una entidad»*. Por eso aquí no se deja ninguno sin revisar:")
    w("")
    w(f"El grafo de las {N_ENTIDADES} entidades persistentes tiene {aristas} aristas —*selecciona*")
    w("cuenta dos, porque pasa por Respuesta_Opción—, así que tiene exactamente")
    w(f"**{aristas} − {N_ENTIDADES} + 1 = {len(CICLOS)} ciclos independientes**: cualquier otro ciclo")
    w("es combinación de estos. `mer/_verificar_mer.py` comprueba que sean esos, que cada uno")
    w("exista en el grafo y que ninguno sea combinación de los otros.")
    w("")
    w("| Ciclo | Camino | Qué tiene que coincidir | Regla | Cómo se cierra |")
    w("|---|---|---|---|---|")
    for c in CICLOS:
        w(f"| **{c['id']}** | {' → '.join(c['camino'])} | {c['que']} | {c['regla'] or '—'} | {c['como']} |")
    w("")
    w("Los cinco ciclos que exigen regla se cierran **por estructura**: el motor rechaza el dato")
    w("que los rompería, sin triggers. C6 nace el 2026-10-26 con el catálogo normalizado (ADR-036)")
    w("y se cierra con la misma técnica. Dos de ellos —C1 y C4— estaban abiertos hasta esta versión,")
    w("y el motor aceptaba incluir en una experiencia una evidencia de otro DBA, o elegir como")
    w("respuesta una opción de otro ítem; las pruebas de `modelo-relacional/pruebas_mr.py` intentan")
    w("los dos casos y ahora el motor los rechaza.")
    w("")


def crud(w):
    casc = {}
    for cu, tabla in (("CU-15", "experiencia"), ("CU-26", "inscripcion")):
        for t in CR.en_cascada(tabla, MR.FKS):
            casc.setdefault(t.upper(), []).append(cu)
    w("## 7. Cómo interactúa: qué caso de uso crea, lee, modifica y borra cada entidad")
    w("")
    w("El diagrama dice qué existe y cómo se relaciona; esta matriz dice **quién** lo crea, lo")
    w("cambia y lo borra, con los casos de uso de `12-casos-de-uso.md`. Los borrados en cascada no")
    w("se escriben a mano: se calculan de las llaves foráneas `ON DELETE CASCADE` del modelo")
    w("relacional. Fuente: `uml/datos_crud.py`; la comprueba `uml/_verificar_uml.py`, bloque F.")
    w("")
    w("| Entidad | Crea | Lee | Modifica | Borra |")
    w("|---|---|---|---|---|")
    for nombre, _, _ in ENTIDADES:
        ops = {op: [cu for cu, d in CR.CRUD.items() if op in d.get(nombre, "")] for op in "CRUD"}
        crea = lista_cus(ops["C"]) if ops["C"] else f"— *{CR.SIN_CREADOR[nombre]}*"
        borra = []
        if ops["D"]:
            borra.append(lista_cus(ops["D"]))
        if nombre in casc:
            borra.append("en cascada: " + ", ".join(sorted(casc[nombre])))
        modif = lista_cus(ops["U"]) if ops["U"] else ("**nunca**" if nombre in CR.INMUTABLES else "—")
        w(f"| {nombre} | {crea} | {lista_cus(ops['R'])} | {modif} | {'; '.join(borra) or '—'} |")
    w("")
    w("Lo que se lee de la matriz:")
    w("")
    w("- **Presentación, Respuesta, Respuesta_Opción y Resultado nunca se modifican.** Son hechos")
    w("  (se mostró, se respondió) y fotografías (lo que se concluyó): RNF-10, RNF-11, ADR-021.")
    w("- **Solo tres cosas se borran directamente:** una experiencia (CU-15), una inscripción")
    w("  (CU-26) y una opción mientras el ítem está en Borrador (CU-18). Todo lo demás cae en")
    w("  cascada, y la cascada nunca alcanza una cuenta ni el currículo (cierra V-11).")
    w("- **Lo que ningún caso de uso crea** es lo que viene de fuera —el currículo del MEN y")
    w("  nuestro dictamen, que el equipo carga— o lo que se calcula: el Reporte.")
    w("- **CU-08** (cerrar sesión) es el único caso de uso que no toca datos: termina la sesión del")
    w("  navegador.")
    w("")


RECORRIDO = """## 8. Un recorrido, de la cuenta al reporte

Las siete vistas siguen el ciclo de vida del sistema. Este es ese ciclo contado con un caso: el
mismo de `14-diagrama-objetos.md`, donde está dibujado con datos concretos y **cargado en el
esquema real** sin violar ninguna restricción.

1. **Vista 1 · Acceso.** Ana se registra con su correo (CU-01): nace su CREDENCIAL, que verifica
   el correo con un código (CU-03). Al elegir el rol (CU-05) nace DOCENTE y la credencial *accede
   como* docente. Luis entra con Google (CU-02): su credencial nace con el correo ya verificado y
   sin contraseña (RI-15), y *accede como* ESTUDIANTE. Ninguna credencial accede como las dos
   cosas ({xor}, RI-12).
2. **Vista 2 · Currículo.** El catálogo ya está cargado: el DBA `MAT-08-01` *pertenece a* el ÁREA
   `MAT`, *corresponde a* el GRADO 8 y *se copia de* el DOCUMENTO_OFICIAL de Matemáticas V.2, que
   *es de* esa misma área (RI-20, ciclo C6). El DBA *comprende* sus EVIDENCIAS, y cada una tiene su
   DICTAMEN, que dice si admite formato cerrado y cuál (RI-19).
3. **Vista 3 · Autoría.** Ana crea una experiencia (CU-11): la EXPERIENCIA *se ancla a* ese DBA e
   *incluye* una EXPERIENCIA_EVIDENCIA *sobre* cada evidencia admitida — todas de ese mismo DBA
   (RI-18, ciclo C1). Guarda con qué servicio y modelo se generó su banco (RI-17).
4. **Vista 4 · Banco.** En el mismo acto (CU-16), cada evidencia incluida *genera* 12 ÍTEMS, y
   cada ítem *ofrece* sus OPCIONES. Ana los edita, descarta o agrega (CU-18 a CU-20) y publica
   (CU-13): el banco se congela.
5. **Vista 5 · Entrega.** Luis se une con el código (CU-22): nace su INSCRIPCIÓN, que *pertenece a*
   la experiencia. Cada pregunta que se le muestra (CU-23) es una PRESENTACIÓN que *atiende* su
   inscripción y en la que *se presenta* un ítem — de esa misma experiencia (RI-13, ciclo C2).
6. **Vista 6 · Respuesta.** Al confirmar la certeza (CU-24), la presentación *registra* una
   RESPUESTA, que *selecciona* opciones por medio de RESPUESTA_OPCIÓN — opciones del ítem que se
   presentó (RI-6, ciclo C4). Si Luis cierra la página antes, la presentación queda sin respuesta,
   y es la pregunta que verá al volver (ADR-031).
7. **Vista 7 · Conclusión.** Cuando la regla adaptativa concluye una evidencia (CU-25), la
   inscripción *arroja* un RESULTADO que *mide* esa evidencia incluida (RI-13, ciclo C3). Cuando
   Ana abre el reporte (CU-27), cada resultado *se agrega en* el REPORTE que *resume* la
   experiencia: se calcula en ese momento y no se guarda.
"""

CLASES = """
## 9. El MER y el diagrama de clases

Los dos describen el mismo mundo, y `uml/_verificar_uml.py` comprueba que no se contradigan:

| En el MER | En el diagrama de clases (`13`) | Por qué así |
|---|---|---|
| Cada entidad persistente | Una clase con el mismo nombre, y los mismos atributos menos las llaves foráneas | En objetos, una llave foránea es una asociación, no un atributo. Verificado columna por columna |
| Cada una de las __N_REL__ relaciones | Una asociación con el mismo nombre y las mismas entidades | Verificado una por una |
| RESPUESTA_OPCION, entidad asociativa | RespuestaOpcion, **clase asociación** de *selecciona* | Es la misma idea en las dos notaciones |
| REPORTE, derivado | Reporte «calculada» | No persiste en ninguno de los dos |
| `progreso` de INSCRIPCION, calculado | El método `Inscripcion.progreso()` | Lo que se calcula es comportamiento |
| DOCENTE y ESTUDIANTE, dos entidades | Dos clases que **heredan de Usuario**, abstracta | Usuario agrupa lo que los dos hacen igual (editar su perfil). En el MER y en la base siguen separados, por la decisión del equipo de que la estructura impida asignar un estudiante como creador; por eso la credencial apunta a uno **o** al otro ({xor}) |
| — | Las clases de servicio (ServicioAcceso, GeneradorBanco, ReglaAdaptativa…) | Son comportamiento, no datos: no tienen entidad |
"""

RESPUESTA = """
## 10. Respuesta a la revisión del docente (2026-09-01)

El docente revisó la versión del MER del 2026-08-20 y entregó doce hallazgos y una propuesta
de modelo (v3, 14 entidades). El equipo los trió el 2026-09-04
(`05-triaje-revision-docente.md`, en la carpeta del borrador) y la Quinta revisión incorporó lo
aceptado. Esta es la cuenta de dónde quedó cada uno **en el modelo final**:

| # | Hallazgo | Dónde quedó |
|---|---|---|
| **H-1** | La configuración del diagnóstico (orden de las evidencias, ítems a presentar, tope de adicionales) no tiene dónde vivir | **Atendido; la parte que sigue vigente es H-4.** Los tres datos que pedía dejaron de ser una decisión del docente: ADR-016 fija el mínimo de 4 y el tope de 6, y ADR-024 fija el orden oficial del DBA. Por eso Experiencia_Evidencia no los lleva. También sale `Item.orden_sugerido`: los ítems se eligen al azar entre los activos que el estudiante no ha visto (RF-04-04). |
| **H-2** | La secuencia adaptativa no se puede reconstruir; RI-11 no es verificable | **Resuelto.** PRESENTACIÓN registra qué ítem se mostró, en qué orden y cuándo; Respuesta tiene `fecha_respuesta`. Con la regla de parada definida (H-7), RI-11 se verifica de verdad. |
| **H-3** | «Se le presentó y no respondió» no es representable | **Resuelto.** *registra* es (0,1) del lado de la presentación: una presentación sin respuesta es exactamente ese caso, y es la pregunta que se repite al retomar (ADR-031). |
| **H-4** | Falta el vínculo Experiencia–Evidencia; RI-1 y RI-2 tapan el hueco | **Resuelto, y su criterio se aplicó a todo el modelo.** EXPERIENCIA_EVIDENCIA; Ítem y Resultado cuelgan de ella. Además, el modelo tiene exactamente 6 ciclos y cada uno está declarado con lo que lo cierra (sección 6). Aplicar ese criterio encontró dos ciclos abiertos (C1 y C4), que el motor dejaba romper; ahora los cierra la estructura. |
| **H-5** | Falta `estado_revision` del ítem, y no publicar con ítems sin revisar | **En parte, con una decisión que el equipo debe confirmar.** Lo que sí: `origen` distingue lo generado por IA de lo editado o creado por el docente (tres valores), y la experiencia guarda con qué servicio y modelo se generó su banco. Lo que no: la regla de publicar solo con todo revisado ya la había rechazado el triaje (`12-spec-modal-banco-items`: revisar el banco no es prerrequisito para publicar). Y `estado_revision`, que el triaje sí había aceptado pendiente de vocabulario (V-7), **sale**: después del triaje llegó ADR-026 (el banco pasa a ser del docente, no algo que solo revisa), y ningún requerimiento ni ventana lo escribe o lo lee. Lo que hoy habilita a publicar es RI-14: al menos 6 ítems activos por evidencia. |
| **H-6** | `aplica_formato_cerrado` cuelga de una entidad «dato del MEN» | **Resuelto.** EVIDENCIA_DICTAMEN, separada de Evidencia — y ahora guarda también qué formato admite la evidencia (RI-19). |
| **H-7** | La regla de parada no está definida | **Resuelto.** RF-04-07 la define (señal fuerte = certeza 3 a 5; mayoría desde la 4.ª respuesta; tope 6) y cierra V-5. Está implementada y probada en `uml/regla.py`. |
| **H-8** | El MER muestra llaves foráneas: deja de ser Chen y se solapa con el MR | **Resuelto.** La Quinta revisión había elegido Chen pero seguía dibujando las FK como atributos. Ahora no: Chen estricta, con llave parcial en las débiles (sección 2). El MR aporta lo que le corresponde: FK, acciones referenciales, tipos. La vista de conjunto sí muestra las llaves, con la estructura de la v3 del propio docente, para leer cómo se enlaza todo. |
| **H-9** | Los mínimos de Opción por formato no están fijados | **Resuelto.** RI-4: 2 en selección única y ordenamiento, 4 en emparejamiento con al menos 2 por grupo; también en RF-03-05 y en el (2,N) de *ofrece*. |
| **H-10** | Conviven varias versiones del MER y las de la carpeta MODESEC son las viejas | **Resuelto.** El vigente es este documento, dentro de la carpeta de la metodología; el borrador lleva su aviso y `03-presentacion-mer.html` está marcado como superado desde el 2026-09-19. |
| **H-11** | Las fuentes citadas (ADR, glosario, currículo) no están en la carpeta entregada | **Resuelto en el repositorio.** `docs/diseno/` (ADR, glosario, visión) y `data/curriculo-men/normalized/curriculo_men_normalizado.json` van junto a la metodología. Toda ADR que cita este documento existe en `docs/diseno/decisiones.md`; la única diferencia con su texto es la de RI-17 con ADR-030 (cambio 4 de la sección 13), que el equipo debe confirmar. |
| **H-12** | Fase II nunca diseñó la toma del diagnóstico ni el Reporte | **Resuelto al cerrar la Fase II:** ventanas 020 a 023 (toma del diagnóstico), 010 (Reporte) y 027 (historial del estudiante). |

**De la propuesta v3 del docente**, además: su `Inscripcion.estado_avance` es nuestro
`progreso`, dibujado como atributo calculado y sin columna (ADR-022); su `calculado_en` es
nuestro `fecha_calculo`; su regla de orden de presentación único por inscripción es nuestra
RI-8; su tope de presentaciones es RI-9, con el 6 fijo de ADR-016; su vacío de autenticación (su
V-1) es la entidad CREDENCIAL; y su notación (mín, máx) es la que llevan ahora las relaciones.
Lo que este modelo agrega sobre la v3 es la credencial, con sus dos relaciones excluyentes, los
ciclos declarados y las restricciones RI-12 a RI-21.

### Revisión del docente del 2026-10-22

El docente revisó el acceso y el catálogo curricular. Sus notas y su triaje están en
`21-revision-docente-2026-10-22.md`. En este modelo:

| # | Nota | Dónde quedó |
|---|---|---|
| **R1** | «Tabla para grados y área, y codificar» | **Aplicada (ADR-036).** Entidades ÁREA y GRADO, y además DOCUMENTO_OFICIAL (recomendación del equipo). El DBA pierde `area` y `grado` como texto y su código pasa a `ÁREA-GG-NN`, sin tildes (RI-21). El ciclo nuevo, C6, se cierra con RI-20. |
| **R2** | `id_usuario` → `id_estudiante` e `id_docente` | **No es de este modelo:** el MER no tiene «usuario». Se aplica al backend en la Fase IV. |
| **R3** | `email` → `estado_verificado` / `estado_procesando` | **Aplicada (ADR-037).** CREDENCIAL guarda `estado_verificacion` (`procesando` o `verificado`) en vez del sí/no; RI-15 se reescribe con el estado. |
| **R4** | Quitar `codigo_expira_en` y `codigo_ultimo_envio` | **Pendiente** de la respuesta del docente a la pregunta P2: sin esos datos, el vencimiento del código y la espera de 30 s para reenviarlo (RF-01-03) necesitan otro lugar. Siguen en CREDENCIAL. |
| **R5** | Correo del sistema `adaptivelearn@` | **No es de este modelo:** es configuración del backend (Fase IV). |
"""

RESTRICCIONES = """
## 11. Restricciones de integridad

Reglas que el diagrama no puede expresar por sí solo. Las once del borrador se conservan con
su número —cambia el texto de las que el cierre de la Fase II tocó— y entran diez nuevas, dos de
ellas (RI-20 y RI-21) con el catálogo normalizado del 2026-10-26. Cómo
hace cumplir cada una el modelo relacional (una restricción del motor o el servicio) está en
`17-modelo-relacional.md`, sección 7.

| RI | Regla | Estado en esta versión |
|---|---|---|
| **RI-1** | El par (Estudiante, Experiencia) es único en Inscripción: unirse dos veces no duplica (`08-spec-unirse-codigo` §7). | Sin cambio |
| **RI-2** | El par (Inscripción, Evidencia) es único en Resultado. Lo garantiza la identificación débil. | Sin cambio |
| **RI-3** | El **correo de la credencial** es único entre los dos roles, sin distinguir mayúsculas (RF-01-04). `codigo_invitacion` es único, de 6 caracteres sin 0/O/1/I/L. | **Reformulada**: el correo pasó a Credencial |
| **RI-4** | El dominio de Opción depende del formato del ítem (ADR-006, ADR-014), con mínimos: 2 opciones en selección única y ordenamiento, 4 en emparejamiento con al menos 2 por grupo (H-9). | Sin cambio |
| **RI-5** | Solo existe una fila de Experiencia_Evidencia para una evidencia cuyo dictamen admite formato cerrado (RF-03-01, RF-06-02). | **Reformulada**: salió `incluida` |
| **RI-6** | Toda Respuesta selecciona al menos una Opción, y **solo del Ítem de su Presentación**; en selección única, exactamente una. Una Presentación sin Respuesta es válida. | **Reforzada**: que la opción sea del ítem presentado pasó a ser estructura (ciclo C4); antes solo lo cuidaba el servicio y el motor aceptaba una opción de otro ítem |
| **RI-7** | Una Experiencia en Borrador no admite Inscripción (`08-spec-unirse-codigo` §2.4, RF-04-02). | Sin cambio |
| **RI-8** | `orden_presentacion` es único dentro de una Inscripción. | **Precisada**: el borrador decía «para una misma evidencia»; el orden que reconstruye la secuencia es el de todo el diagnóstico |
| **RI-9** | Las Presentaciones de una Inscripción para una evidencia no pasan del tope de 6 (ADR-016) ni de los ítems activos de esa evidencia. | Sin cambio |
| **RI-10** | Ítem y Opción no se modifican una vez presentados. | **Reforzada por ADR-026**: todo el banco se congela al publicar, y como solo una experiencia publicada admite inscripciones (RI-7), ningún ítem editable puede tener presentaciones |
| **RI-11** | `Respuesta.correcta` y `Resultado.estado` son derivados y se persisten (ADR-021); su valor guardado coincide con el recálculo. | **Ahora verificable del todo**: la regla está definida (RF-04-07, cierra V-5) |
| **RI-12** | Una credencial da acceso a lo sumo a un rol ({xor}); cada docente y cada estudiante tiene exactamente una credencial. | **Nueva** (RF-01-06) |
| **RI-13** | La experiencia de una Presentación y de un Resultado es la de su Inscripción, y el ítem presentado es de esa experiencia. | **Nueva**: cierra los ciclos C2 y C3 |
| **RI-14** | Solo se publica una experiencia con al menos 6 ítems activos por evidencia incluida. | **Nueva** (RF-02-05) |
| **RI-15** | Una credencial de correo tiene contraseña y no identificador externo; una de Google o Microsoft tiene identificador externo, no tiene contraseña y su `estado_verificacion` es `verificado`. | **Nueva** (RF-01-01, RF-01-02); el 2026-10-26 se escribe con el estado en vez del sí/no (ADR-037) |
| **RI-16** | `fecha_publicacion` es nula si y solo si la experiencia está en Borrador. | **Nueva** (RF-02-05) |
| **RI-17** | Un banco sale entero de un solo servicio y modelo de IA, y se guardan en la Experiencia. El de un ítem generado o editado es el de su experiencia; uno creado por el docente no se atribuye a la IA. | **Nueva**, rehecha en esta versión: antes iba en cada ítem y permitía que un banco mezclara servicios (RF-03-02, RF-03-03) |
| **RI-18** | Las evidencias que incluye una experiencia son del DBA al que se ancla. | **Nueva**: cierra el ciclo C1; el motor aceptaba incluir una evidencia de otro DBA |
| **RI-19** | Un dictamen que admite formato cerrado dice cuál, uno que no lo admite no tiene formato, y todo ítem de una evidencia tiene el formato de su dictamen (RF-03-01, RF-03-07). | **Nueva** |
| **RI-20** | El documento oficial del que se copió un DBA es de la misma área que el DBA. | **Nueva** (2026-10-26, ADR-036): cierra el ciclo C6 |
| **RI-21** | El código del DBA es `ÁREA-GG-NN`: el código de su área, su grado con dos cifras y su número con dos cifras desde 01, sin tildes. Los códigos de área son 2 o 3 letras mayúsculas sin tildes. | **Nueva** (2026-10-26, ADR-036) |
"""

VACIOS = """
## 12. Vacíos: dónde quedó cada uno

| Vacío | Qué era | Estado |
|---|---|---|
| V-1 | Marca temporal de Respuesta | Resuelto en la Quinta revisión (`fecha_respuesta`) |
| V-2 | Inmutabilidad de Ítem y Opción | Resuelto en la Quinta revisión (RI-10) |
| V-3 | Estado de avance de la Inscripción | Resuelto por ADR-022: es `progreso`, calculado, sin columna |
| V-4 | Marca de cálculo de Resultado | Resuelto por ADR-021 (`fecha_calculo`) |
| V-5 | Qué es «señal fuerte»: la regla de parada | **Resuelto** por RF-04-07: certeza 3 a 5 es señal fuerte; mayoría desde la 4.ª respuesta; tope 6. Implementada y probada en `uml/regla.py` |
| V-6 | Valores del dictamen de formato cerrado | **Abierto**: depende del censo QA-014 |
| V-7 | Vocabulario de `estado_revision` | **Cerrado**: el atributo sale (ADR-026) |
| V-8 | Autenticación y credencial | **Resuelto**: entidad CREDENCIAL |
| V-9 | Versionar el contenido del ítem | **Diferido**, y menos necesario: con ADR-026 el banco se congela al publicar y antes no hay respuestas |
| V-10 | Una excepción de contraste (RNF-03) | No es del modelo de datos; sigue diferido en la interfaz |
| V-11 | Qué pasa con los datos al eliminar o salir de una experiencia | **Resuelto** en el MR: borrado en cascada desde Experiencia e Inscripción (sección 7), probado contra MySQL |
| V-12 | Un DBA sin ninguna evidencia que admita formato cerrado | **Nuevo, abierto**: el MER ya impide crear su experiencia (*incluye* es (1,N)), pero qué muestra la pantalla no está especificado. Depende de QA-014 |

Fuera de este modelo, como en el borrador: Unidad, Práctica y Verificación (ADR-007); la
hipótesis de error como dato reportado (ADR-008); Bloom como campo activo; umbrales del
reporte configurables (ADR-013, ADR-017); la autorización del acudiente (ADR-029, RNF-06: es
la condición que impide usar esta versión con estudiantes reales).
"""

CAMBIOS = """
## 13. Qué cambió respecto de la Quinta revisión, y por qué

| # | Cambio | Fuente |
|---|---|---|
| 1 | Entra **CREDENCIAL**, con sus dos relaciones *accede como*, excluyentes ({xor}), y una vista nueva para ella (Vista 1 · Acceso y cuentas). Las otras seis vistas pasan a 2–7. | V-8 · ventanas 014–019 · RF-01-01 a RF-01-09 · backend I1 |
| 2 | **Docente y Estudiante:** `nombre` pasa a `nombres` + `apellidos`; `correo` pasa a Credencial. | RF-01-05, RF-01-11 · ADR-029 · RF-01-04 |
| 3 | **Ítem:** `origen` con tres valores; sale `estado_revision`. | ADR-026 · cierra V-7 |
| 4 | **Experiencia:** entran `servicio_ia` y `modelo_ia`, los del banco entero. | RF-03-02, RF-03-03, ADR-030 · RI-17 |
| 5 | **Evidencia_Dictamen:** entra `formato`, el formato cerrado que admite la evidencia. | RF-03-01, RF-03-07 · RI-19 |
| 6 | **Experiencia_Evidencia:** sale `incluida`. | QA-010 · RF-03-01 |
| 7 | **Inscripción:** `progreso`, calculado (elipse punteada). **Respuesta** pasa de asociativa a propia. | RF-04-01 · ADR-022 · H-3 |
| 8 | **Notación:** Chen estricta, sin llaves foráneas y con llave parcial (cierra H-8); (mín, máx) en cada extremo; elipse punteada para lo derivado; {xor}. | H-8 · v3 del docente |
| 9 | **Ciclos:** los 5 del modelo, declarados con lo que los cierra. Dos estaban abiertos (C1, C4) y ahora los cierra la estructura (RI-18, RI-6). | H-4 |
| 10 | **Matriz CRUD** y **recorrido** guiado: cómo interactúa cada entidad con los casos de uso. | `12`, `14` |
| 11 | Ocho restricciones nuevas (RI-12 a RI-19); RI-3, RI-5 y RI-8 reformuladas; RI-6, RI-10 y RI-11 reforzadas. | Sección 11 |
| 12 | V-5, V-7, V-8 y V-11 cerrados; V-12, nuevo. | Sección 12 |
| 13 | **Reporte** pasa al centro del mapa, entre las cuatro entidades de las que depende. | Legibilidad |
| 14 | *(2026-10-26)* Entran **ÁREA, GRADO y DOCUMENTO_OFICIAL**; el DBA pierde `area` y `grado` como texto y gana *pertenece a*, *corresponde a* y *se copia de*; el documento *es de* un área. Código del DBA `ÁREA-GG-NN`, sin tildes (RI-21). Ciclo nuevo C6, cerrado por RI-20. Las tres van a la Vista 2. | ADR-036 · revisión del docente del 2026-10-22 (R1) |
| 15 | *(2026-10-26)* **Credencial:** `email_verificado` (sí/no) pasa a `estado_verificacion` (`procesando` / `verificado`); RI-15 se reescribe con el estado. | ADR-037 · revisión del docente del 2026-10-22 (R3) |
"""

VERIFICACION = """
## 14. Verificación

Desde `fase-3-diseno-computacional/`:

```bash
cd mer && python construir_vistas.py && python mapa_cajas.py && python _verificar_mer.py && python _verificar_vistas.py && python _verificar_mapa.py
```

| Verificador | Qué comprueba |
|---|---|
| `mer/_verificar_mer.py` | Que la línea doble y el (mín, máx) digan lo mismo; que los ciclos declarados sean exactamente los del grafo, existan y sean independientes; que toda entidad débil tenga su relación identificadora. |
| `mer/_verificar_vistas.py` | Que cada relación esté en exactamente una vista y cada entidad en al menos una. |
| `mer/_verificar_mapa.py`, `mer/mapa_cajas.py` | La geometría de las nueve láminas, por coordenadas: ninguna línea atraviesa una caja ni tacha un rótulo. |
| `modelo-relacional/_verificar_mr_mer.py` | Que cada FK del modelo relacional salga de una relación de este MER, y que cada relación tenga su FK. |
| `modelo-relacional/verificar_mr.py` y `probar_mysql.py` | Que el esquema rechace lo que estas reglas prohíben —incluidos los ciclos C1, C4 y C6 y el formato del código del DBA—, en SQLite y en MySQL 8. |
| `uml/_verificar_uml.py` | Que las clases, las asociaciones y la matriz CRUD (sección 7) coincidan con este MER, y que el diagrama de objetos se cargue en el esquema real. |
"""

if __name__ == "__main__":
    txt = documento()
    with open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(txt)
    print(f"generado: 16-modelo-entidad-relacion.md ({len(txt.splitlines())} líneas)")
