# Encargo 01 — Catálogo curricular normalizado y estado de verificación del correo

**Para:** una sesión de Claude Code que trabaja sobre este repositorio.
**Escrito:** 2026-10-26, desde la sesión local de Alejandro, que tiene el
contexto completo. **Antes de empezar, lee `CLAUDE.md` (raíz) y
`docs/diseno/pendientes.md`.**

## 1. Qué hay que lograr, en una frase

Aplicar al modelo de datos de la Fase III dos pedidos del docente del
curso (revisión del 2026-10-22): **Área, Grado y Documento oficial como
entidades, con códigos sin tildes** (ADR-036), y **el estado de
verificación del correo** (ADR-037). Regenerar todo lo que depende del
modelo y dejar todos los verificadores en verde.

## 2. Lo que tienes que leer (en este orden)

1. `docs/modesec/fase-3-diseno-computacional/21-revision-docente-2026-10-22.md`
   — las notas del docente y su triaje. **Este encargo cubre R1 y R3.**
2. `docs/diseno/decisiones.md` — **ADR-033** (alcance y versiones de
   los PDF, con la tabla verificada), **ADR-036** y **ADR-037**.
3. `docs/modesec/fase-3-diseno-computacional/16-modelo-entidad-relacion.md`
   — el MER vigente. Su fuente es `mer/datos_mer.py`.
4. `docs/modesec/fase-3-diseno-computacional/19-entrega-fase-3.md`,
   sección 3 — la cadena para regenerar.

## 3. Qué cambiar

### 3.1 Tres entidades nuevas (ADR-036)

**ÁREA** — `codigo_area` (PK), `nombre`. Datos de referencia, del MEN:

| `codigo_area` | `nombre` | Valor de `area` en el JSON normalizado |
|---|---|---|
| `MAT` | Matemáticas | `matemáticas` |
| `LEN` | Lenguaje | `lenguaje` |
| `CN` | Ciencias Naturales | `ciencias naturales` |
| `CS` | Ciencias Sociales | `ciencias sociales` |

**GRADO** — `numero` (PK), `nombre`, `nivel`:

| `numero` | `nombre` | `nivel` |
|---|---|---|
| 1 a 5 | Primero, Segundo, Tercero, Cuarto, Quinto | básica primaria |
| 6 a 9 | Sexto, Séptimo, Octavo, Noveno | básica secundaria |
| 10, 11 | Décimo, Undécimo | media |

(Niveles de la educación formal, Ley 115 de 1994. Sin Transición: ADR-033.)

**DOCUMENTO_OFICIAL** — el PDF del MEN de donde se copiaron los DBA de
un área. Atributos: identificador, título, versión, año, páginas,
dirección oficial. Un documento por área en esta versión; **los datos
salen de la tabla de ADR-033, verificada contra los archivos oficiales**:

| Área | Versión | Año | Páginas | Dirección oficial (Colombia Aprende) | Archivo en `data/curriculo-men/pdfs/` |
|---|---|---|---|---|---|
| MAT | V.2 | 2016 | 88 | `http://www.colombiaaprende.edu.co/sites/default/files/files_public/2026-06/dba_matematicas-min.pdf` | `dba_matematicas_v2.pdf` |
| LEN | V.2 | 2016 | 56 | `http://www.colombiaaprende.edu.co/sites/default/files/files_public/2026-05/dba_lenguaje-min.pdf` | `dba_lenguaje_v2.pdf` |
| CN | V.1 | 2016 | 44 | `http://www.colombiaaprende.edu.co/sites/default/files/files_public/2026-05/dba_c.naturales-min.pdf` | `dba_ciencias_naturales_v1.pdf` |
| CS | **V.1** | 2016 | 52 | `http://www.colombiaaprende.edu.co/sites/default/files/files_public/2026-05/dba_c.sociales-v2_0.pdf` | `dba_ciencias_sociales_v2.pdf` |

**Cuidado con Ciencias Sociales:** su archivo se llama "v2" y el JSON
normalizado dice "V.2", pero **es V.1** (ADR-033). No copies la versión
del JSON ni del nombre del archivo.

### 3.2 DBA

- Salen los atributos `area` y `grado`. Entran tres relaciones:
  **pertenece a** (DBA N : 1 Área), **corresponde a** (DBA N : 1 Grado),
  **se copia de** (DBA N : 1 Documento oficial). Las tres, con
  participación total del lado del DBA.
- **Código nuevo:** `codigo_dba` = `ÁREA-GG-NN`, con ceros a la
  izquierda, sin tildes: `MAT-01-01`, `CS-11-05`. Se arma con el código
  del área, el grado y el `numero` que ya trae cada registro del JSON.
  Documenta la equivalencia con el identificador viejo
  (`matemáticas_1_dba_1` → `MAT-01-01`; `ciencias_naturales_2_dba_3` →
  `CN-02-03`).
- **Defecto conocido de los datos, no del modelo.** En el JSON hay 342
  DBA pero solo 329 identificadores distintos: la normalización de la V2
  asignó al grado anterior el primer DBA de algunas páginas (por ejemplo,
  hay dos `matemáticas_2_dba_1`; el segundo es el DBA 1 de 3°).
  `codigo_dba` **debe seguir siendo llave única**. No relajes el modelo
  para tolerar repetidos ni corrijas el JSON: se corrige en la auditoría
  (`pendientes.md`, A12). Si algún script tuyo carga el JSON completo y
  choca con esto, **decláralo** en el pull request en vez de esquivarlo.
  El MER (`16`, entidad DBA) dice hoy que `codigo_dba` se "verificó
  contra el JSON": cámbialo para que diga que el formato es el del JSON
  pero que los datos tienen este defecto.

### 3.3 El ciclo nuevo

DBA → Área y DBA → Documento oficial → Área forman un ciclo. El
verificador `mer/_verificar_mer.py` exige que **todo ciclo esté
declarado en `CICLOS` y cerrado por una regla**. Decláralo (C6) con su
restricción nueva: **el documento de un DBA es de su misma área**, y
ciérralo en el MR con la misma técnica que los ciclos C1 a C4 (llave
foránea compuesta). Si eliges otra forma de cerrarlo, decláralo.

### 3.4 CREDENCIAL (ADR-037)

`email_verificado` (sí/no) se reemplaza por **`estado_verificacion`**,
con dos valores: `procesando` y `verificado`. Una credencial de Google o
Microsoft nace `verificado`: ajusta la restricción RI-15, que hoy lo
dice con el sí/no.

### 3.5 Lo que NO debes hacer en este encargo

- **No quites `codigo_expira_en` ni `codigo_ultimo_envio`.** Es la nota
  R4 del docente, pendiente de su respuesta (pregunta P2).
- **No toques `backend/`.** Alinear el backend es otro encargo (Fase IV).
- **No edites `data/curriculo-men/`.** Está pendiente de auditoría.
- **No escribas ADR nuevas.** Si necesitas decidir algo que nadie
  decidió, decláralo en el documento afectado y en el pull request.

## 4. Dónde se nota el cambio (revisa todos)

| Archivo | Por qué |
|---|---|
| `mer/datos_mer.py` | Entidades, relaciones, ciclo C6, vistas (las tres nuevas van a la vista 2, *Currículo oficial*) |
| `modelo-relacional/datos_mr.py` | Tablas `area`, `grado`, `documento_oficial`; `dba` con sus FK; el tipo de `codigo_dba` (`COD_DBA`) cambia de formato en todas las tablas que lo usan; `estado_verificacion` |
| `modelo-relacional/pruebas_mr.py`, `verificar_mr.py`, `probar_mysql.py` | Pruebas de rechazo nuevas: un DBA sin área o con un documento de otra área, un `estado_verificacion` inválido, un código de DBA mal formado |
| `uml/datos_clases.py` | Clases Área, Grado y DocumentoOficial; DBA sin `area` ni `grado` como texto; el método de búsqueda de DBA (CU-31) recibe códigos |
| `uml/datos_objetos.py`, `uml/datos_crud.py`, `uml/datos_casos_uso.py` | El ejemplo de objetos usa el código nuevo; la matriz CRUD incluye las tablas nuevas (solo lectura); CU-31 filtra por área y grado |
| `api/datos_api.py` | Los endpoints del catálogo filtran por `codigo_area` y `numero` de grado |
| `16-…`, `17-…`, `18-…` | Se regeneran. Agrega el cambio a las tablas de "qué cambió" (`16` §13, `17` §10) citando ADR-036 y ADR-037, y en `16` §10 o donde corresponda, que esto responde a la revisión del 2026-10-22 |
| `19-entrega-fase-3.md` | Está escrito a mano: actualiza conteos y referencias |
| `docs/diseno/pendientes.md` | En "Entrada a Fase III", marca el punto 11 (Área y Grado) como hecho |

## 5. Cuándo está terminado

1. El MER muestra **ÁREA, GRADO y DOCUMENTO_OFICIAL**, el DBA sin
   `area`/`grado` como texto, el código `ÁREA-GG-NN`, el ciclo C6
   declarado y cerrado, y `estado_verificacion` en CREDENCIAL.
2. Corriste la cadena de regeneración de `19` §3 y **todos los
   verificadores de `CLAUDE.md` pasan**, incluido `verificar_mr.py`
   contra SQLite. Si tienes MySQL disponible, corre también
   `probar_mysql.py`; si no, dilo.
3. Si no hay Chrome o Edge para `herramientas/md_a_pdf.py`, no
   regeneres los PDF y dilo.

## 6. Cómo entregarlo

- Trabaja en la rama **`encargo-01-catalogo-curricular`**.
- Abre un **pull request hacia `main`**, sin hacer merge. En la
  descripción, en español simple:
  1. qué cambió, entidad por entidad;
  2. los resultados de los verificadores (copia las líneas de
     resultado);
  3. **qué decidiste por tu cuenta** y por qué;
  4. qué quedó pendiente.
- El equipo lo revisa en la sesión local antes de unirlo.
