"""
CLI Application for the Todo Application.
Provides the main interface for users to interact with their tasks.
"""
from todo import Todo
from utils import print_tasks


def show_menu() -> None:
    """Display the main menu options to the user"""
    print("\n=== CLI Todo Application ===")
    print("1. Add a new task")
    print("2. View all tasks")
    print("3. Update a task")
    print("4. Delete a task")
    print("5. Mark a task as complete")
    print("6. Help")
    print("7. Exit")
    print("=============================")


def show_help() -> None:
    """Display help information to the user"""
    print("\n=== Help ===")
    print("1. Add a new task: Creates a new task with the provided description")
    print("2. View all tasks: Shows all tasks with their completion status")
    print("3. Update a task: Changes the description of an existing task")
    print("4. Delete a task: Removes a task from the list")
    print("5. Mark a task as complete: Changes the completion status of a task")
    print("6. Help: Shows this help information")
    print("7. Exit: Closes the application")
    print("=============================")


def add_task(todo: Todo) -> None:
    """Handle the user interaction for adding a task"""
    description = input("Enter task description: ").strip()
    if not description:
        print("Task description cannot be empty.")
        return

    task_id = todo.add_task(description)
    if task_id == -1:
        print("Failed to add task: description is empty.")
    else:
        print(f"Task added successfully with ID: {task_id}")


def update_task(todo: Todo) -> None:
    """Handle the user interaction for updating a task"""
    try:
        task_id = int(input("Enter task ID to update: "))
    except ValueError:
        print("Invalid task ID. Please enter a number.")
        return

    new_description = input("Enter new task description: ").strip()
    if not new_description:
        print("Task description cannot be empty.")
        return

    success = todo.update_task(task_id, new_description)
    if success:
        print(f"Task {task_id} updated successfully.")
    else:
        print(f"Failed to update task {task_id}. Task may not exist or invalid ID.")


def delete_task(todo: Todo) -> None:
    """Handle the user interaction for deleting a task"""
    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Invalid task ID. Please enter a number.")
        return

    success = todo.delete_task(task_id)
    if success:
        print(f"Task {task_id} deleted successfully.")
    else:
        print(f"Failed to delete task {task_id}. Task may not exist.")


def complete_task(todo: Todo) -> None:
    """Handle the user interaction for marking a task complete"""
    try:
        task_id = int(input("Enter task ID to mark as complete: "))
    except ValueError:
        print("Invalid task ID. Please enter a number.")
        return

    # Ask user if they want to mark as complete or incomplete
    status_input = input("Mark as complete? (y/n): ").strip().lower()
    completed = status_input in ['y', 'yes', '1', 'true']

    success = todo.mark_complete(task_id, completed)
    if success:
        status_str = "complete" if completed else "incomplete"
        print(f"Task {task_id} marked as {status_str} successfully.")
    else:
        print(f"Failed to mark task {task_id} as {'complete' if completed else 'incomplete'}. Task may not exist.")


def main() -> None:
    """Main application loop that handles user interaction"""
    todo = Todo()

    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_task(todo)
        elif choice == "2":
            tasks = todo.get_all_tasks()
            print("\nAll Tasks:")
            print_tasks(tasks)
        elif choice == "3":
            update_task(todo)
        elif choice == "4":
            delete_task(todo)
        elif choice == "5":
            complete_task(todo)
        elif choice == "6":
            show_help()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1-7.")


if __name__ == "__main__":
    main()