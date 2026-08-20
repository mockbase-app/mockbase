#!/usr/bin/env python3
"""Query Mockbase digital-asset supply, pricing, pain, SEO, and opportunities."""

import argparse
import json
from pathlib import Path

from market_intelligence import execute_query, root_path


COMMANDS = (
    "competitors", "related-products", "pricing-distribution", "crowded-categories",
    "common-complaints", "editing-workflow-gaps", "underserved-niches",
    "high-demand-low-supply", "seo-opportunity",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path)
    parser.add_argument("command", choices=COMMANDS)
    parser.add_argument("--keyword", default="")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    print(json.dumps(execute_query(root_path(arguments.root), arguments.command, arguments.keyword), ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
