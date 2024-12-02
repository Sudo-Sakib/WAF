import secrets
from flask import session
import os

def generate_csrf_token():
    token = session.get("_csrf_token")
    if not token:
        token = os.urandom(24).hex()
        session["_csrf_token"] = token
    return token

def validate_csrf_token(token):
    """Validate the CSRF token submitted with the request."""
    return token == session.get("_csrf_token")
