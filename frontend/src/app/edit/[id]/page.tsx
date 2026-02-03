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
  const params = useParams();
  const router = useRouter();
  const taskId = params.id as string;
  
  const { tasks, updateTask, isAuthenticated, isLoading } = useStore();
  const task = tasks.find(t => t.id === taskId);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  const handleSubmit = async (data: { title?: string; description?: string }) => {
    await updateTask(taskId, data);
    router.push('/dashboard');
    router.refresh();
  };

  if (!task) {
    return (
      <div className="container mx-auto py-10 text-center">
        <h1 className="text-2xl font-bold mb-4">Task Not Found</h1>
        <Link href="/dashboard">
          <Button variant="outline">Back to Dashboard</Button>
        </Link>
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
            is_completed: task.is_completed
          }}
          submitButtonText={isLoading ? "Updating..." : "Update Task"}
        />
      </div>
    </div>
  );
}
