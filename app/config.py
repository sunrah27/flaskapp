class Config:
    """
    Configuration class for Flask application.
    """
    DEBUG = True  # Set to False in production
    SECRET_KEY = '9335d4f958c8b6694703556933d82e389647ef15bcd78b3abe5d6acbf07f3ec7'


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Perad303',
    'database': 'testdb',
}