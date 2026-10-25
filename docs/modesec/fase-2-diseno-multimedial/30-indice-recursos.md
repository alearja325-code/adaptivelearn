# 6. Índice de recursos

**Metodología:** MODESEC — Fase II, punto 6.

MODESEC pide inventariar, ventana por ventana, los recursos multimedia
que el software usa (imágenes, audio, video) y recuerda que *"los
materiales multimedia deben utilizarse cuando éstos hagan alguna
aportación relevante a los procesos de enseñanza y aprendizaje"*.

En AdaptiveLearn el inventario es corto a propósito: es un instrumento
de diagnóstico, y cada recurso que no aporta a responder bien es una
distracción o una barrera. **No hay audio ni video en ninguna ventana**:
ninguna tarea depende de escuchar o de ver una animación (decisión de
accesibilidad, E0 Bloque H).

## 1. Recursos globales

| Recurso | Qué es | Origen y licencia | Dónde se usa |
|---|---|---|---|
| Fuente **Inter** | Tipografía de toda la interfaz | Rasmus Andersson, licencia SIL Open Font License 1.1 (uso libre, incluido comercial). En la web se reemplaza por la fuente del sistema (`03-tokens-diseno.md`). | Todas las ventanas |
| Íconos **Lucide** | Íconos de trazo, en `16`, `20`, `24` y `32 px` | Proyecto Lucide, licencia ISC (uso libre con atribución en el código). `05-spec` ya los proponía. | Ver la tabla 2 |
| **Logo de Google** | Botón "Continuar con Google" | Marca de Google. Se usa según sus guías de marca para inicio de sesión; no se recolorea ni se deforma. | 014 |
| **Logo de Microsoft** | Botón "Continuar con Microsoft" | Marca de Microsoft. Mismas condiciones. | 014 |
| **Foto de perfil** | Imagen que sube cada usuario | Del usuario. JPG o PNG, máximo 5 MB, recorte cuadrado automático. Opcional. | 016, 026 (se sube); 001, 006, 020 (Sidebar), 011 (lista de estudiantes) |

**Ilustraciones, fotografías propias, sonidos, música, video:
ninguno.** Las imágenes que pueden traer los ejemplos de algunos DBA
del MEN no se muestran en esta versión (`06-spec` §2.4, ADR-011): no
hay una fuente verificada para usarlas.

**Nota de nombres:** donde una especificación describe un ícono por su
forma ("lupa", "ojo tachado"), la columna de íconos da su nombre en
Lucide. Es la equivalencia sugerida para construirlo; la forma descrita
en la especificación es la que manda.

## 2. Recursos por ventana

| Ventana | Imágenes | Íconos (Lucide) | Audio | Video | Animación |
|---|---|---|---|---|---|
| **001** Dashboard | Foto de perfil (Sidebar) | Ícono de "Mis experiencias" (`20px`; **su forma no está definida en `04-spec`** — sugerido `layout-grid`), `search`, `chevron-right`, ícono de lista vacía (`32px`, forma sin definir). "+" y "→" van como caracteres dentro del texto de los botones ("+ Crear experiencia", "→ Unirse con código"). | No | No | Hover en ítems, cards y bloque de perfil |
| **002** Crear · Paso 1 | — | `calculator`, `book-open`, `leaf`, `globe` (las 4 áreas), `x` | No | No | Selección de card |
| **003** Crear · Paso 2 | — | `search`, `chevron-down` (Grado), `chevron-right`/`chevron-down` (expandir), `x` | No | No | Expandir/colapsar, desplegable de Grado |
| **004** Crear · Paso 3 | — | `chevron-right`/`chevron-down`, `x` | No | No | Expandir InfoBlocks |
| **005** Unirse con código | — | `x` | No | No | Foco que avanza entre cajas |
| **006** Vista Interna (marco) | Foto de perfil (Sidebar) | `arrow-left`, `ellipsis` | No | No | Cambio de pestaña |
| **007** Resumen | — | `chevron-right`/`chevron-down` | No | No | Expandir/colapsar |
| **008** Materiales | — | `search` (Diagnóstico), `chart-column` (Reportes) | No | No | Selección de card |
| **009** Banco de preguntas | — | `search`, `pencil`, `eye-off`/`eye`, `circle-check`, `circle-minus`, `plus`, `chevron-right`/`chevron-down`, `x` | No | No | Atenuar ítem descartado, modo edición |
| **010** Reporte | — | `chevron-right`/`chevron-down`, `x` | No | No | Expandir cards |
| **011** Estudiantes | Foto de perfil de cada estudiante (`32px`) | `users`, `user` (sin foto), `search`, `chevron-right`/`chevron-down` | No | No | Expandir card de estudiante |
| **012** Confirmar publicación | — | `x` | No | No | Hover |
| **013** Código de invitación | — | `x` | No | No | "¡Código copiado!" por 2 s |
| **014** Iniciar sesión / Crear cuenta | Logos de Google y Microsoft | `mail`, `lock`, `eye`/`eye-off` | No | No | Mostrar/ocultar contraseña |
| **015** Verifica tu correo | — | — | No | No | Cuenta regresiva de reenvío |
| **016** Completa tu perfil | Foto de perfil (se sube) | `image-up`, `camera`, `user` | No | No | Capa oscura al pasar el cursor |
| **017** Elige tu rol | — | `presentation` (Docente), `book` (Estudiante) | No | No | Selección de card |
| **018** Recupera tu contraseña | — | `mail` | No | No | — |
| **019** Nueva contraseña | — | `lock`, `eye`/`eye-off` | No | No | Mostrar/ocultar contraseña |
| **020** Diagnóstico · Inicio | Foto de perfil (Sidebar) | `play`, `arrow-right`, `check` (uno por estado), `arrow-left`, `ellipsis` | No | No | — |
| **021** Diagnóstico · Ítem | — | — | No | No | Selección de opción |
| **022** Diagnóstico · Certeza | — | — | No | No | Selección de certeza |
| **023** Diagnóstico · Cierre | — | `check` | No | No | — |
| **024** Cargando | — | `loader-circle` | No | No | Giro continuo del ícono |
| **025** Eliminar / Salir | — | `x` | No | No | Hover |
| **026** Mi perfil | Foto de perfil (se cambia) | `image-up`, `camera`, `user`, `x` | No | No | Capa oscura al pasar el cursor |
| **027** Historial del estudiante | — | `circle-check`, `chevron-right`/`chevron-down`, `x`, ícono de lista vacía (`32px`) | No | No | Expandir/colapsar |

## 3. Lo que queda fuera, y por qué

- **Imágenes de los ejemplos del DBA** — sin fuente verificada del MEN;
  generarlas con IA queda fuera de alcance (ADR-011).
- **Audio de apoyo** (leer en voz alta el enunciado) — sería un apoyo
  real de accesibilidad para estudiantes que todavía no leen con
  fluidez (E0 Bloque H, pendiente de consulta). No está en esta
  versión; se deja anotado como la primera candidata si se agrega
  audio, porque cumpliría la condición de MODESEC: aportar al
  aprendizaje, no decorar.
- **Código QR** para unirse — diferido (`16-spec`).
