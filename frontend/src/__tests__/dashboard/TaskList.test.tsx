import React from 'react';
import { render, screen } from '@testing-library/react';
import { TaskList } from '@/components/feature/TaskList';
import { Task } from '@/lib/types';

// Mock the TaskItem component
jest.mock('@/components/feature/TaskItem', () => ({
  TaskItem: ({ task }: { task: Task }) => <div data-testid={`task-${task.id}`}>{task.title}</div>,
}));

describe('TaskList', () => {
  const mockTasks = [
    { id: '1', title: 'Test Task 1', is_completed: false, created_at: '2026-01-01T00:00:00Z' },
    { id: '2', title: 'Test Task 2', is_completed: true, created_at: '2026-01-01T00:00:00Z' },
  ];

  it('renders tasks when tasks array is provided', () => {
    render(<TaskList tasks={mockTasks} />);

    expect(screen.getByTestId('task-1')).toBeInTheDocument();
    expect(screen.getByTestId('task-2')).toBeInTheDocument();
  });

  it('renders empty state when no tasks are provided', () => {
    render(<TaskList tasks={[]} />);

    expect(screen.getByText('No tasks found')).toBeInTheDocument();
  });

  it('applies filter when filterQuery is provided', () => {
    render(<TaskList tasks={mockTasks} filterQuery="Task 1" />);

    expect(screen.getByTestId('task-1')).toBeInTheDocument();
    expect(screen.queryByTestId('task-2')).not.toBeInTheDocument();
  });
});
