"""CRUD operations for Todo items using SQLModel."""

from datetime import datetime
from typing import List, Optional

from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from models import Todo, User


def get_todos(session: Session, user_id: int, offset: int = 0, limit: int = 100) -> List[Todo]:
    """
    Retrieve all todos for a specific user with optional pagination.

    Args:
        session: Database session
        user_id: ID of the user whose todos to retrieve
        offset: Number of records to skip (for pagination)
        limit: Maximum number of records to return

    Returns:
        List of Todo objects
    """
    try:
        statement = select(Todo).where(Todo.user_id == user_id).offset(offset).limit(limit)
        result = session.exec(statement)
        return result.fetchall()
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving todos: {e}")


def create_todo(
    session: Session,
    title: str,
    user_id: int,
    description: Optional[str] = None,
    completed: bool = False
) -> Todo:
    """
    Create a new todo item for a specific user.

    Args:
        session: Database session
        title: Title of the todo
        user_id: ID of the user who owns the todo (required)
        description: Description of the todo (optional)
        completed: Whether the todo is completed (default: False)

    Returns:
        Created Todo object
    """
    try:
        todo = Todo(
            title=title,
            description=description,
            completed=completed,
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo
    except SQLAlchemyError as e:
        session.rollback()
        raise Exception(f"Error creating todo: {e}")


def update_todo(
    session: Session,
    todo_id: int,
    user_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None
) -> Optional[Todo]:
    """
    Update an existing todo item for a specific user.

    Args:
        session: Database session
        todo_id: ID of the todo to update
        user_id: ID of the user attempting to update (for ownership check)
        title: New title (optional)
        description: New description (optional)
        completed: New completed status (optional)

    Returns:
        Updated Todo object or None if not found or not owned by user
    """
    try:
        todo = session.get(Todo, todo_id)
        if not todo or todo.user_id != user_id:
            return None

        # Update fields if provided
        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        if completed is not None:
            todo.completed = completed

        # Update the timestamp
        todo.updated_at = datetime.utcnow()

        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo
    except SQLAlchemyError as e:
        session.rollback()
        raise Exception(f"Error updating todo: {e}")


def delete_todo(session: Session, todo_id: int, user_id: int) -> bool:
    """
    Delete a todo item for a specific user.

    Args:
        session: Database session
        todo_id: ID of the todo to delete
        user_id: ID of the user attempting to delete (for ownership check)

    Returns:
        True if deleted, False if not found or not owned by user
    """
    try:
        todo = session.get(Todo, todo_id)
        if not todo or todo.user_id != user_id:
            return False

        session.delete(todo)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        raise Exception(f"Error deleting todo: {e}")


def complete_todo(session: Session, todo_id: int, user_id: int, completed: bool) -> Optional[Todo]:
    """
    Mark a todo as completed or incomplete for a specific user.

    Args:
        session: Database session
        todo_id: ID of the todo to update
        user_id: ID of the user attempting to update (for ownership check)
        completed: Whether the todo should be marked as completed

    Returns:
        Updated Todo object or None if not found or not owned by user
    """
    try:
        todo = session.get(Todo, todo_id)
        if not todo or todo.user_id != user_id:
            return None

        todo.completed = completed
        todo.updated_at = datetime.utcnow()

        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo
    except SQLAlchemyError as e:
        session.rollback()
        raise Exception(f"Error updating todo completion status: {e}")