from datamate.evaluate import score


def test_penalized_accuracy():
    refs = [{"id": "a", "type": "number", "answer": 3}, {"id": "b", "type": "number", "answer": 4}]
    preds = [{"id": "a", "type": "number", "answer": 3}, {"id": "b", "type": "abstain", "answer": None}]
    result = score(preds, refs)
    assert result == {"correct": 1, "wrong": 0, "abstain": 1, "total": 2, "pa": 0.5}
