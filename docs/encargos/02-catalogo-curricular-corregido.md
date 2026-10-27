# Encargo 02 — Catálogo curricular corregido y verificado contra los PDF del MEN

**Para:** una sesión de Claude Code sobre este repositorio.
**Escrito:** 2026-10-26, desde la sesión local de Alejandro. **Antes de
empezar, lee `CLAUDE.md` y `docs/diseno/pendientes.md` (A12, A16).**

## 1. Qué hay que lograr

Un **archivo de datos del catálogo curricular**, con los DBA de las 4
áreas y sus evidencias, **verificado frase por frase contra los PDF
oficiales**, sin repetidos y con cada DBA en su grado correcto. Es el
prerrequisito para que el Paso 2 de "Crear experiencia" muestre los DBA
correctos (pendientes, A16).

## 2. El problema que corriges

`data/curriculo-men/normalized/curriculo_men_normalizado.json` (heredado
de la versión 2) tiene **342 DBA y solo 329 identificadores distintos**.
La extracción asignó al grado anterior el primer DBA de algunas páginas:
por ejemplo, hay dos `matemáticas_2_dba_1`, y el segundo es en realidad
el DBA 1 de **3°** (página 22 de `dba_matematicas_v2.pdf`, encabezado
"Matemáticas • Grado 3º"). Lo contrastado en local (pendientes, A12):

- **10 confirmados** contra el encabezado de la página: Matemáticas
  2°→3° (×2), 6°→7°, 9°→10°; Lenguaje 1°→2°, 6°→7°, 7°→8°; Ciencias
  Naturales 1°→2° (×2), 9°→10°.
- **3 pares sin determinar**: Ciencias Naturales 3°, 5° y 7°. Ese PDF
  tiene otro diseño de encabezado; resuélvelos leyendo las páginas.

Por esos errores, **los conteos por grado del JSON tampoco son
confiables**: puede que a algunos grados les falten DBA, o que los
números no sigan en orden.

## 3. Reglas que no se negocian

- **El contenido del MEN se copia exacto.** Enunciados y evidencias
  tal como están en el PDF; solo se normalizan espacios y saltos de
  línea. **Ni una palabra cambiada, agregada o quitada.**
- **No edites el JSON original.** Produce archivos nuevos (sección 4).
  El original queda como evidencia de lo que había.
- **La verdad es el PDF**, no el JSON ni el nombre del archivo
  (ADR-033). Áreas y versiones: Matemáticas V.2, Lenguaje V.2,
  Ciencias Naturales V.1, Ciencias Sociales V.1 (`data/curriculo-men/pdfs/`).
- **Cada cambio respecto al JSON queda en el informe con su prueba**:
  página del PDF y texto del encabezado.
- **Lo que no puedas determinar con certeza, márcalo como dudoso.** No
  lo adivines.

## 4. Qué producir

En `data/curriculo-men/catalogo/`:

| Archivo | Qué es |
|---|---|
| `construir_catalogo.py` | El script que arma el catálogo desde los PDF (y el JSON como punto de partida). Que se pueda volver a correr y dé lo mismo |
| `catalogo_dba.json` | El resultado: por cada DBA, `codigo_dba` (formato `ÁREA-GG-NN`, ADR-036), área, grado, número, enunciado, evidencias en orden, **documento y página del PDF** donde está, y el identificador viejo del JSON si existía |
| `_verificar_catalogo.py` | El verificador (sección 5) |
| `informe-correccion.md` | En español simple: qué estaba mal, qué se corrigió (tabla con DBA, grado viejo → nuevo, página y encabezado), qué quedó dudoso, y los conteos finales por área y grado |

**Fuera de alcance** (es la auditoría completa, A12, para después): el
**ejemplo** de cada DBA (QA-011) y la regla para los ejemplos con
imagen. Si al leer los PDF notas algo útil sobre eso, anótalo en el
informe, pero no lo resuelvas.

## 5. El verificador debe comprobar

1. Cada `codigo_dba` es único y cumple el formato `ÁREA-GG-NN` (RI-21).
2. Dentro de cada área y grado, los números van del 01 al N, sin huecos
   ni repetidos.
3. El enunciado de cada DBA y cada una de sus evidencias **aparecen
   literalmente** en la página del PDF que el registro dice (comparando
   con los espacios normalizados).
4. El grado de cada DBA coincide con el grado del encabezado de su
   página.
5. Cada evidencia pertenece a un solo DBA.

Demuestra que el verificador **sí atrapa errores**: introduce uno a
propósito (por ejemplo, cambia una palabra o un grado en una copia en
memoria), muestra que falla y quítalo.

## 6. Cuándo está terminado

- `_verificar_catalogo.py` pasa sin observaciones, o con observaciones
  explicadas una por una en el informe como "dudoso".
- El informe dice cuántos DBA hay por área y grado, **según el PDF**,
  sin forzar que sumen 342.
- Los verificadores de `CLAUDE.md` siguen pasando (este encargo no
  debería tocarlos).

## 7. Cómo entregarlo

Rama **`encargo-02-catalogo-corregido`** y **pull request hacia `main`**,
sin hacer merge. En la descripción, en español simple: qué estaba mal,
cuántos DBA se corrigieron, qué quedó dudoso, el resultado del
verificador y qué decidiste por tu cuenta. Actualiza la sección A12 de
`docs/diseno/pendientes.md` con el resultado.
