from fastapi import FastAPI, HTTPException, status, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import List
import uvicorn
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from models import TodoCreate, TodoUpdate, TodoComplete, TodoRead, UserCreate
from schemas import Todo
from database import get_session
from crud import get_todos, create_todo, update_todo, delete_todo, complete_todo
from user_service import create_user, authenticate_user
from auth import get_current_user_id, create_access_token
from sqlmodel import Session

app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handler to return consistent error format
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"data": None, "message": exc.detail}
    )

# Handle validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"data": None, "message": f"Validation error: {exc}"}
    )

@app.get("/api/v1/todos", response_model=dict)
def get_todos_endpoint(
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Retrieve all todos for the authenticated user
    """
    try:
        print("DEBUG: GET /api/v1/todos endpoint called")
        logger.info(f"Fetching todos for user ID: {current_user_id}")
        todos = get_todos(session, current_user_id)
        print(f"DEBUG: Retrieved {len(todos)} todos from database")
        logger.info(f"Retrieved {len(todos)} todos")
        # Convert SQLModel objects to Pydantic schemas using from_attributes
        todos_data = [TodoRead.model_validate(todo) for todo in todos]
        return {"data": todos_data, "message": "Todos retrieved successfully"}
    except Exception as e:
        print(f"DEBUG: Error in GET /api/v1/todos: {str(e)}")
        logger.error(f"Error retrieving todos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving todos"
        )


@app.post("/api/v1/todos", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_todo_endpoint(
    todo_data: TodoCreate,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new todo for the authenticated user
    """
    try:
        print(f"DEBUG: POST /api/v1/todos endpoint called with data: {todo_data}")
        logger.info(f"Creating new todo with title: {todo_data.title} for user ID: {current_user_id}")
        todo = create_todo(session, todo_data.title, current_user_id, todo_data.description, todo_data.completed)
        print(f"DEBUG: Todo created successfully with ID: {todo.id}")
        logger.info(f"Todo created successfully with ID: {todo.id}")
        # Convert SQLModel object to Pydantic schema
        todo_response = TodoRead(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
            user_id=todo.user_id
        )
        return {"data": todo_response, "message": "Todo created successfully"}
    except Exception as e:
        print(f"DEBUG: Error in POST /api/v1/todos: {str(e)}")
        logger.error(f"Error creating todo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating todo"
        )


@app.get("/api/v1/todos/{todo_id}", response_model=dict)
def get_todo_endpoint(
    todo_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific todo by ID for the authenticated user
    """
    from models import Todo
    try:
        print(f"DEBUG: GET /api/v1/todos/{todo_id} endpoint called")
        logger.info(f"Fetching todo with ID: {todo_id} for user ID: {current_user_id}")
        # Get the specific todo by ID
        todo = session.get(Todo, todo_id)
        if not todo or todo.user_id != current_user_id:
            print(f"DEBUG: Todo not found with ID: {todo_id} or not owned by user {current_user_id}")
            logger.warning(f"Todo not found with ID: {todo_id} or not owned by user {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        print(f"DEBUG: Todo retrieved successfully with ID: {todo_id}")
        logger.info(f"Todo retrieved successfully with ID: {todo_id}")
        # Convert SQLModel object to Pydantic schema using from_attributes
        todo_data = TodoRead.model_validate(todo)
        return {"data": todo_data, "message": "Todo retrieved successfully"}
    except HTTPException:
        print(f"DEBUG: HTTPException in GET /api/v1/todos/{todo_id}")
        raise
    except Exception as e:
        print(f"DEBUG: Error in GET /api/v1/todos/{todo_id}: {str(e)}")
        logger.error(f"Error retrieving todo {todo_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving todo"
        )


@app.put("/api/v1/todos/{todo_id}", response_model=dict)
def update_todo_endpoint(
    todo_id: int,
    todo_data: TodoUpdate,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update a specific todo by ID for the authenticated user
    """
    try:
        print(f"DEBUG: PUT /api/v1/todos/{todo_id} endpoint called with data: {todo_data}")
        logger.info(f"Updating todo with ID: {todo_id} for user ID: {current_user_id}")
        todo = update_todo(
            session,
            todo_id,
            current_user_id,
            todo_data.title,
            todo_data.description,
            todo_data.completed
        )
        if not todo:
            print(f"DEBUG: Todo not found for update with ID: {todo_id} or not owned by user {current_user_id}")
            logger.warning(f"Todo not found for update with ID: {todo_id} or not owned by user {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        print(f"DEBUG: Todo updated successfully with ID: {todo_id}")
        logger.info(f"Todo updated successfully with ID: {todo_id}")
        # Convert SQLModel object to Pydantic schema using from_attributes
        todo_data_response = TodoRead.model_validate(todo)
        return {"data": todo_data_response, "message": "Todo updated successfully"}
    except HTTPException:
        print(f"DEBUG: HTTPException in PUT /api/v1/todos/{todo_id}")
        raise
    except Exception as e:
        print(f"DEBUG: Error in PUT /api/v1/todos/{todo_id}: {str(e)}")
        logger.error(f"Error updating todo {todo_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating todo"
        )


@app.delete("/api/v1/todos/{todo_id}", response_model=dict)
def delete_todo_endpoint(
    todo_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a specific todo by ID for the authenticated user
    """
    try:
        print(f"DEBUG: DELETE /api/v1/todos/{todo_id} endpoint called")
        logger.info(f"Deleting todo with ID: {todo_id} for user ID: {current_user_id}")
        success = delete_todo(session, todo_id, current_user_id)
        if not success:
            print(f"DEBUG: Todo not found for deletion with ID: {todo_id} or not owned by user {current_user_id}")
            logger.warning(f"Todo not found for deletion with ID: {todo_id} or not owned by user {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        print(f"DEBUG: Todo deleted successfully with ID: {todo_id}")
        logger.info(f"Todo deleted successfully with ID: {todo_id}")
        return {"data": None, "message": "Todo deleted successfully"}
    except HTTPException:
        print(f"DEBUG: HTTPException in DELETE /api/v1/todos/{todo_id}")
        raise
    except Exception as e:
        print(f"DEBUG: Error in DELETE /api/v1/todos/{todo_id}: {str(e)}")
        logger.error(f"Error deleting todo {todo_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting todo"
        )


@app.get("/api/v1/health", response_model=dict)
def health_check():
    """
    Health check endpoint to verify API is running
    """
    return {"data": {"status": "healthy", "timestamp": datetime.now()}, "message": "API is running"}


@app.delete("/api/v1/todos", response_model=dict)
def delete_all_todos_endpoint(
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete all todos for the authenticated user - for testing purposes
    """
    try:
        print(f"DEBUG: DELETE /api/v1/todos endpoint called - clearing all todos for user {current_user_id}")
        # Get all todos for the current user and delete them one by one
        all_todos = get_todos(session, current_user_id)
        for todo in all_todos:
            delete_todo(session, todo.id, current_user_id)
        print("DEBUG: All todos cleared from database")
        return {"data": None, "message": "All todos deleted successfully"}
    except Exception as e:
        print(f"DEBUG: Error in DELETE /api/v1/todos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting all todos"
        )


@app.post("/api/v1/auth/register", response_model=dict)
def register_user_endpoint(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Register a new user with email and password
    """
    try:
        print(f"DEBUG: POST /api/v1/auth/register endpoint called with data: {user_data}")
        logger.info(f"Creating new user with email: {user_data.email}")

        # Validate input data
        print(f"DEBUG: Validating user data - email: {user_data.email}, password length: {len(user_data.password) if user_data.password else 0}")

        # Create the user
        user = create_user(session, user_data)

        print(f"DEBUG: User created successfully with ID: {user.id}")
        logger.info(f"User created successfully with ID: {user.id}")

        # Generate access token for the new user
        access_token = create_access_token(user.id)
        print(f"DEBUG: Generated access token for user ID: {user.id}")

        # Return user data and token
        user_response = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }

        print(f"DEBUG: Returning registration response for user ID: {user.id}")
        return {
            "data": {
                "user": user_response,
                "access_token": access_token,
                "token_type": "bearer"
            },
            "message": "User registered successfully"
        }
    except ValueError as e:
        print(f"DEBUG: ValueError in POST /api/v1/auth/register: {str(e)}")
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"DEBUG: Error in POST /api/v1/auth/register: {str(e)}")
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )


@app.post("/api/v1/auth/login", response_model=dict)
def login_user_endpoint(
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    """
    Authenticate user with email and password
    """
    try:
        print(f"DEBUG: POST /api/v1/auth/login endpoint called with email: {email}")
        logger.info(f"Login attempt for user with email: {email}")

        # Validate input data
        print(f"DEBUG: Validating login data - email: {email}, password length: {len(password) if password else 0}")

        # Authenticate the user
        user = authenticate_user(session, email, password)

        if not user:
            print(f"DEBUG: Invalid credentials for email: {email}")
            logger.warning(f"Invalid login attempt for email: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        print(f"DEBUG: User authenticated successfully with ID: {user.id}")
        logger.info(f"User authenticated successfully with ID: {user.id}")

        # Generate access token for the authenticated user
        access_token = create_access_token(user.id)
        print(f"DEBUG: Generated access token for user ID: {user.id}")

        # Return user data and token
        user_response = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }

        print(f"DEBUG: Returning login response for user ID: {user.id}")
        return {
            "data": {
                "user": user_response,
                "access_token": access_token,
                "token_type": "bearer"
            },
            "message": "Login successful"
        }
    except HTTPException:
        print(f"DEBUG: HTTPException in POST /api/v1/auth/login")
        raise
    except Exception as e:
        print(f"DEBUG: Error in POST /api/v1/auth/login: {str(e)}")
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during login"
        )


@app.post("/api/v1/auth/logout", response_model=dict)
def logout_user_endpoint(
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Logout the current user (token invalidation can be implemented later)
    """
    try:
        print(f"DEBUG: POST /api/v1/auth/logout endpoint called for user ID: {current_user_id}")
        logger.info(f"User logout for user ID: {current_user_id}")

        # In a real implementation, you might want to invalidate the token here
        print(f"DEBUG: User {current_user_id} logged out successfully")

        return {
            "data": None,
            "message": "Logout successful"
        }
    except Exception as e:
        print(f"DEBUG: Error in POST /api/v1/auth/logout: {str(e)}")
        logger.error(f"Error during logout: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during logout"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001, log_level="info")