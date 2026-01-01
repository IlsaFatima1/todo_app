"""Debug script to test the registration endpoint function directly."""

from main import register_user_endpoint
from models import UserCreate
from database import get_session

def test_endpoint():
    print("Testing registration endpoint function directly...")

    # Create user data
    user_data = UserCreate(email="new_direct_test@example.com", password="testpass")

    # Get session
    session_gen = get_session()
    session = next(session_gen)

    try:
        result = register_user_endpoint(user_data, session)
        print(f"Registration successful: {result}")
    except Exception as e:
        print(f"Error in endpoint: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    test_endpoint()