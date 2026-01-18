import React from 'react';
import { TaskItem } from '@/components/feature/TaskItem';
import { Task } from '@/lib/types';
import { AnimatePresence, motion } from 'framer-motion';
import { Inbox } from 'lucide-react';

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
      <div className="flex flex-col items-center justify-center py-20 text-center opacity-50">
        <div className="h-16 w-16 rounded-full bg-white/5 flex items-center justify-center mb-4">
           <Inbox className="h-8 w-8 text-gray-500" />
        </div>
        <h3 className="text-lg font-medium text-gray-400">No tasks found</h3>
        <p className="text-sm text-gray-600 mt-1 max-w-xs">
          {filterQuery ? 'Try searching for something else.' : 'Your workspace is empty. Use the Command Orb to capture a task.'}
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3 pb-24"> {/* Added padding bottom for Orb clearance */}
      <AnimatePresence mode="popLayout">
        {filteredTasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onToggle={onToggle || (() => {})}
            onDelete={onDelete || (() => {})}
          />
        ))}
      </AnimatePresence>
    </div>
  );
};
