# Currículo del MEN

Los documentos oficiales del Ministerio de Educación Nacional de
Colombia sobre los que se construye el catálogo curricular de la
aplicación (subsistema SUB-06): los Derechos Básicos de Aprendizaje
(DBA), sus evidencias y sus ejemplos.

| Carpeta | Qué contiene |
|---|---|
| `pdfs/` | Los PDF oficiales: DBA de Matemáticas (V.2), Lenguaje (V.2), Ciencias Naturales (V.1) y Ciencias Sociales (**V.1**: el archivo se llama `…_v2.pdf`, igual que el que publica el MEN, pero su contenido es la versión 1 — ADR-033), más Estándares Básicos de Competencias y Lineamientos Curriculares, que se usan como referencia |
| `raw_text/`, `text/` | Texto extraído de esos PDF |
| `normalized/` | `curriculo_men_normalizado.json`: el currículo estructurado que usa el diseño |
| `metadata/` | Registro de cada fuente y su auditoría |
| `catalogo/` | **El catálogo de DBA corregido y verificado contra los PDF** (encargo 02, 2026-10-27): `catalogo_dba.json`, el script que lo arma, su verificador y el informe de lo que se corrigió. Es la fuente para cargar el catálogo; el JSON de `normalized/` queda como registro de lo que había |
| `herramientas-v2/` | Los scripts que construyeron y auditaron estos datos en la versión anterior. **Solo como registro de cómo se generaron**: dependen de módulos de la V2 que no están aquí y no se ejecutan solos |

## Estado: pendiente de auditoría

> **Actualización 2026-10-27.** Los DBA y sus evidencias ya tienen una
> versión verificada contra los PDF: `catalogo/catalogo_dba.json` (343 DBA;
> ver `catalogo/informe-correccion.md`). Lo que sigue sin auditar es el
> resto: los ejemplos de cada DBA, los Estándares y los Lineamientos.

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

**Ya se sabe un error:** el JSON registra Ciencias Sociales como "V.2"; es V.1 (ADR-033).

Hasta esa auditoría, `curriculo_men_normalizado.json` no es una fuente
confiable para cifras como "cuántas evidencias tiene un DBA".

Los DBA son documentos públicos del MEN; se usan como referencia
curricular, sin modificarlos.
