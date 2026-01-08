import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { TaskItem } from '@/components/feature/TaskItem';

describe('TaskItem', () => {
  const mockTask = {
    id: '1',
    title: 'Test Task',
    description: 'Test Description',
    is_completed: false,
    created_at: '2026-01-01T00:00:00Z',
  };

  const mockOnToggle = jest.fn();
  const mockOnDelete = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders task details correctly', () => {
    render(<TaskItem task={mockTask} onToggle={mockOnToggle} onDelete={mockOnDelete} />);

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
  });

  it('calls onToggle when toggle button is clicked', () => {
    render(<TaskItem task={mockTask} onToggle={mockOnToggle} onDelete={mockOnDelete} />);

    const toggleButton = screen.getByRole('button', { name: /Mark as complete/i });
    fireEvent.click(toggleButton);

    expect(mockOnToggle).toHaveBeenCalledWith(mockTask.id);
  });

  it('calls onDelete when delete button is clicked', () => {
    render(<TaskItem task={mockTask} onToggle={mockOnToggle} onDelete={mockOnDelete} />);

    const deleteButton = screen.getByRole('button', { name: /delete/i });
    fireEvent.click(deleteButton);

    expect(mockOnDelete).toHaveBeenCalledWith(mockTask.id);
  });

  it('shows completed task with strikethrough', () => {
    const completedTask = { ...mockTask, is_completed: true };
    render(<TaskItem task={completedTask} onToggle={mockOnToggle} onDelete={mockOnDelete} />);

    const taskTitle = screen.getByText('Test Task');
    expect(taskTitle).toHaveClass('line-through');
  });
});