-- Esquema de produccion — AdaptiveLearn
-- GENERADO por modelo-relacional/generar.py — no editar a mano.
-- Dialecto: MySQL 8.0.16 o posterior (RNF-14). Tambien corre en
-- MariaDB 10.11: no usa nada que ese motor no tenga.
-- Ejecutar dentro de una base de datos VACIA, ya seleccionada con USE.
-- Los CHECK se hacen cumplir desde MySQL 8.0.16; antes se ignoraban.
SET NAMES utf8mb4;

CREATE TABLE docente (
  id_docente INT UNSIGNED AUTO_INCREMENT NOT NULL,
  nombres VARCHAR(120) NOT NULL,
  apellidos VARCHAR(120) NOT NULL,
  avatar_url VARCHAR(500) NULL,
  PRIMARY KEY (id_docente),
  CONSTRAINT ck_docente_1 CHECK (TRIM(nombres) <> '' AND TRIM(apellidos) <> '')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE estudiante (
  id_estudiante INT UNSIGNED AUTO_INCREMENT NOT NULL,
  nombres VARCHAR(120) NOT NULL,
  apellidos VARCHAR(120) NOT NULL,
  avatar_url VARCHAR(500) NULL,
  PRIMARY KEY (id_estudiante),
  CONSTRAINT ck_estudiante_1 CHECK (TRIM(nombres) <> '' AND TRIM(apellidos) <> '')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE credencial (
  id_credencial INT UNSIGNED AUTO_INCREMENT NOT NULL,
  id_docente INT UNSIGNED NULL,
  id_estudiante INT UNSIGNED NULL,
  correo VARCHAR(254) NOT NULL,
  proveedor ENUM('correo','google','microsoft') NOT NULL,
  password_hash VARCHAR(255) NULL,
  proveedor_id VARCHAR(255) NULL,
  email_verificado BOOLEAN NOT NULL DEFAULT FALSE,
  codigo_verificacion CHAR(6) NULL,
  codigo_expira_en DATETIME NULL,
  codigo_ultimo_envio DATETIME NULL,
  intentos_codigo TINYINT UNSIGNED NOT NULL DEFAULT 0,
  intentos_login TINYINT UNSIGNED NOT NULL DEFAULT 0,
  bloqueado_hasta DATETIME NULL,
  creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id_credencial),
  CONSTRAINT uq_credencial_1 UNIQUE (correo),
  CONSTRAINT uq_credencial_2 UNIQUE (id_docente),
  CONSTRAINT uq_credencial_3 UNIQUE (id_estudiante),
  CONSTRAINT uq_credencial_4 UNIQUE (proveedor, proveedor_id),
  CONSTRAINT ck_credencial_1 CHECK (id_docente IS NULL OR id_estudiante IS NULL),
  CONSTRAINT ck_credencial_2 CHECK ((proveedor = 'correo' AND password_hash IS NOT NULL AND proveedor_id IS NULL) OR (proveedor <> 'correo' AND password_hash IS NULL AND proveedor_id IS NOT NULL AND email_verificado = 1)),
  CONSTRAINT fk_credencial_1 FOREIGN KEY (id_docente) REFERENCES docente(id_docente) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT fk_credencial_2 FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE dba (
  codigo_dba VARCHAR(40) NOT NULL,
  area VARCHAR(40) NOT NULL,
  grado VARCHAR(4) NOT NULL,
  enunciado TEXT NOT NULL,
  ejemplo TEXT NULL,
  PRIMARY KEY (codigo_dba)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE experiencia (
  id_experiencia INT UNSIGNED AUTO_INCREMENT NOT NULL,
  id_docente INT UNSIGNED NOT NULL,
  codigo_dba VARCHAR(40) NOT NULL,
  nombre VARCHAR(160) NOT NULL,
  estado ENUM('Borrador','Publicada') NOT NULL DEFAULT 'Borrador',
  fecha_creacion DATETIME NOT NULL,
  fecha_publicacion DATETIME NULL,
  codigo_invitacion CHAR(6) NOT NULL,
  servicio_ia ENUM('gemini','deepseek') NOT NULL,
  modelo_ia VARCHAR(80) NOT NULL,
  PRIMARY KEY (id_experiencia),
  CONSTRAINT uq_experiencia_1 UNIQUE (codigo_invitacion),
  CONSTRAINT uq_experiencia_2 UNIQUE (id_experiencia, codigo_dba),
  KEY idx_experiencia_id_docente (id_docente),
  KEY idx_experiencia_codigo_dba (codigo_dba),
  CONSTRAINT ck_experiencia_1 CHECK ((estado = 'Borrador' AND fecha_publicacion IS NULL) OR (estado = 'Publicada' AND fecha_publicacion IS NOT NULL)),
  CONSTRAINT ck_experiencia_2 CHECK (codigo_invitacion REGEXP '^[ABCDEFGHJKMNPQRSTUVWXYZ23456789]{6}$'),
  CONSTRAINT fk_experiencia_1 FOREIGN KEY (id_docente) REFERENCES docente(id_docente) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_experiencia_2 FOREIGN KEY (codigo_dba) REFERENCES dba(codigo_dba) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE evidencia (
  codigo_dba VARCHAR(40) NOT NULL,
  numero_evidencia TINYINT UNSIGNED NOT NULL,
  enunciado TEXT NOT NULL,
  PRIMARY KEY (codigo_dba, numero_evidencia),
  CONSTRAINT ck_evidencia_1 CHECK (numero_evidencia > 0),
  CONSTRAINT fk_evidencia_1 FOREIGN KEY (codigo_dba) REFERENCES dba(codigo_dba) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE evidencia_dictamen (
  codigo_dba VARCHAR(40) NOT NULL,
  numero_evidencia TINYINT UNSIGNED NOT NULL,
  aplica_formato_cerrado BOOLEAN NOT NULL,
  formato ENUM('single_choice','matching','ordering') NULL,
  justificacion TEXT NULL,
  fecha_dictamen DATETIME NOT NULL,
  PRIMARY KEY (codigo_dba, numero_evidencia),
  CONSTRAINT ck_evidencia_dictamen_1 CHECK ((aplica_formato_cerrado = 1 AND formato IS NOT NULL) OR (aplica_formato_cerrado = 0 AND formato IS NULL)),
  CONSTRAINT fk_evidencia_dictamen_1 FOREIGN KEY (codigo_dba, numero_evidencia) REFERENCES evidencia(codigo_dba, numero_evidencia) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE experiencia_evidencia (
  id_experiencia INT UNSIGNED NOT NULL,
  codigo_dba VARCHAR(40) NOT NULL,
  numero_evidencia TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (id_experiencia, codigo_dba, numero_evidencia),
  KEY idx_experiencia_evidencia_codigo_dba_numero_evidencia (codigo_dba, numero_evidencia),
  CONSTRAINT fk_experiencia_evidencia_1 FOREIGN KEY (id_experiencia, codigo_dba) REFERENCES experiencia(id_experiencia, codigo_dba) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_experiencia_evidencia_2 FOREIGN KEY (codigo_dba, numero_evidencia) REFERENCES evidencia(codigo_dba, numero_evidencia) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE inscripcion (
  id_inscripcion INT UNSIGNED AUTO_INCREMENT NOT NULL,
  id_estudiante INT UNSIGNED NOT NULL,
  id_experiencia INT UNSIGNED NOT NULL,
  fecha_union DATETIME NOT NULL,
  PRIMARY KEY (id_inscripcion),
  CONSTRAINT uq_inscripcion_1 UNIQUE (id_estudiante, id_experiencia),
  CONSTRAINT uq_inscripcion_2 UNIQUE (id_inscripcion, id_experiencia),
  KEY idx_inscripcion_id_experiencia (id_experiencia),
  CONSTRAINT fk_inscripcion_1 FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_inscripcion_2 FOREIGN KEY (id_experiencia) REFERENCES experiencia(id_experiencia) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE item (
  id_item INT UNSIGNED AUTO_INCREMENT NOT NULL,
  id_experiencia INT UNSIGNED NOT NULL,
  codigo_dba VARCHAR(40) NOT NULL,
  numero_evidencia TINYINT UNSIGNED NOT NULL,
  enunciado TEXT NOT NULL,
  formato ENUM('single_choice','matching','ordering') NOT NULL DEFAULT 'single_choice',
  origen ENUM('ia','editado_docente','creado_docente') NOT NULL DEFAULT 'ia',
  excluido BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (id_item),
  CONSTRAINT uq_item_1 UNIQUE (id_item, id_experiencia),
  KEY idx_item_id_experiencia_codigo_dba_numero_evidencia (id_experiencia, codigo_dba, numero_evidencia),
  CONSTRAINT fk_item_1 FOREIGN KEY (id_experiencia, codigo_dba, numero_evidencia) REFERENCES experiencia_evidencia(id_experiencia, codigo_dba, numero_evidencia) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE opcion (
  id_opcion INT UNSIGNED AUTO_INCREMENT NOT NULL,
  id_item INT UNSIGNED NOT NULL,
  texto TEXT NOT NULL,
  orden TINYINT UNSIGNED NULL,
  es_correcta BOOLEAN NULL,
  grupo ENUM('izquierda','derecha') NULL,
  hipotesis_error TEXT NULL,
  PRIMARY KEY (id_opcion),
  CONSTRAINT uq_opcion_1 UNIQUE (id_opcion, id_item),
  KEY idx_opcion_id_item (id_item),
  CONSTRAINT fk_opcion_1 FOREIGN KEY (id_item) REFERENCES item(id_item) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE presentacion (
  id_inscripcion INT UNSIGNED NOT NULL,
  id_item INT UNSIGNED NOT NULL,
  id_experiencia INT UNSIGNED NOT NULL,
  orden_presentacion TINYINT UNSIGNED NOT NULL,
  fecha_presentacion DATETIME NOT NULL,
  PRIMARY KEY (id_inscripcion, id_item),
  CONSTRAINT uq_presentacion_1 UNIQUE (id_inscripcion, orden_presentacion),
  KEY idx_presentacion_id_inscripcion_id_experiencia (id_inscripcion, id_experiencia),
  KEY idx_presentacion_id_item_id_experiencia (id_item, id_experiencia),
  CONSTRAINT ck_presentacion_1 CHECK (orden_presentacion > 0),
  CONSTRAINT fk_presentacion_1 FOREIGN KEY (id_inscripcion, id_experiencia) REFERENCES inscripcion(id_inscripcion, id_experiencia) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_presentacion_2 FOREIGN KEY (id_item, id_experiencia) REFERENCES item(id_item, id_experiencia) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE respuesta (
  id_respuesta INT UNSIGNED AUTO_INCREMENT NOT NULL,
  id_inscripcion INT UNSIGNED NOT NULL,
  id_item INT UNSIGNED NOT NULL,
  certeza TINYINT UNSIGNED NOT NULL,
  fecha_respuesta DATETIME NOT NULL,
  correcta BOOLEAN NOT NULL,
  PRIMARY KEY (id_respuesta),
  CONSTRAINT uq_respuesta_1 UNIQUE (id_inscripcion, id_item),
  CONSTRAINT uq_respuesta_2 UNIQUE (id_respuesta, id_item),
  CONSTRAINT ck_respuesta_1 CHECK (certeza BETWEEN 0 AND 5),
  CONSTRAINT fk_respuesta_1 FOREIGN KEY (id_inscripcion, id_item) REFERENCES presentacion(id_inscripcion, id_item) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE respuesta_opcion (
  id_respuesta INT UNSIGNED NOT NULL,
  id_opcion INT UNSIGNED NOT NULL,
  id_item INT UNSIGNED NOT NULL,
  valor_dado TINYINT UNSIGNED NULL,
  PRIMARY KEY (id_respuesta, id_opcion),
  KEY idx_respuesta_opcion_id_respuesta_id_item (id_respuesta, id_item),
  KEY idx_respuesta_opcion_id_opcion_id_item (id_opcion, id_item),
  CONSTRAINT fk_respuesta_opcion_1 FOREIGN KEY (id_respuesta, id_item) REFERENCES respuesta(id_respuesta, id_item) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_respuesta_opcion_2 FOREIGN KEY (id_opcion, id_item) REFERENCES opcion(id_opcion, id_item) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE resultado (
  id_inscripcion INT UNSIGNED NOT NULL,
  id_experiencia INT UNSIGNED NOT NULL,
  codigo_dba VARCHAR(40) NOT NULL,
  numero_evidencia TINYINT UNSIGNED NOT NULL,
  estado ENUM('muestra','no_muestra','no_concluyente') NOT NULL,
  fecha_calculo DATETIME NOT NULL,
  PRIMARY KEY (id_inscripcion, codigo_dba, numero_evidencia),
  KEY idx_resultado_id_inscripcion_id_experiencia (id_inscripcion, id_experiencia),
  KEY idx_resultado_id_experiencia_codigo_dba_numero_evidencia (id_experiencia, codigo_dba, numero_evidencia),
  CONSTRAINT fk_resultado_1 FOREIGN KEY (id_inscripcion, id_experiencia) REFERENCES inscripcion(id_inscripcion, id_experiencia) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_resultado_2 FOREIGN KEY (id_experiencia, codigo_dba, numero_evidencia) REFERENCES experiencia_evidencia(id_experiencia, codigo_dba, numero_evidencia) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

