# Quickstart: Todo Database Persistence

## Prerequisites

- Python 3.11+
- Neon PostgreSQL account with serverless database
- Environment variables configured:
  - `DATABASE_URL`: Neon PostgreSQL connection string (e.g., `postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require`)

## Setup

### 1. Install Dependencies

```bash
pip install sqlmodel fastapi uvicorn psycopg2-binary
```

### 2. Configure Environment

Create a `.env` file with your Neon PostgreSQL connection:

```bash
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

### 3. Initialize Database

Run the database initialization to create tables:

```python
from backend.database import init_db

# Initialize the database tables
init_db()
```

## Usage

### Database Session Setup

The `get_session` dependency provides database sessions to your API endpoints:

```python
from fastapi import Depends
from backend.database import get_session
from sqlmodel import Session

@app.get("/todos")
def get_todos(session: Session = Depends(get_session)):
    # Your database operations here
    pass
```

### CRUD Operations

Use the functions in `crud.py` for database operations:

```python
from backend.crud import create_todo, get_todos, update_todo, delete_todo, complete_todo

# Create a new todo
new_todo = create_todo(session, title="Buy groceries", description="Milk, bread, eggs")

# Get all todos
all_todos = get_todos(session)

# Update a todo
updated_todo = update_todo(session, todo_id=1, title="Buy groceries", completed=True)

# Complete a todo
completed_todo = complete_todo(session, todo_id=1, completed=True)

# Delete a todo
delete_todo(session, todo_id=1)
```

### Example API Integration

```python
from fastapi import FastAPI, Depends, HTTPException
from backend.database import get_session
from backend.crud import get_todos, create_todo
from sqlmodel import Session

app = FastAPI()

@app.get("/todos")
def read_todos(session: Session = Depends(get_session)):
    return get_todos(session)

@app.post("/todos")
def create_new_todo(todo_data: TodoCreate, session: Session = Depends(get_session)):
    try:
        return create_todo(session, todo_data.title, todo_data.description)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create todo")
```

## Running the Application

1. Initialize the database:
```bash
python -c "from backend.database import init_db; init_db()"
```

2. Start the application:
```bash
uvicorn backend.main:app --reload
```

The application will be available at `http://localhost:8000`.

## Testing Database Connection

Verify the database connection works:

```python
from backend.database import get_session

# Test session creation
session_gen = get_session()
session = next(session_gen)
try:
    # Test with a simple query
    result = session.exec("SELECT 1").first()
    print("Database connection successful:", result)
finally:
    session.close()
```