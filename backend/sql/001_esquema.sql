-- Esquema del backend — AdaptiveLearn
-- GENERADO por docs/modesec/fase-3-diseno-computacional/modelo-relacional/
-- generar.py desde datos_mr.py — no editar a mano: cambiar el MR y regenerar.
-- Es mr_mysql.sql, solo con las tablas que el backend usa hoy (encargo 03):
-- credencial, codigo_verificacion, docente, estudiante, area, grado, documento_oficial, dba, evidencia, evidencia_dictamen.
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
  estado_verificacion ENUM('procesando','verificado') NOT NULL DEFAULT 'procesando',
  es_admin BOOLEAN NOT NULL DEFAULT 0,
  nombre_completo VARCHAR(240) NULL,
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
  CONSTRAINT ck_credencial_2 CHECK ((proveedor = 'correo' AND password_hash IS NOT NULL AND proveedor_id IS NULL) OR (proveedor <> 'correo' AND password_hash IS NULL AND proveedor_id IS NOT NULL AND estado_verificacion = 'verificado')),
  CONSTRAINT fk_credencial_1 FOREIGN KEY (id_docente) REFERENCES docente(id_docente) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT fk_credencial_2 FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE codigo_verificacion (
  id_credencial INT UNSIGNED NOT NULL,
  proposito ENUM('verificar_correo','recuperar_contrasena') NOT NULL,
  codigo_hash CHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  intentos TINYINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (id_credencial, proposito),
  CONSTRAINT ck_codigo_verificacion_1 CHECK (intentos <= 5),
  CONSTRAINT ck_codigo_verificacion_2 CHECK (codigo_hash REGEXP '^[0-9a-f]{64}$'),
  CONSTRAINT fk_codigo_verificacion_1 FOREIGN KEY (id_credencial) REFERENCES credencial(id_credencial) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE area (
  codigo_area VARCHAR(3) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  nombre VARCHAR(40) NOT NULL,
  PRIMARY KEY (codigo_area),
  CONSTRAINT uq_area_1 UNIQUE (nombre),
  CONSTRAINT ck_area_1 CHECK (codigo_area REGEXP '^[A-Z]{2,3}$')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE grado (
  numero TINYINT UNSIGNED NOT NULL,
  nombre VARCHAR(20) NOT NULL,
  nivel ENUM('basica_primaria','basica_secundaria','media') NOT NULL,
  PRIMARY KEY (numero),
  CONSTRAINT uq_grado_1 UNIQUE (nombre),
  CONSTRAINT ck_grado_1 CHECK ((numero BETWEEN 1 AND 5 AND nivel = 'basica_primaria') OR (numero BETWEEN 6 AND 9 AND nivel = 'basica_secundaria') OR (numero BETWEEN 10 AND 11 AND nivel = 'media'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE documento_oficial (
  id_documento INT UNSIGNED AUTO_INCREMENT NOT NULL,
  codigo_area VARCHAR(3) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  titulo VARCHAR(200) NOT NULL,
  version VARCHAR(10) NOT NULL,
  anio SMALLINT UNSIGNED NOT NULL,
  paginas SMALLINT UNSIGNED NOT NULL,
  url_oficial VARCHAR(500) NOT NULL,
  PRIMARY KEY (id_documento),
  CONSTRAINT uq_documento_oficial_1 UNIQUE (codigo_area, version),
  CONSTRAINT uq_documento_oficial_2 UNIQUE (id_documento, codigo_area),
  CONSTRAINT ck_documento_oficial_1 CHECK (paginas > 0 AND TRIM(titulo) <> '' AND TRIM(version) <> ''),
  CONSTRAINT fk_documento_oficial_1 FOREIGN KEY (codigo_area) REFERENCES area(codigo_area) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE dba (
  codigo_dba VARCHAR(9) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  codigo_area VARCHAR(3) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  numero_grado TINYINT UNSIGNED NOT NULL,
  id_documento INT UNSIGNED NOT NULL,
  enunciado TEXT NOT NULL,
  ejemplo TEXT NULL,
  PRIMARY KEY (codigo_dba),
  KEY idx_dba_codigo_area (codigo_area),
  KEY idx_dba_numero_grado (numero_grado),
  KEY idx_dba_id_documento_codigo_area (id_documento, codigo_area),
  CONSTRAINT ck_dba_1 CHECK (codigo_dba = CONCAT(codigo_area, '-', LPAD(numero_grado, 2, '0'), '-', RIGHT(codigo_dba, 2)) AND RIGHT(codigo_dba, 2) REGEXP '^[0-9]{2}$' AND RIGHT(codigo_dba, 2) <> '00'),
  CONSTRAINT fk_dba_1 FOREIGN KEY (codigo_area) REFERENCES area(codigo_area) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT fk_dba_2 FOREIGN KEY (numero_grado) REFERENCES grado(numero) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT fk_dba_3 FOREIGN KEY (id_documento, codigo_area) REFERENCES documento_oficial(id_documento, codigo_area) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE evidencia (
  codigo_dba VARCHAR(9) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  numero_evidencia TINYINT UNSIGNED NOT NULL,
  enunciado TEXT NOT NULL,
  PRIMARY KEY (codigo_dba, numero_evidencia),
  CONSTRAINT ck_evidencia_1 CHECK (numero_evidencia > 0),
  CONSTRAINT fk_evidencia_1 FOREIGN KEY (codigo_dba) REFERENCES dba(codigo_dba) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE evidencia_dictamen (
  codigo_dba VARCHAR(9) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  numero_evidencia TINYINT UNSIGNED NOT NULL,
  aplica_formato_cerrado BOOLEAN NOT NULL,
  formato ENUM('single_choice','matching','ordering') NULL,
  justificacion TEXT NULL,
  fecha_dictamen DATETIME NOT NULL,
  PRIMARY KEY (codigo_dba, numero_evidencia),
  CONSTRAINT ck_evidencia_dictamen_1 CHECK ((aplica_formato_cerrado = 1 AND formato IS NOT NULL) OR (aplica_formato_cerrado = 0 AND formato IS NULL)),
  CONSTRAINT fk_evidencia_dictamen_1 FOREIGN KEY (codigo_dba, numero_evidencia) REFERENCES evidencia(codigo_dba, numero_evidencia) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

