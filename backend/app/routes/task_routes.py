"""
Task Routes
RESTful API endpoints for task CRUD operations
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.services import TaskService
from app.schemas import task_schema, tasks_schema, task_update_schema

task_bp = Blueprint('tasks', __name__)


@task_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    Create a new task
    
    Request body:
        {
            "title": str,
            "description": str (optional)
        }
    
    Returns:
        201: Task created successfully
        400: Validation error
        500: Server error
    """
    try:
        # Validate request data
        data = task_schema.load(request.json)
        
        # Create task via service layer
        task = TaskService.create_task(
            title=data['title'],
            description=data.get('description')
        )
        
        return jsonify({
            'message': 'Task created successfully',
            'data': task.to_dict()
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'messages': e.messages
        }), 400
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


@task_bp.route('/tasks', methods=['GET'])
def get_all_tasks():
    """
    Get all tasks
    
    Returns:
        200: List of tasks
        500: Server error
    """
    try:
        tasks = TaskService.get_all_tasks()
        
        return jsonify({
            'data': [task.to_dict() for task in tasks],
            'count': len(tasks)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Get a specific task by ID
    
    Args:
        task_id: ID of the task
    
    Returns:
        200: Task data
        404: Task not found
        500: Server error
    """
    try:
        task = TaskService.get_task_by_id(task_id)
        
        if not task:
            return jsonify({
                'error': f'Task with id {task_id} not found'
            }), 404
        
        return jsonify({
            'data': task.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update an existing task
    
    Args:
        task_id: ID of the task to update
    
    Request body (all fields optional):
        {
            "title": str,
            "description": str
        }
    
    Returns:
        200: Task updated successfully
        400: Validation error
        404: Task not found
        500: Server error
    """
    try:
        # Validate request data
        data = task_update_schema.load(request.json)
        
        if not data:
            return jsonify({
                'error': 'No valid fields to update'
            }), 400
        
        # Update task via service layer
        task = TaskService.update_task(task_id, data)
        
        return jsonify({
            'message': 'Task updated successfully',
            'data': task.to_dict()
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


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a task and all associated comments
    
    Args:
        task_id: ID of the task to delete
    
    Returns:
        200: Task deleted successfully
        404: Task not found
        500: Server error
    """
    try:
        TaskService.delete_task(task_id)
        
        return jsonify({
            'message': 'Task deleted successfully'
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
