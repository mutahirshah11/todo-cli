// API Client wrapper for Tickwen backend
import { Task } from './types';

// The actual API base URL is defined in the request method
// const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api'; // Commenting out to avoid confusion

interface ApiOptions {
  token?: string;
  userId?: string;
}

class ApiClient {
  async request<T>(endpoint: string, options: RequestInit = {}, apiOptions?: ApiOptions): Promise<T> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(apiOptions?.token && { 'Authorization': `Bearer ${apiOptions.token}` }),
      ...options.headers,
    };

    // Use the correct API path format that matches the backend: /api/v1/{endpoint}
    // The user_id is now extracted from the JWT token, not from the URL path
    // Check if NEXT_PUBLIC_API_URL already includes the /api/v1 part
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    // Remove trailing slash if present
    const cleanBaseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
    
    // Construct URL: Check if base url already has /api/v1
    const url = cleanBaseUrl.includes('/api/v1')
      ? `${cleanBaseUrl}/${endpoint}`
      : `${cleanBaseUrl}/api/v1/${endpoint}`;

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        let errorData;
        try {
          errorData = await response.json();
        } catch (e) {
          // If response is not JSON, create a generic error
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Handle different error response formats
        if (typeof errorData === 'string') {
          throw new Error(errorData);
        } else if (Array.isArray(errorData) && errorData.length > 0) {
          // Pydantic validation error format: [{loc: [], msg: "", type: ""}]
          const firstError = errorData[0];
          if (firstError && typeof firstError.msg === 'string') {
            throw new Error(firstError.msg);
          }
        } else if (typeof errorData === 'object') {
          // Check for various possible error message fields
          if (errorData.detail && typeof errorData.detail === 'string') {
            // Special handling for 401 Unauthorized
            if (response.status === 401) {
              throw new Error('UNAUTHORIZED:' + errorData.detail);
            }
            throw new Error(errorData.detail);
          } else if (Array.isArray(errorData.detail) && errorData.detail.length > 0) {
            const firstDetail = errorData.detail[0];
            if (firstDetail && typeof firstDetail.msg === 'string') {
              if (response.status === 401) {
                throw new Error('UNAUTHORIZED:' + firstDetail.msg);
              }
              throw new Error(firstDetail.msg);
            }
          } else if (errorData.error && typeof errorData.error === 'string') {
            if (response.status === 401) {
              throw new Error('UNAUTHORIZED:' + errorData.error);
            }
            throw new Error(errorData.error);
          } else if (errorData.message && typeof errorData.message === 'string') {
            if (response.status === 401) {
              throw new Error('UNAUTHORIZED:' + errorData.message);
            }
            throw new Error(errorData.message);
          } else {
            // If none of the common fields exist, try to create a meaningful error
            const errorStr = JSON.stringify(errorData);
            if (response.status === 401) {
              throw new Error('UNAUTHORIZED:Token expired or invalid');
            }
            throw new Error(`API error: ${errorStr}`);
          }
        }

        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Handle 204 No Content responses
      if (response.status === 204) {
        return undefined as T;
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Specific API methods based on contracts/api.md
  async getTasks(userId: string, token: string): Promise<Task[]> {
    const response = await this.request<{tasks: Task[]}>(`tasks`, { method: 'GET' }, { token });
    // Map backend response to frontend format
    return response.tasks.map(task => this.mapBackendTaskToFrontend(task));
  }

  async getTask(userId: string, taskId: string, token: string): Promise<Task> {
    const response = await this.request<{task: Task}>(`tasks/${taskId}`, { method: 'GET' }, { token });
    // Map backend response to frontend format
    return this.mapBackendTaskToFrontend(response.task);
  }

  async createTask(userId: string, taskData: { title: string; description?: string }, token: string): Promise<Task> {
    // Map frontend format to backend format (include completed field)
    const backendTaskData = {
      title: taskData.title,
      description: taskData.description || "",
      completed: false  // Default to false as per backend model
    };
    const response = await this.request<{task: Task}>(`tasks`, { method: 'POST', body: JSON.stringify(backendTaskData) }, { token });
    // Map backend response to frontend format
    return this.mapBackendTaskToFrontend(response.task);
  }

  async updateTask(userId: string, taskId: string, taskData: { title?: string; description?: string; is_completed?: boolean }, token: string): Promise<Task> {
    // Map frontend format to backend format
    const backendTaskData = {
      title: taskData.title,
      description: taskData.description,
      completed: taskData.is_completed
    };
    const response = await this.request<{task: Task}>(`tasks/${taskId}`, { method: 'PUT', body: JSON.stringify(backendTaskData) }, { token });
    // Map backend response to frontend format
    return this.mapBackendTaskToFrontend(response.task);
  }

  async toggleTask(userId: string, taskId: string, token: string): Promise<Task> {
    // For toggle, we need to get the current task first to know its completion status
    // Get the current task to determine the new completion status
    const currentTask = await this.getTask(userId, taskId, token);
    const response = await this.request<{task: Task}>(`tasks/${taskId}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({completed: !currentTask.is_completed})
    }, { token });

    // Map backend response to frontend format
    return this.mapBackendTaskToFrontend(response.task);
  }

  async deleteTask(userId: string, taskId: string, token: string): Promise<void> {
    return this.request<void>(`tasks/${taskId}`, { method: 'DELETE' }, { token });
  }


  // Helper method to map backend task format to frontend format
  private mapBackendTaskToFrontend(backendTask: any): Task {
    return {
      id: backendTask.id.toString(), // Convert to string as frontend expects
      title: backendTask.title,
      description: backendTask.description || null,
      is_completed: backendTask.completed, // Map 'completed' to 'is_completed'
      created_at: backendTask.created_at
    };
  }
}

export const apiClient = new ApiClient();