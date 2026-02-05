"""Note CRUD using Firestore (write and read), scoped by user_id."""

from datetime import datetime

from app.models.note import NoteCreate, NoteUpdate
from app.services.firestore_service import (
    add_document,
    delete_document,
    get_document,
    list_documents_where,
    update_document,
)

COLLECTION = "notes"
USER_ID_FIELD = "user_id"


def _timestamp() -> datetime:
    return datetime.utcnow()


def create_note(user_id: str, data: NoteCreate) -> str:
    """
    Create a new note for the given user. Auto-generates ID and timestamps.
    :return: Document ID.
    """
    payload = data.model_dump(exclude_none=True)
    # Ensure is_pinned is always present; default to False
    payload.setdefault("is_pinned", False)
    payload[USER_ID_FIELD] = user_id
    payload["created_at"] = _timestamp()
    payload["updated_at"] = _timestamp()
    return add_document(COLLECTION, payload)


def get_note(user_id: str, note_id: str) -> dict | None:
    """Get a single note by ID if it belongs to the user."""
    doc = get_document(COLLECTION, note_id)
    if doc is None or doc.get(USER_ID_FIELD) != user_id:
        return None
    return doc


def list_notes(user_id: str) -> list[dict]:
    """List all notes for the given user, newest first (by created_at)."""
    return list_documents_where(
        COLLECTION,
        USER_ID_FIELD,
        user_id,
        order_by="created_at",
        descending=True,
    )


def update_note(user_id: str, note_id: str, data: NoteUpdate) -> None:
    """Partial update of a note. No-op if note does not exist or does not belong to user."""
    if get_note(user_id, note_id) is None:
        raise ValueError("Note not found or access denied")
    payload = data.model_dump(exclude_none=True)
    payload["updated_at"] = _timestamp()
    update_document(COLLECTION, note_id, payload)


def delete_note(user_id: str, note_id: str) -> None:
    """Delete a note by ID if it belongs to the user."""
    if get_note(user_id, note_id) is None:
        raise ValueError("Note not found or access denied")
    delete_document(COLLECTION, note_id)
