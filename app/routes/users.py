
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import User
from app.schemas.user import UserCreate, UserRead
from app.security.password import hash_password


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=201
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user with a securely hashed password."""

    # Hash the password before saving it.
    hashed_password = hash_password(user_data.password)

    # Create the SQLAlchemy user object.
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists."
        )

    return new_user


@router.get(
    "/",
    response_model=list[UserRead]
)
def get_users(
    db: Session = Depends(get_db)
):
    """Retrieve all registered users."""

    return db.query(User).order_by(User.id).all()


@router.get(
    "/{user_id}",
    response_model=UserRead
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Retrieve a user by their ID."""

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return user
