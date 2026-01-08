import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Trash2, Square, CheckSquare } from 'lucide-react';
import { Task } from '@/lib/types';
import { cn } from '@/lib/utils';

interface TaskItemProps {
  task: Task;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

export const TaskItem: React.FC<TaskItemProps> = ({ task, onToggle, onDelete }) => {
  return (
    <Card className="transition-all duration-200 hover:shadow-md">
      <CardContent className="p-4 flex items-start gap-3">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => onToggle(task.id)}
          className="h-8 w-8 mt-1 p-0"
          aria-label={task.is_completed ? 'Mark as incomplete' : 'Mark as complete'}
        >
          {task.is_completed ? (
            <CheckSquare className="h-4 w-4 text-green-500" />
          ) : (
            <Square className="h-4 w-4" />
          )}
        </Button>

        <div className="flex-1 min-w-0">
          <h3 className={cn(
            'text-lg font-medium truncate',
            task.is_completed && 'line-through text-muted-foreground'
          )}>
            {task.title}
          </h3>
          {task.description && (
            <p className={cn(
              'text-sm text-muted-foreground mt-1',
              task.is_completed && 'line-through'
            )}>
              {task.description}
            </p>
          )}
          <p className="text-xs text-muted-foreground mt-2">
            {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>

        <Button
          variant="destructive"
          size="icon"
          onClick={() => onDelete(task.id)}
          className="h-8 w-8"
          aria-label="Delete task"
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </CardContent>
    </Card>
  );
};