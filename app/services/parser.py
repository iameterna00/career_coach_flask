
import re
import json
import os

def parse_booking_confirmation(text: str):
    """
    Extract lead info from bot reply JSON block.
    Handles:
    - leading/trailing commas
    - missing braces
    - extra braces
    Returns a dictionary if parsing succeeds, else None.
    """
    # Extract <<JSON>> block
    pattern = re.compile(r"<<JSON>>(.*?)<<ENDJSON>>", re.DOTALL)
    match = pattern.search(text)
    if not match:
        return None

    content = match.group(1).strip()

    # Remove any leading commas
    content = re.sub(r'^\s*,+', '', content)
    # Remove any trailing commas
    content = re.sub(r',+\s*$', '', content)
    # Ensure wrapped in braces
    if not content.startswith("{"):
        content = "{\n" + content + "\n}"
    if not content.endswith("}"):
        content = content + "\n}"

    # Remove trailing commas before closing brace
    content = re.sub(r',(\s*})', r'\1', content)

    # Remove any repeated opening braces
    content = re.sub(r'^\{+', '{', content)
    # Remove any repeated closing braces
    content = re.sub(r'\}+$', '}', content)

    try:
        data = json.loads(content)
        return data
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        print("Problematic JSON string:\n", content)
        return None

