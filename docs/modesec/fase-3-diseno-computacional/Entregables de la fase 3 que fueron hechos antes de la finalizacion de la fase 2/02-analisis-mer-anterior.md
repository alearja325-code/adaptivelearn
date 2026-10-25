# Análisis — qué se retoma del MER anterior de AdaptiveLearn, y por qué

**Fuente analizada:** `ADAPTATIVE-LEARN.pdf` (32 páginas, Capítulo VI —
Modelo Entidad-Relación), la misma que se declaró como "documento
recibido" en el informe de validación técnica (U1-01). Se revisa aquí
únicamente su **estructura de presentación**, no su contenido — el
contenido ya se descartó por completo (perfil adaptativo, mediaciones
pedagógicas, sin anclaje al MEN).

## Se retoma

- **Dividir el modelo en bloques pequeños**, cada uno con su propio
  título y una frase que explica qué representa. Ya lo aplicamos en los
  6 bloques de este modelo.
- **Notación Chen**: rectángulos para entidades, rombos para
  relaciones, elipses para atributos, cardinalidad escrita en cada
  extremo de la línea.
- **Llave primaria visualmente distinta** — elipse rellena de negro con
  texto blanco ("id (PK)"). Tomado directo de la referencia que
  compartió Alejandro (Institución/Usuario), no del PDF de 32 páginas.
- **Portada con metadata** (alcance, número de entidades, notación
  usada) antes de entrar a los diagramas — buena práctica de
  presentación, se agrega al documento final.
- **Leyenda visual de los símbolos** antes de mostrar los diagramas —
  para que alguien no técnico entienda qué significa cada forma antes
  de leerlos.

## No se retoma, con razón explícita

- **El color azul de las cajas de entidad.** En el documento original,
  todas las entidades son azules, sin distinción entre sí. Nuestro
  modelo necesita marcar algo que el documento viejo no necesitaba
  marcar: cuáles entidades administramos nosotros (blanco) y cuáles son
  dato oficial del MEN, solo referenciado (tono cálido claro). Mantener
  esa diferencia aporta información real; copiar el azul la habría
  borrado.
- **Cualquier contenido conceptual** — nombres de entidad, atributos,
  relaciones. Ya se descartó por completo, con evidencia, en el informe
  de validación técnica.

## Verificado contra la fuente real de MODESEC

Antes de seguir tratando esto como "Fase III", se confirmó contra el
texto original (no se asumió): en la sección "Modelado del sistema de
conocimiento/bases de datos" de Fase III, MODESEC dice textualmente:

> *"Si la opción es [base de datos relacional], se deberá crear un MER
> (Modelo Entidad Relación), un MR (Modelo relacional) basado en el MER
> y un diccionario de datos para los metadatos..."*

Confirma dos cosas: que el MER sí pertenece a Fase III (Diseño
Computacional), y el orden que sigue después de este documento —
Modelo Relacional, luego diccionario de datos.
