"""Llena la plantilla oficial E1 (curso 203447) con el contenido del equipo."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_relleno import *

ORIGEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "originales",
                      "U1_PL-E1_Requerimientos_de_Producto_197d1b1cac90a24882aae251132a6673.docx")
DESTINO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "E1_Requerimientos_de_Producto_AdaptiveLearn.docx")
REPO = "https://github.com/aalvarezperalta84-lab/AdaptiveLearn"

z, root = abrir(ORIGEN)
b = root.find(W + "body")


def caja(i, esperado):
    """Localiza la caja por indice y comprueba que es la esperada."""
    t = "".join(b[i].itertext())
    assert t.startswith(esperado), (i, t[:40])
    return b[i]


# ------------------------------------------------------------- equipo
rellenar_clave_valor(b[7], {
    "Nombre del equipo": ("pend", "nombre del equipo, por definir"),
    "Integrantes": ["Selenis Acosta Paternina", "Dagner Causil Almanza",
                    "Marinelly Pérez Salcedo", "Natalia Pinto Torres",
                    "Carmen Sarmiento Villadiego", "Alejandro Álvarez Peralta"],
    "Producto que diseñan": "AdaptiveLearn — diagnóstico por evidencias de aprendizaje, anclado a los Derechos Básicos de Aprendizaje (DBA) del MEN",
    "Enlace al repositorio": REPO,
    "Fecha de entrega real": "26 de septiembre de 2026",
    "Versión del documento": "1.0",
})

# ------------------------------------------------------------------ 1
rellenar_caja(caja(28, "Contexto:"), [
    ("Contexto:", [
        "Educación secundaria oficial colombiana, grados 6° a 11°. Los resultados Saber 11 de 2025 dieron un promedio global nacional de **257,6 sobre 500**: quinto año consecutivo de mejora, pero marginal (+1,5 puntos frente a 2024). El Laboratorio de Economía de la Educación (Universidad Javeriana) caracteriza el conjunto como *aprendizajes estancados*: las variaciones por área, de 0,4 a 1 punto, no representan un cambio sustantivo.",
        "Lo que sí cambió son las brechas, y en la dirección equivocada:",
        ("tbl", ["Brecha", "2024", "2025"], [
            ["Urbano (262,1) — rural (236,2)", "24 puntos", "**26 puntos**, la mayor en cinco años"],
            ["Privado (281) — oficial (250)", "29 puntos", "**31 puntos**"],
            ["Hombres (262,4) — mujeres (253,5)", "—", "**9 puntos**, la más alta en cinco años"],
        ], [3, 1, 3]),
    ]),
    ("Necesidad identificada:", [
        "**Existe una distancia entre la escala en que se mide el aprendizaje y la escala en que el docente decide.**",
        "Las pruebas Saber son censales, externas y anuales: informan por área y competencia cuando el año escolar ya terminó. El ICFES ofrece además **Evaluar para Avanzar**, una estrategia formativa gratuita para los grados 3° a 11°; es un avance real, pero sus instrumentos los diseña el ICFES de antemano y están organizados por área y competencia. En ninguno de los dos casos el docente puede elegir un DBA concreto y obtener, estudiante por estudiante, qué evidencias de aprendizaje de ese DBA se muestran y cuáles no.",
        "El marco curricular oficial **ya define la unidad observable a esa escala**: cada DBA se formula con un enunciado y un conjunto de evidencias de aprendizaje, sobre las que el MEN afirma que *«todas en su conjunto buscan dar pistas adecuadas del aprendizaje expresado en el enunciado»*. El marco define la unidad; no provee el instrumento para observarla en el aula. Esa es la necesidad.",
    ]),
    ("Fuente de la que proviene", [
        "ICFES. *Informe nacional de resultados Saber 11*, resultados 2025.",
        "Laboratorio de Economía de la Educación, Pontificia Universidad Javeriana. *Pruebas Saber 11: cerrando brechas de sector, mas no de zona* (Informe 114, 2025).",
        "Ministerio de Educación Nacional. *Derechos Básicos de Aprendizaje — Matemáticas V.2*, secciones 3 y 3.1.",
        "ICFES y Ministerio de Educación Nacional. *Evaluar para Avanzar 3° a 11°* — estrategia de evaluación formativa.",
    ]),
    ("Evidencia que la sustenta:", [
        "La evidencia documental sostiene tres cosas: que los aprendizajes están estancados, que las brechas crecen, y que los instrumentos disponibles no operan sobre la evidencia de un DBA elegido por el docente.",
        "**Lo que la evidencia no sostiene, y por eso no se afirma.** El equipo partía del supuesto de que construir el instrumento *«toma horas que el docente no tiene»*. Ninguna fuente consultada mide ese tiempo. El supuesto fue refutado en su parte no documentable durante el levantamiento (E0, apartado 15) y la necesidad se reformuló alrededor de la escala, que sí es verificable.",
        "**Declaración de orden.** El equipo llegó al levantamiento con un producto ya diseñado, lo que invierte el orden que exige el criterio 1.1. No se disimula: se compensó sometiendo los tres supuestos de partida a refutación documental, y ninguno sobrevivió intacto (E0, apartado 15).",
        "**Punto a verificar.** El equipo no comprobó si los reportes de Evaluar para Avanzar pueden desagregarse al nivel de evidencia de un DBA. Si pudieran, la necesidad se reduciría a la libertad del docente para elegir el DBA; se declara como verificación pendiente.",
    ]),
])

# ------------------------------------------------------------------ 2
rellenar_caja(caja(33, "Área y grado:"), [
    ("Área y grado:", [
        "Las cuatro áreas con DBA publicados por el MEN: **Matemáticas, Lenguaje, Ciencias Naturales y Ciencias Sociales**. Población objetivo: grados **6° a 11°**.",
        "Nota sobre el área: la plantilla sugiere las Orientaciones para Tecnología e Informática. No aplican aquí porque el producto no enseña tecnología: diagnostica aprendizajes de las cuatro áreas anteriores. Se usa, como la plantilla permite, *«el referente curricular que corresponda al área y grado de su población»*.",
    ]),
    ("Referente utilizado:", [
        "**Derechos Básicos de Aprendizaje (DBA)** — versión 2 para Matemáticas, Lenguaje y Ciencias Sociales; versión 1 para Ciencias Naturales. Complementados por los Estándares Básicos de Competencias y los Lineamientos Curriculares de cada área.",
    ]),
    ("Aprendizajes del referente", [
        "El producto **no define aprendizajes propios**: opera solo sobre las evidencias de aprendizaje que el MEN ya formuló para cada DBA. Es una decisión declarada del proyecto: el sistema no se atribuye autoridad curricular que no tiene. La estructura del referente baja directamente al modelo de datos: un DBA tiene evidencias, una experiencia se ancla a un único DBA, y el resultado se emite por evidencia, nunca como puntaje global.",
        "**Una lectura del referente que condiciona el diseño.** Los DBA no son una secuencia rígida por grado. El documento oficial lo dice:",
        ("cita", "«Los DBA también constituyen un conjunto de conocimientos y habilidades que se pueden movilizar de un grado a otro […] Si bien los DBA se formulan para cada grado, el maestro puede trasladarlos de uno a otro en función de las especificidades de los procesos de aprendizaje de los estudiantes. De esta manera, los DBA son una estrategia para promover la flexibilidad curricular.» — MEN, DBA Matemáticas V.2, sección 3."),
        "Por eso el sistema permite anclar una experiencia a un DBA de **cualquier grado entre 1° y 11°**, aunque los usuarios sean de secundaria: un docente de 8° que detecta un vacío correspondiente a un DBA de 5° debe poder diagnosticarlo. Restringir el selector al grado del grupo contradiría al propio referente.",
    ]),
])

# ------------------------------------------------------------------ 3
rellenar_caja(caja(38, "Usuario 1"), [
    ("Usuario 1", [
        "**Docente.** Docente de secundaria oficial de una de las cuatro áreas con DBA. **Banda de edad: adulto.**",
        "*Necesidad:* saber, por evidencia de aprendizaje y por estudiante, qué alcanza y qué no su grupo, sin construir el instrumento desde cero.",
        "*Acciones:* crea una experiencia y la ancla a un DBA; revisa y edita el banco de ítems que genera el sistema; publica; comparte el código de invitación; consulta el reporte por evidencia y la vista de su grupo.",
    ]),
    ("Usuario 2", [
        "**Estudiante.** Estudiante de secundaria, grados 6° a 11°. **Banda de edad: 11 a 17 años — menores de edad.** Este dato condiciona las decisiones de privacidad (sección 7) y de interfaz (E2).",
        "*Necesidad:* responder un diagnóstico breve sin que el sistema le devuelva un veredicto sobre sí mismo.",
        "*Acciones:* se une con un código; responde los ítems uno a uno; declara en cada respuesta qué tan seguro está.",
    ]),
    ("Usuario 3", [
        "**Acudiente o representante legal.** **Banda de edad: adulto.**",
        "*Necesidad:* autorizar el tratamiento de los datos de su representado, como exige la Ley 1581 de 2012.",
        "*Acciones:* **ninguna en esta versión.** El rol se identifica pero **no está modelado en el sistema**. Consecuencia: la versión actual no puede desplegarse con estudiantes reales sin un mecanismo externo que recoja esa autorización (ver sección 7 y sección 15).",
    ]),
])

# ------------------------------------------------------------------ 4
rellenar_caja(caja(44, "Modelo o enfoque"), [
    ("Modelo o enfoque pedagógico", [
        "**Evaluación formativa criterio-referenciada, con medición de certeza.** Criterio-referenciada significa que el desempeño se compara contra un criterio externo —la evidencia de aprendizaje del DBA— y no contra los demás estudiantes: no hay ranking, percentil ni nota.",
        "Se deriva directamente de la necesidad de la sección 1: si el problema es que la medición disponible no opera a nivel de evidencia, el enfoque tiene que ser uno cuyo criterio *sea* la evidencia. Un enfoque normativo reproduciría, a menor escala, el problema que se quiere resolver.",
        "**El componente que lo distingue: la certeza.** Cada respuesta va acompañada del CRI (*Certainty of Response Index*, Hasan, Bagayoko y Kelley, 1999), una escala de 0 a 5 en la que el estudiante declara qué tan seguro estaba. Un acierto con certeza baja no es evidencia de que muestra el aprendizaje —pudo adivinar—, y un error con certeza baja tampoco es evidencia firme de lo contrario. Sin esta medida, un diagnóstico de opción cerrada confunde saber con acertar.",
    ]),
    ("Competencias u objetivos", [
        "Los del DBA al que se ancle cada experiencia, expresados en sus evidencias de aprendizaje oficiales. El producto no formula objetivos propios (sección 2).",
    ]),
    ("Criterios de logro", [
        "El sistema emite, por evidencia y por estudiante, uno de tres estados:",
        ("tbl", ["Estado", "Cuándo se emite"], [
            ["**Muestra**", "Mayoría de señales fuertes en esa dirección (acierto con certeza alta)"],
            ["**No muestra**", "Mayoría de señales fuertes en la dirección contraria (error con certeza alta)"],
            ["**No concluyente**", "Sin mayoría clara al llegar al tope de ítems"],
        ], [1, 3]),
        "Dos reglas limitan cuándo puede emitirse: **mínimo 4 ítems** respondidos siempre —ninguna conclusión con menos— y **tope de 6**: si al sexto no hay mayoría, el estado es *no concluyente* y se detiene para no fatigar al estudiante. El rango procede de la literatura de *mastery testing*: Shrock y Coscarelli recomiendan de 4 a 6 preguntas por objetivo.",
        "*No concluyente* es un resultado legítimo, no una falla: un sistema que siempre emite veredicto afirma más de lo que sus datos sostienen.",
    ]),
])

# ------------------------------------------------------------------ 5
rellenar_caja(caja(49, "F1"), [
    ("F1", ["**Autenticación y perfil.** Registro e ingreso por correo y contraseña o por proveedor externo (Google, Microsoft); verificación de correo; recuperación de contraseña; elección de rol —docente o estudiante—, irreversible."]),
    ("F2", ["**Creación de la experiencia (docente).** Elección de área, elección del DBA con sus evidencias y confirmación. Al confirmar, el sistema genera el banco de ítems."]),
    ("F3", [
        "**Revisión del banco (docente).** Consulta de los ítems generados, con su formato y opciones; edición del enunciado y del contenido; exclusión reversible de ítems.",
        "**F4 — Publicación e invitación (docente).** Paso de borrador a publicada; código de invitación de 6 caracteres.",
        "**F5 — Ingreso a la experiencia (estudiante).** Unirse con el código; ver sus experiencias y el estado de su propio avance (no iniciada, en curso, completada).",
        "**F6 — Toma del diagnóstico (estudiante).** Ítems presentados uno a uno en tres formatos —selección única, emparejar, ordenar—, con captura de la respuesta y de la certeza.",
        "**F7 — Reporte (docente).** Estado general por estudiante y estado por evidencia para todo el grupo, con categoría de brecha por umbral fijo.",
        "**F8 — Vista de aula (docente).** Listado del grupo agrupado por estado, con el detalle por estudiante.",
    ]),
])

# ------------------------------------------------------------------ 6
RF = [
    ("RF-01", "El sistema debe permitir que un docente cree una experiencia anclada a **exactamente un** DBA."),
    ("RF-02", "Al confirmarse la creación, el sistema debe generar un banco de **12 ítems por cada evidencia incluida** del DBA."),
    ("RF-03", "El docente debe poder excluir un ítem del banco de forma **reversible**, sin eliminarlo."),
    ("RF-04", "El sistema debe generar un código de invitación de **6 caracteres alfanuméricos**, único, sin `0`, `O`, `1`, `I` ni `L`."),
    ("RF-05", "El sistema debe impedir que un estudiante se una a una experiencia en estado *borrador*."),
    ("RF-06", "El sistema debe impedir que un mismo estudiante quede inscrito dos veces en la misma experiencia."),
    ("RF-07", "El sistema debe presentar los ítems **uno a uno** y registrar el orden y el momento de cada presentación."),
    ("RF-08", "El sistema debe exigir, en cada respuesta, un valor de certeza **entero entre 0 y 5**."),
    ("RF-09", "El sistema debe registrar **qué opción u opciones** eligió el estudiante, no solo si acertó."),
    ("RF-10", "El sistema debe presentar **como mínimo 4 ítems** por evidencia antes de emitir un estado."),
    ("RF-11", "El sistema debe detenerse al llegar a **6 ítems** por evidencia y emitir *no concluyente* si no hay mayoría clara."),
    ("RF-12", "El sistema debe distinguir un ítem presentado y no respondido de uno nunca presentado."),
    ("RF-13", "Por cada evidencia y estudiante, el sistema debe emitir exactamente uno de tres estados —*muestra*, *no muestra*, *no concluyente*— con su fecha de cálculo."),
    ("RF-14", "El sistema debe impedir modificar un ítem o sus opciones una vez que fue presentado a algún estudiante."),
    ("RF-15", "El sistema no debe mostrar al estudiante ningún resultado ni veredicto sobre su desempeño."),
    ("RF-16", "El sistema debe mostrar al docente el conteo de estudiantes en cada estado, por evidencia, en formato `X/total`."),
]
rellenar_caja(caja(54, "RF-01"), [
    ("RF-01", [RF[0][1]]),
    ("RF-02", [RF[1][1]]),
    ("RF-03", [RF[2][1]] + ["**%s —** %s" % r for r in RF[3:]]),
])

# ------------------------------------------------------------------ 7
rellenar_caja(caja(60, "Privacidad"), [
    ("Privacidad", [
        "El punto de partida es una prohibición legal: el **artículo 7 de la Ley Estatutaria 1581 de 2012** prohíbe el tratamiento de datos de niños, niñas y adolescentes salvo los de naturaleza pública, y exige que todo tratamiento responda al interés superior del menor. La vigilancia corresponde a la Superintendencia de Industria y Comercio.",
        ("tbl", ["ID", "Requerimiento"], [
            ["**RNF-01**", "Del estudiante se recogen **únicamente** nombre y correo. No se recoge documento, fecha de nacimiento, institución, curso ni fotografía obligatoria."],
            ["**RNF-02**", "El resultado de un estudiante **nunca** se expresa como puntaje, nota ni percentil; solo como uno de los tres estados."],
            ["**RNF-03**", "El resultado de un estudiante es visible **solo** para el docente de esa experiencia."],
            ["**RNF-04**", "El sistema debe registrar la autorización del representante legal antes de tratar datos de un menor."],
        ], [1, 6]),
        "**RNF-04 no está satisfecho en esta versión, y se declara.** El sistema no modela al acudiente ni tiene dónde registrar esa autorización. Consecuencia: **la versión 1 no puede desplegarse con estudiantes reales**, solo con datos de prueba o en demostración ante docentes.",
    ]),
    ("Accesibilidad", [
        "Referencia: **WCAG 2.2, nivel AA**.",
        ("tbl", ["ID", "Requerimiento"], [
            ["**RNF-05**", "Todo texto cumple una relación de contraste mínima de **4.5:1** con su fondo."],
            ["**RNF-06**", "Ninguna tarea exige arrastrar y soltar; emparejar y ordenar se resuelven con selectores."],
            ["**RNF-07**", "Ninguna tarea depende de audio o video para completarse."],
            ["**RNF-08**", "Ningún estado se comunica **solo** con color."],
        ], [1, 6]),
        "**RNF-05 tiene un incumplimiento conocido.** La auditoría del propio equipo detectó que el gris `#888888` en texto de 13 px negrita da **3.5:1**, bajo el mínimo, en dos pantallas ya diseñadas. No se cerró en falso: la corrección obvia —oscurecer el gris— choca con otro color del sistema y rompe la distinción entre categorías de resultado. Queda como defecto declarado.",
    ]),
    ("Sostenibilidad", [
        "**Social — la dimensión decisiva aquí.** Según el MinTIC, en 2025 el **51 % de las sedes rurales** tenía conexión a Internet (unas 18.000), frente al 12 % de 2022: el avance es real, pero cerca de la mitad seguía sin conexión. Los 156.546 computadores entregados en más de 8.000 instituciones implican **equipo compartido**, no uno por estudiante.",
        ("tbl", ["ID", "Requerimiento"], [
            ["**RNF-09**", "Funciona en computador de escritorio de gama baja, sin exigir dispositivo personal por estudiante."],
            ["**RNF-10**", "El diagnóstico se completa en **una sesión de clase**, sin trabajo en casa."],
        ], [1, 6]),
        "**Técnica.** El banco se genera una sola vez, al crear la experiencia; la llamada costosa al modelo de lenguaje ocurre una vez por experiencia, no una vez por estudiante.",
        "**Económica.** Sin costo por estudiante ni licencia por institución. Se descartó el ingreso con Apple por exigir una cuenta de desarrollador de pago (99 USD/año) sin beneficio para una plataforma web.",
        "**Ambiental.** Consecuencia de la técnica: generar el banco una vez por experiencia reduce el cómputo asociado a los modelos de lenguaje, que concentra la huella del producto.",
    ]),
    ("Uso de inteligencia artificial", [
        ("tbl", ["ID", "Requerimiento"], [
            ["**RNF-11**", "Todo contenido generado por IA es **revisable y editable** por el docente antes de que un estudiante lo vea."],
            ["**RNF-12**", "El sistema registra si un ítem está **tal como lo generó la IA** o si el docente ya lo intervino."],
            ["**RNF-13**", "Ningún texto del reporte al docente lo redacta la IA: los estados se calculan, no se narran."],
            ["**RNF-14**", "La IA genera ítems **solo** a partir de la evidencia oficial del DBA, no de contenido libre."],
        ], [1, 6]),
        "RNF-13 existe porque un texto generado que interprete el desempeño de un menor introduciría un juicio sin responsable identificable. El sistema calcula; la interpretación es del docente.",
    ]),
    ("Otros", [
        "**RNF-15.** Interfaz íntegramente en español.",
        "**RNF-16.** La generación del banco no obliga al docente a esperar en la pantalla.",
    ]),
])

# ------------------------------------------------------------------ 8
rellenar_caja(caja(65, "Versión 1:"), [
    ("Versión 1:", [
        "El diagnóstico completo, de punta a punta: autenticación y roles; creación de la experiencia anclada a un DBA; generación y revisión del banco; publicación e invitación; toma del diagnóstico con captura de certeza; cálculo del estado por evidencia; reporte al docente.",
        "Es la mínima que ya entrega valor educativo porque cierra el ciclo: sin la toma del diagnóstico no hay dato, y sin el reporte el dato no llega a quien decide.",
    ]),
    ("Versión 2:", [
        "Práctica focalizada sobre las evidencias en *no muestra* y verificación posterior. Su diseño pedagógico existe, pero queda fuera de la v1 a propósito: construir la práctica sobre un diagnóstico aún no validado arriesga trabajo desperdiciado.",
        "También en v2: registro de la autorización del acudiente (RNF-04), que es lo que habilita el despliegue con estudiantes reales.",
    ]),
    ("Versiones posteriores:", [
        "Acceso móvil del estudiante · unidades con varias experiencias conectadas · biblioteca curada por uso real · versionado del contenido de los ítems.",
    ]),
])

# ------------------------------------------------------------------ 9
rellenar_caja(caja(70, "No se hará:"), [
    ("No se hará:", [
        ("tbl", ["No se hará", "Motivo"], [
            ["Asignar nota, puntaje o calificación", "Contradice el enfoque criterio-referenciado. El producto informa; calificar es decisión del docente y de su institución"],
            ["Nombrar la causa del error del estudiante", "Los distractores se construyen con hipótesis de error, pero no se reportan como diagnóstico de causa: exigiría una validación empírica que el proyecto no tiene"],
            ["Mostrar al estudiante su propio resultado", "El producto informa una decisión docente; no devuelve a un menor un juicio sobre sí mismo"],
            ["Preguntas abiertas", "Exigen calificación automática de texto libre, cuya fiabilidad no se puede sostener con el rigor del resto del producto"],
            ["Acceso móvil del estudiante en la v1", "Decisión de sostenibilidad: el escenario realista documentado es la sala de cómputo compartida"],
            ["Funcionar sin conexión", "Limitación real frente a la mitad de sedes rurales sin conexión. **No se resuelve y no se disimula**"],
            ["Que el docente decida cuántos ítems ve el estudiante", "Se evaluó y se revirtió: la cantidad la fija la regla 4-6, fundamentada en literatura. Dejarla al docente era asignarle una responsabilidad sin criterio que la respalde"],
        ], [2, 5]),
    ]),
    ("Motivo:", [
        "Delimitar es una decisión de diseño. Las dos últimas filas registran decisiones que el equipo tomó y **luego revocó**, con su razón: el alcance no se fijó de una vez, se corrigió.",
    ]),
])

# ----------------------------------------------------------------- 10
rellenar_caja(caja(75, "Métrica de aprendizaje:"), [
    ("Métrica de aprendizaje:", [
        "**M1 — Cambio de estado entre dos aplicaciones.** De las evidencias que quedaron en *no muestra* y sobre las que el docente declara haber intervenido, qué proporción pasa a *muestra* en una segunda aplicación. *Meta de referencia:* al menos 40 %.",
        "**Límite honesto:** M1 requiere una segunda aplicación, que es funcionalidad de la v2. En la v1 **no es medible**; se declara en vez de disfrazar una métrica de uso como métrica de aprendizaje.",
        "**M2 — Concordancia con el juicio docente.** Proporción de casos en que el estado emitido coincide con lo que el docente, de forma independiente y antes de ver el reporte, esperaba de ese estudiante en esa evidencia. *Meta:* más de 70 %, con cada discordancia revisada. Sí es medible en la v1 y mide si el instrumento discrimina. Una concordancia del 100 % sería sospechosa: significaría que el sistema no aporta nada que el docente no supiera.",
    ]),
    ("Métrica de uso:", [
        "**M3 — Finalización.** Proporción de inscritos que completan el diagnóstico en una sesión de clase. *Meta:* más de 85 %.",
        "**M4 — Intervención docente sobre el banco.** Proporción de ítems editados o excluidos antes de publicar. Sin meta numérica, pero un 0 % indicaría que el docente no está revisando, y esa revisión es una garantía central del producto.",
    ]),
    ("Métrica de calidad:", [
        "**M5 — Tasa de no concluyente.** Proporción de pares estudiante-evidencia que terminan sin conclusión tras 6 ítems. *Meta:* menos de 25 %; una tasa mayor indicaría ítems que no discriminan.",
    ]),
])

# ----------------------------------------------------------------- 11
rellenar_caja(caja(80, "Criterios de comparación:"), [
    ("Criterios de comparación:", [
        "**Declaración previa.** El proyecto ya trabajaba con MODESEC cuando se hizo esta comparación: no es una evaluación previa a la elección, es su justificación, y se presenta como tal.",
        ("tbl", ["Criterio", "Por qué importa en este proyecto"], [
            ["**C1** ¿Trata el diseño pedagógico como fase propia?", "Un producto educativo con el modelo pedagógico improvisado es un producto cualquiera con contenido escolar"],
            ["**C2** ¿Produce artefactos verificables por fase?", "El equipo necesitaba comprobar que un documento no contradice a otro"],
            ["**C3** ¿Tolera requisitos cambiantes?", "El modelo de datos cambió cinco veces en dos meses"],
            ["**C4** ¿Es practicable sin cliente disponible?", "Restricción real del equipo, documentada en E0 (Modo B)"],
            ["**C5** ¿Encaja con la evaluación por entregables del curso?", "Restricción institucional"],
        ], [2, 3]),
    ]),
    ("Modelo A / B / C", [
        ("tbl", ["", "A · MODESEC", "B · ADDIE", "C · Scrum"], [
            ["**C1**", "**Sí.** La Fase I entera es diseño educativo, antes de la interfaz", "**Sí.** Análisis y diseño son instruccionales por definición", "**No.** Marco de gestión; lo pedagógico le es ajeno"],
            ["**C2**", "**Sí.** Entregables nombrados por fase (MER, MR, diccionario, ventanas)", "Parcial: define fases, no artefactos", "Parcial: incrementos y ceremonias, no documentos"],
            ["**C3**", "Media: fases secuenciales, rehacer una arrastra las siguientes", "Baja en su forma clásica", "**Alta**: es su razón de ser"],
            ["**C4**", "**Alta**: se apoya en referentes documentados", "Alta", "**Baja**: depende de un Product Owner que priorice"],
            ["**C5**", "**Alto**: es la metodología del programa", "Medio", "Medio"],
        ], [1, 3, 3, 3]),
    ]),
    ("Metodología elegida", [
        "**MODESEC**, por C1, C2 y C4: es la única de las tres que trata el diseño educativo como fase con entregables propios, y la que mejor funciona sin un cliente disponible, que es la situación documentada en E0.",
        "**Consecuencias, incluidas las malas:**",
        ("ul", [
            "**C3 es su punto débil, y se pagó.** El modelo entidad-relación tuvo cinco revisiones; en una se descubrió que el modelo relacional había quedado dos revisiones atrás sin que nadie lo notara, porque la secuencialidad no obliga a revisar aguas abajo.",
            "**Se compensó con herramientas propias:** verificadores automáticos que comparan cada documento contra su fuente. Eso no viene de MODESEC; hubo que agregarlo.",
            "**Se adoptó un elemento ajeno:** límite de trabajo en curso, de Kanban. El desorden de una etapa anterior no vino de falta de documentos, sino de tener demasiados abiertos sin cerrar ninguno.",
        ]),
    ]),
])

# ----------------------------------------------------------------- 12
reemplazar_caja(caja(85, "[Escriba"), [
    "La bitácora completa está diligenciada en el formato del final de esta plantilla (apartado *Bitácora de uso de inteligencia artificial*). Registra siete usos, con sus validaciones y **seis descartes o correcciones**, entre ellos dos errores que la propia IA introdujo y que el equipo detectó.",
    "Además, cada decisión de arquitectura del proyecto quedó registrada con su alternativa descartada en `diseno/decisiones.md` del repositorio (25 registros).",
])

# ----------------------------------------------------------------- 13
rellenar_caja(caja(90, "Por qué el problema"), [
    ("Por qué el problema", [
        "Los instrumentos existentes resuelven problemas distintos: Saber mide el sistema; Evaluar para Avanzar ofrece evaluación formativa con instrumentos que el ICFES diseña de antemano; las plataformas de contenido ejercitan; los cuestionarios propios del docente cuestan tiempo de preparación. Ninguno permite al docente elegir el DBA y observar, en su grupo y durante el año, cada una de sus evidencias de aprendizaje.",
    ]),
    ("Qué oportunidad", [
        "Que el MEN haya formulado las evidencias de aprendizaje de forma explícita y pública significa que **el criterio ya está escrito**: no hay que inventar qué observar, solo construir con qué observarlo. Esa condición poco común es la que hace viable un producto que no se atribuye autoridad curricular propia.",
    ]),
])

# ----------------------------------------------------------------- 14
rellenar_caja(caja(95, "Producto 1"), [
    ("Producto 1", [
        "**Evaluar para Avanzar 3° a 11° (ICFES — MEN).** Gratuito, voluntario, formativo.",
        "*Qué aprovechar:* que le explica al docente qué evalúa cada pregunta y por qué cada opción es correcta o no; la transparencia sobre el instrumento es exactamente lo que el docente de AdaptiveLearn necesita al revisar su banco.",
        "*Qué evitar:* que el instrumento llegue cerrado. Aquí el docente elige el DBA y revisa cada ítem antes de publicar.",
    ]),
    ("Producto 2", [
        "**Plataformas de cuestionarios en el aula (tipo Kahoot o Quizizz).**",
        "*Qué aprovechar:* la fricción mínima para entrar —un código y listo—, que AdaptiveLearn replica con su código de invitación de 6 caracteres.",
        "*Qué evitar:* el puntaje, el ranking y la presión de tiempo. Premian responder rápido y comparan estudiantes entre sí; ambas cosas contradicen un diagnóstico criterio-referenciado que además pide certeza.",
    ]),
])

# ----------------------------------------------------------------- 15
rellenar_caja(caja(100, "Supuestos:"), [
    ("Supuestos:", [
        ("tbl", ["#", "Supuesto", "Estado"], [
            ["A1", "El docente tiene voluntad y tiempo para revisar el banco antes de publicar", "Sin verificar. Si no revisa, la garantía de RNF-11 se vuelve nominal"],
            ["A2", "El estudiante declara su certeza con honestidad", "Sin verificar. Todo el mecanismo depende de esto"],
            ["A3", "El sistema dispone de los DBA normalizados de las cuatro áreas", "Parcial: la normalización tiene un defecto de extracción conocido y sin corregir"],
        ], [1, 5, 5]),
    ]),
    ("Restricciones:", [
        ("tbl", ["#", "Restricción", "Origen"], [
            ["R1", "No se tratan datos de menores sin autorización del representante legal", "Ley 1581 de 2012, art. 7 — restricción legal"],
            ["R2", "Cerca de la mitad de las sedes rurales sin conexión en 2025", "MinTIC"],
            ["R3", "Equipos compartidos, no individuales", "MinTIC"],
            ["R4", "El equipo no tuvo acceso a un docente de aula", "E0, Modo B"],
            ["R5", "La regla exacta que convierte respuestas en estado no está definida", "Vacío propio, previo a cualquier implementación"],
        ], [1, 5, 4]),
    ]),
])

# ----------------------------------------------------------------- 16
rellenar_caja(caja(105, "Término"), [
    ("Término", [
        ("tbl", ["Término", "Definición"], [
            ["**DBA**", "Derecho Básico de Aprendizaje: aprendizaje estructurante que el MEN formula por grado y área"],
            ["**Evidencia de aprendizaje**", "Componente de un DBA que describe algo observable en el estudiante. Es la unidad sobre la que opera el producto"],
            ["**Experiencia**", "En este producto: un diagnóstico creado por un docente, anclado a un único DBA"],
            ["**CRI**", "*Certainty of Response Index*: escala de 0 a 5 en la que el estudiante declara su certeza (Hasan et al., 1999)"],
            ["**Señal fuerte / débil**", "Fuerte: respuesta con certeza alta. Débil: certeza baja; no concluye en ninguna dirección"],
            ["**No concluyente**", "Estado legítimo cuando 6 ítems no alcanzan mayoría clara"],
            ["**Criterio-referenciada**", "Evaluación que compara contra un criterio externo, no contra el grupo"],
        ], [2, 5]),
    ]),
])

# ---------------------------------------------------- bitacora (final)
assert "".join(b[114].itertext()).startswith("Fecha")
rellenar_grilla(b[114], [
    ["2026-09-25", "Claude (Anthropic)", "Interpretar las plantillas E0 y E1", "Lectura de ambas y mapa de qué material del proyecto alimenta cada sección", "Se contrastó contra el texto de las plantillas, no contra el resumen", "—"],
    ["2026-09-25", "Claude (Anthropic)", "Redactar la entrevista E0 inventando un docente informante", "La herramienta se negó", "—", "**Descartado:** habría sido testimonio de una persona inexistente. Se aplicó el Modo B que prevé el instrumento"],
    ["2026-09-25", "Claude (Anthropic)", "Buscar evidencia del contexto educativo colombiano", "Saber 11 2025, brechas, conectividad MinTIC, Ley 1581 art. 7", "Cifras contrastadas entre ICFES, LEE Javeriana y prensa", "Se descartó el promedio de 261: es solo calendario A, no el global"],
    ["2026-09-25", "Claude (Anthropic)", "Verificar que los DBA son trasladables entre grados", "Cita textual del documento oficial", "Se buscó el texto literal en la fuente", "Se descartó *«no son camisa de fuerza»*: está en los Lineamientos, no en los DBA"],
    ["2026-09-25", "Claude (Anthropic)", "Revisar la necesidad de la sección 1", "Se detectó que omitía Evaluar para Avanzar (ICFES)", "Se verificó que la estrategia existe y qué cubre", "Se descartó la afirmación de que Saber era el único instrumento masivo"],
    ["2026-09-25", "Claude (Anthropic)", "Redactar la métrica de aprendizaje", "Métrica de cambio de estado entre aplicaciones", "Se detectó que no es medible en la v1 y se declaró", "Se descartó presentar la tasa de finalización como métrica de aprendizaje"],
    ["2026-08 a 09", "Claude (Anthropic)", "Diseño del modelo de datos y de las 22 ventanas", "MER, modelo relacional, diccionario y especificaciones", "Cada decisión quedó registrada con su alternativa descartada (25 registros en `diseno/decisiones.md`)", "Se descartaron las taxonomías SOLO y Bloom por no corresponder a la estructura real de las evidencias del MEN"],
])

# ----------------------------------------------------- autoverificacion
OK, PEND = "✔ Sí", None
rellenar_clave_valor(b[117], {
    "Las doce secciones": "✔ Sí",
    "La necesidad educativa": "✔ Sí",
    "Cada usuario": "✔ Sí",
    "La propuesta pedagógica": "✔ Sí",
    "Los requerimientos no funcionales": "✔ Sí",
    "La sostenibilidad": "✔ Sí",
    "La sección de fuera de alcance": "✔ Sí",
    "Hay al menos una métrica": "✔ Sí",
    "La comparación de modelos": "✔ Sí",
    "La bitácora de IA": "✔ Sí",
    "El repositorio registra": ("pend", "Pendiente"),
    "El video de sustentación": ("pend", "Pendiente"),
})

guardar(z, root, DESTINO)
print("generado:", os.path.normpath(DESTINO))
