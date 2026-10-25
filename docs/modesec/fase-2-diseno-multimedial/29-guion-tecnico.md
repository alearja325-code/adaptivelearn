# 5. Guión técnico

**Metodología:** MODESEC — Fase II, punto 5.
**Archivo generado** por `navegacion/mapa_navegacion.py` a partir de
`navegacion/_plantilla-guion-tecnico.md`. No editar a mano: la tabla de
la sección 3 sale de la misma fuente que el mapa de navegación
(`28-mapa-navegacion.md`), para que ambos no puedan contradecirse.

## 1. Qué es y cómo está organizado

MODESEC define el guión técnico como *"un escrito que contiene
detalladamente qué es lo que queremos mostrar en la pantalla"*: cómo es
cada pantallazo, sus fondos, botones, sonidos, fotografías, colores,
tipo y color de letra, y dónde va situado todo.

En este proyecto ese detalle ya existe, pantalla por pantalla: son las
**27 ventanas especificadas** en los documentos `04` a `27`
de esta carpeta. Cada una describe sus elementos con medidas, colores y
tipografía exactos, ordenados según las 7 categorías que MODESEC pide
para describir una ventana: imagen, nombre, texto, audio, video,
animación y acciones. Repetir ese contenido aquí crearía dos versiones
de lo mismo que tarde o temprano dirían cosas distintas.

Por eso este documento hace dos cosas que ninguna especificación hace
por sí sola:
1. **Reúne las reglas que valen para todas las pantallas** (sección 2):
   lo que MODESEC llama ventana estándar, más todo lo que se repite.
2. **Indexa las ventanas** (sección 3): qué es cada una, para quién,
   dónde está su detalle, desde dónde se llega y adónde lleva.

## 2. Reglas comunes a todas las pantallas

### 2.1 Fondo y marcos

Todas las pantallas se diseñan sobre un lienzo de `1440 × 900`
(computador, ADR-025), fondo **Canvas `#F7F6F3`**. Existen 4 marcos, y
cada pantalla usa exactamente uno:

| Marco | Medida | Dónde se define | Lo usan |
|---|---|---|---|
| Plataforma: Sidebar + Panel | Sidebar `280px` + panel que llena el resto | `04-spec-dashboard.md` | 001, 006 (y sus pestañas 007, 008, 011), 020 |
| Card centrada | `480px` de ancho | `17-spec-auth-login-registro.md` §2.1 | 014–019 (Auth), 021, 022, 023, 026 |
| Modal chico | `412px` de ancho | `08-spec-unirse-codigo.md` §2.1 | 005, 013, 024 |
| Modal grande | `912px` de ancho, alto máximo `852px` | `05-spec-crear-experiencia-paso1.md` §2.1 | 002–004, 009, 010, 012, 025, 027 |

Paneles, cards y modales: fondo **blanco `#FFFFFF`**, borde `1px`
**`#E7E7E7`**, esquinas redondeadas (`24px` en marcos y modales, `16px`
en cards de contenido).

### 2.2 Botones y controles

| Componente | Aspecto | Regla |
|---|---|---|
| Botón primario | Fondo `#111111`, letra blanca, alto `48px`, esquinas `12px` | La acción principal de la pantalla. Uno por pantalla. |
| Botón deshabilitado | Fondo `#BDBDBD`, letra blanca | Mientras falte algo para poder actuar. Si la regla para habilitarlo es exacta, no se agrega mensaje de error. |
| Botón de acción destructiva | Fondo `#991B1B`, letra blanca | Solo en 025 (eliminar / salir). |
| Botón secundario ("Volver", "Cancelar") | Sin fondo ni borde, letra `#555555` | Siempre a la izquierda del primario. |
| Campo de texto | Alto `44px`, borde `#E7E7E7`; al escribir, borde `#111111` | — |
| Botón de ícono (cerrar, "+", "…") | Cuadro de `32px` con ícono de `16px` | La zona clicable es el cuadro, no el ícono (WCAG 2.2: mínimo 24 px). |
| Enlace de texto | Subrayado, letra `#555555` | Sin color de enlace propio en la paleta. |

**Esperas:** toda acción que espera una respuesta del servidor muestra
el **Modal: Cargando** (024), con un título que nombra la acción en
gerundio ("Generando las preguntas...", "Guardando tu perfil..."). No
se puede cerrar mientras espera (excepción documentada en `24-spec`).

### 2.3 Colores y su significado

Un color = un significado. Tabla completa, con contrastes verificados,
en `03-tokens-diseno.md`.

| Uso | Colores |
|---|---|
| Texto principal / secundario / de apoyo | `#111111` / `#555555` / `#888888` |
| Fondos de estado neutro, selección | `#F5F3EE`; pasar el cursor: `#FAFAF8` |
| Resultado de una evidencia | Muestra `#29578E` · No muestra `#7A391F` · No concluyente `#52514E` · Sin concluir `#888888` |
| Información (evidencia que no aplica al formato) | `#6D28D9` |
| Error y acción destructiva | `#991B1B` |

Deliberadamente **sin verde = bien / rojo = mal** para resultados: el
proyecto evita lenguaje de certeza (ADR-008).

### 2.4 Letra

Fuente **Inter** (instalada por defecto en Figma; en la web, la fuente
del sistema). Tamaños en uso, de mayor a menor: títulos de página
`32px`, títulos de pantalla y modal `24px`, enunciados `20px`, texto y
botones `16px`, etiquetas y avisos `13px`, insignias `12px`. Detalle en
`03-tokens-diseno.md`.

### 2.5 Sonido, video, fotografías y animación

- **Audio y video: ninguno.** Ninguna tarea depende de escuchar o ver un
  video (decisión de accesibilidad, E0 Bloque H).
- **Fotografías: solo la foto de perfil** que cada usuario sube (JPG o
  PNG, máximo 5 MB). El sistema no trae fotografías propias.
- **Animación: solo cambios de estado** — pasar el cursor, abrir o
  cerrar, el giro del ícono de carga. Sin transiciones decorativas.
- Inventario completo por ventana: `30-indice-recursos.md`.

### 2.6 Navegación común

- El **Sidebar** (marco Plataforma) aparece en 001, 006 y 020: "Mis
  experiencias" lleva a 001; el **bloque de perfil** abre 026; "Cerrar
  sesión" lleva a 014.
- **Un modal, al cerrarse, vuelve a la pantalla que lo abrió.** El mapa
  no dibuja esa flecha de vuelta, salvo cuando la acción lleva a otro
  lugar (por ejemplo, 025 → 001 al eliminar).
- **El diagnóstico (021, 022) no tiene botón para volver ni para
  salir.** Cerrar la pestaña dispara la advertencia del navegador.

## 3. Índice de ventanas

| Ventana | Nombre | Usuario | Especificación | Se llega desde | Lleva a |
|---|---|---|---|---|---|
| **001** | Dashboard (docente) | Docente | `04-spec-dashboard.md` | 014 Iniciar sesión / Crear cuenta — *Iniciar sesión (docente)*; 017 Elige tu rol — *Soy Docente*; 006 Vista Interna (marco) — *←*; 025 Modal: Eliminar experiencia — *Eliminar experiencia (pasa por 024)* | 002 Crear experiencia · Paso 1 (área) — *Crear experiencia*; 006 Vista Interna (marco) — *Clic en una experiencia*; 026 Modal: Mi perfil — *Bloque de perfil*; 014 Iniciar sesión / Crear cuenta — *Cerrar sesión* |
| **001** | Dashboard (estudiante) | Estudiante | `04-spec-dashboard.md` | 014 Iniciar sesión / Crear cuenta — *Iniciar sesión (estudiante)*; 017 Elige tu rol — *Soy Estudiante*; 020 Diagnóstico · Inicio — *←*; 025 Modal: Salir de la experiencia — *Salir de la experiencia (pasa por 024)*; 023 Diagnóstico · Cierre — *Volver al inicio* | 005 Modal: Unirse con código — *Unirse con código*; 020 Diagnóstico · Inicio — *Clic en una experiencia*; 026 Modal: Mi perfil — *Bloque de perfil*; 014 Iniciar sesión / Crear cuenta — *Cerrar sesión* |
| **002** | Crear experiencia · Paso 1 (área) | Docente | `05-spec-crear-experiencia-paso1.md` | 001 Dashboard (docente) — *Crear experiencia*; 003 Crear experiencia · Paso 2 (DBA) — *Volver* | 003 Crear experiencia · Paso 2 (DBA) — *Continuar* |
| **003** | Crear experiencia · Paso 2 (DBA) | Docente | `06-spec-crear-experiencia-paso2.md` | 002 Crear experiencia · Paso 1 (área) — *Continuar*; 004 Crear experiencia · Paso 3 (confirmar) — *Volver* | 002 Crear experiencia · Paso 1 (área) — *Volver*; 004 Crear experiencia · Paso 3 (confirmar) — *Continuar* |
| **004** | Crear experiencia · Paso 3 (confirmar) | Docente | `07-spec-crear-experiencia-paso3.md` | 003 Crear experiencia · Paso 2 (DBA) — *Continuar* | 003 Crear experiencia · Paso 2 (DBA) — *Volver*; 006 Vista Interna (marco) — *Crear experiencia (pasa por 024)* |
| **005** | Modal: Unirse con código | Estudiante | `08-spec-unirse-codigo.md` | 001 Dashboard (estudiante) — *Unirse con código* | 020 Diagnóstico · Inicio — *Código válido* |
| **006** | Vista Interna (marco) | Docente | `09-spec-vista-interna-marco.md` | 004 Crear experiencia · Paso 3 (confirmar) — *Crear experiencia (pasa por 024)*; 001 Dashboard (docente) — *Clic en una experiencia* | 007 Pestaña Resumen — *pestaña (por defecto)*; 008 Pestaña Materiales — *pestaña*; 011 Pestaña Estudiantes — *pestaña*; 001 Dashboard (docente) — *←*; 025 Modal: Eliminar experiencia — *… (Eliminar)* |
| **007** | Pestaña Resumen | Docente | `10-spec-vista-interna-resumen.md` | 006 Vista Interna (marco) — *pestaña (por defecto)* | vuelve a quien lo abrió |
| **008** | Pestaña Materiales | Docente | `11-spec-vista-interna-materiales.md` | 006 Vista Interna (marco) — *pestaña* | 009 Modal: Banco de preguntas — *Ver banco de preguntas*; 010 Modal: Reporte — *Ver reporte* |
| **009** | Modal: Banco de preguntas | Docente | `12-spec-modal-banco-items.md` | 008 Pestaña Materiales — *Ver banco de preguntas* | vuelve a quien lo abrió |
| **010** | Modal: Reporte | Docente | `13-spec-modal-reporte.md` | 008 Pestaña Materiales — *Ver reporte* | vuelve a quien lo abrió |
| **011** | Pestaña Estudiantes | Docente | `14-spec-vista-interna-estudiantes.md` | 006 Vista Interna (marco) — *pestaña* | 012 Modal: Confirmar publicación — *Publicar experiencia*; 013 Modal: Código de invitación — *Código de invitación*; 027 Modal: Historial del estudiante — *Ver historial completo* |
| **012** | Modal: Confirmar publicación | Docente | `15-spec-modal-confirmar-publicar.md` | 011 Pestaña Estudiantes — *Publicar experiencia* | vuelve a quien lo abrió |
| **013** | Modal: Código de invitación | Docente | `16-spec-modal-codigo-invitacion.md` | 011 Pestaña Estudiantes — *Código de invitación* | vuelve a quien lo abrió |
| **014** | Iniciar sesión / Crear cuenta | Ambos | `17-spec-auth-login-registro.md` | Inicio — *abrir la plataforma*; 015 Verifica tu correo — *Volver (registro)*; 018 Recupera tu contraseña — *Volver a inicio de sesión*; 019 Nueva contraseña — *Guardar*; 001 Dashboard (docente) — *Cerrar sesión*; 001 Dashboard (estudiante) — *Cerrar sesión* | 015 Verifica tu correo — *Crear cuenta con correo*; 016 Completa tu perfil — *Google/Microsoft, cuenta nueva*; 001 Dashboard (docente) — *Iniciar sesión (docente)*; 001 Dashboard (estudiante) — *Iniciar sesión (estudiante)*; 018 Recupera tu contraseña — *¿Olvidaste tu contraseña?* |
| **015** | Verifica tu correo | Ambos | `18-spec-auth-verifica-correo.md` | 014 Iniciar sesión / Crear cuenta — *Crear cuenta con correo*; 018 Recupera tu contraseña — *Enviar código* | 016 Completa tu perfil — *Código válido (registro)*; 019 Nueva contraseña — *Código válido (recuperación)*; 014 Iniciar sesión / Crear cuenta — *Volver (registro)*; 018 Recupera tu contraseña — *Volver (recuperación)* |
| **016** | Completa tu perfil | Ambos | `19-spec-auth-completa-perfil.md` | 014 Iniciar sesión / Crear cuenta — *Google/Microsoft, cuenta nueva*; 015 Verifica tu correo — *Código válido (registro)*; 017 Elige tu rol — *Volver* | 017 Elige tu rol — *Continuar* |
| **017** | Elige tu rol | Ambos | `20-spec-auth-elige-rol.md` | 016 Completa tu perfil — *Continuar* | 016 Completa tu perfil — *Volver*; 001 Dashboard (docente) — *Soy Docente*; 001 Dashboard (estudiante) — *Soy Estudiante* |
| **018** | Recupera tu contraseña | Ambos | `21-spec-auth-recupera-contrasena.md` | 014 Iniciar sesión / Crear cuenta — *¿Olvidaste tu contraseña?*; 015 Verifica tu correo — *Volver (recuperación)* | 015 Verifica tu correo — *Enviar código*; 014 Iniciar sesión / Crear cuenta — *Volver a inicio de sesión* |
| **019** | Nueva contraseña | Ambos | `22-spec-auth-nueva-contrasena.md` | 015 Verifica tu correo — *Código válido (recuperación)* | 014 Iniciar sesión / Crear cuenta — *Guardar* |
| **020** | Diagnóstico · Inicio | Estudiante | `23-spec-toma-diagnostico.md` | 005 Modal: Unirse con código — *Código válido*; 001 Dashboard (estudiante) — *Clic en una experiencia* | 001 Dashboard (estudiante) — *←*; 025 Modal: Salir de la experiencia — *… (Salir)*; 021 Diagnóstico · Ítem — *Comenzar / Continuar* |
| **021** | Diagnóstico · Ítem | Estudiante | `23-spec-toma-diagnostico.md` | 020 Diagnóstico · Inicio — *Comenzar / Continuar*; 022 Diagnóstico · Certeza — *Confirmar · el sistema sigue (pasa por 024)* | 022 Diagnóstico · Certeza — *Siguiente* |
| **022** | Diagnóstico · Certeza | Estudiante | `23-spec-toma-diagnostico.md` | 021 Diagnóstico · Ítem — *Siguiente* | 021 Diagnóstico · Ítem — *Confirmar · el sistema sigue (pasa por 024)*; 023 Diagnóstico · Cierre — *Confirmar · el sistema concluye (pasa por 024)* |
| **023** | Diagnóstico · Cierre | Estudiante | `23-spec-toma-diagnostico.md` | 022 Diagnóstico · Certeza — *Confirmar · el sistema concluye (pasa por 024)* | 001 Dashboard (estudiante) — *Volver al inicio* |
| **024** | Modal: Cargando | Ambos | `24-spec-modal-cargando.md` | cualquier acción que espere al servidor (ver 2.2) | se cierra solo al recibir la respuesta |
| **025** | Modal: Eliminar experiencia | Docente | `25-spec-modal-confirmar-eliminar-salir.md` | 006 Vista Interna (marco) — *… (Eliminar)* | 001 Dashboard (docente) — *Eliminar experiencia (pasa por 024)* |
| **025** | Modal: Salir de la experiencia | Estudiante | `25-spec-modal-confirmar-eliminar-salir.md` | 020 Diagnóstico · Inicio — *… (Salir)* | 001 Dashboard (estudiante) — *Salir de la experiencia (pasa por 024)* |
| **026** | Modal: Mi perfil | Ambos | `26-spec-modal-mi-perfil.md` | 001 Dashboard (docente) — *Bloque de perfil*; 001 Dashboard (estudiante) — *Bloque de perfil* | vuelve a quien lo abrió |
| **027** | Modal: Historial del estudiante | Docente | `27-spec-modal-historial-estudiante.md` | 011 Pestaña Estudiantes — *Ver historial completo* | vuelve a quien lo abrió |

*Las acciones van en cursiva. "Pasa por 024" = muestra el Modal:
Cargando mientras espera. El 001 (Dashboard) y el 025 (eliminar /
salir) aparecen dos veces porque tienen una variante por rol.*
