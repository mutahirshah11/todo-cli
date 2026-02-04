'use client';

import React from 'react';
import { AuthProvider } from '@/app/providers/auth-provider';
import { SplitAuthLayout } from '@/components/layout/SplitAuthLayout';

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AuthProvider>
      <SplitAuthLayout>
        {children}
      </SplitAuthLayout>
    </AuthProvider>
  );
}
