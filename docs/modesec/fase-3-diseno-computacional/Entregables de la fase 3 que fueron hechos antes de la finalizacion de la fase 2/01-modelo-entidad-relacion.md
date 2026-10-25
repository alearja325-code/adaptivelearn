# Modelo Entidad-Relación — AdaptiveLearn (rediseño)

> **⚠ BORRADOR ANTERIOR AL CIERRE DE LA FASE II — no es fuente de verdad.**
> Se hizo entre agosto y septiembre de 2026, mientras la Fase II seguía
> abierta. Después cambiaron decisiones que lo afectan (ADR-026 a
> ADR-029, entre otras). La fuente de verdad es la Fase I, la Fase II y
> `diseno/decisiones.md`; la Fase III se rehace en orden desde
> `10-proceso-desarrollo.md`, y este documento se usa como insumo, no como
> base. Lo que el modelo nuevo debe recibir está en `diseno/pendientes.md`,
> sección "Entrada a Fase III". *(Aviso agregado el 2026-10-21, decisión
> de Alejandro.)*

**Metodología:** MODESEC — Fase III, Diseño Computacional.

**Este fue el MER vigente del proyecto hasta el 2026-10-21** (ver aviso arriba). Cualquier otra versión que
circule —la del 2026-08-20 que revisó el docente, la propuesta v3 de su
crítica, o la reconstruida por el otro grupo desde una imagen— está
superada por este documento. *(Cierra el hallazgo H-10 del docente: que
convivan varias versiones sin que ninguna se declare vigente ya costó que
otro grupo dedicara un informe entero a revisar un modelo que no era el
nuestro.)*

**Estado:** confirmado — 2026-08-18. **Revisado** 2026-08-25, 2026-08-26
y **2026-09-08** (ver las secciones de revisión al final). La Quinta
revisión (2026-09-08) responde a dos revisiones externas: la crítica del
docente Ali del 2026-09-01 y el informe del otro grupo del 2026-09-07.

**14 entidades** (Reporte no cuenta: es vista derivada, no persiste),
**16 relaciones** entre entidades reales (más 2 derivadas, hacia
Reporte, que no cuentan), **11 restricciones de
integridad** y **9 vacíos declarados** — de los cuales 4 ya están
resueltos y se dejan anotados para no perder el rastro.

**Notación: Chen.** Rectángulos para entidades, rombos para relaciones,
elipses para atributos. *(Decidido en la Quinta revisión, cerrando el
hallazgo H-8: el docente Ali acepta ambas notaciones, el docente
Alexander no acepta caja-tabla. Chen satisface a los dos y es la correcta
para este artefacto — con las llaves foráneas dentro de las cajas, como
señala el propio H-8, "el MER ya es casi el MR". La versión caja-tabla
—`diagrama/bt_*`— queda como vista de apoyo, no como el entregable.)*

**Razón de cardinalidad.** Debajo de cada rombo va la razón de
cardinalidad de la relación (`1:1`, `1:n`, `n:m`). Es la misma
información que los `1`/`N` de las líneas, resumida en una sola
etiqueta; se incluye porque es convención establecida de la notación y
la referencia de clase la trae, no porque agregue un dato nuevo. No debe
confundirse con la **participación**, que es lo que expresan las líneas
simple (parcial) y doble (total). Cuando un lado es opcional —el caso de
`registra`, con participación (0,1)— la razón sigue siendo `1:1`: la
opcionalidad es participación, no tipo de relación. La razón se deriva
en código de `card_a`/`card_b` en `diagrama/datos_mer.py`, nunca se
escribe a mano en el trazado.

**Diagrama:** `mer-entrega/` — el **mapa completo** (`mapa-chen.svg`),
seis vistas en Chen (`vista1.svg` a `vista6.svg`, con sus PNG), leyenda
de notación, y `mer-vistas-chen.html` con todo junto y su párrafo de
justificación cada uno. Generados desde `diagrama/construir_vistas.py`.

El mapa completo y las vistas **no son dos modelos**: los dos se generan
de `diagrama/datos_mer.py`, así que no pueden decir cosas distintas. La
única diferencia es que el mapa no dibuja los atributos —son 74 elipses,
y en un lienzo único dejan de leerse—; el detalle vive en las vistas. En
el mapa, las 16 relaciones propias quedan ortogonales y sin cruces; el
único cruce cae sobre `se agrega en`, que es derivada (punteada), donde
se lee como la capa calculada pasando sobre la capa que sí se almacena.

**Verificación geométrica.** `diagrama/_verificar_mapa.py` revisa los SVG
por coordenadas —no a ojo— y falla si una línea atraviesa una caja o un
rombo ajeno, si dos rótulos se encaraman, si una línea tacha un rótulo o
si algo queda fuera del lienzo. Encontró la razón de cardinalidad tachada
por su propia línea de conexión en las vistas 2, 4 y 6, que la revisión
visual había dejado pasar.

**Las vistas se cortan por el ciclo de vida del sistema**, no por cuántas
cajas caben en la hoja: currículo → autoría → banco → entrega → captura
→ conclusión. Regla dura que las hace verificables: **cada relación se
dibuja en exactamente una vista**; si apareciera en dos, el lector no
sabría cuál leer, y si no apareciera en ninguna, faltaría sin que nadie
lo note. Eso no se comprueba a ojo — lo comprueba
`diagrama/_verificar_vistas.py`. Una entidad que reaparece en otra vista
se dibuja como **costura** (borde punteado, sin atributos, rotulada "ya
presentada · Vista N"), para que nadie cuente 20 entidades donde hay 14.

Todo el contenido sale de `diagrama/datos_mer.py`, fuente única que
alimenta también la notación caja-tabla (`diagrama/bt_*`, vista de
apoyo) — así las dos notaciones no pueden desalinearse entre sí ni de
este documento.

## Por qué esto se adelanta a Fase III sin haber cerrado Fase II

Según la fuente primaria de MODESEC, Diseño Computacional (Fase III) viene
después de Diseño Multimedial (Fase II, todavía en curso — llevamos hasta
la Vista Interna de la Experiencia, tab Materiales). Este documento se
adelanta por una razón académica real, no por descuido de orden: el curso
DSE-2 (203453) exige un modelo entidad-relación y un modelo relacional en
su Unidad 1, mientras que DSE-3 (el siguiente curso de la línea) es el que
consumirá esa interfaz — backend antes que frontend, en el orden del
programa, aunque MODESEC ubicaría este trabajo después del diseño de
interfaces. Fase II de MODESEC queda en pausa, no cancelada, y se retoma
después de esto (Vista Interna, pestaña Estudiantes, es lo próximo
pendiente ahí).

## Regla de construcción de este modelo

Cada entidad, atributo y relación de este documento tiene que poder
señalar de dónde sale — un ADR, una entrada del glosario, un campo que ya
aparece en una spec de pantalla ya escrita (`fase-2-diseno-multimedial`),
o un campo verificado directamente en los datos reales
(`curriculo_men_normalizado.json`). Nada entra por parecer razonable. El
backend existente (`mvp/backend`) no se usó como fuente para este modelo
— pertenece a la idea anterior de AdaptiveLearn, ya descartada; solo se
consultará después, de forma defensiva, para ver si algo choca por nombre
o restricción. Excepción puntual: sí se consultó
`curriculo_men_normalizado.json` como fuente de datos reales (no de
diseño) para verificar el formato real de la llave de DBA y la forma en
que se almacenan las evidencias — ver Revisión 2026-08-25.

**Convención de nombres de identificador (Segunda revisión — 2026-08-25):**
`id` pasa a `id_docente`, `id_estudiante`, `id_experiencia`,
`id_inscripcion`, `id_item`, `id_opcion`, `id_respuesta` — namespacing
simple, necesario porque el diagrama muestra las llaves foráneas dentro
de cada caja (ver más abajo); siete columnas llamadas `id` serían
ilegibles ahí, aunque en el texto de este documento no haya ambigüedad.

---

## Entidades

### Docente
**Fuente:** `04-spec-dashboard.md` (bloque de perfil).
- `id_docente` **(PK)**
- `nombre`
- `correo` **(U)** — valor único; necesario para identificar sesión,
  aunque el mecanismo de autenticación en sí quede fuera de este modelo
  (ver "Explícitamente fuera").
- `avatar_url`

Separado de Estudiante como entidad propia (no una tabla "Usuario" con
rol) — decisión de esta sesión: la relación de cada uno con Experiencia es
de naturaleza distinta (creador vs. miembro), y separarlos hace que la
estructura misma impida asignar un estudiante como creador de una
experiencia, en vez de depender de que la aplicación lo revise bien en
cada punto. Se evaluó una generalización ISA (Persona → Docente/
Estudiante) para no repetir los mismos 4 atributos en las dos entidades,
y se descarta: no es una corrección, es revertir una decisión ya
argumentada.

### Estudiante
**Fuente:** `04-spec-dashboard.md` (mismo bloque de perfil, reutilizado).
- `id_estudiante` **(PK)**
- `nombre`
- `correo` **(U)**
- `avatar_url`

### Experiencia
**Fuente:** glosario "Experiencia"; `07-spec-crear-experiencia-paso3.md`
(nombre); `04-spec-dashboard.md` (estado); `09-spec-vista-interna-marco.md`
(fecha de creación); `08-spec-unirse-codigo.md` (código de invitación).
- `id_experiencia` **(PK)**
- `id_docente` **(FK)**
- `codigo_dba` **(FK)**
- `nombre`
- `estado` — Borrador / Publicada
- `fecha_creacion`
- `fecha_publicacion` — nula mientras esté en Borrador; se llena al
  publicar. Sin ella, "cuándo se publicó" no es auditable, y publicar es
  una acción sin vuelta atrás (`15-spec-modal-confirmar-publicar.md`).
- `codigo_invitacion` **(U)** — 6 caracteres alfanuméricos, sin
  `0`/`O`/`1`/`I`/`L`; único porque un código tiene que resolver a
  exactamente una Experiencia (`08-spec-unirse-codigo.md`).

**Área y Grado no son atributos propios** — se derivan del DBA anclado, no
son datos que el docente llena aparte (confirmado en la sesión de Vista
Interna).

### DBA
**Fuente:** glosario "DBA"; ADR-005; ADR-011; `codigo_dba` verificado
contra el campo `id` real de `curriculo_men_normalizado.json` (formato
`"{área}_{grado}_dba_{número}"`, ej. `"matemáticas_1_dba_1"` — Revisión
2026-08-25).

Dato oficial del MEN, referenciado, no administrado por nosotros — no es
una tabla que creamos o editamos. Que el dato lo genere el MEN y no
nosotros no lo exime de ser identificable: sin clave, ni Ítem ni
Resultado podrían apuntarle, y el Modelo Relacional no sería derivable
desde aquí.
- `codigo_dba` **(PK)** — llave natural, no generada por nosotros; sale
  directo del dato real del MEN ya normalizado.
- `area`
- `grado`
- `enunciado`
- `ejemplo` — su rol ya está decidido (ADR-011), pero el dato **todavía
  no existe** en `curriculo_men_normalizado.json`, pendiente real.

### Evidencia
**Fuente:** glosario "Evidencia"; `numero_evidencia` y la naturaleza de
entidad débil verificados contra `curriculo_men_normalizado.json`
(Revisión 2026-08-25) — cada DBA guarda sus evidencias como una lista
ordenada de texto, sin id propio; `aplica_formato_cerrado` verificado 3
veces: ADR-006 + QA-014, modelo-conceptual.md, y directamente en la UI de
`06-spec-crear-experiencia-paso2.md` sección 2.4 (la Card de DBA ya
distingue, con tachado y texto informativo, evidencias que no aplican a
formato cerrado).

Igual que DBA, dato del MEN referenciado, no generado por nosotros.
Entidad **débil**: no tiene identidad propia fuera de su DBA — se modela
como entidad y no como atributo multivaluado de DBA porque un atributo
admite un único valor por registro y un DBA tiene varias evidencias, y
porque necesita identidad propia para relacionarse directamente con Ítem
y con Resultado.
- `codigo_dba` **(PK, FK)** — a qué DBA pertenece; relación identificadora
  (RI-1/RI-2 dependen de esto).
- `numero_evidencia` **(PK)** — posición dentro de la lista de evidencias
  de ese DBA (no existe como campo propio en la fuente, es la forma
  natural de identificar cada evidencia dentro de un DBA a partir de
  cómo el dato real ya está guardado).
- `enunciado`

**`aplica_formato_cerrado` ya no vive aquí** (Quinta revisión — 2026-09-08,
hallazgo H-6 del docente): ese dato **no lo produce el MEN**, es un
dictamen nuestro derivado de ADR-006 y pendiente del censo QA-014.
Tenerlo dentro de una entidad que el propio modelo rotula como "dato
oficial del MEN, referenciado" contradecía esa clasificación justo en el
atributo donde más importa — y borraba la frontera entre contenido
oficial y juicio propio que Fase I §2 declara como valor del proyecto.
Pasa a su propia entidad, **Evidencia_Dictamen** (ver abajo).

Pertenece a 1 DBA. El conteo de evidencias por DBA no es confiable —
bug de extracción, QA-013.

### Experiencia_Evidencia
**Fuente:** hallazgo **H-4** del docente (2026-09-01), aceptado en el
triaje del 2026-09-04. Agregada en la Quinta revisión.

Entidad **asociativa**: qué evidencias del DBA anclado diagnostica
realmente *esta* experiencia. Antes, desde una Experiencia solo se
llegaba a Evidencia por dos caminos indirectos —bajando por su DBA (que
devuelve todas, incluidas las que no aplican) o subiendo desde un Ítem—
y ese hecho, que es propio de la experiencia, no estaba en el modelo.
Las reglas RI-1 y RI-2 de la versión anterior existían solo para tapar
ese hueco; con esta entidad de por medio desaparecen, porque pasan a ser
estructura y no regla externa.
- `id_experiencia` **(PK, FK)**
- `codigo_dba` **(PK, FK)**
- `numero_evidencia` **(PK, FK)**
- `incluida` — booleano; si esta evidencia entra o no al diagnóstico de
  esta experiencia.

**No lleva `orden_evaluacion`, `items_a_presentar` ni
`tope_items_adicionales`**, los tres atributos que la propuesta del
docente sí le ponía (su hallazgo H-1). El triaje del 2026-09-04 los
encontró obsoletos: **ADR-016** le quitó al docente decidir cuántos ítems
(los fija el sistema, mínimo 4 / tope 6) y **ADR-024** eliminó el orden
de evaluación de evidencias (es el orden oficial del documento DBA del
MEN, ni sugerido por IA ni reordenable). Adoptarlos habría reintroducido
dos decisiones que este proyecto ya revocó.

### Evidencia_Dictamen
**Fuente:** hallazgo **H-6** del docente (2026-09-01), aceptado.
Agregada en la Quinta revisión.

Entidad **débil y propia**, 1:1 con Evidencia. Aloja el único dato sobre
una evidencia que **no** viene del MEN: nuestro juicio de si admite
formato cerrado.
- `codigo_dba` **(PK, FK)**
- `numero_evidencia` **(PK, FK)**
- `aplica_formato_cerrado` — booleano (ADR-006).
- `justificacion` — por qué se dictaminó así.
- `fecha_dictamen` — cuándo. Puede cambiar cuando termine el censo
  QA-014, y por eso necesita fecha.

Separarla de Evidencia no es cosmético: mantiene visible la frontera
entre contenido curricular oficial y juicio propio, que Fase I §2 declara
como valor del proyecto ("el sistema no se atribuye autoridad curricular
que no tiene").

### Presentación
**Fuente:** hallazgos **H-2** y **H-3** del docente (2026-09-01),
aceptados. Agregada en la Quinta revisión.

Entidad **débil**, identificada por la Inscripción y el Ítem a la vez.
Registra el hecho de **haber mostrado** un ítem a un estudiante — un
hecho distinto del de haberlo respondido.
- `id_inscripcion` **(PK, FK)**
- `id_item` **(PK, FK)**
- `orden_presentacion` — en qué lugar de la secuencia se mostró.
- `fecha_presentacion` — cuándo.

**Por qué entra ahora, sin esperar a que se diseñe la pantalla del
diagnóstico (pendiente A5):** el dato no lo pide una spec de Fase II, lo
exige **ADR-016**, que ya está decidido. Esa regla presenta ítems uno a
uno y decide si sigue o para según la certeza de lo que se va
respondiendo; sin registro de qué se presentó y en qué orden, esa
secuencia no se puede reconstruir y RI-11 queda sin poder verificarse.
Además, una Presentación **sin** Respuesta es la única forma de
representar "se le mostró y no respondió" — hoy indistinguible de "nunca
se le mostró", justo la distinción que el separador "Sin concluir" de
`14-spec-vista-interna-estudiantes.md` le promete al docente.

### Inscripción
**Fuente:** `08-spec-unirse-codigo.md`; modelo-conceptual.md ("Experiencia
— la cursan — Estudiantes — N, un grupo completo").

Entidad **asociativa**: resuelve la relación N a N entre Estudiante y
Experiencia — un estudiante se une a varias experiencias, una experiencia
agrupa a varios estudiantes. Conserva clave primaria propia (no
compuesta) para que Respuesta y Resultado puedan referenciarla sin
arrastrar una llave doble.
- `id_inscripcion` **(PK)**
- `id_estudiante` **(FK)**
- `id_experiencia` **(FK)**
- `fecha_union`

De aquí sale, por ejemplo, el contador "Estudiantes: N" de
`09-spec-vista-interna-marco.md`.

### Ítem (banco de diagnóstico)
**Fuente:** ADR-005 (se genera al crear la experiencia); ADR-006 (formato);
ADR-008 punto 1 (construcción de distractores plausibles — el atributo
`distractor` se retiró de aquí, ver ADR-020); ADR-014 (enunciado); ADR-015
(`excluido`); ADR-016 (banco de 12 por evidencia, regla adaptativa
mínimo 4/tope 6 — reemplaza la base de 6 de ADR-009).
- `id_item` **(PK)**
- `id_experiencia` **(FK)**
- `codigo_dba` **(FK)**
- `numero_evidencia` **(FK)** — las tres columnas juntas son **una sola**
  llave foránea compuesta hacia Experiencia_Evidencia (Quinta revisión):
  ya no son dos referencias separadas —una a Experiencia, otra a
  Evidencia— que hubiera que obligar a coincidir con una regla externa.
- `enunciado` — el texto de la pregunta (ADR-014)
- `formato` — `single_choice` por defecto, o `matching`/`ordering` según
  la evidencia (ADR-006)
- `origen` — `ia` o `editado_docente`. Distingue un ítem tal como lo
  generó la IA de uno que el docente ya intervino (ADR-015). Fase I §2
  eleva esa distinción a valor declarado del proyecto, y hasta ahora el
  modelo no la representaba (hallazgo H-5 del docente, aceptado en
  parte).
- `estado_revision` — si el docente ya revisó este ítem. El atributo
  entra porque ADR-005 exige la revisión previa a que un estudiante lo
  vea; su vocabulario exacto sigue sin decidirse (V-7).
- `excluido` — booleano, por defecto `falso` (ADR-015). Cuando es
  verdadero, el ítem no se muestra al estudiante durante el diagnóstico,
  aunque sigue existiendo en el banco — reversible, el docente puede
  reincluirlo en cualquier momento.

Un Ítem pertenece a exactamente 1 Experiencia y evalúa exactamente 1
Evidencia — el banco se genera por experiencia, no se comparte entre
experiencias distintas que usen el mismo DBA (ADR-005: "el diagnóstico de
**una experiencia** se genera una sola vez"). **Ya no hay dos caminos al
currículo**: desde la Quinta revisión, un Ítem cuelga de
Experiencia_Evidencia, que es a la vez el vínculo con la Experiencia y
con la Evidencia. Las reglas RI-1 y RI-2 de la versión anterior existían
solo para forzar que esos dos caminos coincidieran; al volverse
estructura, desaparecen.

**Pendiente, no inventado:** el atributo `estado_revision` ya existe
(arriba), pero su **vocabulario** exacto —qué valores admite, qué
significa cada uno— sigue sin definirse en ningún ADR (V-7). Se declara,
no se inventa.

### Opción
**Fuente:** ADR-014; `hipotesis_error` agregado por ADR-020 (2026-08-25).

El contenido de las alternativas de respuesta de un Ítem. Estructura
genérica pensada para cubrir los tres formatos cerrados de esta versión
(ADR-006), a costa de que algunos campos queden sin uso según el formato
— qué campo aplica en cada caso queda formalizado en RI-7, no solo
sugerido en prosa.
- `id_opcion` **(PK)**
- `id_item` **(FK)**
- `texto`
- `orden` — posición de presentación (`single_choice`) o posición en la
  secuencia correcta (`ordering`)
- `es_correcta` — marca la opción correcta en `single_choice`
- `grupo` — solo aplica a `matching`: columna izquierda o derecha; dos
  opciones de distinto grupo con el mismo `orden` forman la pareja
  correcta
- `hipotesis_error` — texto, nulo si la opción es correcta o si aún no
  se le asignó una (ADR-020). Cada opción incorrecta puede representar
  un error plausible distinto (ADR-002, ADR-006, principio del Force
  Concept Inventory y de Haladyna) — antes vivía, mal ubicado, como un
  único campo `distractor` en Ítem, incapaz de distinguir entre varias
  opciones incorrectas del mismo ítem. **Nunca se nombra ni se reporta**
  al docente o al estudiante en esta versión (restricción de ADR-008
  punto 1, sin cambios — solo cambió dónde vive el dato).

Pertenece a exactamente 1 Ítem. Se evaluó partir Opción en 3 subtipos
(uno por formato) para eliminar los campos condicionales — se descarta:
triplicaría la entidad a cambio de quitar 1-2 columnas sin uso por fila;
RI-7 ya resuelve la consistencia sin pagar ese costo.

### Respuesta
**Fuente:** ADR-008 punto 2 (certeza); ADR-016 (cantidad y regla
adaptativa — reemplaza a ADR-009 en ese punto); ADR-019 (`correcta` pasa
a derivado, se agrega Respuesta_Opción).

Entidad **asociativa**: resuelve, junto con su relación a Opción, qué
respondió un estudiante — no solo si acertó.
- `id_respuesta` **(PK)**
- `id_inscripcion` **(FK)** — junto con `id_item`, **una sola** llave
  foránea compuesta hacia Presentación (Quinta revisión): una Respuesta
  ya no cuelga por separado de Inscripción y de Ítem, cuelga del hecho
  de que ese ítem **se le mostró** a esa inscripción.
- `id_item` **(FK)** — ver arriba.
- `certeza` — CRI, escala 0-5
- `fecha_respuesta` — cuándo se envió. **Cierra V-1**, que la versión
  anterior trataba como comodidad de auditoría: no lo es. Sin marca de
  tiempo, la secuencia adaptativa de ADR-016 no se puede reconstruir, y
  RI-11 queda enunciada pero no verificable (hallazgo H-2 del docente,
  aceptado).
- `correcta` — booleano, **derivado y persistido** (ADR-021): su valor se
  calcula comparando las filas de Respuesta_Opción contra
  `es_correcta`/`orden`/`grupo` de las Opciones reales (ADR-019), pero se
  **guarda** en el momento de la respuesta, no se recalcula en cada
  lectura. "Derivado" significa que no lo captura el usuario, no que no se
  almacene. No necesita marca de tiempo propia — una Respuesta corresponde
  a un único evento; que esa marca no exista todavía es V-1, aparte.

Una Respuesta corresponde a exactamente 1 Presentación — y una
Presentación puede existir **sin** Respuesta: eso significa "se le mostró
y no respondió", un caso que la versión anterior del modelo no podía
representar (hallazgo H-3 del docente, aceptado). Cuántos Ítems responde
un estudiante por Evidencia lo fija el sistema con la regla adaptativa de
ADR-016 (mínimo 4, tope 6), no el docente.

### Respuesta_Opción
**Fuente:** ADR-019 (2026-08-25).

Entidad asociativa: materializa la relación N a M "selecciona" entre
Respuesta y Opción — registra qué Opción u Opciones eligió el estudiante,
no solo si el resultado final fue correcto. Sin esto, no hay forma de
saber qué emparejó (`matching`) o en qué orden puso las opciones
(`ordering`); para `single_choice`, se pierde cuál distractor específico
escogió.
- `id_respuesta` **(PK, FK)**
- `id_opcion` **(PK, FK)**
- `valor_dado` — entero, significado según el formato del Ítem (mismo
  criterio de "campo compartido, uso distinto por formato" ya aceptado en
  `Opción.orden`, ADR-014):
  - `single_choice`: sin uso — la existencia de la fila ya es la
    elección (una sola fila por Respuesta).
  - `ordering`: la posición que el estudiante le asignó a esa opción.
  - `matching`: un número de pareja asignado por el estudiante,
    compartido por las 2 opciones que emparejó entre sí.

Una Opción puede aparecer en muchas filas de Respuesta_Opción (distintos
estudiantes, distintas Respuestas); una Respuesta tiene una o varias
filas aquí, según el formato del Ítem que responde (RI-9).

### Resultado
**Fuente:** ADR-008 punto 4; PK compuesta verificada contra la propia
naturaleza de la entidad (Revisión 2026-08-25) — depende enteramente de
Inscripción y Evidencia, sin identidad propia.

Entidad **débil**, sin llave propia — depende de a quién y de qué
evidencia; participación total (obligatoria) en sus dos relaciones
identificadoras (*arroja*, con Inscripción; *mide*, con Evidencia). Como
Evidencia es a su vez débil, la clave de Resultado arrastra tres columnas.
- `id_inscripcion` **(PK, FK)**
- `codigo_dba` **(PK, FK)** — junto con `numero_evidencia`, ya no
  referencia a Evidencia directamente sino a **Experiencia_Evidencia**
  (Quinta revisión): un Resultado mide una evidencia *de esa
  experiencia*, no la evidencia del MEN en abstracto.
- `numero_evidencia` **(PK, FK)** — ver arriba. *(La experiencia
  concreta se deduce de `id_inscripcion`; que esa deducción se resuelva
  con una columna redundante o con una regla, lo decide el Modelo
  Relacional — es exactamente el tipo de detalle que le corresponde a
  él, no al MER.)*
- `estado` — muestra / no muestra / no concluyente. **Derivado y
  persistido** (ADR-021): se calcula a partir de las Respuestas de esa
  Inscripción a los Ítems de esa Evidencia, con la regla de certeza de
  ADR-008/ADR-016, y se guarda como fotografía del momento en que el
  diagnóstico concluyó para esa evidencia. Nunca una certeza, nunca un
  valor que se edite directamente.
- `fecha_calculo` — fecha/hora en que se calculó `estado` (ADR-021). No
  es opcional: una fotografía sin saber de cuándo es, no es auditable.
  Cierra V-4.

Un Resultado depende de 1 Inscripción y 1 Evidencia — es el resumen, por
estudiante inscrito y por evidencia, de lo que sus Respuestas a los ítems
de esa evidencia permiten concluir. Resultado alimenta a Reporte (ver
más abajo) — antes esa relación se afirmaba en texto sin dibujarse; ya
está en la tabla de relaciones.

### Reporte
**Fuente:** ADR-010; ADR-013/ADR-017/ADR-023 (categorías de brecha y su
umbral, revisados); ADR-018 revisado por **ADR-022** (estado agregado por
DBA: 4 estados con precedencia, no 3).

No es una entidad: no persiste, no tiene identificador propio, y no
cuenta entre las entidades del modelo — es un conjunto de vistas
calculadas **sobre Resultado**, por Experiencia:

- **Estado general** (ADR-018, revisado por ADR-022): por estudiante
  inscrito, un estado que agrega **todas** sus evidencias del DBA, en uno
  de **cuatro**, evaluados con precedencia — **no muestra** (al menos una
  evidencia concluida lo indica, sin esperar al resto), **muestra**
  (todas concluyeron y todas muestran), **no concluyente** (todas
  concluyeron y alguna quedó ambigua), **sin concluir** (le falta
  terminar alguna). Se cuenta cuántos estudiantes caen en cada uno.
- **Estado por evidencia** (ADR-010 punto 1): para cada evidencia del
  DBA, cuenta de estudiantes en esos mismos cuatro estados, más una
  categoría de brecha calculada por umbral fijo (ADR-013 + ADR-017,
  3 categorías: **Datos insuficientes**, **Brecha aparente**, **Sin
  brecha aparente** — ya no 4; se fusionaron "Brecha extendida" y
  "Brecha aislada"; ADR-023 amplió qué cuenta hacia el umbral de "Datos
  insuficientes"), nunca texto generado por IA.

*(Corrección 2026-08-26: esta sección quedó sin actualizar en la Cuarta
revisión —que solo tocó V-3—, y seguía diciendo "tres estados" y usando
los nombres "Resultados generales/por evidencia", renombrados a "Estado
general/por evidencia" en `13-spec-modal-reporte.md`.)*
- **Vista de estudiantes (aula):** listado por Inscripción, con el estado
  de cada Evidencia — historial, no agregado (ADR-010 punto 4). Todavía
  sin construir en Fase II (Tab Estudiantes es lo próximo pendiente ahí).
  Necesita V-3 para distinguir "no respondió" de "respondió y no
  concluyente".

---

## Relaciones y cardinalidades

| Entidad A | Relación | Entidad B | Cardinalidad | Participación A / B | Fuente |
|---|---|---|---|---|---|
| Docente | crea | Experiencia | 1 a N | (0,N) / (1,1) | glosario "Experiencia" |
| Experiencia | se ancla a | DBA | N a 1 | (1,1) / (0,N) | modelo-conceptual.md |
| DBA | comprende | Evidencia | 1 a N, identificadora | (1,N) / (1,1) | modelo-conceptual.md (rango no confiable, QA-013) |
| Estudiante | realiza | Inscripción | 1 a N | (0,N) / (1,1) | estructural (modelo-conceptual.md: "Experiencia — la cursan — Estudiantes") |
| Inscripción | pertenece a | Experiencia | N a 1 | (1,1) / (0,N) | modelo-conceptual.md |
| Evidencia | se dictamina | Evidencia_Dictamen | 1 a 1, identificadora | (0,1) / (1,1) | H-6 — Quinta revisión |
| Experiencia | incluye | Experiencia_Evidencia | 1 a N | (1,N) / (1,1) | H-4 — Quinta revisión. Mínimo 1: una experiencia sin ninguna evidencia incluida no diagnostica nada, y ADR-005 genera el banco en el mismo acto de creación. |
| Evidencia | sobre | Experiencia_Evidencia | 1 a N | (0,N) / (1,1) | H-4 — Quinta revisión |
| Experiencia_Evidencia | genera | Ítem | 1 a N | (0,N) / (1,1) | ADR-005 — **reemplaza** a "Experiencia genera Ítem" e "Ítem evalúa Evidencia" (Quinta revisión): un solo camino al currículo |
| Ítem | ofrece | Opción | 1 a N | (2,N) / (1,1) | ADR-014 |
| Inscripción | atiende | Presentación | 1 a N, identificadora | (0,N) / (1,1) | H-2 — Quinta revisión |
| Ítem | se presenta | Presentación | 1 a N, identificadora | (0,N) / (1,1) | H-2 — Quinta revisión |
| Presentación | registra | Respuesta | 1 a 0..1 | (0,1) / (1,1) | H-3 — Quinta revisión. Máximo 1 y mínimo 0: una presentación sin respuesta significa "se le mostró y no respondió". **Reemplaza** a "Ítem recibe Respuesta" y "Respuesta proviene de Inscripción". |
| Respuesta | selecciona | Opción | N a M, asociativa | (1,N) / (0,M) | ADR-019 (vía Respuesta_Opción) |
| Inscripción | arroja | Resultado | 1 a N, identificadora | (0,N) / (1,1) | ADR-008 |
| Resultado | mide | Experiencia_Evidencia | N a 1, identificadora | (1,1) / (0,N) | ADR-008 + H-4 — Quinta revisión: mide la evidencia *de esa experiencia*, no la del MEN en abstracto |
| Resultado | se agrega en | Reporte | N a 1, derivada | — / — | ADR-010, ADR-018 — **agregada en esta revisión**: antes el texto decía "Reporte es una vista calculada sobre Resultado" pero la única relación dibujada era con Experiencia; la dependencia real con Resultado nunca quedó representada. |
| Reporte | resume | Experiencia | 1 a 1, derivada | — / — | modelo-conceptual.md, ADR-010, ADR-018 |

La columna de participación indica (mínimo, máximo) de cada lado — un
mínimo de 1 es participación total. Decide `NULL`/`NOT NULL` en cada
llave foránea del Modelo Relacional.

---

## Restricciones de integridad

Reglas que el diagrama no puede expresar por sí solo y que el Modelo
Relacional va a tener que hacer cumplir — sin ellas, la estructura admite
datos que el mecanismo real no admite. Verificadas contra fuente propia,
no adoptadas solo por aparecer en la comparación con el compañero
(Segunda revisión — 2026-08-25).

*(Quinta revisión — 2026-09-08: eran once, siguen siendo once, pero no
son las mismas. **RI-1 y RI-2 desaparecen**: existían solo para forzar
que los dos caminos de un Ítem/Resultado al currículo coincidieran, y con
Experiencia_Evidencia de por medio eso pasó a ser estructura. **RI-5
también**: la unicidad del par (Inscripción, Ítem) ahora la garantiza la
identificación débil de Presentación. Entran tres nuevas.)*

1. **RI-1** — El par (Estudiante, Experiencia) es único en Inscripción.
   Fuente: `08-spec-unirse-codigo.md` §7 — "sea la primera vez que se une
   o ya estuviera unido, el resultado es el mismo". *(era RI-3)*
2. **RI-2** — El par (Inscripción, Evidencia) es único en Resultado. Lo
   garantiza la identificación débil, no una regla aparte. *(era RI-4)*
3. **RI-3** — `Docente.correo` y `Estudiante.correo` son únicos.
   `Experiencia.codigo_invitacion` es único, de 6 caracteres
   alfanuméricos, sin `0`/`O`/`1`/`I`/`L` (`08-spec-unirse-codigo.md`
   §2.3). *(era RI-6)*
4. **RI-4** — Dominio de Opción según `Item.formato` (ADR-006, ADR-014):
   en `single_choice`, exactamente una opción con `es_correcta` y
   `grupo` sin uso; en `matching`, `grupo` obligatorio y la pareja
   correcta son dos opciones de distinto grupo con el mismo `orden`,
   `es_correcta` sin uso; en `ordering`, `orden` es la posición correcta
   y `es_correcta`/`grupo` quedan sin uso. **Con mínimos por formato**
   (hallazgo H-9 del docente, aceptado): 2 opciones en `single_choice` y
   en `ordering`; **4 en `matching`**, con al menos 2 por grupo — la
   participación (2,N) de la versión anterior alcanzaba para
   `single_choice` pero no para `matching`, donde la pareja correcta son
   dos opciones de distinto grupo. *(era RI-7 + H-9)*
5. **RI-5** — `incluida` en Experiencia_Evidencia solo puede ser
   verdadero si el dictamen correspondiente tiene `aplica_formato_cerrado`
   verdadero; y solo una evidencia incluida genera Ítems. *(era RI-8,
   reformulada por H-4 y H-6)*
6. **RI-6** — Toda Respuesta selecciona al menos una Opción, y solo
   Opciones del Ítem de su Presentación. En `single_choice`, exactamente
   una. Una Presentación **sin** Respuesta es válida y significa "se le
   mostró y no respondió". *(era RI-9, ampliada por H-3)*
7. **RI-7** — Una Experiencia en Borrador no admite Inscripción: el
   estudiante solo entra si está Publicada (`08-spec-unirse-codigo.md`
   §2.4). *(era RI-10)*
8. **RI-8 — nueva.** `orden_presentacion` es único dentro de una
   Inscripción para una misma evidencia. Sin unicidad no hay orden, y el
   orden es justamente el dato que hacía falta (H-2).
9. **RI-9 — nueva.** Las Presentaciones de una Inscripción para una misma
   evidencia no pueden exceder el tope de **6** ítems (ADR-016), ni el
   número de ítems no excluidos que el banco tenga para esa evidencia.
10. **RI-10 — nueva. Cierra V-2.** Ítem y Opción no pueden editarse una
    vez que existe una Presentación de ese Ítem. Antes esto era un vacío
    declarado y no expresable; ahora sí lo es, porque existe el hecho
    "este ítem ya se le mostró a alguien". *(Se evaluó la alternativa
    propuesta por el otro grupo —versionar el contenido con un atributo
    `version`— y se descartó para esta versión: obligaría a que cada
    Respuesta apunte a una versión específica del ítem y no al ítem,
    costando estructura en tres entidades, para resolver un caso —el
    docente quiere corregir un ítem a mitad de curso— que todavía no se
    ha establecido como real. Queda declarado como diferido, no
    descartado, en la lista de vacíos.)*
11. **RI-11** — `Respuesta.correcta` y `Resultado.estado` son derivados
    y **se persisten** (ADR-021): su valor almacenado debe coincidir con
    el recálculo. **A diferencia de la versión anterior, ese recálculo
    ahora sí es posible**: con Presentación existiendo, la secuencia
    adaptativa de ADR-016 se puede reconstruir. Lo único que sigue
    impidiendo verificarla del todo es que la regla de parada exacta no
    está definida (V-5).
    *(Corrección 2026-09-19: esta regla listaba también
    `Inscripcion.estado_avance`, atributo que **no existe** —ni en la
    entidad Inscripción, ni en `diagrama/datos_mer.py`— y que además
    **no debe existir**: V-3 se resolvió por ADR-022 derivando el estado
    de avance de la ausencia de fila en Resultado, «sin columna ni tabla
    nueva». Era un residuo de un borrador previo a esa decisión, y
    constituía exactamente el tipo de contradicción interna que la
    revisión docente señaló en otros puntos. Se retira.)*

---

## Explícitamente fuera de este modelo, y por qué

- **Unidad, Práctica, Verificación** — diferidas (ADR-007), no se
  construyen todavía.
- **Hipótesis de error como dato reportado** — existe internamente en
  Opción (`hipotesis_error`, ADR-020), pero no se expone como "tipo de
  error" a docente ni estudiante (ADR-008).
- **Bloom como campo activo** — se adoptó (ADR-003) pero quedó sin función
  en el mecanismo real (ADR-008); incluirlo sería inventar un uso que no
  existe.
- **Perfil de aprendizaje, mediaciones pedagógicas, acudientes,
  instituciones, Curso** — todo esto pertenece al sistema anterior, ya
  descartado explícitamente (ver `U1-01_Informe_Validacion_Diseno_Tecnico`).
- **Configuración de umbrales del Reporte** — no existe, quedan fijos por
  sistema (ADR-013, ADR-017).
- **Autenticación, registro y gestión de cuenta** — el modelo parte de
  una sesión ya establecida; Docente y Estudiante son entidades raíz
  (nada dentro de este alcance las crea). Ninguna pantalla de acceso
  existe todavía en Fase II y la forma de la credencial no está
  decidida (V-8).
- **Ponderación de evidencias por importancia/dificultad** en el
  veredicto de "Resultados generales" — considerada y rechazada para
  esta versión (ADR-018, consecuencia reconocida): el sistema no tiene
  datos para decidir qué evidencia pesa más; las 3 evidencias entran con
  peso igual.

## Vacíos detectados, no resueltos por cuenta propia

Mismo criterio que ya usó ADR-014 con el contenido del Ítem: lo
siguiente hace falta, pero no sale de ningún ADR, glosario ni spec ya
escrita — queda declarado, no inventado (Segunda revisión — 2026-08-25).

1. **V-1 — Marca temporal de Respuesta. RESUELTO** en la Quinta revisión
   (2026-09-08): entra como `fecha_respuesta`. La versión anterior lo
   trataba como una comodidad de auditoría — el hallazgo H-2 del docente
   mostró que no lo es: sin marca de tiempo, la secuencia adaptativa de
   ADR-016 no se reconstruye y RI-11 no se puede verificar.
2. **V-2 — Inmutabilidad de Ítem y Opción tras la primera Respuesta.
   RESUELTO** en la Quinta revisión: pasa a ser la restricción **RI-10**,
   expresable ahora que existe Presentación.
3. **V-3 — Estado de avance de la Inscripción. RESUELTO** por ADR-022
   (2026-08-26): se agrega un 4.º estado a nivel de DBA, "sin
   concluir", derivado de la simple ausencia de fila en `Resultado`
   para alguna evidencia — sin columna ni tabla nueva.
4. **V-4 — Marca de cálculo de Resultado. RESUELTO** por ADR-021
   (2026-08-26): `fecha_calculo` ya está incorporado como atributo de
   Resultado.
5. **V-5 — Regla de parada del diagnóstico. NUEVO** (Quinta revisión,
   hallazgo H-7 del docente, aceptado en su fondo). ADR-016 define la
   regla de forma cualitativa —mínimo 4, se detiene con mayoría de
   señales fuertes, tope 6— pero **qué combinación exacta de `correcta`
   × `certeza` cuenta como "señal fuerte"** no está definida en ningún
   documento. Es la función que convierte Respuestas en
   `Resultado.estado`, es decir, lo que le da sentido a la entidad
   Resultado. Sin ella, `Resultado.estado` no es computable y RI-11 no es
   verificable. Es previa a cualquier implementación.
6. **V-6 — Dictamen de formato cerrado, pendiente de censo. NUEVO**
   (Quinta revisión). La entidad Evidencia_Dictamen existe, pero sus
   valores dependen de QA-014, que no ha corrido. Hasta entonces RI-5 no
   se puede evaluar contra datos reales.
7. **V-7 — Vocabulario de `estado_revision`.** El atributo entra en esta
   revisión porque ADR-005 lo exige; su dominio exacto sigue sin
   decidirse.
8. **V-8 — Autenticación y credencial. PARCIALMENTE RESUELTO** fuera de
   este documento: `ADR-025` y las Ventanas 014-017 de Fase II ya
   definieron el flujo (correo+contraseña y login social, verificación,
   perfil, rol). Falta llevar esa decisión al modelo de datos — hoy
   ninguna entidad guarda credencial.
9. **V-9 — Versionado de contenido del Ítem. DIFERIDO, no descartado**
   (Quinta revisión). Propuesto por el otro grupo de la asignatura
   (informe del 2026-09-07) como alternativa a RI-10: en vez de prohibir
   editar, versionar. Es más flexible —el docente podría corregir un
   ítem sin romper el historial— y más costoso: cada Respuesta tendría
   que apuntar a una versión, no al ítem. Se difiere porque el caso de
   uso que resolvería no se ha establecido como real en esta versión.

**Ya resueltos en este documento, no siguen abiertos:** el formato exacto
de `codigo_dba` y la forma de `numero_evidencia` (verificados contra
`curriculo_men_normalizado.json`, ver Entidades DBA/Evidencia).

---

## Decisiones tomadas durante la construcción de este modelo

1. Docente y Estudiante son entidades separadas, no una sola tabla con
   rol — confirmado en esta sesión.
2. Los umbrales del Reporte los fija el sistema, no el docente, en esta
   versión — ADR-013, agregado a `decisiones.md`.
3. El contenido propio del Ítem (enunciado y opciones) no estaba
   definido en ningún documento previo — se detectó como vacío real al
   construir este modelo y se resolvió con una entidad Opción genérica —
   ADR-014, agregado a `decisiones.md`.

## Revisión — 2026-08-25

Motivada por dos cosas a la vez: (1) Fase II avanzó (Materiales, banco de
ítems, Reporte) y generó 4 ADR nuevos (015-018) que nunca se habían
incorporado aquí, y (2) una auditoría cruzada del modelo entidad-relación
de un compañero de curso, hecha con el mismo nivel de rigor que el resto
de este proyecto — verificando cada posible hallazgo contra fuente propia
antes de aceptarlo, no copiando por comparación. Cambios:

1. **`Ítem.excluido`** agregado (ADR-015).
2. **Banco de 12, regla adaptativa mínimo 4/tope 6** — todas las citas a
   la base de 6 ítems de ADR-009 se actualizaron a ADR-016, que la
   reemplaza en ese punto.
3. **`DBA` y `Evidencia` no tenían llave primaria** — vacío real desde la
   versión original, sin detectar hasta ahora. Se agregó `codigo_dba`
   (PK de DBA, verificado contra el campo `id` real de
   `curriculo_men_normalizado.json`) y la PK compuesta de Evidencia
   `(codigo_dba, numero_evidencia)`, verificada contra cómo el dato real
   ya guarda las evidencias (lista ordenada dentro de cada DBA, sin id
   propio) — Evidencia se documenta ahora explícitamente como entidad
   débil.
4. **`Resultado` tampoco tenía llave primaria** — mismo tipo de vacío;
   se agregó su PK compuesta `(id_inscripcion, codigo_dba,
   numero_evidencia)`, entidad débil.
5. **`Evidencia.aplica_formato_cerrado`** agregado — verificado 3 veces:
   ADR-006/QA-014, modelo-conceptual.md, y la UI real de
   `06-spec-crear-experiencia-paso2.md` (sección 2.4), que ya distingue
   evidencias que no aplican a formato cerrado con tachado y texto
   informativo. El campo existía de hecho en el diseño, sin existir en
   el modelo de datos.
6. **`Respuesta_Opción`** (entidad nueva, ADR-019): sin esto no había
   forma de registrar qué emparejó o en qué orden puso las opciones un
   estudiante (`matching`/`ordering`), ni cuál distractor específico
   eligió en `single_choice` — vacío real, verificado contra la propia
   estructura de Opción (ADR-014), independiente de la comparación con
   el compañero. `Respuesta.correcta` pasa a ser un valor derivado.
7. **`hipotesis_error` se movió de Ítem a Opción** (ADR-020): ADR-008
   (2026-08-07) asumía un distractor por ítem; ADR-014 (2026-08-19, 12
   días después) introdujo Opción precisamente porque un ítem tiene
   varias opciones incorrectas — nunca se reconciliaron. El campo
   `distractor` de Ítem se retiró; cada Opción incorrecta ahora puede
   llevar su propia hipótesis de error. La restricción de no reportarlo
   a docente/estudiante sigue vigente sin cambios.
8. **Reporte** se actualizó de 2 a 3 vistas descritas (se agregó
   "Resultados generales", ADR-018) y de 4 a 3 categorías de brecha
   (ADR-017).

**Verificado y descartado en esta pasada, no aceptado sin más:** el
compañero también marca `correo` de Docente/Estudiante como valor único
— no se incorporó todavía porque no se había sometido al mismo nivel de
verificación contra fuente propia que el resto de estos cambios. Se
resolvió en la segunda revisión, más abajo.

## Segunda revisión — 2026-08-25

Alejandro compartió una versión más completa del modelo del compañero
(formato caja-tabla, con FK visibles, restricciones de integridad y
vacíos declarados aparte) — con fecha interna 2026-08-19/20, es decir,
anterior a que ADR-019/020 se formalizaran aquí. Llega, por su cuenta, a
casi las mismas correcciones que la revisión anterior de este documento
— confirma el camino tomado, no lo reemplaza. Se verificó cada hallazgo
adicional contra fuente propia antes de aceptarlo:

1. **`correo` y `codigo_invitacion` marcados `(U)`** — ahora sí
   incorporado: segunda fuente independiente, más el hecho de que
   `codigo_invitacion` **tiene** que ser único para que
   `08-spec-unirse-codigo.md` funcione (un código debe resolver a
   exactamente una Experiencia).
2. **Convención de nombres `id_entidad`** en vez de `id` — adoptada
   porque el formato caja-tabla que se usará para el diagrama muestra
   las FK dentro de cada caja; con eso, columnas `id` repetidas serían
   ilegibles.
3. **Relación `Resultado — se agrega en — Reporte` agregada** a la
   tabla — vacío real: el texto de Reporte siempre dijo "vista calculada
   sobre Resultado", pero la tabla de relaciones nunca dibujó esa
   relación, solo la de Reporte con Experiencia.
4. **11 restricciones de integridad (RI-1 a RI-11)** agregadas — reglas
   de negocio que el diagrama por sí solo no puede expresar (ej. que la
   Evidencia de un Ítem coincida con el DBA de su Experiencia). Cada una
   se verificó contra ADR o spec real antes de aceptarse; RI-5 se marca
   explícitamente como supuesto razonable, no como algo que un ADR
   afirme.
5. **4 vacíos nuevos declarados (V-1 a V-4)** — fecha de Respuesta,
   inmutabilidad de Ítem/Opción tras la primera respuesta, estado de
   avance de la Inscripción, marca de cálculo de Resultado. Ninguno se
   resuelve por cuenta propia, mismo criterio que el resto del
   documento.
6. **Columna de participación (mín, máx)** agregada a la tabla de
   relaciones — decide `NULL`/`NOT NULL` en el Modelo Relacional.

**No incorporado, evaluado y descartado:** una futura entidad `Cuenta`
(1:1 con Docente y con Estudiante) para cuando se modele autenticación —
idea razonable del compañero para V-8, pero modelarla ahora sería
inventar estructura sin ADR ni spec de auth que la respalde. Queda como
dirección a considerar cuando exista esa decisión, no como parte de este
modelo.

## Tercera revisión — 2026-08-26

Motivada por la construcción del Modelo Relacional
(`04-modelo-relacional.md`): al bajar este modelo a tablas apareció una
contradicción que no era visible en el nivel entidad-relación. Un
borrador del MR resolvió V-4 por su cuenta —recomendando **no**
persistir los valores derivados— y eso rompía a `Resultado`: `estado` es
su único atributo no-clave, así que no persistirlo no lo convertía en
"tabla con columna calculada", lo convertía en vista, contradiciendo que
este documento lo declara **entidad débil** y reserva "vista derivada"
para Reporte. Se formalizó la decisión correcta como ADR-021 y de ahí
bajan estos cambios:

1. **`Resultado.estado` y `Respuesta.correcta` pasan a "derivado **y
   persistido**"** — se aclara, además, que "derivado" siempre significó
   "no lo captura el usuario", no "no se almacena"; la ambigüedad de ese
   término fue lo que permitió el error.
2. **`Resultado.fecha_calculo`** agregado — consecuencia obligatoria de
   persistir una fotografía, no un campo de conveniencia.
3. **V-4 queda RESUELTO**, con su rastro anotado en vez de borrado.
4. **RI-11 cambia de naturaleza** — deja de poder cumplirse sola y pasa
   a ser una obligación activa de escritura, con V-2 como su amenaza
   real.

**Lección de proceso, anotada a propósito:** este hallazgo no salió de
releer el MER —que se había dado por cerrado dos veces— sino de
**derivarlo a otro formato**. Bajar un modelo a un nivel más concreto
(entidades → tablas) obliga a responder preguntas que el nivel anterior
podía dejar ambiguas, y ahí es donde la ambigüedad se vuelve visible.
Es el mismo efecto que tuvo comparar contra el modelo de un compañero en
la Segunda revisión: lo que encuentra errores no es leer con más
cuidado, es **someter el documento a una prueba externa a él mismo**.

## Cuarta revisión — 2026-08-26

Motivada por Tab Estudiantes (Vista Interna, ADR-010 punto 4): al
evaluar agrupar el listado de estudiantes por su veredicto de DBA
(ADR-018), Alejandro objetó el caso de un estudiante a mitad de camino
— rastrearlo hasta el final mostró que ADR-018 nunca definió qué pasa
mientras un estudiante no ha concluido todas las evidencias, que es el
estado normal, no la excepción. Se formalizó ADR-022: 4 estados con
precedencia (No muestra tiene prioridad; luego Muestra/No concluyente,
solo si todo concluyó; si no, Sin concluir). V-3 queda resuelto —
consecuencia anotada arriba, en su propio punto.

**Nota de proceso:** este hallazgo no salió de comparar contra nada
externo ni de releer — salió de que Alejandro cuestionó un caso límite
antes de aceptar un diseño ("¿de verdad todos quedarían igual al
iniciar?"), y seguir esa pregunta hasta el final destapó que el vacío
era más amplio de lo que parecía. Mismo principio que ya se había
anotado antes (someter el documento a algo externo a sí mismo) — acá lo
externo fue la pregunta, no un documento.

---

## Quinta revisión — 2026-09-08

**Motivo: dos revisiones externas, no una.** El 1 de septiembre el
docente Ali entregó una crítica del MER con 12 hallazgos y una propuesta
de modelo corregido (`revision-docente/revision-docente-2026-09-01.html`).
El 7 de septiembre, otro grupo de la asignatura —clase del docente
Alexander— entregó un informe de observaciones sobre ese mismo material
(`revision-otro-grupo/`). Esta revisión incorpora lo que sobrevivió al
triaje de ambas.

### Qué se aceptó de la revisión del docente (2026-09-01)

Del triaje del 2026-09-04 (`05-triaje-revision-docente.md`), Grupos A y B:

| Hallazgo | Qué entra |
|---|---|
| **H-2 / H-3** | Entidad **Presentación**, `Respuesta.fecha_respuesta`, y Respuesta colgando de Presentación. Cierra V-1 y permite representar "se le mostró y no respondió". |
| **H-4** | Entidad **Experiencia_Evidencia**. Elimina RI-1 y RI-2 al volverlas estructura. |
| **H-5** (en parte) | `Item.origen` y `Item.estado_revision`. **No** se adopta su regla de publicación asociada — contradice lo ya decidido en `12-spec-modal-banco-items.md` (revisar el banco no es prerrequisito para publicar). |
| **H-6** | Entidad **Evidencia_Dictamen**; `aplica_formato_cerrado` sale de Evidencia. |
| **H-7** | Se declara **V-5**, la regla de parada exacta, que el modelo anterior daba por resuelta. |
| **H-9** | Mínimos de Opción por formato, dentro de RI-4. |

**Lo que no se adoptó, y por qué:** **H-1** cae casi entero — pedía
guardar orden de evaluación, cantidad de ítems y tope por evidencia, y
de esos tres, dos dejaron de existir (ADR-016 le quitó al docente
decidir cuántos ítems; ADR-024 eliminó el orden de evaluación). Lo único
que quedaba de H-1 era, en realidad, H-4. **H-10** (tres versiones del
MER conviviendo) es un problema de repositorio, no de modelo; se atiende
aparte.

### Qué se aceptó del informe del otro grupo (2026-09-07)

Poco, y por una razón concreta: **ese informe no revisa este modelo.**
Reconstruyeron el MER desde una imagen (`mer-v3-adaptivelearn.png`) y
llenaron los huecos con supuestos genéricos de plataforma educativa. Su
modelo **no tiene entidad Docente**, no tiene `certeza` (el CRI de
ADR-008, base de toda la regla adaptativa de ADR-016), revive
`nivel_bloom` —retirado por QA-015—, y le pone a Resultado un
`puntaje_obtenido DECIMAL(5,2)`, que contradice de frente el núcleo
epistémico del proyecto: el glosario dice tres veces que el resultado es
"muestra, no muestra, o no concluyente; **nunca una certeza**". Su
RESULTADO es además 1:1 con RESPUESTA — misma palabra, concepto
distinto del nuestro, que agrega 4-6 respuestas por evidencia.

De sus tres recomendaciones:
- **Versionado de contenido** — la única valiosa. Apunta a un hueco real
  (nuestro V-2). Se resolvió por la vía del docente (RI-10, prohibir
  editar) y el versionado queda declarado como **V-9**, diferido con su
  razón escrita.
- **Llave subrogada para Evidencia** — observación correcta (la llave
  compuesta sí se propaga), pero se declina: Evidencia es dato del MEN y
  su identidad *es* ese par; no inventamos identificadores para datos que
  no son nuestros. La propuesta del propio docente también mantuvo la
  compuesta.
- **Índices de rendimiento** — correcto pero prematuro: aplican a
  Presentación, que hasta esta revisión no existía, y el Modelo
  Relacional ya tiene su propia sección de índices.

### Notación

**H-8 queda cerrado: Chen.** El docente Ali acepta ambas notaciones; el
docente Alexander no acepta caja-tabla. Chen satisface a los dos, y es
además la notación correcta para este artefacto — con las llaves
foráneas dentro de las cajas, como señalaba el propio H-8, "el MER ya es
casi el MR" y el entregable siguiente queda reducido a tipos y tamaños.

### Conteo

De 11 entidades a **14** (entran Experiencia_Evidencia, Evidencia_Dictamen
y Presentación; Reporte sigue sin contar, es vista derivada). De 13
relaciones a **16** entre entidades reales, más las 2 derivadas hacia
Reporte, que no cuentan. Once restricciones de
integridad, pero no las mismas: tres se fueron por volverse estructura y
entraron tres nuevas.
