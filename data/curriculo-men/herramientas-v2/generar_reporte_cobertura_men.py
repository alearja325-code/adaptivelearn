#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from men_source_registry import build_men_coverage_report, write_men_coverage_report


def main() -> None:
    report = build_men_coverage_report()
    json_path, md_path = write_men_coverage_report(report)
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


if __name__ == "__main__":
    main()
