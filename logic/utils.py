from functools import wraps
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS
from flask import (current_app, request)


def login_as_admin_required(func):    
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.logged_as_admin:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view
