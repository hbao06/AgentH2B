"""CLI baseline: inspect packages and emit safe abstentions.

The first commit intentionally does not hallucinate answers. The interface is
stable so an agent planner/executor can be plugged in without changing Docker
or submission handling.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .ingest import load_package, write_preview
from .models import Answer


def run(questions_path: str | Path, data_root: str | Path, output_path: str | Path) -> None:
    questions = [json.loads(line) for line in Path(questions_path).read_text(encoding="utf-8").splitlines() if line.strip()]
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for question in questions:
            package_path = Path(data_root) / question.get("business_id", "")
            if package_path.exists():
                package = load_package(package_path, question.get("business_id"))
                write_preview(package, output.parent / f"preview_{package.business_id}.json")
            handle.write(json.dumps(Answer(question["id"], "abstain").as_dict(), ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", default="/data/questions.jsonl")
    parser.add_argument("--data", default="/data")
    parser.add_argument("--output", default="/result/submission.jsonl")
    args = parser.parse_args()
    run(args.questions, args.data, args.output)


if __name__ == "__main__":
    main()
