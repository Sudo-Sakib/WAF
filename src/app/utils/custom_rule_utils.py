import os
import json

# File to store custom rules
CUSTOM_RULES_FILE = "custom_rules.json"

# Load custom rules
def load_custom_rules():
    if not os.path.exists(CUSTOM_RULES_FILE):
        return []
    with open(CUSTOM_RULES_FILE, "r") as file:
        return json.load(file)

# Save custom rules
def save_custom_rules(rules):
    with open(CUSTOM_RULES_FILE, "w") as file:
        json.dump(rules, file)
