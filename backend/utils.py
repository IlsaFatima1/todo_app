"""
Utility functions for the Todo Application.
Contains helper functions for displaying tasks and other utilities.
"""
from typing import List, Dict
import bcrypt


def print_tasks(tasks: List[Dict]) -> None:
    """
    Display a list of tasks in a formatted way

    Args:
        tasks: List of task dictionaries with 'id', 'description', 'completed' keys
    """
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        # Handle malformed task objects gracefully
        task_id = task.get("id", "Unknown")
        description = task.get("description", "No description")
        completed = task.get("completed", False)
        status = "[X]" if completed else "[ ]"
        print(f"{task_id}. {status} {description}")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password to compare against

    Returns:
        True if the password matches, False otherwise
    """
    # Encode both passwords to bytes before comparison
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for a plain text password.

    Args:
        password: The plain text password to hash

    Returns:
        The hashed password
    """
    # Truncate password to 72 bytes to comply with bcrypt limitations
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    # Generate salt and hash the password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')