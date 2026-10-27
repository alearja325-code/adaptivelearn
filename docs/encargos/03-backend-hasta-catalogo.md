# Encargo 03 — Backend: acceso corregido y base de datos hasta el catálogo

**Para:** una sesión de Claude Code sobre este repositorio.
**Escrito:** 2026-10-26, desde la sesión local de Alejandro. **Antes de
empezar, lee `CLAUDE.md`, `docs/diseno/pendientes.md` (A14 y A16) y
`docs/modesec/fase-3-diseno-computacional/21-revision-docente-2026-10-22.md`.**
**Hazlo después de que el encargo 02 esté unido a `main`.**

## 1. Qué hay que lograr

Que el backend (`backend/`, NestJS + MySQL) implemente **el modelo final
hasta el catálogo curricular**, con **todas las correcciones del
docente** del 2026-10-22, y exponga las rutas que necesitan las
pantallas **desde el acceso hasta el Paso 3 de "Crear experiencia"**,
**sin crear la experiencia** (eso dispara la IA y es otra etapa).

## 2. Parte A — Primero, el modelo (ADR-039)

En la fuente del MER y del MR, y regenerando todo (cadena de
`19-entrega-fase-3.md` §3):

- Entidad nueva **CODIGO_VERIFICACION**: el código, su propósito
  (`verificar_correo` o `recuperar_contrasena`), `creado_en`,
  `intentos`, ligada a su credencial; a lo sumo un código vigente por
  credencial y propósito.
- **CREDENCIAL pierde** `codigo_verificacion`, `codigo_expira_en` y
  `codigo_ultimo_envio`. Mueve también a la tabla nueva los intentos del
  código, que hoy viven en la credencial (`intentos_codigo`, en el MR).
- Agrega a las tablas de "qué cambió" (`16` §13, `17` §10) la cita a
  ADR-039 y a la nota R4 del docente.
- Todos los verificadores de `CLAUDE.md` deben seguir pasando.

**Regenera los PDF solo si hay Chrome o Edge; si no, dilo.**

## 3. Parte B — La base de datos del backend

- Reemplaza los scripts de `backend/sql/` por un esquema que sea **el del
  modelo relacional** (`modelo-relacional/mr_mysql.sql`) **para las
  tablas de esta etapa**: `credencial`, `docente`, `estudiante`,
  `codigo_verificacion`, `area`, `grado`, `documento_oficial`, `dba`,
  `evidencia`, `evidencia_dictamen`. Mismos nombres, tipos, llaves y
  restricciones; **no inventes diferencias**. Si el backend necesita una
  columna que el MR no tiene, agrégala primero al MR (con su razón,
  como ya están `intentos_login` y `bloqueado_hasta`) y después al
  backend.
- **Datos de referencia**, cargados por script: las 4 áreas, los 11
  grados con su nivel y los 4 documentos oficiales, **con los valores de
  ADR-036 y de la tabla de ADR-033** (Ciencias Sociales es **V.1**).
- **DBA y evidencias**, cargados desde
  `data/curriculo-men/catalogo/catalogo_dba.json` (encargo 02). **No
  desde el JSON viejo.** Los DBA marcados como "dudosos" en el informe
  del encargo 02: decláralos, no los inventes.
- `evidencia_dictamen` queda sin filas: el censo QA-014 está pendiente.
  Si una ruta lo necesita, decláralo.

## 4. Parte C — El acceso, con las correcciones del docente

Guíate por `20-catalogo-endpoints.md`, sección 3 (E-01 a E-13) y
sección 7.

- **R2 — sin "usuario" genérico.** Quita la entidad `User`, el módulo
  `user/`, las rutas `/users` y `/example/*`, y las columnas
  `nombre_completo`, `nombres`, `apellidos` y `avatar_url` de la
  credencial (viven en docente y estudiante). El sistema trabaja con
  **credencial + docente / estudiante**; la sesión (JWT) identifica el
  rol y el `id_docente` o `id_estudiante`. Editar el perfil (E-12) deja
  de ser `PATCH /users/:id`: ponle la ruta que proponga `20` §3, o una
  bajo `/auth/` si `20` no la fija, y decláralo.
- **R3** — `estado_verificacion` (`procesando` / `verificado`), ADR-037.
- **R4** — los códigos en `codigo_verificacion`; el vencimiento (10 min)
  y la espera para reenviar (30 s) se **calculan** desde `creado_en`
  (ADR-039). Conserva los 5 intentos por código, y el bloqueo de 15
  minutos tras 5 intentos fallidos de inicio de sesión. **Guarda el
  código con hash**, no en texto legible.
- **Tarea nocturna** (ADR-039): con `@nestjs/schedule`, a las 3:00 a. m.
  por defecto, borra los códigos vencidos y las credenciales con más de
  7 días en `procesando` sin rol. Hora y días, configurables en `.env`.
- **R5 — envío real de correos.** Hoy el backend **no envía ningún
  correo**. Implementa el envío de los códigos (registro y
  recuperación) por SMTP, con la configuración en `.env`
  (`MAIL_HOST`, `MAIL_PORT`, `MAIL_USER`, `MAIL_PASSWORD`, `MAIL_FROM`).
  El remitente es la cuenta del sistema, `adaptivelearn@…`, que crea el
  equipo. **Si no hay configuración de correo, en desarrollo escribe el
  código en la consola** y dilo claramente al arrancar. Nunca escribas
  una clave en el código ni en el repositorio.
- **Google y Microsoft (E-04, E-05):** impleméntalos con su
  configuración en `.env` (identificadores de la aplicación de cada
  proveedor, que el equipo todavía no tiene). Sin configuración, que
  respondan un error claro de "no configurado". Pruébalos con un
  proveedor simulado.
- **Registro a medias** (ADR-035): quien no eligió rol y vuelve a
  entrar, retoma en completar perfil.

## 5. Parte D — Las rutas del catálogo

- **E-14** `GET /catalogo/dbas` y **E-15** `GET /catalogo/dbas/:codigo`,
  como los define `20` §4.1, filtrando por `codigo_area` y
  `numero_grado`.
- **Dos rutas nuevas** que `20` no tiene y las pantallas necesitan:
  **`GET /catalogo/areas`** (Paso 1 muestra las 4 áreas) y
  **`GET /catalogo/grados`** (el filtro de grado del Paso 2). Agrégalas a
  `api/datos_api.py`, regenera `20` y decláralas.
- Solo lectura; solo para la sesión de un docente.

## 6. Lo que NO debes hacer

- **No implementes crear la experiencia** ni nada de la IA, el banco,
  el diagnóstico o el reporte.
- **No toques el frontend** (es el encargo 04).
- **No edites los datos de `data/curriculo-men/`.**
- **No subas secretos.** Actualiza `backend/.env.example` con los
  nombres de las variables nuevas, **sin valores**.

## 7. Cuándo está terminado

1. Los verificadores de `CLAUDE.md` pasan.
2. Las pruebas del backend (`npm test` y `npm run test:e2e`) pasan
   contra un MySQL real, y cubren como mínimo: registro → verificar
   código → completar perfil → elegir rol; código vencido; reenvío antes
   de 30 s rechazado; 5 intentos de código; bloqueo de inicio de sesión;
   recuperar contraseña sin revelar si el correo existe; editar perfil
   solo el propio; la tarea nocturna borrando lo que corresponde; las 4
   rutas del catálogo con sus filtros; y que `/users` ya no existe.
3. La colección de Postman de `docs/cursos/dse-2-203453/` se actualiza a
   las rutas nuevas, o se declara cuáles quedaron obsoletas.
4. `backend/README.md` explica cómo arrancarlo desde cero: base de
   datos, carga del catálogo y configuración.

## 8. Cómo entregarlo

Rama **`encargo-03-backend-hasta-catalogo`** y **pull request hacia
`main`**, sin hacer merge. En la descripción, en español simple: qué
cambió (modelo, base de datos, acceso, catálogo), los resultados de los
verificadores y de las pruebas, **qué decidiste por tu cuenta** y qué
quedó pendiente. Marca R2, R3, R4 y R5 en
`21-revision-docente-2026-10-22.md` y en `pendientes.md` (A14) con el
estado real.
