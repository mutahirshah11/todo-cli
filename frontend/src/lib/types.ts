// Data Model interfaces based on data-model.md
export interface User {
  id: string; // UUID
  name: string;
  email: string; // (Optional, if returned by backend)
}

export interface Task {
  id: string; // UUID
  title: string;
  description?: string | null; // Optional
  is_completed: boolean;
  created_at: string; // ISO 8601 Date String
  // updated_at: string; // (Optional)
}

// State Interfaces (Zustand)
export interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
  login: (token: string, user: User) => void;
  logout: (fullCleanup?: boolean) => void;
  initializeAuth: () => void;
  setTokenFromStorage: () => void;
}

export interface TaskState {
  tasks: Task[];
  isLoading: boolean;
  error: string | null;
  filterQuery: string;

  // Actions
  fetchTasks: () => Promise<void>;
  createTask: (data: CreateTaskPayload) => Promise<void>;
  updateTask: (id: string, data: UpdateTaskPayload) => Promise<void>;
  deleteTask: (id: string) => Promise<void>;
  toggleTask: (id: string) => Promise<void>;
  setFilterQuery: (query: string) => void;
}

// API Payloads
export interface CreateTaskPayload {
  title: string;
  description?: string;
}

export interface UpdateTaskPayload {
  title?: string;
  description?: string;
  is_completed?: boolean;
}