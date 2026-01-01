# Data Model: CLI Todo Application

**Feature**: CLI Todo Application
**Date**: 2025-12-29
**Modeler**: Claude Code

## Overview

The data model for the CLI Todo Application defines the structure and relationships of the core entities used in the application. The application uses in-memory storage with a simple but effective design.

## Core Entity: Task

### Attributes
- **id** (int): Unique identifier for each task (auto-incremented)
- **description** (str): Text description of the task
- **completed** (bool): Status indicating whether the task is completed (default: False)
- **created_at** (datetime): Timestamp when the task was created (optional)

### Example
```python
{
    "id": 1,
    "description": "Buy groceries",
    "completed": False,
    "created_at": "2025-12-29 10:30:00"
}
```

## Data Storage Structure

### In-Memory Storage
- **tasks** (list): List of task dictionaries
- **next_id** (int): Counter for generating unique IDs

### Example Structure
```python
{
    "tasks": [
        {
            "id": 1,
            "description": "Buy groceries",
            "completed": False
        },
        {
            "id": 2,
            "description": "Walk the dog",
            "completed": True
        }
    ],
    "next_id": 3
}
```

## Todo Class Interface

### Public Methods
- `add_task(description: str) -> int`: Adds a new task and returns its ID
- `delete_task(task_id: int) -> bool`: Deletes a task by ID, returns success status
- `update_task(task_id: int, new_description: str) -> bool`: Updates task description, returns success status
- `mark_complete(task_id: int, completed: bool = True) -> bool`: Marks task as complete/incomplete, returns success status
- `get_task(task_id: int) -> dict or None`: Retrieves a specific task
- `get_all_tasks() -> list`: Returns all tasks
- `get_pending_tasks() -> list`: Returns only incomplete tasks
- `get_completed_tasks() -> list`: Returns only completed tasks

### Private Methods
- `_generate_id() -> int`: Generates the next unique ID
- `_find_task_index(task_id: int) -> int or None`: Finds the index of a task by ID

## Relationships

Since this is a single-entity application, there are no complex relationships. Each task is independent with its own unique ID.