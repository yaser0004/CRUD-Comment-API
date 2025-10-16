"""
Integration tests for Comment Routes
"""
import pytest
import json
from app import create_app, db
from app.models import Task, Comment


@pytest.fixture
def app():
    """Create and configure test application"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def sample_task(app):
    """Create a sample task for testing"""
    with app.app_context():
        task = Task(title="Test Task", description="Test Description")
        db.session.add(task)
        db.session.commit()
        return task.id


class TestCommentRoutes:
    """Test suite for comment API endpoints"""
    
    def test_create_comment_success(self, client, sample_task):
        """Test POST /api/comments - successful creation"""
        response = client.post(
            '/api/comments',
            data=json.dumps({
                'task_id': sample_task,
                'content': 'Test comment',
                'author': 'John Doe'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Comment created successfully'
        assert data['data']['content'] == 'Test comment'
        assert data['data']['author'] == 'John Doe'
    
    def test_create_comment_missing_fields(self, client):
        """Test POST /api/comments - missing required fields"""
        response = client.post(
            '/api/comments',
            data=json.dumps({
                'content': 'Test comment'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Validation error' in data['error']
    
    def test_create_comment_invalid_task(self, client):
        """Test POST /api/comments - non-existent task"""
        response = client.post(
            '/api/comments',
            data=json.dumps({
                'task_id': 9999,
                'content': 'Test comment',
                'author': 'John Doe'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'Task with id 9999 not found' in data['error']
    
    def test_create_comment_empty_content(self, client, sample_task):
        """Test POST /api/comments - empty content"""
        response = client.post(
            '/api/comments',
            data=json.dumps({
                'task_id': sample_task,
                'content': '   ',
                'author': 'John Doe'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_get_comments_by_task(self, client, app, sample_task):
        """Test GET /api/comments/task/<task_id>"""
        # Create test comments
        with app.app_context():
            comment1 = Comment(task_id=sample_task, content="Comment 1", author="Author 1")
            comment2 = Comment(task_id=sample_task, content="Comment 2", author="Author 2")
            db.session.add_all([comment1, comment2])
            db.session.commit()
        
        response = client.get(f'/api/comments/task/{sample_task}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 2
        assert len(data['data']) == 2
    
    def test_get_comments_by_nonexistent_task(self, client):
        """Test GET /api/comments/task/<task_id> - task not found"""
        response = client.get('/api/comments/task/9999')
        
        assert response.status_code == 404
    
    def test_get_comment_by_id(self, client, app, sample_task):
        """Test GET /api/comments/<comment_id>"""
        # Create test comment
        with app.app_context():
            comment = Comment(task_id=sample_task, content="Test", author="Author")
            db.session.add(comment)
            db.session.commit()
            comment_id = comment.id
        
        response = client.get(f'/api/comments/{comment_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['id'] == comment_id
        assert data['data']['content'] == "Test"
    
    def test_get_comment_not_found(self, client):
        """Test GET /api/comments/<comment_id> - comment not found"""
        response = client.get('/api/comments/9999')
        
        assert response.status_code == 404
    
    def test_update_comment_success(self, client, app, sample_task):
        """Test PUT /api/comments/<comment_id>"""
        # Create test comment
        with app.app_context():
            comment = Comment(task_id=sample_task, content="Original", author="Original Author")
            db.session.add(comment)
            db.session.commit()
            comment_id = comment.id
        
        response = client.put(
            f'/api/comments/{comment_id}',
            data=json.dumps({
                'content': 'Updated content',
                'author': 'Updated Author'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Comment updated successfully'
        assert data['data']['content'] == 'Updated content'
        assert data['data']['author'] == 'Updated Author'
    
    def test_update_comment_partial(self, client, app, sample_task):
        """Test PUT /api/comments/<comment_id> - partial update"""
        with app.app_context():
            comment = Comment(task_id=sample_task, content="Original", author="Original")
            db.session.add(comment)
            db.session.commit()
            comment_id = comment.id
        
        response = client.put(
            f'/api/comments/{comment_id}',
            data=json.dumps({'content': 'Updated only content'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['content'] == 'Updated only content'
        assert data['data']['author'] == 'Original'
    
    def test_update_comment_not_found(self, client):
        """Test PUT /api/comments/<comment_id> - comment not found"""
        response = client.put(
            '/api/comments/9999',
            data=json.dumps({'content': 'Updated'}),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_update_comment_no_fields(self, client, app, sample_task):
        """Test PUT /api/comments/<comment_id> - no valid fields"""
        with app.app_context():
            comment = Comment(task_id=sample_task, content="Content", author="Author")
            db.session.add(comment)
            db.session.commit()
            comment_id = comment.id
        
        response = client.put(
            f'/api/comments/{comment_id}',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_delete_comment_success(self, client, app, sample_task):
        """Test DELETE /api/comments/<comment_id>"""
        with app.app_context():
            comment = Comment(task_id=sample_task, content="Content", author="Author")
            db.session.add(comment)
            db.session.commit()
            comment_id = comment.id
        
        response = client.delete(f'/api/comments/{comment_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Comment deleted successfully'
        
        # Verify deletion
        verify_response = client.get(f'/api/comments/{comment_id}')
        assert verify_response.status_code == 404
    
    def test_delete_comment_not_found(self, client):
        """Test DELETE /api/comments/<comment_id> - comment not found"""
        response = client.delete('/api/comments/9999')
        
        assert response.status_code == 404
    
    def test_get_all_comments(self, client, app, sample_task):
        """Test GET /api/comments - get all comments"""
        with app.app_context():
            task2 = Task(title="Task 2")
            db.session.add(task2)
            db.session.commit()
            
            comment1 = Comment(task_id=sample_task, content="Comment 1", author="Author 1")
            comment2 = Comment(task_id=task2.id, content="Comment 2", author="Author 2")
            db.session.add_all([comment1, comment2])
            db.session.commit()
        
        response = client.get('/api/comments')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 2
        assert len(data['data']) == 2

    def test_create_comment_database_error(self, client, sample_task, monkeypatch):
        """Test database error handling during comment creation"""
        from sqlalchemy.exc import SQLAlchemyError
        from app.services import comment_service
        
        def mock_create_error(*args, **kwargs):
            raise SQLAlchemyError("Database connection failed")
        
        monkeypatch.setattr(comment_service.CommentService, 'create_comment', mock_create_error)
        
        response = client.post('/api/comments', json={
            'task_id': sample_task,
            'content': 'Test comment',
            'author': 'Test Author'
        })
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'Database error' in data['error']

    def test_create_comment_general_exception(self, client, sample_task, monkeypatch):
        """Test general exception handling during comment creation"""
        from app.services import comment_service
        
        def mock_create_exception(*args, **kwargs):
            raise Exception("Unexpected error occurred")
        
        monkeypatch.setattr(comment_service.CommentService, 'create_comment', mock_create_exception)
        
        response = client.post('/api/comments', json={
            'task_id': sample_task,
            'content': 'Test comment',
            'author': 'Test Author'
        })
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'Internal server error' in data['error']
    
    def test_get_comments_by_task_database_error(self, client, sample_task, monkeypatch):
        """Test database error handling when getting comments by task"""
        from sqlalchemy.exc import SQLAlchemyError
        from app.services import comment_service
        
        def mock_get_error(*args, **kwargs):
            raise SQLAlchemyError("Database connection failed")
        
        monkeypatch.setattr(comment_service.CommentService, 'get_comments_by_task', mock_get_error)
        
        response = client.get(f'/api/comments/task/{sample_task}')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'Internal server error' in data['error']
    
    def test_get_comments_by_task_general_exception(self, client, sample_task, monkeypatch):
        """Test general exception handling when getting comments by task"""
        from app.services import comment_service
        
        def mock_get_exception(*args, **kwargs):
            raise Exception("Unexpected error occurred")
        
        monkeypatch.setattr(comment_service.CommentService, 'get_comments_by_task', mock_get_exception)
        
        response = client.get(f'/api/comments/task/{sample_task}')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'Internal server error' in data['error']
    
    def test_get_comment_by_id_database_error(self, client, monkeypatch):
        """Test database error handling when getting comment by ID"""
        from sqlalchemy.exc import SQLAlchemyError
        from app.services import comment_service
        
        def mock_get_error(*args, **kwargs):
            raise SQLAlchemyError("Database connection failed")
        
        monkeypatch.setattr(comment_service.CommentService, 'get_comment_by_id', mock_get_error)
        
        response = client.get('/api/comments/1')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'Internal server error' in data['error']
    
    def test_get_comment_by_id_general_exception(self, client, monkeypatch):
        """Test general exception handling when getting comment by ID"""
        from app.services import comment_service
        
        def mock_get_exception(*args, **kwargs):
            raise Exception("Unexpected error occurred")
        
        monkeypatch.setattr(comment_service.CommentService, 'get_comment_by_id', mock_get_exception)
        
        response = client.get('/api/comments/1')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'Internal server error' in data['error']
    
    def test_update_comment_database_error(self, client, monkeypatch):
        """Test database error handling when updating comment"""
        from sqlalchemy.exc import SQLAlchemyError
        from app.services import comment_service
        
        def mock_update_error(*args, **kwargs):
            raise SQLAlchemyError("Database connection failed")
        
        monkeypatch.setattr(comment_service.CommentService, 'update_comment', mock_update_error)
        
        response = client.put('/api/comments/1', json={
            'content': 'Updated content'
        })
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'Database error' in data['error']
    
    def test_update_comment_general_exception(self, client, monkeypatch):
        """Test general exception handling when updating comment"""
        from app.services import comment_service
        
        def mock_update_exception(*args, **kwargs):
            raise Exception("Unexpected error occurred")
        
        monkeypatch.setattr(comment_service.CommentService, 'update_comment', mock_update_exception)
        
        response = client.put('/api/comments/1', json={
            'content': 'Updated content'
        })
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'Internal server error' in data['error']
    
    def test_delete_comment_database_error(self, client, monkeypatch):
        """Test database error handling when deleting comment"""
        from sqlalchemy.exc import SQLAlchemyError
        from app.services import comment_service
        
        def mock_delete_error(*args, **kwargs):
            raise SQLAlchemyError("Database connection failed")
        
        monkeypatch.setattr(comment_service.CommentService, 'delete_comment', mock_delete_error)
        
        response = client.delete('/api/comments/1')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'Database error' in data['error']
    
    def test_delete_comment_general_exception(self, client, monkeypatch):
        """Test general exception handling when deleting comment"""
        from app.services import comment_service
        
        def mock_delete_exception(*args, **kwargs):
            raise Exception("Unexpected error occurred")
        
        monkeypatch.setattr(comment_service.CommentService, 'delete_comment', mock_delete_exception)
        
        response = client.delete('/api/comments/1')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'Internal server error' in data['error']
    
    def test_get_all_comments_database_error(self, client, monkeypatch):
        """Test database error handling when getting all comments"""
        from sqlalchemy.exc import SQLAlchemyError
        from app.services import comment_service
        
        def mock_get_all_error(*args, **kwargs):
            raise SQLAlchemyError("Database connection failed")
        
        monkeypatch.setattr(comment_service.CommentService, 'get_all_comments', mock_get_all_error)
        
        response = client.get('/api/comments')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'Internal server error' in data['error']
    
    def test_get_all_comments_general_exception(self, client, monkeypatch):
        """Test general exception handling when getting all comments"""
        from app.services import comment_service
        
        def mock_get_all_exception(*args, **kwargs):
            raise Exception("Unexpected error occurred")
        
        monkeypatch.setattr(comment_service.CommentService, 'get_all_comments', mock_get_all_exception)
        
        response = client.get('/api/comments')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'Internal server error' in data['error']

