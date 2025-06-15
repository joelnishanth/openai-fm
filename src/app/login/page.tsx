"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { signIn } from '@/lib/auth';


import { useAuth } from "react-oidc-context";

export default function LoginPage() {
  const auth = useAuth();

  if (auth.isLoading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  if (auth.error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Error: {auth.error.message}</p>
      </div>
    );
  }

  if (auth.isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-custom-gray">
        <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md text-center">
          <p className="mb-4">Hello, {auth.user?.profile.email}</p>
          <button
            onClick={() => auth.signoutRedirect()}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 rounded-md transition"
          >
            Sign out
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-custom-gray">
      <button
        onClick={() => auth.signinRedirect()}
        className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-md transition"
      >
        Sign in
      </button>
    </div>
  );
}