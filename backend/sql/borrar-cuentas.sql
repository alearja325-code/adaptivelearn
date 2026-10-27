-- Borra TODAS las cuentas (credenciales, códigos, docentes y estudiantes)
-- para repetir desde cero las pruebas de la sección 7 de la guía: los ids
-- vuelven a empezar en 1, como en la guía. No toca el catálogo.
-- SOLO para desarrollo.
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE codigo_verificacion;
TRUNCATE TABLE credencial;
TRUNCATE TABLE docente;
TRUNCATE TABLE estudiante;
SET FOREIGN_KEY_CHECKS = 1;
