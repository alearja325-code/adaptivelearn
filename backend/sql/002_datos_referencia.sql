-- Datos de referencia del catálogo curricular — AdaptiveLearn
-- Escrito a mano (encargo 03) con los valores de las decisiones del equipo;
-- cada valor dice de dónde sale. Correr después de 001_esquema.sql.
-- Los DBA y sus evidencias NO van aquí: los carga scripts/preparar-base.mjs
-- desde data/curriculo-men/catalogo/catalogo_dba.json (encargo 02).
SET NAMES utf8mb4;

-- Las 4 áreas de ADR-033, con los códigos de ADR-036 (punto 1).
INSERT INTO area (codigo_area, nombre) VALUES
  ('MAT', 'Matemáticas'),
  ('LEN', 'Lenguaje'),
  ('CN',  'Ciencias Naturales'),
  ('CS',  'Ciencias Sociales');

-- Grados 1 a 11 (ADR-036, punto 2), sin Transición (ADR-033), con el nivel
-- de la educación formal que fija la Ley 115 de 1994: básica primaria (1° a
-- 5°), básica secundaria (6° a 9°) y media (10° y 11°).
INSERT INTO grado (numero, nombre, nivel) VALUES
  (1,  'Primero',  'basica_primaria'),
  (2,  'Segundo',  'basica_primaria'),
  (3,  'Tercero',  'basica_primaria'),
  (4,  'Cuarto',   'basica_primaria'),
  (5,  'Quinto',   'basica_primaria'),
  (6,  'Sexto',    'basica_secundaria'),
  (7,  'Séptimo',  'basica_secundaria'),
  (8,  'Octavo',   'basica_secundaria'),
  (9,  'Noveno',   'basica_secundaria'),
  (10, 'Décimo',   'media'),
  (11, 'Undécimo', 'media');

-- Un documento oficial por área (ADR-036, punto 3), con la versión, el año,
-- las páginas y la dirección que ADR-033 verificó el 2026-10-24 contra los
-- archivos que publica el MEN en Colombia Aprende. La versión se lee del
-- documento, no del nombre del archivo: Ciencias Sociales es V.1 aunque su
-- archivo se llame "...-v2_0.pdf" (ADR-033).
-- El título es una decisión del encargo 03, declarada: "Derechos Básicos de
-- Aprendizaje" y el área, como en la portada del PDF (la de Matemáticas dice
-- "Derechos Básicos de Aprendizaje · V.2 · Matemáticas"); la versión va en su
-- propia columna. La dirección completa une el prefijo del
-- sitio (https://www.colombiaaprende.edu.co/sites/default/) con la ruta de
-- la tabla de ADR-033.
INSERT INTO documento_oficial (id_documento, codigo_area, titulo, version, anio, paginas, url_oficial) VALUES
  (1, 'MAT', 'Derechos Básicos de Aprendizaje — Matemáticas', 'V.2', 2016, 88,
   'https://www.colombiaaprende.edu.co/sites/default/files/files_public/2026-06/dba_matematicas-min.pdf'),
  (2, 'LEN', 'Derechos Básicos de Aprendizaje — Lenguaje', 'V.2', 2016, 56,
   'https://www.colombiaaprende.edu.co/sites/default/files/files_public/2026-05/dba_lenguaje-min.pdf'),
  (3, 'CN',  'Derechos Básicos de Aprendizaje — Ciencias Naturales', 'V.1', 2016, 44,
   'https://www.colombiaaprende.edu.co/sites/default/files/files_public/2026-05/dba_c.naturales-min.pdf'),
  (4, 'CS',  'Derechos Básicos de Aprendizaje — Ciencias Sociales', 'V.1', 2016, 52,
   'https://www.colombiaaprende.edu.co/sites/default/files/files_public/2026-05/dba_c.sociales-v2_0.pdf');

-- evidencia_dictamen queda vacía: el censo QA-014 está pendiente (V-6).
