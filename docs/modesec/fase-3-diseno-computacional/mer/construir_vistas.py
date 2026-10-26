"""Construye las 7 vistas Chen + la leyenda + el mapa, y las junta en un HTML.

Version final de la Fase III. Las vistas 2 a 7 son las seis de la Quinta
revision (renumeradas); la vista 1, Acceso y cuentas, es nueva.
"""
import generador as g
from vistas_chen import Lienzo
from mapa_chen import MAPA, CAPTION as CAP_MAPA
from datos_mer import N_ENTIDADES, N_REL_REALES, RELACIONES

SEL = next(r for r in RELACIONES if r["nombre"] == "selecciona")

V = {}
CAP = {}

# ------------------------------------------------------------------ VISTA 1
v = Lienzo()
v.ent("DOCENTE", 240, 140, first_row=290)
v.ent("CREDENCIAL", 840, 140, first_row=290)
v.ent("ESTUDIANTE", 1440, 140, first_row=290)
v.rel("accede_docente", 540, 140).rel("accede_estudiante", 1140, 140)
v.conecta("CREDENCIAL", "accede_docente", "DOCENTE")
v.conecta("CREDENCIAL", "accede_estudiante", "ESTUDIANTE")
# {xor}: las dos relaciones son excluyentes (RI-12). Arco punteado por encima
# de CREDENCIAL, de rombo a rombo.
for x1, y1, x2, y2 in ((540, 104, 540, 82), (540, 82, 1140, 82), (1140, 82, 1140, 104)):
    v.body += (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#B4536B" '
               f'stroke-width="1.4" stroke-dasharray="5,4"/>\n')
v.body += ('<text x="840" y="74" text-anchor="middle" font-family="Helvetica" font-size="13" '
           'font-weight="700" fill="#B4536B">{xor} — excluyentes: una credencial, un solo rol (RI-12)</text>\n')
V[1] = v.titulo(1).svg(1640)
CAP[1] = ("<b>CREDENCIAL es la entidad que cierra el vacío V-8.</b> La Fase II diseñó "
    "el acceso completo (ventanas 014 a 019): correo y contraseña o Google/Microsoft, "
    "verificación con un código de 6 dígitos que se puede reenviar a los 30 segundos, "
    "perfil y rol. Todo eso es de la <i>cuenta</i>, no de la persona como docente o "
    "estudiante, y vive aquí — igual que en la tabla <code>credencial</code> que el "
    "incremento I1 ya construyó. <b>El correo está en CREDENCIAL y es único</b>: así no "
    "puede haber dos cuentas con el mismo correo aunque una sea de docente y otra de "
    "estudiante (RF-01-04), cosa que dos <code>UNIQUE</code> separados no garantizan. "
    "<b>DOCENTE y ESTUDIANTE siguen siendo entidades separadas</b> (decisión 1): una "
    "credencial <i>accede como</i> uno de los dos y nunca como ambos (RI-12), y el rol no "
    "cambia después: <b>el arco punteado {xor} une las dos relaciones</b> para que se "
    "lea que son excluyentes. Junto a cada entidad va su participación (mín, máx): "
    "CREDENCIAL es (0,1) en cada una porque mientras el registro está en curso —antes "
    "de elegir rol— todavía no accede como ninguno; DOCENTE y ESTUDIANTE son (1,1), "
    "porque cada uno tiene exactamente una credencial. "
    "<code>nombres</code> y <code>apellidos</code> reemplazan al antiguo <code>nombre</code> "
    "(ventanas 016 y 026).")

# ------------------------------------------------------------------ VISTA 2
# El catalogo normalizado (ADR-036) forma un cuadro con ÁREA arriba: es el
# ciclo C6, que se ve a simple vista. GRADO cuelga bajo el DBA; la columna
# de atributos del DBA se corre a un costado para dejar libres las
# lineas que salen de ellos.
v = Lienzo()
v.ent("AREA", 540, 140, first_row=260)
v.ent("DOCUMENTO_OFICIAL", 240, 560, first_row=690)
v.ent("DBA", 840, 560, dx=-240, side="left", first_row=720)
v.ent("GRADO", 840, 1010, dx=260, side="right", first_row=1100)
v.ent("EVIDENCIA", 1440, 560).ent("EVIDENCIA_DICTAMEN", 2040, 560)
v.rel("es de", 240, 140, razon_lado="arriba").rel("pertenece_area", 840, 140, razon_lado="arriba")
v.rel("se copia de", 540, 560).rel("corresponde a", 840, 800, razon_lado="izq")
v.rel("comprende", 1140, 560).rel("se dictamina", 1740, 560)
v.conecta("DOCUMENTO_OFICIAL", "es de", "AREA")
v.conecta("DBA", "pertenece_area", "AREA")
v.conecta("DBA", "se copia de", "DOCUMENTO_OFICIAL")
v.conecta("DBA", "corresponde a", "GRADO")
v.conecta("DBA", "comprende", "EVIDENCIA")
v.conecta("EVIDENCIA", "se dictamina", "EVIDENCIA_DICTAMEN")
V[2] = v.titulo(2).svg(2240)
CAP[2] = ("<b>DBA y EVIDENCIA son dato del MEN</b>, referenciado, no generado por "
    "nosotros: el catálogo es de solo lectura (SUB-06). <b>ÁREA, GRADO y "
    "DOCUMENTO_OFICIAL son nuevas</b> (ADR-036, pedido del docente en la revisión del "
    "2026-10-22): el área y el grado dejan de ser texto suelto dentro de cada DBA, y "
    "cada DBA dice de qué documento oficial del MEN se copió —con su versión, que se lee "
    "del documento y no del nombre del archivo (ADR-033)—. <b>El cuadro de arriba es el ciclo "
    "C6</b>: el documento de un DBA tiene que ser de su misma área (RI-20), y el modelo "
    "relacional lo vuelve estructura. El código del DBA es <code>ÁREA-GG-NN</code>, sin "
    "tildes: <code>MAT-08-01</code> (RI-21). "
    "EVIDENCIA es <b>entidad débil</b> "
    "—se identifica por la llave de su DBA más su <b>llave parcial</b> "
    "<code>numero_evidencia</code> (subrayado punteado)— y por eso <i>comprende</i> es "
    "una <b>relación identificadora</b> (rombo doble). "
    "<b>EVIDENCIA_DICTAMEN guarda el único juicio nuestro</b> sobre ese material: si "
    "una evidencia admite formato cerrado (ADR-006, RF-06-02) y <b>cuál</b> "
    "(<code>formato</code>): «el formato de los ítems lo determina la evidencia» "
    "(RF-03-01), y una pregunta propia se crea con él (RF-03-07, RI-19). No lo produce el MEN, y "
    "tenerlo dentro de EVIDENCIA borraba la frontera entre contenido oficial y criterio "
    "propio. Su participación es (0,1): mientras no termine el censo QA-014 una "
    "evidencia puede no estar dictaminada (V-6).")

# ------------------------------------------------------------------ VISTA 3
v = Lienzo()
v.ref("DOCENTE", 240, 140, 1)
v.ent("EXPERIENCIA", 760, 140, dx=-260, first_row=290)
v.ref("DBA", 1280, 140, 2)
v.ent("EXPERIENCIA_EVIDENCIA", 760, 620, first_row=770)
v.ref("EVIDENCIA", 1280, 620, 2)
v.rel("crea", 500, 140).rel("se ancla a", 1020, 140)
v.rel("incluye", 760, 390, razon_lado="izq").rel("sobre", 1020, 620)
v.conecta("DOCENTE", "crea", "EXPERIENCIA")
v.conecta("EXPERIENCIA", "se ancla a", "DBA")
v.conecta("EXPERIENCIA", "incluye", "EXPERIENCIA_EVIDENCIA")
v.conecta("EVIDENCIA", "sobre", "EXPERIENCIA_EVIDENCIA")
V[3] = v.titulo(3).svg(1460)
CAP[3] = ("<b>EXPERIENCIA_EVIDENCIA dice qué evidencias diagnostica esta experiencia</b> "
    "(hallazgo H-4 del docente). Desde esta versión <b>cada fila es una evidencia "
    "incluida</b> y ya no lleva el atributo <code>incluida</code>: el docente no elige "
    "evidencias (QA-010) y solo entran las que el dictamen admite (RF-03-01), así que "
    "una fila con <code>incluida = falso</code> no decía nada que su ausencia no diga. Se "
    "fija al crear la experiencia y no cambia aunque cambie el dictamen después. "
    "La participación de EXPERIENCIA en <i>incluye</i> es (1,N): una experiencia sin "
    "evidencias no diagnostica nada. <b>Esta vista tiene un ciclo</b> (C1): "
    "EXPERIENCIA → EXPERIENCIA_EVIDENCIA → EVIDENCIA → DBA → EXPERIENCIA. Se cierra con "
    "RI-18 —la evidencia incluida tiene que ser del DBA al que se ancla la experiencia—, "
    "que el modelo relacional vuelve estructura con una llave foránea compuesta; antes "
    "el motor aceptaba incluir una evidencia de otro DBA. <code>estado</code> es Borrador o "
    "Publicada, sin vuelta atrás (ADR-026); <code>fecha_publicacion</code> queda nula "
    "mientras sea Borrador. <code>servicio_ia</code> y <code>modelo_ia</code> dicen con qué "
    "servicio y modelo se generó su banco: un banco sale entero de un solo servicio "
    "(RF-03-02), así que es un dato de la experiencia, no de cada ítem (RI-17).")

# ------------------------------------------------------------------ VISTA 4
v = Lienzo()
v.ref("EXPERIENCIA_EVIDENCIA", 240, 110, 3)
v.ent("ITEM", 840, 110).ent("OPCION", 1440, 110)
v.rel("genera", 540, 110).rel("ofrece", 1140, 110)
v.conecta("EXPERIENCIA_EVIDENCIA", "genera", "ITEM")
v.conecta("ITEM", "ofrece", "OPCION")
V[4] = v.titulo(4).svg(1640)
CAP[4] = ("El banco se genera <b>por experiencia</b>: 12 ítems por evidencia incluida, en "
    "el mismo acto de crearla, todo o nada (RF-03-01, ADR-027) — por eso la participación "
    "de EXPERIENCIA_EVIDENCIA en <i>genera</i> es (12,N): nacen 12 y ninguno se borra "
    "—descartar solo lo excluye—. "
    "<b>El banco es del docente</b> (ADR-026): puede editar, descartar y agregar "
    "preguntas propias mientras la experiencia está en Borrador. <code>origen</code> "
    "distingue <code>ia</code>, <code>editado_docente</code> y <code>creado_docente</code>; "
    "el servicio y el modelo que generaron un ítem de origen IA son los de su experiencia "
    "(Vista 3, RF-03-03). <code>excluido</code> es «descartar»: no borra, oculta y "
    "se puede revertir. Sale <code>estado_revision</code>: revisar el banco no es "
    "requisito de nada y ningún requerimiento lo usa (cierra V-7). "
    "Los mínimos de opciones por formato están en RI-4: 2, y <b>4 en "
    "<code>matching</code></b>.")

# ------------------------------------------------------------------ VISTA 5
v = Lienzo()
v.ref("ESTUDIANTE", 240, 140, 1)
v.ent("INSCRIPCION", 800, 140, dx=-280, first_row=290)
v.ref("EXPERIENCIA", 1360, 140, 3)
v.ent("PRESENTACION", 800, 640, first_row=790)
v.ref("ITEM", 1360, 640, 4)
v.rel("realiza", 520, 140).rel("pertenece a", 1080, 140)
v.rel("atiende", 800, 400, razon_lado="izq").rel("se presenta", 1080, 640)
v.conecta("ESTUDIANTE", "realiza", "INSCRIPCION")
v.conecta("INSCRIPCION", "pertenece a", "EXPERIENCIA")
v.conecta("INSCRIPCION", "atiende", "PRESENTACION")
v.conecta("ITEM", "se presenta", "PRESENTACION")
V[5] = v.titulo(5).svg(1540)
CAP[5] = ("<b>PRESENTACION registra el hecho de haber mostrado un ítem</b> —distinto del "
    "de haberlo respondido (H-2, H-3)—, con su orden y su fecha (RF-04-04). Así se "
    "reconstruye la secuencia adaptativa, y una pregunta mostrada y no respondida "
    "vuelve a aparecer al retomar, sin gastar uno de los 6 cupos (ADR-031, RF-04-09). "
    "Es entidad <b>débil</b> de la Inscripción y del Ítem a la vez. "
    "<code>progreso</code> de la inscripción —No iniciada, En curso, Completada "
    "(RF-04-01)— va en elipse punteada: se calcula de sus presentaciones y resultados y "
    "no se guarda. Es lo que la v3 del docente llamaba <code>estado_avance</code>. "
    "<b>El ítem presentado tiene que ser de la experiencia de la inscripción</b> (RI-13, "
    "ciclo C2): "
    "el modelo relacional lo vuelve estructura con la misma técnica que ya usa en "
    "Resultado. Esto cierra el «hueco» que el borrador del modelo relacional había "
    "dejado declarado.")

# ------------------------------------------------------------------ VISTA 6
v = Lienzo()
v.ref("PRESENTACION", 240, 140, 5)
v.ent("RESPUESTA", 800, 140, dx=-280, first_row=300)
v.asoc("RESPUESTA_OPCION", 1140, 140, "selecciona", first_row=300)
v.ref("OPCION", 1500, 140, 4)
v.rel("registra", 520, 140)
v.conecta("PRESENTACION", "registra", "RESPUESTA")
v.body += g.link(890, 140, 1049, 140, card=SEL["part_a"], total=SEL["total_a"])
v.body += g.link(1231, 140, 1410, 140, card=SEL["part_b"], total=SEL["total_b"])
V[6] = v.titulo(6).svg(1700)
CAP[6] = ("<b>RESPUESTA_OPCION es una entidad asociativa</b>: la relación "
    "<i>selecciona</i> hecha entidad, con su atributo <code>valor_dado</code> (la "
    "posición en <code>ordering</code>, la pareja en <code>matching</code>, ADR-019). "
    "<b>La opción elegida tiene que ser del ítem que se presentó</b> (RI-6, ciclo C4): "
    "antes solo lo cuidaba el servicio y el motor aceptaba una opción de otro ítem; ahora "
    "el modelo relacional lo vuelve estructura. RESPUESTA es entidad <b>propia</b>: cuelga "
    "de una sola entidad y no resuelve ninguna N:M. "
    "<b>La participación (0,1) de PRESENTACION en <i>registra</i> es deliberada:</b> una Presentación sin "
    "Respuesta significa «se le mostró y no respondió». La Respuesta se guarda al "
    "confirmar la certeza, no al final (RF-04-06): <code>certeza</code> es el CRI 0-5 y "
    "<code>correcta</code> es derivado y se guarda — en emparejamiento y ordenamiento, "
    "solo si todos los pares o posiciones están bien.")

# ------------------------------------------------------------------ VISTA 7
v = Lienzo()
v.ref("INSCRIPCION", 240, 140, 5)
v.ent("RESULTADO", 840, 140, dx=-300, first_row=300)
v.ref("EXPERIENCIA_EVIDENCIA", 1440, 140, 3)
v.ent("REPORTE", 840, 700, first_row=850)
v.ref("EXPERIENCIA", 1440, 700, 3)
v.rel("arroja", 540, 140).rel("mide", 1140, 140)
v.rel("se agrega en", 840, 430, razon_lado="izq").rel("resume", 1140, 700)
v.conecta("INSCRIPCION", "arroja", "RESULTADO")
v.conecta("EXPERIENCIA_EVIDENCIA", "mide", "RESULTADO")
v.conecta("RESULTADO", "se agrega en", "REPORTE")
v.conecta("REPORTE", "resume", "EXPERIENCIA")
V[7] = v.titulo(7).svg(1640)
CAP[7] = ("RESULTADO es entidad <b>débil</b> de la Inscripción y de la evidencia "
    "<b>de esa experiencia</b>. <code>estado</code> —muestra / no muestra / no "
    "concluyente, nunca un puntaje— es <b>derivado y persistido</b> como fotografía del "
    "momento en que se concluyó, con su <code>fecha_calculo</code> (ADR-021). "
    "<b>La regla que lo calcula ya está definida</b> (RF-04-07, ADR-016) y cierra el vacío "
    "V-5: señal fuerte es una respuesta con certeza de 3 a 5; desde la 4.ª respuesta, si "
    "más de la mitad son señales fuertes de «muestra» concluye Muestra, si son de «no "
    "muestra» concluye No muestra, y con 6 sin cumplirse, No concluyente. "
    "<b>REPORTE se dibuja punteado porque no persiste</b>: estado general por estudiante "
    "con 4 estados y precedencia (ADR-022) y clasificación por evidencia con umbral fijo "
    "(ADR-013, 017, 023).")

# ----------------------------------------------------------------- LEYENDA
v = Lienzo()
y = 110
v.body += g.entity_box(200, y, "ENTIDAD")[0]
v.body += g.entity_box(200, y + 130, "DÉBIL", double=True)[0]
v.body += g.entity_ref(200, y + 270, "COSTURA", "N")[0]
v.body += g.relation_diamond2(620, y, "relación", razon="1:n")[0]
v.body += g.relation_diamond2(620, y + 130, "identificadora", ident=True)[0]
v.body += g.relation_diamond2(620, y + 270, "derivada", derivada=True)[0]
v.body += g.link(950, y - 20, 1150, y - 20, card="(0,N)")
v.body += g.link(950, y + 110, 1150, y + 110, card="(1,N)", total=True)
etiquetas = [
    (1200, y - 16, "participación parcial (0,N) — línea simple"),
    (1200, y + 114, "participación total (1,N) — línea doble"),
    (1200, y + 254, "elipse negra = llave primaria"),
    (1200, y + 312, "subrayado punteado = llave parcial de una entidad débil"),
    (1200, y + 370, "atributo"),
    (1200, y + 428, "elipse punteada = derivado"),
    (950, y + 460, "Las llaves foráneas no se dibujan: las produce el modelo relacional a partir de cada relación (H-8)."),
    (700, y + 44, "razón de cardinalidad — el tipo de la relación (1:1, 1:n, n:m)"),
    (950, y + 486, "elipse punteada = atributo derivado: «se guarda» (ADR-021) o «calculado» (no se guarda)"),
    (950, y + 512, "(mín, máx) junto a cada entidad = cuántas veces participa un ejemplar suyo en la relación"),
    (950, y + 538, "{xor} punteado entre dos relaciones = son excluyentes"),
]
v.body += g.attribute_stack(1000, y + 200, [("id", "PK"), ("posición", "PD"), ("atributo", ""),
                                            ("total", "C")], y + 250)[0]
for x, yy, txt in etiquetas:
    v.body += (f'<text x="{x}" y="{yy}" font-family="Helvetica" font-size="13" '
               f'fill="#555555">{txt}</text>\n')
v.fondo_max = y + 560
LEYENDA = g.wrap_svg(1700, int(v.fondo_max), v.body)

# -------------------------------------------------------------------- HTML
bloques = [(LEYENDA, "<b>Notación.</b> Chen: rectángulos para entidades, rombos para "
            "relaciones, elipses para atributos. Elipse negra = llave primaria; subrayado "
            "punteado = llave parcial de una entidad débil. <b>Las llaves foráneas no se "
            "dibujan</b>: son lo que el modelo relacional deriva de cada relación (hallazgo "
            "H-8 del docente). Doble borde = entidad débil; rombo "
            "doble = relación identificadora; línea doble = participación total; "
            "punteado = derivado, no persiste. Junto a cada rombo va la "
            "<b>razón de cardinalidad</b> (1:1, 1:n, n:m). Las <b>costuras</b> son "
            "entidades ya presentadas en una vista anterior, que reaparecen solo para "
            f"mostrar el enganche — el modelo tiene {N_ENTIDADES} entidades (Reporte no "
            "cuenta: es vista derivada), no una por cada caja dibujada.")]
bloques.append((MAPA, CAP_MAPA))
for n in range(1, 8):
    bloques.append((V[n], CAP[n]))

g.wrap_html("Modelo Entidad-Relación — AdaptiveLearn",
            f"Versión final de la Fase III · 2026-10-21 · notación Chen · {N_ENTIDADES} "
            f"entidades, {N_REL_REALES} relaciones · siete vistas por ciclo de vida del sistema",
            bloques, "mer-vistas-chen.html")

for n in range(1, 8):
    open(f"vista{n}.svg", "w", encoding="utf-8").write(V[n])
open("leyenda.svg", "w", encoding="utf-8").write(LEYENDA)
open("mapa-chen.svg", "w", encoding="utf-8").write(MAPA)
print("generado: mer-vistas-chen.html + mapa-chen.svg + vista1-7.svg + leyenda.svg")
