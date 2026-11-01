# 21. Revisión del docente del 2026-10-22 — triaje

**Metodología:** MODESEC — Fase III. **Registrado:** 2026-10-26.

**Qué revisó:** la parte que el docente considera la columna vertebral
del sistema: el acceso (credencial, docente, estudiante) y el catálogo
curricular. No revisó el MER completo.

**Fuente:** notas tomadas por el equipo durante la revisión. No hay un
documento escrito por el docente. Por eso cada nota va con **su
interpretación**, y donde hay más de una lectura posible, se declara
como pregunta para el docente en vez de adivinar.

## Las notas, tal como se tomaron

> tabla para grados y área y codificar
> id_usuario cambiar en id_estudiante y docente
> cambiar email a estado_verificado estado_procesando
> quitar codigo_expira_en y codigo_ultimo_envio
> crear correo al sistema adaptivelearn@ (desde aquí se envían los correos al usuario)

## Contra qué se comparó

- **MER final** (`16-modelo-entidad-relacion.md`, fuente `mer/datos_mer.py`).
- **Backend del incremento I1** (`backend/sql/001_esquema_auth.sql`,
  `backend/sql/002_alineacion_guia_y_seguridad.sql`,
  `backend/src/user/entities/user.entity.ts`).

Los campos que nombra el docente están en los dos: `email_verificado`,
`codigo_expira_en` y `codigo_ultimo_envio` son atributos de CREDENCIAL
en el MER y columnas en el backend. "id_usuario" no aparece escrito así
en ningún lado; lo más cercano es la entidad genérica **`User`** del
backend (con su `id` y las rutas `/users`), heredada de la guía de JWT
del curso.

**Hallazgo al comparar:** el backend de I1 está desfasado del MER final.
Docente y estudiante guardan todavía `nombre` y `correo`; la credencial
repite nombres, apellidos y foto, y tiene `nombre_completo`. El
documento `20-catalogo-endpoints.md` ya lo anotaba como ajustes
pendientes del backend.

## Triaje

| # | Nota | Interpretación | Decisión | Dónde se aplica |
|---|---|---|---|---|
| **R1** | Tabla para grados y área, y codificar | Área y Grado como entidades, con código; y un código limpio para el DBA (hoy `matemáticas_1_dba_1`, con tilde) | **Aceptada** — ADR-036. Se agrega además **Documento oficial** (recomendación del equipo) | MER, MR, diccionario |
| **R2** | id_usuario → id_estudiante e id_docente | Que el sistema no trabaje con un "usuario" genérico, sino con docente y estudiante | **Aceptada para el backend**: identificar por `id_docente` / `id_estudiante`. El MER ya no tiene "usuario". *(La idea inicial de quitar `User` y `/users` la reemplazó ADR-040: la guía v2 los evalúa; ver «Estado».)* **Pregunta P1** sobre CREDENCIAL | Backend (Fase IV) |
| **R3** | email → estado_verificado / estado_procesando | Reemplazar el sí/no de correo verificado por un estado | **Aceptada** — ADR-037: `estado_verificacion` con `procesando` / `verificado` | MER, MR, backend |
| **R4** | Quitar `codigo_expira_en` y `codigo_ultimo_envio` | Que la credencial no cargue esos datos | **Aceptada — ADR-039**, a confirmar con el docente (P2): los códigos en su propia tabla; vencimiento y espera se calculan | MER, MR, backend |
| **R5** | Correo del sistema adaptivelearn@ | Una cuenta de correo propia del proyecto como remitente de los códigos | **Aceptada.** No es del modelo de datos: es configuración. La cuenta la crea el equipo; su clave va solo en `backend/.env` | Backend (Fase IV) |

## Preguntas para el docente

- **P1.** ¿Pide también quitar la entidad **CREDENCIAL** (la cuenta de
  acceso, ADR-034), o solo el "usuario" genérico del backend? La
  credencial existe porque el código de verificación se guarda antes de
  que la persona elija rol, y porque el correo debe ser único entre
  docentes y estudiantes.
- **P2.** Al quitar `codigo_expira_en` y `codigo_ultimo_envio`, ¿el
  vencimiento del código y la espera para reenviarlo se guardan en una
  **tabla aparte de códigos de verificación**, o se **simplifica** esa
  regla en esta versión?

## Estado

*(Actualizado el 2026-11-01.)*

| # | Estado | Dónde se ve |
|---|---|---|
| **R1** | **Aplicada** en el MER, el MR y el diccionario (encargo 01, pull request #1). Desde el encargo 03, también en el backend: tablas `area`, `grado` y `documento_oficial` cargadas, y las rutas `/catalogo/*` | `16`, `17`, `backend/sql/` |
| **R2** | **Aplicada en el backend** (encargo 03, ADR-040). La sesión (JWT) lleva el rol (`docente`, `estudiante` o `admin`) y el `idDocente` o el `idEstudiante`. La clase `User` de la guía se queda, pero sobre la tabla `credencial`: la guía v2 la evalúa, con `/users` solo para administrador | `backend/src/auth/interfaces/jwt-payload.interface.ts`, informe de la guía (D-03, D-11) |
| **R3** | **Aplicada** en el modelo (encargo 01) y en el backend (encargo 03): `estado_verificacion` `procesando` / `verificado` | `17`, `backend/src/user/entities/user.entity.ts` |
| **R4** | **Aplicada (ADR-039), a confirmar con el docente:** P2 sigue sin respuesta. `codigo_expira_en`, `codigo_ultimo_envio` y `codigo_verificacion` salieron de la credencial; los códigos viven en la tabla `codigo_verificacion`, el vencimiento (10 min) y la espera (30 s) se calculan, y una tarea nocturna limpia lo vencido | `16` §4, `17` §5.7, `backend/src/auth/codigo.service.ts`, `backend/src/limpieza/` |
| **R5** | **Aplicada en el backend** (encargo 03): los códigos se envían por SMTP con `adaptivelearn.sistema@gmail.com`, configurado en `.env`. **Probado con un envío real el 2026-10-27:** llegó el código y la cuenta quedó `verificado`. Cada integrante pone la contraseña de aplicación en su propio `.env`; sin ella, el código sale en la consola del servidor | `backend/src/correo/`, `backend/README.md` |

Quedan abiertas las preguntas **P1** y **P2**.
