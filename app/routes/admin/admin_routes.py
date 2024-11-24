from flask import Blueprint, render_template, session, redirect, url_for

admin_blueprint = Blueprint("admin", __name__, template_folder="../../../templates")

@admin_blueprint.route("/dashboard")
def dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("auth.login"))
    return render_template("admin/admin_dashboard.html")
