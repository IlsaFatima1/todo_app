# Quickstart: Authentication for Todo Application

## Prerequisites

- Node.js 18+ for frontend
- Python 3.11+ for backend
- Better Auth account/credentials (if required)
- Existing database setup from previous todo-db feature

## Setup

### 1. Install Dependencies

Add Better Auth to the frontend:

```bash
cd frontend
npm install better-auth
```

Add authentication dependencies to the backend:

```bash
cd backend
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

### 2. Configure Better Auth

Create authentication configuration for frontend and backend integration.

### 3. Update Database Models

The User model needs to be added to the existing models.py file with proper relationships to Todo entities.

## Implementation Steps

### 1. Update Models

Update the models.py file to include the User model:

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, max_length=255)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login_at: Optional[datetime] = Field(default=None)

    # Relationship to todos
    todos: List["Todo"] = Relationship(back_populates="user")

# Update Todo model to include user relationship
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")  # Updated from optional to required

    # Relationship to user
    user: Optional[User] = Relationship(back_populates="todos")
```

### 2. Create Authentication Module

Create an auth.py file with authentication functions:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from backend.database import get_session
from backend.models import User
from sqlmodel import Session, select
from jose import JWTError, jwt
from passlib.context import CryptContext

# Security configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_session)) -> int:
    """Get the current user ID from the authentication token."""
    try:
        # Decode the token and extract user ID
        # This is a simplified implementation - actual implementation will depend on Better Auth integration
        token = credentials.credentials
        # Verify token and return user ID
        user_id = verify_token(token)
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_token(token: str) -> Optional[int]:
    """Verify the authentication token and return user ID."""
    # Implementation depends on Better Auth token format
    # This is a placeholder for the actual implementation
    pass
```

### 3. Update CRUD Operations

Modify existing CRUD operations to be user-scoped:

```python
def get_todos(session: Session, user_id: int, offset: int = 0, limit: int = 100) -> List[Todo]:
    """Retrieve todos for a specific user."""
    statement = select(Todo).where(Todo.user_id == user_id).offset(offset).limit(limit)
    result = session.exec(statement)
    return result.fetchall()

def create_todo(session: Session, user_id: int, title: str, description: Optional[str] = None, completed: bool = False) -> Todo:
    """Create a new todo for a specific user."""
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
```

### 4. Protect API Endpoints

Update API endpoints to require authentication:

```python
from backend.auth import get_current_user_id

@app.get("/api/v1/todos", response_model=dict)
def get_todos_endpoint(
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Retrieve todos for the authenticated user."""
    todos = get_todos(session, current_user_id)
    # ... rest of implementation
```

## Running the Application

1. Update the database with the new User model:
```bash
cd backend
python -c "from database import init_db; init_db()"
```

2. Start the backend:
```bash
cd backend
uvicorn main:app --reload
```

3. Start the frontend:
```bash
cd frontend
npm run dev
```

## Testing Authentication

Verify that:
- Users can register and login
- Protected endpoints return 401 for unauthenticated requests
- Users can only access their own todos
- Authentication state is synchronized between frontend and backend