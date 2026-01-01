# Quickstart: Connect Todo App Frontend with Backend using Python FastAPI

**Feature**: Connect Todo App Frontend with Backend using Python FastAPI
**Date**: 2025-12-29
**Guide**: Claude Code

## Getting Started

This guide covers setting up the connection between the Next.js frontend and FastAPI backend for the Todo application.

### Prerequisites
- Python 3.8 or higher
- Node.js 18.x or higher
- npm or yarn package manager

### Setting Up the Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies using the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

3. The backend is already configured with:
   - `main.py`: FastAPI application with CORS, custom exception handlers, and comprehensive endpoints
   - `models.py`: Pydantic models for request validation (TodoCreate, TodoUpdate)
   - `schemas.py`: Pydantic schemas for response validation (Todo)
   - `database.py`: In-memory storage implementation with full CRUD operations

4. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

The backend will be available at http://localhost:8000

### Setting Up the Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Update the environment variables to point to your backend:
   ```bash
   # Create .env.local file with your backend URL
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
   # Or set it to a different port if needed
   # echo "NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1" > .env.local
   ```

4. Start the frontend development server:
   ```bash
   npm run dev
   ```

The frontend will be available at http://localhost:3000

### API Endpoints

The backend provides the following endpoints with consistent response format:

- `GET /api/v1/todos` - Get all todos
- `POST /api/v1/todos` - Create a new todo
- `GET /api/v1/todos/{id}` - Get a specific todo
- `PUT /api/v1/todos/{id}` - Update a specific todo
- `DELETE /api/v1/todos/{id}` - Delete a specific todo
- `GET /api/v1/health` - Health check endpoint

### Response Format

All API endpoints return consistent JSON responses:

**Success responses:**
```json
{
  "data": { /* todo object or array of todos */ },
  "message": "Operation completed successfully"
}
```

**Error responses:**
```json
{
  "data": null,
  "message": "Error description"
}
```

### Error Handling

The backend includes comprehensive error handling with:
- Custom exception handlers for consistent error format
- Proper HTTP status codes (404 for not found, 500 for server errors, etc.)
- Detailed error messages for debugging

### Testing the Connection

1. Start both backend and frontend servers
2. Open the frontend in your browser
3. Create a new todo item
4. Verify that the todo is stored in the backend
5. Refresh the page to confirm data persists

### Development Workflow

1. Define Pydantic models in `models.py` and `schemas.py`
2. Implement API endpoints in `main.py`
3. Update frontend API calls in `lib/api.ts` to connect to backend
4. Test endpoints using the frontend UI
5. Verify data persistence across page refreshes

### API Client Implementation

The frontend uses a centralized API client in `lib/api.ts` that provides:
- Consistent error handling for all API calls
- Loading states for better UX
- Automatic parsing of API responses
- Configurable base URL via environment variables
- Proper request/response formatting

### API Documentation

The API includes automatic OpenAPI documentation available at:
- `/docs` - Interactive API documentation (Swagger UI)
- `/redoc` - Alternative API documentation (ReDoc)
- `/openapi.json` - OpenAPI specification JSON