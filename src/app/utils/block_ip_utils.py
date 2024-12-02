from app.config import Config
from datetime import datetime, timedelta
import json

IP_BLOCKLIST_FILE = 'blocked_ips.json'

def load_blocklist():
    try:
        with open(IP_BLOCKLIST_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def check_ip_access(ip):
    """Check if the client's IP is allowed or blocklisted."""
    blocklist = load_blocklist()

    if ip in blocklist:
        return False, "Your IP is blocklisted."

    if Config.WHITELIST_ENABLED and ip not in Config.WHITELIST:
        return False, "Your IP is not whitelisted."

    return True, ""