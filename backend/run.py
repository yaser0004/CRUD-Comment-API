"""
Flask application entry point
"""
import os
from app import create_app, db

# Create Flask application
app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("Database initialized successfully!")


@app.cli.command()
def seed_db():
    """Seed the database with sample data"""
    from app.models import Task, Comment
    
    # Create sample tasks
    task1 = Task(
        title="Implement user authentication",
        description="Add login and registration functionality"
    )
    task2 = Task(
        title="Create dashboard UI",
        description="Design and implement the main dashboard"
    )
    task3 = Task(
        title="Write API documentation",
        description="Document all API endpoints using Swagger"
    )
    
    db.session.add_all([task1, task2, task3])
    db.session.commit()
    
    # Create sample comments
    comments = [
        Comment(task_id=task1.id, content="Should we use JWT tokens?", author="Alice"),
        Comment(task_id=task1.id, content="Yes, JWT is a good choice", author="Bob"),
        Comment(task_id=task2.id, content="Consider using Material UI", author="Charlie"),
        Comment(task_id=task3.id, content="Swagger UI would be great", author="David"),
    ]
    
    db.session.add_all(comments)
    db.session.commit()
    
    print("Database seeded successfully!")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
