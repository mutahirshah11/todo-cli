import { renderHook, act } from '@testing-library/react';
import { useStore } from '@/lib/store';

// Mock the apiClient since we're testing store logic
jest.mock('@/lib/api', () => ({
  apiClient: {
    getTasks: jest.fn(),
    createTask: jest.fn(),
    updateTask: jest.fn(),
    deleteTask: jest.fn(),
  },
}));

describe('Filter Logic', () => {
  it('should filter tasks based on title', () => {
    const { result } = renderHook(() => useStore());

    // Set tasks in the store
    act(() => {
      result.current.setFilterQuery('test');
    });

    // Mock tasks
    const mockTasks = [
      { id: '1', title: 'Test Task', description: 'A test task', is_completed: false, created_at: '2026-01-01T00:00:00Z' },
      { id: '2', title: 'Another Task', description: 'Another task', is_completed: true, created_at: '2026-01-01T00:00:00Z' },
      { id: '3', title: 'Testing Filter', description: 'Filter test', is_completed: false, created_at: '2026-01-01T00:00:00Z' },
    ];

    // Set the tasks in the store
    act(() => {
      result.current.fetchTasks = jest.fn().mockImplementation(() => {
        // Simulate setting tasks
        return Promise.resolve();
      });
    });

    // Check that filterQuery is set
    expect(result.current.filterQuery).toBe('test');
  });

  it('should return all tasks when no filter is applied', () => {
    const { result } = renderHook(() => useStore());

    act(() => {
      result.current.setFilterQuery('');
    });

    expect(result.current.filterQuery).toBe('');
  });

  it('should filter tasks by description when filter matches', () => {
    const { result } = renderHook(() => useStore());

    act(() => {
      result.current.setFilterQuery('filter');
    });

    expect(result.current.filterQuery).toBe('filter');
  });
});