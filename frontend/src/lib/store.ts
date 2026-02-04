import { create } from 'zustand';
import { toast } from 'sonner';
import { AuthState, TaskState, User, Task, CreateTaskPayload, UpdateTaskPayload } from './types';
import { apiClient } from './api';

// Combine AuthState and TaskState into a single store
export interface StoreState extends AuthState, TaskState {
  // Additional helper methods if needed
  isAuthenticated: () => boolean;
}

export const useStore = create<StoreState>((set, get) => ({
  // Auth State
  user: null,
  token: null,
  isLoading: false,
  error: null,

  // Task State
  tasks: [],
  filterQuery: '',

  // Auth Actions
  login: (token: string, user: User) => {
    // Store token in localStorage for persistence
    localStorage.setItem('auth_token', token);
    set({ token, user, error: null });
  },
  initializeAuth: () => {
    // Initialize auth state from localStorage if available
    if (typeof window !== 'undefined') {
      const storedToken = localStorage.getItem('auth_token');
      if (storedToken) {
        // We have a token, but we need to validate it by fetching user info
        // Since we can't call external APIs from here, we'll just set the token
        // The actual user validation will happen in the AuthProvider
        set({ token: storedToken });
      }
    }
  },
  setTokenFromStorage: () => {
    // Set token from localStorage if store doesn't have one
    const storedToken = localStorage.getItem('auth_token');
    if (storedToken && !get().token) {
      set({ token: storedToken });
    }
  },
  logout: (fullCleanup?: boolean) => {
    if (fullCleanup) {
      // Clear localStorage and other storage for complete logout
      localStorage.removeItem('auth_token');
      sessionStorage.clear();
      document.cookie.split(";").forEach(function(c) {
        document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
      });
    }
    set({ token: null, user: null, tasks: [] });
  },

  // Task Actions
  fetchTasks: async () => {
    const { token, user } = get();
    if (!token || !user) return;

    set({ isLoading: true });
    try {
      const tasks: Task[] = await apiClient.getTasks(user.id, token);
      // Remove any duplicate tasks by ID to ensure uniqueness
      const uniqueTasks = tasks.filter((task, index, self) =>
        index === self.findIndex(t => t.id === task.id)
      );
      set({ tasks: uniqueTasks, isLoading: false });
    } catch (error) {
      let errorMessage = 'Unknown error';
      if (error instanceof Error) {
        errorMessage = error.message;
      } else if (typeof error === 'string') {
        errorMessage = error;
      } else {
        errorMessage = JSON.stringify(error);
      }

      // Check if it's an unauthorized error
      if (errorMessage.includes('UNAUTHORIZED:')) {
        // Automatically logout user
        get().logout(true);
        toast.error('Session expired. Please login again.');
      } else {
        toast.error(`Failed to fetch tasks: ${errorMessage}`);
      }
      set({ isLoading: false });
    }
  },

  createTask: async (data: CreateTaskPayload) => {
    const { token, user } = get();
    if (!token || !user) return;

    set({ isLoading: true });
    try {
      const newTask: Task = await apiClient.createTask(user.id, data, token);
      set((state) => ({ tasks: [...state.tasks, newTask], isLoading: false }));
      toast.success('Task created successfully!');
    } catch (error) {
      let errorMessage = 'Unknown error';
      if (error instanceof Error) {
        errorMessage = error.message;
      } else if (typeof error === 'string') {
        errorMessage = error;
      } else {
        errorMessage = JSON.stringify(error);
      }

      // Check if it's an unauthorized error
      if (errorMessage.includes('UNAUTHORIZED:')) {
        // Automatically logout user
        get().logout(true);
        toast.error('Session expired. Please login again.');
      } else {
        toast.error(`Failed to create task: ${errorMessage}`);
      }
      set({ isLoading: false });
    }
  },

  updateTask: async (id: string, data: UpdateTaskPayload) => {
    const { token, user } = get();
    if (!token || !user) return;

    set({ isLoading: true });
    try {
      const updatedTask: Task = await apiClient.updateTask(user.id, id, data, token);
      set((state) => ({
        tasks: state.tasks.map(task => task.id === id ? updatedTask : task),
        isLoading: false
      }));
      toast.success('Task updated successfully!');
    } catch (error) {
      let errorMessage = 'Unknown error';
      if (error instanceof Error) {
        errorMessage = error.message;
      } else if (typeof error === 'string') {
        errorMessage = error;
      } else {
        errorMessage = JSON.stringify(error);
      }

      // Check if it's an unauthorized error
      if (errorMessage.includes('UNAUTHORIZED:')) {
        // Automatically logout user
        get().logout(true);
        toast.error('Session expired. Please login again.');
      } else {
        toast.error(`Failed to update task: ${errorMessage}`);
      }
      set({ isLoading: false });
    }
  },

  deleteTask: async (id: string) => {
    const { token, user } = get();
    if (!token || !user) return;

    set({ isLoading: true });
    try {
      await apiClient.deleteTask(user.id, id, token);
      set((state) => ({
        tasks: state.tasks.filter(task => task.id !== id),
        isLoading: false
      }));
      toast.success('Task deleted successfully!');
    } catch (error) {
      let errorMessage = 'Unknown error';
      if (error instanceof Error) {
        errorMessage = error.message;
      } else if (typeof error === 'string') {
        errorMessage = error;
      } else {
        errorMessage = JSON.stringify(error);
      }

      // Check if it's an unauthorized error
      if (errorMessage.includes('UNAUTHORIZED:')) {
        // Automatically logout user
        get().logout(true);
        toast.error('Session expired. Please login again.');
      } else {
        toast.error(`Failed to delete task: ${errorMessage}`);
      }
      set({ isLoading: false });
    }
  },

  toggleTask: async (id: string) => {
    const { token, user } = get();
    if (!token || !user) return;

    set({ isLoading: true });
    try {
      // Use the dedicated toggleTask API method instead of updateTask
      const updatedTask: Task = await apiClient.toggleTask(user.id, id, token);

      set((state) => ({
        tasks: state.tasks.map(task =>
          task.id === id ? updatedTask : task
        ),
        isLoading: false
      }));

      // Determine the status message based on the updated task
      const isCompleted = updatedTask.is_completed;
      toast.success(isCompleted ? 'Task marked as complete' : 'Task marked as incomplete');
    } catch (error) {
      let errorMessage = 'Unknown error';
      if (error instanceof Error) {
        errorMessage = error.message;
      } else if (typeof error === 'string') {
        errorMessage = error;
      } else {
        errorMessage = JSON.stringify(error);
      }

      // Check if it's an unauthorized error
      if (errorMessage.includes('UNAUTHORIZED:')) {
        // Automatically logout user
        get().logout(true);
        toast.error('Session expired. Please login again.');
      } else {
        toast.error(`Failed to update task: ${errorMessage}`);
      }
      set({ isLoading: false });
    }
  },

  setFilterQuery: (query: string) => set({ filterQuery: query }),

  // Helper methods
  isAuthenticated: () => {
    const { token } = get();
    return !!token;
  }
}));