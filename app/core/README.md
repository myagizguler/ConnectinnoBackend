# core

Core modules used across the application.

## Modules

### firebase.py

- **`init_firebase()`** – Initializes Firebase Admin SDK (credentials from `config/firebase-service-account.json`), Realtime Database (if `FIREBASE_DATABASE_URL` is set), and Firestore. Call once at app startup.
- **`close_firebase()`** – Cleanup on shutdown (clears module-level references).
- **`get_db()`** – Returns the Firebase Realtime Database root `Reference`, or `None` if the database URL is not set.
- **`get_firestore()`** – Returns the Firestore client. Used by `app.services.firestore_service` for all Firestore write/read operations.

Credentials path and database URL come from `app.config.settings`. Ensure `.env` (or env vars) are set before starting the app.

### auth.py

- **`get_current_user_uid(credentials = Depends(HTTPBearer))`** – FastAPI dependency that reads `Authorization: Bearer <id_token>`, verifies the Firebase ID token with `auth.verify_id_token()`, and returns the Firebase Auth **uid**. Raises **401** if the header is missing or the token is invalid/expired. Use as `user_id: str = Depends(get_current_user_uid)` on routes that require the current user; notes API uses this so data is scoped by `user_id`.

## Adding More Core

- **Security**: JWT validation, API keys, rate limiting.
- **Logging**: Structured logger setup.
- **Dependencies**: FastAPI `Depends()` helpers that use `get_db()` or other core state.
