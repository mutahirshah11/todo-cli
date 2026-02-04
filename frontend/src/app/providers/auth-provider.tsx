'use client';

import React, { ReactNode, createContext, useContext, useState, useEffect, useRef } from 'react';
import { useStore } from '@/lib/store';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';

interface AuthContextType {
  user: any;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const { token: storeToken, user, login: storeLogin, logout: storeLogout, setTokenFromStorage } = useStore();
  const router = useRouter();

  // Initialize auth state from localStorage if store doesn't have a token
  useEffect(() => {
    if (typeof window !== 'undefined') {
      setTokenFromStorage();
    }
  }, [setTokenFromStorage]);

  // Track the last validated token to avoid re-validating the same token
  const lastValidatedToken = useRef<string | null>(null);

  // Check for existing token on mount and validate it
  useEffect(() => {
    // Ensure this only runs on the client side
    if (typeof window === 'undefined') return;

    const currentPath = window.location.pathname;
    const isAuthPage = currentPath.includes('/login') || currentPath.includes('/register');

    const currentToken = storeToken;

    // Only attempt token validation if there's a saved token, not on auth pages, no user is set,
    // and it's a different token than the one we last validated
    if (currentToken && !isAuthPage && !user && currentToken !== lastValidatedToken.current) {
      lastValidatedToken.current = currentToken; // Mark this token as being validated

      // Validate the token by fetching user info, but do it asynchronously to avoid blocking
      const timer = setTimeout(() => {
        validateAndSetUser(currentToken);
      }, 300); // Increased delay to ensure proper initialization

      return () => clearTimeout(timer);
    } else if (!currentToken && user) {
      // If there's no token but user is set, clear the user (happens on logout)
      storeLogout();
      lastValidatedToken.current = null; // Reset the validated token on logout
    }
  }, [storeToken, user, storeLogout]); // Depend on storeToken, user and storeLogout to re-run when they change

  const validateAndSetUser = async (token: string) => {
    try {
      // Use environment variable for auth service URL, fallback to localhost:8001
      const authServiceUrl = process.env.NEXT_PUBLIC_AUTH_URL || 'http://localhost:8001';
      const response = await fetch(`${authServiceUrl}/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const userData = await response.json();
        // Update user in store - make sure token is also stored in localStorage again to ensure persistence
        localStorage.setItem('auth_token', token);
        storeLogin(token, userData);
      } else if (response.status === 401) {
        // Token is invalid, remove it from localStorage
        localStorage.removeItem('auth_token');
        storeLogout();
      } else {
        // For other errors (500, 404, etc.), don't logout immediately
        console.warn(`Auth validation failed with status ${response.status}`);
      }
    } catch (error: any) {
      console.error('Token validation failed:', error);
      // Only remove token if it's a 401 (unauthorized) error, not for network errors
      if (error.message && (error.message.includes('401') || error.message.includes('UNAUTHORIZED'))) {
        // Token is invalid/expired, remove it from localStorage
        localStorage.removeItem('auth_token');
        storeLogout();
      } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
        // Network error - auth service might be down
        // Don't remove the token in this case, just warn
        console.warn('Auth service unavailable, will retry on next interaction');
      } else {
        // For other errors, check if it's a network issue vs a token issue
        // If the error indicates the token is invalid, remove it
        // Otherwise, keep the token and just warn
        if (error.message && (error.message.includes('expired') || error.message.toLowerCase().includes('invalid') || error.message.includes('malformed'))) {
          // Token is invalid/expired, remove it from localStorage
          localStorage.removeItem('auth_token');
          storeLogout();
        } else {
          // Network or other error - don't remove the token to prevent auto-logout
          console.warn('Auth validation error (network issue, keeping token)', error);
        }
      }
    }
  };

  const fetchUserInfoFromToken = async (token: string) => {
    try {
      // Use environment variable for auth service URL, fallback to localhost:8001
      const authServiceUrl = process.env.NEXT_PUBLIC_AUTH_URL || 'http://localhost:8001';
      const response = await fetch(`${authServiceUrl}/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const userData = await response.json();
        // Update user in store
        storeLogin(token, userData);
      } else {
        // Token is invalid, remove it from localStorage
        localStorage.removeItem('auth_token');
        storeLogout();
      }
    } catch (error: any) {
      console.error('Failed to fetch user info:', error);
      // Only remove token if it's a 401 (unauthorized) error, not for network errors
      if (error.message && (error.message.includes('401') || error.message.includes('UNAUTHORIZED'))) {
        // Token is invalid/expired, remove it from localStorage
        localStorage.removeItem('auth_token');
        storeLogout();
      } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
        // Network error - auth service might be down
        // Don't remove the token in this case, just warn
        console.warn('Auth service unavailable during user info fetch');
      } else {
        // For other errors, check if it's a network issue vs a token issue
        // If the error indicates the token is invalid, remove it
        // Otherwise, keep the token and just warn
        if (error.message && (error.message.includes('expired') || error.message.toLowerCase().includes('invalid') || error.message.includes('malformed'))) {
          // Token is invalid/expired, remove it from localStorage
          localStorage.removeItem('auth_token');
          storeLogout();
        } else {
          // Network or other error - don't remove the token to prevent auto-logout
          console.warn('User info fetch error (network issue, keeping token)', error);
        }
      }
    }
  };

  const login = async (email: string, password: string) => {
    try {
      // Use environment variable for auth service URL, fallback to localhost:8001
      const authServiceUrl = process.env.NEXT_PUBLIC_AUTH_URL || 'http://localhost:8001';
      const response = await fetch(`${authServiceUrl}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        let errorData;
        try {
          errorData = await response.json();
        } catch (e) {
          throw new Error(`Login failed with status ${response.status}`);
        }

        // Handle different error response formats
        if (typeof errorData === 'string') {
          throw new Error(errorData);
        } else if (Array.isArray(errorData) && errorData.length > 0) {
          const firstError = errorData[0];
          if (firstError && typeof firstError.msg === 'string') {
            throw new Error(firstError.msg);
          }
        } else if (typeof errorData === 'object') {
          if (errorData.detail && typeof errorData.detail === 'string') {
            throw new Error(errorData.detail);
          } else if (Array.isArray(errorData.detail) && errorData.detail.length > 0) {
            const firstDetail = errorData.detail[0];
            if (firstDetail && typeof firstDetail.msg === 'string') {
              throw new Error(firstDetail.msg);
            }
          } else if (errorData.error && typeof errorData.error === 'string') {
            throw new Error(errorData.error);
          } else if (errorData.message && typeof errorData.message === 'string') {
            throw new Error(errorData.message);
          } else {
            const errorStr = JSON.stringify(errorData);
            throw new Error(`Login failed: ${errorStr}`);
          }
        }
        throw new Error('Login failed with validation error');
      }

      const data = await response.json();
      if (data.access_token) {
        storeLogin(data.access_token, data.user);
        toast.success(`Welcome back, ${data.user.name.split(' ')[0]}!`, {
          description: 'You have successfully signed in.',
          duration: 3000,
        });
      }
    } catch (error: any) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const register = async (name: string, email: string, password: string) => {
    try {
      // Use environment variable for auth service URL, fallback to localhost:8001
      const authServiceUrl = process.env.NEXT_PUBLIC_AUTH_URL || 'http://localhost:8001';
      const response = await fetch(`${authServiceUrl}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, password }),
      });

      if (!response.ok) {
        let errorData;
        try {
          errorData = await response.json();
        } catch (e) {
          throw new Error(`Registration failed with status ${response.status}`);
        }

        if (typeof errorData === 'string') {
          throw new Error(errorData);
        } else if (Array.isArray(errorData) && errorData.length > 0) {
          const firstError = errorData[0];
          if (firstError && typeof firstError.msg === 'string') {
            throw new Error(firstError.msg);
          }
        } else if (typeof errorData === 'object') {
          if (errorData.detail && typeof errorData.detail === 'string') {
            throw new Error(errorData.detail);
          } else if (Array.isArray(errorData.detail) && errorData.detail.length > 0) {
            const firstDetail = errorData.detail[0];
            if (firstDetail && typeof firstDetail.msg === 'string') {
              throw new Error(firstDetail.msg);
            }
          } else if (errorData.error && typeof errorData.error === 'string') {
            throw new Error(errorData.error);
          } else if (errorData.message && typeof errorData.message === 'string') {
            throw new Error(errorData.message);
          } else {
            const errorStr = JSON.stringify(errorData);
            throw new Error(`Registration failed: ${errorStr}`);
          }
        }
        throw new Error('Registration failed with validation error');
      }

      const data = await response.json();
      if (data.access_token) {
        storeLogin(data.access_token, data.user);
        toast.success('Account created!', {
          description: 'Welcome to Tickwen.',
          duration: 3000,
        });
      }
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      // Call the store's logout function with full cleanup
      storeLogout(true);
      
      // Force redirection to home page
      router.push('/');
      
      toast.success('Signed out successfully', {
        duration: 2000,
      });
    } catch (error) {
      console.error('Logout error:', error);
      // Fallback cleanup if store logout fails
      localStorage.removeItem('auth_token');
      sessionStorage.clear();
      document.cookie.split(";").forEach(function(c) {
        document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
      });
      router.push('/');
    }
  };

  const isAuthenticated = !!storeToken;

  const value = {
    user,
    token: storeToken,
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
