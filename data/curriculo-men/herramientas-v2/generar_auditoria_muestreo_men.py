from __future__ import annotations

import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from men_sample_audit import build_men_sample_audit, write_men_sample_audit


def main() -> None:
    report = build_men_sample_audit()
    json_path, md_path = write_men_sample_audit(report)
    summary = report["summary"]
    print(f"Auditoria MEN por muestra generada: {md_path}")
    print(f"JSON: {json_path}")
    print(f"Muestras: {summary['checks_total']}")
    print(f"Aprobadas: {summary['passed']}")
    print(f"Advertencias: {summary['warning']}")
    print(f"Fallidas: {summary['failed']}")
    print(f"Cobertura promedio: {summary['average_lexical_coverage']}")


if __name__ == "__main__":
    main()
