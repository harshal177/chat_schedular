# ics_generator.py
from datetime import datetime, timedelta

def generate_ics(meeting_datetime: str, title: str, description: str) -> str:
    dt = datetime.strptime(meeting_datetime, "%A at %I:%M %p")
    today = datetime.today()
    
    # Adjust to the next occurrence of the specified weekday
    while dt.weekday() != today.weekday():
        today += timedelta(days=1)
        if dt.strftime("%A") == today.strftime("%A"):
            break

    dt_final = today.replace(hour=dt.hour, minute=dt.minute, second=0, microsecond=0)
    dt_end = dt_final + timedelta(hours=1)  # Assume 1-hour meeting

    dt_format = "%Y%m%dT%H%M%S"

    ics = f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
DTSTAMP:{datetime.utcnow().strftime(dt_format)}
DTSTART:{dt_final.strftime(dt_format)}
DTEND:{dt_end.strftime(dt_format)}
SUMMARY:{title}
DESCRIPTION:{description}
LOCATION:Online
STATUS:CONFIRMED
SEQUENCE:0
BEGIN:VALARM
TRIGGER:-PT15M
DESCRIPTION:Reminder
ACTION:DISPLAY
END:VALARM
END:VEVENT
END:VCALENDAR"""
    return ics
