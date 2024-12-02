import logging
import os
import html

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging to write to a file
logging.basicConfig(
    filename="logs/waf_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_request(ip, method, payload, result):
    """
    Log an incoming request with details.

    :param ip: IP address of the requester
    :param method: HTTP method (GET, POST, etc.)
    :param payload: Payload sent in the request
    :param result: WAF result (e.g., "SQL Injection detected")
    """
    sanitized_payload = html.escape(payload) if payload else "None"
    log_entry = f"IP: {ip} | Method: {method} | Payload: {sanitized_payload} | Result: {result}"
    logging.info(log_entry)




