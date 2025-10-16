"""Routes package"""
from app.routes.comment_routes import comment_bp
from app.routes.task_routes import task_bp

__all__ = ['comment_bp', 'task_bp']
