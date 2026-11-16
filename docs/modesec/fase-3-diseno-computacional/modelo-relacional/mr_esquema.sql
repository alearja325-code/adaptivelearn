-- Esquema ejecutable — AdaptiveLearn
-- GENERADO por modelo-relacional/generar.py — no editar a mano.
-- Dialecto: SQLite, solo para la verificacion mecanica (verificar_mr.py).
-- El esquema real (MySQL 8) es mr_mysql.sql.
PRAGMA foreign_keys = ON;

CREATE TABLE credencial (
  id_credencial INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  id_docente INTEGER,
  id_estudiante INTEGER,
  correo TEXT COLLATE NOCASE NOT NULL UNIQUE,
  proveedor TEXT NOT NULL,
  password_hash TEXT,
  proveedor_id TEXT,
  estado_verificacion TEXT NOT NULL DEFAULT 'procesando',
  es_admin INTEGER NOT NULL DEFAULT 0,
  nombre_completo TEXT,
  intentos_login INTEGER NOT NULL DEFAULT 0,
  bloqueado_hasta TEXT,
  creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (id_docente),
  UNIQUE (id_estudiante),
  UNIQUE (proveedor, proveedor_id),
  CHECK (proveedor IN ('correo','google','microsoft')),
  CHECK (estado_verificacion IN ('procesando','verificado')),
  CHECK (id_docente IS NULL OR id_estudiante IS NULL),
  CHECK ((proveedor = 'correo' AND password_hash IS NOT NULL AND proveedor_id IS NULL) OR (proveedor <> 'correo' AND password_hash IS NULL AND proveedor_id IS NOT NULL AND estado_verificacion = 'verificado')),
  FOREIGN KEY (id_docente) REFERENCES docente(id_docente) ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante) ON DELETE RESTRICT ON UPDATE RESTRICT
);

CREATE TABLE codigo_verificacion (
  id_credencial INTEGER NOT NULL,
  proposito TEXT NOT NULL,
  codigo_hash TEXT NOT NULL,
  creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  intentos INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (id_credencial, proposito),
  CHECK (proposito IN ('verificar_correo','recuperar_contrasena')),
  CHECK (intentos <= 5),
  CHECK (length(codigo_hash) = 64 AND codigo_hash NOT GLOB '*[^0-9a-f]*'),
  FOREIGN KEY (id_credencial) REFERENCES credencial(id_credencial) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE docente (
  id_docente INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  nombres TEXT NOT NULL,
  apellidos TEXT NOT NULL,
  avatar_url TEXT,
  CHECK (TRIM(nombres) <> '' AND TRIM(apellidos) <> '')
);

CREATE TABLE estudiante (
  id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  nombres TEXT NOT NULL,
  apellidos TEXT NOT NULL,
  avatar_url TEXT,
  CHECK (TRIM(nombres) <> '' AND TRIM(apellidos) <> '')
);

CREATE TABLE experiencia (
  id_experiencia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  id_docente INTEGER NOT NULL,
  codigo_dba TEXT NOT NULL,
  nombre TEXT NOT NULL,
  estado TEXT NOT NULL DEFAULT 'Borrador',
  fecha_creacion TEXT NOT NULL,
  fecha_publicacion TEXT,
  codigo_invitacion TEXT COLLATE NOCASE NOT NULL UNIQUE,
  servicio_ia TEXT NOT NULL,
  modelo_ia TEXT NOT NULL,
  UNIQUE (id_experiencia, codigo_dba),
  CHECK (estado IN ('Borrador','Publicada')),
  CHECK (servicio_ia IN ('gemini','deepseek')),
  CHECK ((estado = 'Borrador' AND fecha_publicacion IS NULL) OR (estado = 'Publicada' AND fecha_publicacion IS NOT NULL)),
  CHECK (length(codigo_invitacion) = 6 AND substr(upper(codigo_invitacion),1,1) GLOB '[ABCDEFGHJKMNPQRSTUVWXYZ23456789]' AND substr(upper(codigo_invitacion),2,1) GLOB '[ABCDEFGHJKMNPQRSTUVWXYZ23456789]' AND substr(upper(codigo_invitacion),3,1) GLOB '[ABCDEFGHJKMNPQRSTUVWXYZ23456789]' AND substr(upper(codigo_invitacion),4,1) GLOB '[ABCDEFGHJKMNPQRSTUVWXYZ23456789]' AND substr(upper(codigo_invitacion),5,1) GLOB '[ABCDEFGHJKMNPQRSTUVWXYZ23456789]' AND substr(upper(codigo_invitacion),6,1) GLOB '[ABCDEFGHJKMNPQRSTUVWXYZ23456789]'),
  FOREIGN KEY (id_docente) REFERENCES docente(id_docente) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (codigo_dba) REFERENCES dba(codigo_dba) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE area (
  codigo_area TEXT PRIMARY KEY NOT NULL,
  nombre TEXT NOT NULL UNIQUE,
  CHECK (codigo_area GLOB '[A-Z][A-Z]' OR codigo_area GLOB '[A-Z][A-Z][A-Z]')
);

CREATE TABLE grado (
  numero INTEGER PRIMARY KEY NOT NULL,
  nombre TEXT NOT NULL UNIQUE,
  nivel TEXT NOT NULL,
  CHECK (nivel IN ('basica_primaria','basica_secundaria','media')),
  CHECK ((numero BETWEEN 1 AND 5 AND nivel = 'basica_primaria') OR (numero BETWEEN 6 AND 9 AND nivel = 'basica_secundaria') OR (numero BETWEEN 10 AND 11 AND nivel = 'media'))
);

CREATE TABLE documento_oficial (
  id_documento INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  codigo_area TEXT NOT NULL,
  titulo TEXT NOT NULL,
  version TEXT NOT NULL,
  anio INTEGER NOT NULL,
  paginas INTEGER NOT NULL,
  url_oficial TEXT NOT NULL,
  UNIQUE (codigo_area, version),
  UNIQUE (id_documento, codigo_area),
  CHECK (paginas > 0 AND TRIM(titulo) <> '' AND TRIM(version) <> ''),
  FOREIGN KEY (codigo_area) REFERENCES area(codigo_area) ON DELETE RESTRICT ON UPDATE RESTRICT
);

CREATE TABLE dba (
  codigo_dba TEXT PRIMARY KEY NOT NULL,
  codigo_area TEXT NOT NULL,
  numero_grado INTEGER NOT NULL,
  id_documento INTEGER NOT NULL,
  enunciado TEXT NOT NULL,
  ejemplo TEXT,
  ejemplo_tiene_imagen INTEGER NOT NULL DEFAULT 0,
  CHECK (codigo_dba = codigo_area || '-' || printf('%02d', numero_grado) || '-' || substr(codigo_dba, -2) AND substr(codigo_dba, -2) GLOB '[0-9][0-9]' AND substr(codigo_dba, -2) <> '00'),
  FOREIGN KEY (codigo_area) REFERENCES area(codigo_area) ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY (numero_grado) REFERENCES grado(numero) ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY (id_documento, codigo_area) REFERENCES documento_oficial(id_documento, codigo_area) ON DELETE RESTRICT ON UPDATE RESTRICT
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
  formato TEXT,
  justificacion TEXT,
  fecha_dictamen TEXT NOT NULL,
  PRIMARY KEY (codigo_dba, numero_evidencia),
  CHECK (formato IN ('single_choice','matching','ordering')),
  CHECK ((aplica_formato_cerrado = 1 AND formato IS NOT NULL) OR (aplica_formato_cerrado = 0 AND formato IS NULL)),
  FOREIGN KEY (codigo_dba, numero_evidencia) REFERENCES evidencia(codigo_dba, numero_evidencia) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE experiencia_evidencia (
  id_experiencia INTEGER NOT NULL,
  codigo_dba TEXT NOT NULL,
  numero_evidencia INTEGER NOT NULL,
  PRIMARY KEY (id_experiencia, codigo_dba, numero_evidencia),
  FOREIGN KEY (id_experiencia, codigo_dba) REFERENCES experiencia(id_experiencia, codigo_dba) ON DELETE CASCADE ON UPDATE CASCADE,
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
  excluido INTEGER NOT NULL DEFAULT 0,
  UNIQUE (id_item, id_experiencia),
  CHECK (formato IN ('single_choice','matching','ordering')),
  CHECK (origen IN ('ia','editado_docente','creado_docente')),
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
  UNIQUE (id_opcion, id_item),
  CHECK (grupo IN ('izquierda','derecha')),
  FOREIGN KEY (id_item) REFERENCES item(id_item) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE presentacion (
  id_inscripcion INTEGER NOT NULL,
  id_item INTEGER NOT NULL,
  id_experiencia INTEGER NOT NULL,
  orden_presentacion INTEGER NOT NULL,
  fecha_presentacion TEXT NOT NULL,
  PRIMARY KEY (id_inscripcion, id_item),
  UNIQUE (id_inscripcion, orden_presentacion),
  CHECK (orden_presentacion > 0),
  FOREIGN KEY (id_inscripcion, id_experiencia) REFERENCES inscripcion(id_inscripcion, id_experiencia) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (id_item, id_experiencia) REFERENCES item(id_item, id_experiencia) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE respuesta (
  id_respuesta INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  id_inscripcion INTEGER NOT NULL,
  id_item INTEGER NOT NULL,
  certeza INTEGER NOT NULL,
  fecha_respuesta TEXT NOT NULL,
  correcta INTEGER NOT NULL,
  UNIQUE (id_inscripcion, id_item),
  UNIQUE (id_respuesta, id_item),
  CHECK (certeza BETWEEN 0 AND 5),
  FOREIGN KEY (id_inscripcion, id_item) REFERENCES presentacion(id_inscripcion, id_item) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE respuesta_opcion (
  id_respuesta INTEGER NOT NULL,
  id_opcion INTEGER NOT NULL,
  id_item INTEGER NOT NULL,
  valor_dado INTEGER,
  PRIMARY KEY (id_respuesta, id_opcion),
  FOREIGN KEY (id_respuesta, id_item) REFERENCES respuesta(id_respuesta, id_item) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (id_opcion, id_item) REFERENCES opcion(id_opcion, id_item) ON DELETE CASCADE ON UPDATE CASCADE
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
  FOREIGN KEY (id_experiencia, codigo_dba, numero_evidencia) REFERENCES experiencia_evidencia(id_experiencia, codigo_dba, numero_evidencia) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ---- indices sobre FK no cubiertas por una llave existente ----
CREATE INDEX idx_experiencia_id_docente ON experiencia(id_docente);
CREATE INDEX idx_experiencia_codigo_dba ON experiencia(codigo_dba);
CREATE INDEX idx_dba_codigo_area ON dba(codigo_area);
CREATE INDEX idx_dba_numero_grado ON dba(numero_grado);
CREATE INDEX idx_dba_id_documento_codigo_area ON dba(id_documento, codigo_area);
CREATE INDEX idx_experiencia_evidencia_codigo_dba_numero_evidencia ON experiencia_evidencia(codigo_dba, numero_evidencia);
CREATE INDEX idx_inscripcion_id_experiencia ON inscripcion(id_experiencia);
CREATE INDEX idx_item_id_experiencia_codigo_dba_numero_evidencia ON item(id_experiencia, codigo_dba, numero_evidencia);
CREATE INDEX idx_opcion_id_item ON opcion(id_item);
CREATE INDEX idx_presentacion_id_inscripcion_id_experiencia ON presentacion(id_inscripcion, id_experiencia);
CREATE INDEX idx_presentacion_id_item_id_experiencia ON presentacion(id_item, id_experiencia);
CREATE INDEX idx_respuesta_opcion_id_respuesta_id_item ON respuesta_opcion(id_respuesta, id_item);
CREATE INDEX idx_respuesta_opcion_id_opcion_id_item ON respuesta_opcion(id_opcion, id_item);
CREATE INDEX idx_resultado_id_inscripcion_id_experiencia ON resultado(id_inscripcion, id_experiencia);
CREATE INDEX idx_resultado_id_experiencia_codigo_dba_numero_evidencia ON resultado(id_experiencia, codigo_dba, numero_evidencia);
