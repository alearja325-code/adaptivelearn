# Currículo del MEN

Los documentos oficiales del Ministerio de Educación Nacional de
Colombia sobre los que se construye el catálogo curricular de la
aplicación (subsistema SUB-06): los Derechos Básicos de Aprendizaje
(DBA), sus evidencias y sus ejemplos.

| Carpeta | Qué contiene |
|---|---|
| `pdfs/` | Los PDF oficiales: DBA de Matemáticas (v2), Lenguaje (v2), Ciencias Naturales (v1) y Ciencias Sociales (v2), más Estándares Básicos de Competencias y Lineamientos Curriculares, que se usan como referencia |
| `raw_text/`, `text/` | Texto extraído de esos PDF |
| `normalized/` | `curriculo_men_normalizado.json`: el currículo estructurado que usa el diseño |
| `metadata/` | Registro de cada fuente y su auditoría |
| `herramientas-v2/` | Los scripts que construyeron y auditaron estos datos en la versión anterior. **Solo como registro de cómo se generaron**: dependen de módulos de la V2 que no están aquí y no se ejecutan solos |

## Estado: pendiente de auditoría

Estos datos vienen de la versión anterior (V2) y **todavía no se han
auditado** contra los PDF. Hay errores de extracción conocidos (QA-013:
evidencias fusionadas o cortadas) y está pendiente una revisión
exhaustiva (`docs/diseno/pendientes.md`, sección A12):

- que se haya normalizado **todo** el contenido de todas las áreas que
  ofrece la aplicación;
- que el texto sea **copia exacta** del oficial, sin cambios ni
  agregados;
- qué hacer cuando un elemento del DBA (sobre todo el ejemplo) es una
  imagen y no texto.

Hasta esa auditoría, `curriculo_men_normalizado.json` no es una fuente
confiable para cifras como "cuántas evidencias tiene un DBA".

Los DBA son documentos públicos del MEN; se usan como referencia
curricular, sin modificarlos.
