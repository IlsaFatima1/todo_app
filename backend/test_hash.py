"""Test script to debug password hashing issue."""

from utils import get_password_hash

if __name__ == "__main__":
    print("Testing password hashing...")

    # Test with various password lengths
    test_passwords = [
        "123456",
        "testpass",
        "a" * 50,
        "a" * 70,
        "a" * 72,
        "a" * 73,  # This might cause issues
        "a" * 100,  # This should definitely cause issues
    ]

    for i, password in enumerate(test_passwords):
        try:
            print(f"Test {i+1}: Password length = {len(password)}")
            print(f"  Byte length = {len(password.encode('utf-8'))}")
            hashed = get_password_hash(password)
            print(f"  Success: {hashed[:20]}...")
        except Exception as e:
            print(f"  Error: {e}")
        print()