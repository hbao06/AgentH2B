"""Small, dependency-free data contracts used by the baseline."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Table:
    name: str
    columns: list[str]
    rows: list[dict[str, Any]]
    source: str = ""

    @property
    def row_count(self) -> int:
        return len(self.rows)


@dataclass
class DataPackage:
    business_id: str
    tables: list[Table] = field(default_factory=list)
    readme: str = ""
    rulebook: str = ""


@dataclass
class Answer:
    id: str
    type: str
    answer: Any = None

    def as_dict(self) -> dict[str, Any]:
        return {"id": self.id, "type": self.type, "answer": self.answer}
