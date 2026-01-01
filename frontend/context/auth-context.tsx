"use client"

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Define the shape of our auth context
interface AuthContextType {
  user: any | null;
  token: string | null;
  loading: boolean;
  login: (token: string, userData: any) => void;
  logout: () => void;
  register: (name: string, email: string, password: string) => Promise<void>;
  isAuthenticated: boolean;
}

// Create the context with default values
const AuthContext = createContext<AuthContextType>(undefined!);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<any | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Check for existing token in localStorage on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('auth_token');
    const storedUser = localStorage.getItem('auth_user');

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = (token: string, userData: any) => {
    // The backend returns the token and user data directly after login
    setToken(token);
    setUser(userData);
    localStorage.setItem('auth_token', token);
    localStorage.setItem('auth_user', JSON.stringify(userData));
  };

  const register = async (name: string, email: string, password: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1'}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Registration failed');
      }

      const data = await response.json();
      const { data: authData, message } = data;

      if (authData && authData.access_token) {
        setToken(authData.access_token);
        setUser(authData.user);
        localStorage.setItem('auth_token', authData.access_token);
        localStorage.setItem('auth_user', JSON.stringify(authData.user));
      }
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
  };

  const isAuthenticated = !!token;

  const contextValue: AuthContextType = {
    user,
    token,
    loading,
    login,
    logout,
    register,
    isAuthenticated,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};