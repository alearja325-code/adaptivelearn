"""Construye las 6 vistas Chen + la leyenda, y las junta en un HTML."""
import generador as g
from vistas_chen import Lienzo
from mapa_chen import MAPA, CAPTION as CAP_MAPA

V = {}
CAP = {}

# ------------------------------------------------------------------ VISTA 1
v = Lienzo()
v.ent("DBA", 240, 110).ent("EVIDENCIA", 840, 110).ent("EVIDENCIA_DICTAMEN", 1440, 110)
v.rel("comprende", 540, 110).rel("se dictamina", 1140, 110)
v.conecta("DBA", "comprende", "EVIDENCIA")
v.conecta("EVIDENCIA", "se dictamina", "EVIDENCIA_DICTAMEN")
V[1] = v.titulo(1).svg(1640)
CAP[1] = ("<b>DBA y EVIDENCIA son dato del MEN</b>, referenciado, no generado por "
    "nosotros. EVIDENCIA es <b>entidad débil</b>: no tiene identidad fuera de su DBA "
    "—se identifica por (codigo_dba, numero_evidencia)— y por eso <i>comprende</i> es "
    "una <b>relación identificadora</b> (rombo doble) con participación total de los "
    "dos lados (línea doble). "
    "<b>EVIDENCIA_DICTAMEN existe por una razón, no por simetría:</b> "
    "<code>aplica_formato_cerrado</code> —si una evidencia admite pregunta cerrada— "
    "<u>no lo produce el MEN</u>, es un juicio nuestro (ADR-006, pendiente del censo "
    "QA-014). Tenerlo dentro de EVIDENCIA borraba la frontera entre contenido "
    "curricular oficial y criterio propio, que este proyecto declara como valor. "
    "Su participación es (0,1): una evidencia puede no estar dictaminada todavía.")

# ------------------------------------------------------------------ VISTA 2
v = Lienzo()
v.ent("DOCENTE", 240, 140, first_row=290)
v.ent("EXPERIENCIA", 760, 140, dx=-260, first_row=290)
v.ref("DBA", 1280, 140, 1)
v.ent("EXPERIENCIA_EVIDENCIA", 760, 620, first_row=770)
v.ref("EVIDENCIA", 1280, 620, 1)
v.rel("crea", 500, 140).rel("se ancla a", 1020, 140)
v.rel("incluye", 760, 390, razon_lado="izq").rel("sobre", 1020, 620)
v.conecta("DOCENTE", "crea", "EXPERIENCIA")
v.conecta("EXPERIENCIA", "se ancla a", "DBA")
v.conecta("EXPERIENCIA", "incluye", "EXPERIENCIA_EVIDENCIA")
v.conecta("EVIDENCIA", "sobre", "EXPERIENCIA_EVIDENCIA")
V[2] = v.titulo(2).svg(1460)
CAP[2] = ("<b>EXPERIENCIA_EVIDENCIA es la entidad que este modelo no tenía</b> y que "
    "la revisión del docente (hallazgo H-4) señaló como faltante. Sin ella, desde una "
    "Experiencia solo se llegaba a Evidencia por dos caminos indirectos —bajando por "
    "su DBA, que devuelve <i>todas</i> las evidencias incluidas las que no aplican, o "
    "subiendo desde un Ítem— y <b>qué evidencias diagnostica realmente esta "
    "experiencia</b>, que es un hecho propio de la experiencia, no estaba en ninguna "
    "parte. Antes eso se tapaba con dos reglas externas (RI-1 y RI-2) que obligaban a "
    "los dos caminos a coincidir; <b>al volverse estructura, esas dos reglas "
    "desaparecieron</b>. La participación de EXPERIENCIA en <i>incluye</i> es (1,N), "
    "no (0,N): una experiencia sin ninguna evidencia incluida no diagnostica nada.")

# ------------------------------------------------------------------ VISTA 3
v = Lienzo()
v.ref("EXPERIENCIA_EVIDENCIA", 240, 110, 2)
v.ent("ITEM", 840, 110).ent("OPCION", 1440, 110)
v.rel("genera", 540, 110).rel("ofrece", 1140, 110)
v.conecta("EXPERIENCIA_EVIDENCIA", "genera", "ITEM")
v.conecta("ITEM", "ofrece", "OPCION")
V[3] = v.titulo(3).svg(1640)
CAP[3] = ("El banco se genera <b>por experiencia</b>, no se comparte entre "
    "experiencias distintas que usen el mismo DBA (ADR-005). Un Ítem cuelga de "
    "EXPERIENCIA_EVIDENCIA, no de Experiencia y Evidencia por separado: <b>un solo "
    "camino al currículo</b>. La participación (2,N) en <i>ofrece</i> tiene mínimos "
    "por formato (RI-4): 2 opciones en <code>single_choice</code> y en "
    "<code>ordering</code>, pero <b>4 en <code>matching</code></b>, con al menos 2 por "
    "grupo —la pareja correcta son dos opciones de distinto grupo, así que 2 no "
    "alcanza. Lo señaló el hallazgo H-9 y se aceptó. <code>hipotesis_error</code> vive "
    "en OPCION y no en ITEM (ADR-020): un ítem puede tener varios distractores, cada "
    "uno con su propia hipótesis.")

# ------------------------------------------------------------------ VISTA 4
v = Lienzo()
v.ent("ESTUDIANTE", 240, 140, first_row=290)
v.ent("INSCRIPCION", 800, 140, dx=-280, first_row=290)
v.ref("EXPERIENCIA", 1360, 140, 2)
v.ent("PRESENTACION", 800, 640, first_row=790)
v.ref("ITEM", 1360, 640, 3)
v.rel("realiza", 520, 140).rel("pertenece a", 1080, 140)
v.rel("atiende", 800, 400, razon_lado="izq").rel("se presenta", 1080, 640)
v.conecta("ESTUDIANTE", "realiza", "INSCRIPCION")
v.conecta("INSCRIPCION", "pertenece a", "EXPERIENCIA")
v.conecta("INSCRIPCION", "atiende", "PRESENTACION")
v.conecta("ITEM", "se presenta", "PRESENTACION")
V[4] = v.titulo(4).svg(1540)
CAP[4] = ("<b>PRESENTACION es la otra entidad que faltaba</b> (hallazgos H-2 y H-3). "
    "Registra el hecho de <b>haber mostrado</b> un ítem a un estudiante —un hecho "
    "distinto del de haberlo respondido. Sin ella pasaban dos cosas: un estudiante que "
    "vio una pregunta y no la contestó era <u>indistinguible</u> de uno que nunca la "
    "vio, y la secuencia adaptativa de ADR-016 (mínimo 4 ítems, tope 6, sigue o para "
    "según la certeza de lo que va respondiendo) <u>no se podía reconstruir</u>. "
    "Es entidad <b>débil</b> identificada por la Inscripción <i>y</i> el Ítem a la vez "
    "—de ahí los dos rombos dobles. Entra en esta revisión aunque la pantalla del "
    "diagnóstico todavía no esté diseñada, porque <b>el dato lo exige ADR-016</b>, que "
    "ya está decidido, no una spec de interfaz pendiente.")

# ------------------------------------------------------------------ VISTA 5
v = Lienzo()
v.ref("PRESENTACION", 240, 140, 4)
v.ent("RESPUESTA", 800, 140, dx=-280, first_row=300)
v.asoc("RESPUESTA_OPCION", 1140, 140, "selecciona", first_row=300)
v.ref("OPCION", 1500, 140, 3)
v.rel("registra", 520, 140)
v.conecta("PRESENTACION", "registra", "RESPUESTA")
v.body += g.link(890, 140, 1049, 140, card="N", total=True)
v.body += g.link(1231, 140, 1410, 140, card="M")
V[5] = v.titulo(5).svg(1700)
CAP[5] = ("<b>RESPUESTA_OPCION es una entidad asociativa</b>: el rombo dibujado "
    "<i>dentro</i> del rectángulo. No es una entidad más —es la relación "
    "<i>selecciona</i> hecha entidad, porque tiene llave propia "
    "(id_respuesta, id_opcion) y un atributo que no pertenece ni a Respuesta ni a "
    "Opción: <code>valor_dado</code>, que guarda la posición asignada en "
    "<code>ordering</code> o el número de pareja en <code>matching</code> (ADR-019). "
    "Sin ella, la opción que el estudiante eligió se perdía y esos dos formatos no "
    "eran representables. "
    "<b>La cardinalidad (0,1) de <i>registra</i> es deliberada:</b> una Presentación "
    "sin Respuesta es válida y significa exactamente <i>“se le mostró y no "
    "respondió”</i>. <code>certeza</code> es el CRI de Hasan et al. (1999), escala "
    "0-5, y es la señal de la que depende toda la regla adaptativa.")

# ------------------------------------------------------------------ VISTA 6
v = Lienzo()
v.ref("INSCRIPCION", 240, 140, 4)
v.ent("RESULTADO", 840, 140, dx=-300, first_row=300)
v.ref("EXPERIENCIA_EVIDENCIA", 1440, 140, 2)
v.ent("REPORTE", 840, 700, first_row=850)
v.ref("EXPERIENCIA", 1440, 700, 2)
v.rel("arroja", 540, 140).rel("mide", 1140, 140)
v.rel("se agrega en", 840, 430, razon_lado="izq").rel("resume", 1140, 700)
v.conecta("INSCRIPCION", "arroja", "RESULTADO")
v.conecta("EXPERIENCIA_EVIDENCIA", "mide", "RESULTADO")
v.conecta("RESULTADO", "se agrega en", "REPORTE")
v.conecta("REPORTE", "resume", "EXPERIENCIA")
V[6] = v.titulo(6).svg(1640)
CAP[6] = ("RESULTADO es entidad <b>débil</b> con dos relaciones identificadoras: "
    "depende de la Inscripción <i>y</i> de la evidencia <b>de esa experiencia</b> "
    "—no de la evidencia del MEN en abstracto, que es lo que cambió en esta revisión. "
    "<code>estado</code> es <b>derivado y persistido</b> (ADR-021): se calcula desde "
    "las Respuestas y se guarda como fotografía del momento, con su "
    "<code>fecha_calculo</code>; no se recalcula en cada lectura, porque la regla de "
    "cálculo es versionable y un resultado histórico no debería mutar. Sus valores son "
    "<b>muestra / no muestra / no concluyente</b> — nunca un puntaje ni una nota. "
    "<b>REPORTE se dibuja punteado porque no persiste:</b> es una vista calculada "
    "sobre RESULTADO, no una tabla. Dibujarla como entidad normal sugeriría una "
    "escritura que no existe.")

# ----------------------------------------------------------------- LEYENDA
v = Lienzo()
y = 110
v.body += g.entity_box(200, y, "ENTIDAD")[0]
v.body += g.entity_box(200, y + 130, "DÉBIL", double=True)[0]
v.body += g.entity_ref(200, y + 270, "COSTURA", "N")[0]
v.body += g.relation_diamond2(620, y, "relación", razon="1:n")[0]
v.body += g.relation_diamond2(620, y + 130, "identificadora", ident=True)[0]
v.body += g.relation_diamond2(620, y + 270, "derivada", derivada=True)[0]
v.body += g.link(950, y - 20, 1150, y - 20, card="1")
v.body += g.link(950, y + 110, 1150, y + 110, card="N", total=True)
etiquetas = [
    (1200, y - 16, "participación parcial (0,N) — línea simple"),
    (1200, y + 114, "participación total (1,N) — línea doble"),
    (1200, y + 244, "atributo · elipse negra = llave primaria"),
    (700, y + 44, "razón de cardinalidad — el tipo de la relación (1:1, 1:n, n:m)"),
]
v.body += g.attribute_stack(1000, y + 200, [("id", "PK"), ("atributo", "")], y + 250)[0]
for x, yy, txt in etiquetas:
    v.body += (f'<text x="{x}" y="{yy}" font-family="Helvetica" font-size="13" '
               f'fill="#555555">{txt}</text>\n')
v.fondo_max = y + 400
LEYENDA = g.wrap_svg(1700, int(v.fondo_max), v.body)

# -------------------------------------------------------------------- HTML
bloques = [(LEYENDA, "<b>Notación.</b> Chen: rectángulos para entidades, rombos para "
            "relaciones, elipses para atributos. Doble borde = entidad débil; rombo "
            "doble = relación identificadora; línea doble = participación total; "
            "punteado = derivado, no persiste. Debajo de cada rombo va la "
            "<b>razón de cardinalidad</b> (1:1, 1:n, n:m): el tipo de la relación "
            "leído de un vistazo. Es la misma información que los <code>1</code> y "
            "<code>N</code> de las líneas, resumida — convención de la notación, no "
            "un dato adicional. No debe confundirse con la <b>participación</b>, que "
            "es lo que dicen las líneas simple/doble. "
            "Las <b>costuras</b> son entidades ya "
            "presentadas en una vista anterior, que reaparecen solo para mostrar el "
            "enganche — el modelo tiene 14 entidades (Reporte no cuenta: es vista derivada), no una por cada caja dibujada.")]
bloques.append((MAPA, CAP_MAPA))
for n in range(1, 7):
    bloques.append((V[n], CAP[n]))

g.wrap_html("Modelo Entidad-Relación — AdaptiveLearn",
            "Quinta revisión · 2026-09-08 · notación Chen · 14 entidades, 16 relaciones "
            "· seis vistas por ciclo de vida del sistema",
            bloques, "mer-vistas-chen.html")

for n in range(1, 7):
    open(f"vista{n}.svg", "w", encoding="utf-8").write(V[n])
open("leyenda.svg", "w", encoding="utf-8").write(LEYENDA)
print("generado: mer-vistas-chen.html + vista1-6.svg + leyenda.svg")
