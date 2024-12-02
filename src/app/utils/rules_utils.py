import html
import re


def sql_injection_detection(payload):
    """Detect advanced SQL injection patterns in the given payload."""

    # Check for basic SQL keywords (select, insert, drop, union, etc.)
    basic_sql_pattern = r"(select|insert|update|delete|drop|union|or|and)\s+.*(from|set|into|values|where|order|group|having|like|in|limit|join)"

    # Check for SQL comments (used for obfuscation, e.g., '--', '/*', '*/')
    comment_pattern = r"(--|#|/\*|\*/)"

    # Check for SQL functions (e.g., CONCAT, SLEEP, VERSION)
    sql_function_pattern = r"(concat|group_concat|benchmark|sleep|ord|char|ascii|version|database|user|load_file|intooutfile)"

    # Check for time-based SQL injection (e.g., SLEEP, WAITFOR DELAY)
    time_based_pattern = r"(sleep|waitfor\s+delay)\s*\("

    # Check for SQL error-based injection (e.g., incorrect column count)
    error_based_pattern = r"select\s+\*\s+from\s+.*\s+limit\s+1,1"

    # Check for union-based injection (e.g., UNION SELECT)
    union_pattern = r"union\s+select\s+.*\s+from\s+.*\s+limit\s+\d+"

    # Check for blind SQL injection patterns (e.g., using "1=1" or "0=1")
    blind_pattern = r"(\d+\s*=\s*\d+|\d+\s*>\s*\d+|\d+\s*<\s*\d+)"

    # Combine all patterns
    combined_pattern = (
        f"{basic_sql_pattern}|"
        f"{comment_pattern}|"
        f"{sql_function_pattern}|"
        f"{time_based_pattern}|"
        f"{error_based_pattern}|"
        f"{union_pattern}|"
        f"{blind_pattern}"
    )

    # Use re.search to find any of the above patterns
    return bool(re.search(combined_pattern, payload, re.IGNORECASE))

def xss_detection(payload):
    """Detect advanced XSS patterns in the given payload."""
    # Decode HTML entities to detect obfuscated payloads
    decoded_payload = html.unescape(payload)

    # Check for basic <script> tags
    script_pattern = r"<script.*?>.*?</script.*?>"

    # Check for event handler attributes (e.g., onerror, onclick)
    event_handler_pattern = r"on\w+\s*=\s*['\"].*?['\"]"

    # Check for inline JavaScript (e.g., javascript:alert())
    inline_js_pattern = r"javascript\s*[:\w\W]*\("

    # Check for common dangerous HTML tags (e.g., iframe, img, svg)
    dangerous_html_tags = r"<(iframe|img|svg|object|embed|form).*?>"

    # Check for malicious JavaScript functions like eval(), setTimeout(), setInterval()
    js_function_pattern = r"(eval|setTimeout|setInterval)\s*\(.*\)"

    # Combine all patterns
    combined_pattern = f"{script_pattern}|{event_handler_pattern}|{inline_js_pattern}|{dangerous_html_tags}|{js_function_pattern}"

    # Use re.search to find any of the above patterns
    return bool(re.search(combined_pattern, decoded_payload, re.IGNORECASE))