# 19. Entrega de la Fase III — Diseño Computacional

**Metodología:** MODESEC (Caro y Toscano, TISE 2009). **Fecha:** 2026-10-26.

MODESEC: *«La fase del diseño computacional comprende la descripción de los elementos que
permitirán que el sistema funcione a cabalidad con los procesos que fueron definidos en el
transcurso del diseño educativo y multimedial.»* Este documento es el índice de esa fase: qué
pide MODESEC, en qué archivo está, y cómo se comprueba.

## 1. Lo que pide MODESEC, y dónde está

| Sub-etapa de MODESEC | Documento | Diagramas y fuentes |
|---|---|---|
| Descripción del proceso de desarrollo | `10-proceso-desarrollo.md` | — |
| Análisis de requerimientos | `11-analisis-requerimientos.md` | `requerimientos/requerimientos.py` |
| Diagrama de casos de uso | `12-casos-de-uso.md` | `uml/svg/cu-*.svg` (7) · `uml/datos_casos_uso.py` |
| Diagrama de clases | `13-diagrama-clases.md` | `uml/svg/clases-*.svg` (2) · `uml/datos_clases.py` |
| Diagrama de objetos | `14-diagrama-objetos.md` | `uml/svg/objetos-*.svg` (2) · `uml/datos_objetos.py` |
| Diagramas de secuencia | `15-diagramas-secuencia.md` | `uml/svg/secuencia-*.svg` (8) · `uml/datos_secuencias.py` |
| Modelado de la base de datos: MER | `16-modelo-entidad-relacion.md` | `mer/mer-cajas.svg` (vista de conjunto), `mer/mapa-chen.svg`, `mer/vista1.svg` a `vista7.svg`, `mer/leyenda.svg` · `mer/datos_mer.py` |
| Modelado de la base de datos: MR | `17-modelo-relacional.md` | `modelo-relacional/mr_mysql.sql` (MySQL 8), `mr_esquema.sql` (SQLite), `mr_adaptivelearn.dbml` |
| Modelado de la base de datos: diccionario de datos | `18-diccionario-datos.md` | `modelo-relacional/datos_mr.py` |
| *Anexo, no lo pide MODESEC:* catálogo de endpoints | `20-catalogo-endpoints.md` | `api/datos_api.py` |

`10` y `11` son del equipo. Del `12` al `18`, y el `20`, todo lo que es tabla o diagrama **se
genera** desde los `datos_*.py`; ningún documento se edita a mano. Así un mismo dato no puede
decir una cosa en un diagrama y otra en un documento.

El `20` es el puente hacia la construcción: cada endpoint que el frontend le pedirá al backend,
por incremento, con el caso de uso que atiende, la operación del diagrama de clases que lo
resuelve, las entidades que toca y quién puede llamarlo. Numerados de E-01 a E-35, para
repartirlos como tareas.

**En PDF:** `entrega-pdf/`, uno por documento —de `00-Entrega-Fase-III-indice.pdf` (este) a
`20-Catalogo-de-endpoints.pdf`—, más `16-MER-laminas-A1.pdf`, el MER entero en formato A1.

**Para presentar:** `mer/mer-pantalla-completa.html` (el MER entero en una lámina, con la
estructura de la v3 del docente, a pantalla completa y con zoom), `mer/mer-vistas-chen.html`
(el MER formal en Chen, con sus siete vistas) y `uml/uml-fase3.html` (los 19 diagramas UML en
una página, con índice).

## 2. En cifras

| | |
|---|---|
| Requerimientos (de `11`) | 58: 44 funcionales y 14 no funcionales |
| Casos de uso | 31, en 7 diagramas; cubren los 44 requerimientos funcionales |
| Clases | 20 del dominio, 12 enumeraciones, 13 de servicio e interfaces |
| Diagrama de objetos | 34 objetos y 42 enlaces, en 2 vistas del mismo momento |
| Diagramas de secuencia | 8 |
| MER | 18 entidades (+ Reporte, derivado), 22 relaciones (+ 2 derivadas), 71 atributos —en Chen estricta, sin llaves foráneas—, 6 ciclos (todos cerrados), 21 restricciones de integridad; (mín, máx) en cada extremo y matriz CRUD |
| Revisión del docente (2026-09-01) | 12 hallazgos: 11 resueltos y H-5 en parte (decisión por confirmar). Cuenta uno por uno en `16` §10 |
| Revisión del docente (2026-10-22) | 5 notas: R1 (área, grado y código, ADR-036) y R3 (estado de verificación, ADR-037) aplicadas en el MER, el MR y el diccionario el 2026-10-26; R2 y R5 son del backend (Fase IV); R4 espera la pregunta P2. Triaje en `21`; cuenta en `16` §10 |
| MR | 18 tablas, 104 columnas, 23 llaves foráneas, 17 UNIQUE, 14 CHECK |
| Endpoints (anexo `20`) | 35, en los 4 incrementos: 10 ya existen en el backend I1 (2 de ellos por ajustar), 24 faltan y 1 es opcional |

## 3. Cómo se comprueba

Desde `fase-3-diseno-computacional/`. Cada script termina en `RESULTADO: … todas correctas` o
dice qué falló.

```bash
cd mer && python construir_vistas.py && python mapa_cajas.py && python _verificar_mer.py && python _verificar_vistas.py && python _verificar_mapa.py && python generar_documento.py && cd ..
cd modelo-relacional && python generar.py && python documento_mr.py && python _verificar_mr_mer.py && python verificar_mr.py && cd ..
cd uml && python generar_uml.py && python _verificar_uml.py && cd ..
cd api && python generar_api.py && python _verificar_api.py && cd ..
python ../herramientas/md_a_pdf.py
```

El último paso vuelve a sacar los PDF de `entrega-pdf/` desde los Markdown vigentes: un PDF no
se edita, se regenera.

| Verificador | Qué garantiza |
|---|---|
| `mer/_verificar_vistas.py`, `mer/_verificar_mapa.py` | Cada relación en exactamente una vista; ninguna línea atraviesa una caja ni tacha un rótulo. |
| `modelo-relacional/_verificar_mr_mer.py` | El MR no se aparta del MER. |
| `mer/_verificar_mer.py` | Coherencia interna del MER: línea doble ⇔ mínimo ≥ 1, y los 6 ciclos del modelo declarados, reales e independientes. |
| `modelo-relacional/verificar_mr.py` | El esquema hace cumplir lo que dice: 67 pruebas de violación, aceptación y borrado, en SQLite. |
| `modelo-relacional/probar_mysql.py` | Las mismas 67 pruebas contra MySQL real; cada rechazo, por la restricción exacta. Corrido el 2026-10-26 contra MySQL 8.0.46: todo correcto (`salida_probar_mysql.txt`). La versión anterior del esquema se había corrido contra MySQL 8.4.11. |
| `uml/_verificar_uml.py` | Casos de uso ↔ requerimientos; clases ↔ MR y MER; el diagrama de objetos **se carga en el esquema** sin violar nada; la regla adaptativa da lo que el diagrama muestra; toda operación de una secuencia existe en su clase; la matriz CRUD es coherente con los borrados en cascada del MR. |
| `api/_verificar_api.py` | Todo caso de uso tiene endpoint; cada endpoint usa una operación de servicio que existe y toca lo que dice la matriz CRUD, ni más ni menos; quien lo llama es el actor de su caso de uso; toda llamada de la IGU en las secuencias es un endpoint; ninguna ruta hace lo que una decisión prohíbe; y el estado de cada endpoint (hecho o por hacer) es el del código real: lee los controladores de `backend/src/`. |

## 4. Lo que queda abierto, declarado

| Pendiente | Qué falta | Dónde se declara |
|---|---|---|
| **V-6 / QA-014** | El censo de qué evidencias admiten formato cerrado: los valores de `evidencia_dictamen`. | `16` §12, `18` |
| **QA-013** | Errores de extracción del catálogo del MEN. | `11` §5 |
| **QA-011** | `dba.ejemplo` todavía no está en la normalización del currículo. | `18` |
| **V-12** (nuevo) | Qué muestra la pantalla con un DBA en el que ninguna evidencia admite formato cerrado. | `12` §7, `16` §12 |
| **V-9** | Versionar el contenido del ítem: diferido. | `16` §12 |
| **V-10** | Una excepción de contraste en la interfaz: diferida. | `11` §5 |
| **RNF-13** | El tiempo límite de la generación del banco: se mide al construir I2. | `11` |
| **RNF-06** | La autorización del acudiente: mientras falte, el sistema no se usa con estudiantes reales. | `11` |
| **MariaDB y MySQL 8.4** | `mr_mysql.sql` no usa nada que MariaDB 10.11 no tenga, pero no se ha ejecutado en MariaDB; y la versión del 2026-10-26 (catálogo normalizado) se probó en MySQL 8.0.46, no en 8.4. Probarlo al integrar con el backend de I1. | `17` |
| **R4 / P2** (revisión del 2026-10-22) | Si se quitan `codigo_expira_en` y `codigo_ultimo_envio` de la credencial, dónde viven el vencimiento del código y la espera para reenviarlo. Espera la respuesta del docente. | `21` |
| **Datos del catálogo** (A12) | `curriculo_men_normalizado.json` repite 13 de sus 342 identificadores de DBA, y con el código nuevo chocan los mismos 13: cargarlo completo falla por llave duplicada, como debe. Se corrige en la auditoría del currículo. | `16` §4 (DBA), `18` |
| **Backend I1 frente al MER** | El backend todavía guarda `email_verificado` y no tiene las tablas del catálogo: alinearlo con ADR-036 y ADR-037 es trabajo de la Fase IV. | `21` |
| **Backend I1** | Ajustar dos rutas: que `POST /auth/elegir-rol` reciba también el perfil (E-06) y que `PATCH /users/:id` quede solo para editar el perfil (E-12). Quitar del producto las rutas de la guía (`POST /users`, `GET /users`, `GET /users/:id`, `/example/*`). | `20` §3, §7 |
| **Decisiones confirmadas el 2026-10-26** (ADR-034, ADR-035) | Retomar un registro a medias al iniciar sesión (CU-06 3a); tratar un ítem generado inválido como falla del servicio (CU-16 4a); sacar `Item.estado_revision` aunque el triaje del 2026-09-04 lo había aceptado (H-5, por ADR-026); guardar el servicio y el modelo de IA una vez en la experiencia (RI-17), cuando el punto 4 de ADR-030 dice que los guarda cada ítem. | `12` §7, `16` §10 y §13 |

## 5. Notas sobre las fuentes

- **ADR.** Las decisiones están en `docs/diseno/decisiones.md` (ADR-001 a ADR-032 al hacer esta fase; ADR-033 a ADR-037 se agregaron el 2026-10-24 y 26). Las que
  citan los documentos `12` a `20` existen ahí (el 2026-10-26 se sumaron ADR-033, ADR-036 y ADR-037), y las que sostienen el MER se cotejaron con su
  texto el 2026-10-26. Hay una sola diferencia, y se declara arriba: ADR-030, punto 4, dice que
  **cada ítem** guarda qué servicio y qué modelo lo generó; el MER lo guarda una vez en la
  experiencia (RI-17), porque el punto 3 de la misma ADR —«un banco, un servicio»— hace que sea
  el mismo para todos sus ítems, y guardarlo por ítem permitía mezclar servicios en un banco. El
  propósito de la ADR (rastrear de dónde vino una pregunta y comparar los dos servicios) se
  mantiene. **Confirmado el 2026-10-26: ADR-035 modifica ADR-030, punto 4**, así que la diferencia
  quedó resuelta a favor del MER.
- **Currículo.** `data/curriculo-men/normalized/curriculo_men_normalizado.json`, en la raíz del
  repositorio: de ahí salen las evidencias y, desde ADR-036, el área, el grado y el número con que
  se arma cada `codigo_dba` (`ÁREA-GG-NN`). La versión de cada documento oficial no sale de ahí:
  sale de la tabla de ADR-033, verificada contra los archivos del MEN.
- **El borrador.** La carpeta *«Entregables de la fase 3 que fueron hechos antes de la
  finalización de la fase 2»* se usó como insumo, como dice su aviso. El MER final parte de su
  Quinta revisión y conserva su triaje de la revisión docente (H-1 a H-12); `16` §10 responde a cada hallazgo y §13 dice qué
  cambió.
- **PDF.** `herramientas/md_a_pdf.py` usa Chrome en Linux y, en Windows, Chrome o Edge (el
  primero que encuentre). Cada diagrama va en su propia hoja apaisada y entra como vector: se
  amplía sin perder nitidez. El MER entero no se lee en A4, así que va además en A1.
