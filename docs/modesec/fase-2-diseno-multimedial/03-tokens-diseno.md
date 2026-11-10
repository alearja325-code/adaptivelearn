# 3. Tokens de Diseño — Base para la Ventana Estándar

**Origen:** redefinición de `mvp/Auditoria/04_diseno_interfaz/00-MASTER-design-tokens.md`
(sistema anterior, basado en la plantilla genérica "Miyama Graphics"),
validada con el método de la skill de visualización de datos — nada de
esto se eligió a ojo; cada color se comprobó con un script antes de
aceptarse.

## Qué se revisó y pasó sin cambios, con su razón

No se cambia por costumbre — cada uno se revisó con criterio y se
sostiene. Valores exactos, no solo nombres:

### Tinta y superficies

| Token | Valor hex | Uso |
|---|---|---|
| Canvas | `#F7F6F3` | Fondo general, detrás de los paneles |
| Surface 0 | `#FFFFFF` | Paneles, cards, inputs |
| Surface 1 | `#FAFAF8` | Hover de controles, botones secundarios |
| Surface 2 | `#F5F3EE` | Fondos neutros, badge "Borrador", estado activo del nav |
| Border | `#E7E7E7` | Bordes de cards, inputs, divisores |
| Primary Ink | `#111111` | Texto principal, títulos, badge "Publicada" (fondo) |
| Strong | `#222222` | Texto fuerte secundario |
| Secondary | `#555555` | Texto descriptivo, navegación inactiva |
| Muted | `#888888` | Placeholders, íconos inactivos, metadata |
| Disabled | `#BDBDBD` | Elementos deshabilitados |

### Espaciado (base 4px)

`4px · 8px · 12px · 16px · 24px · 32px · 40px · 48px · 64px · 80px · 96px · 128px`

Es el estándar de facto de la industria (mismo sistema que usan Tailwind
y Material) — no hay razón real para cambiarlo.

**Regla de uso — `12px` vs. `16px` dentro y entre cards.** Se ha
aplicado igual en cada ventana (Dashboard, Crear Experiencia, Vista
Interna) sin excepción, pero nunca quedó escrita — se documenta acá
para no depender de reconstruirla a mano cada vez:

- **`12px`** — filas horizontales de elementos chicos/inline dentro de
  un componente compacto (badge + título + metadata + chevron de un
  Row Card; radio + badge + enunciado + ícono de una fila colapsada;
  filas de botones de footer) — y espaciado **entre hermanos** en una
  lista vertical (entre cards de una lista, no dentro de una card).
- **`16px`** — la pila vertical de secciones dentro de **una sola**
  card (el nivel más externo de una card con varias partes) — en estos
  casos el Gap tiende a igualar el Padding de esa misma card, para que
  el ritmo interno quede igual al del borde. También se usa en filas
  horizontales de elementos **grandes** (cards de área de `200px`) —
  a mayor tamaño del elemento, mayor el gap, proporcional.

En corto: `12` para agrupar piezas chicas o muchas, `16` para separar
secciones grandes o pocas.

### Radios de borde

| Paso | Valor | Uso |
|---|---|---|
| XS | `4px` | Badges de estado |
| S | `8px` | Controles seleccionables (nav items, filter chips) |
| M | `12px` | Botones, inputs |
| L | `16px` | Tarjetas de contenido (Row Card) |
| XL | `24px` | Contenedores macro (paneles, modales) |
| Full | `999px` | Avatares, íconos circulares |

Progresión convencional, sin problema real.

### Alturas de control

| Token | Valor | Uso |
|---|---|---|
| CTA | `48px` | Botones primarios/secundarios de confirmación |
| Input | `44px` | Campos de búsqueda, selects, nav items |
| Compact | `40px` | Filter chips |
| Tiny | `32px` | Botones diminutos dentro de tarjetas |

Bien elegido, no arbitrario: 44px es el mínimo de zona táctil de las
guías de Apple (HIG), 48px es lo que recomienda Material — coincide con
estándares reales de accesibilidad táctil, no se inventó.

## Tipografía — sí se corrige, con evidencia

Dos problemas reales, no de gusto:

1. **La familia tipográfica (`Noto Sans JP Rounded`) es japonesa**,
   heredada sin pensarlo de la plantilla base (Miyama Graphics). Carga
   miles de glifos CJK que un producto 100% en español nunca usa — peso
   de descarga innecesario, sin ninguna ventaja para nuestro idioma.
2. **El tamaño base de texto (14px) es más chico de lo recomendado** para
   lectura cómoda de adultos (Material y GOV.UK Design System usan 16px
   como base) — relevante para un docente leyendo enunciados
   curriculares densos, no solo botones cortos.

**Fuente nueva:** pila CSS `system-ui, -apple-system, "Segoe UI", Arial,
sans-serif` — sin descarga, carga instantánea, cubre español sin peso
muerto. Esta pila es para cuando el diseño se convierta en código web; el
navegador la resuelve solo.

**En Figma (ahora), la fuente a elegir es: `Inter`** — viene instalada
por defecto, sin descargar nada, y es el reemplazo estándar de la
industria para "fuente del sistema" en herramientas de diseño: muy
cercana en forma a San Francisco (Mac) y Segoe UI (Windows), que es
justo lo que la pila CSS busca en la web.

**Escala reescalada:**

| Nivel | Antes | Ahora |
|---|---|---|
| H1 | 32/40 Bold | 32/40 Bold *(sin cambio)* |
| H2 | 24/32 Bold | 24/32 Bold *(sin cambio)* |
| H3 | 20/28 Medium | 20/28 Medium *(sin cambio)* |
| H4 | 16/24 Bold | 18/26 Bold *(sube, para no empatar con el nuevo Body)* |
| Body | 14/22 Regular | **16/24 Regular** |
| Button/Input | 14/20 Medium | **16/22 Medium** |
| Caption | 12/18 Regular | 13/20 Regular |
| Badge Label | 11/14 Bold | **12/16 Bold** *(11px es difícil de leer incluso en una etiqueta corta)* |

## Qué se redefine en color, y por qué

El sistema anterior usaba 4 colores pastel (amarillo, rosa, menta, azul)
para estados — heredados sin verificar de la plantilla base "Miyama
Graphics". Validados como conjunto categórico, **fallan**: se leen casi
grises entre sí (croma muy bajo), y dos de ellos (menta vs. rosa) son
prácticamente indistinguibles para daltonismo deuteranopia (ΔE 2.9, muy
por debajo del mínimo de 8 que exige el método).

```
node scripts/validate_palette.js "#FFE59A,#FFB5C1,#B7E1D1,#A9D3FF" --mode light --surface "#F7F6F3"
→ FAIL en 4 de 5 chequeos (banda de luminosidad, piso de croma,
  separación CVD, piso de visión normal)
```

Además, esos 4 colores estaban atados a estados que ya no existen en
esta versión (Draft/Activo/Pendiente/Error del flujo viejo). Se
reemplazan por los 3 estados reales que sí definimos hoy — el resultado
de una evidencia (ADR-008):

## Paleta de estado — Resultado de evidencia

| Estado | Color | Hex | Evidencia |
|---|---|---|---|
| **Muestra** | Azul apagado | `#29578E` | — |
| **No muestra** | Naranja apagado | `#7A391F` | — |
| **No concluyente** | Gris neutro | `#52514e` | deliberadamente sin croma — el estado *debe* leerse apagado, no vívido |
| **Sin concluir** | Muted (reutilizado) | `#888888` | agregado por ADR-022 — **no es un color nuevo**: es el token Muted que ya existía para metadata e íconos inactivos, que es exactamente el registro correcto para "todavía no hay nada que mostrar". Contraste `3.5:1` sobre blanco: no alcanza AA para texto normal, pero **sí** para texto grande (umbral `3:1`), que es el único uso que tiene — el número `24/32` Bold de la card de estado y el punto de `8×8px` de la leyenda. No se usa para texto de párrafo. |

**Revisado (Ventana 010, Reporte):** los valores originales
(`#2a78d6` Azul, `#eb6834` Naranja) se sintieron, al verlos
implementados, más vívidos que el resto del sistema — el proyecto
viene usando una paleta deliberadamente apagada (Informativo, Error),
y estos dos rompían ese registro. Se verificó con HSL + fórmula de
contraste WCAG (no con `validate_palette.js`, que no está en el
repositorio — se calculó directo):

```
Color            Saturación  Luminosidad  Contraste vs #FFF
Informativo      70%         50%          7.1:1
Error            70%         35%          8.31:1
Azul (original)  68%         50%          4.42:1  <- más "claro" que Informativo
Naranja(original)82%         56%          3.2:1   <- el más saturado y claro del sistema
```

Se oscurecieron ambos, mismo tono (hue), hasta calcar el contraste de
Informativo/Error:
- Azul `#2a78d6` → `#29578E` — contraste `7.37:1` (≈ Informativo `7.1:1`).
- Naranja `#eb6834` → `#7A391F` — contraste `8.63:1` (≈ Error `8.31:1`).

Gris no cambia — ya estaba en el registro correcto (2% de saturación).
No se pasó a escala de negros pura: las barras de Reporte necesitan 3
categorías distinguibles a simple vista, y dos grises entre sí son más
difíciles de diferenciar que un color apagado contra un gris neutro.

**Decisión deliberada de valencia:** no se usa verde=bien / rojo=mal. Todo
el diseño de esta versión evita lenguaje de certeza ("ni un acierto ni un
error prueban nada por sí solos", ADR-008) — colorear "no muestra" en rojo
de alarma contradiría ese principio visualmente, aunque el texto sea
cuidadoso. Azul/naranja son neutros en valencia: distinguibles, sin
implicar juicio.

## Color informativo — evidencia que no aplica al formato

Ventana 003 (Crear Experiencia, Paso 2) necesita marcar, dentro de la
lista de Evidencias de un DBA, cuáles no aplican al formato cerrado
(QA-014). No podía reutilizar ninguno de los 3 colores de "Resultado
de evidencia" de arriba — son de un concepto distinto (el resultado de
un diagnóstico ya aplicado, no la aplicabilidad de una evidencia al
formato), y usar el mismo color para dos cosas distintas rompería la
regla de un color = un significado.

| Token | Color | Hex | Uso |
|---|---|---|---|
| Informativo | Violeta | `#6D28D9` | Texto de evidencias que no aplican al formato cerrado (Ventana 003, Paso 2) |

Verificación de contraste (cálculo WCAG 2.1, fórmula de luminancia
relativa, no a ojo):

```
contraste(#6D28D9, #FFFFFF) = 7.1:1  → pasa AAA para texto normal (mínimo 4.5:1 AA / 7:1 AAA)
```

No se corrió `validate_palette.js` (separación CVD entre colores de un
mismo conjunto categórico) porque no aplica aquí: este violeta no
convive en pantalla con los 3 colores de "Resultado de evidencia" — son
features distintas (creación de experiencia vs. reporte de diagnóstico
ya aplicado) que un usuario nunca ve una junto a la otra. El criterio
que sí aplica — contraste de texto sobre fondo blanco — se verificó y
pasa con margen amplio.

## Color de error — primer uso en el sistema

Ventana "Unirse con código" necesita comunicar un código inválido o de
una experiencia que todavía no está publicada — un concepto de
validación de formulario, distinto tanto de los 3 colores de "Resultado
de evidencia" como del violeta "Informativo" de arriba. Tres conceptos
distintos, tres colores distintos — misma regla de siempre.

| Token | Color | Hex | Uso |
|---|---|---|---|
| Error | Rojo | `#991B1B` | Mensaje de código inválido / experiencia no disponible (Ventana "Unirse con código") |

```
contraste(#991B1B, #FFFFFF) = 8.31:1  → pasa AAA para texto normal
```

Mismo criterio que el violeta: no convive en pantalla con los otros 4
colores de estado/informativo (son features distintas), así que el
chequeo de separación CVD categórica no aplica — solo el contraste de
texto sobre fondo blanco, que se verificó y pasa con margen amplio.

## Resuelto — la clasificación por umbral de Reporte no necesitó colores nuevos

*(Esta sección decía "Pendiente, para cuando se diseñe Reporte" y listaba
4 categorías —"brecha extendida", "brecha aislada", "sin brecha
aparente", "datos insuficientes"— que hoy ya no existen así. Reporte se
diseñó (Ventana 010) y la sección quedó obsoleta sin que nadie la
actualizara; se corrige el 2026-08-26.)*

Dos cosas cambiaron respecto a lo que esta sección anticipaba:

1. **Son 3 categorías, no 4.** ADR-017 fusionó "brecha extendida" y
   "brecha aislada" en **"Brecha aparente"** — esa división de severidad
   era la parte menos fundamentada del diseño original. Quedan: Brecha
   aparente · Datos insuficientes · Sin brecha aparente. (ADR-023 después
   amplió qué cuenta hacia el umbral de "Datos insuficientes", sin
   agregar categorías.)
2. **No hicieron falta colores nuevos.** Las 3 categorías reutilizan los
   colores de la Paleta de estado de arriba, aplicados al **texto** del
   separador de grupo, no a un fondo: Brecha aparente → `#7A391F`, Datos
   insuficientes → `#52514E`, Sin brecha aparente → `#29578E`. Se evaluó
   crear 3 tintes de fondo propios y se descartó — habría sido el primer
   badge del sistema con fondo variable (ver `13-spec-modal-reporte.md`,
   Correcciones posteriores #1).

## Filosofía de separadores (consolidada 2026-08-29)

Existen 2 separadores ya construidos — `12-spec-modal-banco-items.md`
§2.3 (por Evidencia) y `13-spec-modal-reporte.md` §2.3 (por categoría
de brecha) — y un 3.º en curso, por estado del veredicto (ADR-022),
que va a vivir dentro de `14-spec-vista-interna-estudiantes.md` §2.3,
Estado 3 (todavía sin escribir). Cada uno se construyó por precedente
del anterior, nunca con una regla escrita de por medio. Se consolida
acá, después de revisar **por qué** cada uno agrupa como agrupa, no
solo cómo.

**Propósito.** Un separador impone, sobre una lista plana y
potencialmente larga, la dimensión de agrupación que responde la
pregunta que el usuario se está haciendo en esa pantalla — no
cualquier atributo disponible en los datos, el que sirve a la tarea.

La prueba de que esto es real y no solo una racionalización: Reporte
**no** agrupa por evidencia, que sería la agrupación obvia (los datos
vienen por evidencia) — agrupa por categoría de brecha, porque ahí la
pregunta del docente es "¿dónde tengo que intervenir?". El banco de
ítems, con los mismos datos-fuente disponibles (evidencias), sí agrupa
por evidencia, porque su pregunta es "¿están bien las preguntas de
esta evidencia?", una por una. Misma clase de dato, agrupación
distinta, porque la tarea es distinta.

**Reglas derivadas de ese propósito:**

- **Qué agrupar** — la dimensión que responde la pregunta de esa
  pantalla, no la agrupación más obvia de los datos disponibles.
- **Orden de los grupos** — prioridad respecto a esa pregunta: urgencia
  primero cuando la tarea es "dónde intervenir" (Reporte, Estudiantes);
  orden neutral cuando no hay urgencia que ordenar (banco de ítems
  sigue el orden natural de las evidencias del DBA — ninguna evidencia
  es "más urgente" que otra).
- **Nombre solo, o nombre + explicación** — nombre solo si se entiende
  sin ayuda (una evidencia se explica con su propio enunciado); nombre
  + explicación de una línea si es una categoría interna del sistema
  que no se auto-explica (brecha, estado del veredicto).
- **Color, y por qué solo a veces** — el separador de evidencia del
  banco de ítems **no** usa color (`#111111` plano): "evidencia" es una
  etiqueta neutra, no hay nada bueno o malo que colorear. El color solo
  aparece cuando la dimensión de agrupación **es** un estado cualitativo
  con paleta ya establecida (brecha, veredicto) — nunca para
  agrupaciones neutras. Cuando aplica, vive en el texto del nombre,
  nunca en un fondo, nunca repetido en cada card de la lista.
- **Forma, constante sin importar el propósito** — separador y sus
  elementos son hermanos directos de una lista plana (Auto Layout
  Vertical, mismo Gap de toda la lista) — nunca un contenedor de grupo
  aparte, nunca caja/fondo/padding propios.
- **Grupos vacíos se omiten** — un separador solo aparece si al menos
  un elemento cae en ese grupo.

## Movimiento (agregado 2026-11-04, ADR-041)

Hasta esta fecha el sistema solo definía **qué** cambia en cada ventana
(sección 6 de cada spec), no **cómo**. La filosofía, los principios y los
13 patrones están en `31-guia-de-movimiento.md`. Aquí, solo los valores
(los mismos de `tokens.json`, sección `movimiento`):

- **Duraciones:** `rapida` 120 ms (color, borde, opacidad) · `media`
  200 ms (tamaño o lugar) · `lenta` 280 ms (un modal o una pantalla que
  entra) · `giro` 800 ms (una vuelta del spinner, lineal).
- **Curvas:** `entrada` `cubic-bezier(0.2, 0, 0, 1)` (lo que aparece) ·
  `estandar` `cubic-bezier(0.4, 0, 0.2, 1)` (lo que cambia). No hay curva
  de salida: lo que se va, se va al instante.
- **Distancias:** `minima` `4px` · `corta` `8px` · `paso` `16px` (de la
  escala de espaciado; no son medidas nuevas).
- **Escala del modal al abrir:** `0.98` → `1`. Es la única del sistema.
