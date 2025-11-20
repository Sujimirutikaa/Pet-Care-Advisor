from flask import Flask
from config import Config
import os

def create_app(config_class=Config):
    """Application factory pattern for Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize knowledge base
    from app.models.knowledge_base import KnowledgeBase
    app.knowledge_base = KnowledgeBase()
    
    # Register blueprints
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app
