#!/usr/bin/env python3
"""Import explicitly supplied digital-asset market data into Mockbase Intelligence."""

import argparse
import json
from pathlib import Path

from market_intelligence import day, import_market_data, root_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--source-name", required=True)
    parser.add_argument("--dataset-version", required=True)
    parser.add_argument("--capture-date")
    arguments = parser.parse_args()
    result = import_market_data(
        root_path(arguments.root), arguments.source, arguments.source_name,
        arguments.dataset_version, day(arguments.capture_date),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
