"""
Comment Service Layer
Business logic for comment CRUD operations
"""
from typing import List, Optional, Dict, Any
from app import db
from app.models import Comment, Task
from sqlalchemy.exc import SQLAlchemyError


class CommentService:
    """
    Service layer for handling comment business logic
    Separates data access from route handlers
    """
    
    @staticmethod
    def create_comment(task_id: int, content: str, author: str) -> Comment:
        """
        Create a new comment for a task
        
        Args:
            task_id: ID of the task to comment on
            content: Comment text content
            author: Name of the comment author
            
        Returns:
            Created comment instance
            
        Raises:
            ValueError: If task doesn't exist
            SQLAlchemyError: If database operation fails
        """
        # Verify task exists
        task = Task.query.get(task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        
        try:
            comment = Comment(
                task_id=task_id,
                content=content.strip(),
                author=author.strip()
            )
            db.session.add(comment)
            db.session.commit()
            return comment
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_comments_by_task(task_id: int) -> List[Comment]:
        """
        Retrieve all comments for a specific task
        
        Args:
            task_id: ID of the task
            
        Returns:
            List of comments for the task
            
        Raises:
            ValueError: If task doesn't exist
        """
        # Verify task exists
        task = Task.query.get(task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        
        return Comment.query.filter_by(task_id=task_id).order_by(Comment.created_at.desc()).all()
    
    @staticmethod
    def get_comment_by_id(comment_id: int) -> Optional[Comment]:
        """
        Retrieve a single comment by ID
        
        Args:
            comment_id: ID of the comment
            
        Returns:
            Comment instance or None if not found
        """
        return Comment.query.get(comment_id)
    
    @staticmethod
    def update_comment(comment_id: int, updates: Dict[str, Any]) -> Comment:
        """
        Update an existing comment
        
        Args:
            comment_id: ID of the comment to update
            updates: Dictionary containing fields to update
            
        Returns:
            Updated comment instance
            
        Raises:
            ValueError: If comment doesn't exist
            SQLAlchemyError: If database operation fails
        """
        comment = Comment.query.get(comment_id)
        if not comment:
            raise ValueError(f"Comment with id {comment_id} not found")
        
        try:
            # Update only provided fields
            if 'content' in updates:
                comment.content = updates['content'].strip()
            if 'author' in updates:
                comment.author = updates['author'].strip()
            
            db.session.commit()
            return comment
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_comment(comment_id: int) -> bool:
        """
        Delete a comment
        
        Args:
            comment_id: ID of the comment to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            ValueError: If comment doesn't exist
            SQLAlchemyError: If database operation fails
        """
        comment = Comment.query.get(comment_id)
        if not comment:
            raise ValueError(f"Comment with id {comment_id} not found")
        
        try:
            db.session.delete(comment)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_all_comments() -> List[Comment]:
        """
        Retrieve all comments in the system
        
        Returns:
            List of all comments
        """
        return Comment.query.order_by(Comment.created_at.desc()).all()
