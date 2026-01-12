'use client';

import { ReactNode, createContext, useContext, useState, useEffect } from 'react';
import { useStore } from '@/lib/store';

interface AuthContextType {
  user: any;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const { token, user, login: storeLogin, logout: storeLogout, fetchUserInfo: storeFetchUserInfo } = useStore();

  // Check for existing token on mount
  useEffect(() => {
    const savedToken = localStorage.getItem('auth_token');
    if (savedToken) {
      storeLogin(savedToken, null); // We'll fetch user info after login
      // Optionally fetch user info with the token
      fetchUserInfoFromToken(savedToken);
    }
  }, []);

  const fetchUserInfoFromToken = async (token: string) => {
    try {
      const response = await fetch('http://localhost:8002/auth/me', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const userData = await response.json();
        // Update user in store - we need to call the store's login again to update user
        // Since store login expects both token and user, we'll call it with current token
        storeLogin(token, userData);
      }
    } catch (error) {
      console.error('Failed to fetch user info:', error);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await fetch('http://localhost:8002/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
      }

      const data = await response.json();
      if (data.access_token) {
        // Use store's login function to update state
        storeLogin(data.access_token, data.user);
        localStorage.setItem('auth_token', data.access_token);
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const register = async (email: string, password: string) => {
    try {
      const response = await fetch('http://localhost:8002/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }

      const data = await response.json();
      if (data.access_token) {
        // Use store's login function to update state
        storeLogin(data.access_token, data.user);
        localStorage.setItem('auth_token', data.access_token);
      }
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = () => {
    storeLogout();
    localStorage.removeItem('auth_token');
  };

  const isAuthenticated = !!token;

  const value = {
    user,
    token,
    login,
    register,
    logout,
    isAuthenticated,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuthContext() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
}