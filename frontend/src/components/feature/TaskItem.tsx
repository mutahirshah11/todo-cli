'use client';

import React, { useRef, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Trash2, Square, CheckSquare, Calendar, Tag } from 'lucide-react';
import { Task } from '@/lib/types';
import { cn } from '@/lib/utils';
import { motion, useMotionTemplate, useMotionValue } from 'framer-motion';

interface TaskItemProps {
  task: Task;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

export const TaskItem: React.FC<TaskItemProps> = ({ task, onToggle, onDelete }) => {
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  function handleMouseMove({ currentTarget, clientX, clientY }: React.MouseEvent) {
    const { left, top } = currentTarget.getBoundingClientRect();
    mouseX.set(clientX - left);
    mouseY.set(clientY - top);
  }

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9, filter: "blur(10px)" }}
      whileHover={{ scale: 1.02, zIndex: 10 }}
      transition={{ type: "spring", stiffness: 500, damping: 30 }}
      className="group relative rounded-xl border border-white/10 bg-[#0f172a] px-4 py-4 shadow-sm transition-colors hover:border-primary/30"
      onMouseMove={handleMouseMove}
    >
      {/* Flashlight Effect */}
      <motion.div
        className="pointer-events-none absolute -inset-px rounded-xl opacity-0 transition duration-300 group-hover:opacity-100"
        style={{
          background: useMotionTemplate`
            radial-gradient(
              650px circle at ${mouseX}px ${mouseY}px,
              rgba(52, 211, 153, 0.15),
              transparent 80%
            )
          `,
        }}
      />

      <div className="relative flex items-start gap-4 z-10">
        <button
          onClick={() => onToggle(task.id)}
          className={cn(
            "mt-1 flex h-5 w-5 shrink-0 items-center justify-center rounded border transition-all hover:scale-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2",
            task.is_completed
              ? "bg-primary border-primary text-black"
              : "border-gray-500 hover:border-primary bg-transparent text-transparent"
          )}
        >
          <CheckSquare className={cn("h-3.5 w-3.5", !task.is_completed && "hidden")} />
        </button>

        <div className="flex-1 min-w-0">
          <h3 className={cn(
            'text-base font-medium transition-all',
            task.is_completed ? 'text-gray-500 line-through decoration-gray-600' : 'text-gray-100'
          )}>
            {task.title}
          </h3>
          
          {task.description && (
            <p className={cn(
              'text-sm mt-1 transition-all',
              task.is_completed ? 'text-gray-600 line-through' : 'text-gray-400'
            )}>
              {task.description}
            </p>
          )}

          <div className="mt-3 flex items-center gap-3 opacity-60 group-hover:opacity-100 transition-opacity">
            <span className="flex items-center text-xs text-gray-500 bg-white/5 px-2 py-0.5 rounded-md border border-white/5">
               <Calendar className="mr-1 h-3 w-3" />
               {new Date(task.created_at).toLocaleDateString()}
            </span>
             {/* Simulated Tags for Visuals */}
            <span className="flex items-center text-xs text-blue-400/80 bg-blue-500/10 px-2 py-0.5 rounded-md border border-blue-500/10">
               <Tag className="mr-1 h-3 w-3" />
               Work
            </span>
          </div>
        </div>

        <Button
          variant="ghost"
          size="icon"
          onClick={() => onDelete(task.id)}
          className="h-8 w-8 opacity-0 group-hover:opacity-100 transition-opacity text-red-400 hover:text-red-300 hover:bg-red-400/10"
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>
    </motion.div>
  );
};
