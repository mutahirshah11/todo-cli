'use client';

import React, { useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useStore } from '@/lib/store';
import { TaskForm } from '@/components/feature/TaskForm';
import { Button } from '@/components/ui/button';
import { Spinner } from '@/components/ui/spinner';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default function EditTaskPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const { tasks, updateTask, fetchTasks, isLoading, isAuthenticated } = useStore();

  useEffect(() => {
    if (isAuthenticated()) {
      fetchTasks();
    }
  }, []);

  const task = tasks.find(t => t.id === id);

  const handleSubmit = async (data: { title: string; description?: string }) => {
    if (isAuthenticated() && id) {
      await updateTask(id, data);
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
            Please log in to edit a task.
          </p>
          <Link href="/login">
            <Button>Go to Login</Button>
          </Link>
        </div>
      </div>
    );
  }

  if (isLoading && !task) {
    return (
      <div className="container mx-auto py-10 flex justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!task) {
    return (
      <div className="container mx-auto py-10">
        <div className="max-w-md mx-auto text-center">
          <h1 className="text-2xl font-bold mb-4">Task Not Found</h1>
          <p className="text-muted-foreground mb-6">
            The task you{'\''}re looking for doesn{'\''}t exist or you don{'\''}t have permission to view it.
          </p>
          <Link href="/dashboard">
            <Button>Back to Dashboard</Button>
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
          defaultValues={{
            title: task.title,
            description: task.description || '',
          }}
          submitButtonText="Update Task"
        />
      </div>
    </div>
  );
}