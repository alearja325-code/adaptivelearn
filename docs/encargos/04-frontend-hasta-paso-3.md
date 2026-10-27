# Encargo 04 — Frontend: del acceso al Paso 3 de "Crear experiencia"

**Para:** una sesión de Claude Code sobre este repositorio.
**Escrito:** 2026-10-27, desde la sesión local de Alejandro.
**Hazlo con el encargo 03 ya unido a `main`** (lo está desde el
2026-10-27, pull request #3).

**Antes de empezar, lee:**
1. `CLAUDE.md` y `docs/diseno/pendientes.md` (A15, A16).
2. **ADR-038** (React, Vite, TypeScript, Tailwind atado a `tokens.json`,
   Lucide) y ADR-040 (con sus 9 decisiones aceptadas) en
   `docs/diseno/decisiones.md`.
3. Las especificaciones de las ventanas de esta etapa, en
   `docs/modesec/fase-2-diseno-multimedial/` (tabla de la sección 3),
   más `03-tokens-diseno.md`, `tokens.json`, `28-mapa-navegacion.md` y
   `30-indice-recursos.md`.
4. `docs/modesec/fase-3-diseno-computacional/20-catalogo-endpoints.md`
   (§3 acceso, §4.1 catálogo) y `backend/README.md`.

## 1. Qué hay que lograr

La carpeta `frontend/` (hoy vacía) con las pantallas **desde el acceso
hasta el Paso 3 de "Crear experiencia"**, conectadas al backend que ya
existe, **sin crear la experiencia** (eso dispara la IA; es la etapa
siguiente). Al terminar, una persona debe poder, en el navegador:

> crear su cuenta → recibir el código → verificar el correo → completar
> su perfil → elegir "Docente" → entrar al Dashboard → abrir "Crear
> experiencia" → elegir un área (Paso 1) → buscar y elegir un DBA,
> filtrando por grado y viendo sus evidencias (Paso 2) → darle nombre
> (Paso 3) — y ahí parar.

Y también: iniciar sesión, cerrar sesión, recuperar la contraseña, ver y
editar su perfil (ventana 026) y elegir "Estudiante" (llega a su
Dashboard, vacío).

## 2. La regla de oro

**Las especificaciones de la Fase II mandan en lo que se ve.** Cada
medida, color, texto, estado y acción sale de la spec de su ventana. No
se inventa ni se "mejora" nada: si algo no está especificado, se toma
la decisión mínima y **se declara** (sección 8).

- **Textos:** exactamente los de la spec, en español, con sus tildes.
- **Estilos:** Tailwind con un tema **generado desde `tokens.json`** (no
  copiado a mano): colores, espaciados, radios, alturas, tamaños de
  letra, grosores y la fuente. Sin valores arbitrarios (`[#123456]`,
  `[13px]`) ni colores o medidas escritos en el código fuera del tema.
  Agrega un **verificador** (`npm run verificar:estilos`) que falle si
  aparece uno: es en el código lo que `verificar_tokens.py` hace en las
  specs.
- **Íconos:** Lucide, los que la spec sugiere.
- **Numeración:** el archivo y la ventana no tienen el mismo número
  (`17-spec-…` es la Ventana 014). Cita siempre la ventana.

## 3. Las pantallas de esta etapa

| Ventana | Archivo | Backend que usa |
|---|---|---|
| 014 Iniciar sesión / Crear cuenta | `17-spec-auth-login-registro.md` | E-01 `POST /auth/register`, E-07 `POST /auth/login`, E-04/E-05 Google y Microsoft |
| 015 Verifica tu correo | `18-spec-auth-verifica-correo.md` | E-02 `POST /auth/verificar-correo`, E-03 `POST /auth/reenviar-codigo` |
| 016 Completa tu perfil | `19-spec-auth-completa-perfil.md` | (ninguno: se envía junto con 017) |
| 017 Elige tu rol | `20-spec-auth-elige-rol.md` | E-06 `POST /auth/elegir-rol` (multipart: `role`, `nombres`, `apellidos`, `foto`) |
| 018 Recupera tu contraseña | `21-spec-auth-recupera-contrasena.md` | E-08, E-09 |
| 019 Nueva contraseña | `22-spec-auth-nueva-contrasena.md` | E-10 |
| 001 Dashboard (docente y estudiante) | `04-spec-dashboard.md` | E-11 `GET /auth/profile` |
| 026 Mi perfil (modal) | `26-spec-modal-mi-perfil.md` | E-11, E-12 `PATCH /auth/profile` |
| 002 Crear experiencia, Paso 1 | `05-spec-crear-experiencia-paso1.md` | `GET /catalogo/areas` |
| 003 Paso 2 | `06-spec-crear-experiencia-paso2.md` | `GET /catalogo/grados`, `GET /catalogo/dbas`, `GET /catalogo/dbas/:codigo` |
| 004 Paso 3 | `07-spec-crear-experiencia-paso3.md` | (ninguno en esta etapa; ver 4.3) |

Lee las rutas, sus campos y sus errores **del código del backend**
(`backend/src/`) y de `20`, no de memoria: por ejemplo, el campo del rol
se llama `role` y la respuesta del login trae `token`.

## 4. Lo que las pantallas piden y todavía no existe

Decidido por Alejandro para esta etapa; no lo resuelvas de otra forma:

1. **Dashboard sin experiencias.** Crear experiencias es la etapa
   siguiente, y no hay ruta para listarlas. El Dashboard muestra su
   **estado vacío** (spec 001, "Empty state") para ambos roles, sin
   llamar a una ruta que no existe. Buscar y los filtros se ven, pero
   no tienen sobre qué actuar.
2. **"Unirse con código" (estudiante)** abre la ventana 005 en una etapa
   posterior. Aquí, al hacer clic, se muestra un aviso informativo
   corto (color Informativo `#6D28D9`, tipografía Caption): *"Unirse a
   una experiencia llega en la siguiente etapa."*
3. **"Crear experiencia" del Paso 3.** El botón se ve y se habilita
   como dice la spec (nombre no vacío), pero **no llama a nada ni abre
   el modal de carga**: muestra en el lugar del mensaje de error de la
   spec, con el mismo estilo pero en color Informativo, *"Crear la
   experiencia llega en la siguiente etapa."* No se guarda nada.
4. **Paso 2, datos que faltan en el catálogo:**
   - **Evidencias:** mientras no haya dictamen (`admiteFormatoCerrado`
     es `null`, censo QA-014 pendiente), todas se muestran como "aplica"
     (texto normal, sin tachar).
   - **Ejemplo:** hoy es `null` en todos los DBA (QA-011). Mientras sea
     `null`, el infoblock "Ejemplo" **no se muestra**. Deja lista la
     forma de la spec para cuando exista.
   - Las evidencias se piden con `GET /catalogo/dbas/:codigo` al
     expandir la card, no todas de una vez.
5. **Cerrar sesión:** no hay ruta (E-13 es opcional). Se borra la
   sesión en el navegador y se va a la ventana 014.
6. **Google y Microsoft:** el equipo todavía no tiene sus credenciales.
   Con `VITE_GOOGLE_CLIENT_ID` y `VITE_MICROSOFT_CLIENT_ID` vacíos, el
   botón muestra el mensaje "no configurado" que responde el backend
   (503). Déjalo listo para cuando existan, y pruébalo con lo que
   puedas sin credenciales reales.

## 5. Cómo debe comportarse

- **El camino de registro sigue al backend:** una cuenta sin verificar
  va a 015; una verificada sin rol, a 016 (registro a medias, ADR-035);
  una con rol, al Dashboard. Esto vale también al iniciar sesión y al
  recargar la página.
- **Rutas protegidas:** sin sesión, a 014. El Dashboard de docente y el
  de estudiante son la misma ventana con dos variantes (spec 001).
- **Errores del backend:** se muestran con los textos de la spec; si la
  spec no tiene uno para ese caso, el `message` del backend. Nunca una
  pantalla en blanco.
- **Sesión vencida (401):** a 014, sin perder el aviso.
- **La contraseña nunca se guarda** en el navegador; el token sí (dónde,
  decídelo y declara por qué).
- **Ancho:** las specs están dibujadas para escritorio. No hace falta
  diseño para celular en esta etapa; que no se rompa en una ventana de
  1280 px de ancho.

## 6. Pruebas

1. **Unitarias** (Vitest + Testing Library): los formularios y sus
   validaciones, el paso entre ventanas según el estado de la cuenta, y
   los tres avisos de la sección 4.
2. **De punta a punta en un navegador real** (Playwright), contra el
   backend real y MySQL (`npm run db:preparar` y el backend sin
   `MAIL_HOST`, así el código sale en la consola y la prueba lo lee de
   ahí). Como mínimo:
   - el camino completo de la sección 1, hasta el aviso del Paso 3;
   - un código equivocado y el reenvío con su espera de 30 s;
   - iniciar sesión, cerrar sesión y volver a entrar;
   - recuperar la contraseña y entrar con la nueva;
   - editar el perfil en la ventana 026;
   - elegir "Estudiante" y ver su Dashboard vacío;
   - en el Paso 2: filtrar por grado, buscar por texto, expandir una
     card y ver sus evidencias (usa `CS-08-08`).
3. **Capturas:** guarda una captura de cada ventana y de cada estado
   importante (vacío, error, seleccionado) en
   `frontend/capturas/`, con el número de la ventana en el nombre. Las
   revisa Alejandro contra las specs.
4. **Comprueba que las pruebas atrapan errores:** rompe a propósito dos
   cosas (por ejemplo, el filtro por grado y el paso de 015 a 016),
   muestra que fallan y quítalo.

## 7. Lo que NO debes hacer

- **No implementes crear la experiencia**, ni la Vista Interna, el
  banco, el diagnóstico, el reporte ni "Unirse con código".
- **No cambies el backend**, salvo un error que impida conectar el
  frontend; si pasa, arréglalo con su prueba y decláralo.
- **No edites las specs de la Fase II** para que coincidan con lo que
  programaste. Si una spec se contradice o es imposible, decláralo.
- **No edites `data/curriculo-men/`.**
- **No subas secretos.** `frontend/.env.example` lista las variables,
  sin valores.

## 8. Cuándo está terminado

1. `npm run build`, `npm run lint`, `npm test`, `npm run test:e2e` y
   `npm run verificar:estilos` pasan en `frontend/`.
2. Los verificadores de `CLAUDE.md` y las pruebas del backend siguen
   pasando.
3. `frontend/README.md` explica, para alguien que no es programador,
   cómo arrancar todo desde cero (base de datos, backend y frontend) y
   cómo recorrer el camino de la sección 1.
4. Cada ventana programada cita su spec en el código (un comentario al
   inicio del componente), para que el grupo B pueda explicarla.

## 9. Cómo entregarlo

Rama **`encargo-04-frontend-hasta-paso-3`** y **pull request hacia
`main`**, sin hacer merge. En la descripción, en español simple: qué
ventanas quedaron, el resultado de las pruebas (con cuántas capturas),
**qué decidiste por tu cuenta** (cada detalle que la spec no definía),
qué no se pudo seguir de la spec y por qué, y qué quedó pendiente.
Actualiza `docs/diseno/pendientes.md` (A16) con el estado real.
