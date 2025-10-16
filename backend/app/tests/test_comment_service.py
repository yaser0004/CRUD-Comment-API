"""
Unit tests for Comment Service
"""
import pytest
from app import create_app, db
from app.models import Task, Comment
from app.services import CommentService


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


class TestCommentService:
    """Test suite for CommentService"""
    
    def test_create_comment_success(self, app, sample_task):
        """Test successful comment creation"""
        with app.app_context():
            comment = CommentService.create_comment(
                task_id=sample_task,
                content="Test comment content",
                author="John Doe"
            )
            
            assert comment is not None
            assert comment.id is not None
            assert comment.content == "Test comment content"
            assert comment.author == "John Doe"
            assert comment.task_id == sample_task
    
    def test_create_comment_nonexistent_task(self, app):
        """Test comment creation with non-existent task"""
        with app.app_context():
            with pytest.raises(ValueError, match="Task with id 9999 not found"):
                CommentService.create_comment(
                    task_id=9999,
                    content="Test content",
                    author="John Doe"
                )
    
    def test_create_comment_strips_whitespace(self, app, sample_task):
        """Test that create_comment strips whitespace"""
        with app.app_context():
            comment = CommentService.create_comment(
                task_id=sample_task,
                content="  Test content  ",
                author="  John Doe  "
            )
            
            assert comment.content == "Test content"
            assert comment.author == "John Doe"
    
    def test_get_comments_by_task(self, app, sample_task):
        """Test retrieving comments by task ID"""
        with app.app_context():
            # Create multiple comments
            CommentService.create_comment(sample_task, "Comment 1", "Author 1")
            CommentService.create_comment(sample_task, "Comment 2", "Author 2")
            CommentService.create_comment(sample_task, "Comment 3", "Author 3")
            
            comments = CommentService.get_comments_by_task(sample_task)
            
            assert len(comments) == 3
            # Verify all comments are present (order may vary if created at same timestamp)
            contents = {c.content for c in comments}
            assert contents == {"Comment 1", "Comment 2", "Comment 3"}
    
    def test_get_comments_by_nonexistent_task(self, app):
        """Test retrieving comments for non-existent task"""
        with app.app_context():
            with pytest.raises(ValueError, match="Task with id 9999 not found"):
                CommentService.get_comments_by_task(9999)
    
    def test_get_comment_by_id(self, app, sample_task):
        """Test retrieving a comment by ID"""
        with app.app_context():
            created_comment = CommentService.create_comment(
                sample_task, "Test content", "Author"
            )
            
            retrieved_comment = CommentService.get_comment_by_id(created_comment.id)
            
            assert retrieved_comment is not None
            assert retrieved_comment.id == created_comment.id
            assert retrieved_comment.content == "Test content"
    
    def test_get_comment_by_id_not_found(self, app):
        """Test retrieving non-existent comment"""
        with app.app_context():
            comment = CommentService.get_comment_by_id(9999)
            assert comment is None
    
    def test_update_comment_content(self, app, sample_task):
        """Test updating comment content"""
        with app.app_context():
            comment = CommentService.create_comment(
                sample_task, "Original content", "Author"
            )
            
            updated_comment = CommentService.update_comment(
                comment.id,
                {'content': 'Updated content'}
            )
            
            assert updated_comment.content == "Updated content"
            assert updated_comment.author == "Author"
    
    def test_update_comment_author(self, app, sample_task):
        """Test updating comment author"""
        with app.app_context():
            comment = CommentService.create_comment(
                sample_task, "Content", "Original Author"
            )
            
            updated_comment = CommentService.update_comment(
                comment.id,
                {'author': 'New Author'}
            )
            
            assert updated_comment.author == "New Author"
            assert updated_comment.content == "Content"
    
    def test_update_comment_multiple_fields(self, app, sample_task):
        """Test updating multiple comment fields"""
        with app.app_context():
            comment = CommentService.create_comment(
                sample_task, "Original", "Original Author"
            )
            
            updated_comment = CommentService.update_comment(
                comment.id,
                {'content': 'New content', 'author': 'New Author'}
            )
            
            assert updated_comment.content == "New content"
            assert updated_comment.author == "New Author"
    
    def test_update_nonexistent_comment(self, app):
        """Test updating non-existent comment"""
        with app.app_context():
            with pytest.raises(ValueError, match="Comment with id 9999 not found"):
                CommentService.update_comment(9999, {'content': 'New'})
    
    def test_delete_comment(self, app, sample_task):
        """Test deleting a comment"""
        with app.app_context():
            comment = CommentService.create_comment(
                sample_task, "Content", "Author"
            )
            comment_id = comment.id
            
            result = CommentService.delete_comment(comment_id)
            
            assert result is True
            assert CommentService.get_comment_by_id(comment_id) is None
    
    def test_delete_nonexistent_comment(self, app):
        """Test deleting non-existent comment"""
        with app.app_context():
            with pytest.raises(ValueError, match="Comment with id 9999 not found"):
                CommentService.delete_comment(9999)
    
    def test_get_all_comments(self, app, sample_task):
        """Test retrieving all comments"""
        with app.app_context():
            # Create task 2
            task2 = Task(title="Task 2")
            db.session.add(task2)
            db.session.commit()
            
            # Create comments for different tasks
            CommentService.create_comment(sample_task, "Comment 1", "Author 1")
            CommentService.create_comment(task2.id, "Comment 2", "Author 2")
            CommentService.create_comment(sample_task, "Comment 3", "Author 3")
            
            all_comments = CommentService.get_all_comments()
            
            assert len(all_comments) == 3
