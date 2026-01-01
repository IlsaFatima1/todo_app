"""User service for handling user authentication operations."""

from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
from utils import verify_password, get_password_hash

from models import User, UserCreate


def create_user(session: Session, user_data: UserCreate) -> User:
    """Create a new user with hashed password.

    Args:
        session: Database session
        user_data: User creation data including name, email and plain text password

    Returns:
        Created User object
    """
    # Check if user with this email already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise ValueError("Email already registered")

    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Create the user object
    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Add to session and commit
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user with email and password.

    Args:
        session: Database session
        email: User's email
        password: User's plain text password

    Returns:
        User object if authentication is successful, None otherwise
    """
    # Find user by email
    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        return None

    # Verify the password
    if not verify_password(password, user.password_hash):
        return None

    # Update last login time
    user.last_login_at = datetime.utcnow()
    user.updated_at = datetime.utcnow()
    session.add(user)
    session.commit()

    return user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Get a user by their email.

    Args:
        session: Database session
        email: User's email

    Returns:
        User object if found, None otherwise
    """
    user = session.exec(select(User).where(User.email == email)).first()
    return user


def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    """Get a user by their ID.

    Args:
        session: Database session
        user_id: User's ID

    Returns:
        User object if found, None otherwise
    """
    user = session.get(User, user_id)
    return user