# Backend de autenticación — comparación con la guía del docente (versión 2)

**Proyecto:** AdaptiveLearn — curso DSE-2
**Guía de referencia:** "Implementación de JWT en NestJS con MySQL (versión corregida)",
`guia-docente/guia-jwt-nestjs-v2-2026-10.txt`
**Código:** `backend/` del repositorio
**Pruebas:** `backend-auth-seccion-7.postman_collection.json` (Postman) y
`backend/scripts/pruebas-guia-seccion-7.mjs` (las mismas 6 pruebas, desde la terminal)
**Fecha:** 2026-10-27 (encargo 03). Reemplaza al informe del 2026-09-29, que comparaba
contra la primera versión de la guía; ese queda en el historial de git.

---

## 1. Resumen

La regla es la de **ADR-040: la guía manda en la forma; AdaptiveLearn manda en el fondo.**

- **De la guía:** las carpetas y los módulos (`user/`, `auth/`, `example/`), los nombres de
  archivos, las rutas (`/auth/register`, `/auth/login`, `/auth/profile`, `/users`,
  `/example/*`), los guards, los decoradores, el `ValidationPipe` y el
  `ClassSerializerInterceptor` globales, `@Exclude()` en la contraseña, y las respuestas:
  401 sin sesión, 403 sin permiso, 409 correo repetido, 400 datos inválidos, 404 no
  existe, **200 en login** y **204 al borrar**. `/users` es solo para administrador.
- **De AdaptiveLearn:** debajo, el modelo de la Fase III. La cuenta es la tabla
  `credencial` (ADR-034), Docente y Estudiante son tablas separadas, el correo tiene un
  estado de verificación (ADR-037) y los códigos viven en su propia tabla (ADR-039).

**Las 6 pruebas de la sección 7 dan el resultado y el formato que la guía espera**, contra
MySQL 8.0.46 real (sección 4). La única diferencia visible es la contraseña de los
ejemplos: la de la guía no tiene mayúscula, y la regla de AdaptiveLearn la exige (D-04).
La tabla de respuestas esperadas de la guía también se cumple completa.

Cada diferencia con la guía está en la sección 5, con su razón. Las razones son de tres
tipos: **el modelo de AdaptiveLearn** (la Fase III y las decisiones del equipo), **la
seguridad** y **las versiones actuales de las herramientas** (NestJS 12 genera proyectos
ESM).

## 2. Entorno

| Componente | Versión |
|---|---|
| Node.js | 22.22.0 |
| NestJS (`@nestjs/core`) | 12.1.0 |
| `@nestjs/jwt` / `@nestjs/passport` / `passport-jwt` | 12.0.2 / 12.0.0 / 4.0.1 |
| TypeORM / `@nestjs/typeorm` / `mysql2` | 1.1.1 / 12.0.1 / 3.24.4 |
| `class-validator` / `class-transformer` | 0.15.1 / 0.5.1 |
| Agregadas por AdaptiveLearn | `@nestjs/schedule` 12.0.2 (tarea nocturna), `nodemailer` 10.2.1 (correo), `jose` 6.2.13 (Google y Microsoft) |
| Base de datos | **MySQL 8.0.46** (la guía usa MySQL; el informe de septiembre usó MariaDB 10.11) |

## 3. Cómo repetir las pruebas

Todo está en `backend/README.md`. En corto:

1. `cd backend && npm install`, y copiar `.env.example` a `.env` con los datos de MySQL.
2. `npm run db:preparar`: crea la base con el esquema del modelo relacional y carga el
   catálogo (la guía, en cambio, crea las tablas con `synchronize`: D-02).
3. `npm run start:dev`.
4. **Postman:** *Import* → `backend-auth-seccion-7.postman_collection.json` → ejecutar la
   carpeta «Sección 7 de la guía v2» **en orden**. La prueba 4 es una sentencia SQL: la
   colección la muestra en su descripción y hay que correrla en MySQL antes de seguir.
   **Desde la terminal:** `node scripts/pruebas-guia-seccion-7.mjs` corre las 6 pruebas
   —incluida la sentencia SQL— y la tabla de respuestas esperadas, y dice si cada
   respuesta es la esperada. Antes vacía las cuentas (`sql/borrar-cuentas.sql`) para que
   los ids empiecen en 1, como en la guía.

## 4. Sección 7 — resultados

Corridas el 2026-10-27 contra el servidor real, con la base vacía. La salida completa,
petición por petición, está en `salida-pruebas-guia-v2.txt`. Los tokens aparecen recortados.

### Prueba 1 — Registrar un nuevo usuario

`POST /auth/register` con
`{ "email": "usuario@example.com", "password": "Password123", "fullName": "Juan Pérez" }`

| Esperado por la guía (201) | Obtenido (201) |
|---|---|
| `{ "user": { "id": 1, "email": "usuario@example.com", "fullName": "Juan Pérez", "role": "user" }, "token": "eyJ..." }` | `{ "user": { "id": 1, "email": "usuario@example.com", "fullName": "Juan Pérez", "role": "user" }, "token": "eyJhbGciOiJIUzI1NiIs…" }` |

**Igual a la guía**, salvo la contraseña de la petición: con la de la guía, `password123`,
el registro responde **400** «Mínimo 8 caracteres, con una mayúscula y un número.» (D-04).
Además, el servidor envía el código para verificar el correo (D-12).

### Prueba 2 — Iniciar sesión

`POST /auth/login` con `{ "email": "usuario@example.com", "password": "Password123" }`

Obtenido: **200**, `{ "user": { "id": 1, "email": "usuario@example.com", "fullName": "Juan Pérez", "role": "user" }, "token": "eyJ…" }`. Igual a la guía.

### Prueba 3 — Obtener perfil (ruta protegida)

`GET /auth/profile` con `Authorization: Bearer <token>`

Obtenido: **200**, `{ "user": { "id": 1, "email": "usuario@example.com", "proveedor": "correo", "estadoVerificacion": "procesando", "idDocente": null, "idEstudiante": null, "createdAt": "…", "updatedAt": "…", "role": "user", "perfil": null, "fullName": "Juan Pérez" } }`.

Mismo formato que la guía (`{ user }`, la entidad serializada, sin contraseña). Los campos
son los de la credencial de AdaptiveLearn en vez de `isActive` (D-05, D-07).

### Prueba 4 — Convertir un usuario en administrador

| Guía | AdaptiveLearn |
|---|---|
| `UPDATE users SET role = 'admin' WHERE email = 'usuario@example.com';` | `UPDATE credencial SET es_admin = 1 WHERE correo = 'usuario@example.com';` |

Después, `POST /auth/login` otra vez: **200**, con `"role": "admin"`. La marca de
administrador es una columna propia (D-06); como en la guía, **solo se pone por SQL**.

### Prueba 5 — Crear usuario (requiere admin)

`POST /users` con el token de admin y
`{ "email": "otro@example.com", "password": "Password456", "fullName": "María García" }`

Obtenido: **201**, `{ "id": 2, "email": "otro@example.com", …, "role": "user", "fullName": "María García" }`, sin contraseña. Igual a la guía, salvo la contraseña (`password456` → `Password456`, D-04).

### Prueba 6 — Listar todos los usuarios (requiere admin)

`GET /users` con el token de admin

Obtenido: **200**, los dos usuarios (id 1 con `"role": "admin"`, id 2 con `"role": "user"`),
sin contraseñas. Igual a la guía.

### Tabla de respuestas esperadas de la guía

| Situación | Esperado | Obtenido |
|---|---|---|
| Sin token o token expirado | 401 | **401** (`GET /users` sin token; `GET /auth/profile` con un token inválido) |
| Token válido pero rol user en /users | 403 | **403** «No tienes permisos para este recurso» |
| Email ya registrado | 409 | **409** «El email ya está registrado. Inicia sesión.» |
| Datos inválidos en el body | 400 | **400**, con un mensaje por campo |
| Usuario con ese ID no existe (admin) | 404 | **404** «Usuario con ID 999 no encontrado» |
| Borrar un usuario (admin) | 204 | **204**, sin cuerpo |

### Sección 6 — los dos ejemplos de guards

| Petición | Obtenido |
|---|---|
| `GET /example/protected` con cualquier sesión | 200 — `{ "message": "Esta ruta está protegida", "user": {…} }` |
| `GET /example/admin` con un usuario normal | 403 |
| `GET /example/admin` con el administrador | 200 — `{ "message": "Esta ruta es solo para administradores", … }` |

Las mismas pruebas, y la tabla, están también automatizadas en
`backend/test/guia-seccion-7.e2e-spec.ts` (sección 8).

## 5. Diferencias con la guía v2 y su razón

**Estados:** *Idéntico* = el código de la guía. *Adaptado* = mismo propósito, con un cambio
justificado. *Agregado* = no está en la guía. *Omitido* = está en la guía pero no aquí.

### 5.1 Configuración (secciones 1 y 2)

| Guía | Backend | Estado | Razón |
|---|---|---|---|
| `nest new` + las dependencias de la guía | Las mismas dependencias, más `@nestjs/schedule`, `nodemailer`, `jose` y `cron` | Agregado | La tarea nocturna (ADR-039), el envío de correos (nota R5) y Google/Microsoft (E-04, E-05). |
| `.env` con 7 variables | Las 7, con los mismos nombres y `JWT_EXPIRATION` en segundos; más las de correo, Google, Microsoft, tarea nocturna y fotos | Agregado | `backend/.env.example` las lista, **sin valores**. |
| `TypeOrmModule.forRootAsync` con `getOrThrow`, `autoLoadEntities` | Igual | Idéntico | — |
| `synchronize: true` | `synchronize: false`; las tablas las crea `sql/001_esquema.sql` | Adaptado (**D-02**) | Las tablas son las del **modelo relacional** de la Fase III (`17`), con sus CHECK y sus llaves compuestas. `sql/001_esquema.sql` lo **genera** el MR, y un verificador comprueba que no se aparte (`verificar_mr.py`). `synchronize` podría alterarlas por su cuenta; la propia guía dice «solo en desarrollo». |
| Imports `'./user/user.module'` | `'./user/user.module.js'` | Adaptado (**D-01**) | NestJS 12 genera proyectos ESM: los imports propios terminan en `.js`. Es mecánico. |

### 5.2 Módulo User (sección 3)

| Guía | Backend | Estado | Razón |
|---|---|---|---|
| `@Entity('users')` | `@Entity('credencial')` | Adaptado (**D-03**) | La cuenta de AdaptiveLearn es la tabla `credencial` (ADR-034): el correo es único entre los dos roles, y Docente y Estudiante son tablas aparte. Las **propiedades conservan los nombres de la guía** (`id`, `email`, `password`, `fullName`, `role`, `createdAt`, `updatedAt`); las columnas, los del MR (`id_credencial`, `correo`, `password_hash`…). |
| `password` con `@Exclude()` y `select: false` | Igual | Idéntico | — |
| `fullName`: columna obligatoria | Getter: el nombre del docente o estudiante si ya hay rol; si no, el que se escribió al registrarse (`nombre_completo`) | Adaptado (**D-07**) | En AdaptiveLearn los nombres oficiales son `nombres` y `apellidos`, de Docente o Estudiante (ventana 016). `nombre_completo` guarda el `fullName` de la guía mientras no hay rol (MR, `17` §5.7). |
| `role`: columna, `'user'` por defecto | Getter: `admin` si tiene la marca; `docente` o `estudiante` según su fila; si no, `user` | Adaptado (**D-05**) | El rol no se guarda: se deduce de las tablas, así no puede contradecirlas. `user` conserva el valor por defecto de la guía y aquí significa «registro a medias, todavía sin rol» (ADR-035). |
| Columna `isActive` | No existe | Omitido (**D-08**) | Ningún requerimiento desactiva cuentas: sería un campo que siempre vale `true`. Por eso `JwtStrategy` no lo revisa. |
| — | `estadoVerificacion`, `proveedor`, `idDocente`, `idEstudiante`, `perfil` en la respuesta | Agregado | R3 (ADR-037), RF-01-04 y la nota R2 del docente. La pantalla los necesita para saber dónde retomar. |
| `CreateUserDto`: contraseña de mínimo 6 | Mínimo 8, con una mayúscula y un número | Adaptado (**D-04**) | RF-01-01 (ventana 014). Por eso los ejemplos usan `Password123` y `Password456`. |
| `CreateUserDto`: `fullName` obligatorio | Opcional | Adaptado (**D-09**) | La ventana 014 (Crear cuenta) no pide nombre; nombres y apellidos se piden en la 016. La prueba 1 lo envía y se guarda igual. |
| `UpdateUserDto`: `PartialType(CreateUserDto)` + `isActive` + `role` | `PartialType(CreateUserDto)`, sin `isActive` ni `role` | Adaptado (**D-10**) | El rol no se cambia (RF-01-06) y la marca de administrador solo se pone por SQL (ADR-040): ninguna ruta la asigna. Enviar `role` responde 400. |
| `UserService`: `create`, `findAll`, `findOne`, `findById`, `findOneByEmail`, `update`, `remove` | Los mismos | Adaptado | `create` responde 409 diciendo con qué método entrar si el correo es de Google o Microsoft (RF-01-04). `update` vuelve el correo a `procesando` si cambia, porque nadie lo verificó. `remove` borra la credencial y su docente o estudiante en una transacción (sus códigos, en cascada); si el docente ya tiene experiencias, la base lo impide y responde 409. |
| `UserController` protegido con `@UseGuards(JwtAuthGuard, RolesGuard)` y `@Roles('admin')` | Igual, las 5 rutas | Idéntico | DELETE responde 204. |

### 5.3 Módulo Auth (sección 4)

| Guía | Backend | Estado | Razón |
|---|---|---|---|
| `LoginDto`, `RegisterDto extends CreateUserDto` | Igual | Idéntico | — |
| `JwtPayload { sub, email, role }` | `{ sub, email, role, idDocente, idEstudiante }` | Adaptado (**D-11**) | Nota R2 del docente: la sesión dice a qué docente o estudiante da acceso, en vez de un `id_usuario` genérico. |
| `AuthResponse { user: { id, email, fullName, role }, token }` | Igual | Idéntico | — |
| `JwtStrategy` con `getOrThrow('JWT_SECRET')` | Igual | Adaptado | Rechaza además el token de recuperación de contraseña (D-14). No revisa `isActive` (D-08). |
| `register()` | Igual, y además envía el código para verificar el correo | Adaptado (**D-12**) | RF-01-03 y nota R5. Si el servidor de correo falla, la cuenta queda creada y el código se puede reenviar. |
| `login()` con «Credenciales inválidas» | Igual, más el bloqueo: 5 intentos fallidos bloquean 15 minutos, con el mismo mensaje | Adaptado (**D-13**) | RF-01-07; la guía v1 lo recomendaba en sus «próximos pasos». Una cuenta de Google o Microsoft responde 409 con el método que debe usar (RF-01-04). |
| `validateToken()` | No existe | Omitido | Nadie lo llama: la guía lo deja «para WebSockets», que este proyecto no usa. |
| `AuthController`: register (201), login (200), profile | Igual | Idéntico | `GET /auth/profile` responde también a una cuenta sin rol: es lo que hace la prueba 3. |
| `AuthModule` | Igual | Adaptado | Registra además el servicio de códigos, el guard de recuperación y los verificadores de Google y Microsoft. |
| `JwtAuthGuard`, `GetUser` | Iguales | Idéntico | — |

### 5.4 Serialización (sección 5)

| Guía | Backend | Estado |
|---|---|---|
| `ValidationPipe({ whitelist, forbidNonWhitelisted, transform })` | Igual | Idéntico |
| `ClassSerializerInterceptor` global | Igual | Idéntico |
| `app.enableCors()` y `process.env.PORT ?? 3000` | Igual, con `\|\|` en vez de `??` | Adaptado: con `??`, un `PORT=` vacío —el de `.env.example`— daría el puerto 0 |
| — | `/uploads` servido como archivos estáticos | Agregado: las fotos de perfil (RF-01-05) |

La configuración global vive en `src/configurar-app.ts`, que llaman `main.ts` y las pruebas:
así las pruebas corren exactamente con la misma configuración que el servidor.

### 5.5 Roles y protección de rutas (sección 6)

| Guía | Backend | Estado |
|---|---|---|
| `roles.decorator.ts` con `ROLES_KEY` | Igual (tipado con los roles del sistema) | Idéntico |
| `roles.guard.ts`: 401 sin usuario, 403 con otro rol | Igual | Idéntico |
| `user.controller.ts` protegido con `@Roles('admin')` | Igual | Idéntico |
| `src/example/example.controller.ts` con `/example/protected` y `/example/admin` | Igual, registrado en `AppModule` | Idéntico |
| — | `/catalogo/*` protegido igual, con `@Roles('docente')` | Agregado (D-15) |

### 5.6 Estructura de carpetas

```
src/
├── auth/
│   ├── decorators/  get-user.decorator.ts, roles.decorator.ts           ← guía
│   ├── dto/         login.dto.ts, register.dto.ts                        ← guía
│   │                + verificar-correo, reenviar-codigo, perfil, elegir-rol,
│   │                  editar-perfil, proveedor-token, solicitar-recuperacion,
│   │                  verificar-recuperacion, nueva-contrasena, password.constants
│   ├── entities/    + codigo-verificacion.entity.ts                      ← ADR-039
│   ├── guards/      jwt-auth.guard.ts, roles.guard.ts                    ← guía
│   │                + recuperacion.guard.ts
│   ├── interfaces/  auth-response.interface.ts, jwt-payload.interface.ts ← guía
│   ├── proveedores/ + Google y Microsoft (E-04, E-05)
│   ├── strategies/  jwt.strategy.ts                                      ← guía
│   ├── + codigo.service.ts, foto.ts
│   └── auth.controller.ts, auth.module.ts, auth.service.ts               ← guía
├── example/         example.controller.ts                                ← guía
├── user/
│   ├── dto/         create-user.dto.ts, update-user.dto.ts               ← guía
│   ├── entities/    user.entity.ts                                       ← guía
│   │                + docente.entity.ts, estudiante.entity.ts
│   └── user.controller.ts, user.module.ts, user.service.ts               ← guía
├── + catalogo/      el catálogo curricular (E-14 a E-17)
├── + correo/        el envío de los códigos (nota R5)
├── + limpieza/      la tarea nocturna (ADR-039)
├── + configurar-app.ts
├── app.module.ts                                                         ← guía
└── main.ts                                                               ← guía
```

Todos los archivos del árbol de la guía existen, con el mismo nombre y en el mismo lugar. Lo
marcado con `+` lo agrega AdaptiveLearn.

### 5.7 Otras diferencias

- **D-14 — token de recuperación.** Quien recupera su contraseña no tiene sesión. Por eso
  existe un token aparte, de 15 minutos, con un campo `proposito`: solo sirve en
  `POST /auth/nueva-contrasena`. `JwtStrategy` lo rechaza en cualquier otra ruta, y un token
  de sesión no sirve para cambiar la contraseña. Las dos cosas están probadas.
- **D-15 — el catálogo usa la misma protección que `/users`**, con otro rol:
  `@UseGuards(JwtAuthGuard, RolesGuard)` y `@Roles('docente')`. Un estudiante o una cuenta
  sin rol reciben 403.
- **D-16 — editar el propio perfil es `PATCH /auth/profile`**, no `PATCH /users/:id`: en la
  guía, `/users/:id` es del administrador. Sin `:id` en la ruta, nadie puede apuntar al
  perfil de otro. El encargo 03 pidió una ruta bajo `/auth/`; esta es la misma que consulta
  el perfil.
- **D-17 — el rol se lee de la base en cada petición**, igual que en la guía
  (`JwtStrategy.validate()` busca al usuario). Por eso, después de la prueba 4, también un
  token firmado antes ya tiene permisos de administrador. La guía pide volver a iniciar
  sesión para tener un token *con* el rol nuevo; eso también funciona (prueba 4).

## 6. Lo que agrega AdaptiveLearn

La autenticación de la guía funciona sola, sin pasos extra: por eso sus 6 pruebas no
dependen de nada de esta sección. Las rutas propias son las del catálogo de endpoints de la
Fase III (`docs/modesec/fase-3-diseno-computacional/20-catalogo-endpoints.md`, §3 y §4.1):

| N.º | Ruta | Qué hace |
|---|---|---|
| E-02 | `POST /auth/verificar-correo` (con token) | Verifica el correo con el código de 6 dígitos (ventana 015) |
| E-03 | `POST /auth/reenviar-codigo` | Reenvía el código, como mínimo cada 30 s; responde igual exista o no la cuenta |
| E-04, E-05 | `POST /auth/google`, `POST /auth/microsoft` | Entrar con Google o Microsoft. Sin su configuración en `.env` responden 503 «no configurado» (el equipo todavía no tiene esas credenciales); se probaron con un proveedor simulado |
| E-06 | `POST /auth/elegir-rol` (con token) | Completa el perfil (nombres, apellidos y foto JPG o PNG de hasta 5 MB) y elige el rol, en una sola transacción. Exige el correo verificado; el rol no se cambia |
| E-08 | `POST /auth/recuperar-contrasena` | Envía el código de recuperación; **responde igual exista o no la cuenta** (RNF-07) |
| E-09 | `POST /auth/recuperar-contrasena/verificar` | Valida el código y entrega un token de 15 minutos que solo sirve para el paso siguiente |
| E-10 | `POST /auth/nueva-contrasena` (token de recuperación) | Guarda la contraseña nueva (204) |
| E-12 | `PATCH /auth/profile` (con token) | Edita el **propio** perfil (D-16) |
| E-14 a E-17 | `GET /catalogo/dbas`, `/catalogo/dbas/:codigo`, `/catalogo/areas`, `/catalogo/grados` | El catálogo curricular, de solo lectura, para la sesión de un docente (D-15) |

**Los códigos (ADR-039, nota R4 del docente).** Viven en la tabla `codigo_verificacion`, a
lo sumo uno por cuenta y propósito (verificar el correo o recuperar la contraseña). Se
guarda un **HMAC-SHA256** del código, no el código. El vencimiento (10 min) y la espera para
reenviar (30 s) **se calculan** desde `creado_en`. Cada código admite 5 intentos fallidos.
Una **tarea nocturna** (3:00 a. m., hora de Colombia) borra los códigos vencidos y las
cuentas que llevan más de 7 días en `procesando` sin rol; la hora y los días se cambian en
`.env`.

**El correo (nota R5).** Los códigos se envían por SMTP con la cuenta del sistema,
`adaptivelearn.sistema@gmail.com` (Gmail, `smtp.gmail.com`, puerto 587). La contraseña de
aplicación la pone el equipo en su `.env`; **ninguna clave está en el código**. Sin
`MAIL_HOST`, el servidor escribe el código en su consola y lo avisa al arrancar.

## 7. Seguridad

**Lo que la guía v2 ya corrigió** respecto de la v1 —y que en septiembre se había corregido
aquí por cuenta propia—: `/users` exige token y rol de administrador; nadie puede darse el
rol desde la API; la contraseña nunca sale en una respuesta (`@Exclude`); el login revisa la
contraseña antes de decir nada del estado de la cuenta; un token de un usuario borrado da 401.

**Lo que se agrega aquí:**

1. **Bloqueo de inicio de sesión:** 5 intentos fallidos bloquean 15 minutos, con el mismo
   mensaje genérico, para no confirmar que la cuenta existe.
2. **Códigos con límite de intentos** (5) y guardados con HMAC: quien lea la base no puede
   usarlos. Generados con `crypto`, no con `Math.random`.
3. **Recuperación sin revelar cuentas** (RNF-07): pedir el código, reenviarlo y verificarlo
   responden lo mismo exista o no el correo.
4. **El token de recuperación no abre sesión**, y un token de sesión no sirve para cambiar
   la contraseña.
5. **La foto se reconoce por su contenido** (los primeros bytes del archivo), no por su
   nombre ni por el tipo que declara el navegador; se guarda con un nombre al azar.
6. **Google y Microsoft se verifican en el servidor**, con las llaves públicas de cada
   proveedor (firma, emisor, audiencia y vencimiento): el backend no confía en lo que diga
   el navegador.

## 8. Verificación realizada

- `npm run build`: compila sin errores. `npm run lint` (oxlint): 0 advertencias.
- `npm test`: **18 pruebas unitarias** (rol y nombre deducidos, serialización sin datos
  secretos, `RolesGuard` 401/403, tiempos e intentos de los códigos, tipo de la foto).
- `npm run test:e2e`: **40 pruebas de punta a punta contra MySQL 8.0.46 real**, en una base
  de pruebas que se crea desde cero en cada corrida con el mismo script del equipo:
  - las 6 pruebas de la guía y su tabla de respuestas (`test/guia-seccion-7.e2e-spec.ts`);
  - el acceso (`test/acceso.e2e-spec.ts`): registro → verificar → completar perfil → elegir
    rol, con foto; código vencido; reenvío antes de 30 s rechazado; 5 intentos de código;
    bloqueo de login; recuperar la contraseña sin revelar si el correo existe; editar solo
    el propio perfil; `/users` con un usuario normal → 403; Google y Microsoft simulados,
    incluido el 503 sin configuración;
  - la tarea nocturna borrando lo que corresponde, y nada más, y las 4 rutas del catálogo
    con sus filtros (`test/limpieza-y-catalogo.e2e-spec.ts`).
- Para comprobar que las pruebas detectan errores, se rompió a propósito la espera de 30 s y
  el límite de 5 intentos: las pruebas correspondientes fallaron. Después se restauró el código.
- `node scripts/pruebas-guia-seccion-7.mjs` contra el servidor encendido: todas las
  respuestas son las esperadas (`salida-pruebas-guia-v2.txt`).
- **La colección de Postman** se corrió entera con `newman` (el ejecutor de Postman en la
  terminal) contra el servidor encendido: **31 peticiones, 0 fallas** en sus verificaciones.
  Los dos pasos que Postman no puede hacer solo —la sentencia SQL de la prueba 4 y copiar el
  código de 6 dígitos de la consola del servidor— los hizo un ayudante de esa corrida, fuera
  del repositorio; a mano se hacen como dice la descripción de cada petición.

## 9. Pendientes conocidos

- **Google y Microsoft con cuentas reales:** falta crear las aplicaciones en Google Cloud y
  en Azure y poner sus identificadores en `.env`. Con Microsoft, además, conviene revisar
  qué cuentas se aceptan: su token no siempre dice si el correo está verificado.
- **Correo real:** falta la contraseña de aplicación de `adaptivelearn.sistema@gmail.com` en
  el `.env` de cada integrante, y probar un envío.
- **Refresh tokens y cierre de sesión en el servidor** (`POST /auth/cerrar-sesion`, E-13,
  opcional): con JWT, cerrar sesión es que el navegador borre el token.
- **Pregunta P2 al docente** (`21-revision-docente-2026-10-22.md`): ADR-039 interpreta la
  nota R4; si el docente responde otra cosa, se ajusta.
