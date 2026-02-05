"""Generic Firestore write operations."""

import logging
from datetime import datetime
from typing import Any

from firebase_admin import firestore

from app.core.firebase import get_firestore

logger = logging.getLogger("app.services.firestore")


def _ensure_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Convert Pydantic model or dict to plain dict for Firestore (timestamps, etc.)."""
    out: dict[str, Any] = {}
    for k, v in data.items():
        if v is None:
            continue
        if isinstance(v, datetime):
            out[k] = v
        elif hasattr(v, "model_dump"):
            out[k] = v.model_dump(exclude_none=True)
        elif isinstance(v, dict):
            out[k] = _ensure_dict(v)
        else:
            out[k] = v
    return out


def set_document(
    collection: str,
    document_id: str,
    data: dict[str, Any],
    merge: bool = False,
) -> str:
    """
    Set a document by ID. Creates or overwrites.
    :param collection: Collection name.
    :param document_id: Document ID.
    :param data: Document data (dict or Pydantic model dict).
    :param merge: If True, merge with existing; else overwrite.
    :return: Document ID.
    """
    client = get_firestore()
    ref = client.collection(collection).document(document_id)
    payload = _ensure_dict(dict(data))
    ref.set(payload, merge=merge)
    logger.info("set_document collection=%s id=%s", collection, document_id)
    return document_id


def add_document(collection: str, data: dict[str, Any]) -> str:
    """
    Add a new document with auto-generated ID.
    :param collection: Collection name.
    :param data: Document data.
    :return: Generated document ID.
    """
    client = get_firestore()
    ref = client.collection(collection).document()
    payload = _ensure_dict(dict(data))
    ref.set(payload)
    logger.info("add_document collection=%s id=%s", collection, ref.id)
    return ref.id


def update_document(
    collection: str,
    document_id: str,
    data: dict[str, Any],
) -> None:
    """
    Update existing document (partial update). Fails if document does not exist.
    :param collection: Collection name.
    :param document_id: Document ID.
    :param data: Fields to update.
    """
    client = get_firestore()
    ref = client.collection(collection).document(document_id)
    payload = _ensure_dict(dict(data))
    ref.update(payload)
    logger.info("update_document collection=%s id=%s", collection, document_id)


def delete_document(collection: str, document_id: str) -> None:
    """
    Delete a document.
    :param collection: Collection name.
    :param document_id: Document ID.
    """
    client = get_firestore()
    client.collection(collection).document(document_id).delete()
    logger.info("delete_document collection=%s id=%s", collection, document_id)


def get_document(collection: str, document_id: str) -> dict[str, Any] | None:
    """
    Get a document by ID.
    :return: Document data with id, or None if not found.
    """
    client = get_firestore()
    ref = client.collection(collection).document(document_id)
    doc = ref.get()
    if not doc.exists:
        logger.info("get_document not found collection=%s id=%s", collection, document_id)
        return None
    data = doc.to_dict()
    data["id"] = doc.id
    logger.info("get_document found collection=%s id=%s", collection, document_id)
    return data


def list_documents(collection: str) -> list[dict[str, Any]]:
    """
    List all documents in a collection.
    :return: List of documents (each with id in the dict).
    """
    client = get_firestore()
    docs = list(client.collection(collection).stream())
    logger.info("list_documents collection=%s count=%d", collection, len(docs))
    return [{"id": d.id, **d.to_dict()} for d in docs]


def list_documents_where(
    collection: str,
    field: str,
    value: Any,
    order_by: str | None = None,
    descending: bool = False,
) -> list[dict[str, Any]]:
    """
    List documents where field equals value (e.g. userId == uid).

    Optionally order by a field (e.g. created_at) ascending or descending.
    :return: List of documents (each with id in the dict).
    """
    client = get_firestore()
    logger.info(
        "list_documents_where collection=%s field=%s value=%s order_by=%s descending=%s",
        collection,
        field,
        value,
        order_by,
        descending,
    )
    query = client.collection(collection).where(field, "==", value)
    if order_by:
        direction = firestore.Query.DESCENDING if descending else firestore.Query.ASCENDING
        query = query.order_by(order_by, direction=direction)
    docs = query.stream()
    return [{"id": d.id, **d.to_dict()} for d in docs]
