/**
 * Custom hook for managing tasks
 */
import { useState, useEffect, useCallback } from 'react';
import apiService from '../services/apiService';
import { Task, CreateTaskDTO, UpdateTaskDTO } from '../types';

export const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Fetch all tasks
   */
  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiService.getTasks();
      setTasks(data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to fetch tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Create a new task
   */
  const createTask = async (taskData: CreateTaskDTO): Promise<Task | null> => {
    setLoading(true);
    setError(null);
    try {
      const newTask = await apiService.createTask(taskData);
      setTasks((prev) => [newTask, ...prev]);
      return newTask;
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to create task');
      console.error('Error creating task:', err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Update an existing task
   */
  const updateTask = async (id: number, updates: UpdateTaskDTO): Promise<Task | null> => {
    setLoading(true);
    setError(null);
    try {
      const updatedTask = await apiService.updateTask(id, updates);
      setTasks((prev) =>
        prev.map((task) => (task.id === id ? updatedTask : task))
      );
      return updatedTask;
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to update task');
      console.error('Error updating task:', err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Delete a task
   */
  const deleteTask = async (id: number): Promise<boolean> => {
    setLoading(true);
    setError(null);
    try {
      await apiService.deleteTask(id);
      setTasks((prev) => prev.filter((task) => task.id !== id));
      return true;
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to delete task');
      console.error('Error deleting task:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Fetch tasks on mount
  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
  };
};
