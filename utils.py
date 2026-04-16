import re
from datetime import datetime, timedelta

def extract_time(text):
    """
    Extracts time information from a natural language string.
    Supported formats:
    - 'at 6pm', 'at 18:00'
    - 'in 5 minutes', 'in 2 hours'
    - 'tomorrow at 9am'
    """
    text = text.lower()
    now = datetime.now()
    
    # 1. "in X minutes/hours"
    in_match = re.search(r"in (\d+) (minute|hour)s?", text)
    if in_match:
        amount = int(in_match.group(1))
        unit = in_match.group(2)
        if "minute" in unit:
            return now + timedelta(minutes=amount)
        else:
            return now + timedelta(hours=amount)

    # 2. "tomorrow at X"
    tomorrow_match = re.search(r"tomorrow(?: at (\d+)(?::(\d+))?\s*(am|pm)?)?", text)
    if tomorrow_match:
        rem_time = now + timedelta(days=1)
        hour = tomorrow_match.group(1)
        if hour:
            h = int(hour)
            m = int(tomorrow_match.group(2)) if tomorrow_match.group(2) else 0
            period = tomorrow_match.group(3)
            if period == "pm" and h < 12: h += 12
            if period == "am" and h == 12: h = 0
            rem_time = rem_time.replace(hour=h, minute=m, second=0, microsecond=0)
        return rem_time

    # 3. "at X am/pm" or "at HH:MM"
    at_match = re.search(r"at (\d+)(?::(\d+))?\s*(am|pm)?", text)
    if at_match:
        h = int(at_match.group(1))
        m = int(at_match.group(2)) if at_match.group(2) else 0
        period = at_match.group(3)
        if period == "pm" and h < 12: h += 12
        if period == "am" and h == 12: h = 0
        
        rem_time = now.replace(hour=h, minute=m, second=0, microsecond=0)
        # If the time has already passed today, assume it's for tomorrow
        if rem_time < now:
            rem_time += timedelta(days=1)
        return rem_time

    return None

def extract_day(text):
    """Extracts day of the week from string."""
    text = text.lower()
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for day in days:
        if f"on {day}" in text or f"on {day[:3]}" in text:
            return day.capitalize()
    return None

def clean_task_text(text):
    """Remove time and day-related keywords from task description."""
    # Remove "on Monday", "on mon", etc.
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for day in days:
        text = re.sub(fr"\s*on\s+{day}s?", "", text, flags=re.IGNORECASE)
        text = re.sub(fr"\s*on\s+{day[:3]}s?", "", text, flags=re.IGNORECASE)
    
    keywords = [r"at \d+.*", r"in \d+.*", r"tomorrow.*"]
    for kw in keywords:
        text = re.sub(kw, "", text).strip()
    return text.strip()
