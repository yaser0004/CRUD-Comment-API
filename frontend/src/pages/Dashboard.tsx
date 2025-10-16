/**
 * Dashboard Page
 * Main page showing tasks and comments
 */
import React, { useState, useEffect } from 'react';
import { TaskList } from '../components/TaskList';
import { TaskForm } from '../components/TaskForm';
import { CommentList } from '../components/CommentList';
import { CommentForm } from '../components/CommentForm';
import { useTasks } from '../hooks/useTasks';
import { useComments } from '../hooks/useComments';
import { Task, Comment, CreateTaskDTO, UpdateTaskDTO, CreateCommentDTO, UpdateCommentDTO } from '../types';
import '../styles/Dashboard.css';

export const Dashboard: React.FC = () => {
  const { tasks, loading: tasksLoading, error: tasksError, createTask, updateTask, deleteTask } = useTasks();
  const { comments, loading: commentsLoading, error: commentsError, fetchCommentsByTask, createComment, updateComment, deleteComment } = useComments();

  const [selectedTaskId, setSelectedTaskId] = useState<number | null>(null);
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [editingComment, setEditingComment] = useState<Comment | null>(null);

  // Fetch comments when task is selected
  useEffect(() => {
    if (selectedTaskId) {
      fetchCommentsByTask(selectedTaskId);
    }
  }, [selectedTaskId, fetchCommentsByTask]);

  // Auto-select first task if none selected
  useEffect(() => {
    if (!selectedTaskId && tasks.length > 0) {
      setSelectedTaskId(tasks[0].id);
    }
  }, [tasks, selectedTaskId]);

  const handleCreateTask = async (data: CreateTaskDTO) => {
    const newTask = await createTask(data);
    if (newTask) {
      setShowTaskForm(false);
      setSelectedTaskId(newTask.id);
    }
  };

  const handleUpdateTask = async (data: UpdateTaskDTO) => {
    if (editingTask) {
      const updated = await updateTask(editingTask.id, data);
      if (updated) {
        setEditingTask(null);
        setShowTaskForm(false);
      }
    }
  };

  const handleTaskSubmit = async (data: CreateTaskDTO | UpdateTaskDTO) => {
    if (editingTask) {
      await handleUpdateTask(data as UpdateTaskDTO);
    } else {
      await handleCreateTask(data as CreateTaskDTO);
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    const success = await deleteTask(taskId);
    if (success && selectedTaskId === taskId) {
      setSelectedTaskId(null);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowTaskForm(true);
  };

  const handleCancelTaskForm = () => {
    setShowTaskForm(false);
    setEditingTask(null);
  };

  const handleCreateComment = async (data: CreateCommentDTO | UpdateCommentDTO) => {
    if (selectedTaskId) {
      const newComment = await createComment(data as CreateCommentDTO);
      if (newComment) {
        // Refresh to update comment count
        fetchCommentsByTask(selectedTaskId);
      }
    }
  };

  const handleUpdateComment = async (data: CreateCommentDTO | UpdateCommentDTO) => {
    if (editingComment) {
      const updated = await updateComment(editingComment.id, data as UpdateCommentDTO);
      if (updated) {
        setEditingComment(null);
      }
    }
  };

  const handleEditComment = (comment: Comment) => {
    setEditingComment(comment);
  };

  const handleDeleteComment = async (commentId: number) => {
    await deleteComment(commentId);
  };

  const handleCancelCommentEdit = () => {
    setEditingComment(null);
  };

  const selectedTask = tasks.find(t => t.id === selectedTaskId);

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Task & Comment Management</h1>
      </header>

      <div className="dashboard-content">
        {/* Left Panel - Tasks */}
        <div className="tasks-panel">
          <div className="panel-header">
            <h2>Tasks</h2>
            <button
              className="btn-primary"
              onClick={() => setShowTaskForm(!showTaskForm)}
            >
              {showTaskForm ? 'Cancel' : 'New Task'}
            </button>
          </div>

          {tasksError && <div className="error-message">{tasksError}</div>}

          {showTaskForm && (
            <TaskForm
              task={editingTask}
              onSubmit={handleTaskSubmit}
              onCancel={handleCancelTaskForm}
            />
          )}

          <TaskList
            tasks={tasks}
            selectedTaskId={selectedTaskId}
            onSelectTask={setSelectedTaskId}
            onEditTask={handleEditTask}
            onDeleteTask={handleDeleteTask}
            loading={tasksLoading}
          />
        </div>

        {/* Right Panel - Comments */}
        <div className="comments-panel">
          {selectedTask ? (
            <>
              <div className="panel-header">
                <h2>Comments for: {selectedTask.title}</h2>
              </div>

              {commentsError && <div className="error-message">{commentsError}</div>}

              {editingComment ? (
                <CommentForm
                  taskId={selectedTask.id}
                  comment={editingComment}
                  onSubmit={handleUpdateComment}
                  onCancel={handleCancelCommentEdit}
                />
              ) : (
                <CommentForm
                  taskId={selectedTask.id}
                  onSubmit={handleCreateComment}
                />
              )}

              <CommentList
                comments={comments}
                onEditComment={handleEditComment}
                onDeleteComment={handleDeleteComment}
                loading={commentsLoading}
              />
            </>
          ) : (
            <div className="no-task-selected">
              <p>Select a task to view and manage comments</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
