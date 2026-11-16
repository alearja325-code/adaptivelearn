# Censo de formato cerrado (QA-014)

Por cada una de las 1282 evidencias del catálogo: si se puede diagnosticar con una pregunta
cerrada y con qué formato (`single_choice`, `matching` u `ordering`). Lo necesita la creación
de experiencias (incremento I2): «el formato de los ítems lo determina la evidencia» (RF-03-01).

**Estado: propuesto por IA, sin validar** (ADR-042). Lo hizo la sesión de Claude del encargo 05
aplicando `docs/diseno/criterios-censo-formato-cerrado.md` a cada evidencia. Pasa a «validado por
muestreo» cuando dos integrantes del equipo revisen `muestra_validacion.md` (criterios §5).

| Archivo | Qué es | ¿Se edita a mano? |
|---|---|---|
| `dictamenes/MAT.txt`, `LEN.txt`, `CN.txt`, `CS.txt` | **El juicio**: una línea por evidencia, con el dictamen, la señal que decide y la justificación | Sí: es la fuente. Si un dictamen cambia, se cambia aquí |
| `generar_censo.py` | Lee los dictámenes, los cruza con el catálogo y escribe los tres archivos siguientes | — |
| `censo_formato_cerrado.json` | El censo completo; lo carga el backend en `evidencia_dictamen` | No: se regenera |
| `informe-censo.md` | Las cifras, en español simple, y las propuestas de ajuste a los criterios | No: se regenera |
| `muestra_validacion.md` | Las 40 al azar (semilla fija) y las dudosas, para los dos validadores | No: se regenera; se copia para marcarla |
| `_verificar_censo.py` | Comprueba el censo y que atrapa errores puestos a propósito | — |

```bash
python3 generar_censo.py && python3 _verificar_censo.py
```

Una línea de `dictamenes/`:

```
LEN-07-01 2 | SC | selecciona la información principal | «Selecciona la información principal … y la utiliza…»: … (single_choice).
CS-10-04 4 | N3 | argumenta | «Argumenta el papel desempeñado…»: «argumenta» no aplica (N3).
LEN-06-02 1 | N1 | utiliza los organizadores gráficos | … (N1). | dudoso: …
```

`SC`, `MT`, `OR`: aplica, con `single_choice`, `matching` u `ordering`. `N1` a `N5`: no aplica, por
esa regla de los criterios. Un quinto campo `dudoso:` explica por qué la evidencia no cabe
claramente en las reglas.

**Cuando el equipo valide:** cambiar `ESTADO` en `generar_censo.py` a `validado-por-muestreo`,
anotar quiénes y cuándo en la cabecera (`validacion`), regenerar y volver a cargar la base.
