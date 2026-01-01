# API Contracts: Connect Todo App Frontend with Backend using Python FastAPI

**Feature**: Connect Todo App Frontend with Backend using Python FastAPI
**Date**: 2025-12-29
**Contracts**: Claude Code

## Overview

This document defines the API contracts between the Next.js frontend and FastAPI backend for the Todo application, specifying the endpoints, request/response formats, and error handling.

## Backend API Contracts

### Base URL
```
http://localhost:8000/api/v1  # For development
https://api.example.com/v1    # For production
```

### Authentication
All API requests require an Authorization header if authentication is implemented:
```
Authorization: Bearer {token}
```

### Todo Endpoints

#### GET /todos
- **Purpose**: Retrieve all todos
- **Request**: No body required
- **Response**:
  - Status: 200 OK
  - Body: `{ "data": [Todo], "message": "Todos retrieved successfully" }`
- **Error Response**: 500 Internal Server Error

#### POST /todos
- **Purpose**: Create a new todo
- **Request Body**: `{ "title": "Todo title", "completed": false }`
- **Response**:
  - Status: 201 Created
  - Body: `{ "data": Todo, "message": "Todo created successfully" }`
- **Error Response**: 400 Bad Request, 500 Internal Server Error

#### GET /todos/{id}
- **Purpose**: Retrieve a specific todo
- **Request**: No body required
- **Response**:
  - Status: 200 OK
  - Body: `{ "data": Todo, "message": "Todo retrieved successfully" }`
- **Error Response**: 404 Not Found, 500 Internal Server Error

#### PUT /todos/{id}
- **Purpose**: Update a specific todo
- **Request Body**: `{ "title"?: "New title", "completed"?: true/false }`
- **Response**:
  - Status: 200 OK
  - Body: `{ "data": Todo, "message": "Todo updated successfully" }`
- **Error Response**: 400 Bad Request, 404 Not Found, 500 Internal Server Error

#### DELETE /todos/{id}
- **Purpose**: Delete a specific todo
- **Response**:
  - Status: 200 OK
  - Body: `{ "data": Todo, "message": "Todo deleted successfully" }`
- **Error Response**: 404 Not Found, 500 Internal Server Error

## Frontend Component Contracts

### TodoForm Component
```typescript
interface TodoFormProps {
  onSubmit: (title: string) => void;
  initialTitle?: string;
  submitLabel: string;
  onCancel?: () => void;
}
```

- **Purpose**: Handle user input for creating or editing a todo
- **Input**: Callback function to handle form submission, optional initial title, submit button label
- **Output**: Calls onSubmit with the todo title when form is submitted
- **Behavior**: Validates that title is not empty before submitting

### TodoItem Component
```typescript
interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onUpdate: (id: string, title: string) => void;
  onDelete: (id: string) => void;
  onEditStart?: (id: string) => void;
}
```

- **Purpose**: Display a single todo with interactive controls
- **Input**: Todo object and callback functions for different actions
- **Output**: UI elements for toggling completion, editing, and deleting
- **Behavior**: Renders todo with checkbox, title display, and action buttons

### TodoList Component
```typescript
interface TodoListProps {
  todos: Todo[];
  onToggle: (id: string) => void;
  onUpdate: (id: string, title: string) => void;
  onDelete: (id: string) => void;
  emptyMessage?: string;
}
```

- **Purpose**: Display a list of todos
- **Input**: Array of todos and callback functions for actions
- **Output**: List of TodoItem components or empty state message
- **Behavior**: Handles empty state display when no todos exist

### HomePage Component
```typescript
interface HomePageProps {}
```

- **Purpose**: Main page component that orchestrates the todo application
- **Input**: None
- **Output**: Complete todo application UI
- **Behavior**: Manages state for todos, handles API calls, and coordinates between components

## Error Handling Contracts

### API Error Response Format
```typescript
interface ApiError {
  detail: string;  // Error message from FastAPI
}
```

### Frontend Error Handling
- Network errors should display user-friendly messages
- Validation errors should be shown inline with the relevant form field
- Loading states should be displayed during API requests
- Error boundaries should catch and handle unexpected errors gracefully