# API Contracts: CLI Todo Application

**Feature**: CLI Todo Application
**Date**: 2025-12-29
**Contracts**: Claude Code

## Overview

This document defines the contracts for the CLI Todo Application, specifying the interfaces between different components and the expected behavior of each function.

## Todo Class Contracts

### Class Definition
```python
class Todo:
    def __init__(self):
        """Initialize the Todo class with empty task list and ID counter"""
```

### Public Methods

#### add_task(description: str) -> int
- **Purpose**: Add a new task to the task list
- **Input**: Task description as string
- **Output**: Integer ID of the newly created task
- **Side Effects**: Adds task to internal task list
- **Preconditions**: Description must be a non-empty string
- **Postconditions**: Task exists in the task list with unique ID
- **Error Handling**: Returns -1 if description is empty

#### delete_task(task_id: int) -> bool
- **Purpose**: Remove a task by its ID
- **Input**: Task ID as integer
- **Output**: Boolean indicating success (True) or failure (False)
- **Side Effects**: Removes task from internal task list if found
- **Preconditions**: Task ID must be a positive integer
- **Postconditions**: Task no longer exists in task list
- **Error Handling**: Returns False if task ID not found

#### update_task(task_id: int, new_description: str) -> bool
- **Purpose**: Update the description of an existing task
- **Input**: Task ID as integer, new description as string
- **Output**: Boolean indicating success (True) or failure (False)
- **Side Effects**: Updates description of task in internal task list
- **Preconditions**: Task ID must be valid, new description must be non-empty
- **Postconditions**: Task description updated in task list
- **Error Handling**: Returns False if task ID not found or description is empty

#### mark_complete(task_id: int, completed: bool = True) -> bool
- **Purpose**: Mark a task as complete or incomplete
- **Input**: Task ID as integer, completion status as boolean (default True)
- **Output**: Boolean indicating success (True) or failure (False)
- **Side Effects**: Updates completion status of task in internal task list
- **Preconditions**: Task ID must be valid
- **Postconditions**: Task completion status updated in task list
- **Error Handling**: Returns False if task ID not found

#### get_task(task_id: int) -> dict or None
- **Purpose**: Retrieve a specific task by its ID
- **Input**: Task ID as integer
- **Output**: Task dictionary if found, None if not found
- **Side Effects**: None
- **Preconditions**: Task ID must be a positive integer
- **Postconditions**: None
- **Error Handling**: Returns None if task ID not found

#### get_all_tasks() -> list
- **Purpose**: Retrieve all tasks
- **Input**: None
- **Output**: List of all task dictionaries
- **Side Effects**: None
- **Preconditions**: None
- **Postconditions**: None
- **Error Handling**: Returns empty list if no tasks exist

#### get_pending_tasks() -> list
- **Purpose**: Retrieve all incomplete tasks
- **Input**: None
- **Output**: List of incomplete task dictionaries
- **Side Effects**: None
- **Preconditions**: None
- **Postconditions**: None
- **Error Handling**: Returns empty list if no pending tasks exist

#### get_completed_tasks() -> list
- **Purpose**: Retrieve all completed tasks
- **Input**: None
- **Output**: List of completed task dictionaries
- **Side Effects**: None
- **Preconditions**: None
- **Postconditions**: None
- **Error Handling**: Returns empty list if no completed tasks exist

## Utility Function Contracts

### print_tasks(tasks: list) -> None
- **Purpose**: Display a list of tasks in a formatted way
- **Input**: List of task dictionaries
- **Output**: None (prints to console)
- **Side Effects**: Prints formatted task list to stdout
- **Preconditions**: Tasks must be in expected format with 'id', 'description', 'completed' keys
- **Postconditions**: Tasks displayed to user
- **Error Handling**: Handles malformed task objects gracefully

## Application Function Contracts

### show_menu() -> None
- **Purpose**: Display the main menu options to the user
- **Input**: None
- **Output**: None (prints to console)
- **Side Effects**: Prints menu to stdout
- **Preconditions**: None
- **Postconditions**: Menu displayed to user

### add_task(todo: Todo) -> None
- **Purpose**: Handle the user interaction for adding a task
- **Input**: Todo instance
- **Output**: None
- **Side Effects**: Adds task to Todo instance via user input
- **Preconditions**: Todo instance must be valid
- **Postconditions**: Task added to Todo instance if input valid

### update_task(todo: Todo) -> None
- **Purpose**: Handle the user interaction for updating a task
- **Input**: Todo instance
- **Output**: None
- **Side Effects**: Updates task in Todo instance via user input
- **Preconditions**: Todo instance must be valid
- **Postconditions**: Task updated in Todo instance if input valid

### delete_task(todo: Todo) -> None
- **Purpose**: Handle the user interaction for deleting a task
- **Input**: Todo instance
- **Output**: None
- **Side Effects**: Deletes task from Todo instance via user input
- **Preconditions**: Todo instance must be valid
- **Postconditions**: Task removed from Todo instance if input valid

### complete_task(todo: Todo) -> None
- **Purpose**: Handle the user interaction for marking a task complete
- **Input**: Todo instance
- **Output**: None
- **Side Effects**: Updates task completion status in Todo instance via user input
- **Preconditions**: Todo instance must be valid
- **Postconditions**: Task completion status updated in Todo instance if input valid

### main() -> None
- **Purpose**: Main application loop that handles user interaction
- **Input**: None
- **Output**: None
- **Side Effects**: Runs the CLI application loop
- **Preconditions**: None
- **Postconditions**: Application runs until user exits
- **Error Handling**: Handles invalid user input gracefully