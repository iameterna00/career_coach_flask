import re
import json

def parse_booking_confirmation(text: str):
    """
    Extract lead info from bot reply JSON block.
    Returns a dictionary if found, else None.
    """
    pattern = re.compile(r"<<JSON>>(.*?)<<ENDJSON>>", re.DOTALL)
    match = pattern.search(text)
    if match:
        try:
            data = json.loads(match.group(1).strip())
            return data
        except json.JSONDecodeError:
            return None
    return None
