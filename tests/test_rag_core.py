import pytest
from rag_core import split_text, make_context

def test_chunk_overlap():
    parts = split_text("abcdefghij", size=6, overlap=2)
    assert parts == ["abcdef", "efghij"]

def test_empty_text():
    assert split_text("  \n ") == []

def test_invalid_overlap():
    with pytest.raises(ValueError):
        split_text("hello", size=5, overlap=5)

def test_context_citations():
    context = make_context([{"source": "paper.pdf", "page": 2, "text": "Useful fact"}])
    assert "[1] paper.pdf page 2" in context
    assert "Useful fact" in context
