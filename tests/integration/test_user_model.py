
import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.database.connection import SessionLocal
from app.database.models import User


@pytest.fixture
def db_session():
    """Create a database session for each integration test."""

    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


def test_create_user_in_database(db_session):
    """Verify that a user can be saved in PostgreSQL."""

    unique_id = uuid.uuid4().hex[:10]

    user = User(
        username=f"testuser_{unique_id}",
        email=f"{unique_id}@example.com",
        password_hash="test_password_hash"
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.username == f"testuser_{unique_id}"
    assert user.email == f"{unique_id}@example.com"
    assert user.password_hash == "test_password_hash"
    assert user.created_at is not None

    # Remove the test record so it does not remain in the database.
    db_session.delete(user)
    db_session.commit()


def test_duplicate_username_is_rejected(db_session):
    """Verify that PostgreSQL prevents duplicate usernames."""

    unique_id = uuid.uuid4().hex[:10]

    first_user = User(
        username=f"duplicate_{unique_id}",
        email=f"first_{unique_id}@example.com",
        password_hash="test_hash"
    )

    db_session.add(first_user)
    db_session.commit()

    duplicate_user = User(
        username=f"duplicate_{unique_id}",
        email=f"second_{unique_id}@example.com",
        password_hash="test_hash"
    )

    db_session.add(duplicate_user)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()

    # Clean up the first user.
    db_session.delete(first_user)
    db_session.commit()


def test_duplicate_email_is_rejected(db_session):
    """Verify that PostgreSQL prevents duplicate email addresses."""

    unique_id = uuid.uuid4().hex[:10]
    shared_email = f"{unique_id}@example.com"

    first_user = User(
        username=f"first_{unique_id}",
        email=shared_email,
        password_hash="test_hash"
    )

    db_session.add(first_user)
    db_session.commit()

    duplicate_user = User(
        username=f"second_{unique_id}",
        email=shared_email,
        password_hash="test_hash"
    )

    db_session.add(duplicate_user)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()

    # Clean up the first user.
    db_session.delete(first_user)
    db_session.commit()
