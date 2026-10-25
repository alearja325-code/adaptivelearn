import sys
sys.path.insert(0, ".")
from vista_general import build_tables_html

def read(path):
    return open(path, encoding="utf-8").read()

legend_svg = read("legend.svg")
bloque_svgs = {n: read(f"bloque{n}.svg") for n in range(1, 7)}

bloques = [
    (1, "Bloque 1 — Creación y anclaje curricular",
        [
            "Este bloque presenta tres entidades nuevas: Docente, Experiencia y DBA. Docente y Experiencia tienen cardinalidad 1 a N: un docente puede crear varias experiencias, pero cada experiencia pertenece a un único creador. Experiencia se ancla a exactamente un DBA (cardinalidad N a 1), el desempeño básico de aprendizaje oficial del Ministerio de Educación. El área y el grado no se modelan como atributos propios de Experiencia, sino como datos heredados del DBA anclado; por esa misma razón, DBA no tiene clave primaria propia en el modelo — es información externa, referenciada, no generada por el sistema. Ese mismo DBA es la entidad que conecta con el siguiente bloque, donde se muestran sus evidencias oficiales.",
        ],
        "Fig. 1 — Docente, Experiencia y DBA, con sus atributos completos."),
    (2, "Bloque 2 — Currículo oficial (MEN)",
        [
            "Retomamos DBA del bloque anterior y agregamos la entidad Evidencia, con cardinalidad 1 a N desde DBA. Ninguna de las dos entidades tiene clave primaria propia, porque ambas son currículo oficial del MEN, solo referenciado por el sistema. Evidencia se modela como entidad y no como atributo de DBA porque un atributo admite un único valor por registro, y un DBA tiene varias evidencias — además, Evidencia necesita identidad propia para poder relacionarse, más adelante, directamente con un Ítem.",
        ],
        "Fig. 2 — DBA y Evidencia; ninguna tiene id propio por ser dato externo del MEN."),
    (3, "Bloque 3 — Inscripción",
        [
            "Retomamos Experiencia y la relacionamos con dos entidades nuevas: Estudiante e Inscripción. Estudiante y Experiencia tienen una relación N a N —un estudiante se une a varias experiencias, una experiencia agrupa a varios estudiantes—; Inscripción es la entidad que resuelve esa relación N a N, con cardinalidad 1 a N desde cada una. Su único atributo propio es la fecha de unión: no duplica datos del estudiante ni de la experiencia, que ya existen en sus propias entidades. Esta misma Inscripción es la que, en el bloque de Respuesta y Resultado, se convierte en el punto de referencia de cada estudiante dentro de la experiencia.",
        ],
        "Fig. 3 — Estudiante, Inscripción y Experiencia."),
    (4, "Bloque 4 — Banco de diagnóstico",
        [
            "Retomamos Experiencia y Evidencia, que ahora convergen en una entidad nueva: Ítem. Experiencia genera su banco de Ítems con cardinalidad 1 a N, y cada Ítem evalúa exactamente una Evidencia (cardinalidad 1 a N desde Evidencia). Cada Ítem tiene además su propia entidad de alternativas de respuesta, Opción (cardinalidad 1 a N desde Ítem), con una estructura genérica pensada para los tres formatos de pregunta del sistema —selección única, emparejamiento y ordenamiento—, por lo que algunos de sus atributos solo aplican según el formato del ítem. Ítem es la entidad que el siguiente bloque retoma para registrar las respuestas de cada estudiante.",
        ],
        "Fig. 4 — Experiencia, Ítem, Opción y Evidencia."),
    (5, "Bloque 5 — Respuesta y resultado",
        [
            "Retomamos Ítem, Inscripción y Evidencia, y agregamos dos entidades nuevas: Respuesta y Resultado. Respuesta pertenece a exactamente una Inscripción y a exactamente un Ítem (cardinalidad 1 a N desde cada una), y registra si la respuesta fue correcta y con qué certeza. Resultado, en cambio, depende de la combinación de Inscripción y Evidencia, no de un solo evento: por eso se modela como entidad débil, sin clave primaria propia, identificada por esas dos entidades de las que depende. Su único atributo es un estado —muestra, no muestra, o no concluyente—, nunca una calificación. Resultado es la entidad que el siguiente bloque agrega para construir el Reporte.",
        ],
        "Fig. 5 — Ítem, Respuesta, Inscripción, Resultado y Evidencia."),
    (6, "Bloque 6 — Reporte",
        [
            "Cerramos con Experiencia, retomada por última vez, y con Reporte, que la resume. Reporte no se modela como una tabla con atributos propios: es una vista calculada sobre Resultado, generada cada vez que se consulta — por eso se representa con notación distinta (borde punteado, sin atributos), marcando que no es un dato almacenado. Su relación con Experiencia es 1 a 1, pero calculada, no persistida. Tiene dos vistas: una agrupa por evidencia y clasifica el grupo según el porcentaje en cada estado; la otra muestra el historial completo por estudiante. Con este bloque se cierra el modelo completo: de la Experiencia que crea un Docente hasta el Reporte que la resume, mostrado en seis partes para mantener cada una legible.",
        ],
        "Fig. 6 — Experiencia y Reporte."),
]

bloques_html = ""
for n, title, parrafos, fig_caption in bloques:
    parrafos_html = "".join(f"<p>{p}</p>" for p in parrafos)
    bloques_html += f"""
<section class="bloque-section">
  <h2>{title}</h2>
  <div class="explicacion">{parrafos_html}</div>
  <div class="bloque">{bloque_svgs[n]}</div>
  <p class="fig-num">{fig_caption}</p>
</section>
"""

html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8">
<title>Modelo Entidad-Relación — AdaptiveLearn</title>
<style>
  body {{ margin:0; padding:0 0 80px 0; background:#FFFFFF; font-family:Helvetica,Arial,sans-serif; color:#111111; }}
  .page {{ max-width:1300px; margin:0 auto; padding:48px 40px; }}
  h1 {{ font-size:26px; margin:0 0 6px 0; }}
  h2 {{ font-size:18px; margin:0 0 10px 0; }}
  p.sub {{ font-size:13.5px; color:#555555; margin:0 0 20px 0; max-width:760px; }}
  section {{ padding:44px 0; border-top:1px solid #E3E7ED; }}
  section:first-of-type {{ border-top:none; }}
  .bloque svg {{ display:block; max-width:100%; height:auto; }}
  .explicacion {{ max-width:900px; margin-bottom:24px; }}
  .explicacion p {{ font-size:14px; line-height:1.65; color:#111111; margin:0 0 12px 0; }}
  .explicacion p:last-child {{ margin-bottom:0; }}
  p.fig-num {{ font-size:12.5px; color:#888888; margin:10px 4px 0 4px; max-width:900px; }}
  /* portada */
  .portada h1 {{ font-size:30px; }}
  .portada p.kicker {{ font-size:13px; color:#3B7DD8; font-weight:700; text-transform:uppercase; letter-spacing:0.04em; margin:0 0 10px 0; }}
  .meta {{ margin-top:28px; border-top:1px solid #E3E7ED; padding-top:20px; display:grid; grid-template-columns:repeat(2,1fr); gap:10px 40px; max-width:640px; }}
  .meta div {{ font-size:13.5px; }}
  .meta b {{ display:block; font-size:11px; color:#888888; text-transform:uppercase; letter-spacing:0.03em; font-weight:600; margin-bottom:2px; }}
  /* alcance / cierre */
  .texto p {{ font-size:14px; line-height:1.6; max-width:800px; }}
  .texto ul {{ font-size:14px; line-height:1.6; max-width:800px; }}
  /* vista general */
  table {{ border-collapse: collapse; width:100%; max-width:900px; font-size:13px; margin-bottom:8px; }}
  th {{ text-align:left; font-size:11.5px; text-transform:uppercase; letter-spacing:0.03em;
        color:#555555; border-bottom:2px solid #111111; padding:8px 10px; }}
  td {{ padding:8px 10px; border-bottom:1px solid #E3E7ED; }}
  td.nombre {{ font-weight:700; }}
  td.rel {{ color:#3B7DD8; font-weight:600; }}
  td.card {{ font-weight:700; text-align:center; }}
  td.bloque {{ color:#555555; }}
  td.nota {{ color:#555555; }}
  .tag {{ border:1px solid #888888; border-radius:4px; padding:2px 8px; font-size:11.5px; }}
  .vg-sub {{ font-size:13.5px; color:#555555; margin:0 0 24px 0; max-width:760px; }}
</style></head><body>
<div class="page">

<section class="portada">
  <p class="kicker">MODESEC — Fase III, Diseño Computacional</p>
  <h1>Modelo Entidad-Relación — AdaptiveLearn (rediseño)</h1>
  <p class="sub">Notación Chen, construido bloque por bloque, con cada entidad, atributo y relación trazable a un ADR, una entrada del glosario o una spec de pantalla ya escrita.</p>
  <div class="meta">
    <div><b>Alcance</b>Diagnóstico → Reporte</div>
    <div><b>Notación</b>Chen</div>
    <div><b>Entidades</b>11</div>
    <div><b>Relaciones</b>13</div>
    <div><b>Modelo confirmado</b>2026-08-19</div>
    <div><b>Metodología</b>MODESEC, Fase III</div>
  </div>
</section>

<section class="texto">
  <h2>Alcance</h2>
  <p>Este modelo cubre el flujo Diagnóstico → Reporte: desde que un Docente crea una Experiencia anclada a un DBA oficial del MEN, hasta que el sistema calcula el Reporte final.</p>
  <p>Quedan fuera de este modelo, con justificación documentada:</p>
  <ul>
    <li>Unidad, Práctica y Verificación — diferidas (ADR-007), no se construyen todavía.</li>
    <li>La hipótesis de error como dato reportado — existe el distractor internamente, pero no se expone como "tipo de error".</li>
    <li>Bloom como campo activo — se adoptó (ADR-003) pero quedó sin función en el mecanismo real (ADR-008).</li>
    <li>Perfil de aprendizaje, mediaciones pedagógicas, acudientes, instituciones, Curso — pertenecen al sistema anterior, ya descartado.</li>
  </ul>
</section>

<section class="notacion">
  <h2>Notación empleada</h2>
  <p class="sub">Los símbolos usados en los 6 bloques, con su significado.</p>
  {legend_svg}
</section>

<section class="vista-general">
  <h2>Vista general del modelo</h2>
  <p class="vg-sub">Las 10 entidades del modelo y sus 12 relaciones, de un vistazo, antes de entrar al detalle bloque por bloque. Cada relación indica en qué bloque se desarrolla con sus atributos completos.</p>
  {build_tables_html()}
</section>

{bloques_html}

<section class="texto cierre">
  <h2>Cierre</h2>
  <p>Este documento cierra el Modelo Entidad-Relación. Por notación Chen, no muestra llaves foráneas — esas se definen en el Modelo Relacional (MR), el siguiente entregable de Fase III según la fuente primaria de MODESEC, junto con el diccionario de datos para los metadatos de cada campo (tipos, tamaños, restricciones).</p>
</section>

</div>
</body></html>"""

open("../03-presentacion-mer.html", "w", encoding="utf-8").write(html)
print("listo")
