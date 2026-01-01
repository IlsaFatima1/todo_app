'use client';

import { useAuth } from '@/context/auth-context';
import Link from 'next/link';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <nav className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-xl font-bold">
          <Link href="/">Todo App</Link>
        </div>

        <div>
          {isAuthenticated ? (
            <div className="flex items-center space-x-4">
              <span>Welcome, {user?.name} </span>
              <button
                onClick={handleLogout}
                className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-md transition-colors"
              >
                Logout
              </button>
            </div>
          ) : (
            <div className="flex space-x-4">
              <Link href="/login" className="hover:underline">
                Login
              </Link>
              <Link href="/register" className="hover:underline">
                Register
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}