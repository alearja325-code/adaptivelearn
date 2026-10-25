-- Esquema ejecutable — AdaptiveLearn
-- GENERADO por modelo-relacional/generar.py — no editar a mano.
-- Dialecto: SQLite, solo para la verificacion mecanica.
-- Los tipos de produccion (MariaDB) estan en 06-diccionario-datos.md
PRAGMA foreign_keys = ON;

CREATE TABLE docente (
  id_docente INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  nombre TEXT NOT NULL,
  correo TEXT NOT NULL UNIQUE,
  avatar_url TEXT,
  UNIQUE (correo)
);

CREATE TABLE estudiante (
  id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  nombre TEXT NOT NULL,
  correo TEXT NOT NULL UNIQUE,
  avatar_url TEXT,
  UNIQUE (correo)
);

CREATE TABLE experiencia (
  id_experiencia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  id_docente INTEGER NOT NULL,
  codigo_dba TEXT NOT NULL,
  nombre TEXT NOT NULL,
  estado TEXT NOT NULL DEFAULT 'Borrador',
  fecha_creacion TEXT NOT NULL,
  fecha_publicacion TEXT,
  codigo_invitacion TEXT NOT NULL UNIQUE,
  UNIQUE (codigo_invitacion),
  CHECK (estado IN ('Borrador','Publicada')),
  CHECK (length(codigo_invitacion) = 6 AND substr(codigo_invitacion,1,1) GLOB '[ABCDEFGHJKMNPQRSTUVWXYZ23456789]' AND substr(codigo_invitacion,2,1) GLOB '[ABCDEFGHJKMNPQRSTUVWXYZ23456789]' AND substr(codigo_invitacion,3,1) GLOB '[ABCDEFGHJKMNPQRSTUVWXYZ23456789]' AND substr(codigo_invitacion,4,1) GLOB '[ABCDEFGHJKMNPQRSTUVWXYZ23456789]' AND substr(codigo_invitacion,5,1) GLOB '[ABCDEFGHJKMNPQRSTUVWXYZ23456789]' AND substr(codigo_invitacion,6,1) GLOB '[ABCDEFGHJKMNPQRSTUVWXYZ23456789]'),
  FOREIGN KEY (id_docente) REFERENCES docente(id_docente) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (codigo_dba) REFERENCES dba(codigo_dba) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE dba (
  codigo_dba TEXT PRIMARY KEY NOT NULL,
  area TEXT NOT NULL,
  grado TEXT NOT NULL,
  enunciado TEXT NOT NULL,
  ejemplo TEXT
);

CREATE TABLE evidencia (
  codigo_dba TEXT NOT NULL,
  numero_evidencia INTEGER NOT NULL,
  enunciado TEXT NOT NULL,
  PRIMARY KEY (codigo_dba, numero_evidencia),
  CHECK (numero_evidencia > 0),
  FOREIGN KEY (codigo_dba) REFERENCES dba(codigo_dba) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE evidencia_dictamen (
  codigo_dba TEXT NOT NULL,
  numero_evidencia INTEGER NOT NULL,
  aplica_formato_cerrado INTEGER NOT NULL,
  justificacion TEXT,
  fecha_dictamen TEXT NOT NULL,
  PRIMARY KEY (codigo_dba, numero_evidencia),
  FOREIGN KEY (codigo_dba, numero_evidencia) REFERENCES evidencia(codigo_dba, numero_evidencia) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE experiencia_evidencia (
  id_experiencia INTEGER NOT NULL,
  codigo_dba TEXT NOT NULL,
  numero_evidencia INTEGER NOT NULL,
  incluida INTEGER NOT NULL DEFAULT 1,
  PRIMARY KEY (id_experiencia, codigo_dba, numero_evidencia),
  FOREIGN KEY (id_experiencia) REFERENCES experiencia(id_experiencia) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (codigo_dba, numero_evidencia) REFERENCES evidencia(codigo_dba, numero_evidencia) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE inscripcion (
  id_inscripcion INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  id_estudiante INTEGER NOT NULL,
  id_experiencia INTEGER NOT NULL,
  fecha_union TEXT NOT NULL,
  UNIQUE (id_estudiante, id_experiencia),
  UNIQUE (id_inscripcion, id_experiencia),
  FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (id_experiencia) REFERENCES experiencia(id_experiencia) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE item (
  id_item INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  id_experiencia INTEGER NOT NULL,
  codigo_dba TEXT NOT NULL,
  numero_evidencia INTEGER NOT NULL,
  enunciado TEXT NOT NULL,
  formato TEXT NOT NULL DEFAULT 'single_choice',
  origen TEXT NOT NULL DEFAULT 'ia',
  estado_revision TEXT NOT NULL DEFAULT 'sin_revisar',
  excluido INTEGER NOT NULL DEFAULT 0,
  CHECK (formato IN ('single_choice','matching','ordering')),
  CHECK (origen IN ('ia','editado_docente')),
  FOREIGN KEY (id_experiencia, codigo_dba, numero_evidencia) REFERENCES experiencia_evidencia(id_experiencia, codigo_dba, numero_evidencia) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE opcion (
  id_opcion INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  id_item INTEGER NOT NULL,
  texto TEXT NOT NULL,
  orden INTEGER,
  es_correcta INTEGER,
  grupo TEXT,
  hipotesis_error TEXT,
  CHECK (grupo IN ('izquierda','derecha')),
  FOREIGN KEY (id_item) REFERENCES item(id_item) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE presentacion (
  id_inscripcion INTEGER NOT NULL,
  id_item INTEGER NOT NULL,
  orden_presentacion INTEGER NOT NULL,
  fecha_presentacion TEXT NOT NULL,
  PRIMARY KEY (id_inscripcion, id_item),
  CHECK (orden_presentacion > 0),
  FOREIGN KEY (id_inscripcion) REFERENCES inscripcion(id_inscripcion) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (id_item) REFERENCES item(id_item) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE respuesta (
  id_respuesta INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  id_inscripcion INTEGER NOT NULL,
  id_item INTEGER NOT NULL,
  certeza INTEGER NOT NULL,
  fecha_respuesta TEXT NOT NULL,
  correcta INTEGER NOT NULL,
  UNIQUE (id_inscripcion, id_item),
  CHECK (certeza BETWEEN 0 AND 5),
  FOREIGN KEY (id_inscripcion, id_item) REFERENCES presentacion(id_inscripcion, id_item) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE respuesta_opcion (
  id_respuesta INTEGER NOT NULL,
  id_opcion INTEGER NOT NULL,
  valor_dado INTEGER,
  PRIMARY KEY (id_respuesta, id_opcion),
  FOREIGN KEY (id_respuesta) REFERENCES respuesta(id_respuesta) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (id_opcion) REFERENCES opcion(id_opcion) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE resultado (
  id_inscripcion INTEGER NOT NULL,
  id_experiencia INTEGER NOT NULL,
  codigo_dba TEXT NOT NULL,
  numero_evidencia INTEGER NOT NULL,
  estado TEXT NOT NULL,
  fecha_calculo TEXT NOT NULL,
  PRIMARY KEY (id_inscripcion, codigo_dba, numero_evidencia),
  CHECK (estado IN ('muestra','no_muestra','no_concluyente')),
  FOREIGN KEY (id_inscripcion, id_experiencia) REFERENCES inscripcion(id_inscripcion, id_experiencia) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (id_experiencia, codigo_dba, numero_evidencia) REFERENCES experiencia_evidencia(id_experiencia, codigo_dba, numero_evidencia) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ---- indices sobre FK no cubiertas por una llave existente ----
CREATE INDEX idx_experiencia_id_docente ON experiencia(id_docente);
CREATE INDEX idx_experiencia_codigo_dba ON experiencia(codigo_dba);
CREATE INDEX idx_experiencia_evidencia_codigo_dba_numero_evidencia ON experiencia_evidencia(codigo_dba, numero_evidencia);
CREATE INDEX idx_inscripcion_id_experiencia ON inscripcion(id_experiencia);
CREATE INDEX idx_item_id_experiencia_codigo_dba_numero_evidencia ON item(id_experiencia, codigo_dba, numero_evidencia);
CREATE INDEX idx_opcion_id_item ON opcion(id_item);
CREATE INDEX idx_presentacion_id_item ON presentacion(id_item);
CREATE INDEX idx_respuesta_opcion_id_opcion ON respuesta_opcion(id_opcion);
CREATE INDEX idx_resultado_id_inscripcion_id_experiencia ON resultado(id_inscripcion, id_experiencia);
CREATE INDEX idx_resultado_id_experiencia_codigo_dba_numero_evidencia ON resultado(id_experiencia, codigo_dba, numero_evidencia);
