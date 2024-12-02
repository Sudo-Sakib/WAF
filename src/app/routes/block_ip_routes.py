from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import json

ip_blueprint = Blueprint('ip', __name__, template_folder="../../templates")

IP_BLOCKLIST_FILE = 'blocked_ips.json'

# Helper: Load or Initialize the JSON file
def load_blocklist():
    try:
        with open(IP_BLOCKLIST_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_blocklist(blocklist):
    with open(IP_BLOCKLIST_FILE, 'w') as file:
        json.dump(blocklist, file, indent=4)

# Route to render Block IP form
@ip_blueprint.route('/block-ip', methods=['GET', 'POST'])
def block_ip_form():
    if request.method == 'POST':
        ip_to_block = request.form.get('ip_address')
        blocklist = load_blocklist()

        if ip_to_block in blocklist:
            flash(f"IP {ip_to_block} is already blocked.", 'warning')
        else:
            blocklist.append(ip_to_block)
            save_blocklist(blocklist)
            flash(f"IP {ip_to_block} has been successfully blocked.", 'success')

        return redirect(url_for('ip.block_ip_form'))

    return render_template('admin/block_ip.html')

# API to get blocked IPs
@ip_blueprint.route('/api/blocked-ips', methods=['GET'])
def get_blocked_ips():
    blocklist = load_blocklist()
    return jsonify(blocklist)

@ip_blueprint.route('/api/delete-blocked-ip', methods=['DELETE'])
def delete_blocked_ip():
    data = request.get_json()
    ip_to_delete = data.get('ip')

    if not ip_to_delete:
        return jsonify({"error": "No IP provided"}), 400

    blocklist = load_blocklist()

    if ip_to_delete not in blocklist:
        return jsonify({"error": f"IP {ip_to_delete} not found in blocklist"}), 404

    blocklist.remove(ip_to_delete)
    save_blocklist(blocklist)

    return jsonify({"message": f"IP {ip_to_delete} has been unblocked"}), 200

