# Pendientes — AdaptiveLearn

> Backlog vivo. Distinto de `preguntas-abiertas.md` (preguntas de diseño
> sin resolver) y de `decisiones.md` (lo ya decidido): esto es **trabajo
> por hacer**, con su estado real y qué lo bloquea.
>
> Última actualización: 2026-10-26.

**Checklist fijo, desde ADR-024 (2026-08-29):** cada vez que se cierre
una ADR nueva que le otorgue o le retire una capacidad al docente o al
estudiante, correr un barrido sobre **todas** las ADR existentes (no
solo la nueva) buscando frases "el docente/estudiante decide/controla/
elige/reordena/ajusta/edita" y verificar que cada una tenga una
interfaz real en Fase II — no solo revisar que la ADR nueva en sí sea
coherente. Nace de encontrar que ADR-005 llevaba semanas otorgando una
capacidad (reordenar evidencias) sin ninguna pantalla que la
respaldara, sin que ninguna de las 4 auditorías previas lo detectara —
ninguna de ellas comprobaba esto. Alejandro además va a revisar
manualmente `diseño/` y Fase I completos en busca de este mismo patrón,
al terminar Fase II, no antes.

---

## A. Fase II (Diseño Multimedial) — en curso

### A1. Tab Estudiantes — ESPECIFICADO COMPLETO (`14-spec-vista-interna-estudiantes.md`)

Vista Interna, 3.ª pestaña. `ADR-010` punto 4 define su mecanismo
("vista de estudiantes/aula: listado del grupo con detalle por
estudiante, historial, no agregado"). Estados 1, 2 y 3 especificados,
tokens verificado limpio, consistencia y cadena íntegras.

**Ya especificado (Estados 1 y 2, actualizado 2026-08-29):**
- Subtítulo de sección: "El grupo inscrito en esta experiencia,
  estudiante por estudiante." — centrado (ver corrección de alineación
  abajo).
- Fila de acciones: **no se renderiza en absoluto** mientras `estado =
  Borrador` (no un botón Disabled — se retira la fila completa, no
  tiene ninguna función real en ese estado). Aparece recién al publicar
  — buscador + botón "Código de invitación". El código se **genera** al
  crear la experiencia (`codigo_invitacion` es NOT NULL en el MR, no
  puede quedar en null hasta publicar), pero solo se **muestra** al
  docente tras publicar — decisión explícita, ver 2.2 del spec.
- Botón "Código de invitación" **abre un modal** (no swap de texto en
  el botón — el docente lo dicta a 30 estudiantes, necesita el código
  sostenido en pantalla).
- "Publicar experiencia" **no** es footer fijo — es un botón centrado
  dentro del Estado 1 (Borrador), con ícono + título + descripción
  arriba (estructura de 4 elementos, gaps `8/4/24px` razonados), más su
  propio modal de confirmación — **ya especificado**, ver A3.
- Estado 1 (Borrador): ícono `Users` `32×32px` `#111111`/`2.5px` +
  título+descripción (Subencabezado del paso) + botón, todo centrado
  vertical y horizontalmente en el panel (sin fila de acciones).
- Estado 2 (Publicada, 0 estudiantes unidos): misma estructura de
  ícono+título+descripción, sin botón — ícono en `#888888`/`1.5px`
  (más suave, sin urgencia, coincide con el único patrón de ese color
  en todo el proyecto).
- **Corrección de alineación (2026-08-29, retroactiva):** encabezados
  de modal y de Vista Interna unificados a título centrado con
  íconos/cajas invisibles en las esquinas (antes mezclado: unos a la
  izquierda, uno centrado). Afectó también la fila de metadata y el nav
  de tabs (ahora centrados como bloque vía `Alignment Center` del Panel
  de contenido) y el subtítulo de sección de las 3 pestañas (vuelve a
  centrado — revierte una decisión de alineación izquierda tomada antes
  de unificar el criterio). Tocó 7 archivos: `05`, `09`, `10`, `11`,
  `12`, `13`, `14`. Verificado: tokens 14/14, consistencia 0 a revisar,
  cadena íntegra.

**Estado 3 (Publicada, con estudiantes) — ESPECIFICADO 2026-08-29:**
- Lista agrupada por estado del veredicto (`ADR-022`), no alfabético
  — responde "¿quién necesita atención?", mismo criterio consolidado
  en la Filosofía de separadores (`03-tokens-diseno.md`). Orden
  confirmado: No muestra → No concluyente → Sin concluir → Muestra.
  Grupos vacíos se omiten. Alfabético dentro de cada grupo.
- Separador de estado — mismo componente que "Separador de brecha" de
  Reporte, nombre + explicación de una línea, color en el texto.
- Card de estudiante: Avatar `32×32px` con ícono por defecto (silueta
  de persona, para avatar no elegido — es opcional) + Nombre (Bold,
  mismo criterio que el Título de la Row Card del Dashboard) — 2 capas,
  expandible. *(Corrección 2026-08-29: era `44×44px` + Nombre+Email en
  vertical — se retiró el correo y se bajó el avatar a `32px`, ninguna
  otra card del proyecto apila elementos en vertical en su fila
  colapsada.)*
- Expandida: InfoBlock "Evidencias" en **lista** (no barra — con 1-2
  evidencias por DBA, una barra de distribución no dice nada útil),
  nombre de evidencia + resultado individual en singular y con color.
  Botón "Ver historial completo" → abre A4 (diferido).
- Decisión revertida en el camino: las cards **sí expanden en línea**
  (la nota anterior de "sin expandir, trabajo que se descarta" ya no
  aplica — se verificó que expandir e historial no son redundantes,
  responden preguntas distintas: "por qué" vs. "qué pasó exactamente").
- Enunciado de evidencia **completo, sin truncar**, dentro de la card
  expandida (distinto del resto del proyecto — ver spec, 2.3).
- **Crítica UI/UX honesta tras especificar** (2026-08-29) encontró 3
  cosas reales: (1) contraste WCAG de `#888888` a `13px` Bold, ver
  **V-10**; (2) orden de evidencias — se citó ADR-005 como si el
  docente pudiera reordenar, Alejandro corrigió: nunca existió esa
  interfaz. Se escribió **ADR-024** (revisa ADR-005 punto 2 únicamente)
  y de paso se encontró **V-9** (columna MR huérfana); (3) enunciados
  truncados y apilados podían volverse indistinguibles — resuelto,
  ahora van completos.

### A2. Modal "Código de invitación" — ESPECIFICADO
`16-spec-modal-codigo-invitacion.md` (Ventana 013), 2026-08-29. **QR:
resuelto — diferido explícitamente a otra versión** (confirmado por
Alejandro, ya no queda abierto). Reutiliza el marco chico y la fila de
6 cajas de `08-spec-unirse-codigo.md` en modo solo lectura (sin Foco ni
Error — es una etiqueta, no un formulario), con botón "Copiar código" +
retroalimentación de texto ("¡Código copiado!" por 2s, descripción
recortada a una línea). El modal no se cierra al copiar — el docente
puede necesitar el código sostenido en pantalla. Tokens verificado,
limpio.

### A3. Modal "Publicar experiencia" (confirmación) — ESPECIFICADO
`15-spec-modal-confirmar-publicar.md` (Ventana 012), 2026-08-29. Card
informativa con 3 preguntas propias (no el genérico Qué es/Para qué
sirve/Cómo funciona): "¿Qué cambia?", "¿Se puede deshacer?", "¿Qué
debo revisar antes?" — la 2.ª existe porque no hay mecanismo de
"despublicar" documentado en ningún lado del proyecto; la 3.ª es un
recordatorio sobre el banco de ítems, no una garantía técnica (depende
de V-2, sin resolver). Ancho `912px`, mismo marco que los modales
grandes, construido con el encabezado centrado desde el principio.
Tokens verificado, limpio.

### A4. Modal de historial del estudiante — ESPECIFICADO 2026-10-21

`27-spec-modal-historial-estudiante.md` (Ventana 027). Idea de
Alejandro: reutilizar el banco de preguntas en modo lectura. Sin
cambios al modelo de datos. **La tensión de abajo queda resuelta: sin
correo** — el historial es solo historial. Decisión propia al
diseñarlo: el resultado por pregunta ("Correcta"/"Incorrecta") va sin
color de estado, porque un acierto aislado no es "muestra la evidencia"
(ADR-008) y un color = un significado.

*(Texto original, se conserva como historial:)*
Idea de Alejandro: ver la interacción completa del estudiante a lo
largo de la experiencia — qué ítem enfrentó por evidencia, su
respuesta, y su certeza (`Respuesta.certeza`, CRI 0-5, ADR-008 punto
2, ya existe en el MR — no hace falta ampliar el modelo de datos para
esto). Es el destino del botón "Ver historial completo" dentro de una
card expandida de A1 — **no** un "Perfil del estudiante" con secciones
distintas (se consideró esa idea y se descartó: el historial es la
misma información de la card expandida, solo más granular, no un
contenedor con partes heterogéneas). Explícitamente fuera de la sesión
en que se planteó.

**Tensión sin resolver, encontrada 2026-08-29:** al quitar el correo de
la card colapsada (A1), Alejandro confirmó que reaparece en A4 — pero
el correo es un dato de **identidad**, no de interacción/historial. Es
exactamente la mezcla heterogénea que llevó a descartar "Perfil con
secciones distintas" un poco antes en la misma sesión. Alejandro
también se refirió a A4 como "el perfil" más de una vez en el camino.
No se resuelve ahora — solo se deja anotado para que quien diseñe A4 no
asuma que sigue siendo historial puro sin revisar esto primero.

### A5. Toma del diagnóstico (pantalla del estudiante) — ESPECIFICADA 2026-09-26
Era el motivo original para tocar el flujo del estudiante (resuelve
H-2/H-3 de la revisión del docente, sección D). Se pausó el 2026-09-04,
antes de empezar, a favor de A9 (Auth); retomada el 2026-09-26.

**`23-spec-toma-diagnostico.md`** — 4 ventanas (020 a 023): pantalla de
inicio (3 estados: No iniciada/En curso/Completada, derivados sin tocar
el MER, mismo criterio que el Badge del Dashboard), ítem, certeza (CRI
0-5, componente nuevo) y cierre. Decisiones reales:
- **Sin indicador de progreso** — la cantidad de ítems varía según la
  certeza reportada (ADR-016), cualquier contador sería falso una parte
  de las veces.
- **Certeza en un paso separado**, no en la misma pantalla que la
  respuesta — decisión de Alejandro.
- **Advertencia al salir a medias es del navegador (`beforeunload`)**,
  no un botón en pantalla — las ventanas de ítem/certeza no tienen
  encabezado ni botón "←", a propósito (secuencia de un solo sentido).
- **"En curso" retoma exactamente donde quedó**, reconstruido desde
  `Presentación` (`orden_presentacion`) — no reinicia. Decisión de
  Alejandro, con una idea a futuro anotada y no resuelta: dar al
  estudiante algún resultado propio por evidencia al completar, en vez
  de nada — **contradice el principio "solo el docente ve
  resultados"**, así que si se retoma más adelante hay que revisar ese
  principio primero, no solo agregar una pantalla. *(Corrección
  2026-10-21: aquí decía que ese principio venía "del glosario y de
  ADR-018". Era falso — ninguno de los dos lo menciona; el principio
  solo existía en `23-spec`. Se formalizó como **ADR-028**, punto 4.)*

**`24-spec-modal-cargando.md`** — Ventana 024, componente genérico
reutilizable en cualquier modal que espere respuesta del servidor.
Cierra un vacío real: ninguno de los 22 specs anteriores lo tenía
definido. Sin botón de cerrar, excepción documentada a la regla general
de `08-spec-unirse-codigo.md`.

**`25-spec-modal-confirmar-eliminar-salir.md`** — Ventana 025, 2
variantes (Docente: eliminar experiencia; Estudiante: salir/
desinscribirse). Cierra la nota "pendiente, fuera de esta ventana" que
`09-spec-vista-interna-marco.md` dejaba abierta sobre el botón "...".
**Primer uso de `#991B1B` (Error) como fondo de botón** — hasta ahora
solo se usaba en texto/borde de validación. **Genera V-11** (ver
sección C) — el comportamiento de borrado en cascada no está decidido a
nivel de MR.

Tokens verificado en los 3 archivos y en `09-spec-vista-interna-marco.md`
(corrección retroactiva), limpio. Consistencia y cadena, sin correr
todavía tras este cambio — pendiente antes de dar la fase por cerrada.

### A6. Dashboard de estudiante, perfil/cuenta — se funde con A9
Lo que quedaba de "Auth, dashboard de estudiante, perfil/cuenta" pasa a
ser parte de A9, ya que se abrió esa puerta completa.

**Agregado real 2026-09-12, al retomar A5:** al diseñar la "vista de la
experiencia" del estudiante (ver A5 abajo) surgió que el Dashboard de
Estudiante necesitaba un **Status Badge propio** — progreso del
estudiante en cada experiencia (No iniciada/En curso/Completada),
derivado de `Presentación`/`Resultado` sin tocar el MER. No contradice
la corrección del 2026-09-04 (que retiró el badge Borrador/Publicada
del estudiante, correctamente — ese eje nunca varía para él): es un eje
distinto, que sí varía card por card. Se agregó también el Bloque 3 de
filtros para Estudiante (Todas/No iniciadas/En curso/Completadas),
reactivando ese bloque con una variable que sí tiene sentido, a
diferencia de la que llevó a quitarlo.

**Corrección de género y plural, mismo día:** primero se escribieron
los 3 estados del estudiante en masculino ("No iniciado"/"Completado")
y el chip del Docente quedó "Borrador" (singular) al lado de
"Publicadas" (plural). Alejandro encontró las dos cosas. Regla real,
aplicada de ahí en adelante: el **Badge** (una card puntual) va en
singular y concuerda en género con "experiencia" — por eso
"No iniciad**a**"/"Completad**a**", igual que "Publicada". El **Chip**
(filtra la lista) va en plural, al lado de "Todas" — por eso
"Borrador**es**" (mismo término que la carpeta de Gmail) y "No
iniciad**as**"/"Completad**as**".

**De paso, mismo día — 2 puntos más resueltos sobre el Dashboard:**
- **Badge de rol (Docente/Estudiante) junto al avatar del Sidebar —
  descartado.** Se propuso y se rechazó con la misma prueba que ya
  había retirado el badge Borrador/Publicada del estudiante: el Sidebar
  de cada rol es un Frame separado que nadie ve junto al del otro rol,
  y el rol de una cuenta es fijo para siempre (`20-spec-auth-elige-rol.md`)
  — el badge diría siempre el mismo valor, para la misma persona, en
  cada sesión. No distingue nada.
- **Metadata de la card, separada por rol** (antes un solo formato para
  los 2): Docente se queda con `"Área · Grado · N estudiantes"` — las 3
  distinguen algo real entre las experiencias de un mismo docente.
  Estudiante cambia a `"Área · Nombre del docente"` — Grado y N
  estudiantes se retiran (señal débil o constante para el estudiante) y
  se agrega el nombre del docente, dato que no existía en ningún lado
  de su vista y es lo que de verdad distingue una experiencia de otra
  si tiene varias.

`04-spec-dashboard.md` actualizado con los 3 puntos; tokens verificado
limpio; 1 falso positivo real del heurístico de consistencia (confundió
estos "3 estados" con los 4 de Reporte, ADR-022) documentado como
excepción en `verificar_consistencia.py`.

### A10. Cierre de Fase II — decisiones del 2026-10-21

Barrido completo de lo pendiente contra el texto de MODESEC y las 22
pantallas existentes. Resuelto en una sesión:
- **Generación del banco** → espera en pantalla, "todo o nada"
  (**ADR-027**). Sin estados de generación en el modelo.
- **Banco del docente** (**ADR-026**): agrega preguntas propias, se
  retira "pedir generar más" (ADR-009), Guardar/Cancelar en el modo
  edición (no existía), mínimo **6 ítems activos por evidencia** para
  publicar, y **banco congelado al publicar**. Cambios en `12`, `14` y
  `15`.
- **"Configuración" se retira del Sidebar.** El bloque de perfil
  completo (avatar, nombre, correo) pasa a ser el botón que abre el
  modal nuevo `26-spec-modal-mi-perfil.md` (Ventana 026), que reutiliza
  "Completa tu perfil" — ideas de Alejandro. "Cerrar sesión" queda
  como único ítem secundario y lleva a Iniciar sesión, sin
  confirmación.
- **Agregar pregunta** → ícono "+" al final del separador de cada
  evidencia en el banco (idea de Alejandro), con zona clicable de
  `32px` (WCAG 2.2 pide mínimo 24) y nombre accesible "Agregar
  pregunta".
- **Historial del estudiante** → A4, arriba.
- **8 referencias viejas** ("se especifica aparte", "sin especificar
  todavía") corregidas en 7 pantallas — una la había dejado a medias la
  sesión del 2026-09-26 (`09`, sección 7).
- **2 huecos de herramientas corregidos:** `verificar_consistencia.py`
  tenía el número de la última ADR escrito a mano (25) y marcó
  ADR-026/027 como inexistentes; ahora lo lee de `decisiones.md`.
- **Seguridad:** `DSE-2/backend-auth.zip` (con el `.env` adentro) no
  estaba excluido de git. Agregado a `.gitignore`.

**Sigue abierto en Fase II:**
- ~~**G** — desplegable de Grado de `06-spec`~~ → **confirmado
  2026-10-21.**
- **V-10** (contraste del gris) — diferido por decisión de Alejandro;
  no toca el modelo de datos.
- **A7**, abajo.

### A11. Revisión de coherencia antes de Fase III — 2026-10-21

Barrido de Fase I (8 docx), `diseno/` (5 documentos) y Fase II contra
todas las decisiones vigentes, para entregarle al responsable del MER
un conjunto sin contradicciones. Fase II ya estaba limpia; los
problemas estaban en Fase I y en `diseno/`, escritos en agosto.

**Corregido:**
- **`08-diseno-aprendizaje`** describía dos reglas de diagnóstico
  contradictorias: la tabla con "mínimo 4, tope 6" (ADR-016) y la
  secuencia con la regla retirada de ADR-008 ("si la primera es
  decisiva, no insiste"). Sobrevivió a las 4 auditorías de agosto.
- **"El docente revisa antes de que cualquier estudiante lo vea"**,
  repetido en `vision`, glosario, Fase I `02`, `03`, `05` y `08`, y en
  QA-016, era falso: el sistema no lo exige. Decisión de Alejandro:
  corregir el texto, no agregar un mecanismo. Lo cierto, ahora escrito:
  nada llega a un estudiante sin que el docente decida publicar; el
  sistema le recuerda revisar.
- **`03-sistema-competencias`**: "banco ampliable a pedido del docente"
  (retirado por ADR-026). **Además, su XML estaba dañado** desde la
  edición del 2026-08-26: un "&" sin escapar en "Shrock & Coscarelli"
  (el respaldo del 2026-09-04 también lo tenía). Word podía negarse a
  abrirlo. Reparado.
- **Problema del proyecto** (`vision`, Fase I `01`): "toma horas que no
  tiene" → la necesidad reformulada por la entrevista E0 (escala de
  medición), con sus fuentes. Los entregables de DSE-1 y DSE-2 ya no se
  contradicen.
- **Estado de las ADR**: las 27 decían "aceptada". Ahora 12 dicen qué
  las reemplazó o modificó; ADR-003 y ADR-009 figuran como reemplazadas.
  ADR-001 prometía una sugerencia de orden por IA sin pantalla: marcada
  como modificada por ADR-024.
- **Desactualizados**: vista de aula e historial "sin construir"
  (glosario, `06`); banco sin lo de ADR-026 (glosario, `06`); dispositivo
  "clic o toque" y falta la habilidad de juzgar la propia certeza
  (`05`); coautores de CRI "no verificados" y falta el principio
  criterio-referenciado de Shrock y Coscarelli (`07`); estado del
  proyecto y de git (`vision`); planeación de Fase II con alcance viejo y
  sin fechas (`01` de Fase II).
- **`modelo-conceptual.md`** reescrito: no tenía Docente, Estudiante,
  Inscripción ni Respuesta, y ponía el banco en la Evidencia y no en la
  Evidencia dentro de una experiencia. Declara que el MER manda.
- **Glosario**: entrada "Inscripción" agregada como **propuesta**,
  pendiente de que Alejandro la confirme (regla del glosario).

**Vacíos formalizados:**
- **ADR-028** — reglas de la toma del diagnóstico (un solo sentido, sin
  contador, certeza aparte, el estudiante no ve resultados). Solo
  existían en `23-spec`, y esta misma página les atribuía un origen
  falso (corregido arriba, en A5).
- **ADR-029** — datos de menores: la Decisión 2 de la entrevista E0
  (autorización del acudiente, Ley 1581) nunca había llegado al diseño.

**Sigue pendiente, de Alejandro:** confirmar la entrada "Inscripción"
del glosario; poner los nombres del reparto de áreas en `EQUIPO.md`.
Respaldo de los 8 docx previo a la edición:
`fase-1-diseño-educativo/.respaldo-2026-10-21/` (el `03` del respaldo
conserva el XML dañado, a propósito: es el estado original).

### A12. Currículo del MEN — anotado 2026-10-24, EN CURSO

**Hecho el 2026-10-24:**
- **Alcance decidido (ADR-033):** 4 áreas, 1° a 11°, versiones oficiales
  vigentes. Inglés y Transición fuera, con razón escrita.
- **Versiones verificadas** contra lo que hoy publica el MEN en Colombia
  Aprende: los 4 PDF oficiales son idénticos, byte a byte, a los de
  `data/curriculo-men/pdfs/`. Matemáticas V.2, Lenguaje V.2, Ciencias
  Naturales V.1, **Ciencias Sociales V.1** — se venía citando como V.2
  por el nombre del archivo (`…_v2.pdf`, igual al del MEN). Corregido en
  la Fase I (`01`, `06`) y en el README del currículo. **Sin corregir:**
  el JSON normalizado (se corrige en la auditoría, no a mano) y la
  entrevista E0, ya entregada en DSE-1 (decisión de Alejandro).
- **Primer diagnóstico de los datos:** 342 DBA (Matemáticas 118,
  Lenguaje 88, Ciencias Sociales 82, Ciencias Naturales 54); **el
  "ejemplo" no se extrajo en ninguno**; ningún registro con confianza de
  extracción "alta"; conteos a comprobar (Ciencias Naturales 2° tiene 3).

**Hallazgo del 2026-10-26 — la auditoría pasa a ser BLOQUEANTE para
cargar el catálogo:** hay 342 DBA pero solo **329 identificadores
distintos**. 13 pares de DBA *distintos* comparten identificador
(`matemáticas_2_dba_1`, `lenguaje_1_dba_1`, etc.). En cada par, uno es
del grado correcto y el otro es **del grado siguiente**: la extracción
de la V2 asignó al grado anterior el primer DBA de algunas páginas.
Contrastado con el encabezado de página de los PDF oficiales: **10
confirmados** (Matemáticas 2°→3° ×2, 6°→7°, 9°→10°; Lenguaje 1°→2°,
6°→7°, 7°→8°; Ciencias Naturales 1°→2° ×2, 9°→10°); **3 pares sin
determinar** (Ciencias Naturales 3°, 5° y 7°: ese PDF tiene otro diseño
de encabezado). Consecuencias: el docente vería en un grado DBA de
otro, a otros grados les faltan, y los conteos por grado de arriba no
son confiables. El modelo exige código único y está bien: el error es
de los datos. El MER (`16`) decía que `codigo_dba` se "verificó contra
el JSON"; el encargo 01 lo corrige.

**Recomendación para el modelo (punto 3 de abajo):** tres tablas de
referencia, no dos — **Área**, **Grado** (con su nivel educativo:
básica primaria 1°-5°, básica secundaria 6°-9°, media 10°-11°, Ley 115
de 1994) y **Documento oficial** (el PDF de cada área, con versión y
dirección), para que cada DBA diga de qué documento y de qué página se
copió. Pendiente de que el docente confirme el alcance de su pedido.

*(Texto original del 2026-10-24:)*

Planteado por Alejandro al decidir el repositorio nuevo. Se hace
**después** de organizar GitHub:

1. **Auditoría exhaustiva de la normalización** del currículo
   (`mvp/backend/data/men_sources/`, de la V2): comprobar contra los PDF
   oficiales de los DBA que se normalizó **todo** el contenido de todas
   las áreas que la aplicación ofrece, y que el texto se copió
   **exactamente**, sin cambiar ni inventar nada —es información
   oficial—. Amplía QA-013 (errores de extracción ya conocidos) y es
   requisito de QA-014 (censo de formato cerrado). Puede terminar en
   volver a normalizar desde cero.
2. **Qué hacer cuando un elemento del DBA no es texto sino imagen**
   (sobre todo los ejemplos). Hoy la regla es no mostrar la imagen y
   avisarlo (`06-spec` §2.4, ADR-011), pero eso se decidió sin saber
   cuántos casos hay ni cuáles. Revisar al hacer la auditoría.
3. **El docente pidió tablas para Área y Grado en el MER.** Alejandro
   no tiene claro el alcance del pedido. Interpretación probable, a
   confirmar con el docente: que Área y Grado sean entidades propias,
   en vez de atributos de texto dentro del DBA. Va a la lista "Entrada
   a Fase III".

### A16. Etapa actual: del acceso al último paso de crear una experiencia — 2026-10-26

**Alcance fijado por Alejandro:** se construye todo, backend y frontend,
**desde el acceso hasta el Paso 3 de "Crear experiencia"**, **sin
crearla** (crearla dispara la IA: es la etapa siguiente). Se para ahí.

El trabajo pesado lo hace Claude Code en la nube, con encargos en
`docs/encargos/`, uno detrás del otro, cada uno por pull request que se
revisa en local antes de unirlo:

1. **02 — Corregir el catálogo curricular** (prerrequisito del Paso 2).
2. **03 — Backend hasta el catálogo:** correcciones del docente R2, R4
   (ADR-039), R5 (envío real de correos: hoy el backend no envía
   ninguno), base de datos hasta el catálogo, rutas de consulta.
   **EN ESPERA:** el acceso debe seguir la guía del docente (el backend
   actual la sigue sección por sección, y sus pruebas usan `/users`), y
   hay una guía actualizada que el equipo todavía no tiene. Se reescribe
   partiendo de esa guía.
3. **04 — Frontend hasta el Paso 3:** se escribe cuando el 03 esté
   unido.

### A15. Fase IV (Producción) — EMPEZADA 2026-10-26

- **Selección de herramienta** hecha:
  `docs/modesec/fase-4-produccion/01-seleccion-herramienta-desarrollo.md`.
  Frontend: **React + Vite + TypeScript + Tailwind** (ADR-038), con los
  estilos limitados a `tokens.json`. Backend y base de datos, fijados por
  el curso (NestJS, MySQL).
- **Siguiente:** codificación por incrementos, empezando por **I1
  acceso**: alinear el backend con el MER (encargo 01, cuando se una) y
  con la revisión del docente (R2, R5; R4 espera P2), y construir su
  frontend (ventanas 014 a 019 y 026).
- **Grupo B (DSE-2):** su actividad es programar y socializar los
  módulos más importantes; coincide con esta fase. Guías de
  socialización en `docs/cursos/dse-2-203453/socializacion/`: cómo
  usarlas (`00`) y **una de muestra, Acceso (`01`)**, para que Alejandro
  la revise antes de hacer las otras cinco. Falta el enunciado exacto
  de la actividad del grupo B (rúbrica).

### A14. Revisión del docente del 2026-10-22 — EN CURSO

Notas sobre la columna vertebral (acceso y catálogo). Triaje en
`fase-3-diseno-computacional/21-revision-docente-2026-10-22.md`:
- **R1** Área, Grado (+ Documento oficial) y códigos → ADR-036.
- **R3** estado de verificación del correo → ADR-037.
- R1 y R3 → **encargo a Claude Code en la nube**:
  `docs/encargos/01-mer-catalogo-y-credencial.md`. **HECHO y unido
  (pull request #1, 2026-10-26):** Área, Grado y Documento oficial,
  código `ÁREA-GG-NN`, ciclo C6 (RI-20), RI-21, `estado_verificacion`.
  Revisado en local: no debilitó verificadores (rechazos de 41 a 57),
  todo pasa (MER 20, MR 80, UML 130, API 33), Ciencias Sociales V.1.
  PDF regenerados en local (en la nube no había Chrome).
  **Quedó para después:** (a) los datos de referencia (4 áreas, 11
  grados, 4 documentos) no están cargados en ningún script: se cargan
  en la Fase IV, con el catálogo, después de la auditoría A12; (b) la
  `guia-para-explicar-el-mer.md` está atrasada (solo tiene un aviso).
- **R2** (sin "usuario" genérico) y **R5** (correo del sistema) → Fase
  IV, al alinear el backend.
- **R4** (quitar los campos del código) → espera respuesta del docente
  (P2). **P1**: ¿también quitar CREDENCIAL?
- Se agregó `CLAUDE.md` en la raíz: instrucciones para cualquier sesión
  de Claude Code en este repositorio.

### A13. Fase III del compañero, revisada y unida — 2026-10-26

El compañero del equipo (cuenta `josemianay987-dot`, trabajando con
Claude) subió la Fase III completa en un solo commit: documentos `12` a
`20` (casos de uso, clases, objetos, secuencias, MER final, MR,
diccionario, índice y catálogo de 35 endpoints). Revisión:

- **Calidad:** todos sus verificadores pasan (MER 18/18, MR 59/59 en
  SQLite y MySQL 8.4, UML 120/120, API 33/33) y los nuestros también.
  Solo modificó dos archivos existentes (README, `md_a_pdf.py` para
  Windows); no tocó `docs/diseno/`.
- **Recibió la lista de abajo:** 10 de 12 puntos hechos (ver estado en
  cada uno). Falta Área y Grado.
- **Decisiones que dejó por confirmar, confirmadas por Alejandro:**
  ADR-035 (servicio de IA en la experiencia —modifica ADR-030 p. 4—,
  retomar el registro a medias, ítem inválido = falla del servicio,
  borrado en cascada). **La entidad CREDENCIAL**, que introdujo sin
  decisión formal, queda respaldada por ADR-034.
- **Puesto al día:** RF-01-07, RF-02-07, RF-03-02, RF-03-03, RF-04-12
  (`11`), `modelo-conceptual.md`, glosario (Inscripción), `12` y `19`
  (decisiones marcadas como confirmadas).
- **Unión** de su commit con el nuestro (ADR-033): sin conflictos.

### Entrada a Fase III — cambios al modelo que dejó Fase II

*(Estado al 2026-10-26, contra `16-modelo-entidad-relacion.md`.)*

Para aplicar todos juntos al rehacer MER → MR → diccionario:
1. ✔ **Hecho en `16`.** `Ítem.origen`: 3 valores — `ia`, `editado_docente`,
   `creado_docente` (ADR-026).
2. ✔ **Hecho en `16`.** **Retirar `Ítem.estado_revision`** (ADR-026). Cierra V-7.
3. ✔ **Hecho en `16` (RI-14).** Regla nueva: publicar exige ≥ 6 ítems no excluidos por cada
   evidencia incluida (ADR-026).
4. ✔ **Hecho en `16` (RI-10, reforzada).** Regla nueva: con la Experiencia Publicada, ningún Ítem ni Opción de
   su banco se crea, edita ni cambia `excluido` (ADR-026 — más fuerte
   que RI-10, que solo protegía ítems ya presentados).
5. ✔ **Hecho en `16`.** `Experiencia.estado` se queda en 2 valores; creación atómica con el
   banco (ADR-027).
6. ✔ **Resuelto en `16` (RI-19):** el formato vive en el dictamen de la evidencia. Antes: el formato se decide por evidencia (ADR-006) pero se guarda
   por ítem — nada impide formatos mezclados en una evidencia.
7. ✔ **Cerrado por ADR-035:** borrado en cascada, probado en `17`. Antes: V-11 (borrado en cascada al eliminar Experiencia o
   Inscripción).
8. ✔ **Hecho en `16` §12.** **ADR-029**: no se agrega entidad Acudiente; declarar como vacío del
   modelo la ausencia de la autorización del representante legal.
   ADR-028 no cambia el modelo (todo lo que exige ya existe:
   `Presentación`, `Respuesta`, RI-10).
9. ✔ **Cambiado por ADR-035:** se guarda en la Experiencia, no en cada Ítem (RI-17). Texto original: **ADR-030**: cada Ítem guarda el servicio de IA y el modelo que lo
   generó; vacío si `origen = creado_docente`. Al editarlo, conserva
   el servicio de origen.
10. ✔ **Hecho en `16`, y programado y probado en `uml/regla.py`.** **ADR-031 resuelve V-5 / H-7**: la regla de parada exacta ya existe,
    así que `Resultado.estado` es computable. `Respuesta.correcta` en
    emparejar y ordenar es todo o nada. Al retomar, se reusa la
    Presentación sin respuesta (no se crea otra): compatible con la
    llave de Presentación (inscripción, ítem) y con el tope de RI-9.
11. ✔ **Hecho en `16`, `17` y `18` (2026-10-26, encargo 01, ADR-036).** ÁREA, GRADO y
    DOCUMENTO_OFICIAL como entidades; DBA sin `area`/`grado` como texto; código del DBA
    `ÁREA-GG-NN` sin tildes (RI-21); ciclo nuevo C6 cerrado por RI-20. En la misma pasada,
    `estado_verificacion` en CREDENCIAL (ADR-037). Sigue abierto en los **datos**: el JSON
    repite 13 identificadores de DBA, y con el código nuevo chocan los mismos 13 (A12).
    Texto anterior: **Área y Grado como tablas propias** (pedido del docente, A12), recomendado
    además Documento oficial.
12. ◐ **En parte:** `16` §12 numera los vacíos de forma coherente (V-1 a V-12), pero la tabla de la sección C de este archivo sigue con la numeración vieja. **Identificadores duplicados**: V-5, V-6 y V-9 significan cosas
   distintas en la sección C y en la sección D de este archivo.
   Renumerar antes de entregar un MER "sin errores".

### A7. Puntos 4, 5 y 6 de Fase II MODESEC — HECHOS 2026-10-21

- `28-mapa-navegacion.md` + `navegacion/mapa-navegacion.{svg,png}`.
- `29-guion-tecnico.md` — generado; reglas comunes (ventana estándar) +
  índice de las 27 ventanas.
- `30-indice-recursos.md` — recursos globales (Inter, Lucide, logos de
  Google y Microsoft, foto de perfil) y por ventana. Sin audio ni video.
- **Fuente única:** `navegacion/mapa_navegacion.py` genera el mapa y la
  tabla del guión, y verifica que ninguna ventana quede fuera, ninguna
  flecha apunte a una ventana inexistente y ninguna pantalla quede
  huérfana. Probado introduciendo los 3 errores a propósito.
- **2 detalles menores encontrados al hacer el índice, sin resolver:**
  la forma del ícono de "Mis experiencias" y la del ícono del estado
  vacío del Dashboard nunca se definieron en `04-spec` (solo su tamaño).
  No bloquean nada; se eligen al construir en Figma.

*(Texto original:)* Puntos 4, 5 y 6 de Fase II MODESEC — NUNCA INICIADOS
Mapa de navegación · Guión técnico · Índice de recursos. Los 3 puntos
restantes de la fase, según la fuente primaria.

### A8. Flujo del estudiante — EN CURSO desde 2026-09-04
Motivado por la revisión del docente al MER (ver sección D): la toma
del diagnóstico es la pantalla que falta para que H-2/H-3 dejen de ser
problemas. Adelantada frente al plan original ("todo el flujo del
docente primero").

- **ADR-025 — dispositivo.** Esta versión, solo computador — es una
  demo para docentes, no despliegue con estudiantes reales. El acceso
  desigual a sala de cómputo entre instituciones queda reconocido y
  diferido, no ignorado — mismo criterio que ADR-007.
- **Corrección real encontrada en el Dashboard del estudiante
  (`04-spec-dashboard.md`), 2026-09-04:** el Status Badge
  (Borrador/Publicada) de la Row Card se mostraba también al
  estudiante. Es el mismo error, sin corregir hasta ahora, que ya había
  llevado a quitarle el Bloque 3 de filtros unas líneas más arriba en
  el mismo archivo: un estudiante nunca ve una experiencia en Borrador,
  así que el badge diría siempre "Publicada" — no distingue nada. Se
  retira para Estudiante, sin cambios para Docente.
- Orden de pantallas del flujo del estudiante — **resuelto en A5**
  (2026-09-26): Dashboard → 020 (inicio) → 021/022 en bucle
  (ítem/certeza) → 023 (cierre) → Dashboard.

### A9. Auth completo — EN CURSO desde 2026-09-04, prioridad sobre A5

**Por qué se abrió ahora:** Alejandro quiere reutilizar pantallas de un
diseño antiguo (mismo criterio ya aplicado en toda la Fase II: tomar la
estructura de una referencia vieja, reconstruirla con nuestros tokens).
Ya tiene 6 pantallas de referencia resueltas en su cabeza y quiere
aprovechar. **Empujó a A5 (toma del diagnóstico) a un segundo plano**
— A5 sigue siendo la razón original por la que se abrió el flujo del
estudiante, no hay que perderla de vista cuando A9 se cierre.

**Resuelve V-8** (autenticación, registro y credencial — bloqueaba A6).

**Las 6 pantallas de referencia que Alejandro trajo** (capturas de un
diseño anterior, fuera del sistema de tokens actual — mismo tratamiento
que cualquier otra referencia vieja de este proyecto: se reconstruye la
estructura con nuestros colores/tipografía/componentes, no se copia el
visual tal cual):
1. **Iniciar sesión** — correo + contraseña, "¿Olvidaste tu
   contraseña?", botón primario, **3 botones de login social (Google /
   Apple / Microsoft)**, link a Registro.
2. **Crear cuenta** — correo + contraseña, checkbox de términos,
   mismos 3 botones sociales, link a Login.
3. **Verifica tu correo** — 6 casillas de código (mismo patrón ya
   existente de `08-spec-unirse-codigo.md`), reenvío con cuenta
   regresiva. Aparece 2 veces en las referencias de Alejandro — se
   reutiliza para 2 flujos distintos (verificación de registro y
   verificación de recuperación de contraseña).
4. **Recupera tu contraseña** (solicitud) — correo, botón "Enviar
   código".
5. **Nueva contraseña** — nueva + confirmar, botón "Guardar".
6. **Completa tu perfil** — selector de avatar (opcional, ver A1 sobre
   el ícono por defecto ya definido), nombre, apellido.

**Lo que las referencias NO tienen y hay que agregar:** selección de
rol (Docente / Estudiante) — señalado por el propio Alejandro. Sin
definir en qué pantalla vive todavía (¿parte de Registro? ¿pantalla
propia entre Verificar y Completar perfil?).

**Resuelto — método de login/registro (2026-09-05):** los dos al
mismo tiempo, correo+contraseña **y** Google/Apple/Microsoft, tal como
las referencias. Cierra V-8 en este punto.

**Resuelto — correo repetido entre métodos (2026-09-05):** si alguien
se registró con Google y después intenta entrar con correo+contraseña
usando el mismo correo, se le avisa que use el método con el que ya
tiene cuenta — no se crean cuentas duplicadas, no se vinculan métodos.

**Resuelto — dónde vive la elección de rol (2026-09-05), tras 2
intentos fallidos (ver historial abajo):** es un **paso nuevo, al
final de toda la secuencia**, después de "Completa tu perfil" — igual
para cualquiera, sin importar si entró con correo o con un botón
social. La cuenta (fila en `Docente` o `Estudiante` — son 2 tablas
separadas) se crea recién ahí, una vez que se sabe el rol; no hace
falta crearla antes.

**Secuencia completa confirmada:**
1. Iniciar sesión / Crear cuenta (correo+contraseña o social)
2. Verifica tu correo — **no aplica** si entró por Google/Apple/
   Microsoft, ya viene verificado por ese proveedor
3. Completa tu perfil (nombre, apellido, avatar)
4. **Elige tu rol** (Docente/Estudiante) — pantalla nueva, no estaba en
   las referencias
5. Entra a la plataforma (Dashboard según el rol elegido)

*(Historial de cómo se llegó aquí, por si hace falta releer: el primer
intento propuso resolver el rol "solo por la puerta de entrada" —
Alejandro lo corrigió, porque sin QR/link no existe tal puerta de
entrada diferenciada. El segundo intento propuso preguntarlo dentro de
"Crear cuenta", con un caso aparte para login social en "Completa tu
perfil" — Alejandro lo rechazó por sobrecomplicado: los botones
sociales son solo un atajo para no escribir correo/contraseña, no un
camino distinto que amerite lógica separada. La versión "al final,
igual para todos" fue la que Alejandro pidió directamente.)*

**Pantalla 1/4 ESPECIFICADA (2026-09-05):**
`17-spec-auth-login-registro.md` (Ventana 014) — Login y Registro en un
solo spec (mismo criterio que el Dashboard Docente/Estudiante). Cambios
reales sobre la referencia, no solo de estilo:
- **Sin Apple** — cuenta de desarrollador de pago (99 USD/año), y esta
  plataforma es web, no aplica la obligación de la App Store de
  ofrecerlo. Quedan Google y Microsoft, gratis de integrar.
- **Sin checkbox de términos y condiciones** — no existe ese documento;
  fingir que sí sería peor que no tenerlo. Una versión real necesitaría
  términos y política de privacidad reales, con criterio legal —
  agravado porque los usuarios son menores de edad (Habeas Data,
  Colombia).
- **Estados de error agregados** (no estaban en la referencia):
  credenciales incorrectas, correo ya registrado, y el caso de correo
  registrado con otro método (resuelve la decisión ya tomada arriba:
  se avisa, no se vincula).
- **Ayuda de contraseña agregada** en Crear cuenta (mínimo 8
  caracteres) — evita que el error se descubra recién al enviar.
- **Validado, no vacío:** la referencia no tiene campo "Confirmar
  contraseña" — es correcto, no un olvido: con el ícono de mostrar/
  ocultar ya disponible, pedirla dos veces es redundante.
- Botones sociales **apilados con texto** ("Continuar con Google"), no
  en fila solo con el ícono — más claro para público no técnico.
- Primer enlace de texto de todo el proyecto — sin color de "link"
  en la paleta (no se agrega uno nuevo), se distingue con subrayado.
Tokens verificado, limpio. Consistencia y cadena, íntegras.

**Aclaración de arquitectura (2026-09-05):** todas las pantallas de
Auth comparten el mismo marco (card centrado `480px`, definido una vez
en `17-spec-auth-login-registro.md` sección 2.1) — mismo criterio que
Crear Experiencia (Paso 1/2/3) y Vista Interna (3 pestañas): marco
compartido, cada momento con su propia Ventana, no se re-describe el
marco en cada spec.

**Pantalla 2/6 ESPECIFICADA (2026-09-05):**
`18-spec-auth-verifica-correo.md` (Ventana 015) — reutilizada por 2
flujos (verificación de registro nuevo, verificación antes de cambiar
contraseña). Diferencias reales frente a "Unirse con código", no solo
de contexto: código **solo numérico** (sin excluir ambiguos — nadie lo
dicta en voz alta, lo genera el sistema y lo escribe quien lo recibió
por correo); descripción partida en **2 líneas fijas** (texto fijo +
correo real en su propia línea, Bold) en vez de una sola oración larga,
para que la altura de la card no varíe según qué tan largo sea el
correo de cada persona; agregado el componente "Reenviar con cuenta
regresiva" (00:30 → activo), nuevo en el proyecto. Tokens verificado,
limpio.

**Pantalla 3/6 ESPECIFICADA (2026-09-05):**
`19-spec-auth-completa-perfil.md` (Ventana 016). Decisiones reales, no
solo copiadas de la referencia:
- **Pre-llenado desde login social** — si viene de Google/Microsoft,
  nombre, apellido y foto llegan ya cargados (editables), en vez de
  vacíos como en el camino de correo+contraseña. La referencia no
  distinguía los 2 caminos.
- **Nombres y Apellidos, sin Label — reconsiderado en el camino
  (2026-09-05).** Primero se decidió CON Label (comparten ícono de
  persona, riesgo de ambigüedad); Alejandro lo revisó de nuevo y se
  revirtió: el riesgo era más teórico que real (se llenan en orden, el
  de arriba ya queda visible al llegar al de abajo) — consistencia con
  Correo/Contraseña ganó. Placeholder plural "Nombres"/"Apellidos",
  no singular — encaja con la convención colombiana.
- **Avatar "simple pero trabajado"**: sube archivo (JPG/PNG, ≤5MB),
  recorte automático, sin editor de imágenes. Círculo `96px` (ya
  existía en `espaciado_px`, no se agregó nada). Opcional, no bloquea
  "Continuar". **Ícono por defecto: galería/subir, no la silueta de
  persona de Tab Estudiantes** — a propósito, son roles distintos (acá
  es un control activo de subida, no una etiqueta pasiva de roster).
  **Interacción simplificada dos veces en el camino:** primero se
  definió una insignia de cámara superpuesta en la esquina (exigía
  sacar una capa de Auto Layout y posicionarla a mano — Alejandro no
  lograba visualizarlo); se reemplazó por un patrón más simple y
  conocido (Facebook/LinkedIn): capa oscura del mismo tamaño que el
  círculo, visible solo en hover, con la cámara centrada — sin ninguna
  posición que calcular.
- **Auditoría de las descripciones de Auth (2026-09-05):** se encontró
  que "Continúa tu experiencia.", "Empieza con una experiencia
  adaptativa." y "Personalízalo para una mejor experiencia." (`17` y la
  referencia de esta pantalla) no informaban nada real — relleno de
  ánimo copiado sin pasar por el filtro "dice qué es esto en el
  modelo" que se le exige al resto del proyecto desde Crear Experiencia.
  Corregidas en `17` (retroactivo) y en esta pantalla, esta vez
  contando caracteres para que quepan en una línea a `480px` —error
  aparte, cometido al proponerlas la primera vez: salieron demasiado
  largas (64-86 caracteres) por no aplicar la misma medida ya usada en
  `16-spec-modal-codigo-invitacion.md`.

**Pantalla 4/6 ESPECIFICADA (2026-09-05):**
`20-spec-auth-elige-rol.md` (Ventana 017) — última pantalla de Auth, sin
referencia de diseño anterior (se construyó reutilizando la Card de
área de Crear Experiencia Paso 1, tal cual, sin reinterpretar su
tamaño). Decisiones reales:
- **Descripción "No podrás cambiarlo después."** — `Docente` y
  `Estudiante` son 2 tablas separadas en el MER, no una casilla
  editable; se le avisa a la persona antes de elegir, mismo criterio
  que el modal "Publicar experiencia".
- **Botón "Volver"** — reutiliza el footer Ghost+Primario de Crear
  Experiencia Paso 2, sin inventar un patrón nuevo. Vuelve a "Completa
  tu perfil" sin perder lo ya escrito ahí.
- **Sin mensaje de error** — se preguntó explícitamente "¿por qué
  fallaría la creación de cuenta?" y la respuesta honesta fue: solo
  fallas genéricas de red/servidor, no una causa propia de esta
  pantalla como sí la tienen los errores de Login/Registro (contraseña
  incorrecta, correo duplicado). No se inventó un caso sin causa real.
- **Ancho**: se confirmó que el ancho fijo de `480px` del marco de Auth
  no cambia por pantalla — el contenido de esta pantalla en particular
  (`200+16+200` cards + `32px` de padding a cada lado) llena ese fijo
  exacto, sin necesitar Fill ni ningún ajuste (se descartó esa idea:
  "las cards miden lo que miden, es reutilización de un elemento").
Tokens verificado, limpio.

**Pantallas 5/6 y 6/6 ESPECIFICADAS (2026-09-10) — flujo de Auth
completo, las 6 pantallas listas:**
- `21-spec-auth-recupera-contrasena.md` (Ventana 018) — solicitud.
  Decisión real: **sin "correo no encontrado"** — al enviar, siempre
  avanza al mismo paso exista o no la cuenta, para no confirmarle a un
  desconocido si un correo está registrado (enumeración de cuentas).
  Solo valida formato, no existencia. Comparte
  `18-spec-auth-verifica-correo.md` para el paso de verificación
  (flujo 2 de ese documento).
- `22-spec-auth-nueva-contrasena.md` (Ventana 019) — un solo campo de
  contraseña, sin "confirmar contraseña" (mismo criterio que Crear
  cuenta: el ícono de mostrar/ocultar ya permite verificarla). Al
  guardar, vuelve a Iniciar sesión con un mensaje de confirmación en
  `#555555` — no se inventó un color de "éxito" que no existe en la
  paleta.

De paso se corrigió un error real encontrado al escribir estas dos:
`17-spec-auth-login-registro.md` tenía el enlace "¿Olvidaste tu
contraseña?" apuntando a "Ventana 015", que ya es "Verifica tu correo"
— una pantalla distinta, ya especificada. Se corrigió a Ventana 018, y
se cerraron las dos referencias "sin especificar todavía" que quedaban
en `18-spec-auth-verifica-correo.md`. Tokens verificado en los 4
archivos, limpio; consistencia y cadena, íntegras.

**Corrección 2026-09-11 — segundo error real, encontrado por
Alejandro al revisar el prototipo en Figma:**
`18-spec-auth-verifica-correo.md`, sección 2.6, tenía el enlace "Volver
a inicio de sesión" con **destino fijo** a Login. Esa pantalla se abre
desde 2 flujos (Crear cuenta y Recuperar contraseña) — el destino fijo
solo tenía sentido para uno: alguien que viene de Crear cuenta no tiene
nada que "reanudar" en Login, y el link le hacía perder el correo y la
contraseña ya escritos. Se corrigió a texto genérico **"Volver"**, sin
nombrar el destino — mismo criterio que el botón "Volver" de
`20-spec-auth-elige-rol.md` (vuelve al paso anterior exacto, sin perder
lo ya escrito). El camino a Login sigue disponible, un clic más allá,
por el enlace "¿Ya tienes cuenta? Inicia sesión" que ya existe en
`17-spec-auth-login-registro.md`, sección 2.9.

De paso, en `21-spec-auth-recupera-contrasena.md` se corrigió el botón
"Enviar código" (antes "Continuar", sin razón real detrás del nombre
genérico) y se le agregó estado Deshabilitado/Habilitado por formato de
correo — el spec original no lo tenía por copiar sin cuestionar el
patrón de Login/Registro; el patrón correcto, con un solo campo y una
sola condición de completitud, es el que ya usa el resto del proyecto
para ese caso (Unirse con código, Verificar código, Continuar de Elige
tu rol). Tokens verificado en los 2 archivos, limpio; consistencia y
cadena, íntegras.

**Corrección 2026-09-11 (continuación) — la misma corrección se quedó
a medias:** al revisar las capturas de Figma contra los 3 documentos,
`22-spec-auth-nueva-contrasena.md` seguía diciendo "Sin estado
Deshabilitado" mientras el botón "Guardar" en Figma ya aparecía
deshabilitado — mismo argumento que ya se había aplicado a Recupera
contraseña (un campo, una regla de completitud exacta), pero no se
propagó al documento gemelo. Se corrigió: Deshabilitado/Habilitado
según los 3 requisitos ya visibles en el texto de ayuda (mínimo 8
caracteres, mayúscula, número). Consecuencia en cadena: como la regla
de habilitación es exacta y completa (no una aproximación, a diferencia
del correo), un intento de "Guardar" con formato inválido deja de ser
alcanzable — se retiró el mensaje de error de formato y el estado
visual de error del campo, mismo criterio ya usado en
`20-spec-auth-elige-rol.md` (no se dibuja un estado para un caso que no
puede ocurrir). Tokens verificado, limpio; consistencia y cadena,
íntegras.

**Nota de alcance (ADR-025):** esta versión es una demo para docentes,
no despliegue real — vale la pena mantener esto en mente si la
discusión deriva hacia seguridad de producción (verificación de correo
real, límites de intentos, etc.), que puede ser más de lo que esta
versión necesita.

---

## B. Auditoría de consistencia — CERRADA (2026-08-26)

Barrido completo de `diseno/`, `fase-1-diseño-educativo/` y
`fase-2-diseno-multimedial/` (27 documentos). **Resultado final: 0
inconsistencias pendientes.**

**Los 9 errores reales que se encontraron y corrigieron:**

| Archivo | Qué estaba mal |
|---|---|
| `glosario.md` (Reporte) | 6 errores: "acción docente recomendada" (ADR-010 descarta recomendaciones de IA); "nunca en un veredicto" (ADR-018 sí calcula uno); "dos vistas" (son 2 secciones + la de aula); 3 estados por evidencia (son 4); "brecha extendida/aislada" (ADR-017); "umbrales los ajusta el docente" (ADR-013) |
| `glosario.md` (Diagnóstico) | Cabecera decía "ajustado por ADR-009"; ADR-016 lo reemplazó |
| `03-tokens-diseno.md` | Sección "Pendiente, para cuando se diseñe Reporte" con las 4 categorías viejas — Reporte ya se diseñó. Reescrita. Y `#888888` (Sin concluir) documentado en la paleta |
| `03-sistema-competencias.docx` | Banco 6→12; nota entera sobre por qué el 6 era débil, reescrita con el fundamento de ADR-016 |
| `06-diseno-contenidos.docx` | "nunca en un veredicto" → "nunca en un texto redactado por IA" + los umbrales los fija el sistema |
| `08-diseno-aprendizaje.docx` | Banco 6→12 |

Los `.docx` tienen respaldo en `fase-1-diseño-educativo/.respaldo-2026-08-26/`
y se verificó su integridad (zip OK, `<w:body>` balanceado, 11 partes).

**Dos herramientas quedaron, re-ejecutables:**
- `verificar_consistencia.py` (esta carpeta) — rastrea términos que un ADR
  posterior dejó obsoletos, citas a ADR/QA inexistentes y referencias a
  archivos rotas. Lleva una lista de **excepciones verificadas a mano**,
  cada una con su razón escrita.
- `fase-2-diseno-multimedial/verificar_tokens.py` — corregido: ya no
  falla sobre `03-tokens-diseno.md`, que es el documento que **registra
  los valores rechazados**. Se resolvió con una lista explícita y finita
  de esos rechazos, no con un heurístico de prosa (un heurístico podría
  tapar un error real después). Comprobado que sigue atrapando errores
  reales inyectando un color falso.

**Dos huecos que la propia auditoría encontró en sus herramientas:**
1. El detector buscaba línea por línea → cualquier frase partida en dos
   líneas era invisible. Caso real: `glosario.md` decía "los umbrales…
   los ajusta / el docente" y no lo veía. Corregido con ventanas de 3
   líneas.
2. El detector solo indexaba 3 carpetas → toda referencia a un archivo
   del backend o de fase-3 salía como "inexistente" (9 falsos positivos).
   Ahora indexa el repositorio completo.

**Lección, para no repetirla:** el detector encontró 3 de los 6 errores
del glosario; los otros 3 salieron leyendo. Es una red, no una garantía.

### Segunda pasada — auditoría SEMÁNTICA (2026-08-26)

La primera pasada cubrió una clase de error (términos que un ADR dejó
obsoletos). Esta cubrió lo que ninguna herramienta puede ver: leer los 8
documentos de Fase I y los 5 de `diseno/` contra los 23 ADR vigentes.
**8 errores más, ninguno detectable por patrones:**

| Archivo | Qué estaba mal |
|---|---|
| `08-diseno-aprendizaje.docx` | **El más grave.** Decía *"El docente, no el sistema, decide cuántos ítems observa el estudiante"* y *"responde… en la cantidad que el docente definió"* — contradice frontalmente a ADR-016 (lo fija el sistema, mínimo 4/tope 6). También describía la regla vieja de ADR-008 ("repetir solo si no fue decisivo") y citaba ADR-009 como fuente vigente |
| `02-fines-educativos.docx` | *"Ningún resultado usa lenguaje de veredicto"* — colisión terminológica: ADR-018/022 llaman "veredicto por DBA" a su propio resultado. Cambiado a "lenguaje de certeza" + nota que separa los dos sentidos |
| `04-conceptos.docx` | Faltaba el concepto "Estado general por DBA" (ADR-018/022) en la lista — solo estaba el resultado por evidencia |
| `11-spec-vista-interna-materiales.md` | Decía "veredicto general" donde el modal dice "Estado general" — dos palabras para lo mismo, **ambas visibles al docente** |
| 5 documentos de Fase I | 7 referencias cruzadas apuntaban a `NN-nombre.md` cuando los archivos son `.docx` |
| `vision.md` | *"Este documento y el glosario cierran la fase de diseño educativo"* — falso desde que existen los 8 documentos de Fase I. Y el "Pendiente: el plan de curso no existe, el semestre inicia en ~4 días", ya vencido |
| `preguntas-abiertas.md` | QA-001 sigue **abierta** pero enunciada con "punto de aprendizaje", término retirado el 2026-08-07 |

**Por qué ninguna herramienta los vio:** no tienen firma de palabra
clave. "El docente decide cuántos ítems" no contiene ningún término
prohibido — es una frase gramaticalmente normal que resulta ser falsa.
Solo se encuentra leyendo el documento con los ADR vigentes al lado.

### Tercera pasada — coherencia DERIVACIONAL (2026-08-26)

Las dos pasadas anteriores buscaban *contradicciones*. Esta verifica algo
distinto: que la **cadena de derivación** de MODESEC se sostenga —
`diseno/` → Fase I (8 sub-etapas) → Fase II (6 puntos), donde cada
documento se apoya en el anterior.

**4 errores más, todos en `02-diagrama-contenidos.md` salvo el último:**
- Decía *"los 14 conceptos"* — quedaron 15 al incorporar "Estado general
  por DBA". **Este lo causé yo** al corregir `04-conceptos.docx` sin
  rastrear quién más dependía de ese conteo.
- El diagrama (`.dot` + `.png`) no incluía el concepto nuevo. Regenerado
  con Graphviz, con sus dos relaciones.
- Citaba ADR-009 como fuente vigente (reemplazado por ADR-016).
- **Eslabón derivacional roto:** `04-conceptos.docx` listaba "Estado
  general por DBA" pero `06-diseno-contenidos.docx` **no lo definía** —
  y MODESEC es explícito en que la sub-etapa 4 lista y la 6 define. Otra
  consecuencia de mi propia corrección. Se agregó la fila a la tabla.

**Herramienta nueva: `verificar_cadena.py`** (esta carpeta). Comprueba
4 eslabones: que todo concepto listado en Fase I·4 esté definido en
Fase I·6; que el conteo del diagrama de Fase II cuadre con Fase I; que
cada spec tenga su número de Ventana; y que toda fuente citada como
`/diseno/...` exista. Resultado actual: **CADENA ÍNTEGRA**.

**La lección más cara de esta sesión:** corregir un documento puede
desalinear otro. Dos de los 4 errores de esta pasada los introduje al
arreglar el anterior, y ninguna de las herramientas existentes los vio —
salieron al preguntarse "¿esto en qué se apoya?" en vez de "¿esto se
contradice?".

### Cuarta pasada — contra el texto oficial de MODESEC (2026-08-26)

Las tres anteriores comparaban los documentos **entre sí**. Esta los
compara contra la **fuente primaria** (`MODESEC_TISE2009.txt`): qué exige
el modelo de cada sub-etapa. Cambia la pregunta de "¿se contradicen?" a
"¿tiene lo que MODESEC pide?".

**Criterio extraído de la fuente:**
- *Fase I·3 (Competencias)* — formato de dos ámbitos: **Objetivos**
  (Enunciado + Elementos) y **Norma** (Contexto + Recursos + Indicadores).
  Verificado: nuestro documento los tiene los 5. ✓
- *Fase I·4 (Conceptos)* — solo la **lista**, sin definir. ✓
- *Fase I·6 (Contenidos)* — tabla `Concepto | Características |
  Definición`, derivada de la lista de I·4. ✓
- *Fase I·8 (Aprendizaje)* — `Elementos | Aplicación del modelo |
  Indicadores` + secuencia en prosa. ✓
- *Fase II·1 (Planeación)* — metas/objetivos + distribución de funciones
  + **cronograma**. Los tres presentes. ✓
- *Fase II — descripción de ventanas* — MODESEC pide 7 categorías:
  imagen, nombre, texto, audio, video, animación, acciones. Nuestros 10
  specs usan exactamente esas 7. ✓

**4 errores más, corregidos:**
- `01-modelo-entidad-relacion.md` — la sección **Reporte** seguía diciendo
  "tres estados" y usando los nombres viejos ("Resultados generales/por
  evidencia"). **La Cuarta revisión del MER solo tocó V-3 y no actualizó
  esta sección.**
- `03-sistema-competencias.docx` — citaba *"ADR-009 (control del docente
  sobre cantidad y orden observado)"* como fuente vigente; ADR-016
  revirtió exactamente eso.
- `06-diseno-contenidos.docx` — "Número base: 6 por evidencia (ADR-009)".
- `06-diseno-contenidos.docx` — "Dos vistas" de Reporte; hoy la vista
  principal tiene dos secciones (Estado general + Estado por evidencia)
  más la de aula.

**Chequeo nuevo, integrado a `verificar_consistencia.py`:** detectar la
cita de un ADR **reemplazado** como si fuera la autoridad vigente. Los
tres primeros errores de esta pasada no tenían ninguna palabra obsoleta
— por eso ningún verificador anterior los veía. Solo cubre ADR-009 y
ADR-018, donde el reemplazo alcanza al punto principal; ADR-013 y ADR-014
se dejan fuera a propósito, porque siguen siendo autoridad del resto de
su contenido y marcarlos daría ruido.

**Estado tras las cuatro pasadas: 25 errores corregidos**, las 3
herramientas en verde, y los 8 `.docx` verificados íntegros tras cada
edición (zip OK, `<w:body>` balanceado).

## C. Vacíos del modelo, declarados y sin resolver

| Id | Qué falta | Dónde está declarado |
|---|---|---|
| **V-1** | Marca temporal de `Respuesta` — sin ella no se ordena, ni se audita, ni se detecta un reintento | MER |
| **V-2** | Inmutabilidad de Ítem/Opción tras la primera Respuesta — hoy nada impide editar una Opción y dejar `correcta` históricamente falso. **Subió de prioridad con ADR-021** (ahora `correcta` se persiste) | MER, MR |
| **V-7** | Vocabulario de estados de revisión del Ítem, más allá de excluido/no-excluido | MER |
| **V-8** | Autenticación, registro y credencial. Bloquea A6. Idea evaluada y no adoptada: entidad `Cuenta` 1:1 con Docente y Estudiante | MER |
| **V-9** | `Item.orden_sugerido` (`04-modelo-relacional.md` línea 217) queda huérfano tras ADR-024 — se documentó como "lo sugiere la IA, lo edita el docente (ADR-005)", pero ADR-024 retira esa capacidad a nivel de evidencia. Sin resolver todavía si la columna: (a) se elimina por completo, (b) se redefine para un propósito distinto y real (ej. orden de selección adaptativa entre los 12 ítems del banco, independiente del orden de evidencias), o (c) se deja como está por ahora. Encontrado 2026-08-29 al corregir las citas de ADR-005, no analizado a fondo todavía — requiere revisar si algún mecanismo (ADR-016, la regla adaptativa) realmente lee este campo. | MR, DBML, SQL |
| **V-10** | Contraste WCAG: `#888888` (Sin concluir) aplicado a texto `13px` Bold da `3.5:1`, no pasa AA para texto normal (`4.5:1` requerido, `13px` Bold no califica como "texto grande"). Afecta al separador de `14-spec-vista-interna-estudiantes.md` Estado 3 **y** a la leyenda ya existente de `13-spec-modal-reporte.md` (mismo patrón, mismo color, mismo tamaño). Sin arreglo trivial: `#555555` (la alternativa obvia) es aún más parecido a `#52514E` (No concluyente) que `#888888` — colisión de distinción categórica, no solo de contraste. Opciones sobre la mesa, sin decidir: `#111111` (pasa contraste, pierde codificación por color) o reutilizar el violeta Informativo `#6D28D9` (pasa contraste y distinción, mezcla 2 conceptos bajo 1 color). Encontrado 2026-08-29, crítica UI/UX de Tab Estudiantes. | Reporte, Estudiantes, `03-tokens-diseno.md` |
| **V-11** | Comportamiento de borrado en cascada, sin decidir a nivel de MR: al eliminar una `Experiencia` (docente, Ventana 025) o una `Inscripción` (estudiante, "salir de la experiencia"), ¿se eliminan físicamente las filas de `Presentación`/`Respuesta` que dependen de ellas, o se conservan de algún modo? El modal ya advierte la consecuencia visible al usuario (cuántos estudiantes/respuestas se pierden), pero el mecanismo técnico detrás no está definido — mismo tipo de vacío que V-2 (persistencia de datos ya capturados). Encontrado 2026-09-26 al especificar A5. | MR |

**Ya resueltos, no reabrir:** V-3 (ADR-022), V-4 (ADR-021), V-5 y V-6
(verificados contra `curriculo_men_normalizado.json`).

### Preguntas abiertas con dependencia de datos reales
- **QA-006** — auditar los generadores de diagnóstico duplicados antes
  de construir el nuevo.
- **QA-011** — el campo `ejemplo` del DBA no existe en
  `curriculo_men_normalizado.json`; ADR-011 ya definió su rol.
- **QA-013** — bug de extracción en las evidencias (viñetas fusionadas,
  texto truncado). Bloquea a QA-014.
- **QA-014** — censo de qué proporción de evidencias admite formato
  cerrado. Alimenta a `Evidencia.aplica_formato_cerrado`.

---

## D. Fase III (Diseño Computacional) — parcialmente entregada

### MER — QUINTA REVISIÓN, 2026-09-08. Responde a las 2 revisiones externas.

`01-modelo-entidad-relacion.md` actualizado. *(Hasta el 2026-10-21: desde
ese día es un borrador anterior al cierre de Fase II, ver A11.)* **Es el MER vigente y ahora
lo declara en su encabezado** — cierra H-10, que ya había costado que
otro grupo revisara un modelo que no era el nuestro.

**Entran 3 entidades** (de 11 a 14): `Experiencia_Evidencia` (H-4),
`Evidencia_Dictamen` (H-6), `Presentación` (H-2/H-3). **Atributos
nuevos:** `Experiencia.fecha_publicacion`, `Item.origen`,
`Item.estado_revision`, `Respuesta.fecha_respuesta`. **Se retira**
`orden_sugerido` de Ítem (V-9 anterior, huérfano desde ADR-024) y
`aplica_formato_cerrado` sale de Evidencia hacia Evidencia_Dictamen.

**Vacíos:** V-1 (marca temporal) y V-2 (inmutabilidad) **resueltos** —
el segundo pasa a ser la restricción RI-10. **Nuevos:** V-5 (regla de
parada exacta, umbral de certeza — previa a cualquier implementación),
V-6 (dictamen pendiente de censo QA-014), V-9 (versionado de contenido,
diferido con razón escrita).

**H-8 cerrado: notación Chen.** El docente Ali acepta ambas; el docente
Alexander no acepta caja-tabla. Chen satisface a los dos y es la
correcta para el artefacto. Caja-tabla queda como vista de apoyo.

**Informe del otro grupo (2026-09-07), triado:** en
`revision-otro-grupo/`. Se aceptó **una** de sus 3 recomendaciones (el
versionado, como V-9 diferido). Las otras 2 se declinaron con razón
escrita. Hallazgo de fondo: **ese informe no revisa nuestro modelo** —
reconstruyeron el MER desde una imagen y llenaron huecos con supuestos
genéricos; su modelo no tiene entidad Docente, no tiene `certeza` (CRI,
base de ADR-016), revive `nivel_bloom` (retirado por QA-015) y le pone
un `puntaje_obtenido DECIMAL` a Resultado, que contradice el núcleo del
proyecto ("nunca una certeza", glosario, 3 veces).

**Diagramas REGENERADOS (2026-09-08).** En `mer-entrega/`: seis vistas
Chen (SVG + PNG), leyenda de notación y un HTML con las seis y su
párrafo de justificación. `diagrama/datos_mer.py` es ahora fuente única
real de contenido, y el generador Chen la consume (antes tenía el
contenido escrito a mano desde el 19-ago, que es como se desalineaba sin
que nadie lo notara).

**Corte de las vistas: por ciclo de vida del sistema** — currículo →
autoría → banco → entrega → captura → conclusión. Cada relación vive en
exactamente una vista; las entidades que reaparecen se dibujan como
"costura" (punteada, sin atributos, rotulada). Lo verifica
`diagrama/_verificar_vistas.py`, no el ojo — y de hecho **atrapó un
error real de modelado**: `RESPUESTA_OPCION` no quedaba en ninguna
vista, porque estaba modelada como relación N:M suelta en vez de como
la **entidad asociativa** que es (rombo dentro del rectángulo, con
llave propia y `valor_dado`), igual que "Membresía" en la referencia
que pide el docente Alexander.

**Errores propios encontrados y corregidos al construir:** conteo de
relaciones mal declarado en el encabezado (decía 15, son 16); texto que
se salía de las elipses y de las cajas (ahora el ancho se calcula del
texto); entidades débiles sin doble borde; y una línea duplicada en la
Vista 5 por una llamada que creí inocua.

### REVISIÓN DEL DOCENTE — recibida 2026-09-01, triada 2026-09-04
El docente del curso revisó el MER (versión 2026-08-20) contra Fase I y
Fase II tal como estaban hace 2-4 semanas, y entregó 12 hallazgos con un
modelo corregido propuesto. **Triaje completo en
`fase-3-diseno-computacional/05-triaje-revision-docente.md`**; el
documento original quedó guardado en
`fase-3-diseno-computacional/revision-docente/`.

Resumen del triaje — no todos los hallazgos aplican igual:
- **Grupo A (5) — se aceptan, son reales e independientes de las
  pantallas que faltan:** H-4 (falta el vínculo Experiencia–Evidencia),
  H-6 (`aplica_formato_cerrado` guardado como si fuera dato del MEN
  cuando es dictamen nuestro), H-9 (mínimos de Opción por formato),
  H-8 (notación Chen — decisión pendiente), H-11 (no se entregó
  `/diseno/`, así que media crítica se apoya en documentos que él nunca
  vio).
- **Grupo B (3) — se disuelven al diseñar la toma del diagnóstico
  (A5):** H-2, H-3 y H-12. Son los que él marca como bloqueantes. No
  son descuidos: son consecuencia de que Fase II no está cerrada.
- **Grupo C (4) — obsoletos o a medias, juzgó una versión anterior:**
  H-1 (cae casi entero por ADR-016 y ADR-024), H-5 (el atributo sí,
  pero su regla de publicación contradice lo ya decidido en
  `12-spec-modal-banco-items.md` — **no se adopta**), H-7 (la regla de
  parada sí existe en ADR-016, pero acierta en que falta el umbral
  exacto de certeza), H-10 (nuestro `01` ya está al día; el obsoleto
  real es `03-presentacion-mer.html`).

**Deuda inmediata que destapó — CORREGIDA 2026-09-04.** La cascada de
ADR-024 no había llegado a Fase I. Se corrigieron **4 menciones en 2
documentos**: `08-diseno-aprendizaje.docx` (3 — el orden sugerido por
IA, "en el orden que el docente definió", y el control del docente
sobre el orden) y `03-sistema-competencias.docx` (1 en el cuerpo + la
etiqueta de la fuente ADR-005, que decía "generación y orden"). Las 2
últimas las encontró el barrido del checklist, no la corrección
puntual — que es exactamente para lo que se creó. Respaldo en
`.respaldo-2026-09-04/`; integridad verificada en los 8 docx.

**Decisión pendiente, no técnica:** confirmar con el docente o con la
rúbrica si el curso evalúa notación Chen estricta (H-8). No se decide
por omisión.

**Fecha de entrega de Fase III:** final del semestre — hay margen para
rehacer el MER en el orden correcto (después de cerrar Fase II), no a
parches.

- **MER** — Quinta revisión, responde a los 12 hallazgos del docente.
  Diagramas Chen en `mer-entrega/` (mapa completo + 6 vistas).
- **MR — ACTUALIZADO 2026-09-19.** Ver abajo: llevaba 2 revisiones de
  atraso.
- **Diccionario de datos — ENTREGADO 2026-09-19**,
  `06-diccionario-datos.md`. 14 tablas, 72 columnas, tipos MariaDB.
- **Los 4 diagramas UML** de Fase III (análisis de requerimientos) —
  no iniciados.

### Los 3 entregables de Fase III, CERRADOS — 2026-09-19

**El problema que se encontró al ir a escribir el diccionario:**
`04-modelo-relacional.md` seguía basado en la **Tercera** revisión del
MER (2026-08-26) cuando el MER ya iba en la **Quinta** (2026-09-08). Le
faltaban justamente las 3 entidades agregadas para responderle al
docente: `Experiencia_Evidencia` (H-4), `Evidencia_Dictamen` (H-6) y
`Presentación` (H-2/H-3). Escribir el diccionario desde ese MR habría
propagado el atraso a un tercer documento.

**Por qué nadie lo notó, que es lo importante:** `verificar_mr.py`
comprobaba el MR **contra sí mismo** (DBML contra SQL). Dos artefactos
internamente coherentes y a la vez contradictorios con el MER pasaban
limpio. Esa era la brecha.

**Cambio de método, no solo de contenido:**
- `modelo-relacional/datos_mr.py` — **fuente única** del MR. De ahí se
  generan el diccionario, el DBML y el SQL. Las columnas dejan de
  listarse a mano en tres sitios distintos.
- `modelo-relacional/_verificar_mr_mer.py` — **nuevo**. Compara el MR
  contra `diagrama/datos_mer.py` (la fuente del MER): entidades,
  atributos, llaves primarias, destino de cada FK. Con este script, el
  atraso de 2 revisiones habría fallado en la primera corrida. Una
  columna del MR que el MER no declare falla la verificación salvo que
  esté documentada con su razón.
- `verificar_mr.py` reescrito para el esquema de 14 tablas: 31
  comprobaciones, 20 de ellas intentando insertar datos que deben ser
  rechazados, 2 en positivo.

**Decisión propia del MR, que el MER le delegó explícitamente:**
`resultado` lleva una columna redundante `id_experiencia` y **dos** FK
compuestas — una contra `inscripcion`, otra contra
`experiencia_evidencia`. Con eso, la vieja RI-2 ("la evidencia de un
Resultado debe pertenecer al DBA de su Experiencia") **deja de necesitar
trigger**: el motor la rechaza solo. Probado con 2 pruebas de violación.

**4 errores reales encontrados y corregidos en el camino:**
1. **El MER se contradecía a sí mismo:** RI-11 declaraba
   `Inscripcion.estado_avance` como derivado y persistido — atributo que
   no existe ni debe existir (V-3 se resolvió por ADR-022 "sin columna
   ni tabla nueva"). Residuo de un borrador. Corregido en el MER.
2. **H-10 seguía abierto:** `03-presentacion-mer.html` (19-ago,
   superado) seguía sin marcar, que era exactamente la queja del docente
   ("quien abra la carpeta encuentra el modelo superado"). Ahora abre
   con un aviso rojo.
3. **El verificador contó mal, no el modelo:** marcó 6 tablas con una
   columna llamada `indexes` — su patrón leía la línea `indexes {` del
   DBML como si fuera columna. Misma lección que ya había quedado
   anotada: averiguar de qué lado está el error antes de tocar nada.
4. **Defectos de presentación del diccionario generado:** filas de tabla
   partidas en dos líneas, y valores de dominio con `|` sin escapar que
   partían las columnas. Invisibles en el fuente, evidentes al renderizar.

**Empaquetado (cierra H-11):** `00-ENTREGA.md` indexa la entrega, mapea
los 12 hallazgos a dónde se resolvió cada uno, declara los 5 vacíos
abiertos, dice dónde están las fuentes citadas (`diseno/` va incluido) y
lista los comandos para verificar todo sin leerlo.

**Lo que se declaró en vez de taparse:** la toma del diagnóstico sigue
sin diseñarse (resto vivo de H-12), y con ella el riesgo real de que
aparezca un campo que hoy falta. `00-ENTREGA.md` §5 lo dice explícito.
También se declaró un **hueco nuevo** encontrado construyendo el MR:
nada impide que una `presentacion` empareje una inscripción de una
experiencia con un ítem de otra. Se deja declarado y no se resuelve ahí,
porque el MER no delegó esa decisión.

### Consecuencia abierta de ADR-022, ya anotada en el propio ADR
Las cards de "Estado general" de Reporte pasaron de 3 a 4 y ya están
corregidas — pero conviene re-verificar que ningún otro documento
asuma todavía que son 3 estados y no 4.
