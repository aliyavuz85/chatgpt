from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sqlalchemy import select

from . import models
from .db import DATA_DIR, get_session
from .utils import ParsedDocument, load_pdf_bytes, parse_pdf, renamed_filename

DOCS_DIR = Path(__file__).resolve().parent.parent / "documents"
DOCS_DIR.mkdir(exist_ok=True, parents=True)


def ingest_documents(paths: Iterable[Path]) -> None:
    with get_session() as session:
        existing_names = {name for (name,) in session.execute(select(models.Document.stored_name)).all()}

        for pdf_path in paths:
            parsed = parse_pdf(pdf_path)
            new_name = renamed_filename(parsed, pdf_path.stem)
            if new_name in existing_names:
                continue

            stored_path = DATA_DIR / new_name
            stored_path.write_bytes(pdf_path.read_bytes())

            document = models.Document(
                stored_name=new_name,
                topic=parsed.topic,
                content=parsed.content,
                doc_number=parsed.doc_number,
                doc_date=parsed.doc_date.date() if parsed.doc_date else None,
                pdf_data=load_pdf_bytes(pdf_path),
            )
            session.add(document)
            existing_names.add(new_name)
        session.commit()


def ingest_all_from_docs_dir() -> None:
    pdfs = sorted(DOCS_DIR.glob("*.pdf"))
    ingest_documents(pdfs)
