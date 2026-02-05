"""Pydantic models for Note (Firestore)."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class NoteCreate(BaseModel):
    """Payload for creating a note."""

    title: str = Field(..., min_length=1, max_length=256)
    content: str = Field("", max_length=50_000)
    is_pinned: bool = False


class NoteUpdate(BaseModel):
    """Payload for partial update of a note."""

    title: str | None = Field(None, min_length=1, max_length=256)
    content: str | None = Field(None, max_length=50_000)
    is_pinned: bool | None = None


class NoteResponse(BaseModel):
    """Note as returned from API."""

    id: str
    user_id: str
    title: str
    content: str
    is_pinned: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def coerce_datetime(cls, v: Any) -> datetime | None:
        """Coerce Firestore timestamp-like to datetime."""
        if v is None:
            return None
        if isinstance(v, datetime):
            return v
        if hasattr(v, "timestamp"):
            return datetime.fromtimestamp(v.timestamp())
        return v
