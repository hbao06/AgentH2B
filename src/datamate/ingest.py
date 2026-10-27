"""Read a business data package into normalized tables.

This is the reusable part inspired by the previous Excel pipeline: every input
source becomes a small, inspectable table preview before an agent plans work.
"""
from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path
from typing import Any

from .models import DataPackage, Table


def _clean(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value if value else None
    return value


def _table(name: str, rows: list[dict[str, Any]], source: str) -> Table:
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(str(key))
    normalized = [{key: _clean(row.get(key)) for key in columns} for row in rows]
    return Table(name=name, columns=columns, rows=normalized, source=source)


def _read_csv(path: Path) -> list[Table]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [_table(path.stem, list(csv.DictReader(handle)), str(path))]


def _read_xlsx(path: Path) -> list[Table]:
    try:
        import openpyxl
    except ImportError as exc:  # pragma: no cover - environment-dependent
        raise RuntimeError("XLSX input requires openpyxl; install the xlsx extra") from exc
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    tables: list[Table] = []
    for sheet in workbook.worksheets:
        values = list(sheet.values)
        if not values:
            continue
        headers = [str(value).strip() if value is not None else f"column_{i}" for i, value in enumerate(values[0])]
        rows = [dict(zip(headers, row, strict=False)) for row in values[1:]]
        tables.append(_table(f"{path.stem}__{sheet.title}", rows, str(path)))
    return tables


def _read_sqlite(path: Path) -> list[Table]:
    with sqlite3.connect(path) as connection:
        names = [row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")]
        tables = []
        for name in names:
            escaped = name.replace('"', '""')
            cursor = connection.execute(f'SELECT * FROM "{escaped}"')
            columns = [item[0] for item in cursor.description or []]
            tables.append(_table(name, [dict(zip(columns, row)) for row in cursor.fetchall()], str(path)))
        return tables


def load_package(path: str | Path, business_id: str | None = None) -> DataPackage:
    root = Path(path)
    if root.is_file():
        root = root.parent
    files = sorted(p for p in root.iterdir() if p.is_file())
    tables: list[Table] = []
    for file in files:
        suffix = file.suffix.lower()
        if suffix == ".csv":
            tables.extend(_read_csv(file))
        elif suffix in {".xlsx", ".xlsm"}:
            tables.extend(_read_xlsx(file))
        elif suffix in {".sqlite", ".sqlite3", ".db"}:
            tables.extend(_read_sqlite(file))
    readme = next((p.read_text(encoding="utf-8") for p in files if p.name.lower() == "readme.md"), "")
    rulebook = next((p.read_text(encoding="utf-8") for p in files if "rule" in p.stem.lower()), "")
    return DataPackage(business_id=business_id or root.name, tables=tables, readme=readme, rulebook=rulebook)


def schema_preview(package: DataPackage, limit: int = 3) -> list[dict[str, Any]]:
    return [{"name": table.name, "source": table.source, "rows": table.row_count,
             "columns": table.columns, "sample": table.rows[:limit]} for table in package.tables]


def write_preview(package: DataPackage, output: str | Path) -> None:
    Path(output).write_text(json.dumps(schema_preview(package), ensure_ascii=False, indent=2), encoding="utf-8")
