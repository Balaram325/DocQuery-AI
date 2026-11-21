import pytest
from evaluate_retrieval import hit_metrics

def test_hit_rate():
    labels = [{"source":"a.pdf","page":2}, {"source":"b.pdf","page":1}]
    predictions = [
        [{"source":"a.pdf","page":1},{"source":"a.pdf","page":2}],
        [{"source":"b.pdf","page":1}]
    ]
    assert hit_metrics(predictions, labels, (1,2)) == {"hit_rate_at_1":.5,"hit_rate_at_2":1.0}

def test_requires_labels():
    with pytest.raises(ValueError):
        hit_metrics([], [], (1,))

def test_invalid_k():
    with pytest.raises(ValueError):
        hit_metrics([[{"source":"a.pdf","page":1}]], [{"source":"a.pdf","page":1}], (0,))
