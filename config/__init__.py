class BaseConfig(object):
    DEBUG = False
    TESTING = False

    GOOGLE_LOGIN_CLIENT_ID = "PUT_YOUR_OWN_LOGIN_CLIENT_ID.apps.googleusercontent.com"
    GOOGLE_LOGIN_CLIENT_SECRET = "PUT_YOUR_OWN_LOGIN_CLIENT_SECRET"
    SQLALCHEMY_DATABASE_URI = 'PUT_YOUR_OWN_DATABASE_URI'
    SECRET_KEY = "secret"
    GOOGLE_LOGIN_REDIRECT_SCHEME = "http",


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True