# Backend — AdaptiveLearn

API del sistema, en **NestJS** con **MySQL** (exigencia del curso DSE-2).

## Estado

Primer incremento del ciclo de vida (`I1 — Acceso`,
`docs/modesec/fase-3-diseno-computacional/10-proceso-desarrollo.md`):
registro e inicio de sesión de docentes y estudiantes, con JWT. El resto
de los subsistemas (experiencias, banco de preguntas, diagnóstico,
reporte) todavía no existe.

## Cómo ejecutarlo

Requisitos: Node.js y un servidor MySQL.

```bash
cd backend
npm install

# 1. Configuración: copiar la plantilla y completar los valores
cp .env.example .env

# 2. Base de datos: crear las tablas, en orden
#    sql/001_esquema_auth.sql
#    sql/002_alineacion_guia_y_seguridad.sql
#    (sql/reset-datos-prueba.sql borra y recarga datos de prueba)

# 3. Arrancar en modo desarrollo
npm run start:dev
```

| Comando | Qué hace |
|---|---|
| `npm run start:dev` | Arranca y se reinicia solo al guardar cambios |
| `npm run build` | Compila a `dist/` |
| `npm test` | Pruebas unitarias |
| `npm run test:e2e` | Pruebas de punta a punta |
| `npm run lint` | Revisión de estilo |

## Seguridad

- **El archivo `.env` nunca se sube** (está en `.gitignore`). Cada
  integrante tiene el suyo, con su propia contraseña de base de datos y
  su propio `JWT_SECRET`.
- Las contraseñas de los usuarios se guardan con hash, nunca en texto
  legible (RNF-08).

## Documentación relacionada

- Informe y colección de Postman del curso: `docs/cursos/dse-2-203453/`.
- Requerimientos del acceso (SUB-01): `docs/modesec/fase-3-diseno-computacional/11-analisis-requerimientos.md`.
- Pantallas del acceso: `docs/modesec/fase-2-diseno-multimedial/`, del `17` al `22`.
