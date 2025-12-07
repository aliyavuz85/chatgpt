from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from . import models, schemas
from .db import get_session, init_db
from .ingest import DOCS_DIR, ingest_all_from_docs_dir

app = FastAPI(title="Evrak Takip API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()
    ingest_all_from_docs_dir()


def get_db() -> Session:
    with get_session() as session:
        yield session


@app.get("/documents", response_model=schemas.PaginatedDocuments)
def list_documents(
    q: str | None = Query(None, description="Konu veya içerik araması"),
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
) -> schemas.PaginatedDocuments:
    stmt = select(models.Document)
    if q:
        stmt = stmt.where(
            models.Document.topic.ilike(f"%{q}%") | models.Document.content.ilike(f"%{q}%")
        )

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.scalar(count_stmt) or 0

    offset = (page - 1) * page_size
    items = db.scalars(stmt.offset(offset).limit(page_size)).all()

    return schemas.PaginatedDocuments(
        total=total,
        page=page,
        page_size=page_size,
        items=[schemas.DocumentResponse.model_validate(item) for item in items],
    )


@app.get("/documents/{doc_id}/content", response_model=schemas.DocumentResponse)
def get_document(doc_id: int, db: Session = Depends(get_db)) -> schemas.DocumentResponse:
    document = db.get(models.Document, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Evrak bulunamadı")
    return schemas.DocumentResponse.model_validate(document)


@app.get("/documents/{doc_id}/file")
def open_document(doc_id: int, db: Session = Depends(get_db)) -> Response:
    document = db.get(models.Document, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Evrak bulunamadı")
    return Response(
        content=document.pdf_data,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={document.stored_name}"},
    )


@app.post("/ingest")
def ingest_directory(db: Session = Depends(get_db)) -> dict[str, str]:
    ingest_all_from_docs_dir()
    return {"status": "ok", "message": f"{DOCS_DIR} içindeki PDF'ler işlendi"}
