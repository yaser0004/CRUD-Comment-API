"""
Task Service Layer
Business logic for task CRUD operations
"""
from typing import List, Optional, Dict, Any
from app import db
from app.models import Task
from sqlalchemy.exc import SQLAlchemyError


class TaskService:
    """
    Service layer for handling task business logic
    """
    
    @staticmethod
    def create_task(title: str, description: Optional[str] = None) -> Task:
        """
        Create a new task
        
        Args:
            title: Task title
            description: Optional task description
            
        Returns:
            Created task instance
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            task = Task(
                title=title.strip(),
                description=description.strip() if description else None
            )
            db.session.add(task)
            db.session.commit()
            return task
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_all_tasks() -> List[Task]:
        """
        Retrieve all tasks
        
        Returns:
            List of all tasks ordered by creation date (newest first)
        """
        return Task.query.order_by(Task.created_at.desc()).all()
    
    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Task]:
        """
        Retrieve a single task by ID
        
        Args:
            task_id: ID of the task
            
        Returns:
            Task instance or None if not found
        """
        return Task.query.get(task_id)
    
    @staticmethod
    def update_task(task_id: int, updates: Dict[str, Any]) -> Task:
        """
        Update an existing task
        
        Args:
            task_id: ID of the task to update
            updates: Dictionary containing fields to update
            
        Returns:
            Updated task instance
            
        Raises:
            ValueError: If task doesn't exist
            SQLAlchemyError: If database operation fails
        """
        task = Task.query.get(task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        
        try:
            # Update only provided fields
            if 'title' in updates:
                task.title = updates['title'].strip()
            if 'description' in updates:
                task.description = updates['description'].strip() if updates['description'] else None
            
            db.session.commit()
            return task
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_task(task_id: int) -> bool:
        """
        Delete a task and all associated comments (cascade)
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            ValueError: If task doesn't exist
            SQLAlchemyError: If database operation fails
        """
        task = Task.query.get(task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        
        try:
            db.session.delete(task)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
