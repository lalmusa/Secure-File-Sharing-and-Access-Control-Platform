from functools import wraps
from flask import abort
from flask_login import current_user


def admin_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):

        if not current_user.is_authenticated:
            abort(401)

        if current_user.role != "admin":
            abort(403)

        return function(*args, **kwargs)

    return decorated_function