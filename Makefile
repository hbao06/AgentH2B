.PHONY: preview baseline test lint

preview:
	python -m datamate.baseline --questions /data/questions.jsonl --data /data --output /result/submission.jsonl

baseline:
	PYTHONPATH=src python -m datamate --questions data/questions.jsonl --data data --output outputs/submission.jsonl

test:
	PYTHONPATH=src python -m pytest

lint:
	python -m ruff check src tests
