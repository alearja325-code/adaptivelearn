"""Matriz CRUD: que caso de uso crea, lee, modifica o borra cada entidad.

Es el lado dinamico del MER: el diagrama dice que existe y como se
relaciona; esta matriz dice quien lo crea, quien lo cambia y quien lo
borra. Va en `16-modelo-entidad-relacion.md`, seccion «Como interactua».

Solo se escriben aqui los borrados DIRECTOS. Lo que se borra en cascada no
se escribe a mano: se calcula de las llaves foraneas ON DELETE CASCADE del
modelo relacional, asi que no puede contradecirlo.

`_verificar_uml.py` (bloque F) comprueba:
  * toda entidad que se guarda tiene quien la cree (o es dato del catalogo);
  * todo caso de uso toca al menos una entidad (o dice por que no);
  * Presentacion, Respuesta, Respuesta_Opcion y Resultado nunca se
    modifican: son hechos y fotografias (RNF-10, RNF-11, ADR-021);
  * solo se borra lo que un flujo borra (experiencia, inscripcion, opcion).
"""

C, R, U, D = "C", "R", "U", "D"

CRUD = {
    "CU-01": {"CREDENCIAL": "CR"},
    "CU-02": {"CREDENCIAL": "CR", "DOCENTE": "R", "ESTUDIANTE": "R"},
    "CU-03": {"CREDENCIAL": "RU"},
    "CU-04": {"CREDENCIAL": "R"},
    "CU-05": {"DOCENTE": "C", "ESTUDIANTE": "C", "CREDENCIAL": "U"},
    "CU-06": {"CREDENCIAL": "RU", "DOCENTE": "R", "ESTUDIANTE": "R"},
    "CU-07": {"CREDENCIAL": "RU"},
    "CU-08": {},
    "CU-09": {"DOCENTE": "RU", "ESTUDIANTE": "RU", "CREDENCIAL": "R"},
    "CU-10": {"EXPERIENCIA": "R", "DBA": "R", "INSCRIPCION": "R"},
    "CU-11": {"EXPERIENCIA": "C", "EXPERIENCIA_EVIDENCIA": "C", "DBA": "R", "EVIDENCIA": "R",
              "EVIDENCIA_DICTAMEN": "R"},
    "CU-12": {"EXPERIENCIA": "R", "DBA": "R", "EVIDENCIA": "R", "INSCRIPCION": "R"},
    "CU-13": {"EXPERIENCIA": "RU", "EXPERIENCIA_EVIDENCIA": "R", "ITEM": "R"},
    "CU-14": {"EXPERIENCIA": "R"},
    "CU-15": {"EXPERIENCIA": "RD", "INSCRIPCION": "R", "RESPUESTA": "R"},
    "CU-16": {"ITEM": "C", "OPCION": "C", "DBA": "R", "EVIDENCIA": "R", "EVIDENCIA_DICTAMEN": "R"},
    "CU-17": {"EXPERIENCIA": "R", "EXPERIENCIA_EVIDENCIA": "R", "ITEM": "R", "OPCION": "R"},
    "CU-18": {"ITEM": "RU", "OPCION": "CRUD"},
    "CU-19": {"ITEM": "U"},
    "CU-20": {"ITEM": "C", "OPCION": "C", "EVIDENCIA_DICTAMEN": "R"},
    "CU-21": {"INSCRIPCION": "R", "EXPERIENCIA": "R", "DOCENTE": "R", "PRESENTACION": "R",
              "RESULTADO": "R"},
    "CU-22": {"EXPERIENCIA": "R", "INSCRIPCION": "CR"},
    "CU-23": {"INSCRIPCION": "R", "EXPERIENCIA_EVIDENCIA": "R", "ITEM": "R", "OPCION": "R",
              "PRESENTACION": "CR", "RESULTADO": "R"},
    "CU-24": {"PRESENTACION": "R", "ITEM": "R", "OPCION": "R", "RESPUESTA": "C",
              "RESPUESTA_OPCION": "C"},
    "CU-25": {"RESPUESTA": "R", "RESULTADO": "C"},
    "CU-26": {"INSCRIPCION": "D", "RESPUESTA": "R"},
    "CU-27": {"REPORTE": "R", "RESULTADO": "R", "INSCRIPCION": "R", "EXPERIENCIA_EVIDENCIA": "R"},
    "CU-28": {"REPORTE": "R", "ESTUDIANTE": "R", "INSCRIPCION": "R", "RESULTADO": "R"},
    "CU-29": {"PRESENTACION": "R", "RESPUESTA": "R", "RESPUESTA_OPCION": "R", "ITEM": "R",
              "OPCION": "R", "RESULTADO": "R"},
    "CU-30": {"REPORTE": "R", "RESULTADO": "R", "EXPERIENCIA_EVIDENCIA": "R"},
    "CU-31": {"DBA": "R", "EVIDENCIA": "R", "EVIDENCIA_DICTAMEN": "R"},
}

# Entidades que ningun caso de uso crea, y por que.
SIN_CREADOR = {
    "DBA": "dato del MEN: lo carga el equipo, fuera del sistema (`10`, §2.3)",
    "EVIDENCIA": "dato del MEN: lo carga el equipo, fuera del sistema",
    "EVIDENCIA_DICTAMEN": "juicio del equipo: lo carga con el censo QA-014, fuera del sistema",
    "REPORTE": "no se crea ni se guarda: se calcula al abrirlo (ADR-022)",
}
# Casos de uso que no tocan datos, y por que.
SIN_DATOS = {"CU-08": "cerrar sesión termina la sesión del navegador; no cambia nada guardado"}
# Hechos y fotografias: nunca se modifican.
INMUTABLES = {"PRESENTACION": "RNF-10", "RESPUESTA": "RNF-10", "RESPUESTA_OPCION": "RNF-10",
              "RESULTADO": "RNF-11 · ADR-021"}
# Lo unico que un flujo borra directamente.
BORRABLES = {"EXPERIENCIA": "CU-15", "INSCRIPCION": "CU-26",
             "OPCION": "CU-18 (quitar una opción mientras el ítem está en Borrador)"}


def en_cascada(tabla, fks):
    """Tablas que se borran en cascada al borrar una fila de `tabla`: se sigue
    cada llave foranea ON DELETE CASCADE que apunte a lo ya borrado."""
    borradas, pila = set(), [tabla]
    while pila:
        t = pila.pop()
        for origen, _, destino, _, on_delete, *_ in fks:
            if destino == t and on_delete == "CASCADE" and origen not in borradas | {tabla}:
                borradas.add(origen)
                pila.append(origen)
    return borradas
