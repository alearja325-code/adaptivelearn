# Backend — AdaptiveLearn

API del sistema, en **NestJS 12** con **MySQL 8** (exigencia del curso DSE-2, RNF-14).

## Estado

**Terminado** (2026-11-17): los cuatro incrementos del sistema, con **37 de los 38 endpoints**
del diseño (`docs/modesec/fase-3-diseno-computacional/20-catalogo-endpoints.md`; el que falta,
cerrar sesión, es opcional porque la sesión es un token que el navegador olvida).

| Incremento | Qué hace | Endpoints |
|---|---|---|
| **I1 — Acceso** | Registro, verificación del correo con un código de 6 dígitos que llega por correo, completar el perfil y elegir el rol (docente o estudiante), inicio de sesión, recuperar la contraseña, editar el propio perfil; Google y Microsoft cuando se configuren | E-01 a E-12 |
| **I2 — Catálogo** | Las 4 áreas, los 11 grados y los 343 DBA del MEN con sus 1282 evidencias, su ejemplo y el dictamen de formato cerrado de cada evidencia, de solo lectura | E-14 a E-17 |
| **I2 — Experiencias y banco** | El docente crea una experiencia sobre un DBA y **DeepSeek genera su banco** (12 preguntas por evidencia, en segundo plano, todo o nada); el docente lo revisa (editar, descartar, volver a incluir, agregar las suyas), lo publica y obtiene el código de invitación | E-18 a E-28 y E-38 |
| **I3 — Diagnóstico** | El estudiante se une con el código y responde pregunta por pregunta, con su certeza; la **regla adaptativa** (ADR-031) decide cuándo concluye cada evidencia; puede retomar y salirse | E-29 a E-34 |
| **I4 — Reporte** | El docente ve cuántos estudiantes hay en cada estado, por evidencia y en general; los estudiantes por estado; y el historial de cada uno | E-35 a E-37 |
| **Guía del curso** | `/users` (administrador) y `/example/*`, que el curso evalúa (ADR-040) | — |

**Cómo se comprueba:** 112 pruebas unitarias y 105 de punta a punta contra MySQL real
(`npm test`, `npm run test:e2e`), incluidas las 6 de la guía del docente. Las reglas del
diagnóstico y del reporte tienen una prueba por cada caso de su decisión. La generación con
DeepSeek se probó de verdad el 2026-11-16: 4 evidencias, 48 preguntas, 114 segundos.

La forma sigue la guía del docente; el modelo de datos es el de la Fase III. Cada diferencia
con la guía está en `docs/cursos/dse-2-203453/backend-auth-informe-guia.md`.

## Arrancar desde cero

Requisitos: **Node.js 22** o más nuevo y un servidor **MySQL 8.0.16** o más nuevo (antes de
8.0.16, MySQL ignora los CHECK del esquema).

### 1. Instalar

```bash
cd backend
npm install
```

### 2. Configurar

```bash
cp .env.example .env
```

Y completar `.env` (nunca se sube al repositorio; cada integrante tiene el suyo):

| Variable | Qué poner |
|---|---|
| `DB_HOST`, `DB_PORT`, `DB_USERNAME`, `DB_PASSWORD`, `DB_DATABASE` | La conexión a MySQL. Por ejemplo `localhost`, `3306`, tu usuario, tu contraseña y `adaptivelearn`. |
| `JWT_SECRET` | Un secreto largo y al azar. Se puede generar con `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`. |
| `JWT_EXPIRATION` | Vida de la sesión, en segundos: `3600` es una hora. |
| `MAIL_HOST`, `MAIL_PORT`, `MAIL_USER`, `MAIL_PASSWORD`, `MAIL_FROM` | El correo que envía los códigos (abajo). Si se dejan vacíos, los códigos se escriben en la consola del servidor. |
| `GOOGLE_CLIENT_ID`, `MICROSOFT_CLIENT_ID` | El identificador de la aplicación en Google Cloud y en Azure. Vacíos: esas rutas responden 503 «no configurado». |
| `LIMPIEZA_CRON`, `LIMPIEZA_ZONA_HORARIA`, `LIMPIEZA_DIAS_SIN_TERMINAR` | La tarea nocturna. Vacíos: a las 3:00 a. m. de Colombia, y 7 días. |
| `UPLOADS_DIR` | Dónde se guardan las fotos de perfil. Vacío: la carpeta `uploads/` (no se sube). |
| `IA_SERVICIO` | `deepseek` (por defecto) genera el banco con DeepSeek; **`falsa`** genera preguntas fijas de prueba sin llamar a nadie: sirve para probar todo el sistema **sin clave de DeepSeek**. |
| `DEEPSEEK_API_KEY`, `DEEPSEEK_MODEL` | La clave de la cuenta de DeepSeek (**nunca se sube**) y el modelo (por defecto `deepseek-chat`). |
| `IA_TIEMPO_LIMITE_MS` | Cuánto se espera la respuesta de cada evidencia. Vacío: 180000 (3 minutos), medido en RNF-13. |
| `DB_DATABASE_PRUEBAS` | La base de las pruebas automáticas. **Se borra en cada corrida.** Vacío: el nombre de `DB_DATABASE` con `_pruebas` al final. |

**El correo del sistema (nota R5 del docente).** La cuenta es
`adaptivelearn.sistema@gmail.com`. Para Gmail: `MAIL_HOST=smtp.gmail.com`, `MAIL_PORT=587`,
`MAIL_USER=adaptivelearn.sistema@gmail.com`, y en `MAIL_PASSWORD` una **contraseña de
aplicación** de esa cuenta (Google: *Cuenta → Seguridad → Verificación en dos pasos →
Contraseñas de aplicaciones*), no la contraseña normal. La pide el equipo a quien administra
la cuenta; **nunca se escribe en el código ni se sube**.

### 3. Crear la base de datos y cargar el catálogo

```bash
npm run db:preparar
```

Hace cinco cosas, en orden:

1. Crea la base `DB_DATABASE` si no existe (`utf8mb4`).
2. Crea las tablas con **`sql/001_esquema.sql`**. Ese archivo **no se edita a mano**: lo
   genera el modelo relacional de la Fase III
   (`docs/modesec/fase-3-diseno-computacional/modelo-relacional/generar.py`), y su
   verificador comprueba que coincida. Si hace falta una columna, se agrega primero al MR.
3. Carga los datos de referencia con **`sql/002_datos_referencia.sql`**: las 4 áreas, los 11
   grados con su nivel y los 4 documentos oficiales del MEN (ADR-033, ADR-036; Ciencias
   Sociales es V.1).
4. Carga los **343 DBA y sus 1282 evidencias** desde
   `data/curriculo-men/catalogo/catalogo_dba.json` (encargo 02), con el **ejemplo** de cada DBA
   y la marca de si incluye una imagen (encargo 05). Si el catálogo no coincide con los
   documentos de 002, se detiene: no corrige nada por su cuenta.
5. Carga el **dictamen de cada evidencia** (si admite pregunta cerrada y con qué formato) en
   `evidencia_dictamen`, desde `data/curriculo-men/censo/censo_formato_cerrado.json` (censo
   QA-014, encargo 05). Es un juicio **propuesto por IA y sin validar** (ADR-042). Si el censo
   no tiene exactamente un dictamen por evidencia, se detiene.

Algunos DBA vienen marcados como **dudosos** en el catálogo (`MAT-11-09` y `MAT-11-10`: su página
del PDF no tiene encabezado de grado; y siete ejemplos de Matemáticas con fórmulas que el PDF no
trae completas) y se cargan tal cual; el script los lista.

Si la base ya tiene tablas, el script se detiene. Para empezar de cero —**borra todo**—:
`node scripts/preparar-base.mjs --borrar`.

### 4. Arrancar

```bash
npm run start:dev
```

En la consola aparece `🚀 Servidor corriendo en http://localhost:3000`. Si el correo no está
configurado, también un aviso: *«MAIL_HOST no está configurado: los códigos NO se envían
por correo; se escriben en esta consola»*. Ahí aparece cada código.

**Probar la API desde el navegador:** abre **http://localhost:3000/docs** (Swagger). Las rutas
están agrupadas por incremento (I1 acceso, I2 experiencias y banco, I3 diagnóstico, I4
reporte). Para las que piden sesión: ejecuta `POST /auth/login`, copia el `token` de la
respuesta, pulsa **Authorize** y pégalo. La especificación OpenAPI está en `/docs-json`
(se puede importar en Insomnia o Postman).

### 5. Recorrido para probarlo todo en Swagger

Con el servidor encendido, en **http://localhost:3000/docs**. Sin clave de DeepSeek, arrancar
con `IA_SERVICIO=falsa` en `.env`. Los códigos de verificación salen en la consola si el correo
no está configurado.

1. **Docente:** `POST /auth/register` → `POST /auth/verificar-correo` (con el código) →
   `POST /auth/elegir-rol` con `role: docente`. Copiar el `token` de la respuesta en **Authorize**.
2. **Catálogo:** `GET /catalogo/dbas?codigo_area=MAT&numero_grado=1` y
   `GET /catalogo/dbas/MAT-01-04`: sus evidencias, cuáles admiten pregunta cerrada y con qué
   formato.
3. **Crear la experiencia:** `POST /experiencias` con `{"codigo_dba": "MAT-01-04", "nombre":
   "Medición 1.°"}` responde `202` con el id de la generación. Repetir
   `GET /experiencias/generaciones/{id}` hasta que diga `lista` (con DeepSeek, unos 2 minutos).
4. **Revisar y publicar:** `GET /experiencias/{id}/banco` → `POST /experiencias/{id}/publicar`
   → `GET /experiencias/{id}/codigo`: el código de invitación.
5. **Estudiante** (otro correo, `role: estudiante`, su propio token en Authorize):
   `POST /inscripciones` con el código → `POST /inscripciones/{id}/presentaciones` (la
   pregunta) → `POST /inscripciones/{id}/respuestas` (las opciones y la certeza de 0 a 5).
   Repetir hasta que `presentaciones` responda `"pregunta": null`: el diagnóstico concluyó.
   El estudiante nunca recibe si acertó ni cómo va (ADR-028).
6. **Reporte** (de nuevo con el token del docente): `GET /experiencias/{id}/reporte`,
   `GET /experiencias/{id}/estudiantes` y `GET /inscripciones/{id}/historial`.

### 6. Marcar al primer administrador

Las rutas `/users` son solo para administrador, como en la guía del docente. **Ninguna ruta
da ese permiso**: se pone en MySQL, sobre una cuenta ya registrada, y después esa persona
vuelve a iniciar sesión:

```sql
UPDATE credencial SET es_admin = 1 WHERE correo = 'correo-de-la-persona@example.com';
```

Es la prueba 4 de la guía (que dice `UPDATE users SET role = 'admin'`: aquí la tabla es
`credencial` y la marca, `es_admin`). El producto no usa administradores: ninguna pantalla
llama a `/users`.

## Comandos

| Comando | Qué hace |
|---|---|
| `npm run start:dev` | Arranca y se reinicia solo al guardar cambios |
| `npm run build` | Compila a `dist/` |
| `npm run db:preparar` | Crea la base y carga el catálogo y el censo (paso 3) |
| `npm test` | Pruebas unitarias |
| `npm run test:e2e` | Pruebas de punta a punta **contra MySQL**: crea `DB_DATABASE_PRUEBAS` desde cero con el mismo script del paso 3 |
| `npm run pruebas:guia` | Con el servidor encendido: las 6 pruebas de la sección 7 de la guía y su tabla de respuestas. **Borra las cuentas** de la base de desarrollo (`sql/borrar-cuentas.sql`) para que los ids empiecen en 1 |
| `npm run lint` | Revisión de estilo (oxlint) |

La colección de Postman con las pruebas de la guía y las rutas propias está en
`docs/cursos/dse-2-203453/backend-auth-seccion-7.postman_collection.json`.

## Qué hay en cada carpeta

```
src/
  auth/        registro, sesión, códigos, recuperación, perfil, Google y Microsoft
  user/        la cuenta (tabla credencial), docente y estudiante; /users (admin)
  catalogo/    áreas, grados, DBA y evidencias (solo lectura)
  banco/       experiencias, banco de preguntas, generación con IA (DeepSeek o la falsa)
  diagnostico/ inscripciones, la siguiente pregunta, las respuestas y la regla adaptativa
  reporte/     el reporte, los estudiantes por estado y el historial
  correo/      el envío de los códigos por SMTP (o a la consola)
  limpieza/    la tarea nocturna (ADR-039)
  example/     los ejemplos de guards de la guía
sql/           001 (generado del MR), 002 (datos de referencia), borrar-cuentas
scripts/       preparar-base.mjs, pruebas-guia-seccion-7.mjs
test/          pruebas de punta a punta
```

## Reglas que conviene saber

- **El código de verificación** vence a los 10 minutos, se puede reenviar a los 30 segundos
  y admite 5 intentos fallidos. Se guarda con HMAC (usa `JWT_SECRET` como clave: si se
  cambia el secreto, los códigos pendientes dejan de servir, y también las sesiones).
- **La tarea nocturna** borra los códigos vencidos y las cuentas que llevan más de 7 días en
  `procesando` (nunca verificaron el correo) sin rol.
- **Inicio de sesión:** 5 contraseñas incorrectas bloquean la cuenta 15 minutos.
- **Hora:** el servidor y MySQL deben estar en la misma zona horaria (lo normal, en la misma
  máquina): las fechas de los códigos las pone el servidor y la de creación de la cuenta, MySQL.

## Seguridad

- **El archivo `.env` nunca se sube** (está en `.gitignore`). `.env.example` lista las
  variables, sin valores.
- Las contraseñas se guardan con bcrypt y los códigos con HMAC: nunca en texto legible (RNF-08).
- La contraseña nunca sale en una respuesta (`@Exclude()` y el serializador global).

## Documentación relacionada

- Comparación con la guía del docente y resultados de sus pruebas:
  `docs/cursos/dse-2-203453/backend-auth-informe-guia.md`.
- Endpoints: `docs/modesec/fase-3-diseno-computacional/20-catalogo-endpoints.md`.
- Modelo de datos: `docs/modesec/fase-3-diseno-computacional/17-modelo-relacional.md`.
- Decisiones: `docs/diseno/decisiones.md` (las del backend: ADR-034 a ADR-045; las reglas del
  diagnóstico y del reporte: ADR-016, ADR-022, ADR-031 y ADR-032).
- El texto que se envía a la IA y por qué: `docs/diseno/instrucciones-ia-banco.md`.
