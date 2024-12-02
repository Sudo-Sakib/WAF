from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from app.utils.custom_rule_utils import load_custom_rules, save_custom_rules
import re

custom_rule_blueprint = Blueprint("custom_rule", __name__, url_prefix="/custom_rule", template_folder="../../../templates")

@custom_rule_blueprint.route("/custom_rule", methods=["GET"])
def custom_rule():
    """Display the custom rule dashboard."""
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("admin/custom_rule.html")

# Add a custom rule
@custom_rule_blueprint.route("/add_custom_rule", methods=["POST"])
def add_custom_rule():
    rule = {
        "name": request.form.get("name"),
        "pattern": request.form.get("pattern"),
        "description": request.form.get("description")
    }

    # Validate rule data
    if not rule["name"] or not rule["pattern"]:
        return jsonify({"error": "Rule name and pattern are required."}), 400
    try:
        re.compile(rule["pattern"])  # Validate regex
    except re.error:
        return jsonify({"error": "Invalid regex pattern."}), 400

    # Add rule to storage
    rules = load_custom_rules()
    rules.append(rule)
    save_custom_rules(rules)
    return jsonify({"message": "Rule added successfully."})

# Retrieve Custom Rules
@custom_rule_blueprint.route("/custom_rules", methods=["GET"])
def custom_rules():
    return jsonify({"rules": load_custom_rules()})

# Delete a Custom Rule
@custom_rule_blueprint.route("/delete_custom_rule", methods=["POST"])
def delete_custom_rule():
    index = int(request.form.get("index"))
    rules = load_custom_rules()
    if 0 <= index < len(rules):
        rules.pop(index)
        save_custom_rules(rules)
        return jsonify({"message": "Rule deleted successfully."})
    return jsonify({"error": "Invalid rule index."}), 400
