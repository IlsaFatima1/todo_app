# Data Model: Next.js Todo Application Frontend

**Feature**: Next.js Todo Application Frontend
**Date**: 2025-12-29
**Modeler**: Claude Code

## Overview

The data model for the Next.js Todo Application Frontend defines the TypeScript interfaces and data structures used in the application. The model is designed to work with both client-side state management and backend API integration.

## Core Entity: Todo

### TypeScript Interface
```typescript
interface Todo {
  id: string;              // Unique identifier for each task
  title: string;           // Task description/title
  completed: boolean;      // Status indicating whether the task is completed (default: false)
  createdAt: Date;         // Timestamp when the task was created
  updatedAt?: Date;        // Timestamp when the task was last updated (optional)
}
```

### Example
```typescript
{
  id: "123e4567-e89b-12d3-a456-426614174000",
  title: "Buy groceries",
  completed: false,
  createdAt: new Date("2025-12-29T10:30:00Z"),
  updatedAt: new Date("2025-12-29T10:30:00Z")
}
```

## State Management Structure

### Todo State in Components
- **todos**: Array of Todo objects
- **loading**: Boolean indicating API request status
- **error**: String or null for error messages
- **editingId**: String or null for tracking which item is being edited

### Example State Structure
```typescript
{
  todos: [
    {
      id: "123e4567-e89b-12d3-a456-426614174000",
      title: "Buy groceries",
      completed: false,
      createdAt: new Date("2025-12-29T10:30:00Z")
    },
    {
      id: "123e4567-e89b-12d3-a456-426614174001",
      title: "Walk the dog",
      completed: true,
      createdAt: new Date("2025-12-29T09:15:00Z")
    }
  ],
  loading: false,
  error: null,
  editingId: null
}
```

## API Contract Interface

### Request/Response Types
```typescript
// For creating a new todo
interface CreateTodoRequest {
  title: string;
}

// For updating an existing todo
interface UpdateTodoRequest {
  title?: string;
  completed?: boolean;
}

// For API responses
interface TodoApiResponse {
  data: Todo | Todo[];
  message?: string;
  error?: string;
}
```

## Component Props Interface

### TodoForm Props
```typescript
interface TodoFormProps {
  onSubmit: (title: string) => void;
  initialTitle?: string;
  submitLabel: string;
  onCancel?: () => void;
}
```

### TodoItem Props
```typescript
interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onUpdate: (id: string, title: string) => void;
  onDelete: (id: string) => void;
  onEditStart?: (id: string) => void;
}
```

### TodoList Props
```typescript
interface TodoListProps {
  todos: Todo[];
  onToggle: (id: string) => void;
  onUpdate: (id: string, title: string) => void;
  onDelete: (id: string) => void;
  emptyMessage?: string;
}
```

## Relationships

Since this is a single-entity application, there are no complex relationships. Each todo is independent with its own unique ID.