# 6. Diccionario de Datos — AdaptiveLearn

> **⚠ BORRADOR ANTERIOR AL CIERRE DE LA FASE II — no es fuente de verdad.**
> Se hizo entre agosto y septiembre de 2026, mientras la Fase II seguía
> abierta. Después cambiaron decisiones que lo afectan (ADR-026 a
> ADR-029, entre otras). La fuente de verdad es la Fase I, la Fase II y
> `diseno/decisiones.md`; la Fase III se rehace en orden desde
> `10-proceso-desarrollo.md`, y este documento se usa como insumo, no como
> base. Lo que el modelo nuevo debe recibir está en `diseno/pendientes.md`,
> sección "Entrada a Fase III". *(Aviso agregado el 2026-10-21, decisión
> de Alejandro.)*

**Metodología:** MODESEC — Fase III, Diseño Computacional, tercer
entregable. MODESEC lo pide textualmente: *«un diccionario de datos
para los metadatos (como tipos, tamaños, y otras cualidades de los
campos de datos)»* (`MODESEC_TISE2009.txt`).

**Base:** `04-modelo-relacional.md`, que a su vez deriva de
`01-modelo-entidad-relacion.md` — **Quinta revisión (2026-09-08)**,
la que responde a la revisión del docente del 2026-09-01.

**Motor objetivo: MariaDB 10.11.** Los tipos concretos de este
documento son los de ese motor, que es el que el curso DSE-2 pide para
el backend. La columna equivalente en SQLite existe en
`modelo-relacional/mr_esquema.sql`, que se usa solo para la
verificación mecánica.

**Generado, no escrito a mano.** Este documento sale de
`modelo-relacional/datos_mr.py` mediante `generar.py`. No se edita
directamente: se edita la fuente y se regenera. La razón es concreta —
el 2026-09-19 se descubrió que el Modelo Relacional llevaba dos
revisiones de atraso respecto al MER sin que nadie lo notara, porque
eran dos documentos escritos a mano por separado. `_verificar_mr_mer.py`
comprueba en cada corrida que esta fuente no se aparte del MER.

---

## Resumen

| Tablas | Columnas | Llaves foráneas |
|---|---|---|
| 14 | 72 | 17 |

Reporte no aparece: no es una tabla. Es un conjunto de vistas
calculadas sobre `resultado`, sin llave ni persistencia propia —
confirmado en el MER y en el MR.

## Cómo leer cada ficha

| Columna | Qué dice |
|---|---|
| **Campo** | Nombre exacto en el esquema. |
| **Tipo (MariaDB)** | Tipo y tamaño concretos. El tamaño no es arbitrario: ver «Convenciones fijadas aquí» al final. |
| **Nulo** | Si admite `NULL`. «No» significa `NOT NULL`. |
| **Llave** | PK, FK, o UNIQUE. |
| **Dominio** | Valores admitidos, cuando están restringidos. |
| **Defecto** | Valor por defecto, si existe. |
| **Descripción y fuente** | Qué significa y de qué ADR o spec sale. |

---

## 1. `docente`

**Entidad del MER:** Docente · **Clasificación:** Propia

Quien crea y publica experiencias.

<!-- tabla:campos -->
| Campo | Tipo (MariaDB) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_docente` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Docente* |
| `nombre` | `VARCHAR(120)` | No | — | — | — | Nombre completo, como lo escribió al registrarse.<br>*Fuente: 19-spec-auth-completa-perfil.md* |
| `correo` | `VARCHAR(254)` | No | UNIQUE | formato de correo | — | Credencial de acceso.<br>*Fuente: RI-3 · 17-spec-auth-login-registro.md* |
| `avatar_url` | `VARCHAR(500)` | Sí | — | — | NULL | Foto de perfil; opcional, no bloquea el registro.<br>*Fuente: 19-spec-auth-completa-perfil.md §2.3* |

**Unicidad**

- `UNIQUE(correo)` — RI-3

## 2. `estudiante`

**Entidad del MER:** Estudiante · **Clasificación:** Propia

Quien se une a una experiencia y responde el diagnóstico.

<!-- tabla:campos -->
| Campo | Tipo (MariaDB) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_estudiante` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Estudiante* |
| `nombre` | `VARCHAR(120)` | No | — | — | — | Nombre completo.<br>*Fuente: 19-spec-auth-completa-perfil.md* |
| `correo` | `VARCHAR(254)` | No | UNIQUE | formato de correo | — | Credencial de acceso.<br>*Fuente: RI-3 · 17-spec-auth-login-registro.md* |
| `avatar_url` | `VARCHAR(500)` | Sí | — | — | NULL | Foto de perfil; opcional.<br>*Fuente: 19-spec-auth-completa-perfil.md §2.3* |

**Unicidad**

- `UNIQUE(correo)` — RI-3

## 3. `experiencia`

**Entidad del MER:** Experiencia · **Clasificación:** Propia

Un diagnóstico anclado a un único DBA, creado por un docente.

<!-- tabla:campos -->
| Campo | Tipo (MariaDB) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_experiencia` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Experiencia* |
| `id_docente` | `INT UNSIGNED` | No | FK | — | — | Docente autor. Participación total: no existe experiencia sin autor.<br>*Fuente: MER · relación «crea»* |
| `codigo_dba` | `VARCHAR(40)` | No | FK | — | — | DBA al que se ancla. Una experiencia, un solo DBA.<br>*Fuente: ADR-003 · 06-spec-crear-experiencia-paso2.md* |
| `nombre` | `VARCHAR(160)` | No | — | — | — | Título que le pone el docente.<br>*Fuente: 07-spec-crear-experiencia-paso3.md* |
| `estado` | `ENUM('Borrador','Publicada')` | No | — | Borrador \| Publicada | 'Borrador' | Borrador = banco generado, sin revisar. Publicada = visible para estudiantes.<br>*Fuente: ADR-005 · 04-spec-dashboard.md §2.3* |
| `fecha_creacion` | `DATETIME` | No | — | — | — | Cuándo se creó.<br>*Fuente: 04-spec-dashboard.md* |
| `fecha_publicacion` | `DATETIME` | Sí | — | — | NULL | Cuándo pasó a Publicada. NULL mientras siga en Borrador.<br>*Fuente: Quinta revisión del MER · 15-spec-modal-confirmar-publicar.md* |
| `codigo_invitacion` | `CHAR(6)` | No | UNIQUE | 6 caracteres alfanuméricos, sin 0 O 1 I L | — | Código que el docente dicta para que los estudiantes se unan.<br>*Fuente: RI-3 · 08-spec-unirse-codigo.md §2.3* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | Por qué esa acción |
|---|---|---|---|
| `id_docente` | `docente(id_docente)` | `RESTRICT` | Raíz: ningún flujo del sistema borra un docente. |
| `codigo_dba` | `dba(codigo_dba)` | `RESTRICT` | Raíz: dato del MEN, no se borra por razones de este sistema. |

*`ON UPDATE CASCADE` en todas, sin excepción — ver el Modelo
Relacional para el porqué.*

**Unicidad**

- `UNIQUE(codigo_invitacion)` — RI-3

**Restricciones de dominio (CHECK)**

- `codigo_invitacion no usa 0 O 1 I L, 6 posiciones` — RI-3 · 08-spec-unirse-codigo.md §2.3

## 4. `dba`

**Entidad del MER:** DBA · **Clasificación:** Externa (MEN)

Derecho Básico de Aprendizaje oficial del MEN. Dato externo, referenciado, no generado por este sistema.

<!-- tabla:campos -->
| Campo | Tipo (MariaDB) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `codigo_dba` | `VARCHAR(40)` | No | PK | — | — | Llave natural del MEN. Única llave no sustituta del modelo.<br>*Fuente: curriculo_men_normalizado.json* |
| `area` | `VARCHAR(40)` | No | — | — | — | Área curricular (Matemáticas, Lenguaje, ...).<br>*Fuente: 05-spec-crear-experiencia-paso1.md* |
| `grado` | `VARCHAR(4)` | No | — | 1° a 11° | — | Grado escolar. Sin Transición: no hay DBA de Transición en los datos reales.<br>*Fuente: 06-spec-crear-experiencia-paso2.md §2.3* |
| `enunciado` | `TEXT` | No | — | — | — | Texto oficial del DBA.<br>*Fuente: curriculo_men_normalizado.json* |
| `ejemplo` | `TEXT` | Sí | — | — | NULL | Ejemplo oficial. NULL real: el campo no existe todavía en la normalización (QA-011).<br>*Fuente: ADR-011 · QA-011* |

## 5. `evidencia`

**Entidad del MER:** Evidencia · **Clasificación:** Externa (MEN), débil

Evidencia de aprendizaje de un DBA. Entidad débil: no tiene identidad fuera de su DBA. Dato del MEN, sin juicio nuestro.

<!-- tabla:campos -->
| Campo | Tipo (MariaDB) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `codigo_dba` | `VARCHAR(40)` | No | PK,FK | — | — | DBA al que pertenece. Relación identificadora.<br>*Fuente: MER · Evidencia* |
| `numero_evidencia` | `TINYINT UNSIGNED` | No | PK | > 0 | — | Posición dentro de la lista de evidencias de ese DBA. Llave parcial.<br>*Fuente: curriculo_men_normalizado.json* |
| `enunciado` | `TEXT` | No | — | — | — | Texto oficial de la evidencia.<br>*Fuente: curriculo_men_normalizado.json* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | Por qué esa acción |
|---|---|---|---|
| `codigo_dba` | `dba(codigo_dba)` | `CASCADE` | Entidad débil: sin su DBA no tiene identidad. |

*`ON UPDATE CASCADE` en todas, sin excepción — ver el Modelo
Relacional para el porqué.*

**Restricciones de dominio (CHECK)**

- `numero_evidencia > 0` — posición dentro del DBA

## 6. `evidencia_dictamen`

**Entidad del MER:** Evidencia_Dictamen · **Clasificación:** Propia, débil

Nuestro juicio sobre una evidencia del MEN: si admite formato cerrado. Separada de `evidencia` a propósito, para no mezclar contenido oficial con criterio propio (H-6).

<!-- tabla:campos -->
| Campo | Tipo (MariaDB) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `codigo_dba` | `VARCHAR(40)` | No | PK,FK | — | — | Evidencia dictaminada (parte 1).<br>*Fuente: H-6 · Quinta revisión* |
| `numero_evidencia` | `TINYINT UNSIGNED` | No | PK,FK | — | — | Evidencia dictaminada (parte 2).<br>*Fuente: H-6 · Quinta revisión* |
| `aplica_formato_cerrado` | `BOOLEAN` | No | — | true \| false | — | Si esta evidencia se puede diagnosticar con pregunta cerrada.<br>*Fuente: ADR-006 · pendiente del censo QA-014* |
| `justificacion` | `TEXT` | Sí | — | — | NULL | Por qué se dictaminó así.<br>*Fuente: H-6 · Quinta revisión* |
| `fecha_dictamen` | `DATETIME` | No | — | — | — | Cuándo se dictaminó. Obligatoria porque el dictamen puede cambiar al cerrar QA-014.<br>*Fuente: H-6 · Quinta revisión* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | Por qué esa acción |
|---|---|---|---|
| `codigo_dba, numero_evidencia` | `evidencia(codigo_dba, numero_evidencia)` | `CASCADE` | Entidad débil: el dictamen no existe sin la evidencia dictaminada. |

*`ON UPDATE CASCADE` en todas, sin excepción — ver el Modelo
Relacional para el porqué.*

## 7. `experiencia_evidencia`

**Entidad del MER:** Experiencia_Evidencia · **Clasificación:** Asociativa

Qué evidencias del DBA anclado diagnostica realmente esta experiencia. Existe para que Ítem y Resultado cuelguen de un solo camino al currículo; elimina las reglas RI-1 y RI-2 de la versión anterior al volverlas estructura (H-4).

<!-- tabla:campos -->
| Campo | Tipo (MariaDB) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_experiencia` | `INT UNSIGNED` | No | PK,FK | — | — | Experiencia (parte 1 de la llave).<br>*Fuente: H-4 · Quinta revisión* |
| `codigo_dba` | `VARCHAR(40)` | No | PK,FK | — | — | Evidencia incluida (parte 2).<br>*Fuente: H-4 · Quinta revisión* |
| `numero_evidencia` | `TINYINT UNSIGNED` | No | PK,FK | — | — | Evidencia incluida (parte 3).<br>*Fuente: H-4 · Quinta revisión* |
| `incluida` | `BOOLEAN` | No | — | true \| false | TRUE | Si esta evidencia entra al diagnóstico de esta experiencia. Solo puede ser true si su dictamen lo permite (RI-5).<br>*Fuente: RI-5 · Quinta revisión* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | Por qué esa acción |
|---|---|---|---|
| `id_experiencia` | `experiencia(id_experiencia)` | `CASCADE` | Composición: la inclusión no significa nada sin su experiencia. |
| `codigo_dba, numero_evidencia` | `evidencia(codigo_dba, numero_evidencia)` | `RESTRICT` | Hacia el currículo del MEN: no se borra una evidencia oficial. |

*`ON UPDATE CASCADE` en todas, sin excepción — ver el Modelo
Relacional para el porqué.*

## 8. `inscripcion`

**Entidad del MER:** Inscripción · **Clasificación:** Asociativa

Un estudiante unido a una experiencia. Llave propia (no compuesta) para que Presentación y Resultado no arrastren llave doble.

<!-- tabla:campos -->
| Campo | Tipo (MariaDB) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_inscripcion` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Inscripción* |
| `id_estudiante` | `INT UNSIGNED` | No | FK | — | — | Estudiante inscrito.<br>*Fuente: MER · relación «realiza»* |
| `id_experiencia` | `INT UNSIGNED` | No | FK | — | — | Experiencia a la que se unió.<br>*Fuente: MER · relación «pertenece a»* |
| `fecha_union` | `DATETIME` | No | — | — | — | Cuándo se unió con el código.<br>*Fuente: 08-spec-unirse-codigo.md* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | Por qué esa acción |
|---|---|---|---|
| `id_estudiante` | `estudiante(id_estudiante)` | `RESTRICT` | Raíz. |
| `id_experiencia` | `experiencia(id_experiencia)` | `CASCADE` | Sin la experiencia, la inscripción no tiene objeto. |

*`ON UPDATE CASCADE` en todas, sin excepción — ver el Modelo
Relacional para el porqué.*

**Unicidad**

- `UNIQUE(id_estudiante, id_experiencia)` — RI-1
- `UNIQUE(id_inscripcion, id_experiencia)` — destino de FK — habilita la comprobación estructural de resultado

## 9. `item`

**Entidad del MER:** Ítem · **Clasificación:** Propia

Pregunta o ejercicio del banco de diagnóstico. Se genera al crear la experiencia (ADR-005); 12 por evidencia (ADR-016).

<!-- tabla:campos -->
| Campo | Tipo (MariaDB) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_item` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Ítem* |
| `id_experiencia` | `INT UNSIGNED` | No | FK | — | — | Parte 1 de la FK compuesta hacia experiencia_evidencia.<br>*Fuente: H-4 · Quinta revisión* |
| `codigo_dba` | `VARCHAR(40)` | No | FK | — | — | Parte 2 de esa misma FK compuesta.<br>*Fuente: H-4 · Quinta revisión* |
| `numero_evidencia` | `TINYINT UNSIGNED` | No | FK | — | — | Parte 3 de esa misma FK compuesta.<br>*Fuente: H-4 · Quinta revisión* |
| `enunciado` | `TEXT` | No | — | — | — | Texto de la pregunta.<br>*Fuente: ADR-014* |
| `formato` | `ENUM('single_choice','matching','ordering')` | No | — | single_choice \| matching \| ordering | 'single_choice' | Cómo se responde el ítem.<br>*Fuente: ADR-006* |
| `origen` | `ENUM('ia','editado_docente')` | No | — | ia \| editado_docente | 'ia' | Distingue un ítem tal como lo generó la IA de uno que el docente intervino. Fase I §2 eleva esa distincion a valor del proyecto.<br>*Fuente: H-5 · ADR-015 · Quinta revisión* |
| `estado_revision` | `VARCHAR(30)` | No | — | VOCABULARIO SIN DECIDIR (V-7) | 'sin_revisar' | Si el docente ya revisó este ítem. ADR-005 exige la revisión previa. **El vocabulario exacto de estados sigue sin decidirse (V-7)** — el tipo queda VARCHAR y no ENUM justamente por eso.<br>*Fuente: H-5 · ADR-005 · V-7 abierto* |
| `excluido` | `BOOLEAN` | No | — | true \| false | FALSE | Si es true el ítem no se muestra, pero sigue en el banco. Reversible.<br>*Fuente: ADR-015* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | Por qué esa acción |
|---|---|---|---|
| `id_experiencia, codigo_dba, numero_evidencia` | `experiencia_evidencia(id_experiencia, codigo_dba, numero_evidencia)` | `CASCADE` | UNA sola FK compuesta, no dos sueltas: es lo que hace estructural la coherencia que antes exigía RI-1. |

*`ON UPDATE CASCADE` en todas, sin excepción — ver el Modelo
Relacional para el porqué.*

## 10. `opcion`

**Entidad del MER:** Opción · **Clasificación:** Propia

Opción de respuesta de un ítem. Qué columnas aplican depende del formato del ítem (RI-4).

<!-- tabla:campos -->
| Campo | Tipo (MariaDB) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_opcion` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Opción* |
| `id_item` | `INT UNSIGNED` | No | FK | — | — | Ítem al que pertenece.<br>*Fuente: MER · relación «ofrece»* |
| `texto` | `TEXT` | No | — | — | — | Texto de la opción.<br>*Fuente: ADR-014* |
| `orden` | `TINYINT UNSIGNED` | Sí | — | según el formato (RI-4) | NULL | En `ordering`: la posición correcta. En `matching`: número de pareja. NULL en `single_choice`.<br>*Fuente: ADR-014 · RI-4* |
| `es_correcta` | `BOOLEAN` | Sí | — | según el formato (RI-4) | NULL | Solo aplica a `single_choice`. NULL en los otros dos formatos.<br>*Fuente: ADR-014 · RI-4* |
| `grupo` | `ENUM('izquierda','derecha')` | Sí | — | izquierda \| derecha, solo en matching | NULL | Solo aplica a `matching`: de qué lado del emparejamiento está.<br>*Fuente: ADR-014 · RI-4* |
| `hipotesis_error` | `TEXT` | Sí | — | — | NULL | Por qué un estudiante podría elegir esta opción incorrecta. No se le muestra al estudiante ni se reporta (ADR-008).<br>*Fuente: ADR-020* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | Por qué esa acción |
|---|---|---|---|
| `id_item` | `item(id_item)` | `CASCADE` | Composición pura; protegida aguas arriba por el RESTRICT de presentación. |

*`ON UPDATE CASCADE` en todas, sin excepción — ver el Modelo
Relacional para el porqué.*

## 11. `presentacion`

**Entidad del MER:** Presentación · **Clasificación:** Propia, débil

El hecho de HABER MOSTRADO un ítem a un estudiante — distinto del hecho de haberlo respondido. Sin esta tabla, «se le mostró y no respondió» es indistinguible de «nunca se le mostró» (H-3), y la secuencia adaptativa de ADR-016 no se puede reconstruir (H-2).

<!-- tabla:campos -->
| Campo | Tipo (MariaDB) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_inscripcion` | `INT UNSIGNED` | No | PK,FK | — | — | A quién se le mostró (parte 1 de la llave).<br>*Fuente: H-2/H-3 · Quinta revisión* |
| `id_item` | `INT UNSIGNED` | No | PK,FK | — | — | Qué ítem se mostró (parte 2 de la llave).<br>*Fuente: H-2/H-3 · Quinta revisión* |
| `orden_presentacion` | `TINYINT UNSIGNED` | No | — | > 0, único por inscripción y evidencia (RI-8) | — | En qué lugar de la secuencia se mostró. Es el dato que permite reconstruir la secuencia adaptativa.<br>*Fuente: RI-8 · ADR-016* |
| `fecha_presentacion` | `DATETIME` | No | — | — | — | Cuándo se mostró.<br>*Fuente: H-2 · Quinta revisión* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | Por qué esa acción |
|---|---|---|---|
| `id_inscripcion` | `inscripcion(id_inscripcion)` | `CASCADE` | Sin la inscripción no hay a quién se le mostró. |
| `id_item` | `item(id_item)` | `RESTRICT` | PROTECCIÓN REAL: mientras exista el registro de que un ítem se mostró, ese ítem no se puede borrar. Refuerza ADR-015 y RI-10 a nivel de esquema. |

*`ON UPDATE CASCADE` en todas, sin excepción — ver el Modelo
Relacional para el porqué.*

**Restricciones de dominio (CHECK)**

- `orden_presentacion > 0` — RI-8

## 12. `respuesta`

**Entidad del MER:** Respuesta · **Clasificación:** Asociativa

Lo que el estudiante respondió a un ítem que se le presentó, con su nivel de certeza. Cuelga de la Presentación, no de Inscripción e Ítem por separado.

<!-- tabla:campos -->
| Campo | Tipo (MariaDB) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_respuesta` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Respuesta* |
| `id_inscripcion` | `INT UNSIGNED` | No | FK | — | — | Parte 1 de la FK compuesta hacia presentación.<br>*Fuente: H-3 · Quinta revisión* |
| `id_item` | `INT UNSIGNED` | No | FK | — | — | Parte 2 de esa misma FK compuesta.<br>*Fuente: H-3 · Quinta revisión* |
| `certeza` | `TINYINT UNSIGNED` | No | — | 0 a 5 (CRI) | — | Certainty of Response Index (Hasan et al. 1999). Es la senal de la que depende toda la regla adaptativa.<br>*Fuente: ADR-008 punto 2* |
| `fecha_respuesta` | `DATETIME` | No | — | — | — | Cuándo se envió. Cierra V-1: sin esto la secuencia adaptativa no se puede ordenar ni auditar.<br>*Fuente: H-2 · Quinta revisión · cierra V-1* |
| `correcta` | `BOOLEAN` | No | — | true \| false | — | DERIVADO Y PERSISTIDO (ADR-021): se calcula comparando respuesta_opcion contra las opciones reales, y se escribe una sola vez, al registrar la respuesta. No se recalcula al leer.<br>*Fuente: ADR-019 · ADR-021* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | Por qué esa acción |
|---|---|---|---|
| `id_inscripcion, id_item` | `presentacion(id_inscripcion, id_item)` | `CASCADE` | UNA sola FK compuesta hacia el hecho de haberse presentado. Una respuesta sin presentación previa es imposible por estructura. |

*`ON UPDATE CASCADE` en todas, sin excepción — ver el Modelo
Relacional para el porqué.*

**Unicidad**

- `UNIQUE(id_inscripcion, id_item)` — una presentación, una respuesta

**Restricciones de dominio (CHECK)**

- `certeza BETWEEN 0 AND 5` — ADR-008 punto 2 (CRI)

## 13. `respuesta_opcion`

**Entidad del MER:** Respuesta_Opción · **Clasificación:** Asociativa

Qué opción u opciones eligió el estudiante — no solo si acertó. Sin esta tabla, `matching` y `ordering` no son representables.

<!-- tabla:campos -->
| Campo | Tipo (MariaDB) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_respuesta` | `INT UNSIGNED` | No | PK,FK | — | — | Respuesta a la que pertenece (parte 1).<br>*Fuente: ADR-019* |
| `id_opcion` | `INT UNSIGNED` | No | PK,FK | — | — | Opción elegida (parte 2).<br>*Fuente: ADR-019* |
| `valor_dado` | `TINYINT UNSIGNED` | Sí | — | según el formato del ítem | NULL | `single_choice`: NULL, la fila ya es la elección. `ordering`: la posición que le asignó. `matching`: el número de pareja.<br>*Fuente: ADR-019* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | Por qué esa acción |
|---|---|---|---|
| `id_respuesta` | `respuesta(id_respuesta)` | `CASCADE` | Sin la respuesta, la selección no tiene sentido. |
| `id_opcion` | `opcion(id_opcion)` | `RESTRICT` | Protege el historial de qué eligió el estudiante. |

*`ON UPDATE CASCADE` en todas, sin excepción — ver el Modelo
Relacional para el porqué.*

## 14. `resultado`

**Entidad del MER:** Resultado · **Clasificación:** Propia, débil

Lo que las respuestas de un estudiante permiten concluir sobre UNA evidencia DE ESTA experiencia. Fotografía persistida, no recalculada al vuelo.

<!-- tabla:campos -->
| Campo | Tipo (MariaDB) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_inscripcion` | `INT UNSIGNED` | No | PK,FK | — | — | De quién es el resultado (parte 1 de la llave).<br>*Fuente: MER · relación «arroja»* |
| `id_experiencia` | `INT UNSIGNED` | No | FK | — | — | COLUMNA REDUNDANTE DELIBERADA, decidida en este MR porque el MER se la delegó explícitamente. Permite que las DOS reglas de coherencia sean estructurales en vez de triggers — ver la sección de FK del documento.<br>*Fuente: MER · Resultado (delegación explícita al MR)* |
| `codigo_dba` | `VARCHAR(40)` | No | PK,FK | — | — | Evidencia medida (parte 2 de la llave).<br>*Fuente: H-4 · Quinta revisión* |
| `numero_evidencia` | `TINYINT UNSIGNED` | No | PK,FK | — | — | Evidencia medida (parte 3 de la llave).<br>*Fuente: H-4 · Quinta revisión* |
| `estado` | `ENUM('muestra','no_muestra','no_concluyente')` | No | — | muestra \| no_muestra \| no_concluyente | — | DERIVADO Y PERSISTIDO (ADR-021). Nunca una certeza; nunca un valor que se edite a mano.<br>*Fuente: ADR-008 punto 4 · ADR-021* |
| `fecha_calculo` | `DATETIME` | No | — | — | — | Cuándo se calculó `estado`. Obligatoria: una fotografía sin fecha no es auditable. Cierra V-4.<br>*Fuente: ADR-021 · cierra V-4* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | Por qué esa acción |
|---|---|---|---|
| `id_inscripcion, id_experiencia` | `inscripcion(id_inscripcion, id_experiencia)` | `CASCADE` | FK compuesta contra un UNIQUE de inscripción: fuerza que la experiencia del resultado sea la de su inscripción. Estructural, sin trigger. |
| `id_experiencia, codigo_dba, numero_evidencia` | `experiencia_evidencia(id_experiencia, codigo_dba, numero_evidencia)` | `RESTRICT` | Fuerza que la evidencia medida sea una de las que ESA experiencia incluye. Junto con la FK anterior, elimina por estructura la vieja RI-2. |

*`ON UPDATE CASCADE` en todas, sin excepción — ver el Modelo
Relacional para el porqué.*

---

## Lo que este diccionario declara como no resuelto

Un diccionario que inventa un tipo para un campo cuyo dominio todavía
no se decidió afirma más de lo que el proyecto sostiene. Estos casos
quedan marcados, no rellenados:

| Campo | Qué falta | Dónde está declarado |
|---|---|---|
| `item.estado_revision` | El vocabulario exacto de estados. Por eso el tipo es `VARCHAR(30)` y **no** un `ENUM`: poner un ENUM aquí sería fijar por la puerta de atrás una decisión que nadie tomó. | **V-7**, MER |
| `resultado.estado` | El tipo sí está cerrado, pero **la función que lo calcula no**: qué combinación exacta de `correcta` × `certeza` cuenta como señal fuerte. | **V-5**, MER (hallazgo H-7 del docente) |
| `dba.ejemplo` | Admite `NULL` porque el campo todavía no existe en la normalización del currículo. No es opcionalidad de diseño, es un dato que falta. | **QA-011** |

## Convenciones fijadas aquí

- **Identificadores:** `INT UNSIGNED AUTO_INCREMENT`. Un `INT UNSIGNED`
  llega a 4.294.967.295 filas — muy por encima de cualquier escala
  realista de este sistema, y ocupa la mitad que un `BIGINT`.
- **`VARCHAR(254)` para correo:** es el máximo que admite una dirección
  de correo según RFC 5321. No es un número redondeado a ojo.
- **`CHAR(6)` para el código de invitación:** longitud fija y conocida
  (`08-spec-unirse-codigo.md` §2.3). `CHAR` y no `VARCHAR` porque nunca
  varía.
- **`TINYINT UNSIGNED` para `certeza`, `numero_evidencia`,
  `orden_presentacion`, `orden` y `valor_dado`:** ninguno pasa de 255
  por definición (la escala CRI llega a 5; el tope de ítems por
  evidencia es 6, ADR-016).
- **`TEXT` para todo enunciado:** los textos del MEN no tienen longitud
  acotada conocida, y truncarlos sería alterar contenido oficial.
- **`DATETIME` y no `TIMESTAMP`:** `TIMESTAMP` en MariaDB tiene el
  límite del año 2038 y conversión automática de zona horaria; ninguna
  de las dos cosas se necesita aquí.
- **`ENUM` donde el dominio está cerrado y decidido**; `VARCHAR` con
  `CHECK` donde no lo está (ver la tabla de arriba).

