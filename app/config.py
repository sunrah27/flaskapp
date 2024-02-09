from datetime import timedelta
import os

class Config:
    """
    Configuration class for Flask application.
    """
    DEBUG = True  # Set to False in production
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_COOKIE_SECURE = True  # Set to True in production (requires HTTPS)
    JWT_COOKIE_CSRF_PROTECT = False  # Set to True if you want CSRF protection

    # Set cookie expiration to match token expiration
    JWT_COOKIE_EXPIRES = timedelta(minutes=30)

    DOMAIN = os.getenv('DOMAIN')

connection = {
    'charset': "utf8mb4",
    'connect_timeout': 10,
    'database': os.getenv('DB_NAME'),
    'host': os.getenv('DB_HOST'),
    'password': os.getenv('DB_PASSWORD'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
}