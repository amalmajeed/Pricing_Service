import functools        # Used to tell the decorated function the name and documentation of the original function


from typing import Callable
from flask import session, flash, redirect, url_for, current_app


def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('email'):
            flash("You need to be logged in for this page ! ", "danger")
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)
    return decorated_function


def requires_admin(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('email') != current_app.config.get('ADMIN', ''):
            # To check if the session email is same as current apps env ADMIN , else use '' by default
            flash("You need to be an administrator for access to this page ! ", "danger")
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)
    return decorated_function
