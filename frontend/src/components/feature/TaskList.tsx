import React from 'react';
import { TaskItem } from '@/components/feature/TaskItem';
import { Task } from '@/lib/types';

interface TaskListProps {
  tasks: Task[];
  filterQuery?: string;
  onToggle?: (id: string) => void;
  onDelete?: (id: string) => void;
}

export const TaskList: React.FC<TaskListProps> = ({
  tasks,
  filterQuery = '',
  onToggle,
  onDelete
}) => {
  // Filter tasks based on the filterQuery
  const filteredTasks = tasks.filter(task =>
    task.title.toLowerCase().includes(filterQuery.toLowerCase()) ||
    (task.description && task.description.toLowerCase().includes(filterQuery.toLowerCase()))
  );

  if (filteredTasks.length === 0) {
    return (
      <div className="text-center py-10">
        <h3 className="text-lg font-medium">No tasks found</h3>
        <p className="text-muted-foreground mt-1">
          {filterQuery ? 'Try a different search' : 'Create your first task to get started'}
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {filteredTasks.map((task, index) => (
        <TaskItem
          key={`${task.id}-${index}`}
          task={task}
          onToggle={onToggle || (() => {})}
          onDelete={onDelete || (() => {})}
        />
      ))}
    </div>
  );
};