# app/routes/admin/admin_logs_routes.py
from flask import Blueprint, request, jsonify, session, url_for, redirect, render_template
import os
from datetime import datetime
import re
import json

# Define the blueprint
user_log_blueprint = Blueprint("user_logs", __name__, url_prefix="/logs", template_folder="../../../templates")


@user_log_blueprint.route("/user_logs_display", methods=["GET"])
def logs_display():
    """Display the dashboard, only accessible after login."""
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("user/user_logs.html")


@user_log_blueprint.route("/logs", methods=["GET"])
def get_logs():
    """Serve filtered log data for recent activity."""
    logs = []
    if os.path.exists("logs/waf_logs.txt"):
        with open("logs/waf_logs.txt", "r") as log_file:
            for line in log_file:
                parts = line.strip().split(" - ")
                if len(parts) == 2:
                    timestamp, details = parts
                    details_parts = details.split(" | ")
                    if len(details_parts) == 4:
                        logs.append({
                            "timestamp": timestamp,
                            "ip": details_parts[0].split(": ")[1],
                            "method": details_parts[1].split(": ")[1],
                            "payload": details_parts[2].split(": ")[1],
                            "result": details_parts[3].split(": ")[1],
                        })
    # Sort the logs by timestamp in descending order
    logs = sorted(logs, key=lambda x: datetime.strptime(x['timestamp'], "%Y-%m-%d %H:%M:%S"), reverse=True)
    return {"logs": logs}


@user_log_blueprint.route("/clear_logs", methods=["POST"])
def clear_logs():
    """Clear all logs from waf_logs.txt."""
    open("logs/waf_logs.txt", "w").close()  # Overwrite file with an empty file
    return {"message": "Logs cleared successfully."}


@user_log_blueprint.route("/api/logs-summary", methods=["GET"])
def logs_summary():
    import json
    import re

    logs = []
    custom_rules = []
    attack_counts = {
        "XSS Detected": 0,
        "SQL Injection Detected": 0,
        "CSRF Detected": 0,
        "File Upload Security": 0,
        "Custom Rule Triggered": 0,
    }
    blocked_attacks = 0
    allowed_requests = 0

    # Load logs from waf_logs.txt
    if os.path.exists("logs/waf_logs.txt"):
        with open("logs/waf_logs.txt", "r") as log_file:
            for line in log_file:
                logs.append(line.strip())

    # Load custom rules from custom_rules.json
    if os.path.exists("custom_rules.json"):
        with open("custom_rules.json", "r") as rules_file:
            custom_rules = json.load(rules_file)

    # Process logs and categorize them
    for log in logs:
        matched = False

        if "XSS" in log:
            attack_counts["XSS Detected"] += 1
            blocked_attacks += 1
            matched = True
        elif "SQL Injection" in log:
            attack_counts["SQL Injection Detected"] += 1
            blocked_attacks += 1
            matched = True
        elif "CSRF" in log:
            attack_counts["CSRF Detected"] += 1
            blocked_attacks += 1
            matched = True
        elif "File Upload Security" in log:
            attack_counts["File Upload Security"] += 1
            blocked_attacks += 1
            matched = True

        # Check against custom rules
        for rule in custom_rules:
            pattern = rule.get("pattern", "")
            if re.search(pattern, log, re.IGNORECASE):
                attack_counts["Custom Rule Triggered"] += 1
                blocked_attacks += 1
                matched = True
                break

        if not matched and "processed" in log.lower():
            allowed_requests += 1

    # Prepare summary data
    summary = {
        "attack_counts": [{"attack_type": k, "count": v} for k, v in attack_counts.items()],
        "blocked_attacks": blocked_attacks,
        "allowed_requests": allowed_requests,
    }
    return jsonify(summary)
