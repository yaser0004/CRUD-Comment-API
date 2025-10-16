"""
Comment Routes
RESTful API endpoints for comment CRUD operations
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.services import CommentService
from app.schemas import comment_schema, comments_schema, comment_update_schema

comment_bp = Blueprint('comments', __name__)


@comment_bp.route('/comments', methods=['POST'])
def create_comment():
    """
    Create a new comment
    
    Request body:
        {
            "task_id": int,
            "content": str,
            "author": str
        }
    
    Returns:
        201: Comment created successfully
        400: Validation error
        404: Task not found
        500: Server error
    """
    try:
        # Validate request data
        data = comment_schema.load(request.json)
        
        # Create comment via service layer
        comment = CommentService.create_comment(
            task_id=data['task_id'],
            content=data['content'],
            author=data['author']
        )
        
        return jsonify({
            'message': 'Comment created successfully',
            'data': comment.to_dict()
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'messages': e.messages
        }), 400
    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 404
    except SQLAlchemyError as e:
        return jsonify({
            'error': 'Database error',
            'message': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@comment_bp.route('/comments/task/<int:task_id>', methods=['GET'])
def get_comments_by_task(task_id):
    """
    Get all comments for a specific task
    
    Args:
        task_id: ID of the task
    
    Returns:
        200: List of comments
        404: Task not found
        500: Server error
    """
    try:
        comments = CommentService.get_comments_by_task(task_id)
        
        return jsonify({
            'data': [comment.to_dict() for comment in comments],
            'count': len(comments)
        }), 200
        
    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@comment_bp.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    """
    Get a specific comment by ID
    
    Args:
        comment_id: ID of the comment
    
    Returns:
        200: Comment data
        404: Comment not found
        500: Server error
    """
    try:
        comment = CommentService.get_comment_by_id(comment_id)
        
        if not comment:
            return jsonify({
                'error': f'Comment with id {comment_id} not found'
            }), 404
        
        return jsonify({
            'data': comment.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@comment_bp.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    """
    Update an existing comment
    
    Args:
        comment_id: ID of the comment to update
    
    Request body (all fields optional):
        {
            "content": str,
            "author": str
        }
    
    Returns:
        200: Comment updated successfully
        400: Validation error
        404: Comment not found
        500: Server error
    """
    try:
        # Validate request data
        data = comment_update_schema.load(request.json)
        
        if not data:
            return jsonify({
                'error': 'No valid fields to update'
            }), 400
        
        # Update comment via service layer
        comment = CommentService.update_comment(comment_id, data)
        
        return jsonify({
            'message': 'Comment updated successfully',
            'data': comment.to_dict()
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'messages': e.messages
        }), 400
    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 404
    except SQLAlchemyError as e:
        return jsonify({
            'error': 'Database error',
            'message': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@comment_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """
    Delete a comment
    
    Args:
        comment_id: ID of the comment to delete
    
    Returns:
        200: Comment deleted successfully
        404: Comment not found
        500: Server error
    """
    try:
        CommentService.delete_comment(comment_id)
        
        return jsonify({
            'message': 'Comment deleted successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 404
    except SQLAlchemyError as e:
        return jsonify({
            'error': 'Database error',
            'message': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@comment_bp.route('/comments', methods=['GET'])
def get_all_comments():
    """
    Get all comments in the system
    
    Returns:
        200: List of all comments
        500: Server error
    """
    try:
        comments = CommentService.get_all_comments()
        
        return jsonify({
            'data': [comment.to_dict() for comment in comments],
            'count': len(comments)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500
