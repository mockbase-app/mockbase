#!/usr/bin/env python3
"""Create or version a Mockbase product Decision Record."""

import argparse
import json
from pathlib import Path

from market_intelligence import manage_decision, root_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path)
    parser.add_argument("action", choices=("create", "revise"))
    parser.add_argument("--product-name", required=True)
    parser.add_argument("--record-json", type=Path, required=True)
    parser.add_argument("--new-evidence")
    arguments = parser.parse_args()
    if arguments.action == "revise" and not arguments.new_evidence:
        parser.error("revise requires --new-evidence")
    record = json.loads(arguments.record_json.read_text(encoding="utf-8"))
    result = manage_decision(root_path(arguments.root), arguments.product_name, record, arguments.new_evidence if arguments.action == "revise" else None)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
