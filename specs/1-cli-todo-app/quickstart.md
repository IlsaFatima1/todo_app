# Quickstart: CLI Todo Application

**Feature**: CLI Todo Application
**Date**: 2025-12-29
**Guide**: Claude Code

## Getting Started

The CLI Todo Application is a simple command-line tool for managing tasks in memory. Follow these steps to get started:

### Prerequisites
- Python 3.8 or higher
- No external dependencies required

### Running the Application

1. Navigate to the project directory
2. Run the application:
   ```bash
   python app.py
   ```

### Using the Application

Once the application starts, you'll see a menu with the following options:
1. Add a new task
2. View all tasks
3. Update a task
4. Delete a task
5. Mark a task as complete
6. Exit

### Example Workflow

1. **Add a task**: Select option 1 and enter your task description
2. **View tasks**: Select option 2 to see all your tasks
3. **Mark complete**: Select option 5, enter the task ID, and confirm completion
4. **Update task**: Select option 3, enter the task ID and new description
5. **Delete task**: Select option 4 and enter the task ID to remove

### Expected Output

When viewing tasks, you'll see output like:
```
1. [ ] Buy groceries
2. [X] Walk the dog
3. [ ] Finish report
```

Where [ ] indicates pending tasks and [X] indicates completed tasks.

## File Structure

The application consists of three main files:
- `todo.py`: Contains the Todo class for task management
- `utils.py`: Contains utility functions for displaying tasks
- `app.py`: Contains the CLI interface and main application logic