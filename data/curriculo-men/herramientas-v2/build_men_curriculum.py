#!/usr/bin/env python3
"""
Builds a traceable MEN curriculum dataset from downloaded official PDFs.

The parser is intentionally conservative. MEN PDFs use multi-column layouts, so
some extracted text appears out of visual order. This script only promotes
records where it can detect a numbered reference plus an "Evidencias de
aprendizaje" block. Everything remains traceable to the original source.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SOURCES = DATA / "men_sources"
PDF_DIR = SOURCES / "pdfs"
RAW_DIR = SOURCES / "raw_text"
OUT_DIR = SOURCES / "normalized"
LEGACY_DIR = DATA / "legacy_curriculum_backups"


@dataclass(frozen=True)
class SourceConfig:
    source_id: str
    file_name: str
    area_key: str
    area_name: str
    kind: str
    title: str


DBA_SOURCES = [
    SourceConfig(
        "dba_matematicas_v2",
        "dba_matematicas_v2.pdf",
        "matemáticas",
        "Matemáticas",
        "DBA",
        "Derechos Básicos de Aprendizaje - Matemáticas V.2",
    ),
    SourceConfig(
        "dba_lenguaje_v2",
        "dba_lenguaje_v2.pdf",
        "lenguaje",
        "Lenguaje",
        "DBA",
        "Derechos Básicos de Aprendizaje - Lenguaje V.2",
    ),
    SourceConfig(
        "dba_ciencias_naturales_v1",
        "dba_ciencias_naturales_v1.pdf",
        "ciencias naturales",
        "Ciencias Naturales",
        "DBA",
        "Derechos Básicos de Aprendizaje - Ciencias Naturales V.1",
    ),
]

ENGLISH_SOURCE = SourceConfig(
    "curriculo_sugerido_ingles_6_11",
    "curriculo_sugerido_ingles_6_11.pdf",
    "inglés",
    "Inglés como lengua extranjera",
    "Currículo sugerido",
    "Esquema Curricular Sugerido de Inglés para grados 6° a 11°",
)

SOCIAL_STUDIES_SOURCE = SourceConfig(
    "dba_ciencias_sociales_v2",
    "dba_ciencias_sociales_v2.pdf",
    "ciencias sociales",
    "Ciencias Sociales",
    "DBA",
    "Derechos Básicos de Aprendizaje - Ciencias Sociales V.2",
)

EBC_SOURCE = SourceConfig(
    "estandares_basicos_competencias_lenguaje_matematicas_ciencias_ciudadanas",
    "estandares_basicos_competencias_lenguaje_matematicas_ciencias_ciudadanas.pdf",
    "estandares basicos",
    "Lenguaje, Matemáticas, Ciencias y Ciudadanas",
    "Estándar Básico de Competencia",
    "Estándares Básicos de Competencias en Lenguaje, Matemáticas, Ciencias y Ciudadanas",
)

GUIDE22_SOURCE = SourceConfig(
    "estandares_ingles_guia_22",
    "estandares_ingles_guia_22.pdf",
    "inglés",
    "Inglés como lengua extranjera",
    "Estándar Básico de Competencia - Inglés",
    "Guía No. 22 Estándares Básicos de Competencias en Lenguas Extranjeras: Inglés",
)

ENGLISH_MANUAL_TEXT_FIXES = {
    "ingles_6_curriculo_5": "Reconoce información específica relacionada con objetos, personas y acciones.",
    "ingles_7_curriculo_3": "Reconoce información específica en textos cortos orales y escritos sobre temas de interés general.",
    "ingles_7_curriculo_7": "Expresa sus emociones y sentimientos sobre una situación o tema específico de su entorno familiar o escolar, presentando sus razones de forma clara y sencilla.",
    "ingles_8_curriculo_7": "Identifica el propósito, las partes y tipo de textos en una lectura o audio cortos y los comparte con sus compañeros.",
    "ingles_9_curriculo_1": "Distingue información general y específica en textos de opinión y discusiones orales y escritos sobre temas conocidos.",
    "ingles_10_curriculo_1": "Identifica la intención de textos orales y escritos de mediana longitud relacionados con temas de interés general y de su entorno académico y la comparte con otros.",
}

SOURCE_METADATA = {
    "dba_matematicas_v2": {
        "url": "https://www.colombiaaprende.edu.co/sites/default/files/files_public/2022-06/DBA_Matematicas-min.pdf",
        "official_page": "https://www.colombiaaprende.edu.co/contenidos/coleccion/derechos-basicos-de-aprendizaje",
        "source_label": "MEN Colombia / Colombia Aprende — DBA Matemáticas V.2",
    },
    "dba_lenguaje_v2": {
        "url": "https://www.colombiaaprende.edu.co/sites/default/files/files_public/2022-06/DBA_Lenguaje-min.pdf",
        "official_page": "https://www.colombiaaprende.edu.co/contenidos/coleccion/derechos-basicos-de-aprendizaje",
        "source_label": "MEN Colombia / Colombia Aprende — DBA Lenguaje V.2",
    },
    "dba_ciencias_naturales_v1": {
        "url": "https://www.colombiaaprende.edu.co/sites/default/files/files_public/2022-06/DBA_C.Naturales-min.pdf",
        "official_page": "https://www.colombiaaprende.edu.co/recurso-coleccion/explora-derechos-basicos-de-aprendizaje-dba-ciencias-naturales",
        "source_label": "MEN Colombia / Colombia Aprende — DBA Ciencias Naturales V.1",
    },
    "dba_ciencias_sociales_v2": {
        "url": "https://www.colombiaaprende.edu.co/sites/default/files/files_public/2022-06/DBA_C.Sociales-V2.pdf",
        "official_page": "https://www.colombiaaprende.edu.co/recurso-coleccion/explora-derechos-basicos-de-aprendizaje-dba-ciencias-sociales",
        "source_label": "MEN Colombia / Colombia Aprende — DBA Ciencias Sociales V.2",
    },
    "estandares_basicos_competencias_lenguaje_matematicas_ciencias_ciudadanas": {
        "url": "https://www.mineducacion.gov.co/1621/articles-340021_recurso_1.pdf",
        "official_page": "https://www.mineducacion.gov.co/portal/Preescolar-basica-y-media/Referentes-de-calidad/340021:Estandares-Basicos-de-competencia",
        "source_label": "MEN Colombia — Estándares Básicos de Competencias",
    },
    "estandares_ingles_guia_22": {
        "url": "https://www.mineducacion.gov.co/1780/articles-115174_archivo_pdf.pdf",
        "url_parte_2": "https://www.mineducacion.gov.co/1780/articles-115174_archivo_pdf1.pdf",
        "official_page": "https://www.mineducacion.gov.co/portal/men/Publicaciones/Guias/115174:Guia-No-22-Estandares-Basicos-de-Competencias-en-Lenguas-Extranjeras-Ingles",
        "source_label": "MEN Colombia — Guía No. 22 Estándares Básicos de Competencias en Lenguas Extranjeras: Inglés",
    },
    "curriculo_sugerido_ingles_6_11": {
        "url": "https://eco.colombiaaprende.edu.co/wp-content/uploads/2021/09/Esquema-Curricular-Espa_RevMEN.pdf",
        "official_page": "https://eco.colombiaaprende.edu.co/2021/09/07/esquema-circular-sugerido/",
        "source_label": "MEN Colombia / Colombia Aprende — Currículo sugerido Inglés 6° a 11°",
    },
}


def run_pdftotext_raw(source: SourceConfig) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    pdf = PDF_DIR / source.file_name
    if not pdf.exists():
        raise FileNotFoundError(f"Missing PDF: {pdf}")
    out = RAW_DIR / f"{source.source_id}.txt"
    subprocess.run(["pdftotext", "-raw", str(pdf), str(out)], check=True)
    return out


def run_pdftotext_bbox_layout(source: SourceConfig) -> Path:
    pdf = PDF_DIR / source.file_name
    if not pdf.exists():
        raise FileNotFoundError(f"Missing PDF: {pdf}")
    tmp = tempfile.NamedTemporaryFile(prefix=f"{source.source_id}_", suffix=".html", delete=False)
    tmp.close()
    out = Path(tmp.name)
    subprocess.run(["pdftotext", "-bbox-layout", str(pdf), str(out)], check=True)
    return out


def clean_text(text: str) -> str:
    text = text.replace("\x0c", "\n")
    text = re.sub(r"[\x00-\x08\x0b\x0e-\x1f]", " ", text)
    text = text.replace("º", "°")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def normalize_sentence(lines: list[str]) -> str:
    text = " ".join(line.strip() for line in lines if line.strip())
    text = re.sub(r"\s+", " ", text).strip()
    return text


def grade_markers(text: str) -> list[tuple[int, str]]:
    markers: list[tuple[int, str]] = []
    patterns = [
        r"Grado\s+(\d{1,2})\s*[°º]",
        r"GRADO SUGERIDO:\s*(\d{1,2})\s*[°º]",
    ]
    for pat in patterns:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            n = int(m.group(1))
            if 1 <= n <= 11:
                markers.append((m.start(), f"{n}°"))
    markers.sort()
    return markers


def nearest_grade(pos: int, markers: list[tuple[int, str]]) -> str | None:
    if not markers:
        return None
    # Multi-column extraction sometimes places the grade header slightly after
    # the first item on a page. Nearest marker is more reliable than previous.
    near = min(markers, key=lambda item: abs(item[0] - pos))
    return near[1] if abs(near[0] - pos) < 4500 else None


def extract_evidence_lines(block: str) -> list[str]:
    lines = [ln.strip() for ln in block.splitlines()]
    evidences: list[str] = []
    current: list[str] = []
    bullet_re = re.compile(r"^[mqu•]\s+(.+)$", re.IGNORECASE)
    stop_re = re.compile(r"^(Ejemplo|Derechos Básicos|[A-Za-z]+ DBA_Final|Matemáticas • Grado|Lenguaje • Grado|Grado \d)", re.IGNORECASE)
    for line in lines:
        if not line:
            continue
        if stop_re.search(line):
            break
        bullet = bullet_re.match(line)
        if bullet:
            if current:
                evidences.append(normalize_sentence(current))
            current = [bullet.group(1)]
        elif current:
            current.append(line)
    if current:
        evidences.append(normalize_sentence(current))
    return [e for e in evidences if len(e) > 16]


def extract_dba_records(source: SourceConfig) -> list[dict]:
    text = clean_text(run_pdftotext_raw(source).read_text(encoding="utf-8", errors="ignore"))
    markers = grade_markers(text)
    item_re = re.compile(
        r"\n\s*(\d{1,2})\.\s*\n(?P<body>.*?)(?=\n\s*\d{1,2}\.\s*\n|\n\s*Grado\s+\d{1,2}\s*[°º]|\Z)",
        flags=re.DOTALL | re.IGNORECASE,
    )
    records: list[dict] = []
    for match in item_re.finditer(text):
        body = match.group("body")
        if "Evidencias de aprendizaje" not in body:
            continue
        grade = nearest_grade(match.start(), markers)
        if not grade:
            continue
        statement_raw, evidence_raw = body.split("Evidencias de aprendizaje", 1)
        statement = normalize_sentence(statement_raw.splitlines())
        evidences = extract_evidence_lines(evidence_raw)
        if len(statement) < 32 or not evidences:
            continue
        number = match.group(1)
        meta = SOURCE_METADATA[source.source_id]
        records.append({
            "id": f"{source.area_key.replace(' ', '_')}_{grade.replace('°', '')}_dba_{number}",
            "area": source.area_key,
            "area_nombre": source.area_name,
            "grado": grade,
            "tipo": source.kind,
            "numero": number,
            "referente": statement,
            "evidencias": evidences[:6],
            "fuente": {
                "id": source.source_id,
                "titulo": source.title,
                "url": meta["url"],
                "pagina_oficial": meta["official_page"],
                "etiqueta": meta["source_label"],
            },
            "confianza_extraccion": "media",
        })
    return dedupe_records(records)


def extract_english_records() -> list[dict]:
    source = ENGLISH_SOURCE
    text = clean_text(run_pdftotext_raw(source).read_text(encoding="utf-8", errors="ignore"))
    heading_re = re.compile(r"\d\.\d\.\s*NIVEL\s*([A-Z0-9.]+).*?GRADO SUGERIDO:\s*(\d{1,2})\s*[°º]", re.IGNORECASE)
    matches = list(heading_re.finditer(text))
    records: list[dict] = []
    meta = SOURCE_METADATA[source.source_id]
    for idx, match in enumerate(matches):
        grade = f"{int(match.group(2))}°"
        level = match.group(1).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        section = text[start:end]
        section = section.split("META", 1)[0]
        bullets = []
        current: list[str] = []
        for raw in section.splitlines():
            line = raw.strip()
            if not line or line in {"DERECHOS", "BÁSICOS", "INGLÉS"}:
                continue
            if line.startswith("•"):
                if current:
                    bullets.append(normalize_sentence(current))
                current = [line.lstrip("• ").strip()]
            elif current:
                current.append(line)
        if current:
            bullets.append(normalize_sentence(current))
        for i, item in enumerate([b for b in bullets if len(b) > 16], start=1):
            records.append({
                "id": f"ingles_{grade.replace('°', '')}_curriculo_{i}",
                "area": source.area_key,
                "area_nombre": source.area_name,
                "grado": grade,
                "tipo": source.kind,
                "numero": str(i),
                "referente": item,
                "evidencias": [item],
                "nivel_mc": level,
                "fuente": {
                    "id": source.source_id,
                    "titulo": source.title,
                    "url": meta["url"],
                    "pagina_oficial": meta["official_page"],
                    "etiqueta": meta["source_label"],
                },
                "confianza_extraccion": "media",
            })
    existing_grades = {rec["grado"] for rec in records}
    module_re = re.compile(
        r"GRADO SUGERIDO:\s*(\d{1,2})\s*[°º]\s*MÓDULO\s+(\d).*?NIVEL MCER:\s*([A-Z0-9.]+)\s*(?P<body>.*?)(?=GRADO SUGERIDO:\s*\d{1,2}\s*[°º]\s*MÓDULO|\Z)",
        re.IGNORECASE | re.DOTALL,
    )
    for match in module_re.finditer(text):
        grade = f"{int(match.group(1))}°"
        if grade in existing_grades:
            continue
        level = match.group(3).strip()
        body = match.group("body")
        lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
        if not lines:
            continue
        statement = lines[0]
        if len(statement) < 20 or not re.search(r"[a-záéíóúñ]", statement, re.IGNORECASE):
            continue
        evidences = []
        current: list[str] = []
        for line in lines[2:]:
            if line.startswith("FUNCIONES DE LENGUA") or line.startswith("ESTÁNDARES BÁSICOS"):
                break
            if line.startswith("•"):
                if current:
                    evidences.append(normalize_sentence(current))
                current = [line.lstrip("• ").strip()]
            elif current:
                current.append(line)
        if current:
            evidences.append(normalize_sentence(current))
        # Keep readable lines; PDF font extraction corrupts some accented glyphs.
        evidences = [ev for ev in evidences if len(ev) > 16 and ev.count("Ã") + ev.count("") + ev.count("") < 3]
        if not evidences:
            evidences = [statement]
        records.append({
            "id": f"ingles_{grade.replace('°', '')}_modulo_{match.group(2)}",
            "area": source.area_key,
            "area_nombre": source.area_name,
            "grado": grade,
            "tipo": source.kind,
            "numero": match.group(2),
            "referente": statement,
            "evidencias": evidences[:6],
            "nivel_mc": level,
            "fuente": {
                "id": source.source_id,
                "titulo": source.title,
                "url": meta["url"],
                "pagina_oficial": meta["official_page"],
                "etiqueta": meta["source_label"],
            },
            "confianza_extraccion": "media",
        })
    return apply_manual_text_fixes(dedupe_records(records))


def extract_social_studies_records() -> list[dict]:
    source = SOCIAL_STUDIES_SOURCE
    bbox_path = run_pdftotext_bbox_layout(source)
    try:
        root = ET.parse(bbox_path).getroot()
    finally:
        bbox_path.unlink(missing_ok=True)
    ns = _xml_namespace(root)
    pages = root.findall(f".//{ns}page")
    flow: list[tuple[str, str]] = []
    current_grade: str | None = None
    for page in pages:
        grade = _social_grade_from_page(page, ns)
        if grade:
            current_grade = grade
        if not current_grade:
            continue
        for column in ("left", "right"):
            for line in _social_column_lines(page, ns, column):
                flow.append((current_grade, line))
    records = _parse_social_studies_flow(source, flow)
    return dedupe_records(records)


EBC_CYCLE_CONFIGS = [
    {
        "area_key": "lenguaje",
        "area_name": "Lenguaje",
        "start_pages": [32, 34, 36, 38, 40],
        "components": [
            "Producción textual",
            "Comprensión e interpretación textual",
            "Literatura",
            "Medios de comunicación y otros sistemas simbólicos",
            "Ética de la comunicación",
        ],
    },
    {
        "area_key": "matemáticas",
        "area_name": "Matemáticas",
        "start_pages": [80, 82, 84, 86, 88],
        "components": [
            "Pensamiento numérico y sistemas numéricos",
            "Pensamiento espacial y sistemas geométricos",
            "Pensamiento métrico y sistemas de medidas",
            "Pensamiento aleatorio y sistemas de datos",
            "Pensamiento variacional y sistemas algebraicos y analíticos",
        ],
    },
    {
        "area_key": "ciencias sociales",
        "area_name": "Ciencias Sociales",
        "start_pages": [122, 124, 126, 128, 130],
        "components": [
            "Me aproximo al conocimiento como científico(a) social",
            "Relaciones con la historia y las culturas",
            "Relaciones espaciales y ambientales",
            "Relaciones ético-políticas",
            "Desarrollo compromisos personales y sociales",
        ],
    },
    {
        "area_key": "ciencias naturales",
        "area_name": "Ciencias Naturales",
        "start_pages": [132, 134, 136, 138, 140],
        "components": [
            "Me aproximo al conocimiento como científico(a) natural",
            "Entorno vivo",
            "Entorno físico",
            "Ciencia, tecnología y sociedad",
            "Desarrollo compromisos personales y sociales",
        ],
    },
    {
        "area_key": "competencias ciudadanas",
        "area_name": "Competencias Ciudadanas",
        "start_pages": [170, 172, 174, 176, 178],
        "components": [
            "Convivencia y paz",
            "Participación y responsabilidad democrática",
            "Pluralidad, identidad y valoración de las diferencias",
        ],
    },
]

EBC_CYCLES = [
    {
        "label": "1°-3°",
        "name": "Primero a tercero",
        "terminal_grade": "3°",
        "grades": ["1°", "2°", "3°"],
    },
    {
        "label": "4°-5°",
        "name": "Cuarto a quinto",
        "terminal_grade": "5°",
        "grades": ["4°", "5°"],
    },
    {
        "label": "6°-7°",
        "name": "Sexto a séptimo",
        "terminal_grade": "7°",
        "grades": ["6°", "7°"],
    },
    {
        "label": "8°-9°",
        "name": "Octavo a noveno",
        "terminal_grade": "9°",
        "grades": ["8°", "9°"],
    },
    {
        "label": "10°-11°",
        "name": "Décimo a undécimo",
        "terminal_grade": "11°",
        "grades": ["10°", "11°"],
    },
]


def extract_ebc_records() -> list[dict]:
    source = EBC_SOURCE
    bbox_path = run_pdftotext_bbox_layout(source)
    try:
        root = ET.parse(bbox_path).getroot()
    finally:
        bbox_path.unlink(missing_ok=True)
    ns = _xml_namespace(root)
    pages = root.findall(f".//{ns}page")
    meta = SOURCE_METADATA[source.source_id]
    records: list[dict] = []
    for area_config in EBC_CYCLE_CONFIGS:
        for cycle, start_page in zip(EBC_CYCLES, area_config["start_pages"], strict=True):
            page_numbers = [start_page, start_page + 1]
            desempenos = _extract_ebc_desempenos_from_pages(pages, ns, page_numbers)
            for grade in cycle["grades"]:
                records.append({
                    "id": (
                        f"ebc_{area_config['area_key'].replace(' ', '_')}_"
                        f"{cycle['label'].replace('°', '').replace('-', '_')}_grado_{grade.replace('°', '')}"
                    ),
                    "area": area_config["area_key"],
                    "area_nombre": area_config["area_name"],
                    "grado": grade,
                    "tipo": source.kind,
                    "numero": cycle["label"],
                    "ciclo": cycle["label"],
                    "grupo_grados": cycle["name"],
                    "grado_terminal": cycle["terminal_grade"],
                    "competencia": f"Competencias básicas en {area_config['area_name']} para el ciclo {cycle['label']}",
                    "componentes": area_config["components"],
                    "referente": (
                        f"Estándares Básicos de Competencias en {area_config['area_name']} "
                        f"para el ciclo {cycle['label']} ({cycle['name']})."
                    ),
                    "evidencias": _ebc_evidence_summary(area_config, cycle, desempenos),
                    "desempenos": desempenos[:40],
                    "fuente": {
                        "id": source.source_id,
                        "titulo": source.title,
                        "url": meta["url"],
                        "pagina_oficial": meta["official_page"],
                        "etiqueta": meta["source_label"],
                    },
                    "confianza_extraccion": "media-ciclo",
                    "uso_curricular": "capa_competencia_ciclo_no_item",
                })
    return dedupe_records(records)


GUIDE22_LAYOUT = [
    {
        "pdf": "estandares_ingles_guia_22.pdf",
        "receptive_page": 18,
        "productive_page": 19,
        "ciclo": "1°-3°",
        "grupo_grados": "Primero a tercero",
        "grades": ["1°", "2°", "3°"],
        "grado_terminal": "3°",
        "nivel_mcer": "A1",
        "nivel_colombia": "Principiante",
    },
    {
        "pdf": "estandares_ingles_guia_22.pdf",
        "receptive_page": 20,
        "productive_page": 21,
        "ciclo": "4°-5°",
        "grupo_grados": "Cuarto a quinto",
        "grades": ["4°", "5°"],
        "grado_terminal": "5°",
        "nivel_mcer": "A2.1",
        "nivel_colombia": "Básico 1",
    },
    {
        "pdf": "estandares_ingles_guia_22_parte2.pdf",
        "receptive_page": 1,
        "productive_page": 2,
        "ciclo": "6°-7°",
        "grupo_grados": "Sexto a séptimo",
        "grades": ["6°", "7°"],
        "grado_terminal": "7°",
        "nivel_mcer": "A2.2",
        "nivel_colombia": "Básico 2",
    },
    {
        "pdf": "estandares_ingles_guia_22_parte2.pdf",
        "receptive_page": 3,
        "productive_page": 4,
        "ciclo": "8°-9°",
        "grupo_grados": "Octavo a noveno",
        "grades": ["8°", "9°"],
        "grado_terminal": "9°",
        "nivel_mcer": "B1.1",
        "nivel_colombia": "Pre intermedio 1",
    },
    {
        "pdf": "estandares_ingles_guia_22_parte2.pdf",
        "receptive_page": 5,
        "productive_page": 6,
        "ciclo": "10°-11°",
        "grupo_grados": "Décimo a undécimo",
        "grades": ["10°", "11°"],
        "grado_terminal": "11°",
        "nivel_mcer": "B1.2",
        "nivel_colombia": "Pre intermedio 2",
    },
]

GUIDE22_SKILLS = [
    {
        "key": "escucha",
        "label": "Escucha",
        "page_kind": "receptive_page",
        "column": (35, 285),
    },
    {
        "key": "lectura",
        "label": "Lectura",
        "page_kind": "receptive_page",
        "column": (285, 560),
    },
    {
        "key": "escritura",
        "label": "Escritura",
        "page_kind": "productive_page",
        "column": (35, 210),
    },
    {
        "key": "monologos",
        "label": "Monólogos",
        "page_kind": "productive_page",
        "column": (210, 385),
    },
    {
        "key": "conversacion",
        "label": "Conversación",
        "page_kind": "productive_page",
        "column": (385, 560),
    },
]

GUIDE22_COMMUNICATIVE_COMPETENCIES = [
    "Competencia lingüística",
    "Competencia pragmática",
    "Competencia sociolingüística",
]


def extract_guide22_english_standards_records() -> list[dict]:
    source = GUIDE22_SOURCE
    meta = SOURCE_METADATA[source.source_id]
    pages_cache: dict[str, tuple[list[ET.Element], str]] = {}
    records: list[dict] = []
    for cycle in GUIDE22_LAYOUT:
        pdf_name = cycle["pdf"]
        if pdf_name not in pages_cache:
            pages_cache[pdf_name] = _guide22_bbox_pages(pdf_name)
        pages, ns = pages_cache[pdf_name]
        skill_standards: dict[str, list[dict]] = {}
        for skill in GUIDE22_SKILLS:
            page_number = cycle[skill["page_kind"]]
            page = pages[int(page_number) - 1]
            standards = _parse_guide22_standards(
                _guide22_column_lines(page, ns, skill["column"])
            )
            skill_standards[skill["key"]] = standards
        for skill in GUIDE22_SKILLS:
            standards = skill_standards.get(skill["key"]) or []
            if len(standards) < 3:
                continue
            for grade in cycle["grades"]:
                records.append({
                    "id": (
                        f"guia22_ingles_{cycle['ciclo'].replace('°', '').replace('-', '_')}_"
                        f"{skill['key']}_grado_{grade.replace('°', '')}"
                    ),
                    "area": source.area_key,
                    "area_nombre": source.area_name,
                    "grado": grade,
                    "tipo": source.kind,
                    "numero": f"{cycle['ciclo']} / {skill['label']}",
                    "ciclo": cycle["ciclo"],
                    "grupo_grados": cycle["grupo_grados"],
                    "grado_terminal": cycle["grado_terminal"],
                    "nivel_mcer": cycle["nivel_mcer"],
                    "nivel_colombia": cycle["nivel_colombia"],
                    "habilidad_comunicativa": skill["label"],
                    "competencia": (
                        f"Competencia comunicativa en inglés {cycle['nivel_mcer']} "
                        f"({cycle['nivel_colombia']}) - {skill['label']}."
                    ),
                    "componentes": GUIDE22_COMMUNICATIVE_COMPETENCIES,
                    "referente": (
                        f"Estándares de inglés Guía 22 para {cycle['grupo_grados']} "
                        f"({cycle['ciclo']}), nivel {cycle['nivel_mcer']} "
                        f"{cycle['nivel_colombia']}, habilidad {skill['label']}."
                    ),
                    "evidencias": _guide22_evidence_summary(cycle, skill, standards),
                    "desempenos": [standard["texto"] for standard in standards],
                    "estandares_especificos": standards,
                    "fuente": {
                        "id": source.source_id,
                        "titulo": source.title,
                        "url": meta["url"],
                        "url_parte_2": meta["url_parte_2"],
                        "pagina_oficial": meta["official_page"],
                        "etiqueta": meta["source_label"],
                    },
                    "archivo_fuente": pdf_name,
                    "confianza_extraccion": "media-ciclo-nivel",
                    "uso_curricular": "capa_estandar_ingles_ciclo_nivel_no_item",
                })
    return dedupe_records(records)


def _guide22_bbox_pages(pdf_name: str) -> tuple[list[ET.Element], str]:
    pdf = PDF_DIR / pdf_name
    if not pdf.exists():
        raise FileNotFoundError(f"Missing PDF: {pdf}")
    tmp = tempfile.NamedTemporaryFile(prefix=f"guide22_{Path(pdf_name).stem}_", suffix=".html", delete=False)
    tmp.close()
    out = Path(tmp.name)
    subprocess.run(["pdftotext", "-bbox-layout", str(pdf), str(out)], check=True)
    try:
        root = ET.parse(out).getroot()
    finally:
        out.unlink(missing_ok=True)
    return root.findall(f".//{_xml_namespace(root)}page"), _xml_namespace(root)


def _guide22_column_lines(page: ET.Element, ns: str, column_range: tuple[float, float]) -> list[str]:
    x0, x1 = column_range
    words: list[tuple[float, float, str]] = []
    for word in page.findall(f".//{ns}word"):
        text = word.text or ""
        x_min = float(word.attrib.get("xMin", "0"))
        x_max = float(word.attrib.get("xMax", "0"))
        y_min = float(word.attrib.get("yMin", "0"))
        y_max = float(word.attrib.get("yMax", "0"))
        height = y_max - y_min
        x_center = (x_min + x_max) / 2
        if height < 5 or y_min < 180 or y_min > 600 or not (x0 <= x_center < x1):
            continue
        words.append((y_min, x_min, text))
    groups: list[list] = []
    for y_min, x_min, text in sorted(words):
        if not groups or abs(groups[-1][0] - y_min) > 3:
            groups.append([y_min, [(x_min, text)]])
        else:
            groups[-1][1].append((x_min, text))
    lines = []
    for _, grouped_words in groups:
        line = _clean_guide22_line(" ".join(token for _, token in sorted(grouped_words)))
        if line:
            lines.append(line)
    return lines


def _parse_guide22_standards(lines: list[str]) -> list[dict]:
    standards: list[dict] = []
    current: list[str] = []
    for line in lines:
        if _is_guide22_noise_line(line):
            continue
        if line.startswith("•"):
            if current:
                standards.append(_serialize_guide22_standard(current))
            current = [line.lstrip("• ").strip()]
        elif current:
            current.append(line)
    if current:
        standards.append(_serialize_guide22_standard(current))
    return [
        standard for standard in standards
        if 20 <= len(standard["texto"]) <= 420
    ]


def _serialize_guide22_standard(lines: list[str]) -> dict:
    text = normalize_sentence(lines)
    refs = re.findall(r"(?:^|\s)([123](?:\s*,\s*[123]){0,2})\.?$", text)
    competencias = []
    if refs:
        ref_text = refs[-1]
        text = text[: text.rfind(ref_text)].strip(" .,")
        competencias = [GUIDE22_COMMUNICATIVE_COMPETENCIES[int(ref) - 1] for ref in re.findall(r"[123]", ref_text)]
    return {
        "texto": _clean_guide22_line(text),
        "referencias_competencia": competencias,
    }


def _guide22_evidence_summary(cycle: dict, skill: dict, standards: list[dict]) -> list[str]:
    return [
        f"Ciclo Guía 22: {cycle['ciclo']} ({cycle['grupo_grados']}); grado terminal: {cycle['grado_terminal']}.",
        f"Nivel esperado: {cycle['nivel_mcer']} ({cycle['nivel_colombia']}).",
        f"Habilidad comunicativa: {skill['label']}.",
        "Uso permitido: orientar competencia comunicativa por ciclo/nivel; no usar como item aislado ni como certificación de dominio.",
        f"Estándares específicos recuperados para esta habilidad: {len(standards)}.",
    ]


def _clean_guide22_line(line: str) -> str:
    line = re.sub(r"\s+", " ", line).strip()
    replacements = {
        "ﬁ": "fi",
        "ﬂ": "fl",
        "Identifi co": "Identifico",
        "identifi co": "identifico",
        "específi ca": "específica",
        "refi eren": "refieren",
        "confi anza": "confianza",
        "difi cultad": "dificultad",
        "leido": "leído",
    }
    for old, new in replacements.items():
        line = line.replace(old, new)
    return line


def _is_guide22_noise_line(line: str) -> bool:
    if not line or re.fullmatch(r"[\d\s,]+", line):
        return True
    noise_tokens = (
        "COMPETENCIAS COMUNICATIVAS",
        "Competencia lingüística",
        "Competencia pragmática",
        "Competencia sociolingüística",
        "Referencias",
        "INGLÉS",
    )
    return any(token in line for token in noise_tokens)


def _extract_ebc_desempenos_from_pages(pages: list[ET.Element], ns: str, page_numbers: list[int]) -> list[str]:
    desempenos: list[str] = []
    for page_number in page_numbers:
        if page_number < 1 or page_number > len(pages):
            continue
        page = pages[page_number - 1]
        for column_range in _ebc_column_ranges(page_number):
            lines = _ebc_column_lines(page, ns, column_range)
            desempenos.extend(_parse_bullet_lines(lines))
    return _dedupe_texts(desempenos)


def _ebc_column_ranges(page_number: int) -> list[tuple[float, float]]:
    # Most EBC tables use two columns on the first page of a cycle and three on
    # the second. Language is narrower, but the same broad ranges still recover
    # usable cycle-level performances without relying on exact item positions.
    if page_number % 2 == 0:
        return [(35, 315), (315, 595)]
    return [(30, 220), (220, 410), (410, 600)]


def _ebc_column_lines(page: ET.Element, ns: str, column_range: tuple[float, float]) -> list[str]:
    x0, x1 = column_range
    words: list[tuple[float, float, str]] = []
    for word in page.findall(f".//{ns}word"):
        text = word.text or ""
        x_min = float(word.attrib.get("xMin", "0"))
        x_max = float(word.attrib.get("xMax", "0"))
        y_min = float(word.attrib.get("yMin", "0"))
        y_max = float(word.attrib.get("yMax", "0"))
        height = y_max - y_min
        x_center = (x_min + x_max) / 2
        if height < 5 or y_min < 80 or y_min > 740 or not (x0 <= x_center < x1):
            continue
        words.append((y_min, x_min, text))
    groups: list[list] = []
    for y_min, x_min, text in sorted(words):
        if not groups or abs(groups[-1][0] - y_min) > 3:
            groups.append([y_min, [(x_min, text)]])
        else:
            groups[-1][1].append((x_min, text))
    lines = []
    for _, grouped_words in groups:
        line = _clean_ebc_line(" ".join(token for _, token in sorted(grouped_words)))
        if not line or _is_ebc_noise_line(line):
            continue
        lines.append(line)
    return lines


def _parse_bullet_lines(lines: list[str]) -> list[str]:
    bullets: list[str] = []
    current: list[str] = []
    for line in lines:
        if line.startswith("•"):
            if current:
                bullets.append(normalize_sentence(current))
            current = [line.lstrip("• ").strip()]
        elif current and not _is_ebc_heading_line(line):
            current.append(line)
    if current:
        bullets.append(normalize_sentence(current))
    return [
        bullet
        for bullet in bullets
        if 35 <= len(bullet) <= 420 and not _looks_like_caption(bullet)
    ]


def _clean_ebc_line(line: str) -> str:
    line = re.sub(r"\s+", " ", line).strip()
    replacements = {
        "ﬁ": "fi",
        "ﬂ": "fl",
        "cientiﬁ": "científi",
        "clasiﬁ": "clasifi",
        "cuantiﬁ": "cuantifi",
        "identiﬁ": "identifi",
        "signiﬁ": "signifi",
        "gráﬁ": "gráfi",
        "geográﬁ": "geográfi",
        "tecnológi- co": "tecnológico",
    }
    for old, new in replacements.items():
        line = line.replace(old, new)
    return line


def _is_ebc_noise_line(line: str) -> bool:
    if re.fullmatch(r"[\d\s\-–.°]+", line):
        return True
    noise_tokens = (
        "Estándares Básicos de Competencias",
        "COMPETENCIAS EN",
        "COMPETENCIAS DEL",
        "CIENCIAS SOCIALES Y NATURALES",
        "Al terminar",
        "Al final de",
        "Para lo cual",
    )
    return any(token in line for token in noise_tokens)


def _is_ebc_heading_line(line: str) -> bool:
    if line.endswith("..."):
        return True
    if line in {"Para lo cual,", "Para lo cual"}:
        return True
    if line.isupper() and len(line) > 10:
        return True
    return False


def _ebc_evidence_summary(area_config: dict, cycle: dict, desempenos: list[str]) -> list[str]:
    return [
        f"Ciclo EBC: {cycle['label']} ({cycle['name']}); grado terminal: {cycle['terminal_grade']}.",
        "Componentes EBC: " + "; ".join(area_config["components"]),
        "Uso permitido: orientar competencias y desempeños del ciclo; no usar como item ni como evidencia psicométrica.",
    ]


def _dedupe_texts(texts: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for text in texts:
        key = re.sub(r"\W+", "", text.lower())[:160]
        if key in seen:
            continue
        seen.add(key)
        unique.append(text)
    return unique


def _parse_social_studies_flow(source: SourceConfig, flow: list[tuple[str, str]]) -> list[dict]:
    item_re = re.compile(r"^(?:[a-záéíóúñ]{1,4}\s+)?(\d{1,2})\.\s*(.*)$", re.IGNORECASE)
    statement_starters = re.compile(
        r"^(Se ubica|Comprende|Analiza|Evalúa|Evalua|Explica|Interpreta|Argumenta|Reconoce|Describe|"
        r"Diferencia|Participa|Establece|Aplica|Compara|Relaciona)\b",
        re.IGNORECASE,
    )
    records: list[dict] = []
    current: dict | None = None
    section: str | None = None
    current_evidence: list[str] | None = None

    def finish_current() -> None:
        nonlocal current, section, current_evidence
        if not current:
            return
        if current_evidence:
            current["evidences"].append(normalize_sentence(current_evidence))
        statement = normalize_sentence(current["statement"])
        evidences = [
            normalize_sentence([ev])
            for ev in current["evidences"]
            if len(normalize_sentence([ev])) > 25
        ]
        if (
            len(statement) >= 35
            and statement_starters.search(statement)
            and len(evidences) >= 2
            and not _looks_like_caption(statement)
        ):
            meta = SOURCE_METADATA[source.source_id]
            records.append({
                "id": f"{source.area_key.replace(' ', '_')}_{current['grade'].replace('°', '')}_dba_{current['number']}",
                "area": source.area_key,
                "area_nombre": source.area_name,
                "grado": current["grade"],
                "tipo": source.kind,
                "numero": current["number"],
                "referente": statement,
                "evidencias": evidences[:6],
                "fuente": {
                    "id": source.source_id,
                    "titulo": source.title,
                    "url": meta["url"],
                    "pagina_oficial": meta["official_page"],
                    "etiqueta": meta["source_label"],
                },
                "confianza_extraccion": "media-conservadora",
            })
        current = None
        section = None
        current_evidence = None

    for grade, raw_line in flow:
        line = _clean_social_line(raw_line)
        if not line:
            continue
        item_match = item_re.match(line)
        if item_match and 1 <= int(item_match.group(1)) <= 8:
            finish_current()
            current = {
                "grade": grade,
                "number": item_match.group(1),
                "statement": [],
                "evidences": [],
            }
            section = "statement"
            current_evidence = None
            rest = item_match.group(2).strip()
            if rest:
                current["statement"].append(rest)
            continue
        if not current:
            continue
        if line == "Evidencias de aprendizaje":
            section = "evidence"
            current_evidence = None
            continue
        if _is_social_stop_line(line):
            if current_evidence:
                current["evidences"].append(normalize_sentence(current_evidence))
                current_evidence = None
            section = "post_evidence"
            continue
        if section == "statement":
            current["statement"].append(line)
        elif section == "evidence":
            if line.startswith("l "):
                if current_evidence:
                    current["evidences"].append(normalize_sentence(current_evidence))
                current_evidence = [line[2:].strip()]
            elif current_evidence:
                current_evidence.append(line)
    finish_current()
    return records


def _xml_namespace(root: ET.Element) -> str:
    if root.tag.startswith("{"):
        return root.tag.split("}", 1)[0] + "}"
    return ""


def _social_grade_from_page(page: ET.Element, ns: str) -> str | None:
    words = []
    for word in page.findall(f".//{ns}word"):
        y_min = float(word.attrib.get("yMin", "999"))
        if y_min < 130:
            words.append((y_min, float(word.attrib.get("xMin", "0")), word.text or ""))
    text = " ".join(token for _, _, token in sorted(words))
    compact = re.sub(r"\s+", "", text)
    patterns = [
        r"G\s*r\s*a\s*d\s*o\s*0?\s*(\d{1,2})\s*[º°]",
        r"Grado\s*0?\s*(\d{1,2})\s*[º°]",
        r"0?(\d{1,2})\s*[º°]\s*o\s*Grad",
        r"0?(\d{1,2})\s*[º°]\s*Grado",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return f"{int(match.group(1))}°"
    compact_match = re.search(r"Grado0?(\d{1,2})[º°]", compact, flags=re.IGNORECASE)
    if not compact_match:
        compact_match = re.search(r"0?(\d{1,2})[º°]oGrad", compact, flags=re.IGNORECASE)
    return f"{int(compact_match.group(1))}°" if compact_match else None


def _social_column_lines(page: ET.Element, ns: str, column: str) -> list[str]:
    words: list[tuple[float, float, str]] = []
    for word in page.findall(f".//{ns}word"):
        text = word.text or ""
        x_min = float(word.attrib.get("xMin", "0"))
        x_max = float(word.attrib.get("xMax", "0"))
        y_min = float(word.attrib.get("yMin", "0"))
        y_max = float(word.attrib.get("yMax", "0"))
        height = y_max - y_min
        x_center = (x_min + x_max) / 2
        if height < 6 or y_min < 90 or y_min > 715:
            continue
        if column == "left" and not (35 <= x_center < 315):
            continue
        if column == "right" and not (315 <= x_center < 590):
            continue
        words.append((y_min, x_min, text))
    groups: list[list] = []
    for y_min, x_min, text in sorted(words):
        if not groups or abs(groups[-1][0] - y_min) > 3:
            groups.append([y_min, [(x_min, text)]])
        else:
            groups[-1][1].append((x_min, text))
    lines = []
    for _, grouped_words in groups:
        line = _clean_social_line(" ".join(token for _, token in sorted(grouped_words)))
        if not line:
            continue
        if re.fullmatch(r"[\d\sOSEN.]+", line) and not re.fullmatch(r"\d{1,2}\.?", line):
            continue
        if "Derechos Básicos de Aprendizaje" in line or "Ciencias Sociales" in line:
            continue
        lines.append(line)
    return lines


def _clean_social_line(line: str) -> str:
    line = re.sub(r"\s+", " ", line).strip()
    replacements = {
        "Co mprende": "Comprende",
        "Comprendelaimportanciadelasasociaciones": "Comprende la importancia de las asociaciones",
        "Evidencias de aprendi zaje": "Evidencias de aprendizaje",
        "geográ cos": "geográficos",
    }
    for old, new in replacements.items():
        line = line.replace(old, new)
    return line


def _is_social_stop_line(line: str) -> bool:
    stop_prefixes = (
        "Ejemplo",
        "Foto ",
        "Foto tomada",
        "Foto tomadas",
        "Fotografía",
        "Fotografia",
        "Imagen",
        "Mapa basado",
        "Gráfico basado",
        "Grafico basado",
    )
    return any(line.startswith(prefix) for prefix in stop_prefixes)


def _looks_like_caption(text: str) -> bool:
    lower = text.lower()
    return any(token in lower for token in ("www.", "goo.gl", "fotografía", "foto tomada", "mapa basado"))


def apply_manual_text_fixes(records: list[dict]) -> list[dict]:
    """Corrects known PDF font-extraction corruption without losing traceability.

    Some official English PDF text is encoded with custom glyph mappings. The
    extraction remains traceable to the source, but these few strings need
    human-readable corrections for UI and prompt quality.
    """
    for rec in records:
        fixed = ENGLISH_MANUAL_TEXT_FIXES.get(rec.get("id"))
        if not fixed:
            continue
        rec["referente"] = fixed
        rec["evidencias"] = [fixed if ev == rec["evidencias"][0] else ev for ev in rec.get("evidencias", [])] or [fixed]
        rec["confianza_extraccion"] = "media-corregida"
    return records


def dedupe_records(records: list[dict]) -> list[dict]:
    seen: set[tuple[str, str, str]] = set()
    unique: list[dict] = []
    for rec in records:
        key = (rec["area"], rec["grado"], re.sub(r"\W+", "", rec["referente"].lower())[:120])
        if key in seen:
            continue
        seen.add(key)
        unique.append(rec)
    return unique


def area_file_name(area_key: str) -> str:
    return {
        "matemáticas": "curriculo_matematicas.json",
        "lenguaje": "curriculo_lenguaje.json",
        "ciencias naturales": "curriculo_ciencias.json",
        "ciencias sociales": "curriculo_ciencias_sociales.json",
        "competencias ciudadanas": "curriculo_competencias_ciudadanas.json",
        "inglés": "curriculo_ingles.json",
    }[area_key]


def build_area_documents(records: list[dict]) -> dict[str, dict]:
    generated_at = datetime.now(timezone.utc).isoformat()
    docs: dict[str, dict] = {}
    for rec in records:
        area = rec["area"]
        if area not in docs:
            docs[area] = {
                "_meta": {
                    "area": rec["area_nombre"],
                    "fuente": "MEN Colombia / Colombia Aprende — fuentes oficiales normalizadas",
                    "generado_en": generated_at,
                    "schema": "adaptivelearn.curriculo.traceable.v1",
                    "nota": "Base generada desde PDFs oficiales descargados localmente. La extracción es conservadora y trazable por fuente.",
                },
                "grados": {},
            }
        grade_doc = docs[area]["grados"].setdefault(rec["grado"], {
            "competencia": "",
            "referentes": [],
            "dba": [],
            "estandares": [],
            "evidencias": [],
        })
        grade_doc["referentes"].append(rec)
        if rec.get("tipo") == "DBA":
            grade_doc["dba"].append(rec["referente"])
        elif str(rec.get("tipo") or "").startswith("Estándar"):
            grade_doc["estandares"].append(rec)
        for ev in rec["evidencias"]:
            if ev not in grade_doc["evidencias"]:
                grade_doc["evidencias"].append(ev)
    for doc in docs.values():
        for grade_doc in doc["grados"].values():
            refs = grade_doc["referentes"]
            if refs:
                grade_doc["competencia"] = f"{len(refs)} referentes curriculares trazables disponibles."
            grade_doc["dba"] = grade_doc["dba"][:14]
            grade_doc["estandares"] = grade_doc["estandares"][:12]
            grade_doc["evidencias"] = grade_doc["evidencias"][:24]
    return docs


def backup_existing_curricula() -> None:
    LEGACY_DIR.mkdir(parents=True, exist_ok=True)
    for file_name in (
        "curriculo_matematicas.json",
        "curriculo_lenguaje.json",
        "curriculo_ciencias.json",
        "curriculo_ciencias_sociales.json",
        "curriculo_competencias_ciudadanas.json",
        "curriculo_ingles.json",
    ):
        src = DATA / file_name
        dst = LEGACY_DIR / file_name
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_records: list[dict] = []
    for source in DBA_SOURCES:
        records = extract_dba_records(source)
        print(f"{source.source_id}: {len(records)} records")
        all_records.extend(records)
    social_records = extract_social_studies_records()
    print(f"{SOCIAL_STUDIES_SOURCE.source_id}: {len(social_records)} records")
    all_records.extend(social_records)
    ebc_records = extract_ebc_records()
    print(f"{EBC_SOURCE.source_id}: {len(ebc_records)} records")
    all_records.extend(ebc_records)
    guide22_records = extract_guide22_english_standards_records()
    print(f"{GUIDE22_SOURCE.source_id}: {len(guide22_records)} records")
    all_records.extend(guide22_records)
    english_records = extract_english_records()
    print(f"{ENGLISH_SOURCE.source_id}: {len(english_records)} records")
    all_records.extend(english_records)

    if not all_records:
        raise RuntimeError("No curriculum records extracted. Aborting.")

    normalized_path = OUT_DIR / "curriculo_men_normalizado.json"
    normalized = {
        "_meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "schema": "adaptivelearn.curriculo.records.v1",
            "total_records": len(all_records),
        },
        "records": all_records,
    }
    normalized_path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")

    docs = build_area_documents(all_records)
    backup_existing_curricula()
    for area, doc in docs.items():
        out = DATA / area_file_name(area)
        out.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")

    report = {
        "total_records": len(all_records),
        "by_area_grade": {},
    }
    for rec in all_records:
        key = f"{rec['area']} / {rec['grado']}"
        report["by_area_grade"][key] = report["by_area_grade"].get(key, 0) + 1
    (OUT_DIR / "build_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
