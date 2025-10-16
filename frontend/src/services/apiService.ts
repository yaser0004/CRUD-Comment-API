/**
 * Centralized API Service
 * Handles all HTTP requests to the Flask backend
 */
import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from 'axios';
import { API_BASE_URL } from '../utils/constants';
import {
  Task,
  Comment,
  CreateTaskDTO,
  UpdateTaskDTO,
  CreateCommentDTO,
  UpdateCommentDTO,
  ApiResponse,
  ApiError,
} from '../types';

class ApiService {
  private axiosInstance: AxiosInstance;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 10000,
    });

    this.setupInterceptors();
  }

  /**
   * Setup request and response interceptors
   */
  private setupInterceptors(): void {
    // Request interceptor
    this.axiosInstance.interceptors.request.use(
      (config) => {
        // Add any auth tokens or custom headers here
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.axiosInstance.interceptors.response.use(
      (response) => response,
      (error: AxiosError<ApiError>) => {
        // Centralized error handling
        if (error.response) {
          // Server responded with error status
          console.error('API Error:', error.response.data);
        } else if (error.request) {
          // Request made but no response
          console.error('Network Error:', error.request);
        } else {
          // Something else happened
          console.error('Error:', error.message);
        }
        return Promise.reject(error);
      }
    );
  }

  /**
   * Generic request method
   */
  private async request<T>(config: AxiosRequestConfig): Promise<T> {
    const response = await this.axiosInstance.request<T>(config);
    return response.data;
  }

  // ========== Task API Methods ==========

  /**
   * Get all tasks
   */
  async getTasks(): Promise<Task[]> {
    const response = await this.request<ApiResponse<Task[]>>({
      method: 'GET',
      url: '/tasks',
    });
    return response.data;
  }

  /**
   * Get a single task by ID
   */
  async getTaskById(id: number): Promise<Task> {
    const response = await this.request<ApiResponse<Task>>({
      method: 'GET',
      url: `/tasks/${id}`,
    });
    return response.data;
  }

  /**
   * Create a new task
   */
  async createTask(data: CreateTaskDTO): Promise<Task> {
    const response = await this.request<ApiResponse<Task>>({
      method: 'POST',
      url: '/tasks',
      data,
    });
    return response.data;
  }

  /**
   * Update an existing task
   */
  async updateTask(id: number, data: UpdateTaskDTO): Promise<Task> {
    const response = await this.request<ApiResponse<Task>>({
      method: 'PUT',
      url: `/tasks/${id}`,
      data,
    });
    return response.data;
  }

  /**
   * Delete a task
   */
  async deleteTask(id: number): Promise<void> {
    await this.request<{ message: string }>({
      method: 'DELETE',
      url: `/tasks/${id}`,
    });
  }

  // ========== Comment API Methods ==========

  /**
   * Get all comments
   */
  async getAllComments(): Promise<Comment[]> {
    const response = await this.request<ApiResponse<Comment[]>>({
      method: 'GET',
      url: '/comments',
    });
    return response.data;
  }

  /**
   * Get comments for a specific task
   */
  async getCommentsByTask(taskId: number): Promise<Comment[]> {
    const response = await this.request<ApiResponse<Comment[]>>({
      method: 'GET',
      url: `/comments/task/${taskId}`,
    });
    return response.data;
  }

  /**
   * Get a single comment by ID
   */
  async getCommentById(id: number): Promise<Comment> {
    const response = await this.request<ApiResponse<Comment>>({
      method: 'GET',
      url: `/comments/${id}`,
    });
    return response.data;
  }

  /**
   * Create a new comment
   */
  async createComment(data: CreateCommentDTO): Promise<Comment> {
    const response = await this.request<ApiResponse<Comment>>({
      method: 'POST',
      url: '/comments',
      data,
    });
    return response.data;
  }

  /**
   * Update an existing comment
   */
  async updateComment(id: number, data: UpdateCommentDTO): Promise<Comment> {
    const response = await this.request<ApiResponse<Comment>>({
      method: 'PUT',
      url: `/comments/${id}`,
      data,
    });
    return response.data;
  }

  /**
   * Delete a comment
   */
  async deleteComment(id: number): Promise<void> {
    await this.request<{ message: string }>({
      method: 'DELETE',
      url: `/comments/${id}`,
    });
  }
}

// Export singleton instance
export default new ApiService();
