'use client';

import { ThemeProvider } from '@/app/providers';
import { AuthProvider } from '@/app/providers/auth-provider';
import { Navbar } from '@/components/feature/Navbar';
import { Toaster } from 'sonner';

interface ThemeProviderWrapperProps {
  children: React.ReactNode;
}

export default function ThemeProviderWrapper({ children }: ThemeProviderWrapperProps) {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      <AuthProvider>
        <Navbar />
        <main>{children}</main>
        <Toaster />
      </AuthProvider>
    </ThemeProvider>
  );
}