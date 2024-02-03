# app/__init__.py
from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.user_routes import user_blueprint

def create_app():
    """
    Factory function to create the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for all routes
    CORS(app)

    # Register blueprints
    app.register_blueprint(user_blueprint)

    return app