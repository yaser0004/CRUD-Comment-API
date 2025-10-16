"""
Flask Application Factory
"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='development'):
    """
    Application factory pattern for creating Flask app instances
    
    Args:
        config_name: Configuration environment (development, testing, production)
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'testing':
        from config.settings import TestingConfig
        app.config.from_object(TestingConfig)
    elif config_name == 'production':
        from config.settings import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        from config.settings import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    from app.routes.comment_routes import comment_bp
    from app.routes.task_routes import task_bp
    
    app.register_blueprint(comment_bp, url_prefix='/api')
    app.register_blueprint(task_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Application is running'}, 200
    
    return app
