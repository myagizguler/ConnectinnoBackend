"""Auth API: register and login (returns id_token for Notes API)."""

import logging

import httpx
from firebase_admin import auth
from fastapi import APIRouter, HTTPException

from app.models.auth import AuthResponse, LoginRequest, RegisterRequest
from app.services import auth_service

logger = logging.getLogger("app.api.auth")

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=201)
async def register(body: RegisterRequest):
    """
    Register a new user. Creates the user in Firebase and returns id_token
    so you can call Notes API immediately with Authorization: Bearer <id_token>.
    """
    logger.info("POST /register called email=%s", body.email)
    try:
        result = await auth_service.register_and_sign_in(
            email=body.email,
            password=body.password,
            display_name=body.display_name,
        )
        logger.info("POST /register succeeded email=%s uid=%s", result.get("email"), result.get("uid"))
        return AuthResponse(**result)
    except auth.EmailAlreadyExistsError:
        raise HTTPException(409, "Email already registered. Use /login instead.")
    except ValueError as e:
        if "FIREBASE_WEB_API_KEY" in str(e) or "not set" in str(e):
            raise HTTPException(503, "Auth not configured (FIREBASE_WEB_API_KEY).")
        raise HTTPException(400, detail=str(e))
    except httpx.HTTPStatusError as e:
        logger.exception("HTTP error during register for email=%s", body.email)
        _handle_firebase_rest_error(e)
    except Exception as e:
        # Catch-all to surface configuration errors like CONFIGURATION_NOT_FOUND
        err = str(e)
        logger.exception("Unexpected error during register for email=%s: %s", body.email, err)
        if "CONFIGURATION_NOT_FOUND" in err or "No auth provider" in err:
            raise HTTPException(
                503,
                "Firebase Auth not configured. In Firebase Console: "
                "Authentication → Sign-in method → enable 'Email/Password'.",
            ) from e
        raise HTTPException(500, "Unexpected error during registration")
    except Exception as e:
        if "CONFIGURATION_NOT_FOUND" in str(e) or "No auth provider" in str(e):
            raise HTTPException(
                503,
                "Firebase Auth not configured. In Firebase Console: "
                "Authentication → Sign-in method → Enable 'Email/Password'.",
            ) from e
        raise


@router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest):
    """
    Login with email and password. Returns id_token for use in
    Authorization: Bearer <id_token> on Notes API.
    """
    logger.info("POST /login called email=%s", body.email)
    try:
        result = await auth_service.login(email=body.email, password=body.password)
        logger.info("POST /login succeeded email=%s uid=%s", result.get("email"), result.get("uid"))
        return AuthResponse(**result)
    except ValueError as e:
        if "FIREBASE_WEB_API_KEY" in str(e) or "not set" in str(e):
            raise HTTPException(503, "Auth not configured (FIREBASE_WEB_API_KEY).")
        raise HTTPException(400, detail=str(e))
    except httpx.HTTPStatusError as e:
        logger.exception("HTTP error during login for email=%s", body.email)
        _handle_firebase_rest_error(e)
    except Exception as e:
        err = str(e)
        logger.exception("Unexpected error during login for email=%s: %s", body.email, err)
        raise HTTPException(500, "Unexpected error during login")


def _handle_firebase_rest_error(e: httpx.HTTPStatusError) -> None:
    """Map Firebase REST error response to HTTPException."""
    try:
        body = e.response.json()
        msg = (body.get("error", {}) or {}).get("message", "")
    except Exception:
        msg = str(e)
    if "EMAIL_EXISTS" in msg:
        raise HTTPException(409, "Email already registered. Use /login instead.")
    if "INVALID_LOGIN_CREDENTIALS" in msg or "INVALID_EMAIL" in msg or "INVALID_PASSWORD" in msg:
        raise HTTPException(401, "Invalid email or password.")
    raise HTTPException(e.response.status_code, detail=msg or "Auth request failed.")
