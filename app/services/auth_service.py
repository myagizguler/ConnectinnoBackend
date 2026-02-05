"""Auth: register (Firebase Admin create_user) and login (Firebase REST signIn)."""

import httpx

from firebase_admin import auth

from app.config import settings

FIREBASE_REST_SIGN_IN = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"


async def _sign_in_with_password(email: str, password: str) -> dict:
    """Call Firebase REST API signInWithPassword; returns response with idToken, etc."""
    if not settings.firebase_web_api_key:
        raise ValueError("FIREBASE_WEB_API_KEY is not set")
    url = f"{FIREBASE_REST_SIGN_IN}?key={settings.firebase_web_api_key}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
    if "idToken" not in data:
        raise ValueError("Firebase did not return idToken")
    return data


def register_user(email: str, password: str, display_name: str | None = None) -> str:
    """
    Create a new Firebase user via Admin SDK.
    :return: uid
    """
    kwargs: dict = {"email": email, "password": password}
    if display_name is not None:
        kwargs["display_name"] = display_name
    user = auth.create_user(**kwargs)
    return user.uid


async def register_and_sign_in(
    email: str, password: str, display_name: str | None = None
) -> dict:
    """
    Create user via Admin SDK, then sign in via REST to get idToken.
    :return: dict with id_token, refresh_token, uid, email, expires_in
    """
    register_user(email, password, display_name)
    data = await _sign_in_with_password(email, password)
    return {
        "id_token": data["idToken"],
        "refresh_token": data.get("refreshToken", ""),
        "uid": data["localId"],
        "email": data.get("email", email),
        "expires_in": int(data.get("expiresIn", 3600)),
    }


async def login(email: str, password: str) -> dict:
    """
    Sign in via Firebase REST API; return idToken etc.
    :return: dict with id_token, refresh_token, uid, email, expires_in
    """
    data = await _sign_in_with_password(email, password)
    return {
        "id_token": data["idToken"],
        "refresh_token": data.get("refreshToken", ""),
        "uid": data["localId"],
        "email": data.get("email", email),
        "expires_in": int(data.get("expiresIn", 3600)),
    }
