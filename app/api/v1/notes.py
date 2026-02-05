"""Notes API - CRUD using Firestore, scoped by Firebase Auth user."""

import logging

from fastapi import APIRouter, Depends, HTTPException, Path

from app.core.auth import get_current_user_uid
from app.models.note import NoteCreate, NoteResponse, NoteUpdate
from app.services import note_firestore_service

logger = logging.getLogger("app.api.notes")

router = APIRouter()


@router.get("", response_model=list[NoteResponse])
async def list_notes(user_id: str = Depends(get_current_user_uid)):
    """List user's notes."""
    logger.info("GET /notes start user_id=%s", user_id)
    try:
        result = note_firestore_service.list_notes(user_id)
        logger.info("GET /notes success user_id=%s count=%d", user_id, len(result))
        return [_note_to_response(n) for n in result]
    except Exception as exc:  # noqa: BLE001
        logger.exception("GET /notes failed for user_id=%s: %s", user_id, exc)
        raise HTTPException(
            status_code=500,
            detail="Internal server error while listing notes",
        ) from exc


@router.post("", response_model=NoteResponse, status_code=201)
async def create_note(body: NoteCreate, user_id: str = Depends(get_current_user_uid)):
    """Create a note."""
    doc_id = note_firestore_service.create_note(user_id, body)
    note = note_firestore_service.get_note(user_id, doc_id)
    return _note_to_response(note)


@router.put("/{id}", response_model=NoteResponse)
async def update_note(
    note_id: str = Path(..., alias="id"),
    body: NoteUpdate = ...,
    user_id: str = Depends(get_current_user_uid),
):
    """Update a note."""
    try:
        note_firestore_service.update_note(user_id, note_id, body)
    except ValueError:
        raise HTTPException(404, "Note not found")
    updated = note_firestore_service.get_note(user_id, note_id)
    return _note_to_response(updated)


@router.delete("/{id}", status_code=204)
async def delete_note(
    note_id: str = Path(..., alias="id"),
    user_id: str = Depends(get_current_user_uid),
):
    """Delete a note."""
    try:
        note_firestore_service.delete_note(user_id, note_id)
    except ValueError:
        raise HTTPException(404, "Note not found")


def _note_to_response(note: dict) -> NoteResponse:
    """Normalize Firestore doc to NoteResponse (ensure user_id and is_pinned)."""
    is_pinned = bool(note.get("is_pinned", False))
    return NoteResponse(
        id=note["id"],
        user_id=note.get("user_id", ""),
        title=note.get("title", ""),
        content=note.get("content", ""),
        is_pinned=is_pinned,
        created_at=note.get("created_at"),
        updated_at=note.get("updated_at"),
    )
