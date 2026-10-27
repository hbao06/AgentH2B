"""Output normalization and conservative answer contracts."""
from __future__ import annotations

import math
import unicodedata
from typing import Any


ANSWER_TYPES = {"number", "percent", "string", "date", "boolean", "list", "table", "unanswerable", "abstain"}


def normalize_string(value: Any) -> str:
    text = unicodedata.normalize("NFC", str(value)).lower()
    text = " ".join("".join(ch if (ch.isalnum() or ch.isspace()) else " " for ch in text).split())
    return text


def normalize_answer(answer_type: str, value: Any) -> Any:
    if answer_type not in ANSWER_TYPES:
        raise ValueError(f"Unsupported answer type: {answer_type}")
    if answer_type in {"unanswerable", "abstain"}:
        return None
    if answer_type == "string":
        return str(value).strip()
    if answer_type == "percent":
        return round(float(value), 2)
    if answer_type == "number":
        number = float(value)
        return int(number) if number.is_integer() else round(number, 2)
    if answer_type == "boolean":
        if isinstance(value, bool):
            return value
        lowered = str(value).strip().lower()
        if lowered in {"true", "1", "yes", "có", "co"}:
            return True
        if lowered in {"false", "0", "no", "không", "khong"}:
            return False
        raise ValueError(f"Cannot normalize boolean: {value}")
    return value


def validate_answer(answer_type: str, value: Any) -> None:
    normalized = normalize_answer(answer_type, value)
    if answer_type == "number" and (isinstance(normalized, float) and not math.isfinite(normalized)):
        raise ValueError("Non-finite number")
