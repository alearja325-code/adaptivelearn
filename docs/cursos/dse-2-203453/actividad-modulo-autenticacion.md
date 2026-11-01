# Módulo de autenticación en NestJS — cumplimiento de la actividad

**Curso:** Diseño de Software Educativo II (DSE-2, 203453).
**Proyecto:** AdaptiveLearn. **Fecha:** 2026-11-01.
**Código:** carpeta `backend/` (NestJS 12 + TypeORM + MySQL 8).

Este documento recorre los 9 puntos de la actividad y dice, para cada uno,
dónde está en el código y cómo se comprobó. El módulo sigue la guía del
docente *"Implementación de JWT en NestJS con MySQL"* (versión 2) y, por
debajo, el modelo relacional del proyecto: la tabla de cuentas es
`credencial`, con sus tablas `docente` y `estudiante` (punto 2). Cada
diferencia con la guía está declarada, con su razón, en
`docs/cursos/dse-2-203453/backend-auth-informe-guia.md`.

## Cómo se comprobó

Todo se probó contra un **MySQL 8 real**, no con una base simulada:

| Prueba | Resultado |
|---|---|
| Las 6 pruebas de la sección 7 de la guía y su tabla de respuestas esperadas (`npm run pruebas:guia`) | Todas dan la respuesta esperada (201, 200, 401, 403, 409, 400, 404, 204) |
| Pruebas unitarias (`npm test`) | 20 de 20 pasan |
| Pruebas de punta a punta contra MySQL (`npm run test:e2e`) | 43 de 43 pasan, 3 de ellas sobre los puntos 3, 4 y 8 de esta actividad |
| Colección de Postman (`backend-auth-seccion-7.postman_collection.json`), con newman | 31 peticiones, 0 fallas (corrida del 2026-10-27) |
| Frontend real usando este backend, en un navegador (9 pruebas con Playwright) | Todas pasan |

Para comprobar que las pruebas detectan errores, se rompió a propósito una
regla (por ejemplo, se quitó la exigencia de minúscula en la contraseña) y
la prueba correspondiente falló; después se restauró.

## Los 9 puntos

### 1. Configuración del proyecto — cumplido

- NestJS con TypeORM para MySQL: `src/app.module.ts`
  (`TypeOrmModule.forRootAsync`, `type: 'mysql'`).
- Credenciales sensibles en variables de entorno: `.env` (nunca se sube al
  repositorio); la plantilla sin valores es `.env.example`. Se leen con
  `@nestjs/config`.
- Dependencias instaladas (`package.json`): `@nestjs/jwt`,
  `@nestjs/passport`, `passport-jwt`, `bcrypt`, `class-validator`,
  `class-transformer`, `@nestjs/typeorm`, `typeorm`, `mysql2`.

### 2. Modelado de datos — cumplido, con la entidad del M-R

- La entidad `User` de la guía está **mapeada sobre la tabla `credencial`**
  del modelo relacional (`src/user/entities/user.entity.ts`). Sus campos son
  los del diccionario de datos (`18-diccionario-datos.md`): correo,
  contraseña (hash), proveedor, estado de verificación, marca de
  administrador, intentos de inicio de sesión, bloqueo y fechas.
- Las personas están en `docente` y `estudiante`
  (`src/user/entities/docente.entity.ts`, `estudiante.entity.ts`), y los
  códigos de verificación en `codigo_verificacion`.
- El esquema de la base (`sql/001_esquema.sql`) **lo genera el modelo
  relacional**, y un verificador falla si alguien lo edita a mano.

### 3. DTOs con validación — cumplido

- `RegisterDto` (`src/auth/dto/register.dto.ts`, hereda de
  `src/user/dto/create-user.dto.ts`): formato de email (`@IsEmail`), campos
  requeridos (`@IsNotEmpty`) y contraseña de **mínimo 8 caracteres, con
  mayúscula, minúscula y número** (`@Matches`, regla en
  `src/auth/dto/password.constants.ts`).
- `LoginDto` (`src/auth/dto/login.dto.ts`): email y contraseña requeridos.
- `UpdateUserDto` (`src/user/dto/update-user.dto.ts`): `PartialType(CreateUserDto)`,
  como en la guía. `PartialType` le pone `@IsOptional()` a cada campo y
  conserva sus demás validaciones: se valida solo lo que se envía.
- `ValidationPipe` global con `whitelist` y `forbidNonWhitelisted`
  (`src/configurar-app.ts`): un campo que el DTO no declara se rechaza con
  400.

### 4. Servicio de autenticación — cumplido

En `src/auth/auth.service.ts` y `src/user/user.service.ts`:

- `register()`: verifica que el email no exista (si existe,
  `ConflictException`, 409), cifra la contraseña con **bcrypt de 10
  rondas** (`saltRounds = 10`), crea la cuenta y responde **sin la
  contraseña**.
- `login()`: llama a `validateUser()` y genera el **JWT con payload
  `{ sub, email, role }`** (más el número de docente o de estudiante, que
  pidió el docente en su revisión del 2026-10-22). Retorna el token y los
  datos del usuario.
- `validateUser()`: busca la cuenta por email, **verifica que esté activa**
  y compara la contraseña con `bcrypt.compare`. En AdaptiveLearn "activa"
  significa **no bloqueada**: tras 5 intentos fallidos la cuenta se bloquea
  15 minutos (RF-01-07). El modelo no tiene cuentas desactivadas porque
  ningún requerimiento lo pide.

### 5. JWT — cumplido

- `JwtModule` (`src/auth/auth.module.ts`) con el secreto y la expiración
  desde `.env` (`JWT_SECRET`, `JWT_EXPIRATION`, por ejemplo 3600 s = 1 h).
- `JwtStrategy` (`src/auth/strategies/jwt.strategy.ts`) extiende
  `PassportStrategy`: extrae el token del encabezado `Authorization:
  Bearer`, lo valida y devuelve la cuenta autenticada (y rechaza el token
  si la cuenta ya no existe).

### 6. Guards — cumplido

- `JwtAuthGuard` (`src/auth/guards/jwt-auth.guard.ts`), usado con
  `@UseGuards(JwtAuthGuard)`.
- `RolesGuard` (`src/auth/guards/roles.guard.ts`) con el decorador
  personalizado `@Roles(...roles)` (`src/auth/decorators/roles.decorator.ts`),
  combinado con `JwtAuthGuard`: `@UseGuards(JwtAuthGuard, RolesGuard)`.

### 7. Controladores — cumplido, incluido el opcional

- `AuthController` (`src/auth/auth.controller.ts`): `POST /auth/register`,
  `POST /auth/login` (responde 200) y `GET /auth/profile` (protegida).
- `UsersController` (`src/user/user.controller.ts`): `GET /users`,
  `GET /users/:id`, `PATCH /users/:id` y `DELETE /users/:id` (responde
  204). **Las cuatro son solo para administrador**, como en la guía v2: el
  administrador se marca únicamente por SQL. Cada persona edita su propio
  perfil en `PATCH /auth/profile`.

### 8. Seguridad — cumplido; *refresh tokens* no implementados

- Contraseñas con hash bcrypt; nunca en texto plano.
- **CORS configurado:** solo la dirección del frontend puede llamar al
  backend desde un navegador (`CORS_ORIGIN` en `.env`; por defecto
  `http://localhost:5173`). Una prueba comprueba que otra dirección no
  recibe permiso.
- Entrada saneada: `ValidationPipe` con `whitelist`,
  `forbidNonWhitelisted` y `transform`.
- `@Exclude()` en la contraseña (`user.entity.ts`) y
  `ClassSerializerInterceptor` global: ninguna respuesta la incluye.
- Además: bloqueo de 15 minutos tras 5 intentos fallidos, y los códigos de
  verificación del correo se guardan como huella (HMAC), no tal cual.
- **No implementado: refresh tokens** (opcional avanzado). La sesión dura
  lo que diga `JWT_EXPIRATION`, y después se vuelve a iniciar sesión.

### 9. Manejo de errores — cumplido

| Excepción | Cuándo |
|---|---|
| `UnauthorizedException` (401) | Credenciales inválidas, sin token o token vencido |
| `ConflictException` (409) | Email ya registrado |
| `ForbiddenException` (403) | Token válido pero sin el rol requerido |
| `NotFoundException` (404) | Usuario que no existe |

## Cómo ejecutarlo

Los pasos completos están en `backend/README.md`: instalar dependencias
(`npm install`), copiar `.env.example` a `.env` y completarlo, preparar la
base (`npm run db:preparar`), arrancar (`npm run start:dev`) y correr las
pruebas (`npm test`, `npm run test:e2e`, `npm run pruebas:guia`).
