from datetime import timedelta

class Config:
    """
    Configuration class for Flask application.
    """
    DEBUG = True  # Set to False in production
    SECRET_KEY = '9335d4f958c8b6694703556933d82e389647ef15bcd78b3abe5d6acbf07f3ec7'
    JWT_SECRET_KEY = '46d54bbbf94a9d201dcc4df7de307dcd8d8b71d7716a23f16e16b5cb4f971157'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_COOKIE_SECURE = True  # Set to True in production (requires HTTPS)
    JWT_COOKIE_CSRF_PROTECT = True  # Set to True if you want CSRF protection

    # Set cookie expiration to match token expiration
    JWT_COOKIE_EXPIRES = timedelta(minutes=30)

connection = {
    'charset': "utf8mb4",
    'connect_timeout': 10,
    'database': "testdb",
    'host': "mysql-c84cbdd-shanurislam-api.a.aivencloud.com",
    'password': "AVNS_KfXrQqgF7G0Yp3FXD2Z",
    'port': 19082,
    'user': "avnadmin",
}