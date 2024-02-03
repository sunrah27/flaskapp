# app/constants.py
class UserCodes:
    """
    Class to store user-related status codes.
    """
    USER_REGISTERED = 2010
    USER_LOGGEDIN = 2011
    MISSING_CREDENTIALS = 4011
    INCORRECT_CREDENTIALS = 4012
    DUPLICATE_EMAIL = 4013
    DATABASE_CONNECTION_ERROR = 5001