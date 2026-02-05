# services

Business logic and Firestore/Realtime Database operations.

## Purpose

- Keep route handlers thin: they validate input, call services, and return responses.
- Services contain Firestore write/read logic and any transformations that don't belong in Pydantic.

## Firestore services

### firestore_service.py

Generic Firestore operations (any collection):

| Function | Description |
|----------|-------------|
| `set_document(collection, document_id, data, merge=False)` | Set a document by ID (create or overwrite). |
| `add_document(collection, data)` | Add a new document with auto-generated ID. |
| `update_document(collection, document_id, data)` | Partial update; fails if doc does not exist. |
| `delete_document(collection, document_id)` | Delete a document. |
| `get_document(collection, document_id)` | Get one document (returns dict with `id` or `None`). |
| `list_documents(collection)` | List all documents in a collection. |
| `list_documents_where(collection, field, value)` | List documents where `field == value` (e.g. `user_id == uid`). |

Uses `app.core.firebase.get_firestore()`. Data is normalized for Firestore (e.g. Pydantic models converted to dict, timestamps supported).

### note_firestore_service.py

Note-specific Firestore CRUD (collection `notes`), scoped by **user_id** (Firebase Auth uid). Each note document has a `user_id` field; list/get/update/delete enforce ownership.

| Function | Description |
|----------|-------------|
| `create_note(user_id, data: NoteCreate)` | Create note for user; sets `user_id`, `created_at`, `updated_at`. |
| `get_note(user_id, note_id)` | Get one note if it belongs to the user; else `None`. |
| `list_notes(user_id)` | List all notes where `user_id` equals the given uid. |
| `update_note(user_id, note_id, data: NoteUpdate)` | Partial update; raises if note not found or not owned. |
| `delete_note(user_id, note_id)` | Delete note; raises if not found or not owned. |

Used by `api/v1/notes.py`; `user_id` comes from `get_current_user_uid` (Firebase ID token).
