import re
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_password_strength(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Za-z]", password):
        raise ValueError("Password must include at least one letter.")
    if not re.search(r"\d", password):
        raise ValueError("Password must include at least one number.")
    return password


class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=80)
    email: str = Field(..., max_length=120)
    password: str = Field(..., max_length=128)
    confirm_password: str = Field(..., max_length=128)
    academic_level: str = Field(..., min_length=2, max_length=60)

    @field_validator("full_name", "academic_level", mode="before")
    @classmethod
    def normalize_required_text(cls, value: Any) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("This field is required.")
        return value.strip()

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: Any) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Email is required.")
        email = value.strip().lower()
        if not EMAIL_PATTERN.match(email):
            raise ValueError("Enter a valid email address.")
        return email

    @field_validator("password")
    @classmethod
    def password_is_strong(cls, value: str) -> str:
        return validate_password_strength(value)

    @model_validator(mode="after")
    def passwords_match(self) -> "RegisterRequest":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        return self


class LoginRequest(BaseModel):
    email: str = Field(..., max_length=120)
    password: str = Field(..., min_length=1, max_length=128)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: Any) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Email is required.")
        email = value.strip().lower()
        if not EMAIL_PATTERN.match(email):
            raise ValueError("Enter a valid email address.")
        return email


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    academic_level: str
    created_at: str


class AuthResponse(BaseModel):
    message: str
    user: UserResponse
    session_token: str
