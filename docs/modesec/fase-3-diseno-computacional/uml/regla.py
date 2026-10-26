"""La regla adaptativa de RF-04-07, escrita una sola vez.

La usan el verificador (para comprobar que el diagrama de objetos y las
pruebas de aceptacion de CU-25 digan lo que la regla dice) y sirve de
referencia para implementar ReglaAdaptativa.concluir() en el incremento I3.

RF-04-07: "Una senal fuerte es una respuesta con certeza de 3 a 5
(correcta: 'muestra'; incorrecta: 'no muestra'); con certeza 0 a 2 es
debil. Desde la 4.a respuesta, si mas de la mitad son senales fuertes de
'muestra', concluye Muestra; si mas de la mitad son de 'no muestra',
concluye No muestra; con 6 respuestas sin cumplirse, No concluyente."
"""
MINIMO, TOPE, CERTEZA_FUERTE = 4, 6, 3


def concluir(respuestas):
    """respuestas: [(certeza, correcta)] en orden. Devuelve el estado o None
    si todavia no se puede concluir."""
    n = len(respuestas)
    if n < MINIMO:
        return None
    fuertes_si = sum(1 for c, ok in respuestas if c >= CERTEZA_FUERTE and ok)
    fuertes_no = sum(1 for c, ok in respuestas if c >= CERTEZA_FUERTE and not ok)
    if fuertes_si * 2 > n:
        return "muestra"
    if fuertes_no * 2 > n:
        return "no_muestra"
    if n >= TOPE:
        return "no_concluyente"
    return None


def primera_conclusion(respuestas):
    """Aplica la regla tras cada respuesta, como el sistema: (n, estado) de
    la primera vez que concluye, o (len, None) si no concluyo."""
    for i in range(1, len(respuestas) + 1):
        e = concluir(respuestas[:i])
        if e:
            return i, e
    return len(respuestas), None
