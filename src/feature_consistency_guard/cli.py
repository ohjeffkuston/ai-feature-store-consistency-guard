from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from .guard import evaluate_contract


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate an ML feature-store consistency contract.")
    parser.add_argument("contract", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    contract = yaml.safe_load(args.contract.read_text(encoding="utf-8"))
    result = evaluate_contract(contract)
    if args.as_json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"{result.decision}: {result.score}% ({result.passed}/{result.total} checks passed)")
        for item in result.findings:
            print(f"[{item.status}] {item.rule_id} {item.message}")
    return 0 if result.decision == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
