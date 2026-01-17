'use client';

import React, { useEffect, useState } from 'react';
import { useStore } from '@/lib/store';
import { TaskList } from '@/components/feature/TaskList';
import { DeleteConfirmationModal } from '@/components/feature/DeleteConfirmationModal';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Plus, Loader2 } from 'lucide-react';
import Link from 'next/link';

export default function DashboardPage() {
  const {
    tasks,
    isLoading,
    error,
    filterQuery,
    setFilterQuery,
    fetchTasks,
    toggleTask,
    deleteTask,
    isAuthenticated,
    user
  } = useStore();
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    if (isAuthenticated()) {
      fetchTasks();
    }
  }, []);

  const handleDeleteClick = (taskId: string, taskTitle: string) => {
    setSelectedTaskId(taskId);
    setIsModalOpen(true);
  };

  const handleConfirmDelete = () => {
    if (selectedTaskId) {
      deleteTask(selectedTaskId);
      setIsModalOpen(false);
      setSelectedTaskId(null);
    }
  };

  if (!isAuthenticated()) {
    return (
      <div className="container mx-auto py-10">
        <div className="max-w-md mx-auto text-center">
          <h1 className="text-2xl font-bold mb-4">Access Denied</h1>
          <p className="text-muted-foreground mb-6">
            Please log in to view your tasks.
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
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">Welcome back, {user?.name}!</p>
        </div>
        <Link href="/create">
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Create Task
          </Button>
        </Link>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-destructive/10 border border-destructive rounded-md text-destructive">
          {error}
        </div>
      )}

      <div className="mb-6">
        <Input
          placeholder="Search tasks..."
          value={filterQuery}
          onChange={(e) => setFilterQuery(e.target.value)}
          className="max-w-md"
        />
      </div>

      {isLoading ? (
        <div className="flex justify-center items-center py-10">
          <Loader2 className="h-8 w-8 animate-spin" />
        </div>
      ) : (
        <TaskList
          tasks={tasks}
          filterQuery={filterQuery}
          onToggle={toggleTask}
          onDelete={(id) => {
            const task = tasks.find(t => t.id === id);
            handleDeleteClick(id, task?.title || '');
          }}
        />
      )}

      <DeleteConfirmationModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onConfirm={handleConfirmDelete}
        taskTitle={tasks.find(t => t.id === selectedTaskId)?.title}
      />
    </div>
  );
}