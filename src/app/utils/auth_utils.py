from bcrypt import hashpw, gensalt, checkpw
import re

def hash_password(password):
    """Hash the password using bcrypt."""
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

def check_password(password, hashed_password):
    """Verify a password against a hash."""
    return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def is_password_strong(password):
    """Check if the password is strong."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must include at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must include at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must include at least one digit"
    if not re.search(r"[!@#$%^&*]", password):
        return False, "Password must include at least one special character (!@#$%^&*)"
    return True, ""