# Guía de movimiento

**Metodología:** MODESEC — Fase II, punto 6 (animación) de cada ventana.
**Escrita:** 2026-11-04. **Decisión:** ADR-041.
**Valores:** `tokens.json`, sección `movimiento`, y `03-tokens-diseno.md`,
sección "Movimiento".

---

## Por qué existe

Cada especificación dice **qué cambia** en su sección 6 (un hover, una
selección, un panel que se abre), pero ninguna dice **cómo** cambia: ni
cuánto dura ni con qué curva. Sin esa regla, en el código todo cambia de
golpe y las pantallas se sienten secas. Al revés, si cada pantalla
inventara su propia animación, el sistema se sentiría desordenado.

Esta guía es la regla común. **No agrega movimiento que las
especificaciones no pidan:** le da forma a lo que ya piden. Donde una
spec dice "sin animación compleja", sigue siendo cierto: aquí no hay
animaciones complejas, solo transiciones cortas.

## La filosofía, en una frase

> **El movimiento explica; no decora.**

AdaptiveLearn es una herramienta de trabajo para docentes y un espacio de
diagnóstico para estudiantes. No es un juego ni una vitrina: el
movimiento solo existe para que la persona entienda **qué pasó, de dónde
vino algo y a dónde fue**.

## Los 6 principios

1. **Explica un cambio.** Algo se mueve solo si cambió de estado (se
   eligió, se abrió, apareció, se fue). Nada se mueve "para llamar la
   atención" ni en bucle, salvo el indicador de carga.
2. **Es rápido.** Ninguna transición pasa de `280 ms`. La persona nunca
   espera a que termine una animación para seguir: puede hacer clic
   mientras ocurre.
3. **Es tranquilo.** Sin rebotes, sin elasticidad, sin giros ni
   sacudidas. **Lo que llega, llega suave y frena al llegar; lo que se
   va, se va al instante:** nadie espera a que algo termine de irse para
   seguir.
4. **Una cosa a la vez.** Cada acción mueve un solo elemento (o un solo
   grupo). No hay listas que aparecen fila por fila ni efectos en cadena.
5. **Los errores no castigan.** Un error **no tiembla ni parpadea**:
   aparece con la misma suavidad que cualquier mensaje. Quien se equivocó
   al escribir un código o una contraseña, o quien no muestra una
   evidencia, no recibe una sacudida. Es coherente con el resto del
   proyecto: nunca una nota, nunca un puntaje.
6. **Respeta a quien pide menos movimiento.** Si el sistema operativo
   tiene activado "reducir movimiento", desaparecen los desplazamientos y
   las escalas; quedan solo los cambios de color y de opacidad, en
   `120 ms` o menos (sección "Reducir movimiento").

## Los valores

Solo existen estos. El código no puede usar otros (lo comprueba
`npm run verificar:estilos`, igual que con los colores).

### Duraciones

| Nombre | Valor | Para qué |
|---|---|---|
| `rapida` | `120 ms` | Cambios de color, borde, opacidad: hover, foco, selección, habilitar un botón |
| `media` | `200 ms` | Algo cambia de tamaño o de lugar: expandir una card, cambiar de paso, un mensaje que aparece |
| `lenta` | `280 ms` | Algo grande entra a la pantalla: abrir un modal, llegar a una pantalla nueva |
| `giro` | `800 ms` | Una vuelta completa del spinner de la Ventana 024 (el único movimiento en bucle) |

### Curvas

| Nombre | Valor CSS | Para qué |
|---|---|---|
| `entrada` | `cubic-bezier(0.2, 0, 0, 1)` | Lo que **aparece**: arranca rápido y frena suave al llegar |
| `estandar` | `cubic-bezier(0.4, 0, 0.2, 1)` | Lo que **cambia sin entrar ni salir**: colores, una card que se expande |

### Distancias

Los desplazamientos son cortos, para sugerir una dirección, no para
recorrer la pantalla. Salen de la escala de espaciado (`tokens.json`):

| Nombre | Valor | Para qué |
|---|---|---|
| `minima` | `4px` | Un mensaje que aparece junto a lo que lo causó (M9) |
| `corta` | `8px` | Lo que aparece en su lugar: una pantalla, un modal |
| `paso` | `16px` | Cambiar de paso dentro de un modal: hacia la izquierda al avanzar, hacia la derecha al volver |

Escala de un modal al abrir: de `0.98` a `1`. Es la única escala del
sistema.

## Los patrones

Cada patrón dice qué ventanas lo usan. Si una ventana nueva necesita un
movimiento, primero se busca aquí; si no está, se agrega a esta guía
antes de programarlo.

| # | Patrón | Cómo se mueve | Ventanas |
|---|---|---|---|
| M1 | **Hover y foco** | Color de fondo, borde u opacidad (el `85%` de los botones primarios): `rapida`, `estandar` | Todas |
| M2 | **Habilitar o deshabilitar un botón** | El color del fondo cambia en `rapida`, `estandar` | 002–004, 014–019, 021, 022 |
| M3 | **Seleccionar una card u opción** | Fondo, borde y peso del texto en `rapida`, `estandar`. Sin escala ni sombra | 002, 003, 017, 021, 022 |
| M4 | **Abrir un modal** | El fondo oscuro aparece por opacidad en `media`; el panel, en `lenta` con `entrada`, por opacidad, subiendo `corta` (8px) y creciendo de `0.98` a `1` | 002, 005, 009, 010, 012, 013, 025, 026, 027 |
| M5 | **Cerrar un modal** | Desaparece al instante, en cuanto se pide (principio 3) | Las mismas |
| M6 | **Llegar a una pantalla** | El contenido aparece por opacidad, subiendo `corta` (8px), en `lenta` con `entrada`. La pantalla de fondo no se mueve | 001, 006, 014–019, 020–023 |
| M7 | **Cambiar de paso en un modal** | El contenido del paso que entra aparece por opacidad desde `paso` (16px) a la derecha al avanzar, o a la izquierda al volver, en `media` con `entrada`. La línea del stepper se completa en `media` | 002 → 003 → 004 |
| M8 | **Expandir o colapsar** | El chevron gira en `media`, `estandar`. Al expandir, el cuerpo aparece por opacidad, bajando `minima` (4px), en `media` con `entrada`; al colapsar, desaparece al instante (principio 3) | 003 (DBA), 009 (ítem), 010 (evidencia), 011 (estudiante), 027 |
| M9 | **Aparece un mensaje** (error, aviso, confirmación) | Por opacidad, bajando `minima` (4px) hasta su lugar, en `media` con `entrada`. **Nunca tiembla** (principio 5) | 014, 015, 018, 019, 004, 001 (aviso de estudiante) |
| M10 | **Cajas del código con error** | El borde pasa a rojo en `rapida`, `estandar`, las 6 a la vez. Sin sacudida | 005, 015 |
| M11 | **Cambio de texto en un botón** | El texto nuevo reemplaza al viejo por opacidad en `rapida` | 013 ("¡Código copiado!") |
| M12 | **Cargando** | El spinner gira una vuelta cada `giro` (800 ms), sin curva (lineal). El modal 024 entra como M4 | 024 |
| M13 | **Abrir una lista desplegable** | La lista aparece como M9 (opacidad, bajando `minima`, `media`, `entrada`); se cierra al instante. El chevron gira como en M8 | 003 (Select de Grado) |

## Lo que no se anima

Tan importante como lo anterior:

- **Los resultados del diagnóstico y del reporte** (010, 011, 023, 027):
  aparecen quietos. No hay barras que crecen, números que cuentan hacia
  arriba ni celebraciones. Un resultado es información para decidir, no
  un premio ni un castigo (principio 5).
- **Las listas que se filtran** (búsqueda, chips, grado): el resultado
  aparece al instante. Que la lista cambie mientras se escribe ya es la
  respuesta, y animarla la haría más lenta de leer.
- **El texto mientras se escribe**, el desplazamiento (scroll) y el
  cursor.
- **El cambio de pestaña** de la Vista Interna (006): el subrayado pasa
  a la pestaña activa como M1; el contenido cambia al instante, como dice
  su spec.

## Reducir movimiento

Con la preferencia del sistema operativo "reducir movimiento"
(`prefers-reduced-motion: reduce`):

- M4, M5, M6, M7 y M9 pierden el desplazamiento y la escala: quedan solo
  como cambio de opacidad, en `rapida`.
- M8 y M13 aparecen solo por opacidad, sin desplazamiento; el chevron cambia al instante.
- M12 (el spinner) sigue girando: es la única señal de que el sistema
  está trabajando. Su modal entra sin escala.
- M1, M2, M3, M10 y M11 no cambian: son cambios de color, que no mueven
  nada.

## Cómo se usa al programar

1. Los valores salen del tema generado desde `tokens.json`, nunca
   escritos a mano (`300ms`, `ease-in-out`).
2. Cada animación cita su patrón en un comentario (`// M7`), para que se
   pueda revisar contra esta guía.
3. Una ventana nueva que necesite un movimiento que no está aquí
   **primero agrega el patrón a esta guía** (con su razón) y después se
   programa.
