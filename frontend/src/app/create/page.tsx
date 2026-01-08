'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { useStore } from '@/lib/store';
import { TaskForm } from '@/components/feature/TaskForm';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default function CreateTaskPage() {
  const router = useRouter();
  const { createTask, isAuthenticated, isLoading } = useStore();

  const handleSubmit = async (data: { title: string; description?: string }) => {
    if (isAuthenticated()) {
      await createTask(data);
      router.push('/dashboard');
      router.refresh(); // Refresh to update the UI
    }
  };

  if (!isAuthenticated()) {
    return (
      <div className="container mx-auto py-10">
        <div className="max-w-md mx-auto text-center">
          <h1 className="text-2xl font-bold mb-4">Access Denied</h1>
          <p className="text-muted-foreground mb-6">
            Please log in to create a task.
          </p>
          <Link href="/login">
            <Button>Go to Login</Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-6">
      <div className="flex items-center gap-2 mb-6">
        <Link href="/dashboard">
          <Button variant="outline" size="sm">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
        </Link>
      </div>

      <div className="max-w-2xl mx-auto">
        <TaskForm
          onSubmit={handleSubmit}
          submitButtonText={isLoading ? "Creating..." : "Create Task"}
        />
      </div>
    </div>
  );
}