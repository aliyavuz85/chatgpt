from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class DocumentBase(BaseModel):
    stored_name: str
    topic: str
    content: str
    doc_number: Optional[str]
    doc_date: Optional[date]


class DocumentResponse(DocumentBase):
    id: int

    class Config:
        orm_mode = True


class PaginatedDocuments(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[DocumentResponse]
