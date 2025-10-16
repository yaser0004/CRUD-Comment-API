/**
 * CommentList Component
 * Displays list of comments for a task
 */
import React from 'react';
import { Comment } from '../types';
import '../styles/CommentList.css';

interface CommentListProps {
  comments: Comment[];
  onEditComment: (comment: Comment) => void;
  onDeleteComment: (commentId: number) => void;
  loading?: boolean;
}

export const CommentList: React.FC<CommentListProps> = ({
  comments,
  onEditComment,
  onDeleteComment,
  loading = false,
}) => {
  const handleDelete = (commentId: number) => {
    if (window.confirm('Are you sure you want to delete this comment?')) {
      onDeleteComment(commentId);
    }
  };

  if (loading) {
    return <div className="comment-list-loading">Loading comments...</div>;
  }

  if (comments.length === 0) {
    return <div className="comment-list-empty">No comments yet. Be the first to comment!</div>;
  }

  return (
    <div className="comment-list">
      {comments.map((comment) => (
        <div key={comment.id} className="comment-item">
          <div className="comment-header">
            <span className="comment-author">{comment.author}</span>
            <span className="comment-date">
              {new Date(comment.created_at).toLocaleString()}
            </span>
          </div>
          <div className="comment-content">
            <p>{comment.content}</p>
          </div>
          <div className="comment-actions">
            <button
              className="btn-edit-small"
              onClick={() => onEditComment(comment)}
              title="Edit comment"
            >
              Edit
            </button>
            <button
              className="btn-delete-small"
              onClick={() => handleDelete(comment.id)}
              title="Delete comment"
            >
              Delete
            </button>
          </div>
          {comment.updated_at !== comment.created_at && (
            <div className="comment-edited">
              (edited: {new Date(comment.updated_at).toLocaleString()})
            </div>
          )}
        </div>
      ))}
    </div>
  );
};
