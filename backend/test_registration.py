"""Debug script to test user registration process."""

from database import get_session
from user_service import create_user
from models import UserCreate

def test_registration():
    print("Testing user registration...")

    # Create a user data object
    user_data = UserCreate(email="test3@example.com", password="testpass")

    # Create a database session
    session_gen = get_session()
    session = next(session_gen)

    try:
        # Try to create the user
        user = create_user(session, user_data)
        print(f"User created successfully: ID={user.id}, Email={user.email}")
        print(f"Password hash: {user.password_hash[:30]}...")
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    test_registration()