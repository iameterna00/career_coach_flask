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
        json_str = match.group(1).strip()

        # Split lines, strip, and fix missing commas
        lines = [line.rstrip() for line in json_str.splitlines() if line.strip()]
        fixed_lines = []
        for i, line in enumerate(lines):
            # Skip lines that already end with ',' or are the last line
            if not line.endswith(",") and i < len(lines) - 1:
                line += ","
            fixed_lines.append(line)

        json_fixed = "{\n" + "\n".join(fixed_lines) + "\n}"

        try:
            data = json.loads(json_fixed)
            return data
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            print("Fixed JSON string:\n", json_fixed)
            return None
    return None
