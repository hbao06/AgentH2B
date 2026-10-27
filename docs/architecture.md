# Baseline architecture

This repository carries over the safe, reusable ideas from the previous Excel
pipeline without carrying over its competition-specific assumptions.

```text
data package + questions.jsonl
            |
            v
 ingest: CSV / XLSX sheets / SQLite tables
            |
            v
 schema preview + samples + README/rulebook context
            |
            v
 planner (to be implemented after public data is available)
            |
            v
 read-only executor (filter / join / aggregate / Python sandbox)
            |
            v
 evidence and contract checks
            |
            v
 typed answer -> submission.jsonl
```

## What was reused conceptually

- **Region/preview thinking:** input is converted into inspectable tables before
  a planner makes a decision. The first adapter treats each CSV, SQLite table,
  and XLSX sheet as a table. A richer merged-cell Region parser can be added
  without changing the contracts in `models.py`.
- **Structured planning:** the future planner should return a JSON plan rather
  than free-form prose.
- **Controlled execution:** query and generated-code execution must be
  read-only, time-limited, and restricted to the mounted data directory.
- **Result review:** the evaluator and normalizer are separate from planning so
  output mistakes can be measured independently.

## What is deliberately not copied

- The old `submission.csv` contract; DataMate uses JSONL and typed answers.
- The old sheet-count/region-size routing rule; routing must be learned from
  the question, schema and rulebook after the official data is available.
- Any online LLM/API dependency; Rule requires offline inference.
- Any hard-coded question or business-id logic; Rule prohibits it.

## Next implementation seam

Implement `planner.py` against `DataPackage` and `Table`, then make it return a
small operation plan such as `select`, `filter`, `group_by`, `aggregate`,
`sort`, `limit`, and `answer_type`. Keep execution deterministic and test it
against hand-written fixtures before connecting an offline model.
