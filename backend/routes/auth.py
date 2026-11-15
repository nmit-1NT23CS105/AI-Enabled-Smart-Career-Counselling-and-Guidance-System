import hashlib
import secrets
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from backend.models.user import AuthResponse, LoginRequest, RegisterRequest
from backend.services.storage import store


router = APIRouter(tags=["Authentication"])


def _hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    salt = salt or secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        120_000,
    ).hex()
    return salt, password_hash


def _verify_password(password: str, salt: str, expected_hash: str) -> bool:
    _, candidate_hash = _hash_password(password, salt)
    return secrets.compare_digest(candidate_hash, expected_hash)


def _public_user(user: dict) -> dict:
    return {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "academic_level": user["academic_level"],
        "created_at": user["created_at"],
    }


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest) -> dict:
    if store.find_user_by_email(payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    salt, password_hash = _hash_password(payload.password)
    user = {
        "id": str(uuid.uuid4()),
        "full_name": payload.full_name,
        "email": payload.email,
        "password_hash": password_hash,
        "salt": salt,
        "academic_level": payload.academic_level,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "assessments": [],
        "latest_recommendations": [],
    }

    users = store.read_users()
    users.append(user)
    store.write_users(users)

    return {
        "message": "Registration successful.",
        "user": _public_user(user),
        "session_token": secrets.token_urlsafe(32),
    }


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest) -> dict:
    user = store.find_user_by_email(payload.email)
    if not user or not _verify_password(payload.password, user["salt"], user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    return {
        "message": "Login successful.",
        "user": _public_user(user),
        "session_token": secrets.token_urlsafe(32),
    }
