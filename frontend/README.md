# Frontend — AdaptiveLearn

La parte que se ve en el navegador. Está hecha con **React + Vite + TypeScript + Tailwind**
y los íconos de **Lucide** (ADR-038).

## Estado

Hecho hasta el **Paso 3 de "Crear experiencia"** (encargo 04, 2026-10-27), conectado al
backend real:

| Ventana | Qué es | Spec |
|---|---|---|
| 014 | Iniciar sesión / Crear cuenta | `17-spec-auth-login-registro.md` |
| 015 | Verifica tu correo (código de 6 dígitos) | `18-spec-auth-verifica-correo.md` |
| 016 | Completa tu perfil | `19-spec-auth-completa-perfil.md` |
| 017 | Elige tu rol | `20-spec-auth-elige-rol.md` |
| 018 | Recuperar contraseña | `21-spec-auth-recupera-contrasena.md` |
| 019 | Nueva contraseña | `22-spec-auth-nueva-contrasena.md` |
| 001 | Dashboard (docente y estudiante), vacío | `04-spec-dashboard.md` |
| 026 | Mi perfil | `26-spec-modal-mi-perfil.md` |
| 002 | Crear experiencia — Paso 1: el área | `05-spec-crear-experiencia-paso1.md` |
| 003 | Crear experiencia — Paso 2: el DBA | `06-spec-crear-experiencia-paso2.md` |
| 004 | Crear experiencia — Paso 3: confirmar | `07-spec-crear-experiencia-paso3.md` |

Las specs están en `docs/modesec/fase-2-diseno-multimedial/`. Cada pantalla cita la suya al
comienzo de su archivo, en `src/ventanas/`.

**Lo que todavía NO hace** (encargo 04 §7): crear la experiencia de verdad (el botón del
Paso 3 solo muestra *"Crear la experiencia llega en la siguiente etapa."*), unirse con
código, la Vista Interna, el banco de preguntas, el diagnóstico y el reporte.

## Arrancar todo desde cero

Hacen falta tres cosas encendidas a la vez: **MySQL** (la base de datos), **el backend** (el
servidor) y **el frontend** (la página). Cada una en su propia terminal.

### Lo que hay que tener instalado

- **Node.js 22** o más nuevo (se comprueba con `node -v`).
- **MySQL 8.0.16** o más nuevo, encendido.

### 1. La base de datos y el backend

Se sigue el `backend/README.md`, pasos 1 a 4. En resumen:

```bash
cd backend
npm install
cp .env.example .env      # y se completa .env (la tabla del README del backend)
npm run db:preparar       # crea la base y carga los 343 DBA del catálogo
npm run start:dev         # deja esta terminal abierta
```

Cuando en la consola aparece `🚀 Servidor corriendo en http://localhost:3000`, el backend
está listo. **Si el correo no está configurado** (`MAIL_HOST` vacío), los códigos de
verificación no llegan al correo: **aparecen en esta consola**. Así se prueba sin correo.

### 2. El frontend

En **otra** terminal:

```bash
cd frontend
npm ci
cp .env.example .env      # se puede dejar vacío: usa el backend de http://localhost:3000
npm run dev
```

Y se abre **http://localhost:5173** en el navegador.

> Si `npm ci` falla con un error que menciona `edgesOut`, es un defecto de npm 10 (no del
> proyecto). Se arregla instalando con npm 11: `npx -y npm@11 ci`.

`.env` nunca se sube al repositorio. Sus variables, todas opcionales:

| Variable | Qué poner |
|---|---|
| `VITE_API_URL` | Dónde está el backend. Vacía: `http://localhost:3000`. |
| `VITE_GOOGLE_CLIENT_ID`, `VITE_MICROSOFT_CLIENT_ID` | Los **mismos** identificadores que `GOOGLE_CLIENT_ID` y `MICROSOFT_CLIENT_ID` del backend. Vacíos: el botón muestra el mensaje «no configurado» del backend (encargo 04 §4.6). |

## Recorrer el camino (encargo 04 §1)

Con todo encendido, en http://localhost:5173:

1. **014 — Crear cuenta.** En la pestaña "Crear cuenta" se escribe un correo y una contraseña
   (mínimo 8 caracteres, con una mayúscula, una minúscula y un número) y se pulsa el botón.
2. **015 — Verifica tu correo.** El código de 6 dígitos se copia de la **consola del
   backend** (o del correo, si está configurado). Se puede pedir otro a los 30 segundos.
3. **016 — Completa tu perfil.** Nombres, apellidos y, si se quiere, una foto (JPG o PNG).
4. **017 — Elige tu rol.** "Docente" (el que puede crear experiencias) o "Estudiante".
5. **001 — Dashboard.** Aparece vacío: todavía no hay experiencias (encargo 04 §4.1). Arriba
   a la derecha, la foto abre **026 — Mi perfil**, y el ícono de salida cierra la sesión.
6. **002 — Crear experiencia, Paso 1** (solo docente). Se elige un área.
7. **003 — Paso 2.** Se filtra por grado o se busca por texto; se expande un DBA para ver
   sus evidencias, y se elige uno. Por ejemplo, Ciencias Sociales, grado 8.°, `CS-08-08`.
8. **004 — Paso 3.** Se revisa el nombre y se pulsa "Crear experiencia": sale el aviso de
   que eso llega en la siguiente etapa. **No se crea nada.**

También: **"¿Olvidaste tu contraseña?"** en 014 lleva a 018 → 015 → 019, y después se
inicia sesión con la contraseña nueva.

Si se cierra el navegador a mitad del registro, al iniciar sesión de nuevo la página lleva
a donde quedó (sin verificar → 015; sin perfil → 016; con rol → Dashboard).

## Comandos

Todos se corren dentro de `frontend/`.

| Comando | Qué hace |
|---|---|
| `npm run dev` | Arranca la página en http://localhost:5173 y la actualiza sola al guardar cambios |
| `npm run build` | Revisa los tipos y compila a `dist/` |
| `npm run lint` | Revisión de estilo del código (oxlint) |
| `npm test` | Pruebas unitarias (Vitest): las pantallas con un backend falso, sin MySQL |
| `npm run test:e2e` | Pruebas de punta a punta (Playwright) **contra el backend real y MySQL** (abajo) |
| `npm run verificar:estilos` | Comprueba que todo color, medida y clase salga de `tokens.json` (abajo) |
| `npm run tema` | Regenera el tema de Tailwind desde `tokens.json` (los demás comandos ya lo hacen) |

### Las pruebas de punta a punta

`npm run test:e2e` hace todo solo: compila el backend si no está compilado, **crea desde
cero una base aparte** y arranca su propio backend (en el puerto 3100) y su propia página
(en el 5174), así que no choca con los que estén encendidos.

- Esa base se llama como `DB_DATABASE` del `backend/.env` con `_e2e_frontend` al final
  (o lo que diga la variable `DB_DATABASE_E2E_FRONTEND`). **Se borra en cada corrida.**
  Si se llamara igual que la base de desarrollo, la prueba se niega a arrancar.
- Lee la conexión a MySQL del `backend/.env`.
- Si se cambió el backend, hay que compilarlo de nuevo (`npm run build` en `backend/`):
  las pruebas usan lo que haya en `backend/dist/`.
- Mientras corren, guardan **capturas de pantalla** en `capturas/`. Cada nombre empieza con
  el número de la ventana (`003-paso2-...png`), para compararlas con su spec.

**Las pruebas atrapan errores** (encargo 04 §6.4). Se rompieron a propósito dos cosas y se
comprobó que fallan:

| Lo que se rompió | Unitarias | Punta a punta |
|---|---|---|
| El filtro por grado del Paso 2 (no se manda `numero_grado`) | 1 falla | 1 falla: aparece `CS-01-01` donde se esperaba un DBA de 8.° |
| El paso de 015 a 016 (no se relee la sesión después de verificar) | 1 falla | 3 fallan: nunca aparece "Completa tu perfil" |

Después se quitó lo roto y todo volvió a pasar.

### El verificador de estilos

`npm run verificar:estilos` es al código lo que `verificar_tokens.py` es a las specs: falla
si en `src/` aparece un color escrito a mano (`#ff0000`), una medida a mano (`16px`), un
valor arbitrario de Tailwind (`w-[13px]`), una clase con un valor que el tema no tiene
(`p-5`, `bg-red-500`), un ícono de un tamaño que `tokens.json` no tiene, o una opacidad que
ninguna spec usa. El tema (`src/estilos/tema.generado.css`) **no se edita a mano**: lo
genera `scripts/generar-tema.mjs` desde `tokens.json`.

Los logos de Google y Microsoft (`src/marcas/`) están exentos: llevan sus colores de marca
(014 §2.8).

## Entrar con Google o Microsoft

Funciona solo si el equipo registra la aplicación en Google Cloud y en Azure. Además de
poner el mismo identificador en el `.env` del backend y del frontend, en esa consola hay que
autorizar como **dirección de retorno** (redirect URI) la de la página seguida de
`/oauth/retorno`. Por ejemplo: `http://localhost:5173/oauth/retorno`. Sin eso, el
proveedor rechaza el inicio de sesión.

## Qué hay en cada carpeta

```
src/
  ventanas/      una pantalla por archivo (V014Acceso.tsx, V015Verificar.tsx…)
    crear/       los pasos 1, 2 y 3 de "Crear experiencia" y su stepper
  componentes/   piezas que se repiten: botones, campos, modal, cajas del código
  api/           las llamadas al backend
  sesion/        la sesión abierta, las reglas (contraseña, a qué pantalla ir) y Google/Microsoft
  estilos/       el tema generado desde tokens.json
  marcas/        logos oficiales de Google y Microsoft
  pruebas/       ayudas de las pruebas unitarias
e2e/             pruebas de punta a punta (Playwright)
scripts/         generar-tema.mjs y verificar-estilos.mjs
capturas/        las capturas que dejan las pruebas e2e
```

## Seguridad y sesión

- **La contraseña nunca se guarda** en el navegador: se manda al backend y se olvida.
- **El token de la sesión** (la "llave" que el backend entrega al iniciar sesión) se guarda
  en el `sessionStorage` del navegador: dura mientras la pestaña esté abierta y se borra al
  cerrar sesión. Es una decisión propia del encargo 04, declarada para que el equipo la
  confirme.
- Si el backend responde que la sesión venció, la página vuelve a 014 con el aviso *"Tu
  sesión terminó. Inicia sesión de nuevo."*
