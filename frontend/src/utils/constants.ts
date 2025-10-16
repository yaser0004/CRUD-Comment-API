/**
 * Application constants
 */

export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const API_ENDPOINTS = {
  TASKS: '/tasks',
  TASK_BY_ID: (id: number) => `/tasks/${id}`,
  COMMENTS: '/comments',
  COMMENT_BY_ID: (id: number) => `/comments/${id}`,
  COMMENTS_BY_TASK: (taskId: number) => `/comments/task/${taskId}`,
} as const;

export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection.',
  SERVER_ERROR: 'Server error. Please try again later.',
  NOT_FOUND: 'Resource not found.',
  VALIDATION_ERROR: 'Validation error. Please check your input.',
} as const;

export const SUCCESS_MESSAGES = {
  TASK_CREATED: 'Task created successfully!',
  TASK_UPDATED: 'Task updated successfully!',
  TASK_DELETED: 'Task deleted successfully!',
  COMMENT_CREATED: 'Comment created successfully!',
  COMMENT_UPDATED: 'Comment updated successfully!',
  COMMENT_DELETED: 'Comment deleted successfully!',
} as const;
