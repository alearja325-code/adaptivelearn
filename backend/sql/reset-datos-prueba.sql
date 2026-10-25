-- Vacía las 3 tablas de Auth para repetir la demostración de la sección 7
-- desde cero (los ids vuelven a empezar en 1, como en la guía).
-- SOLO para desarrollo: borra TODAS las cuentas.
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE credencial;
TRUNCATE TABLE docente;
TRUNCATE TABLE estudiante;
SET FOREIGN_KEY_CHECKS = 1;
