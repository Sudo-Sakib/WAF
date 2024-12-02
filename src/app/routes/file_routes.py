# app/routes/file_routes.py
import re
from flask import Blueprint, request, jsonify, session
from app.utils.csrf_utils import validate_csrf_token
from app.utils.file_utils import allowed_file, inspect_file, detect_malicious_content
from app.utils.logs_utils import log_request
from app.config import Config
import os
from werkzeug.utils import secure_filename #FUV

# Define the blueprint
file_blueprint = Blueprint("file", __name__, url_prefix="/file")

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'txt', 'pdf'}  # Allowed file types
MAX_FILE_SIZE = 5 * 1024 * 1024  # Maximum file size (5MB)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@file_blueprint.route("/upload", methods=["POST"])
def upload_file():
    ip = request.remote_addr
    file = request.files.get('file')
    csrf_token = request.form.get("_csrf_token")

    # Validate CSRF token
    if not validate_csrf_token(csrf_token):
        log_request(ip, "UPLOAD", "None", "File Upload Security - CSRF token invalid or missing")
        return jsonify({"error": "CSRF token invalid or missing"}), 403

    if not file:
        log_request(ip, "UPLOAD", "None", "File Upload Security - No file uploaded")
        return jsonify({"error": "No file uploaded"}), 400

    filename = secure_filename(file.filename)

    # Check if file has an allowed extension
    if not allowed_file(filename):
        log_request(ip, "UPLOAD", filename, "File Upload Security - Disallowed file extension")
        return jsonify({"error": "Disallowed file extension"}), 400

    # Save file temporarily for inspection
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Check file size
    if os.stat(file_path).st_size > MAX_FILE_SIZE:
        os.remove(file_path)
        log_request(ip, "UPLOAD", filename, "File Upload Security - File size exceeds limit")
        return jsonify({"error": "File size exceeds limit"}), 400

    # Inspect MIME type
    mime_type = inspect_file(file_path)
    if mime_type not in ["image/jpeg", "image/png", "application/pdf", "text/plain"]:
        os.remove(file_path)
        log_request(ip, "UPLOAD", filename, f"File Upload Security - Suspicious MIME type: {mime_type}")
        return jsonify({"error": "Suspicious MIME type detected"}), 400

    # Detect malicious content
    if detect_malicious_content(file_path):
        os.remove(file_path)
        log_request(ip, "UPLOAD", filename, "File Upload Security - Malicious content detected")
        return jsonify({"error": "Malicious content detected"}), 400

    # Safe file upload
    log_request(ip, "UPLOAD", filename, "File Upload Security - File uploaded successfully")
    return jsonify({"message": "File uploaded successfully"})
