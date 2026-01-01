"""
Todo class implementation for the CLI Todo Application.
Manages tasks in memory with CRUD operations.
"""
from datetime import datetime
from typing import Dict, List, Optional


class Todo:
    """
    Todo class that manages tasks in memory.
    Provides methods for adding, deleting, updating, and viewing tasks.
    """

    def __init__(self):
        """Initialize the Todo class with empty task list and ID counter"""
        self.tasks = []  # List of task dictionaries
        self.next_id = 1  # Counter for generating unique IDs

    def _generate_id(self) -> int:
        """Generate the next unique ID"""
        new_id = self.next_id
        self.next_id += 1
        return new_id

    def _find_task_index(self, task_id: int) -> Optional[int]:
        """Find the index of a task by ID"""
        for index, task in enumerate(self.tasks):
            if task["id"] == task_id:
                return index
        return None

    def add_task(self, description: str) -> int:
        """
        Add a new task to the task list

        Args:
            description: Task description as string

        Returns:
            Integer ID of the newly created task, or -1 if description is empty
        """
        if not description.strip():
            return -1

        task_id = self._generate_id()
        task = {
            "id": task_id,
            "description": description.strip(),
            "completed": False,
            "created_at": datetime.now()
        }
        self.tasks.append(task)
        return task_id

    def get_all_tasks(self) -> List[Dict]:
        """
        Retrieve all tasks

        Returns:
            List of all task dictionaries
        """
        return self.tasks.copy()

    def get_task(self, task_id: int) -> Optional[Dict]:
        """
        Retrieve a specific task by its ID

        Args:
            task_id: Task ID as integer

        Returns:
            Task dictionary if found, None if not found
        """
        index = self._find_task_index(task_id)
        if index is not None:
            return self.tasks[index].copy()
        return None

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task by its ID

        Args:
            task_id: Task ID as integer

        Returns:
            Boolean indicating success (True) or failure (False)
        """
        if task_id <= 0:
            return False

        index = self._find_task_index(task_id)
        if index is not None:
            self.tasks.pop(index)
            return True
        return False

    def update_task(self, task_id: int, new_description: str) -> bool:
        """
        Update the description of an existing task

        Args:
            task_id: Task ID as integer
            new_description: New description as string

        Returns:
            Boolean indicating success (True) or failure (False)
        """
        if task_id <= 0 or not new_description.strip():
            return False

        index = self._find_task_index(task_id)
        if index is not None:
            self.tasks[index]["description"] = new_description.strip()
            return True
        return False

    def mark_complete(self, task_id: int, completed: bool = True) -> bool:
        """
        Mark a task as complete or incomplete

        Args:
            task_id: Task ID as integer
            completed: Completion status as boolean (default True)

        Returns:
            Boolean indicating success (True) or failure (False)
        """
        if task_id <= 0:
            return False

        index = self._find_task_index(task_id)
        if index is not None:
            self.tasks[index]["completed"] = completed
            return True
        return False

    def get_pending_tasks(self) -> List[Dict]:
        """
        Retrieve all incomplete tasks

        Returns:
            List of incomplete task dictionaries
        """
        return [task for task in self.tasks if not task.get("completed", False)]

    def get_completed_tasks(self) -> List[Dict]:
        """
        Retrieve all completed tasks

        Returns:
            List of completed task dictionaries
        """
        return [task for task in self.tasks if task.get("completed", False)]