# app/__init__.py
from flask import Flask
from flask_jwt_extended import JWTManager
from app.config import Config

# Initialize Flask-JWT-Extended outside of the create_app function
jwt = JWTManager()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    # Initialize Flask-JWT-Extended
    jwt.init_app(app)

    # Import and register blueprints
    from app.user_routes import user_blueprint
    app.register_blueprint(user_blueprint)

    return app