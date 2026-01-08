import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { TaskForm } from '@/components/feature/TaskForm';

describe('TaskForm', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders form fields correctly', () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    expect(screen.getByLabelText(/title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
  });

  it('shows validation error for empty title', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const submitButton = screen.getByRole('button', { name: /submit/i });
    fireEvent.click(submitButton);

    expect(await screen.findByText(/title is required/i)).toBeInTheDocument();
  });

  it('shows validation error for title exceeding 100 characters', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/title/i);
    fireEvent.change(titleInput, {
      target: { value: 'a'.repeat(101) }
    });

    const submitButton = screen.getByRole('button', { name: /submit/i });
    fireEvent.click(submitButton);

    expect(await screen.findByText(/title must be 100 characters or less/i)).toBeInTheDocument();
  });

  it('shows validation error for description exceeding 500 characters', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const descriptionInput = screen.getByLabelText(/description/i);
    fireEvent.change(descriptionInput, {
      target: { value: 'a'.repeat(501) }
    });

    const titleInput = screen.getByLabelText(/title/i);
    fireEvent.change(titleInput, { target: { value: 'Valid Title' } });

    const submitButton = screen.getByRole('button', { name: /submit/i });
    fireEvent.click(submitButton);

    expect(await screen.findByText(/description must be 500 characters or less/i)).toBeInTheDocument();
  });

  it('calls onSubmit with valid data', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/title/i);
    fireEvent.change(titleInput, { target: { value: 'Test Title' } });

    const descriptionInput = screen.getByLabelText(/description/i);
    fireEvent.change(descriptionInput, { target: { value: 'Test Description' } });

    const submitButton = screen.getByRole('button', { name: /submit/i });
    fireEvent.click(submitButton);

    // Wait for form submission to complete
    await new Promise(resolve => setTimeout(resolve, 0));

    expect(mockOnSubmit).toHaveBeenCalledWith({
      title: 'Test Title',
      description: 'Test Description',
      is_completed: false
    });
  });
});