"""Firebase Auth: verify ID token and return current user uid."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from firebase_admin import auth

security = HTTPBearer(auto_error=False)


def get_current_user_uid(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    """
    Verify Firebase ID token from Authorization: Bearer <token> and return uid.
    Raises 401 if missing or invalid.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header (Bearer token)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    try:
        decoded = auth.verify_id_token(token)
    except (ValueError, auth.InvalidIdTokenError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    uid = decoded.get("uid")
    if not uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing uid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return uid
