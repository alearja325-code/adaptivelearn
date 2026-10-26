# 1. Selección de la herramienta de desarrollo

**Metodología:** MODESEC — Fase IV, Producción, primera etapa.
**Fecha:** 2026-10-26.

MODESEC: *«En la fase de producción se agrupan todos los materiales
obtenidos en el desarrollo de las fases anteriores, por tal motivo es
aquí donde se realiza la implementación de todos los documentos
obtenidos en las fases de diseños […]»*, y como primer paso: *«Para
llevar a cabo la codificación es necesario seleccionar una herramienta
o lenguaje de programación que sea acorde con las especificaciones del
software desarrollado, es importante tener en cuenta que la persona
encargada de la codificación domine la herramienta o lenguaje
seleccionado para que se facilite la programación de las actividades y
contenidos del software, permitiendo el cumplimiento de las metas
propuestas en términos de eficacia y eficiencia.»*

## 1. Los dos criterios de MODESEC, aplicados

| Criterio | Cómo se aplica en este proyecto |
|---|---|
| **Acorde con las especificaciones** | Una aplicación web, solo para computador (ADR-025), detrás de un inicio de sesión; 27 ventanas con componentes que se repiten (Fase II); un sistema de diseño cerrado (`tokens.json`); un backend que expone una API (`20-catalogo-endpoints.md`) |
| **Que quien programa domine la herramienta** | Nadie del equipo es programador profesional: se programa con asistencia de IA. Se elige lo **más usado y documentado**, en **un solo lenguaje** para todo el sistema, para que el equipo pueda leerlo, probarlo y explicarlo |

## 2. La selección

| Parte | Herramienta | Quién la decidió | Por qué |
|---|---|---|---|
| **Backend** | NestJS (TypeScript) | El curso DSE-2 | Guía del curso; el incremento I1 (acceso) ya está construido así (`backend/`) |
| **Base de datos** | MySQL | El curso DSE-2 | El modelo relacional se probó en MySQL 8.4 (`17`, `probar_mysql.py`). Compatible con MariaDB por diseño; queda probarlo al integrar (`19` §4) |
| **Frontend** | **React + Vite + TypeScript + Tailwind** | El equipo — **ADR-038** | Ver sección 3 |
| **Íconos** | Lucide | El equipo — `30-indice-recursos.md` | Libre, completa, ya usada en las especificaciones |
| **Pruebas** | Vitest | El backend ya la usa | La misma herramienta en las dos partes |

### Herramientas de apoyo

| Herramienta | Para qué |
|---|---|
| **Git y GitHub** | Historial de cambios y trabajo en equipo (`alearja325-code/adaptivelearn`) |
| **Claude Code** (local y en la nube) | Asistencia de programación, con las reglas de `CLAUDE.md` |
| **Figma** | El prototipo visual de las 27 ventanas |
| **Postman** | Probar la API del backend (colección en `docs/cursos/dse-2-203453/`) |
| **Python 3 + Graphviz** | Los verificadores y generadores de la documentación |

## 3. El frontend, en detalle (ADR-038)

| Pieza | Qué es, en simple | Por qué esta |
|---|---|---|
| **React** | Construye las pantallas por piezas reutilizables (componentes) | La más usada; donde más ejemplos y ayuda existen. Las 27 ventanas ya están pensadas por componentes |
| **TypeScript** | JavaScript que avisa de errores antes de ejecutar | El mismo lenguaje del backend |
| **Vite** | Arranca y empaqueta el proyecto | Simple y rápida |
| **Tailwind** | Aplica estilos desde un archivo de configuración | Se configura **solo con `tokens.json`**: el código no puede usar un color o una medida fuera del sistema de diseño |

**Descartadas:** Next.js (pensada para páginas públicas o generadas en
el servidor; esta aplicación está detrás de un inicio de sesión y ya
tiene backend), Angular (más difícil de aprender, menos ayuda), Vue
(válida, pero con menos ejemplos y sin la experiencia previa del
equipo), HTML y JavaScript a mano (demasiado trabajo para 27
pantallas).

## 4. Lo que sigue en la Fase IV

MODESEC ordena la producción así; el ciclo incremental
(`fase-3-diseno-computacional/10-proceso-desarrollo.md`) dice en qué
orden se construye:

| Etapa de MODESEC | En este proyecto |
|---|---|
| **Selección de herramienta** | Este documento |
| **Codificación** | Por incrementos: **I1** acceso (backend iniciado; falta alinearlo con el MER y con la revisión del docente, y su frontend), **I2** experiencia y banco, **I3** diagnóstico, **I4** reporte |
| **Presentación del prototipo** | Al cerrar cada incremento, una demostración funcionando |
| **Evaluación del prototipo** | Con docentes, no con estudiantes reales (ADR-025, ADR-029) |
| **Manual de usuario** | Al final, uno para el docente y uno para el estudiante |
