'use client';

import React, { useState } from 'react';
import { TodoFormProps } from '@/types/todo';

const TodoForm: React.FC<TodoFormProps> = ({
  onSubmit,
  initialTitle = '',
  submitLabel,
  onCancel
}) => {
  const [title, setTitle] = useState(initialTitle);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (title.trim() && !isLoading) {
      setIsLoading(true);
      try {
        await onSubmit(title.trim());
        setTitle('');
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6">
      <div className="flex gap-2">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter a new task..."
          disabled={isLoading}
          className={`flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${isLoading ? 'bg-gray-100' : ''}`}
          autoFocus
          aria-label="Task description"
        />
        <button
          type="submit"
          disabled={isLoading}
          className={`px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${isLoading ? 'bg-blue-400 text-gray-200 cursor-not-allowed' : 'bg-blue-500 text-white hover:bg-blue-600'}`}
          aria-label="Add task"
        >
          {isLoading ? 'Adding...' : submitLabel}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={isLoading}
            className={`px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 ${isLoading ? 'bg-gray-400 text-gray-200 cursor-not-allowed' : 'bg-gray-500 text-white hover:bg-gray-600'}`}
            aria-label="Cancel"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};

export default TodoForm;