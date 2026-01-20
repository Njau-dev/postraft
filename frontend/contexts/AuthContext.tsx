'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { setToken, getToken, removeToken } from '@/lib/auth';
import { User, Plan } from '@/types';

interface AuthContextType {
  user: User | null;
  plan: Plan | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, user_name: string) => Promise<void>;
  forgotPassword: (email: string) => Promise<void>;
  resetPassword: (token: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}


const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [plan, setPlan] = useState<Plan | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Fetch current user on mount
  useEffect(() => {
    const initAuth = async () => {
      const token = getToken();
      if (token) {
        try {
          const response = await api.get('/auth/me');
          setUser(response.data.data.user);
          setPlan(response.data.data.plan);
        } catch (error) {
          removeToken();
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password });
    const { user, token } = response.data.data;

    setToken(token);
    setUser(user);

    // Fetch full user data including plan
    await refreshUser();

    router.push('/dashboard');
  };

  const register = async (email: string, password: string, user_name: string) => {
    const response = await api.post('/auth/register', { email, password, user_name });
    const { user, token } = response.data.data;

    setToken(token);
    setUser(user);

    // Fetch full user data including plan
    await refreshUser();

    router.push('/dashboard');
  };

  const logout = () => {
    removeToken();
    setUser(null);
    setPlan(null);
    router.push('/login');
  };

  const refreshUser = async () => {
    try {
      const response = await api.get('/auth/me');
      setUser(response.data.data.user);
      setPlan(response.data.data.plan);
    } catch (error) {
      console.error('Failed to refresh user:', error);
    }
  };

  const forgotPassword = async (email: string) => {
    await api.post('/auth/forgot-password', { email })
  }

  const resetPassword = async (token: string, password: string) => {
    await api.post('/auth/reset-password', {
      token,
      password,
    })
  }

  return (
    <AuthContext.Provider
      value={{ user, plan, loading, login, register, forgotPassword, resetPassword, logout, refreshUser }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
