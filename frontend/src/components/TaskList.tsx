/**
 * TaskList Component
 * Displays list of tasks with actions
 */
import React from 'react';
import { Task } from '../types';
import '../styles/TaskList.css';

interface TaskListProps {
  tasks: Task[];
  selectedTaskId: number | null;
  onSelectTask: (taskId: number) => void;
  onEditTask: (task: Task) => void;
  onDeleteTask: (taskId: number) => void;
  loading?: boolean;
}

export const TaskList: React.FC<TaskListProps> = ({
  tasks,
  selectedTaskId,
  onSelectTask,
  onEditTask,
  onDeleteTask,
  loading = false,
}) => {
  const handleDelete = (e: React.MouseEvent, taskId: number) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this task? All associated comments will be deleted.')) {
      onDeleteTask(taskId);
    }
  };

  const handleEdit = (e: React.MouseEvent, task: Task) => {
    e.stopPropagation();
    onEditTask(task);
  };

  if (loading) {
    return <div className="task-list-loading">Loading tasks...</div>;
  }

  if (tasks.length === 0) {
    return <div className="task-list-empty">No tasks found. Create your first task!</div>;
  }

  return (
    <div className="task-list">
      {tasks.map((task) => (
        <div
          key={task.id}
          className={`task-item ${selectedTaskId === task.id ? 'selected' : ''}`}
          onClick={() => onSelectTask(task.id)}
        >
          <div className="task-content">
            <h4 className="task-title">{task.title}</h4>
            {task.description && <p className="task-description">{task.description}</p>}
            <div className="task-meta">
              <span className="task-comments-count">
                {task.comments_count} {task.comments_count === 1 ? 'comment' : 'comments'}
              </span>
              <span className="task-date">
                Created: {new Date(task.created_at).toLocaleDateString()}
              </span>
            </div>
          </div>
          <div className="task-actions">
            <button
              className="btn-edit"
              onClick={(e) => handleEdit(e, task)}
              title="Edit task"
            >
              Edit
            </button>
            <button
              className="btn-delete"
              onClick={(e) => handleDelete(e, task.id)}
              title="Delete task"
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};
