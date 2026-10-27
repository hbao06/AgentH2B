"""Local evaluator for DataMate-style JSONL answers."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .normalize import normalize_string


def _equal(kind: str, actual: Any, expected: Any) -> bool:
    if kind == "string":
        return normalize_string(actual) == normalize_string(expected)
    if kind == "percent":
        return round(float(actual), 2) == round(float(expected), 2)
    if kind == "number":
        return float(actual) == float(expected)
    return actual == expected


def score(predictions: list[dict[str, Any]], references: list[dict[str, Any]]) -> dict[str, Any]:
    predicted = {row["id"]: row for row in predictions}
    correct = wrong = abstain = 0
    for reference in references:
        row = predicted.get(reference["id"])
        if not row or row.get("type") == "abstain":
            abstain += 1
        elif row.get("type") == reference.get("type") and _equal(row["type"], row.get("answer"), reference.get("answer")):
            correct += 1
        else:
            wrong += 1
    total = len(references)
    return {"correct": correct, "wrong": wrong, "abstain": abstain,
            "total": total, "pa": (correct - wrong) / total if total else 0.0}


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
