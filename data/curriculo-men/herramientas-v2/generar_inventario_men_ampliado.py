from __future__ import annotations

import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from men_extended_inventory import build_extended_men_inventory, write_extended_men_inventory


def main() -> None:
    report = build_extended_men_inventory()
    json_path, md_path = write_extended_men_inventory(report)
    print(f"Inventario MEN ampliado generado: {md_path}")
    print(f"JSON: {json_path}")
    print(f"Fuentes inventariadas: {report['summary']['items_total']}")
    print(f"Usables hoy: {report['summary']['usable_for_generation_now']}")
    print(f"Pendientes: {report['summary']['pending_items']}")


if __name__ == "__main__":
    main()
