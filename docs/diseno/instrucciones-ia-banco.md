# El texto que se le envía a la IA para generar el banco

**Fecha:** 2026-11-16 (encargo 06). **Archivo:** `backend/src/banco/instrucciones-ia.ts`.

Este documento explica **por qué** el texto dice lo que dice. El texto en sí
está solo en el código, en un archivo, para que se revise como cualquier
otro cambio (ADR-045, punto 4). Si cambias el texto, cambia este documento
en el mismo pull request.

## 1. Cómo se usa

- Se hace **una llamada por evidencia**, con 12 preguntas cada una, hasta 3
  llamadas a la vez (ADR-045, punto 2; RF-03-01, ADR-016).
- Cada llamada tiene dos partes: un mensaje de **sistema** (quién es la IA y
  cómo responde) y un mensaje de **usuario** (qué evidencia, qué formato,
  con qué reglas).
- La IA responde **solo JSON**: `{"items": [ …12 preguntas… ]}`. DeepSeek se
  llama con `response_format: json_object` para obligarlo.
- Lo que responde **no se acepta sin revisar**: cada pregunta pasa la misma
  validación que usa el docente al editar (RI-4, `validar-item.ts`). Si una
  sola falla, esa evidencia se pide una vez más; si vuelve a fallar, no se
  guarda nada (ADR-045, punto 3; ADR-027).

## 2. Qué dice cada parte, y de dónde sale

| Parte del texto | Qué pide | Fuente |
|---|---|---|
| Sistema: «experto en evaluación… de 1.° a 11.° grado» | El tono y el público. | Fase I (población), RNF-02 |
| Sistema: «La evidencia es un texto oficial: no la cambias» | La IA no reescribe al MEN. | CLAUDE.md, ADR-033 |
| Datos: área, grado, DBA, evidencia | El contexto mínimo para que la pregunta mida esa evidencia. | RF-03-01 |
| Escenario: el ejemplo oficial del DBA, «no lo copies» | Preguntas parecidas a la situación que el MEN da de ejemplo, sin repetirla. | ADR-011 |
| Escenario: «el ejemplo trae una figura que tú no recibes» | Que la IA no invente lo que muestra una imagen que no ve. | ADR-044, encargo 05 (`ejemplo_tiene_imagen`) |
| Escenario sin ejemplo: «situaciones cercanas… sin suponer cuál es su familia» | Contexto sin depender de la vida del estudiante. | ADR-044, punto 2 (N6) |
| Regla 1: solo texto; una tabla se escribe, una figura se describe | Sin imágenes ni audio. | ADR-044, punto 1 |
| Regla 2: una sola respuesta correcta, que no depende de opiniones | Que el diagnóstico se pueda corregir solo. | RI-4, ADR-008 |
| Regla 3: mide la evidencia indicada | Cada ítem cuelga de una evidencia. | RF-03-01, H-4 |
| Regla 4: nada de «todas/ninguna de las anteriores», «A y B», «no sé» | Opciones que no dicen nada del error del estudiante. | ADR-045, punto 4 |
| Reglas 5 a 8: lenguaje del grado, nombres inventados, sin repetir, sin la respuesta en el enunciado | Calidad básica de un ítem. | ADR-045, punto 4 (decisión del encargo; ver §4) |
| Selección única: 4 opciones, 1 correcta, `hipotesis_error` en cada distractor, sin rotular | Distractores plausibles con su hipótesis, que nunca se muestra. | ADR-008, ADR-014, ADR-020 |
| Ordenamiento: 3 a 6 elementos, `orden` de 1 a n, escritos desordenados | El orden correcto es lo que se mide. | ADR-014, RI-4 |
| Emparejamiento: 3 a 5 parejas, `grupo` y número de pareja | Dos columnas del mismo tamaño. | ADR-014, RI-4, H-9 |

## 3. Lo que el backend comprueba después

Además de RI-4 (lo mismo que al editar), solo para lo generado:

- en selección única, cada distractor trae su `hipotesis_error` (ADR-020);
- ninguna opción es «todas las anteriores» ni «ninguna de las anteriores»;
- vienen exactamente 12 preguntas.

**No** se comprueba automáticamente que una pregunta sea «solo texto» ni que
mida bien la evidencia: eso lo garantiza el texto y lo revisa el docente
antes de publicar (CU-17, CU-18). Es un límite declarado.

## 4. Decisiones de este encargo (por confirmar)

- **4 opciones** en selección única, **3 a 6** elementos en ordenamiento y
  **3 a 5** parejas en emparejamiento. RI-4 solo pone el mínimo (2, 2 y 4);
  estos números son una elección para que los ítems se parezcan a una prueba
  escolar común. Si el equipo prefiere otros, se cambian en `FORMA`.
- Las reglas 5 a 8 no vienen de una ADR: son prácticas comunes al escribir
  ítems. Están para que el equipo las discuta.
- El texto se escribió **sin probarlo con DeepSeek** (en la nube no hay
  clave). La primera prueba es la de Alejandro en local; si DeepSeek se
  equivoca seguido en algo, se ajusta aquí.

## 5. Cómo probarlo en local

1. En `backend/.env`: `IA_SERVICIO=deepseek`, `DEEPSEEK_API_KEY=` (la clave),
   y si se quiere, `DEEPSEEK_MODEL` e `IA_TIEMPO_LIMITE_MS`.
2. Crear una experiencia desde Insomnia (`POST /experiencias`) y consultar
   `GET /experiencias/generaciones/:id` hasta que diga `lista` o `fallida`.
3. La consola del backend muestra, por evidencia, cuánto tardó y en qué
   intento salió, y el total: con eso se mide RNF-13. Nunca muestra la
   clave ni datos del docente.
