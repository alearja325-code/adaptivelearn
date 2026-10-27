# Informe de corrección del catálogo de DBA

**Encargo 02** (`docs/encargos/02-catalogo-curricular-corregido.md`). **Archivo generado** por
`construir_catalogo.py`: no se edita a mano. Las cifras y las tablas salen del catálogo que ese
script arma leyendo los cuatro PDF oficiales del MEN (`../pdfs/`).

## 1. En una frase

El catálogo nuevo, `catalogo_dba.json`, tiene **343 DBA y 1282 evidencias**, cada
uno con la página del PDF de donde se copió. Frente al JSON heredado de la versión 2
(342 DBA, 1254 evidencias): **37 DBA estaban en el grado equivocado**,
**1 faltaba**, y **77**
tenían errores en el texto del enunciado o de las evidencias. El JSON original no se tocó.

## 2. Qué estaba mal en el JSON viejo

- **DBA en el grado equivocado: 37.** La extracción de la V2 asignó al grado
  anterior el primer DBA (a veces los dos primeros) de la primera página de muchos grados. En
  13 casos eso produjo un identificador repetido (por ejemplo, dos
  `matemáticas_2_dba_1`): son los 13 pares que ya se conocían (pendientes, A12). En los otros
  24 el número no chocaba con nada, y por eso el error no se veía.
  Consecuencia: el docente vería en un grado DBA de otro, y a algunos grados les faltaban.
- **DBA que faltaba: MAT-06-05.** Está en el PDF (página 47) y no en el JSON.
- **Evidencias perdidas o pegadas: en 17 DBA**
  el JSON tenía menos evidencias que el PDF: a veces se perdió la primera o la última, a veces
  dos venían pegadas en una (se ve una «m» suelta en medio del texto: es la viñeta).
- **Textos con basura o incompletos.** Números de las marcas de corte de la imprenta pegados al
  final («… vereda o lugar donde vive. 6 5 0 1 12»), el pie de página o el encabezado
  («Ciencias Naturales • Grado 6°»), el ejemplo o una tabla pegados a la última evidencia,
  palabras perdidas o fuera de lugar en algunas páginas de Ciencias Sociales, y frases cortadas.
- **Palabras pegadas** («Reconoceelsignoigualcomo…»): en esas páginas el PDF separa las palabras
  solo por su posición, sin carácter de espacio, y la extracción vieja no lo notó.

## 3. Qué se corrigió

### 3.1 DBA que cambian de grado

La prueba es el encabezado de la página del PDF donde está el DBA.

| DBA nuevo | Identificador viejo | Grado viejo → nuevo | Página | Encabezado de la página |
|---|---|---|---|---|
| `MAT-03-01` | `matemáticas_2_dba_1` (repetido en el JSON) | 2° → 3° | 22 | Matemáticas•Grado3º |
| `MAT-03-02` | `matemáticas_2_dba_2` (repetido en el JSON) | 2° → 3° | 22 | Matemáticas•Grado3º |
| `MAT-04-01` | `matemáticas_3_dba_1` | 3° → 4° | 30 | Matemáticas•Grado4º |
| `MAT-05-01` | `matemáticas_4_dba_1` | 4° → 5° | 37 | Matemáticas•Grado5º |
| `MAT-06-01` | `matemáticas_5_dba_1` | 5° → 6° | 45 | Matemáticas•Grado6º |
| `MAT-07-01` | `matemáticas_6_dba_1` | 6° → 7° | 53 | Matemáticas•Grado7º |
| `MAT-07-02` | `matemáticas_6_dba_2` (repetido en el JSON) | 6° → 7° | 53 | Matemáticas•Grado7º |
| `MAT-08-01` | `matemáticas_7_dba_1` | 7° → 8° | 59 | Matemáticas•Grado8º |
| `MAT-08-02` | `matemáticas_7_dba_2` | 7° → 8° | 59 | Matemáticas•Grado8º |
| `MAT-09-01` | `matemáticas_8_dba_1` | 8° → 9° | 66 | Matemáticas•Grado9º |
| `MAT-10-01` | `matemáticas_9_dba_1` | 9° → 10° | 74 | Matemáticas•Grado10º |
| `MAT-10-02` | `matemáticas_9_dba_2` (repetido en el JSON) | 9° → 10° | 74 | Matemáticas•Grado10º |
| `MAT-11-01` | `matemáticas_10_dba_1` | 10° → 11° | 81 | Matemáticas•Grado11º |
| `LEN-02-01` | `lenguaje_1_dba_1` (repetido en el JSON) | 1° → 2° | 12 | Lenguaje•Grado2º |
| `LEN-03-01` | `lenguaje_2_dba_1` | 2° → 3° | 16 | Lenguaje•Grado3º |
| `LEN-04-01` | `lenguaje_3_dba_1` | 3° → 4° | 20 | Lenguaje•Grado4º |
| `LEN-05-01` | `lenguaje_4_dba_1` | 4° → 5° | 24 | Lenguaje•Grado5º |
| `LEN-06-01` | `lenguaje_5_dba_1` | 5° → 6° | 28 | Lenguaje•Grado6º |
| `LEN-07-02` | `lenguaje_6_dba_2` (repetido en el JSON) | 6° → 7° | 32 | Lenguaje•Grado7º |
| `LEN-08-01` | `lenguaje_7_dba_1` (repetido en el JSON) | 7° → 8° | 36 | Lenguaje•Grado8º |
| `LEN-09-01` | `lenguaje_8_dba_1` | 8° → 9° | 40 | Lenguaje•Grado9º |
| `LEN-10-01` | `lenguaje_9_dba_1` | 9° → 10° | 44 | Lenguaje•Grado10º |
| `LEN-11-01` | `lenguaje_10_dba_1` | 10° → 11° | 48 | Lenguaje•Grado11º |
| `CN-02-01` | `ciencias_naturales_1_dba_1` (repetido en el JSON) | 1° → 2° | 10 | CienciasNaturales•Grado2º |
| `CN-02-02` | `ciencias_naturales_1_dba_2` (repetido en el JSON) | 1° → 2° | 10 | CienciasNaturales•Grado2º |
| `CN-03-01` | `ciencias_naturales_2_dba_1` | 2° → 3° | 12 | CienciasNaturales•Grado3º |
| `CN-04-01` | `ciencias_naturales_3_dba_1` | 3° → 4° | 15 | CienciasNaturales•Grado4º |
| `CN-04-02` | `ciencias_naturales_3_dba_2` (repetido en el JSON) | 3° → 4° | 15 | CienciasNaturales•Grado4º |
| `CN-05-02` | `ciencias_naturales_4_dba_2` | 4° → 5° | 19 | CienciasNaturales•Grado5º |
| `CN-06-01` | `ciencias_naturales_5_dba_1` (repetido en el JSON) | 5° → 6° | 21 | CienciasNaturales•Grado6º |
| `CN-06-02` | `ciencias_naturales_5_dba_2` | 5° → 6° | 21 | CienciasNaturales•Grado6º |
| `CN-07-01` | `ciencias_naturales_6_dba_1` | 6° → 7° | 24 | CienciasNaturales•Grado7º |
| `CN-08-01` | `ciencias_naturales_7_dba_1` | 7° → 8° | 27 | CienciasNaturales•Grado8º |
| `CN-08-02` | `ciencias_naturales_7_dba_2` (repetido en el JSON) | 7° → 8° | 27 | CienciasNaturales•Grado8º |
| `CN-09-02` | `ciencias_naturales_8_dba_2` | 8° → 9° | 30 | CienciasNaturales•Grado9º |
| `CN-10-01` | `ciencias_naturales_9_dba_1` (repetido en el JSON) | 9° → 10° | 34 | CienciasNaturales•Grado10º |
| `CN-11-01` | `ciencias_naturales_10_dba_1` | 10° → 11° | 37 | CienciasNaturales•Grado11º |

### 3.2 DBA cuyo texto cambia

Cada fila dice qué le pasaba al texto del JSON viejo. «Basura de la página» son los números
de las marcas de corte, el pie o el encabezado, o el ejemplo o una tabla pegados al final. Si
el DBA también cambió de grado, está además en la tabla anterior. El detalle de cada
diferencia está en el anexo.

| DBA | Página | Enunciado | Evidencias |
|---|---|---|---|
| `MAT-01-06` | 11 | — | el JSON tenía 3, el PDF tiene 4 |
| `MAT-01-09` | 13 | solo espacios (palabras pegadas o separadas) | — |
| `MAT-04-02` | 30 | palabras distintas | el JSON tenía 2, el PDF tiene 5 |
| `MAT-04-04` | 32 | solo espacios (palabras pegadas o separadas) | el JSON tenía 4, el PDF tiene 5 |
| `MAT-04-05` | 33 | — | el JSON tenía 1, el PDF tiene 4 |
| `MAT-05-06` | 40 | — | el JSON tenía 5, el PDF tiene 6 |
| `MAT-06-04` | 46 | — | el JSON tenía 2, el PDF tiene 3 |
| `MAT-06-10` | 50 | solo espacios (palabras pegadas o separadas) | — |
| `MAT-07-06` | 56 | — | el JSON tenía 3, el PDF tiene 4 |
| `MAT-08-05` | 61 | — | solo espacios (palabras pegadas o separadas) |
| `MAT-08-08` | 63 | solo espacios (palabras pegadas o separadas) | — |
| `MAT-09-03` | 67 | — | tenía texto de más (basura de la página) |
| `MAT-09-05` | 68 | solo espacios (palabras pegadas o separadas) | — |
| `MAT-09-06` | 69 | — | el JSON tenía 1, el PDF tiene 4 |
| `MAT-09-07` | 70 | solo espacios (palabras pegadas o separadas) | — |
| `MAT-10-07` | 77 | — | tenía texto de más (basura de la página) |
| `LEN-02-05` | 14 | solo espacios (palabras pegadas o separadas) | — |
| `LEN-03-01` | 16 | — | solo espacios (palabras pegadas o separadas) |
| `LEN-03-06` | 18 | — | el JSON tenía 3, el PDF tiene 4 |
| `LEN-04-01` | 20 | — | solo espacios (palabras pegadas o separadas) |
| `LEN-07-02` | 32 | — | solo espacios (palabras pegadas o separadas) |
| `LEN-11-06` | 51 | — | solo espacios (palabras pegadas o separadas) |
| `LEN-11-07` | 51 | — | solo espacios (palabras pegadas o separadas) |
| `CN-03-06` | 14 | — | el JSON tenía 1, el PDF tiene 4 |
| `CN-04-05` | 16 | — | el JSON tenía 3, el PDF tiene 4 |
| `CN-06-03` | 22 | — | solo espacios (palabras pegadas o separadas); tenía texto de más (basura de la página) |
| `CN-06-04` | 22 | — | tenía texto de más (basura de la página) |
| `CN-06-05` | 23 | — | tenía texto de más (basura de la página) |
| `CN-08-01` | 27 | — | solo espacios (palabras pegadas o separadas) |
| `CN-08-03` | 28 | — | solo espacios (palabras pegadas o separadas) |
| `CN-08-04` | 28 | — | el JSON tenía 3, el PDF tiene 4 |
| `CN-09-04` | 31 | — | tenía texto de más (basura de la página) |
| `CN-09-05` | 32 | tenía texto de más (basura de la página) | — |
| `CN-10-03` | 35 | — | estaba cortado: le faltaba el final |
| `CN-11-01` | 37 | solo espacios (palabras pegadas o separadas) | — |
| `CS-01-02` | 8 | — | el JSON tenía 3, el PDF tiene 4 |
| `CS-01-03` | 8 | tenía texto de más (basura de la página) | el JSON tenía 3, el PDF tiene 4 |
| `CS-01-04` | 9 | — | el JSON tenía 3, el PDF tiene 4 |
| `CS-01-05` | 9 | — | palabras distintas; tenía texto de más (basura de la página) |
| `CS-01-07` | 10 | — | tenía texto de más (basura de la página) |
| `CS-01-08` | 11 | — | tenía texto de más (basura de la página) |
| `CS-02-02` | 12 | — | el JSON tenía 3, el PDF tiene 4 |
| `CS-02-03` | 12 | — | estaba cortado: le faltaba el final; palabras distintas |
| `CS-02-05` | 13 | — | tenía texto de más (basura de la página) |
| `CS-02-07` | 15 | palabras distintas | palabras distintas |
| `CS-02-08` | 16 | — | estaba cortado: le faltaba el final; tenía texto de más (basura de la página) |
| `CS-03-04` | 18 | — | tenía texto de más (basura de la página) |
| `CS-03-06` | 19 | — | tenía texto de más (basura de la página) |
| `CS-03-08` | 20 | — | tenía texto de más (basura de la página) |
| `CS-04-02` | 21 | — | tenía texto de más (basura de la página) |
| `CS-04-04` | 22 | — | tenía texto de más (basura de la página) |
| `CS-04-06` | 23 | — | tenía texto de más (basura de la página) |
| `CS-05-01` | 25 | — | solo espacios (palabras pegadas o separadas) |
| `CS-05-02` | 25 | — | tenía texto de más (basura de la página) |
| `CS-05-04` | 26 | — | tenía texto de más (basura de la página) |
| `CS-05-06` | 27 | — | palabras distintas |
| `CS-05-08` | 28 | — | tenía texto de más (basura de la página) |
| `CS-06-02` | 29 | — | tenía texto de más (basura de la página) |
| `CS-06-04` | 30 | — | tenía texto de más (basura de la página) |
| `CS-06-05` | 31 | — | palabras distintas; solo espacios (palabras pegadas o separadas); tenía texto de más (basura de la página) |
| `CS-06-06` | 31 | — | el JSON tenía 3, el PDF tiene 4 |
| `CS-06-08` | 32 | — | tenía texto de más (basura de la página) |
| `CS-07-01` | 33 | palabras distintas | palabras distintas; solo espacios (palabras pegadas o separadas) |
| `CS-07-03` | 34 | — | palabras distintas |
| `CS-07-05` | 35 | — | tenía texto de más (basura de la página) |
| `CS-07-06` | 36 | palabras distintas | palabras distintas |
| `CS-07-07` | 36 | — | palabras distintas; tenía texto de más (basura de la página) |
| `CS-08-04` | 39 | — | tenía texto de más (basura de la página) |
| `CS-08-06` | 40 | — | tenía texto de más (basura de la página) |
| `CS-08-07` | 41 | — | palabras distintas |
| `CS-08-08` | 41 | — | palabras distintas |
| `CS-09-04` | 43 | — | tenía texto de más (basura de la página) |
| `CS-09-06` | 44 | — | tenía texto de más (basura de la página) |
| `CS-10-04` | 47 | — | tenía texto de más (basura de la página) |
| `CS-10-05` | 48 | — | tenía texto de más (basura de la página) |
| `CS-11-04` | 50 | — | solo espacios (palabras pegadas o separadas); tenía texto de más (basura de la página) |
| `CS-11-05` | 51 | — | tenía texto de más (basura de la página) |

### 3.3 Donde el texto del PDF no dice lo que la página muestra

En estos casos la capa de texto del PDF (lo que un programa puede leer) no coincide con la
página impresa, y se corrigió mirando la página. Solo tocan espacios, un salto de línea o una
ligadura: ninguna palabra. Están escritas en `CORRECCIONES`, dentro del script, y el verificador
comprueba cada una.

| DBA | Dónde | El PDF trae | Se copia | Página | Por qué |
|---|---|---|---|---|---|
| `MAT-02-01` | evidencia 2 | «? +b = c.» | «? + b = c.» | 15 | la página muestra «+ b», como «a + b» en la línea anterior; la capa de texto no trae ese espacio |
| `MAT-04-02` | enunciado | «(fraccionarios)1» | «(fraccionarios)» | 30 | el «1» es la llamada en superíndice a una nota al pie de la misma página, no parte del enunciado |
| `MAT-09-06` | evidencia 1 | «bidimen-sionales» | «bidimensionales» | 69 | guion de partición al final de la línea (la palabra se corta en dos renglones) |
| `CS-06-05` | evidencia 1 | «geográ cos» | «geográficos» | 31 | la ligadura «fi» está dibujada pero el PDF no la declara como texto: queda un hueco |
| `CS-07-07` | enunciado | «Co mprende» | «Comprende» | 36 | hueco de diagramación dentro de la palabra, sin carácter de espacio |
| `CS-08-08` | enunciado | «Comprendelaimportanciadelasasociaciones,» | «Comprende la importancia de las asociaciones,» | 41 | el PDF oficial imprime esas palabras sin espacios (se ve así en la página): solo se agregan los espacios |

## 4. Qué quedó dudoso

No se adivinó. Cada uno está marcado en el registro (campo `dudoso`):

- **`MAT-11-09`** (p. 86): la página no tiene encabezado de grado: se toma el de la página anterior y la numeración que sigue
- **`MAT-11-10`** (p. 86): la página no tiene encabezado de grado: se toma el de la página anterior y la numeración que sigue

Además, cosas del propio PDF que se copiaron tal cual y conviene que el equipo conozca:

- **Erratas del documento oficial**, conservadas: «dados en en América» (`CS-07-06`) y «con
  los se cuenta» (`CS-08-08`, evidencia 2). Copiar exacto incluye sus errores.
- **Superíndices y subíndices** quedan como un carácter normal pegado a su palabra: «dm3»
  (decímetro cúbico, `MAT-08-05`) y «H2O» (`CN-06-03`). Mostrarlos como ³ y ₂ es una
  decisión de presentación para la interfaz.
- **Evidencias repetidas por el MEN:** algunas evidencias tienen las mismas palabras en DBA
  distintos (sobre todo en Matemáticas). El verificador comprueba que el PDF las imprime bajo
  cada uno: no es un error de extracción.
- **Guiones al final de un renglón:** se unen sin espacio a la línea siguiente. Tres son
  guiones reales («arena-gravilla,», «(Boyle-Mariotte,», «(Capitalista-Comunista),»);
  el de «bidimen-sionales» es partición de palabra y se corrigió (3.3).

## 5. Conteos finales, según el PDF

No se forzó que sumaran 342: es lo que hay en los documentos.

| Área | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° | 10° | 11° | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Matemáticas (MAT) | 10 | 11 | 11 | 11 | 12 | 12 | 9 | 12 | 11 | 10 | 10 | **119** |
| Lenguaje (LEN) | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | **88** |
| Ciencias Naturales (CN) | 4 | 4 | 6 | 7 | 4 | 5 | 4 | 5 | 6 | 4 | 5 | **54** |
| Ciencias Sociales (CS) | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 5 | 5 | **82** |
| **Total** | 30 | 31 | 33 | 34 | 32 | 33 | 29 | 33 | 33 | 27 | 28 | **343** |

Como estaban en el JSON viejo, para comparar:

| Área | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° | 10° | 11° | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Matemáticas | 10 | 13 | 10 | 11 | 12 | 12 | 9 | 11 | 12 | 9 | 9 | 118 |
| Lenguaje | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 7 | 88 |
| Ciencias Naturales | 6 | 3 | 7 | 6 | 5 | 4 | 5 | 4 | 6 | 4 | 4 | 54 |
| Ciencias Sociales | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 5 | 5 | 82 |

Documentos (ADR-033): Matemáticas **V.2** (`dba_matematicas_v2.pdf`); Lenguaje **V.2** (`dba_lenguaje_v2.pdf`); Ciencias Naturales **V.1** (`dba_ciencias_naturales_v1.pdf`); Ciencias Sociales **V.1** (`dba_ciencias_sociales_v2.pdf`).

## 6. Cómo se hizo y cómo se comprueba

- **Cómo se lee el PDF** (`construir_catalogo.py`). El grado sale del encabezado de cada
  página. Las palabras se arman siguiendo el orden en que el PDF guarda los caracteres, con los
  espacios que el PDF trae; donde no los trae, un hueco del ancho de un espacio también separa.
  Cada parte del DBA se reconoce por su tamaño de letra: el número (~26 pt), el enunciado
  (11 pt), los títulos «Evidencias de aprendizaje» y «Ejemplo», y cada evidencia por su viñeta.
  Una evidencia puede seguir en la otra columna o en la página siguiente.
- **Cómo se comprueba** (`_verificar_catalogo.py`). Con otro programa (`pdftotext`, de
  poppler), para no depender del lector que armó el catálogo: formato y unicidad del código,
  numeración sin huecos, enunciado y evidencias literales en su página (las letras en orden, sin
  los espacios), grado igual al del encabezado, cada evidencia en un solo DBA, que los números
  de DBA impresos en cada página sean exactamente los del catálogo, y la versión de cada
  documento. Al final introduce siete errores a propósito en copias en memoria y comprueba que
  los atrapa todos.
- **Lo que el verificador anota sin que sea falla:** textos que siguen en la otra columna o
  en la página siguiente (se aceptan solo si el corte cae justo en un borde de renglón);
  textos cuyo espaciado no coincide con el de poppler, que lee distinto las palabras que el
  PDF separa solo por posición (son los de 3.3 y casos como «mujeres, derechos», donde el PDF
  sí trae el espacio); y las evidencias que el MEN repite en varios DBA. Las dos observaciones
  que reporta son `MAT-11-09` y `MAT-11-10`, sin encabezado de grado (sección 4).
- **Lo que el verificador no puede ver:** una palabra que esté en la capa de texto del PDF pero
  no impresa en la página (pasó una vez: un «con» de una columna aparecía en la otra; se
  encontró comparando con la página impresa y con el JSON viejo, y se corrigió el lector). Las
  diferencias con el JSON viejo se revisaron una por una, y las de Ciencias Sociales 3°, 6°, 7°
  y 8° se confirmaron mirando la página renderizada.

## 7. Notas para la auditoría completa (A12) — fuera de este encargo

- **El ejemplo de cada DBA** no se copió (QA-011). Al leer los PDF se vio que muchos ejemplos
  dependen de una imagen, una tabla o una fórmula (por ejemplo, Matemáticas 9°, `MAT-09-03`, y
  10°, `MAT-10-07`; Ciencias Sociales, con fotografías y sus créditos). El JSON viejo pegaba
  parte de esos ejemplos al final de la última evidencia; aquí se quitaron porque no son
  evidencia.
- **Notas al pie:** hay llamadas a nota en algunos títulos «Ejemplo» de Matemáticas (páginas
  )
  y en el enunciado de `MAT-04-02`. El catálogo no tiene dónde guardar notas.
- **Las direcciones del JSON viejo** apuntan a rutas de Colombia Aprende de 2022; las vigentes
  son las de ADR-033.

## Anexo · cada diferencia de texto con el JSON viejo

Formato: «…texto del JSON…» → «…texto del PDF…». Solo el primer par de diferencias de cada
texto; el resto, en el catálogo.

- `MAT-01-06` evidencias: el JSON tenía 3, el PDF tiene 4.
- `MAT-01-09` enunciado: solo espacios: «…Reconoceelsignoigualcomounaequivalencia entre ex…» → «…Reconoce el signo igual como una equivalencia en…»
- `MAT-04-02` enunciado: «…ales (fraccionarios)1 , expresados como fr…» → «…ales (fraccionarios), expresados como fr…»
- `MAT-04-02` evidencias: el JSON tenía 2, el PDF tiene 5.
- `MAT-04-04` enunciado: solo espacios: «…Caracterizaycomparaatributosmediblesdelos objetos (…» → «…Caracteriza y compara atributos medibles de los obj…»
- `MAT-04-04` evidencias: el JSON tenía 4, el PDF tiene 5.
- `MAT-04-05` evidencias: el JSON tenía 1, el PDF tiene 4.
- `MAT-05-06` evidencias: el JSON tenía 5, el PDF tiene 6.
- `MAT-06-04` evidencias: el JSON tenía 2, el PDF tiene 3.
- `MAT-06-10` enunciado: solo espacios: «…Interpretainformaciónestadísticapresentada en dive…» → «…Interpreta información estadística presentada en d…»
- `MAT-07-06` evidencias: el JSON tenía 3, el PDF tiene 4.
- `MAT-08-05` evidencia 2: solo espacios: «…volumen (litros, dm3 , etc) en la solución de un problema.…» → «…volumen (litros, dm3, etc) en la solución de un problema.…»
- `MAT-08-08` enunciado: solo espacios: «…Identificayanalizarelacionesentrepropiedades de la…» → «…Identifica y analiza relaciones entre propiedades …»
- `MAT-09-03` evidencia 2: «…on otras sucesiones. No cuadrados Lado Perímetro Área 1 1u 4u 1u2 2 1u 1u 1u2 3 2u 4 3u 5 5u 6 7 8 9…» → «…on otras sucesiones.…»
- `MAT-09-05` enunciado: solo espacios: «…laciones geométricas(teoremadeThalesyelteoremade Pitágoras) …» → «…laciones geométricas (teorema de Thales y el teorema de Pitá…»
- `MAT-09-06` evidencias: el JSON tenía 1, el PDF tiene 4.
- `MAT-09-07` enunciado: solo espacios: «…Interpretaelespaciodemaneraanalíticaapartir de rel…» → «…Interpreta el espacio de manera analítica a partir…»
- `MAT-10-07` evidencia 4: «…roximación sucesiva. P(t)=…» → «…roximación sucesiva.…»
- `LEN-02-05` enunciado: solo espacios: «…Identificalaspalabrasrelevantesdeunmensaje y las a…» → «…Identifica las palabras relevantes de un mensaje y…»
- `LEN-03-01` evidencia 1: solo espacios: «…Reconocelosusosdelosmediosdecomunicación con los…» → «…Reconoce los usos de los medios de comunicación …»
- `LEN-03-06` evidencias: el JSON tenía 3, el PDF tiene 4.
- `LEN-04-01` evidencia 4: solo espacios: «…Dialogasobreelcontenidodelostextosinformativos …» → «…Dialoga sobre el contenido de los textos inform…»
- `LEN-07-02` evidencia 4: solo espacios: «…Comprendequelosgestospermitencomplementar los men…» → «…Comprende que los gestos permiten complementar lo…»
- `LEN-11-06` evidencia 3: solo espacios: «…Dacuentadelaorganizaciónydeloscomponentes …» → «…Da cuenta de la organización y de los comp…»
- `LEN-11-07` evidencia 5: solo espacios: «…Evitaelusodefalaciasendiscusionesacadémicas.…» → «…Evita el uso de falacias en discusiones acadé…»
- `CN-03-06` evidencias: el JSON tenía 1, el PDF tiene 4.
- `CN-04-05` evidencias: el JSON tenía 3, el PDF tiene 4.
- `CN-06-03` evidencia 2: solo espacios: «…s químicos (NaCl, H2 O, Cu).…» → «…s químicos (NaCl, H2O, Cu).…»
- `CN-06-03` evidencia 4: «…mentos y medicinas). un seguimiento al calentamiento del agua hasta que se acciona la válvula de seguridad. A partir de esta información explica la relación de la temperatura y la presión con el comportamiento de la sustancia y representa la relación del tiempo (t) con la temperatura (T) mediante una gráfica en la que identifica el punto de ebullición.…» → «…mentos y medicinas).…»
- `CN-06-04` evidencia 4: «…organelas celulares. Ciencias Naturales • Grado 6°…» → «…organelas celulares.…»
- `CN-06-05` evidencia 3: «…ntre los organismos. Ciencias Naturales • Grado 6°…» → «…ntre los organismos.…»
- `CN-08-01` evidencia 4: solo espacios: «…Explica,haciendousodelasleyestermodinámicas, el …» → «…Explica, haciendo uso de las leyes termodinámica…»
- `CN-08-03` evidencia 3: solo espacios: «…de los gases (Boyle- Mariotte, Charles, Gay-Lussac, Ley comb…» → «…de los gases (Boyle-Mariotte, Charles, Gay-Lussac, Ley combi…»
- `CN-08-04` evidencias: el JSON tenía 3, el PDF tiene 4.
- `CN-09-04` evidencia 4: «… Herencia de Mendel. concentración. Elabora preguntas y predice posibles respuestas con base en argumentos de tipo teórico y experimental en las cuales se realicen variaciones de cantidad de soluto – solvente o se someta la muestra a la acción de la temperatura u otras variaciones que considere necesarias. (disoluciones, mezclas) que considere adecuados según el propósito y evaluando el nivel de precisión de los indicadores utilizados. Durante el proceso formula conclusiones y proyecta lo que podría pasar al aplicar el protocolo a nuevas sustancias. Reconoce además, algunos límites y variables que intervienen en las conclusiones que elabora. Ciencias Naturales • Grado 9°…» → «… Herencia de Mendel.…»
- `CN-09-05` enunciado: «…ión de las especies. Ejemplo En los guisantes las plantas altas (T) son dominantes de las enanas (t), el color amarillo de las semillas (A) es dominante del verde (a), y la semilla lisa (L) es dominante de la rugosa (l). Explica los genotipos, los fenotipos y las proporciones de los descendientes del siguiente cruce: TtAaLl x ttaall…» → «…ión de las especies.…»
- `CN-10-03` evidencia 4: «…os compuestos, dando…» → «…os compuestos, dando ejemplos de cada tipo de reacción.…»
- `CN-11-01` enunciado: solo espacios: «…Comprendelanaturalezadelapropagacióndel sonido y …» → «…Comprende la naturaleza de la propagación del son…»
- `CS-01-02` evidencias: el JSON tenía 3, el PDF tiene 4.
- `CS-01-03` enunciado: «… propios y sociales. 0…» → «… propios y sociales.…»
- `CS-01-03` evidencias: el JSON tenía 3, el PDF tiene 4.
- `CS-01-04` evidencias: el JSON tenía 3, el PDF tiene 4.
- `CS-01-05` evidencia 2: «…s entre sus gustos, 6 costumbres y formas …» → «…s entre sus gustos, costumbres y formas …» · «… de comunicarse, con 5 los demás integrant…» → «… de comunicarse, con los demás integrant…» · (y más)
- `CS-01-05` evidencia 4: «… o lugar donde vive. 0 1 12…» → «… o lugar donde vive.…»
- `CS-01-07` evidencia 4: «…e las metas comunes. 6 Las reglas de juego serán… 0 12…» → «…e las metas comunes.…»
- `CS-01-08` evidencia 4: «… familiar y escolar. 6 5 0 1 12…» → «… familiar y escolar.…»
- `CS-02-02` evidencias: el JSON tenía 3, el PDF tiene 4.
- `CS-02-03` evidencia 1: «… de la conformación 12 de su familia antes …» → «… de la conformación de su familia antes …»
- `CS-02-03` evidencia 3: «…sde la lectura de su…» → «…sde la lectura de su registro civil de nacimiento y elabora un árbol genealógico.…»
- `CS-02-05` evidencia 4: «…r estas situaciones. 6 5 0 1 12…» → «…r estas situaciones.…»
- `CS-02-07` enunciado: «…ón territorial en su 150 S municipio, desde: c…» → «…ón territorial en su municipio, desde: c…»
- `CS-02-07` evidencia 1: «…pio y lo diferencia 30 N 0 entre los demás muni…» → «…pio y lo diferencia entre los demás muni…» · «…os del departamento. 1…» → «…os del departamento.…»
- `CS-02-07` evidencia 2: «…mientos, localidades 12 y/o territorios ind…» → «…mientos, localidades y/o territorios ind…»
- `CS-02-08` evidencia 2: «…os integrantes de su…» → «…os integrantes de su familia) y en las preferencias en los juegos entre los compañeros del grupo en la escuela.…»
- `CS-02-08` evidencia 4: «… ayuda y protección. 6 0 12…» → «… ayuda y protección.…»
- `CS-03-04` evidencia 4: «…man su departamento. 6 0 12…» → «…man su departamento.…»
- `CS-03-06` evidencia 4: «…ntes de información. 6 5 0 1 12…» → «…ntes de información.…»
- `CS-03-08` evidencia 4: «… en las comunidades. 6 0…» → «… en las comunidades.…»
- `CS-04-02` evidencia 4: «…des que en el campo. 6 5 0 1 12…» → «…des que en el campo.…»
- `CS-04-04` evidencia 4: «…ada de los europeos. 6 0 12…» → «…ada de los europeos.…»
- `CS-04-06` evidencia 4: «…uilibrio de poderes. 6 5 0 1 12…» → «…uilibrio de poderes.…»
- `CS-05-01` evidencia 1: solo espacios: «…E xplica las formas de división territori…» → «…Explica las formas de división territoria…»
- `CS-05-02` evidencia 4: «…tar con dos océanos. 6 5 0 1 12…» → «…tar con dos océanos.…»
- `CS-05-04` evidencia 4: «…ntes de información. 6 0 12…» → «…ntes de información.…»
- `CS-05-06` evidencia 4: «…a y constructora de 6 una cultura de paz. …» → «…a y constructora de una cultura de paz.…» · «… una cultura de paz. 5 0 1 12…» → «… una cultura de paz.…»
- `CS-05-08` evidencia 4: «…dad en su comunidad. 6 0 12…» → «…dad en su comunidad.…»
- `CS-06-02` evidencia 4: «…en caso de un sismo. 6 5 0 1 12…» → «…en caso de un sismo.…»
- `CS-06-04` evidencia 4: «…sociedades actuales. 6 0 12 Derechos Básicos 11…» → «…sociedades actuales.…»
- `CS-06-05` evidencia 2: «…lógicos y culturales las sociedades preh…» → «…lógicos y culturales de las sociedades preh…» · «…spectos religiosos, astronomía y las téc…» → «…spectos religiosos, la astronomía y las téc…»
- `CS-06-05` evidencia 3: solo espacios: «…C o m p a r a l a e s t r u c t u r a s o…» → «…Compara la estructura social, política y …»
- `CS-06-05` evidencia 4: «…mundo contemporáneo. Machu Picchu (Perú). Fotografía tomada de: www.pixabay.com (banco de imágenes) en: goo.gl/BFM3xO de Aprendizaje • V.1…» → «…mundo contemporáneo.…»
- `CS-06-06` evidencias: el JSON tenía 3, el PDF tiene 4.
- `CS-06-08` evidencia 4: «…la condición humana. 6 0 12 Derechos Básicos 11…» → «…la condición humana.…»
- `CS-07-01` enunciado: «…las representaciones mundo han cambiado …» → «…las representaciones del mundo han cambiado …» · «…an y de los avances la tecnología.…» → «…an y de los avances de la tecnología.…»
- `CS-07-01` evidencia 1: «…cia de los viajes de exploradores del me…» → «…cia de los viajes de los exploradores del me…» · «…evo en la expansión conocimiento del mun…» → «…evo en la expansión del conocimiento del mun…»
- `CS-07-01` evidencia 2: «…ión y representación mundo que se tenía …» → «…ión y representación del mundo que se tenía …» · «…ra espacial europea señala los cambios y…» → «…ra espacial europea y señala los cambios y…» · (y más)
- `CS-07-01` evidencia 3: solo espacios: «…as e imágenes sateli tales y, describe el uso de la cartogra…» → «…as e imágenes satelitales y, describe el uso de la cartograf…»
- `CS-07-03` evidencia 4: «… con el paso de los 6 siglos.…» → «… con el paso de los siglos.…»
- `CS-07-05` evidencia 4: «…cial de los pueblos. 6 5 0 1 12…» → «…cial de los pueblos.…»
- `CS-07-06` enunciado: «…s y consecuencias de procesos de Conquis…» → «…s y consecuencias de los procesos de Conquis…»
- `CS-07-06` evidencia 2: «…s y continuidades de organizaciones soci…» → «…s y continuidades de las organizaciones soci…»
- `CS-07-06` evidencia 3: «…ada de los europeos continente americano…» → «…ada de los europeos al continente americano…»
- `CS-07-07` evidencia 1: «…echos fundamentales las enunciados en la Con…» → «…echos fundamentales enunciados en la Con…»
- `CS-07-07` evidencia 3: «…rgumentada, a partir estudio de casos y …» → «…rgumentada, a partir del estudio de casos y …» · «…onstitucional frente al a hechos o situacio…» → «…onstitucional frente a hechos o situacio…»
- `CS-07-07` evidencia 4: «…nsa de los derechos. histó- a se que…» → «…nsa de los derechos.…»
- `CS-08-04` evidencia 4: «…e colombianos,....). 6 5…» → «…e colombianos,....).…»
- `CS-08-06` evidencia 4: «…diano y largo plazo. 6 0 12 Derechos Básicos 11…» → «…diano y largo plazo.…»
- `CS-08-07` evidencia 1: «…s, el incremento de pobreza y la violenc…» → «…s, el incremento de la pobreza y la violenc…»
- `CS-08-07` evidencia 2: «…uación actual, desde concretos, de la vu…» → «…uación actual, desde casos concretos, de la vu…»
- `CS-08-07` evidencia 3: «…os relacionados con exclusión, la discri…» → «…os relacionados con la exclusión, la discri…» · «…n y la intolerancia a diferencia, que ha…» → «…n y la intolerancia a la diferencia, que ha…» · (y más)
- `CS-08-07` evidencia 4: «… y constitucionales Colombia y en el mun…» → «… y constitucionales en Colombia y en el mun…»
- `CS-08-08` evidencia 2: «…tas y procedimientos la alternativos (diálo…» → «…tas y procedimientos alternativos (diálo…» · «…uenta para resolver casos conflicto social o …» → «…uenta para resolver un conflicto social o …»
- `CS-08-08` evidencia 3: «…el magisterio,...), la como todo conflicto …» → «…el magisterio,...), como todo conflicto …» · «…al o laboral, puede la resolverse mediante …» → «…al o laboral, puede resolverse mediante …» · (y más)
- `CS-08-08` evidencia 4: «…cia de un desarrollo con social, económico y…» → «…cia de un desarrollo social, económico y…» · «…na lógica orientada bienestar colectivo.…» → «…na lógica orientada al bienestar colectivo.…» · (y más)
- `CS-09-04` evidencia 4: «…pción, entre otros). 6 5 0 1 12…» → «…pción, entre otros).…»
- `CS-09-06` evidencia 4: «…ncialidades humanas. 6 0…» → «…ncialidades humanas.…»
- `CS-10-04` evidencia 4: «…os Derechos Humanos. 6 5 0 1 12…» → «…os Derechos Humanos.…»
- `CS-10-05` evidencia 4: «…s bélicos mundiales. 6 0 12…» → «…s bélicos mundiales.…»
- `CS-11-04` evidencia 1: solo espacios: «…ónicos (Capitalista- Comunista), como sistemas políticos y e…» → «…ónicos (Capitalista-Comunista), como sistemas políticos y ec…»
- `CS-11-04` evidencia 4: «…es en la actualidad. 6 0 12…» → «…es en la actualidad.…»
- `CS-11-05` evidencia 4: «…nasur, entre otros). 6 5 0 1 12 Centro Administrativo Bogotá Conmutador: Línea gratuita Línea gratuita Ministerio de Calle 43 No 57-14 Nacional, CAN D.C. – Colombia 6 (+571) 2222800 150 210 Fax: (+571) 2222800 fuera de Bogotá Bogotá (+571) 2220206 0 12 www.mineducacion.gov.co @Mineducación Educación Nacional…» → «…nasur, entre otros).…»
