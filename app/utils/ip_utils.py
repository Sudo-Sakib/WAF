from app.config import Config
from datetime import datetime, timedelta

def check_ip_access(ip):
    """Check if the client's IP is allowed or blocklisted."""
    # Check blocklist
    if ip in Config.BLOCKLIST:
        return False, "Your IP is blocklisted."

    # Check whitelist if enabled
    if Config.WHITELIST_ENABLED and ip not in Config.WHITELIST:
        return False, "Your IP is not whitelisted."

    return True, ""
