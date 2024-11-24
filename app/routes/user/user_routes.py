# user_routes.py
from flask import Blueprint, render_template, session, redirect, url_for, flash

user_blueprint = Blueprint("user", __name__, template_folder="../../../templates")

@user_blueprint.route("/dashboard")
def dashboard():
    # Ensure the user is logged in and has the "user" role
    if session.get("role") != "user":
        flash("Unauthorized access! Please log in as a user.", "danger")
        return redirect(url_for("auth.login"))  # Correct blueprint name
    return render_template("user/user_dashboard.html")
