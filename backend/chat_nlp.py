import re
from typing import Dict, List, Tuple, Optional
from collections import Counter
from datetime import datetime

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DEFAULT_TIME = "12:00 PM"

# Extracts structured availability + clarifications
def extract_availability(user_messages: Dict[str, List[str]]) -> Tuple[Dict[str, List[str]], Dict[str, str], Dict[str, List[str]]]:
    availability = {}
    clarifications = {}
    raw_slots = {}

    for user, messages in user_messages.items():
        slots = []
        unclear = False
        for msg in messages:
            msg_l = msg.lower()
            if any(x in msg_l for x in ["free", "available", "can meet"]):
                days = re.findall(r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday|everyday)', msg_l)
                times = re.findall(r'(\d{1,2}(:\d{2})?\s?(am|pm))', msg_l)

                if 'everyday' in days:
                    days = DAYS

                selected_time = times[0][0] if times else DEFAULT_TIME
                    # Normalize format: convert "12pm" → "12:00 PM"
                if ":" not in selected_time:
                    selected_time = selected_time.replace("am", ":00 AM").replace("pm", ":00 PM")
                else:
                    selected_time = selected_time.upper()

                # Remove any accidental space between numbers and colon
                selected_time = re.sub(r"\s*:\s*", ":", selected_time)

                


                if not times:
                    unclear = True  # Mark this user for follow-up

                for day in days:
                    slot = f"{day.capitalize()} at {selected_time.upper()}"
                    slots.append(slot)

        if slots:
            availability[user] = slots
            raw_slots[user] = slots

        if unclear:
            clarifications[user] = "Missing specific time info. Please clarify what time you are available."

    return availability, clarifications, raw_slots

# Picks majority slot + computes explanation and confidence
def propose_meeting_time(avail: Dict[str, List[str]]) -> Tuple[Optional[str], Dict[str, int], float]:
    all_slots = []
    for slots in avail.values():
        all_slots.extend(slots)

    if not all_slots:
        return None, {}, 0.0

    count = Counter(all_slots)
    total_users = len(avail)
    best_slot, freq = count.most_common(1)[0]

    confidence = round((freq / total_users) * 100, 2)
    return best_slot, dict(count), confidence
