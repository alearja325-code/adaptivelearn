# Backend — AdaptiveLearn

API del sistema, en **NestJS 12** con **MySQL 8** (exigencia del curso DSE-2, RNF-14).

## Estado

Hecho hasta el **catálogo curricular** (encargo 03, 2026-10-27):

- **El acceso completo** (incremento I1, `20-catalogo-endpoints.md` §3, E-01 a E-12):
  registro, verificación del correo con un código de 6 dígitos que llega por correo,
  completar el perfil y elegir el rol, inicio de sesión, recuperar la contraseña, editar el
  propio perfil, y entrar con Google o Microsoft (cuando se configuren).
- **El catálogo curricular** (E-14 a E-17): áreas, grados, DBA y evidencias, de solo
  lectura, para la sesión de un docente. Desde el encargo 05 (2026-11-10), cada DBA trae su
  ejemplo y la marca de si incluye una imagen (`ejemploTieneImagen`), y cada evidencia, el
  dictamen del censo de formato cerrado (`admiteFormatoCerrado`, `formato`).
- **Las rutas de la guía del docente** (`/users` para administrador y `/example/*`), que el
  curso evalúa (ADR-040).

Todavía no existe nada de crear experiencias, banco de preguntas, IA, diagnóstico ni reporte.

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

### 5. Marcar al primer administrador

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
- Decisiones: ADR-034 a ADR-040 en `docs/diseno/decisiones.md`.
