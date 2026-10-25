-- Esquema de autenticación — AdaptiveLearn V3, DSE-2
--
-- docente y estudiante: EXACTAMENTE como en
-- Metodologia MODESEC/fase-3-diseno-computacional/04-modelo-relacional.md
-- (ya aprobado y verificado con tokens). No se les agrega ninguna columna.
--
-- credencial: tabla nueva (decisión 2026-09-17, ver decisiones.md — ADR
-- pendiente de redactar). Guarda todo lo que la autenticación necesita y
-- que el modelo relacional de fase 3 no contemplaba: contraseña, proveedor
-- (correo/Google/Microsoft), verificación de correo, y los datos del
-- registro mientras está en curso (spec 19: nombres/apellidos/avatar antes
-- de que exista la fila final en docente o estudiante).
--
-- id_docente / id_estudiante son ambas NULL mientras el registro está en
-- curso; el CHECK impide que las dos tengan valor a la vez (spec 20: el rol
-- es una sola tabla, nunca las dos). Que ambas sigan NULL después de
-- "Elige tu rol" no lo puede impedir la base de datos — eso lo garantiza el
-- código de la aplicación.
--
-- Sin ON UPDATE CASCADE en esas 2 FK (a diferencia del resto del proyecto):
-- MariaDB no permite un CHECK sobre una columna que además es hija de una FK
-- con ON UPDATE CASCADE (error 1901). Es inofensivo omitirlo aquí — son
-- llaves sustitutas que nunca cambian de valor, mismo caso ya documentado
-- en 04-modelo-relacional.md para el resto de las FK del proyecto.

CREATE TABLE IF NOT EXISTS docente (
  id_docente  INT AUTO_INCREMENT PRIMARY KEY,
  nombre      VARCHAR(255) NOT NULL,
  correo      VARCHAR(255) NOT NULL,
  avatar_url  VARCHAR(512) NULL,
  CONSTRAINT uq_docente_correo UNIQUE (correo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS estudiante (
  id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
  nombre        VARCHAR(255) NOT NULL,
  correo        VARCHAR(255) NOT NULL,
  avatar_url    VARCHAR(512) NULL,
  CONSTRAINT uq_estudiante_correo UNIQUE (correo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS credencial (
  id_credencial         INT AUTO_INCREMENT PRIMARY KEY,
  correo                VARCHAR(255) NOT NULL,
  password_hash         VARCHAR(255) NULL,
  proveedor             ENUM('correo', 'google', 'microsoft') NOT NULL,
  proveedor_id          VARCHAR(255) NULL,
  email_verificado      BOOLEAN NOT NULL DEFAULT FALSE,
  codigo_verificacion   CHAR(6) NULL,
  codigo_expira_en      DATETIME NULL,
  codigo_ultimo_envio   DATETIME NULL,
  nombres               VARCHAR(255) NULL,
  apellidos             VARCHAR(255) NULL,
  avatar_url            VARCHAR(512) NULL,
  id_docente            INT NULL,
  id_estudiante         INT NULL,
  creado_en             DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_credencial_correo UNIQUE (correo),
  CONSTRAINT chk_credencial_un_solo_rol
    CHECK (id_docente IS NULL OR id_estudiante IS NULL),
  CONSTRAINT fk_credencial_docente
    FOREIGN KEY (id_docente) REFERENCES docente(id_docente)
    ON DELETE RESTRICT,
  CONSTRAINT fk_credencial_estudiante
    FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante)
    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
