'use client';

import React from 'react';
import { TodoListProps } from '@/types/todo';
import TodoItem from './TodoItem';

const TodoList: React.FC<TodoListProps> = ({
  todos,
  onToggle,
  onUpdate,
  onDelete,
  emptyMessage = 'No tasks found. Add a new task to get started!'
}) => {
  if (todos.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={onToggle}
          onUpdate={onUpdate}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
};

export default TodoList;