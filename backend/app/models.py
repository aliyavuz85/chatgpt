from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy import Date, Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    stored_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    topic: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    doc_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    doc_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    pdf_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
