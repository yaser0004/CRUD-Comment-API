/**
 * Custom hook for managing comments
 */
import { useState, useCallback } from 'react';
import apiService from '../services/apiService';
import { Comment, CreateCommentDTO, UpdateCommentDTO } from '../types';

export const useComments = (taskId?: number) => {
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Fetch comments for a specific task
   */
  const fetchCommentsByTask = useCallback(async (id: number) => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiService.getCommentsByTask(id);
      setComments(data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to fetch comments');
      console.error('Error fetching comments:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Create a new comment
   */
  const createComment = async (commentData: CreateCommentDTO): Promise<Comment | null> => {
    setLoading(true);
    setError(null);
    try {
      const newComment = await apiService.createComment(commentData);
      setComments((prev) => [newComment, ...prev]);
      return newComment;
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to create comment');
      console.error('Error creating comment:', err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Update an existing comment
   */
  const updateComment = async (id: number, updates: UpdateCommentDTO): Promise<Comment | null> => {
    setLoading(true);
    setError(null);
    try {
      const updatedComment = await apiService.updateComment(id, updates);
      setComments((prev) =>
        prev.map((comment) => (comment.id === id ? updatedComment : comment))
      );
      return updatedComment;
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to update comment');
      console.error('Error updating comment:', err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Delete a comment
   */
  const deleteComment = async (id: number): Promise<boolean> => {
    setLoading(true);
    setError(null);
    try {
      await apiService.deleteComment(id);
      setComments((prev) => prev.filter((comment) => comment.id !== id));
      return true;
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to delete comment');
      console.error('Error deleting comment:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  return {
    comments,
    loading,
    error,
    fetchCommentsByTask,
    createComment,
    updateComment,
    deleteComment,
  };
};
