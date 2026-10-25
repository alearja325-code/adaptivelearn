import os

DIR = os.path.dirname(__file__)


def read(name):
    return open(os.path.join(DIR, name), encoding="utf-8").read()


unificado = read("bt_unificado.svg")
leyenda = read("bt_leyenda.svg")
bloques = [read(f"bt_bloque{n}.svg") for n in range(1, 8)]

captions = [
    "Docente, Experiencia y DBA — quién crea, y a qué currículo se ancla.",
    "DBA y Evidencia — Evidencia es entidad débil, identificada por su DBA (PK compuesta, antes ausente).",
    "Estudiante, Inscripción y Experiencia — cómo un estudiante se une a una experiencia.",
    "Experiencia, Ítem, Evidencia y Opción — el banco de diagnóstico y su contenido.",
    "Ítem, Respuesta, Inscripción, Respuesta_Opción y Opción — qué respondió el estudiante, no solo si acertó.",
    "Inscripción, Resultado y Evidencia — el resumen por estudiante y evidencia (Resultado, entidad débil doble).",
    "Resultado, Reporte y Experiencia — Reporte es una vista derivada, no persiste.",
]

blocks_html = "".join(
    f'<div class="bloque">{svg}</div><p class="fig-num">Fig. {i+1} — {cap}</p>'
    for i, (svg, cap) in enumerate(zip(bloques, captions))
)

html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><title>Modelo Entidad-Relación — AdaptiveLearn</title>
<style>
  body {{ margin:0; padding:0 0 80px 0; background:#FFFFFF; font-family:Helvetica,Arial,sans-serif; color:#111111; }}
  .page {{ max-width:1300px; margin:0 auto; padding:48px 40px; }}
  h1 {{ font-size:26px; margin:0 0 6px 0; }}
  h2 {{ font-size:18px; margin:0 0 10px 0; }}
  p.sub {{ font-size:13.5px; color:#555555; margin:0 0 20px 0; max-width:760px; }}
  section {{ padding:44px 0; border-top:1px solid #E3E7ED; }}
  section:first-of-type {{ border-top:none; }}
  .bloque svg {{ display:block; max-width:100%; height:auto; }}
  p.fig-num {{ font-size:12.5px; color:#888888; margin:10px 4px 0 4px; max-width:900px; }}
  .unificado .bloque {{ width:100vw; margin-left:calc(50% - 50vw); padding:0 24px; box-sizing:border-box; }}
  .unificado .bloque svg {{ margin:0 auto; }}
  code {{ font-family:Consolas,Monaco,monospace; font-size:12.5px; background:#F3F5F8; padding:1px 5px; border-radius:3px; }}
</style></head><body>
<div class="page">

<section class="portada">
  <p class="sub" style="color:#3B7DD8;font-weight:700;text-transform:uppercase;letter-spacing:0.04em;">MODESEC — Fase III, Diseño Computacional</p>
  <h1>Modelo Entidad-Relación — AdaptiveLearn (rediseño)</h1>
  <p class="sub">Notación caja-tabla (Chen + extensiones): atributos como filas dentro de la caja, columna PK/FK a la izquierda, color por categoría de entidad. Texto completo, con cada decisión trazada a su fuente, en <code>01-modelo-entidad-relacion.md</code>.</p>
</section>

<section class="unificado">
  <h2>Modelo completo</h2>
  <p class="sub">Las 11 entidades más la vista derivada Reporte, con sus 16 relaciones. Solo trazado ortogonal (0°/90°) — sin diagonales de ángulo libre, verificado por código, no a ojo. 4 relaciones se rutean por el margen (arriba/abajo/derecha) para no cruzar cajas intermedias: Ítem–Evidencia, Inscripción–Resultado, Reporte–Resultado y Reporte–Experiencia.</p>
  <div class="bloque">{unificado}</div>
  <p class="fig-num">Fig. 0 — Modelo completo del MER de AdaptiveLearn.</p>
</section>

<section class="notacion">
  <h2>Notación empleada</h2>
  <div class="bloque" style="width:auto;">{leyenda}</div>
</section>

<section class="bloques">
  <h2>El modelo por bloques</h2>
  <p class="sub">La misma figura de arriba, recorrida en 7 partes — para leer cada grupo de entidades sin el ruido del resto.</p>
  {blocks_html}
</section>

<section class="cierre">
  <h2>Cierre</h2>
  <p class="sub">Texto completo del modelo — entidades, atributos, relaciones, restricciones de integridad (RI-1 a RI-11) y vacíos declarados (V-1 a V-4) — en <code>01-modelo-entidad-relacion.md</code>. El siguiente entregable de Fase III, según la fuente primaria de MODESEC, es el Modelo Relacional (MR) derivado de este MER, junto con el diccionario de datos.</p>
</section>

</div>
</body></html>"""

open(os.path.join(DIR, "bt_presentacion.html"), "w", encoding="utf-8").write(html)
print("listo")
