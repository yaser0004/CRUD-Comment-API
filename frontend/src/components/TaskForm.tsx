/**
 * TaskForm Component
 * Form for creating and editing tasks
 */
import React, { useState, useEffect } from 'react';
import { Task, CreateTaskDTO, UpdateTaskDTO } from '../types';
import '../styles/TaskForm.css';

interface TaskFormProps {
  task?: Task | null;
  onSubmit: (data: CreateTaskDTO | UpdateTaskDTO) => Promise<void>;
  onCancel: () => void;
}

export const TaskForm: React.FC<TaskFormProps> = ({ task, onSubmit, onCancel }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [errors, setErrors] = useState<{ title?: string; description?: string }>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description || '');
    }
  }, [task]);

  const validate = (): boolean => {
    const newErrors: { title?: string; description?: string } = {};

    if (!title.trim()) {
      newErrors.title = 'Title is required';
    } else if (title.length > 200) {
      newErrors.title = 'Title must be less than 200 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    setIsSubmitting(true);
    try {
      const data: CreateTaskDTO | UpdateTaskDTO = {
        title: title.trim(),
        description: description.trim() || undefined,
      };

      await onSubmit(data);

      // Reset form
      setTitle('');
      setDescription('');
      setErrors({});
    } catch (error) {
      console.error('Error submitting form:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    setTitle('');
    setDescription('');
    setErrors({});
    onCancel();
  };

  return (
    <div className="task-form">
      <h3>{task ? 'Edit Task' : 'Create New Task'}</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">
            Title <span className="required">*</span>
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter task title"
            className={errors.title ? 'error' : ''}
            disabled={isSubmitting}
          />
          {errors.title && <span className="error-message">{errors.title}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Enter task description (optional)"
            rows={4}
            className={errors.description ? 'error' : ''}
            disabled={isSubmitting}
          />
          {errors.description && <span className="error-message">{errors.description}</span>}
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-primary" disabled={isSubmitting}>
            {isSubmitting ? 'Saving...' : task ? 'Update Task' : 'Create Task'}
          </button>
          <button type="button" className="btn-secondary" onClick={handleCancel} disabled={isSubmitting}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};
