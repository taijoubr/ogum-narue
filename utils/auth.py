import os
import functools
import secrets
from datetime import timedelta
from flask import session, redirect, url_for, request, current_app, g
from models.user_level import UserLevel


def init_app(app):
    app.config.setdefault("PERMANENT_SESSION_LIFETIME", timedelta(hours=2))
    app.config.setdefault("SESSION_COOKIE_HTTPONLY", True)
    app.config.setdefault("SESSION_COOKIE_SECURE", False)


def login_required(view):
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def role_required(level_value):
    def decorator(view):
        @functools.wraps(view)
        def wrapped(*args, **kwargs):
            lvl = session.get("user_level")
            if not lvl:
                return redirect(url_for("admin_login", next=request.path))
            # programador bypass
            if lvl == UserLevel.PROGRAMADOR.value:
                return view(*args, **kwargs)
            if lvl != level_value and level_value != "ANY":
                return redirect(url_for("admin_access_denied"))
            return view(*args, **kwargs)

        return wrapped

    return decorator


def programador_required(view):
    return role_required(UserLevel.PROGRAMADOR.value)(view)


def admin_required(view):
    return role_required(UserLevel.ADMINISTRADOR.value)(view)


def secretaria_required(view):
    return role_required(UserLevel.SECRETARIA.value)(view)


def tesouraria_required(view):
    return role_required(UserLevel.TESOURARIA.value)(view)


def generate_csrf_token():
    token = session.get("_csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["_csrf_token"] = token
    return token


def validate_csrf(token):
    return token and token == session.get("_csrf_token")
