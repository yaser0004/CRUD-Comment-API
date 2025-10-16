"""
Comment Model
Represents a comment entity associated with a task
"""
from datetime import datetime
from app import db


class Comment(db.Model):
    """
    Comment model representing a comment on a task
    
    Attributes:
        id: Primary key
        task_id: Foreign key referencing tasks table
        content: Comment text content
        author: Name of the comment author
        created_at: Timestamp when comment was created
        updated_at: Timestamp when comment was last updated
    """
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """
        Convert comment instance to dictionary
        
        Returns:
            Dictionary representation of comment
        """
        return {
            'id': self.id,
            'task_id': self.task_id,
            'content': self.content,
            'author': self.author,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None,
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Comment {self.id} by {self.author}>'
