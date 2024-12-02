# app/routes/test_routes.py
import re
from flask import Blueprint, request, jsonify, render_template
from app.utils.rules_utils import sql_injection_detection, xss_detection
from app.utils.csrf_utils import generate_csrf_token, validate_csrf_token
from app.utils.block_ip_utils import check_ip_access
from app.utils.logs_utils import log_request
from app.utils.custom_rule_utils import load_custom_rules
import html

# Define the blueprint
test_blueprint = Blueprint("test", __name__, url_prefix="/test", template_folder="../../templates")

@test_blueprint.route("/", methods=["GET", "POST"])
def handle_request():
    ip = request.remote_addr
    method = request.method
    payload = request.form.get("data") if method == "POST" else None

    # Load and check custom rules
    custom_rules = load_custom_rules()
    for rule in custom_rules:
        if re.search(rule["pattern"], payload or ""):
            log_request(ip, method, payload, f"Custom rule triggered: {rule['name']}")
            return jsonify({"error": f"Request blocked by custom rule: {rule['name']}"}), 400

    # Check IP access
    is_allowed, message = check_ip_access(ip)
    if not is_allowed:
        log_request(ip, method, payload, message)
        return jsonify({"error": message}), 403

    if method == "GET":
        # Pass CSRF Token to the template
        csrf_token = generate_csrf_token()
        return render_template("test.html", csrf_token=csrf_token)

    elif method == "POST":

        # Validate CSRF token
        csrf_token = request.form.get("_csrf_token")
        if not validate_csrf_token(csrf_token):
            log_request(ip, method, payload, "CSRF token invalid or missing")
            return jsonify({"error": "CSRF token invalid or missing"}), 403

        # Ensure payload is logged and sanitized
        sanitized_payload = html.escape(payload) if payload else ""

        # SQL Injection detection
        if sql_injection_detection(payload):
            log_request(ip, method, sanitized_payload, "SQL Injection detected")
            return jsonify({"error": "SQL Injection detected!"}), 400

        # XSS detection
        if xss_detection(payload):
            log_request(ip, method, sanitized_payload, "XSS detected")
            return jsonify({"error": "XSS detected!"}), 400

        # Safe request
        log_request(ip, method, sanitized_payload, "Request processed successfully")
        return jsonify({"message": "Request processed successfully."})
