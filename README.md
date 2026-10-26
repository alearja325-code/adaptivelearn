# AdaptiveLearn

Diagnóstico por **evidencias de aprendizaje**, anclado a los Derechos
Básicos de Aprendizaje (DBA) del Ministerio de Educación Nacional de
Colombia.

Un docente de secundaria crea una experiencia anclada a un DBA; el
sistema genera con IA un banco de preguntas sobre las evidencias de ese
DBA; el docente lo revisa, lo completa y lo publica; sus estudiantes
responden declarando qué tan seguros están de cada respuesta; y el
docente recibe —por evidencia y por estudiante— uno de tres estados:
*muestra*, *no muestra* o *no concluyente*.

Nunca una nota. Nunca un puntaje. Nunca un texto sobre un estudiante
redactado por IA.

---

## Estado del proyecto

| Parte | Estado |
|---|---|
| Diseño educativo (MODESEC, Fase I) | Completo — 8 documentos |
| Diseño multimedial (Fase II) | Completo — 27 ventanas en 24 especificaciones, mapa de navegación, guión técnico, índice de recursos |
| Diseño computacional (Fase III) | Completo, en el orden de MODESEC: proceso de desarrollo (`10`), requerimientos (`11`), casos de uso, clases, objetos y secuencias (`12` a `15`), MER, MR y diccionario de datos (`16` a `18`), y como anexo el catálogo de endpoints (`20`). Índice y cómo se comprueba: `19-entrega-fase-3.md`. El borrador anterior al cierre de la Fase II se conserva como insumo |
| Backend | Iniciado (NestJS + MySQL): solo el acceso (I1). Lo que falta, endpoint por endpoint y por incremento: `20-catalogo-endpoints.md` |
| Frontend | Sin empezar; su diseño está completo en la Fase II |
| Datos del currículo del MEN | Disponibles, **pendientes de auditoría** |

## Cómo está organizado

```
docs/                        Toda la documentación
  diseno/                    El cerebro del proyecto: 32 decisiones (ADR),
                             visión, glosario, preguntas abiertas y
                             pendientes.md (qué falta y qué recibe el MER)
  modesec/                   La metodología, fase por fase
    fase-1-diseño-educativo/
    fase-2-diseno-multimedial/
    fase-3-diseno-computacional/
  cursos/
    dse-1-203447/            Diseño y Desarrollo de Software Educativo I
    dse-2-203453/            Diseño y Desarrollo de Software Educativo II
data/
  curriculo-men/             PDF oficiales de los DBA y su versión normalizada
backend/                     API en NestJS
frontend/                    Todavía vacío
EQUIPO.md                    Integrantes y reparto de responsabilidades
```

**Para empezar a leer:** `docs/diseno/vision.md` (qué es y por qué),
`docs/diseno/glosario.md` (qué significa cada término) y
`docs/diseno/decisiones.md` (por qué es como es).

## Cómo se trabaja aquí

**1. Cada afirmación señala de dónde sale.** Ninguna pantalla, requisito
o decisión existe "porque sí": cada una cita la decisión, la
especificación o el documento oficial del MEN del que proviene. Cuando
algo no tiene fundamento, se declara como vacío en vez de rellenarse.

**2. Lo que se afirma, se comprueba con código.** Hay verificadores que
fallan si un documento contradice a otro:

```bash
# Los documentos de diseño no se contradicen, y la cadena Fase I → Fase II se sostiene
cd docs/diseno && python3 verificar_consistencia.py && python3 verificar_cadena.py

# Cada pantalla usa solo colores y medidas del sistema de diseño
cd docs/modesec/fase-2-diseno-multimedial && python3 verificar_tokens.py [0-9][0-9]-spec*.md

# Ninguna pantalla queda fuera del mapa de navegación
cd docs/modesec/fase-2-diseno-multimedial/navegacion && python3 mapa_navegacion.py

# Ninguna pantalla queda sin requerimientos; toda decisión citada existe
cd docs/modesec/fase-3-diseno-computacional/requerimientos && python3 requerimientos.py
```

Los dos últimos, además, **generan** sus documentos (`28`, `29` y
`11`): el mapa, el guión y los requerimientos no se editan a mano, para
que no puedan contradecir a su fuente.

Del resto de la Fase III (`12` a `18` y `20`), todo lo que es tabla o
diagrama también se genera, y estos verificadores comprueban que el MER,
el modelo relacional, el UML, los endpoints y el backend no se aparten:

```bash
cd docs/modesec/fase-3-diseno-computacional
cd mer && python3 _verificar_mer.py && python3 _verificar_vistas.py && python3 _verificar_mapa.py && cd ..
cd modelo-relacional && python3 _verificar_mr_mer.py && python3 verificar_mr.py && cd ..
cd uml && python3 _verificar_uml.py && cd ..
cd api && python3 _verificar_api.py && cd ..
```

La cadena completa —regenerar cada documento y sus PDF, y probar el
esquema contra MySQL— está en `19-entrega-fase-3.md`, sección 3.

Requisito: Python 3 con `lxml` (`pip install lxml`), y Graphviz para
regenerar el mapa de navegación.

## Historia

Este es el **rediseño (V3)**. Las versiones anteriores tenían backend y
frontend construidos y no se continúan: su motor de diagnóstico estaba
acoplado a un modelo pedagógico que el proyecto retiró. De ellas solo se
conservan los datos del currículo del MEN (`data/curriculo-men/`). El
detalle está en `docs/diseno/vision.md`.

## Datos y licencia

Los Derechos Básicos de Aprendizaje son documentos públicos del
Ministerio de Educación Nacional de Colombia y se usan como referencia
curricular, sin modificarlos.

Este repositorio **no contiene datos de estudiantes reales**. La versión
actual no puede usarse con menores de edad hasta registrar la
autorización de su representante legal, que exige el artículo 7 de la
Ley 1581 de 2012 (`docs/diseno/decisiones.md`, ADR-029).
