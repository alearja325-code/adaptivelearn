#!/usr/bin/env python3
"""Fuente unica de la navegacion de AdaptiveLearn (MODESEC Fase II).

De aqui salen, sin escribir nada dos veces:
  - mapa-navegacion.dot / .svg / .png   (punto 4: mapa de navegacion)
  - ../29-guion-tecnico.md              (punto 5: tabla de ventanas)

Y se verifica, contra los specs reales:
  - que toda Ventana especificada (NNN en "# Ventana NNN") este en el mapa
  - que todo nodo del mapa apunte a un spec que exista
  - que ninguna flecha salga o llegue a un nodo inexistente
  - que toda pantalla (no modal generico) sea alcanzable desde Inicio

Uso: python3 mapa_navegacion.py
"""
import glob, os, re, subprocess, sys
from collections import deque

AQUI = os.path.dirname(os.path.abspath(__file__))
F2 = os.path.dirname(AQUI)

# ------------------------------------------------------------- ventanas
# id: (numero, nombre, usuario, spec, grupo)
V = {
    "014":  ("014", "Iniciar sesión / Crear cuenta", "Ambos", "17-spec-auth-login-registro.md", "auth"),
    "015":  ("015", "Verifica tu correo", "Ambos", "18-spec-auth-verifica-correo.md", "auth"),
    "016":  ("016", "Completa tu perfil", "Ambos", "19-spec-auth-completa-perfil.md", "auth"),
    "017":  ("017", "Elige tu rol", "Ambos", "20-spec-auth-elige-rol.md", "auth"),
    "018":  ("018", "Recupera tu contraseña", "Ambos", "21-spec-auth-recupera-contrasena.md", "auth"),
    "019":  ("019", "Nueva contraseña", "Ambos", "22-spec-auth-nueva-contrasena.md", "auth"),

    "001D": ("001", "Dashboard (docente)", "Docente", "04-spec-dashboard.md", "docente"),
    "002":  ("002", "Crear experiencia · Paso 1 (área)", "Docente", "05-spec-crear-experiencia-paso1.md", "docente"),
    "003":  ("003", "Crear experiencia · Paso 2 (DBA)", "Docente", "06-spec-crear-experiencia-paso2.md", "docente"),
    "004":  ("004", "Crear experiencia · Paso 3 (confirmar)", "Docente", "07-spec-crear-experiencia-paso3.md", "docente"),
    "006":  ("006", "Vista Interna (marco)", "Docente", "09-spec-vista-interna-marco.md", "docente"),
    "007":  ("007", "Pestaña Resumen", "Docente", "10-spec-vista-interna-resumen.md", "docente"),
    "008":  ("008", "Pestaña Materiales", "Docente", "11-spec-vista-interna-materiales.md", "docente"),
    "011":  ("011", "Pestaña Estudiantes", "Docente", "14-spec-vista-interna-estudiantes.md", "docente"),
    "009":  ("009", "Modal: Banco de preguntas", "Docente", "12-spec-modal-banco-items.md", "docente"),
    "010":  ("010", "Modal: Reporte", "Docente", "13-spec-modal-reporte.md", "docente"),
    "012":  ("012", "Modal: Confirmar publicación", "Docente", "15-spec-modal-confirmar-publicar.md", "docente"),
    "013":  ("013", "Modal: Código de invitación", "Docente", "16-spec-modal-codigo-invitacion.md", "docente"),
    "027":  ("027", "Modal: Historial del estudiante", "Docente", "27-spec-modal-historial-estudiante.md", "docente"),
    "025D": ("025", "Modal: Eliminar experiencia", "Docente", "25-spec-modal-confirmar-eliminar-salir.md", "docente"),

    "001E": ("001", "Dashboard (estudiante)", "Estudiante", "04-spec-dashboard.md", "estudiante"),
    "005":  ("005", "Modal: Unirse con código", "Estudiante", "08-spec-unirse-codigo.md", "estudiante"),
    "020":  ("020", "Diagnóstico · Inicio", "Estudiante", "23-spec-toma-diagnostico.md", "estudiante"),
    "021":  ("021", "Diagnóstico · Ítem", "Estudiante", "23-spec-toma-diagnostico.md", "estudiante"),
    "022":  ("022", "Diagnóstico · Certeza", "Estudiante", "23-spec-toma-diagnostico.md", "estudiante"),
    "023":  ("023", "Diagnóstico · Cierre", "Estudiante", "23-spec-toma-diagnostico.md", "estudiante"),
    "025E": ("025", "Modal: Salir de la experiencia", "Estudiante", "25-spec-modal-confirmar-eliminar-salir.md", "estudiante"),

    "024":  ("024", "Modal: Cargando", "Ambos", "24-spec-modal-cargando.md", "comun"),
    "026":  ("026", "Modal: Mi perfil", "Ambos", "26-spec-modal-mi-perfil.md", "comun"),
}

# Componentes genericos: se invocan desde muchas pantallas. Dibujar todas
# sus flechas haria el mapa ilegible; se documentan en la leyenda y en
# la columna "Pasa por" de la tabla.
GENERICOS = {"024"}

# --------------------------------------------------------------- flechas
# (desde, hacia, accion, estilo)  estilo: "" | "tab" | "vuelve"
E = [
    ("INICIO", "014", "abrir la plataforma", ""),
    # Auth
    ("014", "015", "Crear cuenta con correo", ""),
    ("014", "016", "Google/Microsoft, cuenta nueva", ""),
    ("014", "001D", "Iniciar sesión (docente)", ""),
    ("014", "001E", "Iniciar sesión (estudiante)", ""),
    ("014", "018", "¿Olvidaste tu contraseña?", ""),
    ("015", "016", "Código válido (registro)", ""),
    ("015", "019", "Código válido (recuperación)", ""),
    ("015", "014", "Volver (registro)", "vuelve"),
    ("015", "018", "Volver (recuperación)", "vuelve"),
    ("016", "017", "Continuar", ""),
    ("017", "016", "Volver", "vuelve"),
    ("017", "001D", "Soy Docente", ""),
    ("017", "001E", "Soy Estudiante", ""),
    ("018", "015", "Enviar código", ""),
    ("018", "014", "Volver a inicio de sesión", "vuelve"),
    ("019", "014", "Guardar", ""),
    # Docente
    ("001D", "002", "Crear experiencia", ""),
    ("002", "003", "Continuar", ""),
    ("003", "002", "Volver", "vuelve"),
    ("003", "004", "Continuar", ""),
    ("004", "003", "Volver", "vuelve"),
    ("004", "006", "Crear experiencia (pasa por 024)", ""),
    ("001D", "006", "Clic en una experiencia", ""),
    ("006", "007", "pestaña (por defecto)", "tab"),
    ("006", "008", "pestaña", "tab"),
    ("006", "011", "pestaña", "tab"),
    ("006", "001D", "←", "vuelve"),
    ("006", "025D", "… (Eliminar)", ""),
    ("025D", "001D", "Eliminar experiencia (pasa por 024)", ""),
    ("008", "009", "Ver banco de preguntas", ""),
    ("008", "010", "Ver reporte", ""),
    ("011", "012", "Publicar experiencia", ""),
    ("011", "013", "Código de invitación", ""),
    ("011", "027", "Ver historial completo", ""),
    ("001D", "026", "Bloque de perfil", ""),
    ("001D", "014", "Cerrar sesión", ""),
    # Estudiante
    ("001E", "005", "Unirse con código", ""),
    ("005", "020", "Código válido", ""),
    ("001E", "020", "Clic en una experiencia", ""),
    ("020", "001E", "←", "vuelve"),
    ("020", "025E", "… (Salir)", ""),
    ("025E", "001E", "Salir de la experiencia (pasa por 024)", ""),
    ("020", "021", "Comenzar / Continuar", ""),
    ("021", "022", "Siguiente", ""),
    ("022", "021", "Confirmar · el sistema sigue (pasa por 024)", ""),
    ("022", "023", "Confirmar · el sistema concluye (pasa por 024)", ""),
    ("023", "001E", "Volver al inicio", ""),
    ("001E", "026", "Bloque de perfil", ""),
    ("001E", "014", "Cerrar sesión", ""),
]

GRUPOS = {
    "auth":       ("AUTENTICACIÓN (ambos roles)", "#FAFAF8", "#555555"),
    "docente":    ("DOCENTE", "#F5F3EE", "#111111"),
    "estudiante": ("ESTUDIANTE", "#FFFFFF", "#111111"),
    "comun":      ("COMPONENTES COMUNES", "#FFFFFF", "#888888"),
}


def verificar():
    fallos = []
    # 1) ventanas especificadas en los specs reales
    especificadas = set()
    for f in glob.glob(os.path.join(F2, "[0-9][0-9]-spec*.md")):
        cab = open(f, encoding="utf-8").readline()
        m = re.match(r"# Ventana (\d{3})(?:-(\d{3}))?", cab)
        if not m:
            fallos.append(f"{os.path.basename(f)}: sin '# Ventana NNN' en la 1.a linea")
            continue
        a = int(m.group(1)); b = int(m.group(2) or a)
        especificadas |= {f"{n:03d}" for n in range(a, b + 1)}
    en_mapa = {v[0] for v in V.values()}
    for n in sorted(especificadas - en_mapa):
        fallos.append(f"Ventana {n} especificada pero ausente del mapa")
    for n in sorted(en_mapa - especificadas):
        fallos.append(f"Ventana {n} en el mapa pero sin spec")
    # 2) cada nodo apunta a un spec que existe
    for k, (n, _, _, spec, _) in V.items():
        if not os.path.exists(os.path.join(F2, spec)):
            fallos.append(f"{k}: spec inexistente {spec}")
    # 3) flechas con extremos validos
    for a, b, _, _ in E:
        for x in (a, b):
            if x != "INICIO" and x not in V:
                fallos.append(f"flecha {a}->{b}: nodo {x} no existe")
    # 4) alcanzabilidad desde INICIO
    ady = {}
    for a, b, _, _ in E:
        ady.setdefault(a, []).append(b)
    vistos, cola = {"INICIO"}, deque(["INICIO"])
    while cola:
        x = cola.popleft()
        for y in ady.get(x, []):
            if y not in vistos:
                vistos.add(y); cola.append(y)
    for k in V:
        if k not in vistos and k not in GENERICOS:
            fallos.append(f"{k} ({V[k][1]}) no es alcanzable desde Inicio")
    return especificadas, fallos


def dot():
    L = ['digraph Navegacion {',
         '  graph [rankdir=LR, bgcolor="#F7F6F3", fontname="Inter", pad="0.4",'
         ' nodesep=0.35, ranksep=0.7, splines=true, compound=true];',
         '  node [shape=box, style="rounded,filled", fontname="Inter", fontsize=11,'
         ' fillcolor="#FFFFFF", color="#BDBDBD", penwidth=1.2, margin="0.15,0.08"];',
         '  edge [fontname="Inter", fontsize=9, fontcolor="#555555", color="#888888",'
         ' penwidth=1.1, arrowsize=0.7];',
         '  INICIO [label="Inicio", shape=circle, fillcolor="#111111",'
         ' fontcolor="#FFFFFF", color="#111111", fontsize=10];']
    for g, (titulo, fondo, borde) in GRUPOS.items():
        L.append(f'  subgraph cluster_{g} {{')
        L.append(f'    label="{titulo}"; fontsize=12; fontcolor="{borde}";'
                 f' style="rounded,filled"; fillcolor="{fondo}"; color="{borde}"; penwidth=1.4;')
        for k, (n, nombre, _, _, grupo) in V.items():
            if grupo == g:
                extra = ', style="rounded,filled,dashed"' if k in GENERICOS else ""
                L.append(f'    "{k}" [label="{n}\\n{nombre}"{extra}];')
        L.append('  }')
    for a, b, accion, estilo in E:
        attrs = [f'label="{accion}"']
        if estilo == "tab":
            attrs += ['style=dashed', 'arrowhead=none']
        elif estilo == "vuelve":
            attrs += ['style=dotted', 'constraint=false']
        L.append(f'  "{a}" -> "{b}" [{", ".join(attrs)}];')
    L.append('}')
    return "\n".join(L) + "\n"


def guion(especificadas):
    entra, sale = {}, {}
    for a, b, accion, _ in E:
        sale.setdefault(a, []).append((b, accion))
        entra.setdefault(b, []).append((a, accion))

    def nom(k):
        return "Inicio" if k == "INICIO" else f"{V[k][0]} {V[k][1]}"

    filas = []
    for k, (n, nombre, usuario, spec, _) in sorted(V.items(), key=lambda kv: (kv[1][0], kv[0])):
        desde = "; ".join(f"{nom(a)} — *{acc}*" for a, acc in entra.get(k, [])) or "—"
        hacia = "; ".join(f"{nom(b)} — *{acc}*" for b, acc in sale.get(k, [])) or "vuelve a quien lo abrió"
        if k in GENERICOS:
            desde = "cualquier acción que espere al servidor (ver 2.2)"
            hacia = "se cierra solo al recibir la respuesta"
        filas.append(f"| **{n}** | {nombre} | {usuario} | `{spec}` | {desde} | {hacia} |")
    return filas


def main():
    especificadas, fallos = verificar()
    if fallos:
        print("FALLO — mapa de navegacion")
        for f in fallos:
            print("  " + f)
        sys.exit(1)
    ruta_dot = os.path.join(AQUI, "mapa-navegacion.dot")
    open(ruta_dot, "w", encoding="utf-8").write(dot())
    for fmt in ("svg", "png"):
        args = ["dot", f"-T{fmt}", ruta_dot, "-o", os.path.join(AQUI, f"mapa-navegacion.{fmt}")]
        if fmt == "png":
            args.insert(1, "-Gdpi=160")
        subprocess.run(args, check=True)
    filas = guion(especificadas)
    plantilla = os.path.join(AQUI, "_plantilla-guion-tecnico.md")
    texto = open(plantilla, encoding="utf-8").read()
    texto = texto.replace("{{TABLA_VENTANAS}}", "\n".join(
        ["| Ventana | Nombre | Usuario | Especificación | Se llega desde | Lleva a |",
         "|---|---|---|---|---|---|"] + filas))
    texto = texto.replace("{{N_VENTANAS}}", str(len(especificadas)))
    open(os.path.join(F2, "29-guion-tecnico.md"), "w", encoding="utf-8").write(texto)
    print(f"OK — {len(especificadas)} ventanas especificadas, todas en el mapa; "
          f"{len(E)} flechas, todas con extremos validos; todas las pantallas "
          f"alcanzables desde Inicio.")
    print("generado: navegacion/mapa-navegacion.{dot,svg,png} y 29-guion-tecnico.md")


if __name__ == "__main__":
    main()
