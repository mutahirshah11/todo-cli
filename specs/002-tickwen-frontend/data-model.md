# Data Model: Tickwen Frontend

**Feature**: 002-tickwen-frontend

This document defines the TypeScript interfaces and types used within the frontend application. These types mirror the backend entities but are tailored for client-side consumption.

## Entities

### User
Represents the currently authenticated user.

```typescript
interface User {
  id: string; // UUID
  username: string;
  // email: string; // (Optional, if returned by backend)
}
```

### Task
Represents a todo item.

```typescript
interface Task {
  id: string; // UUID
  title: string;
  description?: string | null; // Optional
  is_completed: boolean;
  created_at: string; // ISO 8601 Date String
  // updated_at: string; // (Optional)
}
```

## State Interfaces (Zustand)

### AuthState
Manages authentication status.

```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
  login: (token: string, user: User) => void;
  logout: () => void;
}
```

### TaskState
Manages the list of tasks and client-side filtering.

```typescript
interface TaskState {
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
```

## API Payloads

### CreateTaskPayload
```typescript
interface CreateTaskPayload {
  title: string;
  description?: string;
}
```

### UpdateTaskPayload
```typescript
interface UpdateTaskPayload {
  title?: string;
  description?: string;
  is_completed?: boolean;
}
```

## Validation Schemas (Zod)

### TaskSchema
Used for form validation.

```typescript
import { z } from 'zod';

export const taskSchema = z.object({
  title: z.string().min(1, "Title is required").max(100, "Title must be 100 characters or less"),
  description: z.string().max(500, "Description must be 500 characters or less").optional(),
  is_completed: z.boolean().optional(),
});

export type TaskFormValues = z.infer<typeof taskSchema>;
```
