import pytest

from app.exceptions import EmptyDocumentError, UnsupportedFileTypeError
from app.services.extraction import extract_text


def test_extract_utf8_text():
    text = extract_text("notes.txt", b"Retrieval augmented generation")
    assert "Retrieval" in text


def test_extract_rejects_empty_file():
    with pytest.raises(EmptyDocumentError):
        extract_text("notes.txt", b"")


def test_extract_rejects_whitespace_only():
    with pytest.raises(EmptyDocumentError):
        extract_text("notes.txt", b"   \n  ")


def test_extract_rejects_unsupported_type():
    with pytest.raises(UnsupportedFileTypeError):
        extract_text("image.png", b"not-an-image")
