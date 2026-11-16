# Encargo 06 — Backend de I2: crear la experiencia y generar su banco

**Para:** una sesión de Claude Code sobre este repositorio.
**Escrito:** 2026-11-16, desde la sesión local de Alejandro.
**Es el backend del incremento I2**
(`docs/modesec/fase-4-produccion/01-seleccion-herramienta-desarrollo.md`):
el docente crea una experiencia sobre un DBA, el sistema genera su banco
de preguntas con DeepSeek, el docente lo revisa y lo publica, y obtiene
el código de invitación.

**Solo backend.** El docente del curso pide todo el backend antes de que
termine noviembre de 2026; el frontend de I2 a I4 va después, en otro
encargo. **Corre en paralelo con el encargo 07** (backend de I3 e I4) en
otra sesión: no toques los módulos de inscripciones, diagnóstico ni
reporte, y si los dos necesitan el mismo archivo (`app.module.ts`,
`datos_api.py`, `pendientes.md`), cambia solo tus partes.

**Antes de empezar, lee:**
1. `CLAUDE.md` y `docs/diseno/pendientes.md` (A12, A15, A16).
2. Las decisiones que mandan aquí, en `docs/diseno/decisiones.md`:
   **ADR-045** (cómo se genera el banco: es la guía de este encargo),
   ADR-043 (solo DeepSeek), ADR-044 (solo texto), ADR-042 (el censo),
   ADR-027 (todo o nada), ADR-026 (revisar antes de publicar; publicar no
   se deshace), ADR-035, ADR-030, ADR-006, ADR-011, ADR-014, ADR-020.
3. El catálogo de endpoints `docs/modesec/fase-3-diseno-computacional/20-catalogo-endpoints.md`
   §4.2 y §4.3 (E-18 a E-28) y sus casos de uso en `12-casos-de-uso.md`
   (CU-10 a CU-20). El modelo: `17-modelo-relacional.md` y
   `18-diccionario-datos.md` (tablas `experiencia`, `experiencia_evidencia`,
   `item`, `opcion`; reglas RI-3, RI-4, RI-5, RI-14, RI-17, RI-18, RI-19).
4. Lo que las pantallas necesitan del backend, en las especificaciones
   de `docs/modesec/fase-2-diseno-multimedial/`: `07` (004 Paso 3, y su
   mensaje de error), `12` (009 Banco), `15` (012 Publicar), `16` (013
   Código) y `24` (024 Cargando). Solo para saber qué datos piden.
5. Cómo se trabajó antes: `docs/encargos/03-backend-hasta-catalogo.md`.

## Parte A — La base (ya hecha)

`backend/sql/001_esquema.sql` ya tiene **todas** las tablas del modelo
relacional (2026-11-16, `modelo-relacional/generar.py`). No hay que
cambiar el esquema: si lo necesitas, el cambio va al MR y se regenera.

## Parte B — El backend

1. **Los endpoints E-18 a E-28**, como los describe el catálogo, con
   los cambios de ADR-043 y ADR-045:
   - `POST /experiencias` responde **202** con el identificador de la
     generación; **`GET /experiencias/generaciones/:id`** (nuevo) dice
     `generando`, `lista` (con el id de la experiencia) o `fallida`.
     Solo lo puede consultar el docente que la pidió.
   - Solo entran las evidencias cuyo dictamen aplica (RI-5), cada una con
     el formato de su dictamen (RI-19). Un DBA sin evidencias aplicables
     responde `409` con un mensaje claro.
   - El código de invitación se crea al guardar la experiencia (RI-3).
2. **El servicio de IA**, detrás de una interfaz (ADR-043 punto 3), con
   dos implementaciones: `DeepSeekServicio` (API compatible con OpenAI,
   `https://api.deepseek.com`, modelo de `DEEPSEEK_MODEL`, respuesta en
   JSON) y `IaFalsa` para las pruebas. Cuál se usa lo decide una
   variable de entorno (`IA_SERVICIO=deepseek|falsa`); las pruebas
   siempre usan la falsa. **La clave nunca se escribe en un log ni en una
   respuesta**, ni siquiera en un error.
   Agrega las variables a `.env.example`, sin valores reales. Sin
   `IA_SERVICIO` se usa DeepSeek; el arranque de las pruebas del frontend
   (`frontend/e2e/arrancar-backend.mjs`) pone `IA_SERVICIO=falsa`.
3. **El texto que se envía a la IA** (ADR-045 punto 4) va en un solo
   archivo, por ejemplo `backend/src/banco/instrucciones-ia.ts`, en
   español, con:
   - el área, el grado, el enunciado del DBA, la evidencia exacta y su
     formato;
   - el ejemplo del DBA como escenario (ADR-011). Si
     `ejemplo_tiene_imagen`, decirle a la IA que el ejemplo tenía una
     figura que no recibe y que no se refiera a ella. Si no hay ejemplo,
     que proponga un escenario cercano a la vida de un estudiante
     colombiano de ese grado;
   - las reglas: **solo texto** (ADR-044: ninguna pregunta puede pedir
     mirar una imagen, un mapa o una gráfica; una tabla escrita sí);
     una sola respuesta correcta; distractores plausibles, cada uno con
     su hipótesis de error (ADR-020), sin rotularlos; nada de "todas las
     anteriores" ni "ninguna de las anteriores"; lenguaje para la edad del
     grado; sin nombres de personas reales;
   - la forma exacta del JSON que debe devolver, por formato (opciones,
     `es_correcta` en `single_choice`, `orden` en `ordering`, `grupo` y
     `orden` como número de pareja en `matching`; `18-diccionario-datos.md`).
   Escribe en `docs/diseno/` un documento corto que explique ese texto y
   por qué dice lo que dice: es lo que el equipo revisará.
4. **La validación** de cada ítem generado (RI-4 y los mínimos de H-9) es
   la misma que usan editar y agregar (CU-18, CU-20): una sola función.
5. **Los tiempos:** límite por llamada configurable
   (`IA_TIEMPO_LIMITE_MS`, por defecto 120000) y, por cada generación,
   registrar en la consola cuánto tardó cada evidencia y el total, sin
   datos del docente. Con eso se mide RNF-13 en la revisión local.
6. **Pruebas:** unitarias de la validación (cada regla de RI-4, con su
   caso inválido) y del armado del texto; de punta a punta, con `IaFalsa`:
   crear (202 → `lista`), todo o nada (una evidencia inválida dos veces
   → `fallida` y la base sin la experiencia), el reintento (inválida una
   vez → `lista`), editar, descartar, reincluir, agregar, publicar (con
   menos de 6 activos → `409`), código (en Borrador → `409`), eliminar
   en cascada, y que otro docente recibe `403`.

## Parte C — Los documentos

1. `datos_api.py` (y su salida `20-catalogo-endpoints.md`): E-18 a E-28
   pasan a **Hecho**; E-19 dice lo de ADR-043 y ADR-045 (sin respaldo,
   202, reintento), y aparece el endpoint de la generación.
2. `requerimientos.py`: RF-03-02 dice que el respaldo está suspendido por
   ADR-043, y RNF-13 queda pendiente de la medición local.
3. Si cambias el MR o el diagrama de clases, regenera la cadena de la
   Fase III (`19-entrega-fase-3.md` §3) y deja los verificadores en verde.
4. `pendientes.md` (A16) con su estado real. V-12 (ADR-045 punto 6) es
   de la pantalla: queda para el encargo del frontend.

## Lo que NO debes hacer

- **No llames a DeepSeek** ni a ningún otro servicio de IA: aquí no hay
  clave y las pruebas usan `IaFalsa`. La prueba real la hace Alejandro en
  local, al revisar.
- **No construyas I3 ni I4** (unirse con código, tomar el diagnóstico,
  reporte): son el encargo 07, en paralelo.
- **No toques el frontend**, salvo si un cambio del backend rompe sus
  pruebas actuales.
- **No cambies el censo ni el catálogo** ni el texto del MEN.
- **No subas secretos** ni escribas valores de ejemplo que parezcan una
  clave real en `.env.example`.

## Cuándo está terminado

1. Los verificadores de `CLAUDE.md`, `_verificar_catalogo.py` y
   `_verificar_censo.py` pasan.
2. Backend: `npm test` y `npm run test:e2e`. Las pruebas del frontend
   (`npm test`, `npm run test:e2e`) siguen en verde.
3. Las pruebas atrapan errores puestos a propósito: rompe a mano una
   regla de RI-4 en la validación y el todo o nada en la transacción,
   comprueba que alguna prueba falla, y vuelve a dejarlos bien. Dilo en
   el pull request.

## Cómo entregarlo

Rama **`encargo-06-backend-i2`** y **pull request hacia
`main`**, sin hacer merge. En la descripción, en español simple: qué
endpoints quedaron, con un ejemplo de petición y respuesta de cada uno; cómo es el texto que se envía a la IA,
copiado entero; qué decidiste por tu cuenta; qué quedó para la prueba local con DeepSeek; y
qué no alcanzaste.
