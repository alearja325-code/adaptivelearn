# AdaptiveLearn — instrucciones para Claude Code

Plataforma de diagnóstico por evidencias de aprendizaje, anclada a los
Derechos Básicos de Aprendizaje (DBA) del MEN de Colombia. Proyecto de
estudiantes de Licenciatura en Informática (Universidad de Córdoba),
diseñado con la metodología **MODESEC** (Fases I a III hechas; la Fase IV
es programar).

## Con quién trabajas

- **Alejandro** dirige el proyecto. **No es ingeniero de software.**
  Escríbele en español, en lenguaje simple, sin jerga sin explicar y sin
  omitir nada importante. Si algo es técnico, dilo con un ejemplo.
- Prefiere una recomendación clara a una lista de opciones; si hay una
  decisión que es suya, pregúntale, no la tomes por él.
- Hay otros integrantes del equipo que también trabajan aquí, a veces
  con Claude.

## Fuentes de verdad, en este orden

1. `docs/diseno/decisiones.md` — las decisiones (ADR) y su estado. Si
   una ADR dice "reemplazada" o "modificada por", manda la sucesora.
2. `docs/modesec/fase-2-diseno-multimedial/` — las 27 ventanas (qué hace
   cada pantalla).
3. `docs/modesec/fase-3-diseno-computacional/11-analisis-requerimientos.md`
   — los requerimientos (RF/RNF).
4. `docs/modesec/fase-3-diseno-computacional/16-modelo-entidad-relacion.md`
   — el modelo de datos vigente.
5. `docs/diseno/pendientes.md` — qué falta y por qué. **Léelo antes de
   empezar**.

La carpeta `fase-3-diseno-computacional/Entregables de la fase 3 que
fueron hechos antes de la finalizacion de la fase 2/` es un **borrador
viejo**: úsalo solo como antecedente, nunca como base.

## Reglas de trabajo

- **Cada afirmación cita su fuente** (ADR, ventana, RF, documento del
  MEN). Lo que no tiene fundamento se declara como vacío o como
  pregunta; **no se rellena en silencio**.
- **Los datos del MEN no se inventan ni se editan a mano.**
  `data/curriculo-men/` contiene los PDF oficiales y su normalización,
  pendiente de auditoría (`pendientes.md`, A12). La versión de un
  documento se lee de su contenido, nunca del nombre del archivo
  (ADR-033).
- **Los documentos generados no se editan a mano.** Si dicen "Archivo
  generado por X", cambia X y regenera. Esto aplica al MER, MR,
  diccionario, UML, endpoints (`16`-`18`, `12`-`15`, `20`), a los
  requerimientos (`11`) y al mapa de navegación y guión técnico (`28`,
  `29`).
- **Si tienes que tomar una decisión que nadie tomó**, tómala solo si es
  necesaria para terminar, y **declárala** (en el documento y en el
  mensaje del commit o del pull request) para que el equipo la
  confirme. Las ADR nuevas las aprueba Alejandro.
- **Nunca subas secretos**: `.env`, contraseñas, tokens, claves de API.
  `backend/.env.example` lista las variables, sin valores.
- **No trabajes directo sobre `main`**: crea una rama, y al terminar
  abre un pull request que diga qué cambió, por qué, qué decidiste por
  tu cuenta y qué quedó pendiente.

## Antes de dar algo por terminado: los verificadores

Todos deben pasar. Desde la raíz del repositorio:

```bash
(cd docs/diseno && python3 verificar_consistencia.py && python3 verificar_cadena.py)
(cd docs/modesec/fase-2-diseno-multimedial && python3 verificar_tokens.py [0-9][0-9]-spec*.md)
(cd docs/modesec/fase-2-diseno-multimedial/navegacion && python3 mapa_navegacion.py)
F3=docs/modesec/fase-3-diseno-computacional
(cd $F3/requerimientos && python3 requerimientos.py)
(cd $F3/mer && python3 _verificar_mer.py && python3 _verificar_vistas.py && python3 _verificar_mapa.py)
(cd $F3/modelo-relacional && python3 _verificar_mr_mer.py && python3 verificar_mr.py)
(cd $F3/uml && python3 _verificar_uml.py)
(cd $F3/api && python3 _verificar_api.py)
```

La cadena completa para **regenerar** la Fase III está en
`docs/modesec/fase-3-diseno-computacional/19-entrega-fase-3.md`, sección 3.
Requisitos: Python 3 con `lxml`, y Graphviz.

Si un verificador falla, primero averigua si el error es del documento o
del verificador; no lo "arregles" debilitando la comprobación.

## Mapa del repositorio

```
docs/diseno/            decisiones, visión, glosario, pendientes, verificadores
docs/modesec/           fase-1 (docx), fase-2 (ventanas), fase-3 (UML, MER, MR...)
docs/cursos/            entregables de los cursos DSE-1 y DSE-2
docs/encargos/          encargos escritos para sesiones de Claude Code
data/curriculo-men/     PDF oficiales de los DBA y su normalización
backend/                NestJS + MySQL (hoy: solo el acceso, incremento I1)
frontend/               vacío todavía
```

## Mensajes de commit

En español, diciendo qué cambió y por qué, y terminando con la línea de
coautoría de Claude.
