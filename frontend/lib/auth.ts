import { Todo } from '@/types/todo';

// Utility function to get the auth token from localStorage
export const getAuthToken = (): string | null => {
  return localStorage.getItem('auth_token');
};

// Utility function to add auth headers to requests
export const getAuthHeaders = (): { [key: string]: string } => {
  const token = getAuthToken();
  const headers: { [key: string]: string } = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  return headers;
};

// Utility function to check if user is authenticated
export const isAuthenticated = (): boolean => {
  return !!getAuthToken();
};

// Utility function to logout and clear auth data
export const logout = (): void => {
  localStorage.removeItem('auth_token');
  localStorage.removeItem('auth_user');
};

// Utility function to refresh token if needed
export const refreshTokenIfNeeded = async (): Promise<boolean> => {
  // In a real implementation, you would check if the token is expired
  // and refresh it if needed. For now, we'll just return true.
  return true;
};

// Example API call using auth headers
export const getTodosWithAuth = async (): Promise<Todo[]> => {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'}/todos`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token might be expired, logout the user
        logout();
        throw new Error('Authentication required');
      }
      const errorData = await response.json().catch(() => ({}));
      const errorMessage = errorData.detail || errorData.message || `HTTP error! status: ${response.status}`;
      throw new Error(errorMessage);
    }

    const data = await response.json();
    return data.data || [];
  } catch (error) {
    console.error('Error fetching todos:', error);
    throw error;
  }
};

// Utility function to handle API errors related to authentication
export const handleAuthError = (error: any): void => {
  if (error.message === 'Authentication required' || error.status === 401) {
    // Redirect to login page or handle auth error appropriately
    console.log('Redirecting to login page due to auth error');
    // In a real app, you might redirect to login page here
  }
};