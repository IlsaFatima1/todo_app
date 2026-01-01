# Data Model: Connect Todo App Frontend with Backend using Python FastAPI

**Feature**: Connect Todo App Frontend with Backend using Python FastAPI
**Date**: 2025-12-29
**Modeler**: Claude Code

## Overview

The data model for the Todo application defines the Pydantic models for request/response validation and the data structure for in-memory storage in the FastAPI backend.

## Pydantic Models

### TodoCreate Model
```python
class TodoCreate(BaseModel):
    title: str
    completed: bool = False
```

**Purpose**: Used for validating requests to create a new todo item.
**Fields**:
- `title`: Required string representing the task description
- `completed`: Optional boolean with default value False

### TodoUpdate Model
```python
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
```

**Purpose**: Used for validating requests to update an existing todo item.
**Fields**:
- `title`: Optional string for updating the task description
- `completed`: Optional boolean for updating completion status

### Todo Response Model
```python
class Todo(BaseModel):
    id: str
    title: str
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
```

**Purpose**: Used for validating responses that return todo items.
**Fields**:
- `id`: Unique identifier for the todo item
- `title`: String representing the task description
- `completed`: Boolean indicating completion status
- `created_at`: Timestamp when the todo was created
- `updated_at`: Optional timestamp when the todo was last updated

## In-Memory Data Structure

### Todo Storage Format
```python
todos: Dict[str, Todo] = {}
```

**Purpose**: Dictionary to store todos in memory with ID as key and Todo object as value.
**Structure**:
- Key: String ID of the todo
- Value: Todo object with all properties

### Example Storage Entry
```python
{
    "1": {
        "id": "1",
        "title": "Learn FastAPI",
        "completed": False,
        "created_at": "2025-12-29T10:00:00Z",
        "updated_at": "2025-12-29T10:00:00Z"
    },
    "2": {
        "id": "2",
        "title": "Build a todo app",
        "completed": True,
        "created_at": "2025-12-29T10:15:00Z",
        "updated_at": "2025-12-29T10:20:00Z"
    }
}
```

## API Endpoints

### GET /todos
- **Method**: GET
- **Description**: Retrieve all todos
- **Response**: List of Todo objects

### POST /todos
- **Method**: POST
- **Request Body**: TodoCreate object
- **Description**: Create a new todo
- **Response**: Created Todo object

### GET /todos/{id}
- **Method**: GET
- **Description**: Retrieve a specific todo by ID
- **Response**: Todo object

### PUT /todos/{id}
- **Method**: PUT
- **Request Body**: TodoUpdate object
- **Description**: Update a specific todo by ID
- **Response**: Updated Todo object

### DELETE /todos/{id}
- **Method**: DELETE
- **Description**: Delete a specific todo by ID
- **Response**: Deleted Todo object