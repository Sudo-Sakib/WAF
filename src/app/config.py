class Config:
    SECRET_KEY = "your-secret-key"
    WAF_MODE = "active"  # Can be 'active' or 'passive'

    # Blocklist: Deny access to these IPs
    BLOCKLIST = [
        "192.168.0.105",  # Example blocklisted IP
        "192.168.0.106"
    ]

    # Whitelist: Allow access only from these IPs (if whitelisting is enabled)
    WHITELIST_ENABLED = True  # Set to True to enable whitelisting
    WHITELIST = [
        "192.168.0.103",  # Example whitelisted IP
        "127.0.0.1"
    ]

    # Admin credentials (you can replace this with a database or more secure storage)
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "password"  # In practice, never store passwords as plain text
