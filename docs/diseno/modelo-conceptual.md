# Modelo conceptual — AdaptiveLearn (rediseño)

**Estado:** confirmado — 2026-08-06; **actualizado 2026-10-21** (barrido
de coherencia antes de Fase III).

> El glosario dice qué es cada cosa. Este documento dice cuántos de uno le
> corresponden a cuántos de otro — la forma de los datos, en lenguaje simple,
> antes de que se vuelva una tabla de base de datos.
>
> **Qué manda.** La fuente de verdad es la Fase I, la Fase II y
> `decisiones.md`. Este documento las resume en forma de datos, en
> lenguaje simple. El MER que existe hoy
> (`fase-3-diseno-computacional/01-modelo-entidad-relacion.md`, Quinta
> revisión) es un **borrador anterior al cierre de la Fase II**: si dice
> algo distinto de este documento, la diferencia se revisa contra las
> decisiones, no se resuelve a favor del MER. *(Corrección 2026-10-21:
> una primera versión de esta nota, escrita ese mismo día, decía "manda
> el MER". Alejandro aclaró que la Fase III se rehace en orden y que el
> MER actual no puede tomarse como base.)*

*(Por qué se actualizó: la versión del 2026-08-06 no tenía Docente,
Estudiante, Inscripción ni Respuesta —se escribió antes de diseñar las
pantallas que los necesitan— y decía que el banco de preguntas era de la
Evidencia, cuando es de la Evidencia **dentro de una experiencia**.)*

## Quién hace qué

| Objeto A | Relación | Objeto B | Cardinalidad / nota |
|---|---|---|---|
| Docente | crea | Experiencia | 1 a N — cada experiencia tiene exactamente 1 docente |
| Estudiante | se inscribe en | Experiencia | N a N, a través de una **Inscripción** — con el código de invitación, y solo si la experiencia está Publicada |
| Persona registrada | es | Docente **o** Estudiante | exactamente uno, fijo para siempre (`20-spec`). Son dos tipos de usuario separados, no uno con una casilla de rol. *(No existe una entidad "Cuenta" común: se evaluó y no se adoptó, V-8 del MER.)* |

## El currículo (dato del MEN, no nuestro)

| Objeto A | Relación | Objeto B | Cardinalidad / nota |
|---|---|---|---|
| DBA | tiene | Evidencia | 1 a N. El rango "1 a 6, promedio 3.7" de la versión anterior **no es confiable**: el "1" resultó ser un error de extracción (QA-013); se re-verifica al auditar los datos curriculares |
| Evidencia | tiene | Dictamen | exactamente 1 — nuestro juicio de si admite formato cerrado (no viene del MEN). Pendiente del censo QA-014 |
| DBA | necesita | Experiencia | N — un DBA es de tamaño-año, no de tamaño-experiencia |

## La experiencia y su banco

| Objeto A | Relación | Objeto B | Cardinalidad / nota |
|---|---|---|---|
| Experiencia | se ancla a | DBA | exactamente 1 |
| Experiencia | tiene | estado | Borrador o Publicada (2 valores; ADR-027). Al publicar, el banco se congela (ADR-026). No hay "despublicar" |
| Experiencia | incluye | Evidencia | todas las del DBA que admiten formato cerrado, sin selección del docente en esta versión (QA-010, QA-012, QA-014) |
| Evidencia *dentro de una experiencia* | tiene | Banco de ítems | 12 generados por la IA al crear la experiencia (ADR-005, ADR-016), más los que el docente agregue (ADR-026). **El banco no se comparte entre experiencias**, aunque usen el mismo DBA |
| Banco de una evidencia | necesita, para publicar | Ítems activos | **mínimo 6** no descartados (ADR-026) |
| Ítem | tiene | Opción | 2 o más; 4 o más en emparejamiento (RI-4) |
| Ítem | tiene | origen | generado por IA, editado por el docente, o creado por el docente (ADR-026) |

## Lo que pasa cuando el estudiante responde

| Objeto A | Relación | Objeto B | Cardinalidad / nota |
|---|---|---|---|
| Inscripción | se le muestra | Ítem | por cada evidencia, **mínimo 4, tope 6**, según la regla adaptativa por certeza (ADR-016). Cada vez que se muestra un ítem queda una **Presentación**, con su orden |
| Presentación | tiene | Respuesta | 0 o 1 — cero significa "se le mostró y no respondió" |
| Respuesta | lleva | Certeza | exactamente 1, de 0 a 5 (CRI, ADR-008) |
| Respuesta | elige | Opción | 1 en selección única; varias en emparejamiento y ordenamiento (con el par o la posición que dio) |
| Inscripción | obtiene, por cada evidencia | Resultado | 0 o 1: Muestra / No muestra / No concluyente — guardado como fotografía del momento en que se concluyó (ADR-021) |
| Inscripción | tiene | Estado general por DBA | 1, **calculado, no guardado**: Muestra / No muestra / No concluyente / Sin concluir (ADR-018, ADR-022) |
| Experiencia | tiene | Reporte | 1, **calculado, no guardado** — agrega los resultados del grupo |

## Lo que esta versión no tiene

| Objeto | Por qué |
|---|---|
| Práctica, Verificación | Diferidas a v2 (ADR-007) |
| Unidad | Fuera de alcance — no está definida |
| Acudiente y su autorización | No se modela; por eso esta versión no se usa con estudiantes reales (ADR-029) |

## Nota sobre Reporte y Unidad

En esta versión las experiencias son independientes entre sí — no existe
Unidad para conectarlas. Por eso el Reporte de esta versión agrega evidencia
de **una sola experiencia**, no de varias. Si en el futuro Unidad existe, un
"reporte de unidad" sería un objeto distinto, que agregaría varias
experiencias — no una extensión del Reporte actual.
