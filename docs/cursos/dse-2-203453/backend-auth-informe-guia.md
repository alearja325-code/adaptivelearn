# Backend de autenticación — comparación con la guía del docente

**Proyecto:** AdaptiveLearn V3 — curso DSE-2
**Guía de referencia:** "Guía Didáctica Completa — Implementación de JWT en NestJS con MySQL"
**Código:** `DSE-2/backend-auth/`
**Pruebas (Postman / Insomnia):** `DSE-2/entregables/backend-auth-seccion-7.postman_collection.json`
**Fecha:** 2026-09-29
**Autor:** Alejandro

---

## 1. Resumen

El backend sigue la guía sección por sección. La estructura de carpetas, los nombres de
archivos y rutas, los DTOs, la estrategia JWT, los guards, los decoradores y la
configuración son los de la guía.

**Las 5 pruebas de la sección 7 dan el resultado que espera la guía**, con el mismo
formato de respuesta. Los 2 ejemplos de la sección 6 también funcionan.

Todas las diferencias con la guía están listadas en la sección 5 de este informe, cada una
con su razón. Las razones son de 3 tipos:

1. **Especificaciones del proyecto.** Las pantallas de autenticación de AdaptiveLearn ya
   estaban diseñadas antes de este curso (metodología MODESEC, specs 17 a 22). La regla con
   más peso es que **Docente y Estudiante son 2 tablas separadas**: no hay una sola tabla de
   usuarios con un campo "role".
2. **Seguridad.** Algunas partes de la guía tienen problemas de seguridad; se describen en
   la sección 7.
3. **Versiones actuales de las herramientas.** La guía no fija versiones. NestJS 12
   genera proyectos ESM, y ahí algunas líneas de la guía no compilan o no funcionan.

Ningún cambio se hizo por gusto o por estilo.

## 2. Entorno

| Componente | Versión |
|---|---|
| Node.js | 24.11.0 |
| NestJS (`@nestjs/core`) | 12.1.0 |
| `@nestjs/jwt` / `@nestjs/passport` / `passport-jwt` | 12.0.2 / 12.0.0 / 4.0.1 |
| TypeORM / `@nestjs/typeorm` | 1.1.1 / 12.0.1 |
| Base de datos | MariaDB 10.11.14 (el curso pide MariaDB; la guía usa MySQL — mismo driver `mysql2`, mismo `type: 'mysql'`) |

## 3. Cómo ejecutar las pruebas de la sección 7

1. **Base de datos** (solo la primera vez): crear las tablas con `sql/001_esquema_auth.sql`
   y `sql/002_alineacion_guia_y_seguridad.sql`.
2. **Variables de entorno:** el `.env` tiene las mismas variables que la guía (`DB_HOST`,
   `DB_PORT`, `DB_USERNAME`, `DB_PASSWORD`, `DB_DATABASE`, `JWT_SECRET`,
   `JWT_EXPIRATION=1h`).
3. **Vaciar la base antes de cada demostración**, para que el registro no choque con un
   correo ya existente y los ids empiecen en 1:
   `mariadb -u adaptivelearn -p adaptivelearn_auth < sql/reset-datos-prueba.sql`
4. **Levantar el servidor:** `npm run start:dev`. En la terminal aparece
   `🚀 Servidor corriendo en http://localhost:3000`.
5. **Postman:** *Import* → elegir `backend-auth-seccion-7.postman_collection.json` →
   ejecutar las peticiones **en orden**. Otra opción es *Run collection*. Las pruebas 1 y 2
   guardan el token en la variable `{{token}}`, y las siguientes lo usan. Cada petición
   trae verificaciones automáticas que aparecen en la pestaña *Test Results*.
   **Insomnia:** *Import* → el mismo archivo. Las peticiones se importan, pero los scripts
   de verificación automática son propios de Postman y podrían no convertirse.

## 4. Sección 7 — comandos y resultados

Resultados obtenidos el 2026-09-29 con la base vacía. Los tokens aparecen recortados.

### Prueba 1 — Registrar un nuevo usuario

`POST http://localhost:3000/auth/register`
```json
{ "email": "usuario@example.com", "password": "Password123", "fullName": "Juan Pérez" }
```

| Esperado por la guía | Obtenido (201) |
|---|---|
| `{ "user": { "id": 1, "email": "usuario@example.com", "fullName": "Juan Pérez", "role": "user" }, "token": "eyJ..." }` | `{ "user": { "id": 1, "email": "usuario@example.com", "fullName": "Juan Pérez", "role": null, "emailVerificado": false }, "token": "eyJ..." }` |

**Diferencias:** la contraseña (D7), `role: null` (D6) y el campo `emailVerificado`
(D15). La contraseña de la guía, `password123`, se rechaza con error 400 porque no tiene
mayúscula.

### Prueba 2 — Iniciar sesión

`POST http://localhost:3000/auth/login`
```json
{ "email": "usuario@example.com", "password": "Password123" }
```
Obtenido (201): `{ "user": { "id": 1, "email": "usuario@example.com", "fullName": "Juan Pérez", "role": null, "emailVerificado": false }, "token": "eyJ..." }`

Tiene el mismo formato que el login de la guía. **Diferencias:** las mismas de la prueba 1.

### Prueba 3 — Obtener perfil (ruta protegida)

`GET http://localhost:3000/auth/profile` — header `Authorization: Bearer <token>`

Obtenido (200): `{ "user": { "id": 1, "email": "usuario@example.com", "fullName": "Juan Pérez", "role": null, "emailVerificado": false } }`

Sin token responde `401 Unauthorized`, igual que la guía.

### Prueba 4 — Crear usuario (desde módulo User)

`POST http://localhost:3000/users` — header `Authorization: Bearer <token>`
```json
{ "email": "otro@example.com", "password": "Password456", "fullName": "María García" }
```
Obtenido (201): `{ "id": 2, "email": "otro@example.com", "fullName": "María García", "role": null, "emailVerificado": false }`

**Diferencia:** la ruta **exige el token** (D11). Sin token responde 401.

### Prueba 5 — Listar todos los usuarios

`GET http://localhost:3000/users` — header `Authorization: Bearer <token>`

Obtenido (200): lista con los 2 usuarios (id 1 y 2), sin contraseñas.
**Diferencia:** la ruta exige el token (D11).

### Sección 6 — Ejemplo de guards y decoradores

| Petición | Obtenido |
|---|---|
| `GET /example/protected` con token | 200 — `{ "message": "Esta ruta está protegida", "user": {...} }` |
| `GET /example/docente` con un usuario sin rol | 403 — `RolesGuard` lo rechaza |
| `GET /example/docente` con un usuario docente | 200 — `{ "message": "Esta ruta es solo para docentes", ... }` |

## 5. Diferencias con la guía y su justificación

**Estados:** *Idéntico* = mismo código que la guía. *Adaptado* = mismo propósito, con un
cambio justificado. *Agregado* = no está en la guía. *Omitido* = está en la guía pero no
en el backend, por la razón indicada.

### 5.1 Sección 1 — Configuración inicial

| Paso de la guía | Backend | Estado | Justificación |
|---|---|---|---|
| `npm i -g @nestjs/cli` + `nest new` | `npx @nestjs/cli new` | Adaptado (D1) | En este equipo, `npm` usa el Node que trae el editor Zed; una instalación global quedaría en una carpeta que el editor reemplaza al actualizarse. `npx` ejecuta la misma herramienta sin instalarla. El resultado es el mismo. |
| Dependencias | Todas las de la guía | Idéntico | — |

### 5.2 Sección 2 — Base de datos

| Paso de la guía | Backend | Estado | Justificación |
|---|---|---|---|
| `.env` con 7 variables | Las mismas 7, con los mismos nombres | Idéntico | — |
| `ConfigModule.forRoot(...)` | Igual | Idéntico | — |
| `type: 'mysql'` | Igual, conectado a MariaDB | Idéntico | MariaDB es compatible con el driver `mysql2`. Es la base que pide el curso. |
| `entities: [__dirname + '/**/*.entity{.ts,.js}']` | `import.meta.dirname + '/**/*.entity{.ts,.js}'` | Adaptado (D2) | NestJS 12 genera proyectos ESM, donde `__dirname` **no existe** (verificado: `typeof __dirname` da `undefined`). `import.meta.dirname` es su equivalente directo. |
| `synchronize: true` | `synchronize: false` + scripts `sql/001` y `sql/002` | Adaptado (D4) | Las tablas siguen un modelo relacional ya diseñado y aprobado (MODESEC, fase 3), que incluye una restricción `CHECK`. `synchronize` podría modificarlas por su cuenta. La guía misma advierte que `synchronize` es "solo en desarrollo" y recomienda migraciones. |

### 5.3 Sección 3 — Módulo User

| Paso de la guía | Backend | Estado | Justificación |
|---|---|---|---|
| Tabla `users` con columna `role` | Entidad `User` sobre la tabla `credencial`, sin columna `role`, más las tablas `docente` y `estudiante` | Adaptado (D5) | La spec 20 exige que Docente y Estudiante sean **2 tablas separadas**, no una tabla con un campo de rol. `User` representa la cuenta con la que se inicia sesión (correo y contraseña). El rol se deduce de cuál de las 2 tablas tiene la fila de esa persona. Las propiedades de la guía conservan su nombre: `id`, `email`, `password` (con `select: false`), `fullName`, `createdAt`, `updatedAt`. |
| Columna `role` con valor por defecto `'user'` | `role` calculado; `null` hasta que la persona elige su rol | Adaptado (D6) | El modelo no tiene un rol genérico "user". El rol se elige en un paso posterior (spec 20) y después no se puede cambiar. |
| Columna `isActive` | No existe | Omitido (D9) | Ninguna spec ni ningún endpoint desactiva cuentas. Sería un campo que siempre vale `true`. |
| `CreateUserDto` (email, password de mínimo 6, fullName obligatorio) | Email; password de mínimo 8 con mayúscula y número; fullName opcional | Adaptado (D7, D8) | La spec 17 fija la regla de contraseña. La pantalla de registro (spec 17) no pide el nombre: se pide en la spec 19. |
| `UpdateUserDto` (todo opcional, más `isActive` y `role`) | Solo `nombres`, `apellidos` y `avatarUrl` | Adaptado (D10) | Son los datos de "Completa tu perfil" (spec 19). **No incluye `role`**, porque el rol no se cambia nunca (spec 20); en la guía, cualquiera podría cambiarlo (ver sección 7). |
| `UserService`: `create`, `findAll`, `findOne`, `findOneByEmail`, `update`, `remove` | Los mismos, salvo `remove` | Adaptado | `remove` se omite: ninguna spec define borrar cuentas, y el modelo relacional usa `RESTRICT` sobre Docente y Estudiante. |
| `UserController`: POST, GET, GET `:id`, PATCH `:id`, DELETE `:id`, sin protección | POST, GET, GET `:id`, PATCH `:id`, todas con `JwtAuthGuard`; en PATCH, solo la propia cuenta; sin DELETE | Adaptado (D11) | En la guía estas rutas no tienen ninguna protección (ver sección 7). Por eso las pruebas 4 y 5 llevan el header `Authorization`. |
| `UserModule` que exporta `UserService` | Igual | Idéntico | — |

### 5.4 Sección 4 — Módulo Auth

| Paso de la guía | Backend | Estado | Justificación |
|---|---|---|---|
| `LoginDto` | Igual, con los mismos mensajes | Idéntico | — |
| `RegisterDto` | Igual que `CreateUserDto` (como en la guía) | Adaptado (D7, D8) | Igual que en `CreateUserDto`. |
| `JwtPayload { sub, email, role }` | `{ sub, email, role }`, con `role` que puede ser `null` | Adaptado (D6) | — |
| `JwtStrategy` busca al usuario en la base en cada petición | Igual | Adaptado (D12) | (a) `getOrThrow('JWT_SECRET')` en vez de `get`: con los tipos actuales de `passport-jwt`, la línea de la guía **no compila**; además impide arrancar el servidor sin secreto. (b) Si el usuario no existe responde 401: en la guía, `findOne` lanza 404, que no es la respuesta correcta para un token inválido. (c) Rechaza el token de recuperación de contraseña (D17). (d) Sin la revisión de `isActive` (D9). |
| `register` crea el usuario y devuelve `{user, token}` | Igual, y además genera el código de verificación de correo | Adaptado (D17) | La spec 18 exige verificar el correo. En modo desarrollo, el código se imprime en la terminal del servidor. |
| `login` con los mensajes "Credenciales inválidas" y "Usuario inactivo" | Mensaje "Correo o contraseña incorrectos." y límite de 5 intentos | Adaptado (D13) | El mensaje es el que fija la spec 17. Se quitó "Usuario inactivo" porque revela que la cuenta existe sin conocer la contraseña. Tras 5 intentos fallidos, la cuenta se bloquea 15 minutos; la propia guía lo lista en "Próximos pasos recomendados". |
| `generateToken` | Igual | Idéntico | — |
| `validateToken` | No existe | Omitido (D14) | En la guía ningún archivo lo llama: es código que nunca se ejecuta. |
| `AuthController`: `/auth/register`, `/auth/login`, `/auth/profile` | Las mismas 3 rutas | Idéntico | Se agregan 6 rutas (ver sección 6). |
| `AuthModule` con `JwtModule.registerAsync` y `JWT_EXPIRATION` | Igual | Idéntico | Importa además `DocentesModule` y `EstudiantesModule`, que se usan al elegir el rol. |

### 5.5 Sección 5 — `ValidationPipe`

| Paso de la guía | Backend | Estado |
|---|---|---|
| `ValidationPipe({ whitelist, forbidNonWhitelisted, transform })` | Igual | Idéntico |
| `app.enableCors()` | Igual | Idéntico |
| `app.listen(3000)` + mensaje en consola | Igual | Idéntico |

### 5.6 Sección 6 — Guards y decoradores

| Archivo de la guía | Estado | Justificación |
|---|---|---|
| `jwt-auth.guard.ts` | Idéntico | — |
| `roles.guard.ts` | Idéntico | — |
| `roles.decorator.ts` | Idéntico | — |
| `get-user.decorator.ts` | Idéntico | — |
| `ExampleController`, con `@Roles('admin')` | Adaptado (D16) | Usa `@Roles('docente')`: el modelo no tiene rol "admin", solo docente y estudiante (spec 20). |

### 5.7 Estructura de carpetas

```
src/
├── auth/
│   ├── decorators/  get-user.decorator.ts, roles.decorator.ts          ← guía
│   ├── dto/         login.dto.ts, register.dto.ts                       ← guía
│   │                + reenviar-codigo, verificar-correo, elegir-rol,
│   │                  solicitar-recuperacion, verificar-recuperacion,
│   │                  nueva-contrasena, password.constants              ← specs 17-22
│   ├── guards/      jwt-auth.guard.ts, roles.guard.ts                   ← guía
│   │                + recuperacion.guard.ts                             ← specs 21-22
│   ├── interfaces/  jwt-payload.interface.ts                            ← guía
│   │                + recuperacion-payload.interface.ts                 ← specs 21-22
│   ├── strategies/  jwt.strategy.ts                                     ← guía
│   └── auth.controller.ts, auth.module.ts, auth.service.ts              ← guía
├── user/
│   ├── dto/         create-user.dto.ts, update-user.dto.ts              ← guía
│   ├── entities/    user.entity.ts                                      ← guía
│   │                + user.entity.spec.ts (prueba unitaria)
│   └── user.controller.ts, user.module.ts, user.service.ts              ← guía
├── docentes/        + entidad, módulo y service                         ← spec 20
├── estudiantes/     + entidad, módulo y service                         ← spec 20
├── example.controller.ts                                                ← guía, sección 6
├── app.module.ts                                                        ← guía
└── main.ts                                                              ← guía
sql/                 + 001, 002 y reset-datos-prueba                     ← D4
```

Todos los archivos de la estructura de la guía existen, con el mismo nombre y en el mismo
lugar. Lo marcado con `+` se agrega por las specs.

En la raíz hay además `README.md`, `test/`, `vitest.config*.ts`, `oxlint.json` y
`tsconfig.build.json`. Los genera `nest new`; el árbol de la guía simplemente no los
muestra.

### 5.8 Otras diferencias menores

- **D2 — imports terminados en `.js`:** en un proyecto ESM, los imports entre archivos
  propios deben terminar en `.js` aunque el archivo sea `.ts` (por ejemplo,
  `'./auth.service.js'`). Es mecánico y no cambia la lógica.
- **D15 — campo `emailVerificado` en el usuario:** el frontend lo necesita para saber si
  falta verificar el correo (spec 18).
- **D18 — `toJSON()` en la entidad `User`:** controla qué campos aparecen en las respuestas.
  La guía usa `select: false` en la contraseña. Esta entidad tiene más campos internos
  (código de verificación, contadores de intentos, bloqueo), y ninguno debe salir en una
  respuesta. Hay una prueba unitaria que lo verifica.
- **`@Request() req` con tipo:** con el modo estricto de TypeScript, el parámetro sin tipo
  de la guía no compila.
- **`@nestjs/mapped-types`:** la guía la usa en `UpdateUserDto` sin incluirla en su lista de
  instalación. Está instalada, pero no se usa, porque `UpdateUserDto` no hereda de
  `CreateUserDto` (D10).

## 6. Funciones agregadas (specs 17 a 22)

La autenticación en sí (registro, login, perfil y rutas protegidas) funciona igual que en
la guía. Configurar la cuenta es un paso **posterior**, que se hace con la sesión ya
iniciada. Por eso las pruebas de la sección 7 no dependen de ningún paso extra.

| Ruta | Spec | Qué hace |
|---|---|---|
| `POST /auth/verificar-correo` (con token) | 18 | Verifica el correo con el código de 6 dígitos |
| `POST /auth/reenviar-codigo` | 18 | Reenvía el código; se puede pedir cada 30 s como mínimo |
| `PATCH /users/:id` (con token) | 19 | Completa el perfil (nombres, apellidos, avatar) |
| `POST /auth/elegir-rol` (con token) | 20 | Crea la fila en `docente` o en `estudiante`. Una sola vez; exige el correo verificado y el perfil completo |
| `POST /auth/recuperar-contrasena` | 21 | Envía el código de recuperación. **Responde igual exista o no la cuenta** |
| `POST /auth/recuperar-contrasena/verificar` | 18 | Valida el código y entrega un token de 15 min que solo sirve para el paso siguiente |
| `POST /auth/nueva-contrasena` (con token de recuperación) | 22 | Guarda la contraseña nueva |

**D17 — token de recuperación:** quien recupera su contraseña no tiene sesión iniciada. Por
eso existe un token aparte, de 15 minutos. Ese token solo sirve en `nueva-contrasena`: no
abre rutas protegidas, y un token de sesión normal no sirve en `nueva-contrasena`. Las 2
cosas están probadas.

Al final de la guía hay una lista de **"Próximos pasos recomendados"**. Su estado en este
backend:

| Próximo paso de la guía | Estado |
|---|---|
| Implementar recuperación de contraseña | Hecho (specs 21-22) |
| Agregar verificación de email | Hecho (spec 18) |
| Agregar límite de intentos de login | Hecho (5 intentos, bloqueo de 15 min) |
| Configurar migraciones | Parcial: scripts SQL versionados (`sql/001`, `sql/002`), no migraciones de TypeORM |
| Implementar refresh tokens | Pendiente |
| Implementar logout con lista negra de tokens | Pendiente |

## 7. Problemas de seguridad de la guía que se corrigieron

Estos puntos explican por qué no se copió la guía literalmente en esas partes:

1. **Cualquiera puede darse permisos de administrador.** Las rutas `/users` no tienen guard,
   y `UpdateUserDto` acepta `role`. Un `PATCH /users/1` con `{"role":"admin"}`, sin
   iniciar sesión, cambia el rol. Aquí `/users` exige token, `PATCH` solo modifica la cuenta
   propia, y el campo `role` se rechaza con error 400 (probado).
2. **Cualquiera puede listar o borrar todas las cuentas** con `GET /users` o
   `DELETE /users/:id`, sin autenticarse. Aquí la lista exige token y `DELETE` no existe.
3. **`POST /users` crea cuentas sin pasar por el registro.** Aquí exige token, y la cuenta
   creada igual debe verificar su correo antes de elegir rol.
4. **El login dice "Usuario inactivo" antes de revisar la contraseña**, lo que confirma a
   un desconocido que la cuenta existe. Aquí todos los fallos dan el mismo mensaje.
5. **`remove()` dice "soft delete" en su comentario, pero borra de verdad.**
6. **Si el usuario de un token no existe, `JwtStrategy` responde 404**, cuando lo correcto
   es 401.

Además se agregó lo siguiente, que la guía no trae:
- **Límite de 5 intentos por código de verificación.** Sin límite, se pueden probar
  1.000.000 de combinaciones durante los 10 minutos de validez.
- **Códigos generados con `crypto`, no con `Math.random`.**

## 8. Verificación realizada

- `npm run build`: compila sin errores.
- `npm test`: 7 pruebas unitarias pasan. Verifican que el usuario nunca expone contraseña,
  códigos ni contadores al convertirse en respuesta, que el rol se deduce bien, y la regla
  de contraseña.
- Linter (`oxlint`): 0 advertencias.
- **Colección de Postman:** se ejecutaron sus 7 peticiones contra el servidor real y las 7
  dieron el código esperado.
- **Pruebas manuales adicionales**, todas con el resultado esperado:
  - El flujo completo: verificar correo → perfil → rol → ruta de docente.
  - Los límites de intentos: el código correcto o la contraseña correcta se rechazan
    después de 5 fallos.
  - La recuperación de contraseña: la contraseña vieja deja de funcionar y la nueva
    funciona.
  - Que el token de recuperación y el token de sesión no se puedan intercambiar.
  - Que las rutas protegidas respondan 401 sin token.
  - Que no se pueda modificar una cuenta ajena.
  - Que no se pueda enviar el campo `role`.
  - Que el token dure exactamente 3600 s con `JWT_EXPIRATION=1h`.

## 9. Pendientes conocidos

- **Login con Google y Microsoft:** decidido para esta entrega, todavía no implementado.
  Requiere crear las aplicaciones OAuth en Google Cloud y en Azure.
- **Subida real del avatar** (JPG/PNG de hasta 5 MB): hoy se acepta una URL.
- **Envío real del correo:** hoy el código se imprime en la terminal del servidor (modo
  desarrollo).
- **Mensaje para "demasiados intentos":** ninguna spec lo define, así que se usa el mismo
  mensaje genérico. Hay que definirlo en el diseño.
- **Refresh tokens y logout con lista negra de tokens:** los "próximos pasos" que quedan de
  la guía.
- **Control de versiones:** el `.gitignore` del repositorio excluye toda la carpeta
  `backend-auth/`. Por eso el código no queda en git, y el linter solo se puede ejecutar
  desde una copia fuera del repositorio.
- **Registrar como ADR** en `diseno/decisiones.md` 2 decisiones: la tabla `credencial`, y
  separar la autenticación de la configuración de la cuenta.
