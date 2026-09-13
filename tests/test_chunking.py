import pytest

from app.services.chunking import split_text


def test_split_text_respects_size_and_overlap():
    text = "abcdefghijklmnopqrstuvwxyz"
    chunks = split_text(text, chunk_size=10, overlap=3)
    assert chunks[0] == "abcdefghij"
    assert chunks[1].startswith("hij")
    assert all(len(chunk) <= 10 for chunk in chunks)


def test_split_text_empty():
    assert split_text("   ", chunk_size=10, overlap=2) == []


def test_split_text_shorter_than_chunk():
    assert split_text("hello", chunk_size=800, overlap=150) == ["hello"]


def test_split_text_rejects_invalid_overlap():
    with pytest.raises(ValueError):
        split_text("hello world", chunk_size=8, overlap=8)
