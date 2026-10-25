"""Llena la plantilla oficial E0 (curso 203447), aplicada en Modo B."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_relleno import *

ORIGEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "originales",
                      "U1_PL-E0_Entrevista_Tecnica_d52abb9283c84f234fd62cf9a94d0b24.docx")
DESTINO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "E0_Entrevista_Tecnica_AdaptiveLearn.docx")

z, root = abrir(ORIGEN)
b = root.find(W + "body")


def caja(i, esperado):
    t = "".join(b[i].itertext())
    assert t.startswith(esperado), (i, t[:40])
    return b[i]


DOC = "**Lo que responde la evidencia documental (Modo B)**"
CONSULTA = "**Pendiente de consulta al docente del curso**"


def bloque(i, documental, pendientes):
    """Cada bloque en Modo B: lo que responde el caso documentado, con su
    cita, y lo que no, marcado para consultar al docente."""
    items = [("h", "Lo que responde la evidencia documental (Modo B)")] + documental
    items += [("h", "Pendiente de consulta al docente del curso")]
    items += [("pend", p) for p in pendientes]
    rellenar_caja(caja(i, "Respuestas registradas"), [("Respuestas registradas", items)])


# ------------------------------------------------------------ registro
rellenar_clave_valor(b[7], {
    "Equipo": ["Selenis Acosta Paternina · Dagner Causil Almanza · Marinelly Pérez Salcedo · Natalia Pinto Torres · Carmen Sarmiento Villadiego · Alejandro Álvarez Peralta"],
    "Integrante que condujo": ("pend", "Pendiente: el equipo lo asigna"),
    "Integrante que tomó": ("pend", "Pendiente: el equipo lo asigna"),
    "Nombre del informante": "Docente del curso 203447, en su rol de responsable del producto (Modo B)",
    "Rol y relación": "Responsable del producto para efectos del ejercicio. No es usuario final del sistema",
    "Institución": "Universidad de Córdoba — curso 203447",
    "Fecha y duración": ("pend", "Pendiente: se registra en la sesión de consulta"),
    "Modalidad": ("pend", "Pendiente: se registra en la sesión de consulta"),
    "Modo aplicado": ["**B.** El equipo no tuvo acceso a un informante del contexto escolar. Lo que responde la evidencia documental se registra con su cita; lo que no, queda marcado para consulta al docente. No se atribuye ninguna frase a una persona que no la dijo."],
    "Autorización de registro": ("pend", "Pendiente: se registra en la sesión de consulta"),
})

# -------------------------------------------------------- consentimiento
rellenar_caja(caja(18, "Texto para leer"), [
    ("Respuesta del informante:", [("pend", "se registra en la sesión de consulta con el docente del curso")]),
    ("¿Autoriza el uso del nombre", [("pend", "se registra en la sesión de consulta")]),
    ("¿Autoriza grabación", [
        ("pend", "se registra en la sesión de consulta"),
        "**No se entrevistó a ningún menor de edad.** El producto se dirige a estudiantes de 11 a 17 años; toda la información sobre ellos proviene de fuentes públicas y agregadas (ICFES, MEN, MinTIC), nunca de un menor.",
    ]),
], limpiar_vacios=True)

# ------------------------------------------------------- preparacion
rellenar_caja(caja(23, "Objetivo:"), [("Objetivo:", [
    "Establecer si la dificultad que AdaptiveLearn asume —que un docente de secundaria no tiene una forma fundamentada de saber qué evidencias de aprendizaje de un DBA alcanzan y cuáles no sus estudiantes— es una necesidad real y documentada del sistema educativo colombiano, o una premisa que el equipo dio por cierta sin comprobarla.",
])])

rellenar_caja(caja(26, "Supuesto 1:"), [
    ("Supuesto 1:", ["«Un docente colombiano que quiere diseñar una experiencia alineada al currículo del MEN debe consultar DBA, evidencias oficiales y estándares, y construir preguntas desde cero — trabajo que toma horas que no tiene.» *(transcrito de `diseno/vision.md`, escrito antes de este ejercicio)*"]),
    ("Supuesto 2:", ["El problema principal es de **tiempo de preparación** del docente: si se le ahorra construir el material, el problema queda resuelto."]),
    ("Supuesto 3:", [
        "Las condiciones técnicas de las instituciones permiten un producto web de uso individual por estudiante en sala de cómputo.",
        "*Nota:* el propio proyecto ya advertía, antes de esta entrevista: «esta premisa nunca se confrontó con un docente real — sigue siendo hipótesis, no hecho verificado». Esa advertencia es la razón de ser de este instrumento para el equipo. Además, el equipo llega con un producto ya diseñado, lo que invierte el orden «primero el problema, después la solución»; se declara y se compensa sometiendo estos supuestos a refutación (apartado 15).",
    ]),
])

# ------------------------------------------------------------ bloque A
bloque(36, [
    "**Población y área.** Secundaria, grados 6° a 11° (11 a 17 años), en las cuatro áreas con DBA del MEN: Matemáticas, Lenguaje, Ciencias Naturales y Ciencias Sociales.",
    "**Estado del aprendizaje.** Saber 11 de 2025: promedio global nacional **257,6/500**, quinto año de mejora marginal (+1,5). El LEE de la Universidad Javeriana lo describe como *aprendizajes estancados*.",
    ("tbl", ["Brecha", "2024", "2025"], [
        ["Urbano (262,1) — rural (236,2)", "24 puntos", "**26 puntos**, la mayor en cinco años"],
        ["Privado (281) — oficial (250)", "29 puntos", "**31 puntos**"],
        ["Hombres (262,4) — mujeres (253,5)", "—", "**9 puntos**"],
    ], [3, 1, 3]),
    "**Referentes curriculares.** DBA (v2 en Matemáticas, Lenguaje y Sociales; v1 en Naturales), Estándares Básicos de Competencias y Lineamientos Curriculares.",
    "**Rasgo decisivo del marco:** los DBA no son una secuencia rígida por grado.",
    ("cita", "«Si bien los DBA se formulan para cada grado, el maestro puede trasladarlos de uno a otro en función de las especificidades de los procesos de aprendizaje de los estudiantes. De esta manera, los DBA son una estrategia para promover la flexibilidad curricular.» — MEN, DBA Matemáticas V.2, sección 3."),
    "*Fuentes:* ICFES, resultados Saber 11 2025; LEE Javeriana, Informe 114 (2025); MEN, DBA Matemáticas V.2.",
], [
    "Cómo transcurre una clase típica del tema en una institución de la región.",
    "Número real de estudiantes por grupo y frecuencia de encuentro.",
    "Qué referentes usa efectivamente un docente al planear, frente a los que indica la norma.",
])

# ------------------------------------------------------------ bloque B
bloque(47, [
    "**El problema no es la falta de resultados, sino su escala y su oportunidad.** Saber es censal, externa y anual: llega cuando terminó el año e informa por área y competencia. No le dice a un docente qué evidencias de aprendizaje de un DBA alcanzó cada estudiante de su grupo.",
    "**El marco oficial ya define la unidad observable pero no provee el instrumento.** Cada DBA se formula con evidencias de aprendizaje que, según el MEN, *«todas en su conjunto buscan dar pistas adecuadas del aprendizaje expresado en el enunciado»* (DBA Matemáticas V.2, §3.1). Qué observar ya está escrito; con qué observarlo queda en manos del docente.",
    "**Por qué persiste pese a los recursos existentes.** Las brechas crecientes entre lo rural y lo urbano, y entre lo oficial y lo privado, indican que los recursos disponibles no llegan igual, o no resuelven lo mismo, en ambos contextos.",
], [
    "Qué contenido o competencia le cuesta más que los estudiantes alcancen, con un caso concreto y reciente. **Es la ausencia que más pesa:** ninguna estadística nacional sustituye el relato de la última vez que ocurrió.",
    "Qué ha intentado y con qué resultado.",
    "Si es un problema de un grupo o se repite cada año.",
])

# ------------------------------------------------------------ bloque C
bloque(58, [
    ("tbl", ["Usuario", "Banda de edad", "Qué necesita", "Qué hace en el sistema"], [
        ["**Docente**", "Adulto", "Saber qué evidencias de un DBA alcanzan sus estudiantes, sin construir el instrumento desde cero", "Crea la experiencia, la ancla a un DBA, revisa el banco de ítems, publica, consulta el reporte"],
        ["**Estudiante**", "**11 a 17 años** (6° a 11°)", "Responder un diagnóstico breve sin recibir un veredicto sobre sí mismo", "Se une con un código, responde ítems, declara su certeza"],
    ], [2, 2, 4, 4]),
    "**El acudiente no está modelado en esta versión**, con consecuencias que se declaran en el Bloque G.",
    "**Sobre los grados visibles.** El selector permite anclar a un DBA de 1° a 11° aunque la población sea secundaria: se apoya en la cita del Bloque A. Un docente de 8° que detecta un vacío de un DBA de 5° debe poder diagnosticarlo.",
], [
    "Si los estudiantes trabajarían solos o acompañados.",
    "Qué necesitaría ver un docente que hoy no ve.",
    "Si hay estudiantes con condiciones que requieran apoyos específicos (ver Bloque H).",
])

# ------------------------------------------------------------ bloque D
bloque(68, [
    "Lo que existe hoy, y por qué no cubre esta necesidad:",
    ("tbl", ["Instrumento", "Qué resuelve", "Qué deja sin resolver"], [
        ["Pruebas Saber (ICFES)", "Comparabilidad nacional, medición del sistema", "Llegan al cierre del año, agregan por área, no informan sobre el grupo en curso"],
        ["**Evaluar para Avanzar 3° a 11°** (ICFES — MEN)", "Evaluación formativa gratuita y voluntaria; explica al docente qué evalúa cada pregunta y por qué cada opción es o no correcta", "Instrumentos diseñados de antemano por el ICFES, organizados por área y competencia: el docente no elige el DBA. *No se verificó si sus reportes llegan al nivel de evidencia de un DBA*"],
        ["Plataformas de contenido y ejercitación", "Práctica y repetición", "El contenido no está anclado a la evidencia oficial del DBA"],
        ["Cuestionarios del propio docente", "Ajuste total al contexto", "Cuestan tiempo de preparación"],
    ], [3, 4, 5]),
    "*Fuentes:* ICFES; MEN, comunicado *Novedades de Evaluar para Avanzar 3° a 11°*.",
], [
    "Qué recursos digitales usa hoy, qué le funciona y qué le estorba.",
    "Si ha dejado de usar alguno y por qué — lo abandonado dice más que lo adoptado.",
    "Cómo registra hoy el avance de los estudiantes.",
])

# ------------------------------------------------------------ bloque E
bloque(77, [
    "El proyecto adoptó un criterio que limita qué cuenta como éxito: **nada se declara con certeza.** Ni un acierto certifica dominio ni un error certifica una brecha. Por eso cada respuesta lleva el índice de certeza del propio estudiante (CRI, Hasan, Bagayoko y Kelley, 1999), y un acierto con certeza baja no cuenta como evidencia fuerte.",
    "Criterios de éxito verificables dentro del sistema:",
    ("ul", [
        "Que el docente obtenga, por evidencia y estudiante, un estado entre *muestra*, *no muestra* y *no concluyente*, admitiendo el tercero.",
        "Que ningún estado se emita con menos de 4 ítems respondidos (Shrock y Coscarelli: 4 a 6 preguntas por objetivo).",
        "Que ningún texto mostrado al docente lo haya redactado la IA sin su revisión.",
    ]),
], [
    "En qué se fijaría, a un semestre de uso, para decir que sirvió.",
    "Qué señal le indicaría que un estudiante avanzó.",
    "Qué tendría que ocurrir para que dejara de usarlo.",
])

# ------------------------------------------------------------ bloque F
bloque(88, [
    "**Conectividad.** Según el MinTIC, en 2025 el **51 % de las escuelas rurales** tenía conexión (unas 18.000), frente al 12 % de 2022. El avance es real y, aun así, **cerca de la mitad de las sedes rurales no tenía conexión** al momento de este diseño.",
    "**Equipos.** 156.546 computadores entregados en más de 8.000 instituciones: cifra grande en absoluto y pequeña frente a la matrícula. Implica **equipo compartido**, no uno por estudiante.",
    "**Consecuencia ya tomada.** El proyecto restringe esta versión a computador y difiere el acceso móvil del estudiante, reconociendo el acceso desigual a sala de cómputo. Diseñar suponiendo dispositivo personal y conexión permanente sería excluyente en la región.",
    "*Fuente:* MinTIC, reporte de conectividad en sedes educativas rurales, 2025.",
], [
    "Cuánto tiempo real de clase podría dedicarse a esto.",
    "Si hay algún costo que la institución no podría asumir.",
    "Si existe alguna restricción institucional sobre el uso de aplicaciones.",
])

# ------------------------------------------------------------ bloque G
bloque(98, [
    "**El punto de partida es una prohibición.** El **artículo 7 de la Ley Estatutaria 1581 de 2012** prohíbe el tratamiento de datos de niños, niñas y adolescentes salvo los de naturaleza pública, y exige respetar su interés superior. Vigila la Superintendencia de Industria y Comercio.",
    ("tbl", ["Dato del estudiante", "Para qué se usa", "Frente al artículo 7"], [
        ["Nombre", "Identificarlo en el listado del docente", "Dato de menor: requiere autorización del representante legal"],
        ["Correo", "Credencial de acceso", "Ídem. Un menor puede no tener correo propio"],
        ["Respuestas y certeza", "Producir el resultado por evidencia", "Dato de comportamiento, el más sensible"],
        ["Resultado por evidencia", "Alimentar el reporte del docente", "Juicio sobre el desempeño de un menor"],
    ], [2, 3, 4]),
    "**Minimización ya decidida:** no se recoge fecha de nacimiento, documento, institución ni curso; el resultado nunca es puntaje ni va acompañado de texto generado por IA; el correo se retiró de la tarjeta del listado de aula.",
    "**Vacío que este bloque destapa:** el sistema **no modela al acudiente ni su autorización**. Sin dónde registrarla, la versión actual no puede operar legalmente con estudiantes reales. No estaba declarado antes de este ejercicio.",
], [
    "Cómo maneja hoy la institución la autorización de los acudientes.",
    "Quién debería poder ver el avance de un estudiante.",
    "Qué información preferiría no registrar.",
])

# ------------------------------------------------------------ bloque H
bloque(108, [
    "El proyecto audita contraste contra **WCAG 2.2 nivel AA**, y esa auditoría arrojó un incumplimiento real sin resolver: el gris `#888888` en texto de 13 px negrita da **3.5:1**, cuando AA exige 4.5:1. Afecta a dos pantallas. Se mantiene abierto porque la corrección obvia choca con otro color del sistema y rompería la distinción entre categorías.",
    "**Decisiones ya tomadas:** todo en español; ninguna tarea depende de audio o video; sin arrastrar y soltar —emparejar y ordenar se resuelven con selectores—.",
], [
    "Si hay estudiantes con dificultades visuales, auditivas o motoras.",
    "Si hay estudiantes que aún no leen con fluidez — **crítico**: todo el diagnóstico es textual.",
    "Si hay alguna lengua distinta al español en el grupo.",
])

# ------------------------------------------------------------ bloque I
rellenar_caja(caja(118, "Respuestas registradas"), [("Respuestas registradas", [
    "**Este bloque no puede diligenciarse por vía documental:** su función es que una persona valide lo entendido. Queda para la sesión de consulta con el docente del curso, con estas preguntas preparadas:",
    ("ul", [
        "«Le repito lo que entendimos: un docente no tiene cómo saber, a nivel de evidencia de aprendizaje de un DBA, qué alcanzó cada estudiante de su grupo durante el año. ¿Es correcto?»",
        "¿Qué de lo registrado por vía documental **no** corresponde a lo que usted observa en las instituciones de la región?",
        "¿A quién más deberíamos escuchar?",
        "¿Podemos volver a consultarle si surge una duda?",
    ]),
    ("pend", "respuestas de la sesión de consulta"),
])])

# ------------------------------------------------------------ 14 sintesis
assert "".join(b[123].itertext()).startswith("Hallazgo")
rellenar_grilla(b[123], [
    ["Los aprendizajes están estancados y las brechas crecen: urbano-rural de 24 a 26 puntos y oficial-privado de 29 a 31 (2024→2025)", "ICFES; LEE Javeriana, Saber 11 2025", "1"],
    ["Saber opera a escala de área, anual y censal; el docente decide a escala de evidencia de un DBA, durante el año, sobre su grupo", "Estructura de Saber 11 frente a estructura de los DBA (MEN, §3.1)", "1, 13"],
    ["Existe evaluación formativa oficial (Evaluar para Avanzar), pero con instrumentos fijos del ICFES: el docente no elige el DBA", "ICFES — MEN, Evaluar para Avanzar 3° a 11°", "1, 14"],
    ["El marco del MEN define la unidad observable —la evidencia— pero no el instrumento", "DBA Matemáticas V.2, §3.1", "2, 4"],
    ["Los DBA son trasladables entre grados, lo que valida anclar a un DBA de otro grado", "DBA Matemáticas V.2, §3", "3, 5"],
    ["Cerca de la mitad de sedes rurales sin conexión en 2025; equipos de uso compartido", "MinTIC, 2025", "7"],
    ["Tratar datos de menores está prohibido salvo excepciones y exige autorización del representante legal", "Ley 1581 de 2012, art. 7; SIC", "7"],
    ["El sistema no modela al acudiente ni su autorización", "Modelo de datos vigente contrastado con la Ley 1581", "3, 7, 15"],
    ["Hay un incumplimiento de contraste WCAG AA sin resolver", "Auditoría propia del equipo", "7"],
])

# -------------------------------------------------------- 15 supuestos
assert "".join(b[127].itertext()).startswith("Supuesto inicial")
rellenar_grilla(b[127], [
    ["**S1** — El docente construye el instrumento desde cero y eso cuesta horas que no tiene", "**Parcialmente confirmado.** Se confirma que el marco define la unidad y no el instrumento; **no** se confirma lo de las horas: ninguna fuente lo mide", "La afirmación sobre horas no se sostiene en E1; la necesidad se reformula alrededor de la escala de medición, que sí es documentable"],
    ["**S2** — El problema es de tiempo de preparación; ahorrar la construcción del material lo resuelve", "**Refutado en su suficiencia.** Si fuera solo producción de material, los contextos con más recursos no se estarían distanciando", "El producto solo puede prometer resolver la instrumentación, no el problema educativo; obliga a declarar límites en la sección 9 de E1"],
    ["**S3** — Las condiciones técnicas permiten uso individual por estudiante en sala de cómputo", "**Refutado parcialmente.** Con la mitad de sedes rurales sin conexión y equipos compartidos, no se sostiene como condición general", "Se mantiene el uso solo en computador y el acceso desigual pasa a tratarse como decisión de sostenibilidad social"],
])

# -------------------------------------------------------- 16 decisiones
rellenar_caja(caja(131, "Decisión 1"), [
    ("Decisión 1", ["**La necesidad de E1 se reformula alrededor de la escala de medición, no del tiempo.** Motivada por la refutación parcial de S1: *«toma horas que no tiene»* no tiene fuente, y el criterio 1.1 exige evidencia verificable. La distancia entre la escala del instrumento disponible y la escala en que el docente decide sí es documentable."]),
    ("Decisión 2", ["**El consentimiento del acudiente entra como requerimiento no funcional explícito, y como límite declarado de la versión actual.** Motivada por el vacío del Bloque G: la Ley 1581 exige la autorización y el sistema no tiene dónde registrarla. En vez de simularlo, E1 lo declara como condición no satisfecha que impide el despliegue con estudiantes reales."]),
    ("Decisión 3", ["**La restricción a computador pasa de decisión técnica a decisión de sostenibilidad social**, con la cifra que la respalda. Motivada por el dato del MinTIC sobre conectividad rural."]),
])

# -------------------------------------------------------- 17 opcionales
agregar_tras_etiqueta(b[133], "Secciones opcionales que este equipo", [
    "Ninguna de las cinco en su forma prevista: no hubo entrevista grabada, ni primera entrevista con informante del contexto, ni acceso a un aula, ni instrumento complementario.",
    "**Notas de campo, en forma de análisis documental:** los bloques A a H incorporan fuentes públicas verificables que suplen parcialmente —con sus límites declarados— lo que habría aportado la observación directa.",
])

# ---------------------------------------------------------- 19 bitacora
assert "".join(b[141].itertext()).startswith("Fecha")
rellenar_grilla(b[141], [
    ["2026-09-25", "Claude (Anthropic)", "Interpretar las plantillas E0 y E1", "Lectura de ambas y mapa del material del proyecto que alimenta cada sección", "Se contrastó contra el texto de las plantillas", "—"],
    ["2026-09-25", "Claude (Anthropic)", "**Redactar la entrevista inventando un docente informante**", "La herramienta se negó", "—", "**Descartado:** habría sido testimonio atribuido a una persona inexistente. Se aplicó el Modo B que prevé el instrumento"],
    ["2026-09-25", "Claude (Anthropic)", "Buscar evidencia del contexto educativo colombiano", "Saber 11 2025, brechas, conectividad MinTIC, Ley 1581 art. 7, Evaluar para Avanzar", "Cifras contrastadas entre ICFES, LEE Javeriana y prensa", "Se descartó el promedio de 261: corresponde solo a calendario A"],
    ["2026-09-25", "Claude (Anthropic)", "Verificar que los DBA son trasladables entre grados", "Cita textual del documento oficial", "Se buscó el texto literal en la fuente", "Se descartó *«no son camisa de fuerza»*: está en los Lineamientos, no en los DBA"],
    ["2026-09-25", "Claude (Anthropic)", "Contrastar los supuestos con la evidencia", "Refutación parcial de S1, S2 y S3", "El equipo verificó que los supuestos transcritos fueran los escritos antes del ejercicio", "Se descartó la afirmación de que Saber era el único instrumento masivo: existe Evaluar para Avanzar"],
])

# ----------------------------------------------------- 20 autoverif
rellenar_clave_valor(b[143], {
    "El consentimiento": ("pend", "Pendiente"),
    "No se entrevistó a ningún menor": "✔ Sí",
    "Se declaró el modo": "✔ Sí (B)",
    "Los nueve bloques": "✔ Sí",
    "Las respuestas se registraron": "✔ Sí",
    "No se presentó la solución": ("pend", "Declarado"),
    "El bloque F": "✔ Sí",
    "El bloque G": ("pend", "Pendiente"),
    "Cada hallazgo": "✔ Sí",
    "Al menos un supuesto": "✔ Sí",
    "Las decisiones de diseño": "✔ Sí",
    "El informante validó": ("pend", "Pendiente"),
})

guardar(z, root, DESTINO)
print("generado:", os.path.normpath(DESTINO))
