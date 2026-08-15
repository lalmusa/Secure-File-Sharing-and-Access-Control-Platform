from functools import wraps
from flask import abort
from flask_login import current_user, login_required
from app.audit import log_action


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):

        if current_user.role != "admin":
            log_action(
                current_user.id,
                "Unauthorized admin access attempt"
            )
            abort(403)

        return f(*args, **kwargs)

    return decorated_function