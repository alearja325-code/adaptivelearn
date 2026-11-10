# Encargo 05 — El ejemplo de cada DBA y el censo de formato cerrado

**Para:** una sesión de Claude Code sobre este repositorio.
**Escrito:** 2026-11-10, desde la sesión local de Alejandro.
**Es el prerrequisito de datos del incremento I2** (crear la experiencia
y generar su banco): la generación usa el ejemplo de cada DBA como
contexto (ADR-011) y el formato de cada evidencia (RF-03-01).

**Antes de empezar, lee:**
1. `CLAUDE.md` y `docs/diseno/pendientes.md` (A12, A16).
2. `docs/encargos/02-catalogo-curricular-corregido.md` y
   `data/curriculo-men/catalogo/informe-correccion.md`: cómo se armó y
   verificó el catálogo. **La Parte A sigue exactamente el mismo método.**
3. `docs/diseno/criterios-censo-formato-cerrado.md` (**aceptados**),
   ADR-042, ADR-006, ADR-011, y QA-011, QA-012, QA-014 y QA-017 en
   `docs/diseno/preguntas-abiertas.md`.
4. `docs/modesec/fase-2-diseno-multimedial/06-spec-crear-experiencia-paso2.md`
   §2.4: cómo se muestran el ejemplo y la evidencia que no aplica.

## Parte A — El ejemplo de cada DBA (QA-011)

Cada DBA de los PDF tiene, además del enunciado y las evidencias, un
**"Ejemplo"**. Hoy `catalogo_dba.json` no lo trae y en la base es `NULL`
en los 343.

1. **Extráelo de los PDF** ampliando `construir_catalogo.py`, con las
   mismas reglas del encargo 02: **el texto del MEN se copia exacto**
   (solo se normalizan espacios y saltos de línea), cada ejemplo con su
   página, y lo que no se pueda determinar con certeza se marca
   **dudoso**. No edites el JSON a mano: se regenera.
2. **Ejemplos con imagen.** Algunos ejemplos son o incluyen una figura
   (ADR-011: entre 2 y 8 por área). Marca cada DBA con
   `ejemplo_tiene_imagen` (verdadero o falso), revisando la página
   renderizada, no solo la capa de texto. El texto que acompañe a la
   imagen se copia igual; el texto que está **dentro** de la imagen no.
   El Paso 2 muestra para esos casos *"Este ejemplo incluye una imagen que
   no se muestra en esta versión."* (`06-spec` §2.4).
3. **El modelo necesita esa marca:** agrega `ejemplo_tiene_imagen` a DBA
   en la fuente del MER y del MR (con su razón: `06-spec` §2.4 la pide y
   no había dónde guardarla), regenerando la cadena de la Fase III
   (`19-entrega-fase-3.md` §3).
4. **El verificador** (`_verificar_catalogo.py`) comprueba también que
   cada ejemplo aparece literalmente en su página, y sigue atrapando los
   errores puestos a propósito (agrega uno sobre un ejemplo).

## Parte B — El censo de formato cerrado (QA-014)

Aplica **`criterios-censo-formato-cerrado.md`** a las **1282 evidencias**.

1. **Es juicio, no una búsqueda de palabras.** Puedes usar un script
   para ordenar el trabajo o proponer un primer dictamen por los verbos,
   pero **cada evidencia la lees tú y decides tú**, con su justificación
   (una o dos frases que citan el verbo o la frase decisiva y la regla:
   N1 a N5, o el formato y su señal). Hazlo por lotes, área por área.
   **No uses una API de IA externa** (ni DeepSeek): el censo lo hace esta
   sesión.
2. Si una evidencia no cabe claramente en las reglas, dictamínala igual
   y márcala `dudoso` con la razón. **No cambies los criterios por tu
   cuenta:** si un patrón de casos no está cubierto, anótalo en el
   informe como propuesta de ajuste.
3. **Produce, en `data/curriculo-men/censo/`:**
   - `censo_formato_cerrado.json`: por evidencia (`codigo_dba`,
     `numero_evidencia`), `aplica`, `formato`, `regla`, `justificacion` y
     `dudoso`; y en su cabecera, `estado: "propuesto-por-ia"`, la fecha,
     y la versión de los criterios que aplicaste.
   - `informe-censo.md`, en español simple: cuántas aplican por área y por
     grado, con qué formato, cuántas por cada regla N1 a N5, y cuántas
     quedaron dudosas. **Responde la pregunta de fondo de QA-014:** si en
     alguna área la proporción es baja, dilo claro. **Lista los DBA que
     quedaron sin ninguna evidencia que aplique** (QA-012: esos DBA no se
     pueden usar para crear una experiencia en esta versión).
   - `muestra_validacion.md`: 40 evidencias al azar, 10 por área, con una
     semilla fija escrita en el archivo, más todas las dudosas. Por cada
     una: el texto, tu dictamen y su justificación, y dos casillas en
     blanco para los dos validadores (sección 5 de los criterios).
   - `_verificar_censo.py`: comprueba que hay exactamente un dictamen por
     cada evidencia del catálogo, que `formato` es nulo si y solo si no
     aplica (RI-19), que toda justificación cita una regla, y que la
     muestra se puede volver a sacar igual con su semilla.
4. Las 20 evidencias de la sección 7 de los criterios ya están
   clasificadas a mano. Si tu dictamen difiere en alguna, explica por qué
   en el informe; no copies el de la tabla sin leerla.

## Parte C — Cargarlo en el sistema

1. `backend/scripts/preparar-base.mjs` carga el ejemplo, la marca de
   imagen y el censo en `evidencia_dictamen`, con `fecha_dictamen`. El
   texto de `justificacion` es el del censo.
2. `GET /catalogo/dbas/:codigo` ya devuelve `ejemplo` y, por evidencia,
   `admiteFormatoCerrado` y `formato`: comprueba que ahora llegan con
   datos, y agrega `ejemplo_tiene_imagen` a la respuesta.
3. **El Paso 2 del frontend** ya sabe mostrar el ejemplo, la evidencia
   tachada y el aviso de imagen (`06-spec` §2.4): comprueba que se ve con
   los datos reales. Hay pruebas que hoy esperan "ninguna tachada" y "sin
   ejemplo" porque no había datos (`frontend/e2e/1-camino-completo.spec.ts`
   y `frontend/src/ventanas/avisos.test.tsx`): cámbialas para que
   comprueben el comportamiento real con un DBA que tenga evidencias que
   no aplican y uno con ejemplo con imagen, si existe.

## Lo que NO debes hacer

- **No cambies el texto del MEN** ni edites a mano `catalogo_dba.json`
  ni el censo: se regeneran desde sus scripts.
- **No cambies los criterios del censo.** Propón ajustes en el informe.
- **No construyas I2** (crear experiencia, banco, IA): es el encargo 06.
- **No subas secretos.**

## Cuándo está terminado

1. `_verificar_catalogo.py` y `_verificar_censo.py` pasan, y los dos
   atrapan sus errores puestos a propósito.
2. Los verificadores de `CLAUDE.md`, las pruebas del backend
   (`npm test`, `npm run test:e2e`) y las del frontend (`npm test`,
   `npm run test:e2e`, `npm run verificar:estilos`) pasan.
3. `pendientes.md` (A12) y `preguntas-abiertas.md` (QA-011 y QA-014)
   dicen su estado real.

## Cómo entregarlo

Rama **`encargo-05-ejemplos-y-censo`** y **pull request hacia `main`**,
sin hacer merge. En la descripción, en español simple: cuántos ejemplos
se extrajeron, cuántos tienen imagen y cuántos quedaron dudosos; **las
cifras del censo por área**; los DBA que quedaron sin evidencias
aplicables; qué decidiste por tu cuenta; y las propuestas de ajuste a los
criterios, si las hay.
