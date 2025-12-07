from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

from PyPDF2 import PdfReader

DATE_PATTERN = re.compile(r"(20\d{2})[./-](\d{2})[./-](\d{2})")
DOC_NUMBER_PATTERN = re.compile(r"Sayı\s*:\s*[^-]+-([0-9]+)")
TOPIC_PATTERN = re.compile(r"Konu\s*:\s*(.+)", re.IGNORECASE)


class ParsedDocument:
    def __init__(
        self,
        topic: str,
        content: str,
        doc_number: Optional[str],
        doc_date: Optional[datetime],
    ) -> None:
        self.topic = topic
        self.content = content
        self.doc_number = doc_number
        self.doc_date = doc_date


def extract_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    text_parts = []
    for page in reader.pages:
        text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)


def parse_pdf(pdf_path: Path) -> ParsedDocument:
    raw_text = extract_text(pdf_path)
    topic_match = TOPIC_PATTERN.search(raw_text)
    topic = topic_match.group(1).strip() if topic_match else "Bilinmeyen Konu"

    doc_number_match = DOC_NUMBER_PATTERN.search(raw_text)
    doc_number = doc_number_match.group(1) if doc_number_match else None

    doc_date = _extract_date(raw_text)

    content = _extract_content(raw_text, topic_match)
    return ParsedDocument(topic=topic, content=content, doc_number=doc_number, doc_date=doc_date)


def _extract_date(raw_text: str) -> Optional[datetime]:
    match = DATE_PATTERN.search(raw_text)
    if match:
        try:
            return datetime.strptime(".".join(match.groups()), "%Y.%m.%d")
        except ValueError:
            return None
    return None


def _extract_content(raw_text: str, topic_match: Optional[re.Match[str]]) -> str:
    if not topic_match:
        return raw_text.strip()
    start = topic_match.end()
    return raw_text[start:].strip()


def renamed_filename(parsed: ParsedDocument, original_stem: str) -> str:
    date_str = parsed.doc_date.strftime("%Y.%m.%d") if parsed.doc_date else datetime.now().strftime("%Y.%m.%d")
    safe_topic = re.sub(r"[^\w.-]+", "_", parsed.topic) or original_stem
    return f"{date_str}_{safe_topic}.pdf"


def load_pdf_bytes(pdf_path: Path) -> bytes:
    return pdf_path.read_bytes()
