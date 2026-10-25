from __future__ import annotations

import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from men_canonical_layer import build_men_canonical_layer, write_men_canonical_layer


def main() -> None:
    report = build_men_canonical_layer()
    json_path, md_path = write_men_canonical_layer(report)
    summary = report["summary"]
    print(f"Capa canonica MEN generada: {md_path}")
    print(f"JSON: {json_path}")
    print(f"Fuentes: {summary['sources_total']}")
    print(f"Registros indexados: {summary['anchors_total']}")
    print(f"Anclajes literales: {summary['exact_span_found']}")
    print(f"Soporte lexico: {summary['lexical_support_only']}")
    print(f"Revision manual: {summary['manual_review_required']}")


if __name__ == "__main__":
    main()
