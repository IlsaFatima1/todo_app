'use client';

import { useState, useEffect } from 'react';
import TodoForm from '@/components/TodoForm';
import TodoList from '@/components/TodoList';
import { Todo } from '@/types/todo';
import { api } from '@/lib/api';
import { useAuth } from '@/context/auth-context';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import Navbar from '@/components/auth/Navbar';

export default function DashboardPage() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const { isAuthenticated } = useAuth();

  // Load todos on component mount
  useEffect(() => {
    if (isAuthenticated) {
      const fetchTodos = async () => {
        try {
          setLoading(true);
          const response = await api.getTodos();
          setTodos(response.data as Todo[]);
        } catch (err) {
          setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
          setLoading(false);
        }
      };

      fetchTodos();
    } else {
      // If not authenticated, redirect to login
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  const handleAddTodo = async (title: string) => {
    try {
      const response = await api.createTodo({ title });
      setTodos(prev => [...prev, response.data as Todo]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    }
  };

  const handleToggleTodo = async (id: string) => {
    const todo = todos.find(t => t.id === id);
    if (todo) {
      try {
        const response = await api.updateTodo(id, { completed: !todo.completed });
        setTodos(prev =>
          prev.map(t =>
            t.id === id ? response.data as Todo : t
          )
        );
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      }
    }
  };

  const handleUpdateTodo = async (id: string, title: string) => {
    try {
      const response = await api.updateTodo(id, { title });
      setTodos(prev =>
        prev.map(t =>
          t.id === id ? response.data as Todo : t
        )
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    }
  };

  const handleDeleteTodo = async (id: string) => {
    try {
      await api.deleteTodo(id);
      setTodos(prev => prev.filter(t => t.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    }
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <div className="py-8">
            <div className="max-w-2xl mx-auto px-4">
              <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">Todo Dashboard</h1>
              <div className="flex justify-center items-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
              </div>
            </div>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="py-8">
          <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">Todo Dashboard</h1>

            {error && (
              <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-lg">
                Error: {error}
              </div>
            )}

            <TodoForm
              onSubmit={handleAddTodo}
              submitLabel="Add Task"
            />

            <TodoList
              todos={todos}
              onToggle={handleToggleTodo}
              onUpdate={handleUpdateTodo}
              onDelete={handleDeleteTodo}
            />
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}