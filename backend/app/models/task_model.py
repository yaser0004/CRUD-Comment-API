"""
Task Model
Represents a task entity in the database
"""
from datetime import datetime
from app import db


class Task(db.Model):
    """
    Task model representing a task in the system
    
    Attributes:
        id: Primary key
        title: Task title
        description: Task description
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
        comments: Relationship to associated comments
    """
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship: One task can have many comments
    comments = db.relationship('Comment', backref='task', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """
        Convert task instance to dictionary
        
        Returns:
            Dictionary representation of task
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None,
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None,
            'comments_count': len(self.comments)
        }
    
    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'
