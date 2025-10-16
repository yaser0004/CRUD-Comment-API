/**
 * CommentForm Component
 * Form for creating and editing comments
 */
import React, { useState, useEffect } from 'react';
import { Comment, CreateCommentDTO, UpdateCommentDTO } from '../types';
import '../styles/CommentForm.css';

interface CommentFormProps {
  taskId: number;
  comment?: Comment | null;
  onSubmit: (data: CreateCommentDTO | UpdateCommentDTO) => Promise<void>;
  onCancel?: () => void;
}

export const CommentForm: React.FC<CommentFormProps> = ({
  taskId,
  comment,
  onSubmit,
  onCancel,
}) => {
  const [content, setContent] = useState('');
  const [author, setAuthor] = useState('');
  const [errors, setErrors] = useState<{ content?: string; author?: string }>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (comment) {
      setContent(comment.content);
      setAuthor(comment.author);
    }
  }, [comment]);

  const validate = (): boolean => {
    const newErrors: { content?: string; author?: string } = {};

    if (!content.trim()) {
      newErrors.content = 'Comment content is required';
    } else if (content.length > 2000) {
      newErrors.content = 'Comment must be less than 2000 characters';
    }

    if (!comment && !author.trim()) {
      newErrors.author = 'Author name is required';
    } else if (author.length > 100) {
      newErrors.author = 'Author name must be less than 100 characters';
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
      if (comment) {
        // Editing existing comment
        const data: UpdateCommentDTO = {
          content: content.trim(),
          author: author.trim() || undefined,
        };
        await onSubmit(data);
      } else {
        // Creating new comment
        const data: CreateCommentDTO = {
          task_id: taskId,
          content: content.trim(),
          author: author.trim(),
        };
        await onSubmit(data);
      }

      // Reset form
      setContent('');
      setAuthor('');
      setErrors({});
    } catch (error) {
      console.error('Error submitting comment:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    setContent('');
    setAuthor('');
    setErrors({});
    if (onCancel) {
      onCancel();
    }
  };

  return (
    <div className="comment-form">
      <h4>{comment ? 'Edit Comment' : 'Add Comment'}</h4>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="content">
            Comment <span className="required">*</span>
          </label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Write your comment here..."
            rows={4}
            className={errors.content ? 'error' : ''}
            disabled={isSubmitting}
          />
          {errors.content && <span className="error-message">{errors.content}</span>}
        </div>

        {!comment && (
          <div className="form-group">
            <label htmlFor="author">
              Author <span className="required">*</span>
            </label>
            <input
              type="text"
              id="author"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
              placeholder="Your name"
              className={errors.author ? 'error' : ''}
              disabled={isSubmitting}
            />
            {errors.author && <span className="error-message">{errors.author}</span>}
          </div>
        )}

        <div className="form-actions">
          <button type="submit" className="btn-primary" disabled={isSubmitting}>
            {isSubmitting ? 'Saving...' : comment ? 'Update Comment' : 'Add Comment'}
          </button>
          {(comment || onCancel) && (
            <button
              type="button"
              className="btn-secondary"
              onClick={handleCancel}
              disabled={isSubmitting}
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};
