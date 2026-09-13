from io import BytesIO
from pathlib import Path

from pypdf import PdfReader

from app.exceptions import EmptyDocumentError, UnsupportedFileTypeError

SUPPORTED_EXTENSIONS = {".txt", ".pdf"}


def extract_text(filename: str, data: bytes) -> str:
    if not data:
        raise EmptyDocumentError("Uploaded file is empty")

    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileTypeError(
            f"Unsupported file type '{suffix or filename}'. Allowed: .pdf, .txt"
        )

    if suffix == ".txt":
        text = _decode_text(data)
    else:
        text = _extract_pdf(data)

    text = text.strip()
    if not text:
        raise EmptyDocumentError("No text could be extracted from the document")
    return text


def _decode_text(data: bytes) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise UnsupportedFileTypeError("Text file must be valid UTF-8") from exc


def _extract_pdf(data: bytes) -> str:
    reader = PdfReader(BytesIO(data))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)
