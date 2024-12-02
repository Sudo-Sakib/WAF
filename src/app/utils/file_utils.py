import os
import magic
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'txt', 'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def inspect_file(file_path):
    """Check MIME type of a file using magic library."""
    mime = magic.Magic(mime=True)
    return mime.from_file(file_path)

def detect_malicious_content(file_path):
    """Detect malicious content such as PHP tags or scripts in files."""
    try:
        with open(file_path, 'r', errors='ignore') as f:
            content = f.read()
            if "<?php" in content or "<script>" in content:
                return True
    except Exception as e:
        return False
    return False
