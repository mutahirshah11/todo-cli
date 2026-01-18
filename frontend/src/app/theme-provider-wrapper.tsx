'use client';

import { ThemeProvider } from '@/app/providers';
import { AuthProvider } from '@/app/providers/auth-provider';
import { Toaster } from 'sonner';

interface ThemeProviderWrapperProps {
  children: React.ReactNode;
}

export default function ThemeProviderWrapper({ children }: ThemeProviderWrapperProps) {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="dark"
      forcedTheme="dark"
      enableSystem={false}
      disableTransitionOnChange
    >
      <AuthProvider>
        <main className="min-h-screen bg-background">{children}</main>
        <Toaster theme="dark" position="top-center" richColors />
      </AuthProvider>
    </ThemeProvider>
  );
}
