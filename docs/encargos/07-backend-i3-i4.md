# Encargo 07 — Backend de I3 e I4: el diagnóstico y el reporte

**Para:** una sesión de Claude Code sobre este repositorio.
**Escrito:** 2026-11-16, desde la sesión local de Alejandro.
**Es el backend de los incrementos I3 (diagnóstico) e I4 (reporte)**
(`docs/modesec/fase-4-produccion/01-seleccion-herramienta-desarrollo.md`):
el estudiante se une con un código, toma el diagnóstico adaptativo y el
docente ve el reporte.

**Solo backend.** El docente del curso pide todo el backend antes de que
termine noviembre de 2026; el frontend va después, en otro encargo.
**Corre en paralelo con el encargo 06** (backend de I2: crear la
experiencia y generar el banco) en otra sesión. Por eso:
- no toques los módulos de experiencias ni de banco, ni sus endpoints
  (E-18 a E-28);
- tus pruebas **arman sus propias experiencias publicadas** con sus ítems
  y opciones, insertándolas directo en la base de pruebas con un ayudante
  de prueba (no por los endpoints de I2, que aún no existen);
- si los dos necesitan el mismo archivo (`app.module.ts`, `datos_api.py`,
  `pendientes.md`), cambia solo tus partes.

**Antes de empezar, lee:**
1. `CLAUDE.md` y `docs/diseno/pendientes.md` (A15, A16).
2. Las decisiones, en `docs/diseno/decisiones.md`. **Son la regla exacta y
   mandan sobre cualquier intuición:**
   - el diagnóstico: ADR-008, ADR-016 (mínimo 4, tope 6), **ADR-031**
     (señal fuerte, cuándo se detiene, qué pregunta sigue), ADR-024 (orden
     oficial de las evidencias), **ADR-028** (un solo sentido, sin
     contador, certeza en paso aparte, el estudiante no ve resultados),
     ADR-019 (qué eligió, no solo si acertó), ADR-021 (los resultados se
     guardan como fotografía);
   - el reporte: ADR-010, ADR-013, ADR-017, ADR-018, **ADR-022** (el 4.º
     estado, "sin concluir", y la precedencia), ADR-023, **ADR-032**
     (clasificación por evidencia);
   - los datos: ADR-029 (menores de edad: el docente no ve el correo del
     estudiante).
3. El catálogo de endpoints `docs/modesec/fase-3-diseno-computacional/20-catalogo-endpoints.md`
   §5 y §6 (**E-29 a E-37**), y sus casos de uso en `12-casos-de-uso.md`
   (**CU-21 a CU-30**). Las secuencias de `15` §5, §6 y §7.
4. El modelo: `17-modelo-relacional.md` y `18-diccionario-datos.md`
   (tablas `inscripcion`, `presentacion`, `respuesta`, `respuesta_opcion`,
   `resultado`; reglas RI-1, RI-6 a RI-13).
5. Lo que las pantallas necesitan del backend: `08-spec` (unirse con
   código), `23-spec` (tomar el diagnóstico), `13-spec` (reporte), `14-spec`
   (estudiantes) y `27-spec` (historial). Solo para saber qué datos piden.
6. Cómo se trabajó antes: `docs/encargos/03-backend-hasta-catalogo.md`.

## Parte A — La base

Ya está: `backend/sql/001_esquema.sql` tiene **todas** las tablas del
modelo relacional (2026-11-16). Si necesitas cambiar algo del esquema, el
cambio va al MR (`modelo-relacional/datos_mr.py`) y se regenera la cadena
de la Fase III; dilo en el pull request.

## Parte B — I3, el diagnóstico (E-29 a E-34)

1. **Los endpoints E-29 a E-34**, como los describe el catálogo, solo para
   el rol estudiante (y cada uno solo sobre sus inscripciones: `403` si
   no).
2. **La regla adaptativa** (CU-25, ADR-031) va en **una clase sola, sin
   base de datos ni HTTP**: recibe las respuestas de una evidencia y dice
   si concluyó y con qué resultado. Así se prueba con todos sus casos.
   Cada caso de ADR-031 tiene su prueba unitaria con el número de la
   regla en el nombre de la prueba.
3. **Lo que el estudiante nunca recibe** (RF-04-08, ADR-028): si acertó,
   `es_correcta`, `hipotesis_error`, el número de pregunta, cuántas
   faltan, ni su resultado. Una prueba de punta a punta lo comprueba
   revisando las respuestas JSON completas, no solo un campo.
4. **Las reglas de integridad:** una respuesta no se cambia (RNF-10); una
   opción de otro ítem se rechaza (RI-6); unirse dos veces no duplica
   (RI-1); un código en Borrador da el mismo `404` que uno inexistente
   (RI-7).
5. **Con certeza:** la respuesta guarda la certeza de 0 a 5 (ADR-028), y
   la regla la usa como dice ADR-031.

## Parte C — I4, el reporte (E-35 a E-37)

1. **Los endpoints E-35 a E-37**, solo para el docente dueño de la
   experiencia (`403` si no). El reporte se **calcula al abrirlo**, no se
   guarda (ADR-022). Ningún texto afirma certeza (RNF-04).
2. **La clasificación** por evidencia (ADR-032) y el **estado general**
   por estudiante (CU-30, ADR-018, ADR-022, ADR-023) también van en
   clases sin base de datos, con una prueba unitaria por cada caso de la
   regla, citando la ADR.
3. **Sin el correo del estudiante** en ninguna respuesta del docente
   (ADR-029, RNF-05). Una prueba lo comprueba.

## Parte D — Pruebas de punta a punta

Con experiencias armadas por el ayudante de prueba (una de cada formato:
`single_choice`, `matching` y `ordering`):
1. El camino del estudiante: unirse, comenzar, responder hasta que
   concluyen todas las evidencias, y el cierre (sin pregunta).
2. Retomar: dejar una pregunta sin responder y recibir la misma (ADR-031).
3. Salir y volver con el código: aparece "No iniciada" (CU-26).
4. Varios estudiantes con respuestas distintas, y el reporte, los
   estudiantes por estado y el historial del docente con los números que
   la regla predice, calculados a mano en la prueba.
5. Los errores: `400`, `403`, `404` y `409` de cada endpoint.

## Parte E — Los documentos

1. `datos_api.py` (y su salida `20-catalogo-endpoints.md`): E-29 a E-37
   pasan a **Hecho**.
2. Si cambias el MR o el diagrama de clases, regenera la cadena de la
   Fase III (`19-entrega-fase-3.md` §3) y deja los verificadores en verde.
3. `pendientes.md` (A16) con su estado real.
4. Si una regla de ADR-031 o ADR-032 resulta ambigua al programarla, **no
   la decidas en silencio**: elige la lectura más fiel al texto, escríbela
   en el pull request con el caso concreto, y déjala con una prueba que
   la muestre.

## Lo que NO debes hacer

- **No construyas I2** (crear experiencia, banco, IA): es el encargo 06.
- **No toques el frontend**, salvo si un cambio del backend rompe sus
  pruebas actuales.
- **No cambies las reglas de las ADR** para que el código sea más fácil.
- **No subas secretos.**

## Cuándo está terminado

1. Los verificadores de `CLAUDE.md`, `_verificar_catalogo.py` y
   `_verificar_censo.py` pasan.
2. Backend: `npm test` y `npm run test:e2e`. Las pruebas del frontend
   (`npm test`, `npm run test:e2e`) siguen en verde.
3. Las pruebas atrapan errores puestos a propósito: cambia a mano el
   tope de 6 de la regla adaptativa, la precedencia del estado general y
   el filtro que oculta `es_correcta` al estudiante; comprueba que alguna
   prueba falla en cada caso, y vuelve a dejarlos bien. Dilo en el pull
   request.

## Cómo entregarlo

Rama **`encargo-07-backend-i3-i4`** y **pull request hacia `main`**, sin
hacer merge. En la descripción, en español simple: qué endpoints
quedaron, con un ejemplo de petición y respuesta de cada uno; cómo
quedaron la regla adaptativa y la clasificación, con sus casos; qué
decidiste por tu cuenta (sobre todo las lecturas de ADR-031 y ADR-032); y
qué no alcanzaste.
