-- 002 — Alineación con la guía del docente + límites de intentos
--
-- Solo agrega columnas a `credencial`; no toca docente ni estudiante (siguen
-- idénticas al modelo relacional aprobado).
--
-- nombre_completo  → el `fullName` de la entidad User de la guía. Se llena
--                    al registrarse (si se envía) o al completar el perfil
--                    (spec 19: nombres + apellidos).
-- actualizado_en   → el `updatedAt` de la entidad User de la guía.
-- intentos_codigo  → límite de intentos del código de 6 dígitos (sin límite,
--                    1.000.000 de combinaciones se pueden probar por fuerza
--                    bruta dentro de los 10 min de validez).
-- intentos_login / bloqueado_hasta → límite de intentos de login (la propia
--                    guía lo lista en "Próximos pasos recomendados").

ALTER TABLE credencial
  ADD COLUMN nombre_completo  VARCHAR(255) NULL AFTER password_hash,
  ADD COLUMN intentos_codigo  INT NOT NULL DEFAULT 0 AFTER codigo_ultimo_envio,
  ADD COLUMN intentos_login   INT NOT NULL DEFAULT 0 AFTER intentos_codigo,
  ADD COLUMN bloqueado_hasta  DATETIME NULL AFTER intentos_login,
  ADD COLUMN actualizado_en   DATETIME NOT NULL
    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP AFTER creado_en;

UPDATE credencial
  SET nombre_completo = CONCAT_WS(' ', nombres, apellidos)
  WHERE nombres IS NOT NULL AND apellidos IS NOT NULL;
