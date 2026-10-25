import sys
sys.path.insert(0, ".")
from generador import AZUL_STROKE, REF_FILL, GRIS_MEDIO, NEGRO

entidades = [
    ("Docente", "propia", "id propio, la administramos nosotros"),
    ("Estudiante", "propia", "id propio, la administramos nosotros"),
    ("Experiencia", "propia", "id propio, la administramos nosotros"),
    ("Inscripción", "propia", "id propio, la administramos nosotros"),
    ("Ítem", "propia", "id propio, la administramos nosotros"),
    ("Opción", "propia", "id propio, la administramos nosotros"),
    ("Respuesta", "propia", "id propio, la administramos nosotros"),
    ("DBA", "men", "dato oficial del MEN, referenciado, sin id propio"),
    ("Evidencia", "men", "dato oficial del MEN, referenciado, sin id propio"),
    ("Resultado", "debil", "entidad débil: depende de Inscripción + Evidencia, sin id propio"),
    ("Reporte", "calculada", "vista calculada sobre Resultado, no persiste, sin atributos"),
]

relaciones = [
    ("Docente", "crea", "Experiencia", "1 a N", 1),
    ("Experiencia", "se ancla a", "DBA", "N a 1", 1),
    ("DBA", "tiene", "Evidencia", "1 a N", 2),
    ("Estudiante", "tiene", "Inscripción", "1 a N", 3),
    ("Experiencia", "tiene", "Inscripción", "1 a N", 3),
    ("Experiencia", "genera", "Ítem", "1 a N", 4),
    ("Evidencia", "se evalúa con", "Ítem", "1 a N", 4),
    ("Ítem", "tiene", "Opción", "1 a N", 4),
    ("Inscripción", "da", "Respuesta", "1 a N", 5),
    ("Ítem", "recibe", "Respuesta", "1 a N", 5),
    ("Inscripción", "tiene", "Resultado", "1 a N", 5),
    ("Evidencia", "mide", "Resultado", "1 a N", 5),
    ("Experiencia", "tiene", "Reporte", "1 a 1 (calculado)", 6),
]

tipo_color = {
    "propia": "#FFFFFF",
    "men": REF_FILL,
    "debil": "#FFFFFF",
    "calculada": "#FFFFFF",
}
tipo_label = {
    "propia": "Propia",
    "men": "Externa (MEN)",
    "debil": "Débil",
    "calculada": "Calculada",
}

rows_ent = ""
for nombre, tipo, nota in entidades:
    rows_ent += f"""<tr>
      <td class="nombre">{nombre}</td>
      <td><span class="tag" style="background:{tipo_color[tipo]}">{tipo_label[tipo]}</span></td>
      <td class="nota">{nota}</td>
    </tr>\n"""

rows_rel = ""
for a, rel, b, card, bloque in relaciones:
    rows_rel += f"""<tr>
      <td>{a}</td>
      <td class="rel">{rel}</td>
      <td>{b}</td>
      <td class="card">{card}</td>
      <td class="bloque">Bloque {bloque}</td>
    </tr>\n"""

def build_tables_html():
    """Las dos tablas solas (sin <html>/<body>/estilos) -- para incrustar
    dentro del documento final, que ya trae su propio CSS."""
    return f"""<h2>Entidades</h2>
<table>
  <tr><th>Entidad</th><th>Tipo</th><th>Qué representa ese tipo</th></tr>
  {rows_ent}
</table>

<h2>Relaciones y cardinalidades</h2>
<table>
  <tr><th>Entidad A</th><th>Relación</th><th>Entidad B</th><th>Cardinalidad</th><th>Se detalla en</th></tr>
  {rows_rel}
</table>"""

html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><title>Vista general</title>
<style>
  body {{ margin:0; padding:40px; background:#FFFFFF; font-family:Helvetica,Arial,sans-serif; color:{NEGRO}; }}
  h1 {{ font-size:20px; margin:0 0 4px 0; }}
  p.sub {{ font-size:13px; color:{GRIS_MEDIO}; margin:0 0 28px 0; max-width:720px; }}
  h2 {{ font-size:15px; margin:32px 0 10px 0; }}
  table {{ border-collapse: collapse; width:100%; max-width:900px; font-size:13px; }}
  th {{ text-align:left; font-size:11.5px; text-transform:uppercase; letter-spacing:0.03em;
        color:{GRIS_MEDIO}; border-bottom:2px solid #111111; padding:8px 10px; }}
  td {{ padding:8px 10px; border-bottom:1px solid #E3E7ED; }}
  td.nombre {{ font-weight:700; }}
  td.rel {{ color:{AZUL_STROKE}; font-weight:600; }}
  td.card {{ font-weight:700; text-align:center; }}
  td.bloque {{ color:{GRIS_MEDIO}; }}
  td.nota {{ color:{GRIS_MEDIO}; }}
  .tag {{ border:1px solid #888888; border-radius:4px; padding:2px 8px; font-size:11.5px; }}
</style></head><body>
<h1>Vista general del modelo</h1>
<p class="sub">Las 11 entidades del modelo y sus 13 relaciones, de un vistazo, antes de entrar al detalle bloque por bloque. Cada relación indica en qué bloque se desarrolla con sus atributos completos.</p>

{build_tables_html()}

</body></html>"""

open("vista-general.html", "w", encoding="utf-8").write(html)
print("listo")
