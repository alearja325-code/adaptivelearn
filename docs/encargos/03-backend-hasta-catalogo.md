# Encargo 03 — Backend: el acceso según la guía del docente, y la base de datos hasta el catálogo

**Para:** una sesión de Claude Code sobre este repositorio.
**Escrito:** 2026-10-26, desde la sesión local de Alejandro. *(Reescrito
el mismo día sobre la guía actualizada del docente; la primera versión
mandaba quitar `/users` y rompía las pruebas de la guía.)*
**Hazlo después de que el encargo 02 esté unido a `main`.**

**Antes de empezar, lee:**
1. `CLAUDE.md` y `docs/diseno/pendientes.md` (A14, A16).
2. **La guía del docente, versión 2:**
   `docs/cursos/dse-2-203453/guia-docente/guia-jwt-nestjs-v2-2026-10.txt`.
3. **ADR-040** (cómo se aplica la guía), y ADR-034, 035, 037, 039 en
   `docs/diseno/decisiones.md`.
4. `docs/cursos/dse-2-203453/backend-auth-informe-guia.md` — cómo se
   siguió la guía v1 en septiembre, y cada diferencia con su razón.
5. `docs/modesec/fase-3-diseno-computacional/21-revision-docente-2026-10-22.md`.

## 1. Qué hay que lograr

Que el backend (`backend/`, NestJS + MySQL):

- **siga la guía v2 del docente** en todo lo que ella evalúa, con **sus 6
  pruebas de la sección 7 funcionando**;
- implemente **por debajo el modelo final de AdaptiveLearn** hasta el
  catálogo curricular, con **las correcciones del docente** (R2 a R5);
- exponga lo que necesitan las pantallas **desde el acceso hasta el
  Paso 3 de "Crear experiencia"**, **sin crear la experiencia** (eso
  dispara la IA; es otra etapa).

## 2. La regla de oro (ADR-040)

**La guía manda en la forma; AdaptiveLearn manda en el fondo.**

- **De la guía:** carpetas y módulos (`user/`, `auth/`, `example/`),
  nombres de archivos, rutas (`/auth/register`, `/auth/login`,
  `/auth/profile`, `/users`, `/example/*`), guards, decoradores,
  `ValidationPipe` y `ClassSerializerInterceptor` globales, `@Exclude`
  en la contraseña, y las respuestas: 401 sin sesión, 403 sin permiso,
  409 correo repetido, 400 datos inválidos, 404 no existe, **200 en
  login**, **204 al borrar**.
- **`/users` solo para administrador**, como en la guía (crear, listar,
  ver, editar, borrar). La credencial tiene una **marca de
  administrador**, falsa por defecto, que **solo se pone por SQL**,
  como en la prueba 4 de la guía. Ninguna ruta la asigna.
- **De AdaptiveLearn:** la tabla `credencial` (no `users`) y las tablas
  `docente` / `estudiante`. La sesión (JWT) lleva el rol (`docente`,
  `estudiante` o `admin`) y el `id_docente` o `id_estudiante` (nota R2).
- **Toda diferencia con la guía se declara con su razón** en
  `backend-auth-informe-guia.md`, que pasa a comparar contra la v2.

## 3. Parte A — Primero, el modelo

En la fuente del MER y del MR, regenerando todo (cadena de
`19-entrega-fase-3.md` §3):

- **ADR-039:** entidad **CODIGO_VERIFICACION** (el código guardado con
  hash, su propósito —`verificar_correo` o `recuperar_contrasena`—,
  `creado_en`, `intentos`, ligada a su credencial; a lo sumo uno
  vigente por credencial y propósito). **CREDENCIAL pierde**
  `codigo_verificacion`, `codigo_expira_en`, `codigo_ultimo_envio` y
  los intentos del código.
- **ADR-040:** CREDENCIAL gana la **marca de administrador**.
- Cita ADR-039, ADR-040 y la nota R4 en las tablas de "qué cambió"
  (`16` §13, `17` §10).
- Todos los verificadores de `CLAUDE.md` deben seguir pasando. Regenera
  los PDF solo si hay Chrome o Edge; si no, dilo.

## 4. Parte B — La base de datos del backend

- El esquema de `backend/sql/` debe ser **el del modelo relacional**
  (`modelo-relacional/mr_mysql.sql`) para las tablas de esta etapa:
  `credencial`, `docente`, `estudiante`, `codigo_verificacion`, `area`,
  `grado`, `documento_oficial`, `dba`, `evidencia`, `evidencia_dictamen`.
  Mismos nombres, tipos, llaves y restricciones. **Si el backend
  necesita una columna que el MR no tiene, agrégala primero al MR con
  su razón.**
- **Datos de referencia** por script: 4 áreas, 11 grados con su nivel y
  4 documentos oficiales, con los valores de ADR-036 y de la tabla de
  ADR-033 (Ciencias Sociales es **V.1**).
- **DBA y evidencias**, desde `data/curriculo-men/catalogo/catalogo_dba.json`
  (encargo 02), **no** desde el JSON viejo. Los DBA que el encargo 02
  marcó como dudosos: decláralos, no los inventes.
- `evidencia_dictamen` queda sin filas (censo QA-014 pendiente).

## 5. Parte C — El acceso

Además de la guía (sección 2), las rutas propias de AdaptiveLearn de
`20-catalogo-endpoints.md` §3 (E-01 a E-13):

- **R3 / ADR-037:** `estado_verificacion` (`procesando` / `verificado`).
- **R4 / ADR-039:** códigos en `codigo_verificacion`; vencimiento (10
  min) y espera para reenviar (30 s) **calculados** desde `creado_en`;
  5 intentos por código; bloqueo de 15 min tras 5 intentos fallidos de
  inicio de sesión.
- **Tarea nocturna** (ADR-039), con `@nestjs/schedule`: a las 3:00 a. m.
  por defecto, borra códigos vencidos y credenciales con más de 7 días
  en `procesando` sin rol. Hora y días, configurables en `.env`.
- **R5 — envío real de correos.** Hoy el backend **no envía ninguno**.
  Envía los códigos (registro y recuperación) por SMTP, configurado en
  `.env` (`MAIL_HOST`, `MAIL_PORT`, `MAIL_USER`, `MAIL_PASSWORD`,
  `MAIL_FROM`). La cuenta del sistema es
  **`adaptivelearn.sistema@gmail.com`** (Gmail: `smtp.gmail.com`, 587;
  la contraseña de aplicación la pone el equipo en su `.env`). **Sin
  configuración de correo, en desarrollo escribe el código en la
  consola** y avísalo al arrancar. **Nunca** una clave en el código.
- **Google y Microsoft (E-04, E-05):** con su configuración en `.env`
  (el equipo todavía no tiene esas credenciales). Sin configuración, un
  error claro de "no configurado"; pruébalos con un proveedor simulado.
- **Registro a medias** (ADR-035): quien no eligió rol retoma en
  completar perfil.
- **Editar el propio perfil (E-12)** no puede ser `PATCH /users/:id`,
  que en la guía es de administrador: usa la ruta que proponga `20` §3,
  o una bajo `/auth/`, y decláralo.

## 6. Parte D — Las rutas del catálogo

- **E-14** `GET /catalogo/dbas` y **E-15** `GET /catalogo/dbas/:codigo`
  (`20` §4.1), filtrando por `codigo_area` y `numero_grado`.
- **Nuevas:** `GET /catalogo/areas` (Paso 1) y `GET /catalogo/grados`
  (filtro del Paso 2). Agrégalas a `api/datos_api.py`, regenera `20` y
  decláralas.
- Solo lectura, solo para la sesión de un docente.

## 7. Lo que NO debes hacer

- **No implementes crear la experiencia**, ni IA, banco, diagnóstico o
  reporte.
- **No toques el frontend** (encargo 04).
- **No edites `data/curriculo-men/`.**
- **No subas secretos.** Actualiza `backend/.env.example` con los nombres
  de las variables nuevas, **sin valores**.

## 8. Cuándo está terminado

1. Los verificadores de `CLAUDE.md` pasan.
2. **Las 6 pruebas de la sección 7 de la guía v2** dan el resultado y el
   formato que la guía espera, contra un MySQL real. Muéstralas en el
   informe de comparación, como en septiembre.
3. `npm test` y `npm run test:e2e` pasan contra MySQL y cubren, como
   mínimo: registro → verificar → completar perfil → elegir rol; código
   vencido; reenvío antes de 30 s rechazado; 5 intentos de código;
   bloqueo de login; recuperar contraseña sin revelar si el correo
   existe; editar solo el propio perfil; `/users` con usuario normal →
   403; la tarea nocturna borrando lo que corresponde; las 4 rutas del
   catálogo con sus filtros.
4. La colección de Postman (`docs/cursos/dse-2-203453/`) incluye las 6
   pruebas de la guía v2 y las rutas nuevas.
5. `backend/README.md` explica cómo arrancarlo desde cero: base de
   datos, carga del catálogo, configuración y cómo marcar al primer
   administrador.

## 9. Cómo entregarlo

Rama **`encargo-03-backend-hasta-catalogo`** y **pull request hacia
`main`**, sin hacer merge. En la descripción, en español simple: qué
cambió (modelo, base de datos, acceso, catálogo), el resultado de las 6
pruebas de la guía, de los verificadores y de las pruebas del backend,
**qué decidiste por tu cuenta**, y qué quedó pendiente. Marca R2, R3,
R4 y R5 en `21-revision-docente-2026-10-22.md` y en `pendientes.md` (A14)
con su estado real.
