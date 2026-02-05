"""Firebase Admin SDK initialization: Realtime Database and Firestore."""

from pathlib import Path

from firebase_admin import credentials, db, firestore, initialize_app

from app.config import settings

_app = None
_db_ref = None
_firestore_client = None


def init_firebase() -> None:
    """Initialize Firebase Admin SDK, Realtime Database and Firestore."""
    global _app, _db_ref, _firestore_client
    if _app is not None:
        return
    cred_path = Path(settings.firebase_credentials_path)
    if not cred_path.exists():
        raise FileNotFoundError(
            f"Firebase credentials not found at {cred_path}. "
            "Copy your service account JSON to config/firebase-service-account.json"
        )
    cred = credentials.Certificate(str(cred_path))
    opts = {"databaseURL": settings.firebase_database_url} if settings.firebase_database_url else {}
    _app = initialize_app(cred, opts)
    if settings.firebase_database_url:
        _db_ref = db.reference()
    _firestore_client = firestore.client()


def close_firebase() -> None:
    """Clean up Firebase (optional; SDK has no explicit close)."""
    global _app, _db_ref, _firestore_client
    _db_ref = None
    _firestore_client = None
    _app = None


def get_db() -> "db.Reference | None":
    """Return Firebase Realtime Database root reference. None if not configured."""
    return _db_ref


def get_firestore():
    """Return Firestore client. Available after init_firebase()."""
    return _firestore_client
