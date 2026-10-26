# Guía para explicar el MER, paso a paso

**Para qué es:** para que cualquiera del equipo pueda explicar el Modelo Entidad-Relación de
AdaptiveLearn delante del profesor y responder lo que pregunte, hasta lo más mínimo.
**Qué no es:** no es un entregable. El documento oficial es `16-modelo-entidad-relacion.md`;
esta guía lo explica con otras palabras. Si el modelo cambia, manda el documento 16 (las
cifras de aquí son las del 2026-10-22).

> **Aviso (2026-10-26): esta guía quedó atrasada.** El MER cambió por la revisión del docente
> del 2026-10-22 (ADR-036 y ADR-037): ahora tiene **18 entidades** (entran ÁREA, GRADO y
> DOCUMENTO_OFICIAL), 22 relaciones, **6 ciclos** (el nuevo, C6, lo cierra RI-20) y **21
> restricciones**; el DBA ya no tiene `area` ni `grado` como texto y su código es `ÁREA-GG-NN`
> (`MAT-08-01`, RI-21); y CREDENCIAL guarda `estado_verificacion` (`procesando` o
> `verificado`) en vez de `email_verificado`. Mientras no se reescriba, para esas partes manda
> el documento 16 (§4, §6, §10 y §11).

**Qué tener abierto mientras se expone:**
- La lámina completa: `mer/mer-pantalla-completa.html`, a pantalla completa, con zoom.
- El documento 16, para buscar una restricción (§11) o un hallazgo (§10) si lo pide.

---

## 1. Las cifras que hay que saber de memoria

| Qué | Cuánto | Cómo decirlo |
|---|---|---|
| Entidades | **15**, más Reporte | «Quince entidades que se guardan, y Reporte, que es derivada: se calcula, no se guarda.» |
| Relaciones | **18**, más 2 derivadas | «Dieciocho relaciones reales; las dos de Reporte son derivadas.» |
| Atributos | **62** | Cuentan también los 3 calculados (`progreso` y los 2 de Reporte). |
| Entidades débiles | **4** | Evidencia, Evidencia_Dictamen, Presentación, Resultado. |
| Entidades asociativas | **3** | Experiencia_Evidencia, Inscripción, Respuesta_Opción. |
| Ciclos | **5**, todos revisados | 4 los cierra la estructura de la base; el quinto no necesita regla. |
| Restricciones de integridad | **19** (RI-1 a RI-19) | Las 11 del borrador y 8 nuevas. |
| Vistas | **7**, más la lámina de conjunto y el mapa completo | Cortadas por el ciclo de vida: de la cuenta al reporte. |
| Modelo relacional | **15 tablas, 91 columnas, 19 llaves foráneas, 13 UNIQUE, 10 CHECK** | Reporte no tiene tabla. |
| Pruebas | **49** | En SQLite y contra MySQL 8.4: la base rechaza lo que el modelo prohíbe. |
| Revisión del profesor | **12 hallazgos** | 11 resueltos y H-5 en parte. |

---

## 2. El guion: cómo exponerlo en 5 minutos

Exponer en este orden, señalando la lámina.

**1. Qué es el sistema, en una frase.** «Un docente crea una experiencia de diagnóstico sobre
un DBA del MEN; la IA genera las preguntas; el estudiante se une con un código y responde,
diciendo también qué tan seguro está; y el sistema concluye, por cada evidencia, si el
estudiante la muestra o no, y se lo reporta al docente.»

**2. Cómo leer la lámina (30 segundos).**
- Los colores dicen el tipo de entidad:
  - morado: propia
  - dorado: asociativa
  - café claro: dato del MEN
  - rosado: débil
  - gris: derivada
- Los rombos verdes son las relaciones.
- La línea doble es participación total.
- El (mín, máx) junto a cada entidad dice cuántas veces participa.
- La leyenda está abajo.

**3. El recorrido, de izquierda a derecha y de arriba abajo.** Contarlo con el caso de Ana
(docente) y Luis (estudiante). Es el mismo caso del diagrama de objetos, que se cargó en la
base real sin violar nada.
1. **Acceso.** Ana crea su cuenta: nace su CREDENCIAL. Al elegir el rol nace DOCENTE. Luis
   entra con Google y su credencial accede como ESTUDIANTE. Una credencial nunca accede a
   los dos roles ({xor}).
2. **Currículo.** El DBA del MEN *comprende* sus evidencias. Cada evidencia tiene nuestro
   DICTAMEN: si admite pregunta cerrada y con qué formato.
3. **Autoría.** Ana crea una EXPERIENCIA anclada a un DBA. La experiencia *incluye* las
   evidencias admitidas de ese DBA (EXPERIENCIA_EVIDENCIA).
4. **Banco.** Cada evidencia incluida *genera* 12 ÍTEMS, y cada ítem *ofrece* sus OPCIONES.
   Ana edita, descarta o agrega; al publicar, el banco se congela.
5. **Entrega.** Luis se une con el código: nace su INSCRIPCIÓN. Cada pregunta que se le
   muestra queda registrada como una PRESENTACIÓN.
6. **Respuesta.** Al confirmar su certeza, la presentación *registra* una RESPUESTA, que
   *selecciona* opciones (RESPUESTA_OPCIÓN).
7. **Conclusión.** Cuando la regla adaptativa concluye una evidencia, nace un RESULTADO.
   Cuando Ana abre el reporte, se calcula REPORTE (no se guarda).

**4. Lo que demuestra que el modelo es sólido (1 minuto).**
- **Los ciclos.** «El modelo tiene exactamente 5 ciclos, y cada uno está declarado con lo que
  lo cierra. Cuatro los cierra la propia estructura de la base, sin triggers. Lo comprobamos
  con pruebas que intentan romperlos.»
- **La notación.** «Es Chen estricta, como pidió en H-8: no dibujamos llaves foráneas.»

**5. Su revisión (30 segundos).** «Sus 12 hallazgos están respondidos uno por uno en la sección
10 del documento 16.»

---

## 3. La notación, símbolo por símbolo

| Símbolo | Qué significa | Cómo explicarlo si pregunta |
|---|---|---|
| Rectángulo | Entidad | Algo de lo que guardamos datos y que tiene identidad propia. |
| Rectángulo de **doble borde** | Entidad débil | No se puede identificar sola: necesita la llave de otra entidad (su «dueña»). |
| Rombo | Relación | Un vínculo entre entidades. |
| Rombo **doble** | Relación identificadora | La relación que le presta la identidad a una entidad débil. |
| Elipse | Atributo | Un dato de la entidad. |
| Elipse **negra** (o subrayada) | Llave primaria | Lo que identifica a cada ejemplar. |
| Subrayado **punteado** | Llave parcial | Lo que distingue a una débil *dentro* de su dueña. Solo la tiene `numero_evidencia`. |
| Elipse **punteada** | Atributo derivado | Sale de otros datos. Hay dos clases: **D** = derivado que *se guarda*; **C** = calculado, *no se guarda*. |
| Línea **simple** | Participación parcial | Puede haber ejemplares que no participen (mínimo 0). |
| Línea **doble** | Participación total | Todo ejemplar participa (mínimo 1 o más). |
| **(mín, máx)** junto a la entidad | Cuántas veces participa *un* ejemplar de esa entidad | Es la notación de la tabla de la v3 del profesor. |
| **1:1, 1:N, N:M** bajo el rombo | La razón de la relación | El tipo de relación, mirando los dos extremos. |
| **{xor}** punteado entre dos rombos | Relaciones excluyentes | Un ejemplar participa en una o en la otra, nunca en las dos. |
| Rombo y caja **punteados** | Derivados | Reporte y sus dos relaciones: se calculan, no se guardan. |

**Las dos maneras de leer cardinalidad (pregunta casi segura).**
- **La razón (1:N) se lee «cruzando».** En *crea*, 1:N dice: un docente, muchas experiencias.
- **El (mín, máx) se lee «aquí mismo».** Va junto a cada entidad y dice cuántas veces participa
  un ejemplar de *esa* entidad:
  - DOCENTE (0,N): un docente crea de cero a muchas experiencias.
  - EXPERIENCIA (1,1): cada experiencia la crea exactamente un docente.
- **Las dos dicen lo mismo y son coherentes.** La línea doble aparece exactamente donde el
  mínimo es 1 o más. Un verificador (`mer/_verificar_mer.py`) comprueba que coincidan.

**¿Por qué no se ven las llaves foráneas?** Es Chen estricta, y lo pidió el profesor en H-8:
- La llave foránea *es* lo que se obtiene al pasar al modelo relacional a partir de la
  relación dibujada. Dibujarla en el MER es repetir el MR.
- Las llaves foráneas están en el documento 17.
- Un verificador (`_verificar_mr_mer.py`) comprueba que cada llave foránea salga de una
  relación del MER y que cada relación tenga su llave foránea.
- **Ojo:** la lámina de conjunto (la de colores) *sí* muestra PK y FK. Es a propósito, con la
  estructura de la v3 del profesor, para ver de un vistazo cómo se enlaza todo. Esas llaves
  se calculan del MR, así que no lo pueden contradecir. El MER formal es el de Chen (mapa y
  7 vistas).

---

## 4. Entidad por entidad

Para cada una:
- qué es, en una frase
- su tipo y por qué
- cada atributo
- lo que *no* tiene, y por qué
- preguntas probables

### 4.1 CREDENCIAL — propia · vista 1

**Qué es.** La cuenta de acceso: con qué correo y qué método se entra, si el correo está
verificado y a qué rol da acceso.

**Por qué existe, separada de Docente y Estudiante.**
- **Nace antes que el rol.** Existe desde «Crear cuenta», antes de que la persona elija su
  rol, y hace falta para guardar el código de verificación (RF-01-03). El docente o el
  estudiante se crea recién al elegir el rol (RF-01-05, RF-01-06).
- **El correo vive aquí** para que sea único **entre los dos roles** (RF-01-04): con un UNIQUE
  en Docente y otro en Estudiante, el mismo correo podría estar en las dos tablas.
- **Cierra el vacío V-8.**
- **Es la tabla que el backend de I1 ya construyó.**

| Atributo | Qué guarda |
|---|---|
| `id_credencial` (PK) | Identificador interno. |
| `correo` (único) | El correo de la cuenta; único sin distinguir mayúsculas (RI-3). |
| `proveedor` | Con qué método se creó: `correo`, `google` o `microsoft`. No se vinculan métodos: si ya existe con otro, se avisa cuál usar (RF-01-04). Sin Apple. |
| `password_hash` | La contraseña con hash, nunca legible (RNF-08). Vacía si entra con Google o Microsoft (RI-15). |
| `proveedor_id` | El identificador de la persona en Google o Microsoft. Vacío si es de correo (RI-15). |
| `email_verificado` | Si el correo se verificó con el código. Con Google o Microsoft llega verdadero: lo verificó el proveedor. |
| `codigo_verificacion` | El último código de 6 dígitos enviado, sea de registro o de recuperación: la misma ventana sirve a los dos. |
| `codigo_expira_en` | Hasta cuándo vale ese código. |
| `codigo_ultimo_envio` | Cuándo se envió; el reenvío se habilita 30 s después. |
| `creado_en` | Cuándo se creó la cuenta. |

**Lo que no está en el MER y sí en el MR.** Son seguridad del backend de I1, no datos del
dominio; el MER no dibuja mecanismos de seguridad. Están justificadas en el documento 17:
- `intentos_codigo`, `intentos_login`, `bloqueado_hasta`: contadores de intentos y bloqueo
- `actualizado_en`: fecha de la última modificación

**Preguntas probables**
- *¿Por qué no hay una entidad Usuario?* En el MER no hace falta: lo común de los dos roles
  (el correo, la contraseña) vive en la credencial. En el diagrama de clases sí aparece
  `Usuario`, como clase abstracta de la que heredan Docente y Estudiante, porque ahí agrupa
  comportamiento (editar el perfil).
- *¿Una credencial puede no tener rol?* Sí, mientras el registro está en curso. Por eso su
  mínimo es 0 en *accede como*: (0,1).
- *¿Cómo sabe el sistema si es docente o estudiante?* Por cuál de las dos relaciones *accede
  como* tiene. En la base, por cuál de `id_docente` / `id_estudiante` está lleno; nunca los
  dos, por un CHECK (RI-12).

### 4.2 DOCENTE y ESTUDIANTE — propias · vista 1

**Qué son.** Las dos personas del sistema. El docente crea y publica experiencias; el
estudiante se une con un código y responde.

| Atributo | Qué guarda |
|---|---|
| `id_docente` / `id_estudiante` (PK) | Identificador interno. |
| `nombres`, `apellidos` | Obligatorios, separados (ventanas 016 y 026; RF-01-05). |
| `avatar_url` | La foto, opcional. Se reemplaza, no se quita. |

**Por qué son dos entidades y no una con un campo «rol».**
- **La estructura impide un error.** La relación de cada uno con Experiencia es distinta:
  uno *crea* y el otro se *inscribe*. Con dos entidades, la llave foránea del autor de una
  experiencia apunta a DOCENTE, así que un estudiante no puede quedar como autor ni por
  error.
- **Es una decisión del borrador que se mantiene.** Equivale a una especialización disjunta
  de «usuario»; la disyunción se expresa con el {xor} de la credencial.

**Lo que no tienen.**
- **No tienen correo:** está en la credencial.
- **El estudiante tiene solo datos mínimos (ADR-029):** nombres, apellidos y foto opcional.

**Pregunta probable**
- *¿Una persona puede ser docente y estudiante a la vez?* No con la misma cuenta: el rol se
  elige una vez y no se cambia (RF-01-06). Tendría que usar otro correo.

### 4.3 EXPERIENCIA — propia · vista 3

**Qué es.** Un diagnóstico anclado a un único DBA, creado por un docente.

| Atributo | Qué guarda |
|---|---|
| `id_experiencia` (PK) | Identificador interno. |
| `nombre` | Llega prellenado con el enunciado del DBA; el docente puede cambiarlo. |
| `estado` | `Borrador` o `Publicada`. Sin vuelta atrás (ADR-026). |
| `fecha_creacion` | Cuándo se creó. |
| `fecha_publicacion` | Cuándo se publicó; vacía mientras está en Borrador (RI-16, con CHECK). |
| `codigo_invitacion` (único) | 6 caracteres, sin 0/O ni 1/I/L para que no se confundan al dictarlo (RI-3). Se genera al crear la experiencia y se muestra solo cuando está publicada (RF-02-06). |
| `servicio_ia` | Con qué servicio se generó el banco: `gemini` o `deepseek` (ADR-030). |
| `modelo_ia` | Qué modelo de ese servicio. |

**Preguntas probables**
- *¿Por qué no tiene área ni grado?* Porque se derivan del DBA al que se ancla; guardarlos
  sería repetirlos.
- *¿Por qué el servicio de IA está en la experiencia y no en cada ítem?*
  - Un banco sale entero de un solo servicio: si el principal falla, se pide **todo** al de
    respaldo (RF-03-02).
  - Es un dato del banco, no de cada ítem. Guardarlo por ítem lo repetía 12 veces por
    evidencia y, peor, permitía un banco con servicios mezclados (RI-17).
  - Un ítem editado por el docente sigue siendo del servicio de su experiencia; uno creado
    por el docente no se atribuye a la IA.
- *¿Por qué `servicio_ia` no puede estar vacío?* Porque toda experiencia guardada tiene banco:
  se guarda solo si la generación salió completa («todo o nada», ADR-027).
- *¿Se puede despublicar?* No: ADR-026, y está fuera de alcance (documento 10, §2.4).

### 4.4 DBA — dato del MEN · vista 2

**Qué es.** El Derecho Básico de Aprendizaje oficial. Lo carga el equipo desde el currículo
del MEN; el sistema solo lo lee.

| Atributo | Qué guarda |
|---|---|
| `codigo_dba` (PK) | Llave **natural** del MEN, con el formato `{área}_{grado}_dba_{número}`. Es la única llave del modelo que no es un número interno. |
| `area` | Una de las 4: Matemáticas, Lenguaje, Ciencias Naturales, Ciencias Sociales. |
| `grado` | El grado escolar. |
| `enunciado` | El texto oficial, sin reescribir. |
| `ejemplo` | El ejemplo oficial; se le da a la IA como contexto (ADR-011). Puede faltar mientras la normalización no lo tenga (QA-011). |

**Pregunta probable**
- *¿Por qué no tiene llave sustituta?* Porque el MEN ya le da un código estable y único:
  inventar otro sería redundante.

### 4.5 EVIDENCIA — dato del MEN, **débil** · vista 2

**Qué es.** Una evidencia de aprendizaje de un DBA: lo que el estudiante debería poder hacer.

| Atributo | Qué guarda |
|---|---|
| `numero_evidencia` (**llave parcial**, subrayado punteado) | Su posición en la lista del MEN para ese DBA. Es también el **orden oficial** en que se diagnostica (ADR-024). |
| `enunciado` | El texto oficial. |

**Por qué es débil.**
- **No tiene identidad sin su DBA.** «Evidencia 2» no dice nada: es «la evidencia 2 *del DBA
  tal*».
- **Así se identifica:** la llave del DBA (por la relación identificadora *comprende*, rombo
  doble) más su llave parcial `numero_evidencia`.
- **En la base**, su llave primaria es `(codigo_dba, numero_evidencia)`.

**Preguntas probables**
- *¿Por qué es la única con llave parcial?* Porque es la única débil con una sola dueña que
  tiene muchas de ellas: un DBA tiene varias evidencias, y hay que distinguirlas. Las otras
  débiles las identifica por completo la combinación de sus dueñas.
- *¿El rango de evidencias es confiable?* No del todo: el catálogo tiene errores de extracción
  conocidos (QA-013).

### 4.6 EVIDENCIA_DICTAMEN — **débil** · vista 2

**Qué es.** **Nuestro** juicio sobre una evidencia del MEN: si se puede diagnosticar con
pregunta cerrada y con qué formato.

| Atributo | Qué guarda |
|---|---|
| `aplica_formato_cerrado` | Sí o no. |
| `formato` | Cuál formato admite: `single_choice` (selección única), `matching` (emparejamiento) u `ordering` (ordenamiento). Vacío si no admite (RI-19, con CHECK). |
| `justificacion` | Por qué se dictaminó así. |
| `fecha_dictamen` | Cuándo; es obligatoria porque el dictamen puede cambiar cuando se cierre el censo QA-014. |

**Preguntas probables**
- *¿Por qué no son atributos de Evidencia?* Es el hallazgo **H-6** del profesor:
  - Evidencia es dato oficial del MEN; el dictamen es criterio nuestro. Separarlos evita
    mezclar contenido oficial con juicio propio.
  - Además el dictamen cambia: tiene fecha. La evidencia oficial no cambia.
- *¿Por qué es débil y sin llave parcial?* Es 1:1 con su evidencia: la identifica la
  evidencia misma, y no hay varios dictámenes por evidencia que distinguir.
- *¿Por qué `formato` está aquí?* Porque «el formato de los ítems lo determina la evidencia»
  (RF-03-01) y una pregunta propia «se crea con el formato de esa evidencia» (RF-03-07).
  Antes no había dónde guardarlo.
- *¿Qué falta?* Los **valores** del dictamen dependen del censo QA-014 (vacío V-6). La
  estructura está; faltan los datos.

### 4.7 EXPERIENCIA_EVIDENCIA — **asociativa**, sin atributos propios · vista 3

**Qué es.** Las evidencias que diagnostica **esta** experiencia. Una fila es «la evidencia N
del DBA, dentro de la experiencia X».

**Por qué existe.**
- **Es el hallazgo H-4.** Sin ella, Ítem y Resultado tendrían que colgar de la Experiencia y de
  la Evidencia por separado, y haría falta una regla para que coincidieran.
- **Da un solo camino al currículo.** Ítem y Resultado cuelgan de *esta* entidad.
- **Cada experiencia tiene su propio banco.** La misma evidencia en dos experiencias distintas
  tiene ítems distintos.

**Preguntas probables**
- *¿Por qué no tiene atributos?* Su identidad es el par (experiencia, evidencia), y no hay nada
  más que decir de ella:
  - Antes tenía `incluida` (sí/no) y salió: el docente no elige evidencias (QA-010), y solo
    entran las que el dictamen admite (RI-5).
  - Una fila **es** una evidencia incluida; un campo siempre verdadero no aporta nada.
- *Si no tiene atributos, ¿por qué es entidad y no una relación N:M?* Porque **participa en
  otras relaciones**: *genera* ítems y *mide* resultados. En Chen, una relación no puede
  relacionarse con otra cosa; para eso tiene que ser entidad (entidad asociativa).
- *¿Su llave?* En la base, `(id_experiencia, codigo_dba, numero_evidencia)`.
  - **No tiene llave sustituta, a propósito:** llevar `codigo_dba` en la llave es lo que
    permite que la base compruebe que la evidencia sea del DBA de la experiencia (RI-18,
    ciclo C1).
  - Llevar `id_experiencia` hasta el ítem permite comprobar RI-13.
- *¿Puede una experiencia no incluir ninguna evidencia?* No: *incluye* es (1,N). Si un DBA no
  tuviera ninguna evidencia que admita formato cerrado, no se podría crear su experiencia.
  Qué muestra la pantalla en ese caso es el vacío V-12, abierto.

### 4.8 INSCRIPCIÓN — **asociativa** con llave propia · vista 5

**Qué es.** Un estudiante unido a una experiencia.

| Atributo | Qué guarda |
|---|---|
| `id_inscripcion` (PK) | Identificador interno. |
| `fecha_union` | Cuándo se unió con el código. |
| `progreso` (**C**, elipse punteada) | No iniciada, En curso o Completada (RF-04-01). **Se calcula, no se guarda** (ADR-022). Es lo que la v3 del profesor llamaba `estado_avance`. |

**Preguntas probables**
- *¿Por qué es asociativa?* Resuelve la relación muchos a muchos entre Estudiante y
  Experiencia: un estudiante en muchas experiencias, una experiencia con muchos estudiantes.
- *¿Por qué tiene llave propia y Experiencia_Evidencia no?* Para que Presentación y Resultado,
  que cuelgan de ella, no arrastren una llave doble (estudiante + experiencia). Lo que la
  llave doble aseguraba lo cubre un UNIQUE(estudiante, experiencia): unirse dos veces no
  duplica (RI-1).
- *¿Por qué `progreso` no se guarda?*
  - Se deduce de lo que ya existe: sin presentaciones es «No iniciada»; con alguna es «En
    curso»; con un resultado por cada evidencia incluida es «Completada».
  - Guardarlo sería tener el mismo dato dos veces, con riesgo de que no coincidan.
- *¿Por qué es entidad y no relación?* Porque participa en otras relaciones: *atiende*
  presentaciones y *arroja* resultados.

### 4.9 ÍTEM — propia · vista 4

**Qué es.** Una pregunta del banco.

| Atributo | Qué guarda |
|---|---|
| `id_item` (PK) | Identificador interno. |
| `enunciado` | El texto de la pregunta. |
| `formato` | `single_choice`, `matching` u `ordering`: el que fija el dictamen de su evidencia (RI-19). |
| `origen` | `ia`, `editado_docente` o `creado_docente`. Editar uno de la IA lo pasa a `editado_docente`. |
| `excluido` | «Descartar»: no se muestra a los estudiantes, pero sigue en el banco. Reversible. |

**Preguntas probables**
- *¿Por qué cuelga de Experiencia_Evidencia y no de Evidencia?* Porque cada experiencia tiene
  su propio banco: el ítem es de una evidencia *dentro de* una experiencia (H-4).
- *¿Por qué se descarta y no se borra?* Descartar es reversible y no pierde lo editado
  (RF-03-06). Por eso *genera* es **(12,N)**: la IA genera 12 y ninguno se borra.
- *¿Dónde quedó `estado_revision`?* Salió (cierra V-7). Sacarlo es una de las tres decisiones
  que el equipo tiene que confirmar:
  - Después del triaje llegó ADR-026: el banco pasa a ser del docente, no algo que solo
    revisa.
  - Ningún requerimiento ni ventana lo usa.
  - Lo que habilita a publicar es tener al menos **6 ítems activos por evidencia** (RI-14).
- *¿Y `orden_sugerido`?* También salió (H-1): los ítems se eligen al azar entre los activos que
  el estudiante no ha visto (RF-04-04).
- *¿Se puede editar un ítem ya publicado?* No: al publicar, todo el banco se congela (ADR-026,
  RI-10).

### 4.10 OPCIÓN — propia · vista 4

**Qué es.** Una opción de respuesta de un ítem.

| Atributo | Qué guarda |
|---|---|
| `id_opcion` (PK) | Identificador interno. |
| `texto` | El texto de la opción. |
| `orden` | En ordenamiento: la posición correcta. En emparejamiento: el número de pareja. Vacío en selección única. |
| `es_correcta` | Solo en selección única. |
| `grupo` | Solo en emparejamiento: `izquierda` o `derecha`. |
| `hipotesis_error` | Por qué un estudiante podría elegirla si está equivocada. **Nunca se muestra ni se reporta** (ADR-008, ADR-020). |

**Preguntas probables**
- *¿Por qué una sola entidad para los tres formatos, con columnas que a veces van vacías?*
  - Los tres formatos comparten casi todo. Tres entidades separadas complicarían cada
    consulta sin ganar nada.
  - Qué columnas aplican lo controla RI-4. La hace cumplir el servicio (`Item.esValido`),
    porque el formato está en otra tabla, Ítem, y un CHECK de MySQL no puede consultar otra
    tabla.
- *¿Cuántas opciones como mínimo?* 2 en selección única y en ordenamiento; 4 en emparejamiento,
  con al menos 2 por lado (RI-4, hallazgo H-9). Por eso *ofrece* es **(2,N)**.
- *¿Para qué guardan `hipotesis_error` si nunca se muestra?* La genera la IA junto con la opción
  y sirve para revisar la calidad del ítem. No se muestra porque el sistema nunca afirma qué
  piensa el estudiante (ADR-008: nunca lenguaje de certeza).

### 4.11 PRESENTACIÓN — **débil** · vista 5

**Qué es.** El hecho de **haber mostrado** un ítem a un estudiante. Es un hecho distinto del de
haberlo respondido (hallazgos H-2 y H-3).

| Atributo | Qué guarda |
|---|---|
| `orden_presentacion` | Su lugar en la secuencia de todo el diagnóstico de esa inscripción (1, 2, 3…). Único dentro de la inscripción (RI-8). |
| `fecha_presentacion` | Cuándo se mostró. |

**Por qué es débil.**
- **La identifican dos dueñas a la vez:** la inscripción (*atiende*) y el ítem (*se
  presenta*). Las dos son identificadoras: rombo doble.
- **No necesita llave parcial.** En la base su llave es `(id_inscripcion, id_item)`, y eso
  además garantiza que **a un estudiante no se le muestra dos veces el mismo ítem**.

**Preguntas probables**
- *¿Para qué separar «mostrar» de «responder»?*
  - Para representar «se le mostró y no respondió» (H-3).
  - Esa presentación sin respuesta es la pregunta que el estudiante verá otra vez al volver
    (ADR-031).
  - Con orden y fecha se reconstruye la secuencia adaptativa completa (H-2).
- *Si la identifican inscripción e ítem, ¿no es una relación N:M?* Podría dibujarse así, pero
  participa en otra relación, *registra* una respuesta, así que tiene que ser entidad. Al
  ser débil de las dos, su llave sale de ellas sin inventar un número interno.
- *¿Cómo se asegura que el ítem sea de la experiencia del estudiante?* Es el ciclo **C2**
  (RI-13); ver la sección 6.

### 4.12 RESPUESTA — propia · vista 6

**Qué es.** Lo que el estudiante respondió a un ítem que se le presentó, con su certeza.

| Atributo | Qué guarda |
|---|---|
| `id_respuesta` (PK) | Identificador interno. |
| `certeza` | De 0 («Adiviné») a 5 («Segurísimo/a»): escala CRI (Hasan et al., 1999). De 3 a 5 es señal fuerte (RF-04-07). CHECK entre 0 y 5. |
| `correcta` (**D**, se guarda) | Si acertó. En emparejamiento y ordenamiento, verdadero solo si todo está bien. |
| `fecha_respuesta` | Cuándo confirmó. |

**Preguntas probables**
- *¿Por qué cuelga de Presentación y no de Ítem e Inscripción?* Porque no existe respuesta sin
  presentación: es imposible por estructura (H-3).
- *¿Por qué es propia y no débil o asociativa?*
  - **No es asociativa.** Antes figuraba como asociativa, pero desde H-3 cuelga de una sola
    entidad y no resuelve ninguna N:M. La asociativa de esa parte es Respuesta_Opción.
  - **Tiene dependencia de existencia, no de identificación.** Su participación total en
    *registra* (línea doble, (1,1)) ya dice que no existe sin su presentación. Pero es un
    evento con identidad propia, y así la trató la Quinta revisión: lleva llave interna.
  - **En la base**, un UNIQUE(`id_inscripcion`, `id_item`) asegura una sola respuesta por
    presentación.
  - **Modelarla débil también era válido;** se eligió propia.
- *¿Por qué `correcta` se guarda si se puede calcular?*
  - Es una fotografía del momento (ADR-021), y el reporte no tiene que recalcular cada
    respuesta.
  - La regla RI-11 exige que el valor guardado coincida con el recálculo, y siempre coincide
    porque el banco está congelado.
- *¿Se puede cambiar una respuesta?* Nunca: es un hecho (RNF-10).

### 4.13 RESPUESTA_OPCIÓN — **asociativa** · vista 6

**Qué es.** Qué opción u opciones eligió el estudiante, no solo si acertó.

| Atributo | Qué guarda |
|---|---|
| `valor_dado` | En selección única: vacío, porque la fila ya es la elección. En ordenamiento: la posición que le asignó. En emparejamiento: el número de pareja. |

**Preguntas probables**
- *¿Para qué guardar las opciones si ya está `correcta`?* Sin esto, emparejar y ordenar no
  serían representables. Además, el historial (CU-29) muestra *qué* respondió, no solo si
  acertó (ADR-019).
- *¿Por qué esta asociativa se dibuja con el rombo *selecciona* y Experiencia_Evidencia no?*
  Porque esta no participa en ninguna otra relación: es la N:M Respuesta–Opción con un
  atributo. Experiencia_Evidencia e Inscripción sí participan en otras relaciones, así que
  son entidades completas.
- *¿Cómo se asegura que la opción sea del ítem presentado?* Es el ciclo **C4** (RI-6).

### 4.14 RESULTADO — **débil** · vista 7

**Qué es.** Lo que las respuestas de un estudiante permiten concluir sobre una evidencia.

| Atributo | Qué guarda |
|---|---|
| `estado` (**D**, se guarda) | `muestra`, `no_muestra` o `no_concluyente`, con la regla adaptativa (RF-04-07). |
| `fecha_calculo` | Cuándo se concluyó. Una fotografía sin fecha no se puede auditar. |

**Por qué es débil.**
- **La identifican dos dueñas:** la inscripción (*arroja*) y la evidencia incluida (*mide*).
- **Un solo resultado por evidencia por estudiante:** RI-2 lo garantiza la propia llave.

**La regla adaptativa (por si pregunta cómo se concluye).**
1. Con menos de 4 respuestas en la evidencia, se sigue preguntando.
2. Desde la 4.ª, cada respuesta con certeza de 3 a 5 es una **señal fuerte**: de «muestra» si
   es correcta, de «no muestra» si no. Con certeza de 0 a 2, la señal es débil.
3. Si más de la mitad son señales fuertes de «muestra», concluye **Muestra**. Si más de la
   mitad son de «no muestra», concluye **No muestra**.
4. Si no, y ya van 6 respuestas, concluye **No concluyente**.

Mínimo 4, tope 6, certeza fuerte desde 3 (ADR-016, RF-04-07). Está programada y probada en
`uml/regla.py`. Esto cerró el vacío V-5 y el hallazgo H-7.

**Preguntas probables**
- *¿Por qué `estado` se guarda y el Reporte no?* El resultado es la conclusión **en un
  momento** (RNF-11), y no cambia. El reporte agrega todos los resultados cada vez que se
  abre, y si se guardara quedaría viejo con el siguiente resultado.
- *¿Por qué no hay un estado «sin concluir» en Resultado?* Porque «sin concluir» es justamente
  **no tener** resultado todavía. Lo calcula el Reporte.
- *¿El estudiante ve su resultado?* No: el diagnóstico no le muestra resultados (ADR-028,
  RF-04-08).

### 4.15 REPORTE — **derivada**, no se guarda · vista 7

**Qué es.** El resumen de una experiencia, calculado sobre los resultados cada vez que el
docente lo abre.

| Atributo | Cómo se calcula |
|---|---|
| `estado_general` (**C**) | Por estudiante, con precedencia (ADR-022, CU-30). Se aplica la primera que se cumpla. |
| `estado_por_evidencia` (**C**) | Por evidencia, sobre los N inscritos (CU-27). Se aplica la primera que se cumpla. |

Las reglas de `estado_general`, en orden de precedencia:
1. Alguna evidencia es «no muestra» → **No muestra**.
2. Todas están concluidas y todas son «muestra» → **Muestra**.
3. Todas están concluidas y alguna es «no concluyente» → **No concluyente**.
4. Si falta concluir alguna → **Sin concluir**.

Las reglas de `estado_por_evidencia`:
1. «No concluyente» más «sin concluir» suman al menos el 40 % de N → **Datos insuficientes**.
2. Si no, alguien tiene «no muestra» → **Brecha aparente**.
3. Si no → **Sin brecha aparente**.

Los umbrales son fijos (ADR-013, ADR-017, ADR-023).

**Preguntas probables**
- *¿Por qué está en el MER si no es una tabla?* Porque es información que el sistema entrega y
  el profesor tiene que ver de dónde sale. Se dibuja punteada (derivada), igual que sus dos
  relaciones, y no cuenta entre las 15 entidades.
- *¿En la base qué es?* Una consulta, no una tabla.

---

## 5. Relación por relación

Cómo leer cada fila en voz alta: «Un A se relaciona con (mín,máx de A) B; cada B con (mín,máx
de B) A».

| Relación | Razón | Lectura en voz alta | Por qué así |
|---|---|---|---|
| CREDENCIAL *accede como* DOCENTE {xor} | 1:1 | Una credencial accede como a lo sumo un docente (0,1); cada docente tiene exactamente una credencial (1,1). | Mínimo 0 en la credencial: mientras el registro está en curso todavía no tiene rol. |
| CREDENCIAL *accede como* ESTUDIANTE {xor} | 1:1 | Igual que la anterior, con estudiante. | El {xor} dice que una credencial accede a uno **o** al otro, nunca a los dos (RI-12). |
| DBA *comprende* EVIDENCIA (identificadora) | 1:N | Un DBA comprende una o más evidencias (1,N); cada evidencia es de exactamente un DBA (1,1). | Identificadora: la evidencia es débil. |
| EVIDENCIA *se dictamina* EVIDENCIA_DICTAMEN (identificadora) | 1:1 | Una evidencia tiene a lo sumo un dictamen (0,1); cada dictamen es de exactamente una evidencia (1,1). | Mínimo 0: el censo QA-014 no ha terminado, así que puede haber evidencias sin dictamen. |
| DOCENTE *crea* EXPERIENCIA | 1:N | Un docente crea cero o más experiencias (0,N); cada experiencia la crea exactamente un docente (1,1). | Un docente recién registrado no tiene ninguna. |
| EXPERIENCIA *se ancla a* DBA | N:1 | Cada experiencia se ancla a exactamente un DBA (1,1); un DBA tiene cero o más experiencias (0,N). | «Una experiencia, un DBA» (RF-02-02). |
| EXPERIENCIA *incluye* EXPERIENCIA_EVIDENCIA | 1:N | Una experiencia incluye una o más evidencias (1,N); cada evidencia incluida es de exactamente una experiencia (1,1). | Sin evidencias no hay banco. |
| EVIDENCIA *sobre* EXPERIENCIA_EVIDENCIA | 1:N | Una evidencia está incluida en cero o más experiencias (0,N); cada evidencia incluida es sobre exactamente una evidencia (1,1). | — |
| EXPERIENCIA_EVIDENCIA *genera* ÍTEM | 1:N | Cada evidencia incluida genera **12 o más** ítems (12,N); cada ítem es de exactamente una (1,1). | La IA genera 12 por evidencia (RF-03-01) y ninguno se borra: descartar solo excluye. |
| ÍTEM *ofrece* OPCIÓN | 1:N | Un ítem ofrece **2 o más** opciones (2,N); cada opción es de exactamente un ítem (1,1). | El mínimo sube a 4 en emparejamiento (RI-4). |
| ESTUDIANTE *realiza* INSCRIPCIÓN | 1:N | Un estudiante tiene cero o más inscripciones (0,N); cada inscripción es de exactamente un estudiante (1,1). | — |
| INSCRIPCIÓN *pertenece a* EXPERIENCIA | N:1 | Cada inscripción pertenece a exactamente una experiencia (1,1); una experiencia tiene cero o más (0,N). | De aquí sale el contador de estudiantes. |
| INSCRIPCIÓN *atiende* PRESENTACIÓN (identificadora) | 1:N | Una inscripción tiene cero o más presentaciones (0,N); cada una es de exactamente una inscripción (1,1). | Cero: se unió y todavía no empieza. |
| ÍTEM *se presenta* PRESENTACIÓN (identificadora) | 1:N | Un ítem se presenta cero o más veces (0,N); cada presentación es de exactamente un ítem (1,1). | Cero: un ítem puede no salir nunca al azar. |
| PRESENTACIÓN *registra* RESPUESTA | 1:1 | Una presentación registra a lo sumo una respuesta (0,1); cada respuesta es de exactamente una presentación (1,1). | El 0 es «se le mostró y no respondió» (H-3). |
| RESPUESTA *selecciona* OPCIÓN, vía RESPUESTA_OPCIÓN | N:M | Una respuesta selecciona una o más opciones (1,N); una opción puede ser elegida en cero o más respuestas (0,N). | Al menos una (RI-6); en selección única, exactamente una. |
| INSCRIPCIÓN *arroja* RESULTADO (identificadora) | 1:N | Una inscripción arroja cero o más resultados (0,N); cada resultado es de exactamente una (1,1). | Uno por evidencia concluida. |
| EXPERIENCIA_EVIDENCIA *mide* RESULTADO (identificadora) | 1:N | Una evidencia incluida tiene cero o más resultados (0,N); cada resultado mide exactamente una (1,1). | — |
| RESULTADO *se agrega en* REPORTE (derivada) | N:1 | Cada resultado se agrega en el reporte de su experiencia. | Derivada: no se guarda. |
| REPORTE *resume* EXPERIENCIA (derivada) | 1:1 | Cada experiencia tiene un reporte, que se calcula al abrirlo. | Derivada: no se guarda. |

**Las relaciones identificadoras (rombo doble) son 6, para 4 débiles:**
- *comprende*, para Evidencia
- *se dictamina*, para el Dictamen
- *atiende* y *se presenta*, las dos de Presentación
- *arroja* y *mide*, las dos de Resultado

---

## 6. Los ciclos: la parte que más impresiona, y cómo explicarla fácil

**Qué es un ciclo.** Un camino de relaciones que sale de una entidad y vuelve a ella. Cuando al
volver algo tiene que coincidir, el diagrama solo no lo puede garantizar. Ejemplo: que la
evidencia incluida sea del mismo DBA de la experiencia.

**Por qué importan.** El profesor lo dijo en H-4: *«un ciclo que hay que restringir con una
regla externa suele indicar que falta una entidad»*. Por eso revisamos **todos**.

**Por qué son exactamente 5.**
- El grafo tiene 15 entidades y 19 aristas. Son 19 y no 18 porque *selecciona* pasa por
  Respuesta_Opción y cuenta como dos.
- Un grafo conexo tiene **aristas − nodos + 1** ciclos independientes: 19 − 15 + 1 = **5**.
- Cualquier otro ciclo es combinación de esos 5.
- El verificador `mer/_verificar_mer.py` comprueba que sean exactamente esos, que existan y que
  ninguno sea combinación de los otros.

| Ciclo | El camino | Qué tiene que coincidir | Cómo se cierra |
|---|---|---|---|
| **C1** | Experiencia → Exp_Evidencia → Evidencia → DBA → Experiencia | Que la evidencia incluida sea **del DBA** de la experiencia | RI-18, por estructura |
| **C2** | Inscripción → Presentación → Ítem → Exp_Evidencia → Experiencia → Inscripción | Que el ítem presentado sea **de la experiencia** del estudiante | RI-13, por estructura |
| **C3** | Inscripción → Resultado → Exp_Evidencia → Experiencia → Inscripción | Que el resultado sea de una evidencia **de la experiencia** del estudiante | RI-13, por estructura |
| **C4** | Respuesta → Presentación → Ítem → Opción → Respuesta_Opción → Respuesta | Que la opción elegida sea **del ítem que se presentó** | RI-6, por estructura |
| **C5** | Credencial → Docente → Experiencia → Inscripción → Estudiante → Credencial | Nada | No necesita regla: el {xor} hace que los dos extremos sean siempre credenciales distintas |

**«Por estructura», explicado sin tecnicismos.** Tomar C2 como ejemplo:
- La tabla `presentacion` guarda **también** `id_experiencia`.
- Esa columna está dentro de dos llaves foráneas compuestas a la vez:
  - `(id_inscripcion, id_experiencia)` apunta a la inscripción
  - `(id_item, id_experiencia)` apunta al ítem
- Como la misma columna tiene que calzar con las dos, la base **rechaza sola** una
  presentación de un ítem de otra experiencia. No hace falta trigger ni código.
- C1, C3 y C4 usan la misma técnica:

  | Ciclo | Columna compartida | Tabla |
  |---|---|---|
  | C1 | `codigo_dba` | `experiencia_evidencia` |
  | C3 | `id_experiencia` | `resultado` |
  | C4 | `id_item` | `respuesta_opcion` |

**Si pregunta «¿eso no viola la normalización?».**
- Sí, en sentido estricto es una redundancia: depende de una parte de la llave, así que viola
  la 2FN.
- Es **deliberada** y no puede quedar inconsistente, porque las mismas llaves foráneas obligan
  a que coincida.
- A cambio, cuatro reglas pasan de «el programa debe acordarse» a «la base no lo permite».
- Está documentado en el documento 17, §5 y §6.

**La prueba.** C1 y C4 estaban abiertos en el borrador: la base aceptaba incluir una evidencia
de otro DBA, o elegir una opción de otro ítem. Las pruebas (`pruebas_mr.py`) intentan
exactamente eso y ahora la base lo rechaza, en SQLite y en MySQL.

---

## 7. Las 19 restricciones de integridad, en una línea cada una

«Motor» = la base de datos lo impide sola. «Servicio» = lo controla el backend, porque depende
de otra tabla o del momento.

| RI | Qué dice | Quién la hace cumplir |
|---|---|---|
| RI-1 | Un estudiante se une una sola vez a cada experiencia. | Motor: UNIQUE |
| RI-2 | Un solo resultado por evidencia por inscripción. | Motor: la llave de la débil |
| RI-3 | El correo es único entre los dos roles; el código de invitación es único, de 6 caracteres sin 0/O/1/I/L. | Motor: UNIQUE y CHECK |
| RI-4 | Las columnas de Opción y sus mínimos dependen del formato (2 / 2 / 4). | Servicio |
| RI-5 | Solo se incluyen evidencias cuyo dictamen admite formato cerrado. | Servicio |
| RI-6 | Toda respuesta elige al menos una opción, **solo del ítem presentado**; una sola en selección única. | Motor (ciclo C4) y servicio |
| RI-7 | Una experiencia en Borrador no admite inscripciones. | Servicio |
| RI-8 | El orden de presentación no se repite dentro de una inscripción. | Motor: UNIQUE y CHECK |
| RI-9 | No más de 6 presentaciones por evidencia, ni más que los ítems activos. | Servicio (la regla) |
| RI-10 | Ítem y Opción no cambian una vez presentados (el banco se congela al publicar). | Servicio |
| RI-11 | `correcta` y `estado` se guardan y coinciden con el recálculo. | Servicio |
| RI-12 | Una credencial, a lo sumo un rol ({xor}); cada persona, una credencial. | Motor: CHECK y UNIQUE |
| RI-13 | El ítem presentado y la evidencia del resultado son de la experiencia de la inscripción. | Motor (ciclos C2 y C3) |
| RI-14 | Solo se publica con al menos 6 ítems activos por evidencia. | Servicio |
| RI-15 | Cuenta de correo: con contraseña y sin identificador externo. Google o Microsoft: con identificador, sin contraseña y con el correo verificado. | Motor: CHECK |
| RI-16 | `fecha_publicacion` vacía si y solo si está en Borrador. | Motor: CHECK |
| RI-17 | Un banco sale de un solo servicio y modelo, guardados en la experiencia. | Motor: columnas obligatorias en experiencia |
| RI-18 | Las evidencias incluidas son del DBA de la experiencia. | Motor (ciclo C1) |
| RI-19 | El dictamen que admite formato cerrado dice cuál; el ítem usa ese formato. | Motor: CHECK, y servicio |

**Si pregunta por qué no usaron triggers:** para que cada regla de negocio viva en un solo
lugar y se pueda probar. Lo que la base puede impedir sola, lo impide la base. El resto lo
controla un servicio con nombre, que está en la tabla del documento 17, §7.

---

## 8. Derivados: D y C, la diferencia exacta

| | **D — derivado que se guarda** | **C — calculado, no se guarda** |
|---|---|---|
| Cuáles | `Respuesta.correcta`, `Resultado.estado` | `Inscripcion.progreso`, `Reporte.estado_general`, `Reporte.estado_por_evidencia` |
| Por qué | Son una **fotografía del momento** (ADR-021, RNF-11) y no cambian después | Cambian cada vez que llega algo nuevo; guardarlos los dejaría viejos (ADR-022) |
| En la base | Tienen columna | No tienen columna |
| En el diagrama | Elipse punteada, rótulo «derivado · se guarda» | Elipse punteada, rótulo «calculado» |

---

## 9. Del MER al modelo relacional, por si pregunta «¿y cómo queda en la base?»

| En el MER | En la base |
|---|---|
| Entidad propia | Tabla con llave interna `id_<tabla>` (número autoincremental). La excepción es DBA, que usa el código del MEN. |
| Relación 1:N | Llave foránea en el lado N. Si el mínimo de ese lado es 1 (línea doble), la columna es obligatoria (NOT NULL). |
| Relación 1:1 *accede como* | `id_docente` / `id_estudiante` en `credencial`, opcionales (el mínimo es 0) y con UNIQUE (es 1:1). Un CHECK impide que estén las dos (RI-12). |
| Entidad débil | Su llave primaria es la de su(s) dueña(s) más su llave parcial, si la tiene. Llave foránea con borrado en cascada. |
| N:M *selecciona* | Tabla `respuesta_opcion`, con llave `(id_respuesta, id_opcion)`. |
| Asociativas que participan en otras relaciones | Tablas propias: `experiencia_evidencia`, `inscripcion`. |
| Atributo C | No tiene columna. |
| Reporte | No es tabla: es una consulta. |

**Borrado (pregunta probable).**
- **Solo tres cosas se borran directamente:**
  - una experiencia (CU-15)
  - una inscripción (el estudiante sale, CU-26)
  - una opción mientras se edita un ítem en Borrador (CU-18)
- **Todo lo que cuelga de ellas cae en cascada.**
- **La cascada nunca toca** una cuenta ni el currículo: esas llaves están en RESTRICT.
- Esto cerró el vacío V-11.

**Lo que nunca se modifica:** Presentación, Respuesta, Respuesta_Opción y Resultado. Son hechos
y fotografías (RNF-10, RNF-11).

---

## 10. La revisión del profesor: qué decir de cada hallazgo

| # | Lo que señaló | Qué decir |
|---|---|---|
| H-1 | La configuración del diagnóstico no tenía dónde vivir | Dejó de ser decisión del docente: el mínimo 4 y el tope 6 son fijos (ADR-016), y el orden es el oficial del DBA (ADR-024). Lo que sigue vigente de su punto es H-4. |
| H-2 | No se podía reconstruir la secuencia adaptativa | Presentación guarda qué ítem, en qué orden y cuándo. |
| H-3 | «Se le presentó y no respondió» no era representable | *registra* es (0,1) del lado de Presentación: una presentación sin respuesta es exactamente eso. |
| H-4 | Faltaba el vínculo Experiencia–Evidencia | Experiencia_Evidencia. Y aplicamos su criterio a todo el modelo: 5 ciclos, todos declarados y cerrados. |
| H-5 | Faltaba `estado_revision` | En parte. `origen` distingue IA, editado y creado. `estado_revision` salió por ADR-026, y esa es una decisión que el equipo debe confirmar. Publicar exige 6 activos por evidencia (RI-14). |
| H-6 | `aplica_formato_cerrado` colgaba de un dato del MEN | Evidencia_Dictamen, separada, que ahora además guarda el formato. |
| H-7 | La regla de parada no estaba definida | RF-04-07 la define (mínimo 4, tope 6, señal fuerte desde certeza 3), y está programada y probada. |
| H-8 | El MER mostraba llaves foráneas | Chen estricta: sin llaves foráneas y con llave parcial. |
| H-9 | No estaban fijados los mínimos de opciones | 2 en selección única y ordenamiento, 4 en emparejamiento (RI-4); es el (2,N) de *ofrece*. |
| H-10 | Convivían varias versiones del MER | El vigente es el documento 16; el borrador lleva su aviso. |
| H-11 | Las fuentes citadas no venían en la carpeta | Resuelto: en el repositorio están `docs/diseno/` (las ADR) y el currículo del MEN, junto a la metodología. |
| H-12 | La Fase II no diseñó la toma ni el reporte | Se cerró con las ventanas 020 a 023, 010 y 027. |

**De la v3 del profesor tomamos:**
- su `estado_avance`, que es nuestro `progreso`, calculado
- su `calculado_en`, que es nuestro `fecha_calculo`
- su orden único por inscripción, que es RI-8
- su tope de presentaciones, que es RI-9
- su notación (mín, máx)
- su vacío de autenticación, que resolvimos con CREDENCIAL

**Lo que agregamos sobre la v3:**
- la credencial, con sus dos relaciones excluyentes
- los ciclos declarados
- las restricciones RI-12 a RI-19

---

## 11. Preguntas difíciles (y trampa), con respuesta

**Sobre el diseño general**

1. *¿Por qué 15 entidades y no menos?* Cada una responde a un requerimiento o a un hallazgo
   suyo: Credencial (V-8), Evidencia_Dictamen (H-6), Experiencia_Evidencia (H-4), Presentación
   (H-2, H-3). Si se quita cualquiera, deja de poder representarse algo que el sistema hace.
2. *¿Por qué Reporte no cuenta como entidad?* Porque no se guarda: se calcula al abrirlo
   (ADR-022). Se dibuja punteada para que se vea de dónde sale.
3. *¿Cómo saben que el MER y la base no se contradicen?*
   - **Hay verificadores automáticos:**
     - cada llave foránea sale de una relación, y cada relación tiene su llave foránea
     - las clases coinciden con las entidades
     - el diagrama de objetos se carga en la base real sin errores
   - **Hay 49 pruebas** que intentan meter datos inválidos, en SQLite y en MySQL 8.4.
4. *¿Por qué siete vistas?* Siguen el ciclo de vida del sistema: acceso, currículo, autoría,
   banco, entrega, respuesta, conclusión. Cada relación está en exactamente una vista, y un
   verificador lo comprueba. Una entidad que reaparece en otra vista se dibuja sin atributos,
   como «costura».

**Sobre cardinalidad**

5. *¿Qué diferencia hay entre 1:N y (0,N)?* La razón 1:N es el tipo de relación (se lee
   cruzando). El (0,N) junto a la entidad es cuántas veces participa *un* ejemplar de esa
   entidad (se lee aquí mismo).
6. *¿Por qué (12,N) y no (1,N) en genera?* Porque la IA genera 12 por evidencia y ninguno se
   borra; descartar solo los excluye. El mínimo real es 12.
7. *Si se descartan 7 de 12, ¿no se rompe el (12,N)?* No: descartar no borra. Siguen siendo 12
   ítems, de los que 5 están activos. Lo que exige 6 **activos** es publicar (RI-14), no el
   MER.
8. *¿Por qué la credencial tiene mínimo 0 en accede como, si toda persona tiene rol?* Porque
   entre «verificar el correo» y «elegir el rol» la credencial existe sin rol (RF-01-05).
9. *¿Qué pasa si la persona nunca elige rol?* Queda una credencial sin rol. Al iniciar sesión
   se la manda a completar el perfil (CU-06, alterno 3a); esa es una decisión del equipo,
   por confirmar.

**Sobre entidades débiles y asociativas**

10. *¿Cuál es la diferencia entre débil y asociativa?*
    - **Débil:** no tiene identidad propia y la toma de su dueña, por una relación
      identificadora.
    - **Asociativa:** resuelve una relación entre entidades y además tiene atributos o
      relaciones propias.
    - Presentación y Resultado podrían verse como asociativas. Se modelaron como débiles con
      dos dueñas porque su identidad *es* la combinación de esas dos.
11. *¿Por qué Inscripción tiene llave propia y Experiencia_Evidencia no?*
    - Inscripción tiene llave propia para que Presentación y Resultado no arrastren una
      llave doble.
    - Experiencia_Evidencia no la tiene a propósito: su llave compuesta lleva `codigo_dba`
      hacia abajo, y eso es lo que cierra C1 y RI-13 por estructura.
12. *¿Respuesta no debería ser débil de Presentación?* Podría. Se eligió propia porque su
    dependencia es de existencia, que ya la dice su línea doble, y no de identificación: es
    un evento con identidad propia. Un UNIQUE en la base asegura una respuesta por
    presentación. Las dos opciones son válidas.
13. *¿Por qué Evidencia_Dictamen es débil si es 1:1?* Porque no existe sin la evidencia que
    dictamina, y la identifica esa misma evidencia. Al ser 1:1, no hace falta llave parcial.

**Sobre atributos**

14. *¿Por qué `correcta` se guarda si se puede calcular?* Es una fotografía (ADR-021), y la
    regla RI-11 exige que coincida con el recálculo.
15. *¿Por qué `progreso` no se guarda?* Se deduce de presentaciones y resultados; guardarlo
    sería duplicar el dato (ADR-022).
16. *¿Dónde está el área de la experiencia?* En su DBA. No se repite.
17. *¿Por qué `hipotesis_error` existe si nunca se muestra?* La genera la IA y sirve para
    revisar la calidad del ítem. El sistema nunca afirma qué piensa el estudiante (ADR-008).
18. *¿Por qué hay columnas en la base que no están en el MER?* Hay dos clases:
    - **Llaves foráneas.** No se dibujan en Chen.
    - **Seguridad del backend:** intentos, bloqueo y `actualizado_en`. Son mecanismo, no
      dominio, y están justificadas en el documento 17.
    - Un verificador comprueba que cada columna «extra» esté justificada.

**Sobre las reglas**

19. *¿Qué impide que a un estudiante se le muestre un ítem de otra experiencia?* La estructura
    (ciclo C2, RI-13): la base lo rechaza sola.
20. *¿Qué impide mostrarle dos veces el mismo ítem?* La llave de Presentación,
    `(id_inscripcion, id_item)`.
21. *¿Qué impide que un banco mezcle Gemini y DeepSeek?* Que el servicio se guarda una sola vez,
    en la experiencia (RI-17).
22. *¿Qué impide editar el banco después de publicar?* El servicio
    (`Experiencia.bancoEditable`, RI-10), porque depende del estado de otra tabla.
23. *¿Qué pasa con todo al eliminar una experiencia?* Se borra en cascada: evidencias incluidas,
    ítems, opciones, inscripciones, presentaciones, respuestas y resultados. Las cuentas y el
    currículo no se tocan. Hay una prueba que lo cuenta tabla por tabla.

**Sobre lo que no está**

24. *¿Por qué no hay práctica ni verificación después del diagnóstico?* Fuera de alcance
    (ADR-007).
25. *¿Por qué no se guarda la autorización del acudiente?* Fuera de esta versión (ADR-029). Por
    eso el sistema no se usa con estudiantes reales (RNF-06).
26. *¿Por qué no se versiona el ítem?* Diferido (V-9) y casi innecesario: el banco se congela al
    publicar, y antes de publicar no hay respuestas.

---

## 12. Lo que está abierto, y cómo decirlo sin que suene a hueco

| Pendiente | Cómo decirlo |
|---|---|
| **V-6 / QA-014** | «La tabla del dictamen existe y la base ya exige que sea coherente; faltan los **valores**, que salen del censo de formato cerrado. No frena el desarrollo.» |
| **V-12** | «Qué muestra la pantalla con un DBA sin evidencias admitidas. El MER ya impide crear esa experiencia; falta definir el mensaje, y depende del mismo censo.» |
| **V-9** | «Versionar ítems: diferido, porque el banco se congela al publicar.» |
| **Tres decisiones del equipo** | «Están marcadas como decisiones nuestras, para confirmar: sacar `estado_revision`, retomar un registro a medias y tratar un ítem inválido de la IA como falla del servicio.» |
| **ADR-030** | «Su punto 4 dice que cada ítem guarda el servicio de IA; nosotros lo guardamos una vez en la experiencia, porque su punto 3 dice “un banco, un servicio”. El propósito se mantiene; el equipo lo tiene que confirmar.» |
| **MariaDB** | «El esquema no usa nada que MariaDB no tenga, pero solo lo ejecutamos en MySQL 8.4, que es lo que pide RNF-14.» |

---

## 13. Errores que conviene no cometer al explicar

- **No decir «llave foránea» señalando el diagrama Chen.** Ahí no hay FK, y es justo lo que
  corrigió H-8. Decir «la relación *crea*», y dejar las FK para el modelo relacional.
- **No decir que Reporte es una tabla.** Se calcula.
- **No decir que el estudiante ve sus resultados.** No los ve (ADR-028).
- **No decir que el docente elige las evidencias.** Entran todas las que el dictamen admite
  (QA-010).
- **No decir que descartar borra.** Descartar excluye, y es reversible.
- **No confundir Presentación con Respuesta.** Presentación es «se mostró», Respuesta es «se
  respondió». Puede haber presentación sin respuesta, pero nunca respuesta sin presentación.
- **No decir «certeza» como si el sistema estuviera seguro.** Certeza es lo que **declara el
  estudiante** (0 a 5). El sistema nunca usa lenguaje de certeza (ADR-008).

---

## 14. Tarjeta de bolsillo (para repasar 5 minutos antes)

- **15 + 1** entidades · **18 + 2** relaciones · **62** atributos · **5** ciclos · **19** RI.
- **4 débiles:** Evidencia (con llave parcial), Dictamen, Presentación, Resultado.
- **3 asociativas:** Experiencia_Evidencia, Inscripción, Respuesta_Opción.
- **2 que se guardan (D):** `correcta` y `estado`.
- **3 que se calculan (C):** `progreso`, `estado_general` y `estado_por_evidencia`.
- **{xor}:** una credencial, un solo rol.
- **(12,N)** en *genera*; **(2,N)** en *ofrece*; **(0,1)** en *registra*.
- **Ciclos:** C1 (RI-18), C2 y C3 (RI-13), C4 (RI-6), cerrados por la estructura; C5 no
  necesita regla.
- **La regla adaptativa:** mínimo 4, tope 6, señal fuerte con certeza de 3 a 5, mayoría.
- **Se borra directo** solo una experiencia, una inscripción o una opción en Borrador; todo lo
  demás, en cascada.
- **Nunca cambian:** Presentación, Respuesta, Respuesta_Opción y Resultado.
