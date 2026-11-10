
import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from app.security.password import hash_password, verify_password
from app.schemas.user import UserCreate, UserRead


# Password hashing tests

def test_password_is_hashed():
    password = "TestPassword123"
    hashed = hash_password(password)

    assert hashed != password
    assert hashed.startswith("$argon2")


def test_correct_password_verification():
    password = "TestPassword123"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_incorrect_password_verification():
    hashed = hash_password("TestPassword123")

    assert verify_password("WrongPassword123", hashed) is False


def test_same_password_produces_different_hashes():
    password = "TestPassword123"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    # Argon2 generates a unique salt for each hash.
    assert first_hash != second_hash

    # Both hashes should still verify successfully.
    assert verify_password(password, first_hash)
    assert verify_password(password, second_hash)


# Pydantic UserCreate schema tests

def test_valid_user_creation_schema():
    user = UserCreate(
        username="testuser",
        email="test@example.com",
        password="TestPassword123"
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.password == "TestPassword123"


def test_invalid_email_is_rejected():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="invalid-email",
            password="TestPassword123"
        )


def test_short_password_is_rejected():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="test@example.com",
            password="short"
        )


def test_short_username_is_rejected():
    with pytest.raises(ValidationError):
        UserCreate(
            username="ab",
            email="test@example.com",
            password="TestPassword123"
        )


# Pydantic UserRead schema tests

def test_user_read_does_not_expose_password_hash():
    user = UserRead(
        id=1,
        username="testuser",
        email="test@example.com",
        created_at=datetime.now(timezone.utc)
    )

    user_data = user.model_dump()

    assert "password_hash" not in user_data
    assert "password" not in user_data
    assert user_data["username"] == "testuser"
