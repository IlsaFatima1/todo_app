import { Todo, CreateTodoRequest, UpdateTodoRequest, TodoApiResponse } from '@/types/todo';

// API functions for connecting to the Python backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1';

// Function to add headers to requests
const getHeaders = (includeAuth: boolean = true): { [key: string]: string } => {
  const headers: { [key: string]: string } = {
    'Content-Type': 'application/json',
  };

  if (includeAuth) {
    // Get token from localStorage
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('auth_token');
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }
  }

  return headers;
};

// API functions that connect to the Python backend
export const api = {
  // Get all todos
  getTodos: async (): Promise<TodoApiResponse> => {
    const response = await fetch(`${API_BASE_URL}/todos`, {
      method: 'GET',
      headers: getHeaders(),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      // Handle both standard FastAPI error format and custom format
      const errorMessage = errorData.detail || errorData.message || `HTTP error! status: ${response.status}`;

      // If it's an authentication error (401), we might want to handle it differently
      if (response.status === 401) {
        // Optionally clear the stored token if it's invalid
        if (typeof window !== 'undefined') {
          localStorage.removeItem('auth_token');
          localStorage.removeItem('auth_user');
        }
      }

      throw new Error(errorMessage);
    }

    const data = await response.json();
    return {
      data: data.data,
      message: data.message
    };
  },

  // Create a new todo
  createTodo: async (request: CreateTodoRequest): Promise<TodoApiResponse> => {
    const response = await fetch(`${API_BASE_URL}/todos`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      // Handle both standard FastAPI error format and custom format
      const errorMessage = errorData.detail || errorData.message || `HTTP error! status: ${response.status}`;

      // If it's an authentication error (401), we might want to handle it differently
      if (response.status === 401) {
        // Optionally clear the stored token if it's invalid
        if (typeof window !== 'undefined') {
          localStorage.removeItem('auth_token');
          localStorage.removeItem('auth_user');
        }
      }

      throw new Error(errorMessage);
    }

    const data = await response.json();
    return {
      data: data.data,
      message: data.message
    };
  },

  // Update an existing todo
  updateTodo: async (id: string, request: UpdateTodoRequest): Promise<TodoApiResponse> => {
    const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      // Handle both standard FastAPI error format and custom format
      const errorMessage = errorData.detail || errorData.message || `HTTP error! status: ${response.status}`;

      // If it's an authentication error (401), we might want to handle it differently
      if (response.status === 401) {
        // Optionally clear the stored token if it's invalid
        if (typeof window !== 'undefined') {
          localStorage.removeItem('auth_token');
          localStorage.removeItem('auth_user');
        }
      }

      throw new Error(errorMessage);
    }

    const data = await response.json();
    return {
      data: data.data,
      message: data.message
    };
  },

  // Delete a todo
  deleteTodo: async (id: string): Promise<TodoApiResponse> => {
    const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
      method: 'DELETE',
      headers: getHeaders(),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      // Handle both standard FastAPI error format and custom format
      const errorMessage = errorData.detail || errorData.message || `HTTP error! status: ${response.status}`;

      // If it's an authentication error (401), we might want to handle it differently
      if (response.status === 401) {
        // Optionally clear the stored token if it's invalid
        if (typeof window !== 'undefined') {
          localStorage.removeItem('auth_token');
          localStorage.removeItem('auth_user');
        }
      }

      throw new Error(errorMessage);
    }

    const data = await response.json();
    return {
      data: data.data,
      message: data.message
    };
  },
};