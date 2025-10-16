/**
 * Type definitions for the application
 */

export interface Task {
  id: number;
  title: string;
  description: string | null;
  created_at: string;
  updated_at: string;
  comments_count: number;
}

export interface Comment {
  id: number;
  task_id: number;
  content: string;
  author: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskDTO {
  title: string;
  description?: string;
}

export interface UpdateTaskDTO {
  title?: string;
  description?: string;
}

export interface CreateCommentDTO {
  task_id: number;
  content: string;
  author: string;
}

export interface UpdateCommentDTO {
  content?: string;
  author?: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  count?: number;
}

export interface ApiError {
  error: string;
  messages?: Record<string, string[]>;
  message?: string;
}
