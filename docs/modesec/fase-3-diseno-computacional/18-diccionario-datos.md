# 18. Diccionario de Datos — AdaptiveLearn

**Metodología:** MODESEC — Fase III, Diseño Computacional. Último
entregable del modelado de la base de datos. MODESEC lo pide
textualmente: *«un diccionario de datos para los metadatos (como tipos,
tamaños, y otras cualidades de los campos de datos)»*
(`MODESEC_TISE2009.txt`).

**Base:** `17-modelo-relacional.md`, que deriva de
`16-modelo-entidad-relacion.md` — el MER final de la Fase III, hecho
con la Fase II cerrada y el análisis de requerimientos
(`11-analisis-requerimientos.md`) como fuente.

**Motor objetivo: MySQL 8** (RNF-14: *«NestJS y MySQL»*). Los tipos de
este documento son los de ese motor, y no usan nada que MariaDB 10.11
no tenga: el backend del incremento I1 hoy corre sobre MariaDB y debe
aceptarlo igual. El esquema ejecutable es
`modelo-relacional/mr_mysql.sql`, **probado contra MySQL 8 real** (8.4 y 8.0)
(ver `17-modelo-relacional.md`, «Verificación mecánica»). La columna
equivalente en SQLite vive en `modelo-relacional/mr_esquema.sql`, que
se usa solo para la verificación automática.

**Generado, no escrito a mano.** Este documento sale de
`modelo-relacional/datos_mr.py` mediante `generar.py`. No se edita
directamente: se edita la fuente y se regenera. La razón es concreta —
el 2026-09-19 se descubrió que el Modelo Relacional llevaba dos
revisiones de atraso respecto al MER sin que nadie lo notara, porque
eran dos documentos escritos a mano por separado. `_verificar_mr_mer.py`
comprueba en cada corrida que esta fuente no se aparte del MER.

---

## Resumen

| Tablas | Columnas | Llaves foráneas | UNIQUE | CHECK |
|---|---|---|---|---|
| 19 | 108 | 24 | 17 | 16 |

Reporte no aparece: no es una tabla. Se calcula sobre `resultado` cada
vez que el docente lo abre, sin llave ni persistencia propia — así lo
declara el MER y así lo implementa el MR.

## Cómo leer cada ficha

| Columna | Qué dice |
|---|---|
| **Campo** | Nombre exacto en el esquema. |
| **Tipo (MySQL)** | Tipo y tamaño concretos. El tamaño no es arbitrario: ver «Convenciones fijadas aquí» al final. |
| **Nulo** | Si admite `NULL`. «No» significa `NOT NULL`. |
| **Llave** | PK, FK, o UNIQUE. |
| **Dominio** | Valores admitidos, cuando están restringidos. |
| **Defecto** | Valor por defecto, si existe. |
| **Descripción y fuente** | Qué significa y de qué RF, ADR o spec sale. |

---

## 1. `credencial`

**Entidad del MER:** Credencial · **Clasificación:** Propia

La cuenta de acceso: con qué correo y qué método se entra, la verificación del correo y a qué rol da acceso. Existe desde «Crear cuenta», antes de que exista la fila de docente o de estudiante, que se crea al elegir el rol (ventana 017). Es la tabla que el incremento I1 ya construyó (`backend/sql/`).

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_credencial` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Credencial* |
| `id_docente` | `INT UNSIGNED` | Sí | FK | — | NULL | Docente al que da acceso. NULL mientras el registro está en curso o si el rol es estudiante. Nunca a la vez que `id_estudiante` (RI-12).<br>*Fuente: MER · relación «accede como» · 20-spec-auth-elige-rol.md* |
| `id_estudiante` | `INT UNSIGNED` | Sí | FK | — | NULL | Estudiante al que da acceso. Mismas reglas que `id_docente`.<br>*Fuente: MER · relación «accede como» · 20-spec-auth-elige-rol.md* |
| `correo` | `VARCHAR(254)` | No | UNIQUE | formato de correo | — | Correo de la cuenta. Único entre los dos roles: no hay dos cuentas con el mismo correo, ni con métodos distintos (RF-01-04).<br>*Fuente: RI-3 · RF-01-04 · 17-spec-auth-login-registro.md* |
| `proveedor` | `ENUM('correo','google','microsoft')` | No | — | correo \| google \| microsoft | — | Método con el que se creó la cuenta. No se vinculan métodos: se avisa cuál usar (RF-01-04). Sin Apple.<br>*Fuente: RF-01-01 · RF-01-02 · 17-spec-auth-login-registro.md §2.8* |
| `password_hash` | `VARCHAR(255)` | Sí | — | hash de contraseña | NULL | Contraseña con función de hash; nunca en texto legible (RNF-08). NULL si la cuenta entra con Google o Microsoft (RI-15).<br>*Fuente: RNF-08 · RF-01-01 · 26-spec-modal-mi-perfil.md* |
| `proveedor_id` | `VARCHAR(255)` | Sí | — | — | NULL | Identificador de la persona en Google o Microsoft. NULL si `proveedor` es `correo` (RI-15).<br>*Fuente: RF-01-02* |
| `estado_verificacion` | `ENUM('procesando','verificado')` | No | — | procesando \| verificado | 'procesando' | `procesando`: se envió el código y todavía no se confirma. `verificado`: se confirmó con el código. Con Google o Microsoft nace `verificado`: lo verificó el proveedor (RI-15). Reemplaza al antiguo sí/no `email_verificado`.<br>*Fuente: ADR-037 · RF-01-03 · 18-spec-auth-verifica-correo.md* |
| `es_admin` | `BOOLEAN` | No | — | 0 \| 1 | 0 | Marca de administrador de la guía del docente: da acceso a `/users`. Falsa por defecto; solo se pone por SQL, ninguna ruta la asigna. No es un rol del producto: ninguna pantalla la usa.<br>*Fuente: ADR-040 · guía JWT del docente v2, prueba 4* |
| `nombre_completo` | `VARCHAR(240)` | Sí | — | — | NULL | El nombre que la persona escribió al registrarse (`fullName` de la guía). Sirve para mostrarla y para proponer nombres y apellidos al completar el perfil; los nombres oficiales viven en `docente` o `estudiante` (ventana 016).<br>*Fuente: ADR-040 · guía JWT del docente v2, §2 · 19-spec-auth-completa-perfil.md* |
| `intentos_login` | `TINYINT UNSIGNED` | No | — | >= 0 | 0 | Intentos de inicio de sesión fallidos seguidos.<br>*Fuente: RF-01-07 · backend I1, sql/002 · encargo 03* |
| `bloqueado_hasta` | `DATETIME` | Sí | — | — | NULL | Si se superó el límite de intentos (5), hasta cuándo no se admite iniciar sesión (15 minutos).<br>*Fuente: RF-01-07 · backend I1, sql/002* |
| `creado_en` | `DATETIME` | No | — | — | CURRENT_TIMESTAMP | Cuándo se creó la cuenta.<br>*Fuente: MER · Credencial · backend I1* |
| `actualizado_en` | `DATETIME` | No | — | — | CURRENT_TIMESTAMP | Última modificación. En MySQL se actualiza sola (ON UPDATE).<br>*Fuente: backend I1, sql/002* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |
|---|---|---|---|---|
| `id_docente` | `docente(id_docente)` | `RESTRICT` | `RESTRICT` | Raíz: ningún flujo borra un docente. Sin ON UPDATE CASCADE: MySQL no admite un CHECK sobre una columna con acción referencial, y aquí lo hay (RI-12). |
| `id_estudiante` | `estudiante(id_estudiante)` | `RESTRICT` | `RESTRICT` | Igual que la anterior. |

**Unicidad**

- `UNIQUE(correo)` — RI-3 · RF-01-04: una cuenta por correo, entre los dos roles
- `UNIQUE(id_docente)` — una credencial por docente (1:1)
- `UNIQUE(id_estudiante)` — una credencial por estudiante (1:1)
- `UNIQUE(proveedor, proveedor_id)` — RF-01-04: una misma cuenta de Google o Microsoft no abre dos credenciales

**Restricciones de dominio (CHECK)**

- `id_docente IS NULL OR id_estudiante IS NULL` — una credencial accede como un solo rol. *RI-12 · 20-spec-auth-elige-rol.md*
- `(proveedor = 'correo' AND password_hash IS NOT NULL AND proveedor_id IS NULL) OR (proveedor <> 'correo' AND password_hash IS NULL AND proveedor_id IS NOT NULL AND estado_verificacion = 'verificado')` — contraseña solo con correo; identificador externo y correo verificado solo con Google o Microsoft. *RI-15 · RF-01-01 · RF-01-02*

## 2. `codigo_verificacion`

**Entidad del MER:** Codigo_Verificacion · **Clasificación:** Propia, débil

El código de 6 dígitos que se envía por correo para verificar la cuenta (ventana 015) o para recuperar la contraseña (ventana 018). Entidad débil de la credencial: a lo sumo uno por credencial y propósito; uno nuevo reemplaza al anterior. El vencimiento (10 min) y la espera para reenviar (30 s) se calculan desde `creado_en`. La tarea nocturna borra los vencidos (ADR-039).

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_credencial` | `INT UNSIGNED` | No | PK,FK | — | — | Credencial que lo recibió. Relación identificadora «recibe».<br>*Fuente: MER · relación «recibe» · ADR-039* |
| `proposito` | `ENUM('verificar_correo','recuperar_contrasena')` | No | PK | verificar_correo \| recuperar_contrasena | — | Para qué es el código. Llave parcial: un código vigente por propósito.<br>*Fuente: ADR-039 · RF-01-03 · RF-01-08* |
| `codigo_hash` | `CHAR(64) CHARACTER SET ascii COLLATE ascii_bin` | No | — | 64 caracteres hexadecimales | — | HMAC-SHA256 del código, en hexadecimal. El código nunca se guarda legible: quien lea la tabla no puede usarlo (RNF-08).<br>*Fuente: ADR-039 · RNF-08* |
| `creado_en` | `DATETIME` | No | — | — | CURRENT_TIMESTAMP | Cuándo se envió. Vence a los 10 minutos y se puede reenviar a los 30 segundos: los dos se calculan desde aquí, no se guardan.<br>*Fuente: ADR-039 · nota R4 · RF-01-03* |
| `intentos` | `TINYINT UNSIGNED` | No | — | 0 a 5 | 0 | Intentos fallidos con este código. Al quinto, el código deja de servir y hay que pedir otro (fuerza bruta: RNF-07).<br>*Fuente: ADR-039 · RNF-07* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |
|---|---|---|---|---|
| `id_credencial` | `credencial(id_credencial)` | `CASCADE` | `CASCADE` | Entidad débil: un código no existe sin su credencial. Borrar la credencial (tarea nocturna, ADR-039) borra sus códigos. |

**Restricciones de dominio (CHECK)**

- `intentos <= 5` — a lo sumo 5 intentos fallidos por código. *ADR-039 · RNF-07*
- `codigo_hash REGEXP '^[0-9a-f]{64}$'` — el hash es hexadecimal de 64 caracteres: un código de 6 dígitos sin hash no cabe. *ADR-039 · RNF-08*

## 3. `docente`

**Entidad del MER:** Docente · **Clasificación:** Propia

Quien crea y publica experiencias. Se crea al elegir el rol Docente (ventana 017); el rol no cambia después.

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_docente` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Docente* |
| `nombres` | `VARCHAR(120)` | No | — | no vacío | — | Nombres. Obligatorio.<br>*Fuente: RF-01-05 · 19-spec-auth-completa-perfil.md §2.3* |
| `apellidos` | `VARCHAR(120)` | No | — | no vacío | — | Apellidos. Obligatorio.<br>*Fuente: RF-01-05 · 19-spec-auth-completa-perfil.md §2.4* |
| `avatar_url` | `VARCHAR(500)` | Sí | — | JPG o PNG, ≤ 5 MB | NULL | Foto de perfil; opcional. Se reemplaza, no se quita (ventana 026).<br>*Fuente: RF-01-05 · RF-01-11 · 26-spec-modal-mi-perfil.md* |

**Restricciones de dominio (CHECK)**

- `TRIM(nombres) <> '' AND TRIM(apellidos) <> ''` — nombres y apellidos no vacíos. *RF-01-05*

## 4. `estudiante`

**Entidad del MER:** Estudiante · **Clasificación:** Propia

Quien se une a una experiencia y responde el diagnóstico. Solo los datos mínimos (ADR-029): nombres, apellidos, foto opcional; el correo está en su credencial.

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_estudiante` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Estudiante* |
| `nombres` | `VARCHAR(120)` | No | — | no vacío | — | Nombres. Obligatorio.<br>*Fuente: RF-01-05 · ADR-029* |
| `apellidos` | `VARCHAR(120)` | No | — | no vacío | — | Apellidos. Obligatorio.<br>*Fuente: RF-01-05 · ADR-029* |
| `avatar_url` | `VARCHAR(500)` | Sí | — | JPG o PNG, ≤ 5 MB | NULL | Foto de perfil; opcional.<br>*Fuente: RF-01-05 · ADR-029* |

**Restricciones de dominio (CHECK)**

- `TRIM(nombres) <> '' AND TRIM(apellidos) <> ''` — nombres y apellidos no vacíos. *RF-01-05*

## 5. `experiencia`

**Entidad del MER:** Experiencia · **Clasificación:** Propia

Un diagnóstico anclado a un único DBA, creado por un docente. Se guarda solo si su banco se generó completo (ADR-027).

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_experiencia` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Experiencia* |
| `id_docente` | `INT UNSIGNED` | No | FK | — | — | Docente autor. Participación total: no existe experiencia sin autor.<br>*Fuente: MER · relación «crea»* |
| `codigo_dba` | `VARCHAR(9) CHARACTER SET ascii COLLATE ascii_bin` | No | FK | — | — | DBA al que se ancla. Una experiencia, un solo DBA.<br>*Fuente: RF-02-02 · 06-spec-crear-experiencia-paso2.md* |
| `nombre` | `VARCHAR(160)` | No | — | no vacío | — | Título; llega prellenado con el enunciado del DBA y es editable.<br>*Fuente: RF-02-02 · 07-spec-crear-experiencia-paso3.md* |
| `estado` | `ENUM('Borrador','Publicada')` | No | — | Borrador \| Publicada | 'Borrador' | Borrador = el banco se puede editar. Publicada = banco congelado y visible para estudiantes. No hay vuelta atrás (ADR-026).<br>*Fuente: RF-02-05 · ADR-026 · 04-spec-dashboard.md* |
| `fecha_creacion` | `DATETIME` | No | — | — | — | Cuándo se creó.<br>*Fuente: RF-02-04 · 09-spec-vista-interna-marco.md* |
| `fecha_publicacion` | `DATETIME` | Sí | — | NULL ⇔ Borrador (RI-16) | NULL | Cuándo pasó a Publicada. NULL mientras siga en Borrador.<br>*Fuente: RF-02-05 · 15-spec-modal-confirmar-publicar.md* |
| `codigo_invitacion` | `CHAR(6)` | No | UNIQUE | 6 caracteres, sin 0 O 1 I L | — | Código para unirse. Se genera al crear la experiencia y se muestra solo cuando está publicada. Sin distinguir mayúsculas.<br>*Fuente: RI-3 · RF-02-06 · 08-spec-unirse-codigo.md §2.3* |
| `servicio_ia` | `ENUM('gemini','deepseek')` | No | — | gemini \| deepseek | — | Servicio de IA que generó el banco: el principal, o el de respaldo si el principal falló. Un banco sale entero de un solo servicio (RF-03-02), así que es un dato del banco y no de cada ítem: el de un ítem de origen ia o editado_docente es este (RI-17). El docente no lo ve.<br>*Fuente: RF-03-02 · RF-03-03 · ADR-030* |
| `modelo_ia` | `VARCHAR(80)` | No | — | — | — | Qué modelo de ese servicio generó el banco.<br>*Fuente: RF-03-03 · ADR-030* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |
|---|---|---|---|---|
| `id_docente` | `docente(id_docente)` | `RESTRICT` | `CASCADE` | Raíz: ningún flujo del sistema borra un docente. |
| `codigo_dba` | `dba(codigo_dba)` | `RESTRICT` | `CASCADE` | Raíz: dato del MEN, no se borra por razones de este sistema. |

**Unicidad**

- `UNIQUE(codigo_invitacion)` — RI-3
- `UNIQUE(id_experiencia, codigo_dba)` — destino de FK: habilita la comprobación estructural de RI-18

**Restricciones de dominio (CHECK)**

- `(estado = 'Borrador' AND fecha_publicacion IS NULL) OR (estado = 'Publicada' AND fecha_publicacion IS NOT NULL)` — fecha de publicación solo si está Publicada. *RI-16 · RF-02-05*
- `codigo_invitacion REGEXP '^[ABCDEFGHJKMNPQRSTUVWXYZ23456789]{6}$'` — 6 caracteres de letras y números, sin 0 O 1 I L. *RI-3 · RF-02-06*

## 6. `area`

**Entidad del MER:** Área · **Clasificación:** Externa (MEN)

Área del currículo con DBA en esta versión: las 4 de ADR-033. Dato de referencia, de solo lectura (SUB-06). Se carga con el catálogo.

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `codigo_area` | `VARCHAR(3) CHARACTER SET ascii COLLATE ascii_bin` | No | PK | MAT \| LEN \| CN \| CS | — | Código del área, sin tildes: Matemáticas `MAT`, Lenguaje `LEN`, Ciencias Naturales `CN`, Ciencias Sociales `CS`. Encabeza el código de cada DBA (RI-21).<br>*Fuente: ADR-036 · ADR-033* |
| `nombre` | `VARCHAR(40)` | No | UNIQUE | no vacío | — | Nombre del área, como lo escribe el MEN.<br>*Fuente: ADR-036 · 05-spec-crear-experiencia-paso1.md* |

**Unicidad**

- `UNIQUE(nombre)` — dos áreas no se llaman igual

**Restricciones de dominio (CHECK)**

- `codigo_area REGEXP '^[A-Z]{2,3}$'` — 2 o 3 letras mayúsculas, sin tildes (en MySQL la columna es ASCII binaria: una tilde no cabe y el REGEXP distingue mayúsculas). *ADR-036*

## 7. `grado`

**Entidad del MER:** Grado · **Clasificación:** Externa (MEN)

Grado de la educación básica y media, de 1° a 11°. Sin Transición (ADR-033). Dato de referencia, de solo lectura.

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `numero` | `TINYINT UNSIGNED` | No | PK | 1 a 11 | — | Número del grado. Va, con dos cifras, en el código de cada DBA (RI-21).<br>*Fuente: ADR-036 · ADR-033* |
| `nombre` | `VARCHAR(20)` | No | UNIQUE | Primero a Undécimo | — | Nombre del grado.<br>*Fuente: ADR-036* |
| `nivel` | `ENUM('basica_primaria','basica_secundaria','media')` | No | — | basica_primaria \| basica_secundaria \| media | — | Nivel de la educación formal: básica primaria (1° a 5°), básica secundaria (6° a 9°) o media (10° y 11°). Un CHECK lo ata al número.<br>*Fuente: ADR-036 · Ley 115 de 1994* |

**Unicidad**

- `UNIQUE(nombre)` — dos grados no se llaman igual

**Restricciones de dominio (CHECK)**

- `(numero BETWEEN 1 AND 5 AND nivel = 'basica_primaria') OR (numero BETWEEN 6 AND 9 AND nivel = 'basica_secundaria') OR (numero BETWEEN 10 AND 11 AND nivel = 'media')` — grados 1 a 11, sin Transición, y el nivel que les da la Ley 115. *ADR-036 · ADR-033 · Ley 115 de 1994*

## 8. `documento_oficial`

**Entidad del MER:** Documento_Oficial · **Clasificación:** Externa (MEN)

El PDF del MEN del que se copiaron los DBA de un área. Uno por área en esta versión, con los datos que ADR-033 verificó contra los archivos oficiales: la versión se lee del documento, nunca del nombre del archivo.

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_documento` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Documento_Oficial* |
| `codigo_area` | `VARCHAR(3) CHARACTER SET ascii COLLATE ascii_bin` | No | FK | — | — | Área cuyos DBA trae el documento.<br>*Fuente: MER · relación «es de» · ADR-036* |
| `titulo` | `VARCHAR(200)` | No | — | no vacío | — | Título del documento.<br>*Fuente: ADR-036* |
| `version` | `VARCHAR(10)` | No | — | como la escribe el documento, ej. `V.2` | — | Versión que dice la portada del documento. Ciencias Sociales es `V.1` aunque su archivo se llame «v2» (ADR-033).<br>*Fuente: ADR-033 · ADR-036* |
| `anio` | `SMALLINT UNSIGNED` | No | — | — | — | Año de publicación. Los cuatro de esta versión, 2016.<br>*Fuente: ADR-033* |
| `paginas` | `SMALLINT UNSIGNED` | No | — | > 0 | — | Número de páginas del PDF oficial.<br>*Fuente: ADR-033* |
| `url_oficial` | `VARCHAR(500)` | No | — | dirección en Colombia Aprende | — | Dónde publica hoy el MEN ese documento.<br>*Fuente: ADR-033 · ADR-036* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |
|---|---|---|---|---|
| `codigo_area` | `area(codigo_area)` | `RESTRICT` | `RESTRICT` | Raíz: el catálogo no se borra por razones de este sistema. |

**Unicidad**

- `UNIQUE(codigo_area, version)` — una misma versión de un área se carga una sola vez (ADR-033, punto 4)
- `UNIQUE(id_documento, codigo_area)` — destino de FK: habilita la comprobación estructural de RI-20

**Restricciones de dominio (CHECK)**

- `paginas > 0 AND TRIM(titulo) <> '' AND TRIM(version) <> ''` — título y versión no vacíos; al menos una página. *ADR-036*

## 9. `dba`

**Entidad del MER:** DBA · **Clasificación:** Externa (MEN)

Derecho Básico de Aprendizaje oficial del MEN. Dato externo, de solo lectura para los usuarios (SUB-06). El área y el grado ya no son texto: son llaves foráneas hacia `area` y `grado` (ADR-036).

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `codigo_dba` | `VARCHAR(9) CHARACTER SET ascii COLLATE ascii_bin` | No | PK | `ÁREA-GG-NN` (RI-21) | — | Código del DBA: código del área, grado y número del DBA con dos cifras, sin tildes (`MAT-01-01`, `CS-11-05`). Se arma con el área, el grado y el `numero` de cada registro de `curriculo_men_normalizado.json`; reemplaza al identificador viejo (`matemáticas_1_dba_1` → `MAT-01-01`). Los datos de hoy repiten 13 identificadores: se corrige en la auditoría (A12), no aquí.<br>*Fuente: ADR-036 · curriculo_men_normalizado.json · RF-06-01* |
| `codigo_area` | `VARCHAR(3) CHARACTER SET ascii COLLATE ascii_bin` | No | FK | — | — | Área del DBA. Está también en la FK hacia su documento: obliga a que el documento sea de esta misma área (RI-20).<br>*Fuente: MER · relación «pertenece a» · ADR-036* |
| `numero_grado` | `TINYINT UNSIGNED` | No | FK | — | — | Grado del DBA. Se llama `numero_grado` y no `numero` para no confundirlo con el número del DBA, que va al final del código.<br>*Fuente: MER · relación «corresponde a» · ADR-036* |
| `id_documento` | `INT UNSIGNED` | No | FK | — | — | Documento oficial del que se copió.<br>*Fuente: MER · relación «se copia de» · ADR-036* |
| `enunciado` | `TEXT` | No | — | — | — | Texto oficial, sin simplificar ni reescribir.<br>*Fuente: RF-06-01* |
| `ejemplo` | `TEXT` | Sí | — | — | NULL | Ejemplo oficial; se usa como contexto al generar el banco (ADR-011). NULL cuando el PDF no trae ejemplo con texto: la mayoría de los DBA de Ciencias Sociales V.1 no tienen ejemplo, y algunos de Ciencias Naturales son solo una figura (encargo 05).<br>*Fuente: RF-06-01 · ADR-011 · QA-011* |
| `ejemplo_tiene_imagen` | `BOOLEAN` | No | — | 0 \| 1 | 0 | Si el ejemplo del PDF incluye una figura (imagen, dibujo, tabla o fórmula aparte) que el texto no trae. El Paso 2 avisa que no se muestra. Se agrega porque `06-spec` §2.4 la pide y no había dónde guardarla.<br>*Fuente: 06-spec-crear-experiencia-paso2.md §2.4 · ADR-011 · encargo 05* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |
|---|---|---|---|---|
| `codigo_area` | `area(codigo_area)` | `RESTRICT` | `RESTRICT` | Raíz. Sin ON UPDATE CASCADE: el CHECK de RI-21 lee esta columna. |
| `numero_grado` | `grado(numero)` | `RESTRICT` | `RESTRICT` | Raíz. Sin ON UPDATE CASCADE, por la misma razón. |
| `id_documento, codigo_area` | `documento_oficial(id_documento, codigo_area)` | `RESTRICT` | `RESTRICT` | Compuesta con codigo_area: el documento del que se copió el DBA es de su misma área (RI-20, ciclo C6 del MER). |

**Restricciones de dominio (CHECK)**

- `codigo_dba = CONCAT(codigo_area, '-', LPAD(numero_grado, 2, '0'), '-', RIGHT(codigo_dba, 2)) AND RIGHT(codigo_dba, 2) REGEXP '^[0-9]{2}$' AND RIGHT(codigo_dba, 2) <> '00'` — el código es ÁREA-GG-NN, con el área y el grado de la fila y un número de dos cifras desde 01. *RI-21 · ADR-036*

## 10. `evidencia`

**Entidad del MER:** Evidencia · **Clasificación:** Externa (MEN), débil

Evidencia de aprendizaje de un DBA. Entidad débil: no tiene identidad fuera de su DBA. Dato del MEN, sin juicio nuestro.

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `codigo_dba` | `VARCHAR(9) CHARACTER SET ascii COLLATE ascii_bin` | No | PK,FK | — | — | DBA al que pertenece. Relación identificadora.<br>*Fuente: MER · Evidencia* |
| `numero_evidencia` | `TINYINT UNSIGNED` | No | PK | > 0 | — | Posición dentro de la lista de evidencias de ese DBA: es también el orden oficial en que se diagnostican (ADR-024).<br>*Fuente: curriculo_men_normalizado.json · ADR-024* |
| `enunciado` | `TEXT` | No | — | — | — | Texto oficial de la evidencia.<br>*Fuente: RF-06-01* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |
|---|---|---|---|---|
| `codigo_dba` | `dba(codigo_dba)` | `CASCADE` | `CASCADE` | Entidad débil: sin su DBA no tiene identidad. |

**Restricciones de dominio (CHECK)**

- `numero_evidencia > 0` — posición dentro del DBA. *MER*

## 11. `evidencia_dictamen`

**Entidad del MER:** Evidencia_Dictamen · **Clasificación:** Propia, débil

Nuestro juicio sobre una evidencia del MEN: si admite formato cerrado, y cuál. Separada de `evidencia` a propósito, para no mezclar contenido oficial con criterio propio (H-6).

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `codigo_dba` | `VARCHAR(9) CHARACTER SET ascii COLLATE ascii_bin` | No | PK,FK | — | — | Evidencia dictaminada (parte 1).<br>*Fuente: H-6 · MER* |
| `numero_evidencia` | `TINYINT UNSIGNED` | No | PK,FK | — | — | Evidencia dictaminada (parte 2).<br>*Fuente: H-6 · MER* |
| `aplica_formato_cerrado` | `BOOLEAN` | No | — | true \| false | — | Si esta evidencia se puede diagnosticar con pregunta cerrada.<br>*Fuente: RF-06-02 · ADR-006 · ADR-042 · censo QA-014* |
| `formato` | `ENUM('single_choice','matching','ordering')` | Sí | — | single_choice \| matching \| ordering | NULL | Qué formato cerrado admite: «el formato de los ítems lo determina la evidencia» (RF-03-01), y una pregunta propia se crea con él (RF-03-07). NULL si no admite formato cerrado (RI-19).<br>*Fuente: RF-03-01 · RF-03-07 · ADR-006* |
| `justificacion` | `TEXT` | Sí | — | — | NULL | Por qué se dictaminó así: cita la frase decisiva de la evidencia y la regla de los criterios del censo.<br>*Fuente: H-6 · MER · ADR-042* |
| `fecha_dictamen` | `DATETIME` | No | — | — | — | Cuándo se dictaminó. Obligatoria porque el dictamen puede cambiar al validar el censo QA-014.<br>*Fuente: H-6 · MER · V-6* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |
|---|---|---|---|---|
| `codigo_dba, numero_evidencia` | `evidencia(codigo_dba, numero_evidencia)` | `CASCADE` | `CASCADE` | Entidad débil: el dictamen no existe sin la evidencia dictaminada. |

**Restricciones de dominio (CHECK)**

- `(aplica_formato_cerrado = 1 AND formato IS NOT NULL) OR (aplica_formato_cerrado = 0 AND formato IS NULL)` — si admite formato cerrado dice cuál; si no, no tiene formato. *RI-19 · RF-03-01*

## 12. `experiencia_evidencia`

**Entidad del MER:** Experiencia_Evidencia · **Clasificación:** Asociativa

Las evidencias que diagnostica esta experiencia: una fila por evidencia incluida, fijada al crearla (solo las que el dictamen admite, RI-5). Hace que Ítem y Resultado cuelguen de un solo camino al currículo (H-4).

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_experiencia` | `INT UNSIGNED` | No | PK,FK | — | — | Experiencia (parte 1 de la llave).<br>*Fuente: H-4 · MER* |
| `codigo_dba` | `VARCHAR(9) CHARACTER SET ascii COLLATE ascii_bin` | No | PK,FK | — | — | Evidencia incluida (parte 2).<br>*Fuente: H-4 · MER* |
| `numero_evidencia` | `TINYINT UNSIGNED` | No | PK,FK | — | — | Evidencia incluida (parte 3).<br>*Fuente: H-4 · MER* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |
|---|---|---|---|---|
| `id_experiencia, codigo_dba` | `experiencia(id_experiencia, codigo_dba)` | `CASCADE` | `CASCADE` | Compuesta con codigo_dba: la evidencia incluida tiene que ser del DBA al que se ancla la experiencia (RI-18, ciclo C1 del MER). Eliminar la experiencia elimina sus evidencias incluidas (V-11). |
| `codigo_dba, numero_evidencia` | `evidencia(codigo_dba, numero_evidencia)` | `RESTRICT` | `CASCADE` | Hacia el currículo del MEN: no se borra una evidencia oficial en uso. |

## 13. `inscripcion`

**Entidad del MER:** Inscripción · **Clasificación:** Asociativa

Un estudiante unido a una experiencia con su código. Llave propia (no compuesta) para que Presentación y Resultado no arrastren llave doble.

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_inscripcion` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Inscripción* |
| `id_estudiante` | `INT UNSIGNED` | No | FK | — | — | Estudiante inscrito.<br>*Fuente: MER · relación «realiza»* |
| `id_experiencia` | `INT UNSIGNED` | No | FK | — | — | Experiencia a la que se unió.<br>*Fuente: MER · relación «pertenece a»* |
| `fecha_union` | `DATETIME` | No | — | — | — | Cuándo se unió con el código.<br>*Fuente: RF-04-02 · 08-spec-unirse-codigo.md* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |
|---|---|---|---|---|
| `id_estudiante` | `estudiante(id_estudiante)` | `RESTRICT` | `CASCADE` | Raíz. |
| `id_experiencia` | `experiencia(id_experiencia)` | `CASCADE` | `CASCADE` | Eliminar la experiencia elimina a sus inscritos de ella (V-11, RF-02-07). |

**Unicidad**

- `UNIQUE(id_estudiante, id_experiencia)` — RI-1
- `UNIQUE(id_inscripcion, id_experiencia)` — destino de FK: habilita la comprobación estructural de RI-13

## 14. `item`

**Entidad del MER:** Ítem · **Clasificación:** Propia

Pregunta del banco de diagnóstico. La IA genera 12 por evidencia al crear la experiencia; el docente puede editarlas, descartarlas y agregar las suyas mientras esté en Borrador (ADR-026).

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_item` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Ítem* |
| `id_experiencia` | `INT UNSIGNED` | No | FK | — | — | Parte 1 de la FK compuesta hacia experiencia_evidencia.<br>*Fuente: H-4 · MER* |
| `codigo_dba` | `VARCHAR(9) CHARACTER SET ascii COLLATE ascii_bin` | No | FK | — | — | Parte 2 de esa misma FK compuesta.<br>*Fuente: H-4 · MER* |
| `numero_evidencia` | `TINYINT UNSIGNED` | No | FK | — | — | Parte 3 de esa misma FK compuesta.<br>*Fuente: H-4 · MER* |
| `enunciado` | `TEXT` | No | — | — | — | Texto de la pregunta.<br>*Fuente: ADR-014 · RF-03-05* |
| `formato` | `ENUM('single_choice','matching','ordering')` | No | — | single_choice \| matching \| ordering | 'single_choice' | Cómo se responde: lo determina la evidencia.<br>*Fuente: ADR-006 · RF-03-01* |
| `origen` | `ENUM('ia','editado_docente','creado_docente')` | No | — | ia \| editado_docente \| creado_docente | 'ia' | Generado por IA, editado por el docente o creado por el docente. Editar uno generado lo pasa a `editado_docente`. Qué servicio y modelo lo generó está en su experiencia (RI-17).<br>*Fuente: RF-03-03 · RF-03-05 · RF-03-07 · ADR-026* |
| `excluido` | `BOOLEAN` | No | — | true \| false | FALSE | «Descartar»: no se muestra a los estudiantes, pero sigue en el banco. Reversible.<br>*Fuente: RF-03-06 · ADR-015* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |
|---|---|---|---|---|
| `id_experiencia, codigo_dba, numero_evidencia` | `experiencia_evidencia(id_experiencia, codigo_dba, numero_evidencia)` | `CASCADE` | `CASCADE` | UNA sola FK compuesta: el ítem es de una evidencia que su experiencia incluye. |

**Unicidad**

- `UNIQUE(id_item, id_experiencia)` — destino de FK: habilita la comprobación estructural de RI-13

## 15. `opcion`

**Entidad del MER:** Opción · **Clasificación:** Propia

Opción de respuesta de un ítem. Qué columnas aplican depende del formato del ítem (RI-4).

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_opcion` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Opción* |
| `id_item` | `INT UNSIGNED` | No | FK | — | — | Ítem al que pertenece.<br>*Fuente: MER · relación «ofrece»* |
| `texto` | `TEXT` | No | — | — | — | Texto de la opción.<br>*Fuente: ADR-014* |
| `orden` | `TINYINT UNSIGNED` | Sí | — | según el formato (RI-4) | NULL | En `ordering`: la posición correcta. En `matching`: número de pareja. NULL en `single_choice`.<br>*Fuente: ADR-014 · RI-4* |
| `es_correcta` | `BOOLEAN` | Sí | — | según el formato (RI-4) | NULL | Solo aplica a `single_choice`. NULL en los otros dos formatos.<br>*Fuente: ADR-014 · RI-4* |
| `grupo` | `ENUM('izquierda','derecha')` | Sí | — | izquierda \| derecha, solo en matching | NULL | Solo aplica a `matching`: de qué lado del emparejamiento está.<br>*Fuente: ADR-014 · RI-4* |
| `hipotesis_error` | `TEXT` | Sí | — | — | NULL | Por qué un estudiante podría elegir esta opción incorrecta. No se muestra ni se reporta (ADR-008).<br>*Fuente: ADR-020* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |
|---|---|---|---|---|
| `id_item` | `item(id_item)` | `CASCADE` | `CASCADE` | Composición: una opción no existe sin su ítem. |

**Unicidad**

- `UNIQUE(id_opcion, id_item)` — destino de FK: habilita la comprobación estructural de RI-6

## 16. `presentacion`

**Entidad del MER:** Presentación · **Clasificación:** Propia, débil

El hecho de HABER MOSTRADO un ítem a un estudiante — distinto del de haberlo respondido. Una pregunta mostrada y sin responder se vuelve a mostrar al retomar (ADR-031).

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_inscripcion` | `INT UNSIGNED` | No | PK,FK | — | — | A quién se le mostró (parte 1 de la llave).<br>*Fuente: H-2/H-3 · MER* |
| `id_item` | `INT UNSIGNED` | No | PK,FK | — | — | Qué ítem se mostró (parte 2 de la llave).<br>*Fuente: H-2/H-3 · MER* |
| `id_experiencia` | `INT UNSIGNED` | No | FK | — | — | COLUMNA REDUNDANTE DELIBERADA, igual que en `resultado`: está en las dos FK compuestas y obliga a que el ítem sea de la misma experiencia que la inscripción (RI-13). Estructural, sin trigger.<br>*Fuente: RI-13 · MER (Presentación) · cierra el hueco del borrador del MR* |
| `orden_presentacion` | `TINYINT UNSIGNED` | No | — | > 0, único por inscripción (RI-8) | — | Lugar en la secuencia completa del diagnóstico de esa inscripción. Reconstruye la secuencia adaptativa.<br>*Fuente: RF-04-04 · RI-8 · ADR-016* |
| `fecha_presentacion` | `DATETIME` | No | — | — | — | Cuándo se mostró.<br>*Fuente: RF-04-04 · H-2* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |
|---|---|---|---|---|
| `id_inscripcion, id_experiencia` | `inscripcion(id_inscripcion, id_experiencia)` | `CASCADE` | `CASCADE` | Salir de la experiencia borra lo que se le presentó (V-11, RF-04-12). La columna compartida id_experiencia hace estructural RI-13. |
| `id_item, id_experiencia` | `item(id_item, id_experiencia)` | `CASCADE` | `CASCADE` | El ítem presentado es de la misma experiencia (RI-13). CASCADE y no RESTRICT: un ítem solo desaparece cuando desaparece su experiencia entera (ADR-026: descartar no borra), y eso debe poder hacerse aunque tenga respuestas (RF-02-07). |

**Unicidad**

- `UNIQUE(id_inscripcion, orden_presentacion)` — RI-8

**Restricciones de dominio (CHECK)**

- `orden_presentacion > 0` — orden desde 1. *RI-8*

## 17. `respuesta`

**Entidad del MER:** Respuesta · **Clasificación:** Asociativa

Lo que el estudiante respondió a un ítem que se le presentó, con su certeza. Se guarda al confirmar la certeza, no al final (RF-04-06).

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_respuesta` | `INT UNSIGNED AUTO_INCREMENT` | No | PK | — | — | Identificador interno.<br>*Fuente: MER · Respuesta* |
| `id_inscripcion` | `INT UNSIGNED` | No | FK | — | — | Parte 1 de la FK compuesta hacia presentación.<br>*Fuente: H-3 · MER* |
| `id_item` | `INT UNSIGNED` | No | FK | — | — | Parte 2 de esa misma FK compuesta.<br>*Fuente: H-3 · MER* |
| `certeza` | `TINYINT UNSIGNED` | No | — | 0 a 5 (CRI) | — | Certeza declarada (CRI, Hasan et al. 1999). De 3 a 5 es señal fuerte (RF-04-07).<br>*Fuente: ADR-008 punto 2 · RF-04-05* |
| `fecha_respuesta` | `DATETIME` | No | — | — | — | Cuándo se confirmó.<br>*Fuente: RF-04-06 · H-2* |
| `correcta` | `BOOLEAN` | No | — | true \| false | — | DERIVADO Y PERSISTIDO (ADR-021). En emparejamiento y ordenamiento, verdadero solo si todos los pares o posiciones están bien.<br>*Fuente: RF-04-06 · ADR-019 · ADR-021* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |
|---|---|---|---|---|
| `id_inscripcion, id_item` | `presentacion(id_inscripcion, id_item)` | `CASCADE` | `CASCADE` | Una respuesta sin presentación previa es imposible por estructura (H-3). |

**Unicidad**

- `UNIQUE(id_inscripcion, id_item)` — una presentación, una respuesta
- `UNIQUE(id_respuesta, id_item)` — destino de FK: habilita la comprobación estructural de RI-6

**Restricciones de dominio (CHECK)**

- `certeza BETWEEN 0 AND 5` — escala CRI. *ADR-008 punto 2*

## 18. `respuesta_opcion`

**Entidad del MER:** Respuesta_Opción · **Clasificación:** Asociativa

Qué opción u opciones eligió el estudiante — no solo si acertó. Sin esta tabla, `matching` y `ordering` no son representables.

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_respuesta` | `INT UNSIGNED` | No | PK,FK | — | — | Respuesta a la que pertenece (parte 1).<br>*Fuente: ADR-019* |
| `id_opcion` | `INT UNSIGNED` | No | PK,FK | — | — | Opción elegida (parte 2).<br>*Fuente: ADR-019* |
| `id_item` | `INT UNSIGNED` | No | FK | — | — | COLUMNA REDUNDANTE DELIBERADA, como id_experiencia en presentacion: está en las dos FK compuestas y obliga a que la opción elegida sea del ítem que se presentó (RI-6, ciclo C4 del MER). Estructural, sin trigger.<br>*Fuente: RI-6 · ciclo C4 del MER* |
| `valor_dado` | `TINYINT UNSIGNED` | Sí | — | según el formato del ítem | NULL | `single_choice`: NULL, la fila ya es la elección. `ordering`: la posición que le asignó. `matching`: el número de pareja.<br>*Fuente: ADR-019* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |
|---|---|---|---|---|
| `id_respuesta, id_item` | `respuesta(id_respuesta, id_item)` | `CASCADE` | `CASCADE` | Sin la respuesta, la selección no tiene sentido. Compuesta con id_item: fija de qué ítem es la respuesta (RI-6). |
| `id_opcion, id_item` | `opcion(id_opcion, id_item)` | `CASCADE` | `CASCADE` | Compuesta con id_item: la opción elegida es del ítem que se presentó (RI-6, ciclo C4). CASCADE y no RESTRICT: una opción solo se borra editando un ítem en Borrador, cuando todavía no hay respuestas (ADR-026, RI-10), o al eliminar la experiencia entera, que debe poder hacerse (RF-02-07). |

## 19. `resultado`

**Entidad del MER:** Resultado · **Clasificación:** Propia, débil

Lo que las respuestas de un estudiante permiten concluir sobre UNA evidencia DE ESTA experiencia. Fotografía del momento en que se concluyó, no recalculada al vuelo (RNF-11).

<!-- tabla:campos -->
| Campo | Tipo (MySQL) | Nulo | Llave | Dominio | Defecto | Descripción y fuente |
|---|---|---|---|---|---|---|
| `id_inscripcion` | `INT UNSIGNED` | No | PK,FK | — | — | De quién es el resultado (parte 1 de la llave).<br>*Fuente: MER · relación «arroja»* |
| `id_experiencia` | `INT UNSIGNED` | No | FK | — | — | COLUMNA REDUNDANTE DELIBERADA, que el MER delega al MR: permite que las dos reglas de coherencia sean estructurales (RI-13).<br>*Fuente: MER · Resultado (delegación explícita al MR)* |
| `codigo_dba` | `VARCHAR(9) CHARACTER SET ascii COLLATE ascii_bin` | No | PK,FK | — | — | Evidencia medida (parte 2 de la llave).<br>*Fuente: H-4 · MER* |
| `numero_evidencia` | `TINYINT UNSIGNED` | No | PK,FK | — | — | Evidencia medida (parte 3 de la llave).<br>*Fuente: H-4 · MER* |
| `estado` | `ENUM('muestra','no_muestra','no_concluyente')` | No | — | muestra \| no_muestra \| no_concluyente | — | DERIVADO Y PERSISTIDO con la regla de RF-04-07 (cierra V-5). Nunca una certeza; nunca un valor que se edite a mano.<br>*Fuente: RF-04-07 · ADR-016 · ADR-021* |
| `fecha_calculo` | `DATETIME` | No | — | — | — | Cuándo se concluyó. Una fotografía sin fecha no es auditable.<br>*Fuente: ADR-021 · RNF-11* |

**Llaves foráneas**

<!-- tabla:fks -->
| Columnas | Referencia | ON DELETE | ON UPDATE | Por qué esa acción |
|---|---|---|---|---|
| `id_inscripcion, id_experiencia` | `inscripcion(id_inscripcion, id_experiencia)` | `CASCADE` | `CASCADE` | La experiencia del resultado es la de su inscripción (RI-13). Salir borra los resultados (V-11). |
| `id_experiencia, codigo_dba, numero_evidencia` | `experiencia_evidencia(id_experiencia, codigo_dba, numero_evidencia)` | `CASCADE` | `CASCADE` | La evidencia medida es una que esa experiencia incluye. CASCADE para que eliminar la experiencia no quede bloqueado por sus resultados (V-11). |

---

## Lo que este diccionario declara como no resuelto

Un diccionario que inventa un valor para un dato que todavía no se
tiene afirma más de lo que el proyecto sostiene. Estos casos quedan
marcados, no rellenados:

| Campo | Qué falta | Dónde está declarado |
|---|---|---|
| `evidencia_dictamen.aplica_formato_cerrado` | El tipo está cerrado y **los valores están propuestos**: el censo QA-014 (encargo 05) dictaminó las 1282 evidencias, pero es un juicio de IA hasta que el equipo lo valide por muestreo. | **V-6**, ADR-042 |
| `dba.codigo_dba` | El formato `ÁREA-GG-NN` está cerrado (RI-21), y los datos lo cumplen como llave desde el catálogo corregido (`data/curriculo-men/catalogo/catalogo_dba.json`, 343 DBA, encargo 02). El JSON viejo, `curriculo_men_normalizado.json`, tenía 342 DBA y solo 329 códigos distintos; cargarlo falla por llave duplicada en 13, y eso es lo correcto: se corrigió en los datos, no en el modelo. | **Pendientes, A12** · ADR-036 |

**Cerrados desde el borrador anterior** (para no perder el rastro):
`item.estado_revision` sale del modelo (V-7: tras ADR-026 revisar el
banco no es requisito de nada); la función que calcula
`resultado.estado` quedó definida en RF-04-07 (V-5); la credencial ya
tiene tabla (V-8); y la política de borrado está en las FK (V-11).

## Convenciones fijadas aquí

- **Identificadores:** `INT UNSIGNED AUTO_INCREMENT`. Un `INT UNSIGNED`
  llega a 4.294.967.295 filas — muy por encima de cualquier escala
  realista de este sistema, y ocupa la mitad que un `BIGINT`.
- **`VARCHAR(254)` para correo:** es el máximo que admite una dirección
  de correo según RFC 5321. No es un número redondeado a ojo.
- **`CHAR(6)` para el código de invitación y el de verificación:**
  longitud fija y conocida (`08-spec-unirse-codigo.md` §2.3,
  RF-01-03). `CHAR` y no `VARCHAR` porque nunca varía.
- **`TINYINT UNSIGNED` para `certeza`, `numero_evidencia`,
  `orden_presentacion`, `orden`, `valor_dado`, el número del grado y los
  contadores de intentos:** ninguno pasa de 255 por definición (la escala
  CRI llega a 5; el tope de ítems por evidencia es 6, ADR-016; los grados,
  a 11). `SMALLINT UNSIGNED` para el año y las páginas de un documento.
- **`TEXT` para todo enunciado:** los textos del MEN no tienen longitud
  acotada conocida, y truncarlos sería alterar contenido oficial.
- **`DATETIME` y no `TIMESTAMP`:** `TIMESTAMP` tiene el límite del año
  2038 y conversión automática de zona horaria; ninguna de las dos
  cosas se necesita aquí.
- **`ENUM` donde el dominio está cerrado y decidido.** Desde que V-7 se
  cerró ya no queda ningún dominio abierto; en SQLite, que no tiene
  `ENUM`, cada uno se vuelve un `CHECK ... IN (...)`.
- **`utf8mb4` con cotejamiento `utf8mb4_unicode_ci`:** acentos y eñes
  sin pérdida, y comparación sin distinguir mayúsculas — por eso
  `correo` y `codigo_invitacion` son únicos sin importar cómo se
  escriban (RF-01-04, `08-spec-unirse-codigo.md`). Se elige ese
  cotejamiento y no el `utf8mb4_0900_ai_ci` por defecto de MySQL 8
  porque MariaDB no lo tiene.
- **Códigos del catálogo en ASCII con cotejamiento binario**
  (`CHARACTER SET ascii COLLATE ascii_bin`): `codigo_dba` y `codigo_area`, y
  toda columna que los repite como llave foránea. ADR-036 pide códigos sin
  tildes: con ASCII, una tilde no se puede guardar; con el cotejamiento
  binario, `mat` no es igual a `MAT`. Las dos cosas existen igual en MySQL 8 y
  en MariaDB. Es una decisión de este modelo, no de una ADR: va declarada en
  `17-modelo-relacional.md` para que el equipo la confirme.
- **`VARCHAR(9)` para `codigo_dba`:** `ÁREA-GG-NN` mide 8 o 9 caracteres
  (`CN-01-01`, `MAT-01-01`).
- **Nombres de restricción** `ck_<tabla>_<n>`, `fk_<tabla>_<n>` y
  `uq_<tabla>_<n>`: un error del motor nombra la regla rota, y con el
  número se encuentra aquí.

