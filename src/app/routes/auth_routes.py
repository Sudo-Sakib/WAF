# app/routes/auth_routes.py
from flask import Blueprint, request, session, flash, render_template, redirect, url_for
from app.utils.csrf_utils import generate_csrf_token, validate_csrf_token
from app.config import Config
from app import db, bcrypt
from app.models import User
from app.utils.auth_utils import is_password_strong

# Define the blueprint
auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth", template_folder="../../templates")

@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Handle the login page."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        csrf_token = request.form.get("_csrf_token")

        # Validate CSRF token
        if not validate_csrf_token(csrf_token):
            flash("Invalid CSRF token", "danger")
            return redirect(url_for("auth.login"))  # Correct blueprint name

        # Authenticate user
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session["username"] = username
            session["role"] = user.role  # Store role in the session
            session.modified=True
            flash("Login successful!", "success")

            # Debugging: Check if role is 'user' and confirm the redirect is happening
            print(f"Redirecting to user dashboard. Role: {session['role']}")

            # Redirect based on role
            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))  # Admin dashboard route
            else:
                return redirect(url_for("user.dashboard"))  # User dashboard route
        else:
            flash("Invalid username or password", "danger")

    return render_template("auth/login.html", csrf_token=generate_csrf_token())

# Logout Route
@auth_blueprint.route("/logout")
def logout():
    """Handle the logout functionality."""
    # Clear the user session
    session.clear()
    # Flash a logout success message (if needed)
    flash('You have been logged out successfully.', 'success')
    # Redirect to the login page
    return redirect(url_for("auth.login")) 

# Register Route
@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")  # Fetch role from the form
        csrf_token = request.form.get("_csrf_token")

        # Validate CSRF token
        if not validate_csrf_token(csrf_token):
            flash("Invalid CSRF token", "danger")
            return redirect(url_for("auth.register"))

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists!", "danger")
            return redirect(url_for("auth.register"))

        # Check password strength
        is_strong, message = is_password_strong(password)
        if not is_strong:
            flash(message, "danger")
            return redirect(url_for("auth.register"))
        
        # Hash the password and save the user
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, password=password_hash, role=role)
        db.session.add(new_user)
        db.session.commit()

        # Flash registration success only once
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    # Render the registration form
    return render_template("auth/register.html", csrf_token=generate_csrf_token())
