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
**{{N_VENTANAS}} ventanas especificadas** en los documentos `04` a `27`
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

{{TABLA_VENTANAS}}

*Las acciones van en cursiva. "Pasa por 024" = muestra el Modal:
Cargando mientras espera. El 001 (Dashboard) y el 025 (eliminar /
salir) aparecen dos veces porque tienen una variante por rol.*
