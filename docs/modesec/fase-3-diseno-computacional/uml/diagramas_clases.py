"""Diagramas de clases: el del dominio y el de los servicios.

El trazado del dominio sigue la topologia del mapa del MER
(`../mer/mapa_chen.py`): curriculo arriba, autoria y banco en la fila del
docente, inscripcion y respuestas en la fila del estudiante. Asi quien
ya leyo el MER encuentra cada cosa en el mismo lugar.

La columna de identidad pone a Usuario ENTRE sus dos subclases (Docente
arriba, Estudiante abajo): las dos generalizaciones quedan verticales y
cortas, y Credencial llega a cada subclase sin cruzar nada.
"""
from lienzo import Lienzo, NEGRO, GRIS, GRIS_CLARO
from cajas_uml import caja_clase, caja_enum, medir_clase, medir_enum
from datos_clases import (POR_NOMBRE, ASOCIACIONES, GENERALIZACIONES, ENUMERACIONES,
                          CLASE_ASOCIACION, DEPENDENCIAS)

# ------------------------------------------------------------ ubicacion
# nombre: (x, y, ancho forzado o None)
POS = {
    "Credencial": (40, 482, None),
    "Docente": (532, 384, 240), "Usuario": (440, 610, None), "Estudiante": (532, 900, 240),
    "DBA": (940, 90, 300), "Evidencia": (1400, 90, 220), "EvidenciaDictamen": (1700, 90, 250),
    "Experiencia": (940, 380, 320), "ExperienciaEvidencia": (1400, 380, 200),
    "Item": (1700, 380, 330), "Opcion": (2380, 380, 230),
    "Reporte": (1000, 708, 340),
    "Inscripcion": (940, 900, 320), "Resultado": (1400, 900, 390),
    "Presentacion": (1820, 900, None), "Respuesta": (2380, 900, 230),
    "RespuestaOpcion": (2660, 664, 190),
}
ANCHO, ALTO = 2900, 1500


def rutas(B):
    """Recorrido de cada asociacion, de A hacia B (en el orden de ASOCIACIONES)."""
    def c(n):
        return ((B[n][0] + B[n][2]) / 2, (B[n][1] + B[n][3]) / 2)
    yD, yE = 430, 946                     # filas del docente y del estudiante
    return {
        ("Credencial", "Docente"): [(300, B["Credencial"][1]), (300, yD), (B["Docente"][0], yD)],
        ("Credencial", "Estudiante"): [(300, B["Credencial"][3]), (300, yE), (B["Estudiante"][0], yE)],
        ("DBA", "Evidencia"): [(B["DBA"][2], 150), (B["Evidencia"][0], 150)],
        ("Evidencia", "EvidenciaDictamen"): [(B["Evidencia"][2], 150), (B["EvidenciaDictamen"][0], 150)],
        ("Docente", "Experiencia"): [(B["Docente"][2], yD), (B["Experiencia"][0], yD)],
        ("Experiencia", "DBA"): [(1090, B["Experiencia"][1]), (1090, B["DBA"][3])],
        ("Experiencia", "ExperienciaEvidencia"): [(B["Experiencia"][2], yD), (B["ExperienciaEvidencia"][0], yD)],
        ("Evidencia", "ExperienciaEvidencia"): [(1490, B["Evidencia"][3]), (1490, B["ExperienciaEvidencia"][1])],
        ("ExperienciaEvidencia", "Item"): [(B["ExperienciaEvidencia"][2], yD), (B["Item"][0], yD)],
        ("Item", "Opcion"): [(B["Item"][2], yD), (B["Opcion"][0], yD)],
        ("Estudiante", "Inscripcion"): [(B["Estudiante"][2], yE), (B["Inscripcion"][0], yE)],
        ("Inscripcion", "Experiencia"): [(965, B["Inscripcion"][1]), (965, B["Experiencia"][3])],
        ("Inscripcion", "Presentacion"): [(1100, B["Inscripcion"][3]), (1100, 1132), (1960, 1132),
                                          (1960, B["Presentacion"][3])],
        ("Item", "Presentacion"): [(1900, B["Item"][3]), (1900, B["Presentacion"][1])],
        ("Presentacion", "Respuesta"): [(B["Presentacion"][2], yE), (B["Respuesta"][0], yE)],
        ("Respuesta", "Opcion"): [(2495, B["Respuesta"][1]), (2495, B["Opcion"][3])],
        ("Inscripcion", "Resultado"): [(B["Inscripcion"][2], yE), (B["Resultado"][0], yE)],
        ("ExperienciaEvidencia", "Resultado"): [(1540, B["ExperienciaEvidencia"][3]),
                                                (1540, B["Resultado"][1])],
        ("Resultado", "Reporte"): [(1440, B["Resultado"][1]), (1440, 760), (B["Reporte"][2], 760)],
        ("Reporte", "Experiencia"): [(1170, B["Reporte"][1]), (1170, B["Experiencia"][3])],
    }


def rotulos(L, ruta, mult_a, mult_b, nombre, rombo, dueno):
    """Multiplicidades junto a cada extremo y el nombre junto al tramo mas largo."""
    def extremo(p, q, texto, lejos):
        # p: el extremo; q: el punto siguiente hacia adentro de la linea
        dx, dy = q[0] - p[0], q[1] - p[1]
        if dy == 0:                              # tramo horizontal: arriba
            s = 1 if dx > 0 else -1
            L.texto(p[0] + s * lejos, p[1] - 7, texto, tam=12, peso=700,
                    anchor="start" if s > 0 else "end", dueno=dueno)
        else:                                    # tramo vertical: a la derecha
            s = 1 if dy > 0 else -1
            L.texto(p[0] + 7, p[1] + s * lejos + (9 if s > 0 else 0), texto, tam=12,
                    peso=700, dueno=dueno)
    extremo(ruta[0], ruta[1], mult_a, 30 if rombo else 8)
    extremo(ruta[-1], ruta[-2], mult_b, 14)
    tramos = list(zip(ruta, ruta[1:]))
    p, q = max(tramos, key=lambda t: abs(t[1][0] - t[0][0]) + abs(t[1][1] - t[0][1]))
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    if p[1] == q[1]:
        L.texto(mx, my + 17, nombre, tam=12, color=GRIS, anchor="middle", cursiva=True, dueno=dueno)
    else:
        L.texto(mx - 7, my + 4, nombre, tam=12, color=GRIS, anchor="end", cursiva=True, dueno=dueno)
    return (mx, my)


def dibujar_dominio():
    L = Lienzo(ANCHO, ALTO)
    L.texto(32, 40, "Diagrama de clases 1 · Dominio", tam=16, peso=700, color="#333333")
    L.texto(32, 62, "Atributos: los del modelo relacional, sin las columnas de llave foránea "
            "(esas son las asociaciones). Métodos: de los casos de uso que cada uno cita en 13-diagrama-clases.md.",
            tam=12, color=GRIS)
    B = {}
    for n, (x, y, w) in POS.items():
        B[n] = caja_clase(L, POR_NOMBRE[n], x, y, w)
    R = rutas(B)
    puntos_medios = {}
    for a, b, nombre, ma, mb, tipo in ASOCIACIONES:
        ruta = R[(a, b)]
        derivada = tipo == "derivada"
        L.linea(ruta, color=NEGRO, sw=1.3, dash="7,5" if derivada else None,
                inicio="rombo" if tipo == "composicion" else None,
                permitidos={a, b}, desc=f"{a}—{b}")
        puntos_medios[nombre] = rotulos(L, ruta, ma, mb, ("/" if derivada else "") + nombre,
                                        tipo == "composicion", dueno=None)
    for hijo, padre in GENERALIZACIONES:
        x = 652
        if B[hijo][1] < B[padre][1]:
            ruta = [(x, B[hijo][3]), (x, B[padre][1])]
        else:
            ruta = [(x, B[hijo][1]), (x, B[padre][3])]
        L.linea(ruta, color=NEGRO, sw=1.3, fin="herencia", permitidos={hijo, padre},
                desc=f"{hijo}▷{padre}")
    # clase asociacion: punteada del tramo de «selecciona» a su caja
    nombre_ca, rel = CLASE_ASOCIACION
    mx, my = 2495, 718
    L.linea([(mx, my), (B[nombre_ca][0], my)], color=NEGRO, sw=1.2, dash="4,4",
            permitidos={nombre_ca}, desc="clase asociación")
    # enumeraciones, en una fila
    x, y = 40, 1190
    L.texto(40, y - 16, "Enumeraciones — las 7 primeras son los ENUM del modelo relacional, valor por "
            "valor; las 3 últimas son de valores calculados, que no se guardan.", tam=12, color=GRIS)
    for nombre, valores, _ in ENUMERACIONES:
        w, h = medir_enum(nombre, valores)
        caja_enum(L, nombre, valores, x, y, w)
        x += w + 26
    L.texto(32, ALTO - 20,
            "Rombo negro: composición (la parte no existe sin el todo). Triángulo hueco: generalización. "
            "Punteado: asociación derivada (se calcula, no se guarda) o vínculo de la clase asociación. "
            "«calculada»: no persiste.", tam=11.5, color=GRIS_CLARO)
    return L


# ---------------------------------------------------------- servicios
POS_S = {
    "ServicioAcceso": (40, 110), "ServicioCorreo": (40, 420), "ProveedorIdentidad": (355, 420),
    "ServicioExperiencias": (610, 110), "Catalogo": (610, 340), "GeneradorBanco": (1160, 110),
    "ServicioGeneracion": (1160, 300), "ClienteGemini": (900, 480), "ClienteDeepSeek": (1400, 480),
    "ServicioBanco": (1160, 650), "ServicioDiagnostico": (40, 650), "ReglaAdaptativa": (120, 860),
    "ServicioReporte": (700, 860),
}


def dibujar_servicios():
    L = Lienzo(1880, 1080)
    L.texto(32, 40, "Diagrama de clases 2 · Servicios (control) e interfaces externas", tam=16,
            peso=700, color="#333333")
    L.texto(32, 62, "Reciben lo que el usuario hace en la IGU y coordinan a las clases del dominio "
            "(diagrama 1). Son los objetos que aparecen en los diagramas de secuencia.", tam=12, color=GRIS)
    B = {n: caja_clase(L, POR_NOMBRE[n], x, y) for n, (x, y) in POS_S.items()}

    def c(n):
        return ((B[n][0] + B[n][2]) / 2, (B[n][1] + B[n][3]) / 2)
    R = {
        ("ServicioAcceso", "ServicioCorreo"): [(150, B["ServicioAcceso"][3]), (150, B["ServicioCorreo"][1])],
        ("ServicioAcceso", "ProveedorIdentidad"): [(440, B["ServicioAcceso"][3]), (440, B["ProveedorIdentidad"][1])],
        ("ServicioExperiencias", "Catalogo"): [(750, B["ServicioExperiencias"][3]), (750, B["Catalogo"][1])],
        ("ServicioExperiencias", "GeneradorBanco"): [(B["ServicioExperiencias"][2], 160), (B["GeneradorBanco"][0], 160)],
        ("GeneradorBanco", "ServicioGeneracion"): [(1260, B["GeneradorBanco"][3]), (1260, B["ServicioGeneracion"][1])],
        ("ClienteGemini", "ServicioGeneracion"): [(1060, B["ClienteGemini"][1]), (1060, 345), (B["ServicioGeneracion"][0], 345)],
        ("ClienteDeepSeek", "ServicioGeneracion"): [(1500, B["ClienteDeepSeek"][1]), (1500, B["ServicioGeneracion"][3])],
        ("ServicioDiagnostico", "ReglaAdaptativa"): [(240, B["ServicioDiagnostico"][3]), (240, B["ReglaAdaptativa"][1])],
    }
    for cli, prov, tipo in DEPENDENCIAS:
        ruta = R[(cli, prov)]
        L.linea(ruta, color=NEGRO, sw=1.3, dash="7,5",
                fin="herencia" if tipo == "realiza" else "abierta",
                permitidos={cli, prov}, desc=f"{cli}→{prov}")
        p, q = max(zip(ruta, ruta[1:]), key=lambda t: abs(t[1][0] - t[0][0]) + abs(t[1][1] - t[0][1]))
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        if p[1] == q[1]:
            L.texto(mx, my - 8, f"«{tipo}»", tam=12, color=GRIS, anchor="middle")
        else:
            L.texto(mx + 8, my + 4, f"«{tipo}»", tam=12, color=GRIS)
    L.texto(32, 1060, "Flecha punteada abierta: «usa» (dependencia). Flecha punteada con triángulo "
            "hueco: «realiza» (implementa la interfaz). GeneradorBanco recibe el servicio principal y el "
            "de respaldo por configuración (RF-03-02).", tam=11.5, color=GRIS_CLARO)
    return L


def todos():
    return [("clases-1-dominio.svg", "Diagrama de clases 1 · Dominio", dibujar_dominio()),
            ("clases-2-servicios.svg", "Diagrama de clases 2 · Servicios", dibujar_servicios())]
