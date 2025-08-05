import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
from ics_generator import generate_ics

# Real sender email credentials
SENDER_EMAIL = "harshalsoni694@gmail.com"
SENDER_PASSWORD = "bady tilv ivsf brjc"  # Use app-specific password or secure storage

def send_confirmation_email(meeting):
    subject = "📅 Meeting Confirmation - SmartChat Scheduler"
    body = f"""Hi team,

Your meeting is scheduled on **{meeting['datetime']}**.

Participants:
{', '.join(meeting['participants'])}

This invite includes a calendar file you can add.

Thanks,  
SmartChat Scheduler
"""

    # Generate .ics file content
    ics_content = generate_ics(meeting["datetime"], "Team Meeting", "Scheduled via SmartChat")

    for recipient in meeting['participants']:
        try:
            send_email_with_ics(recipient, subject, body, ics_content)
        except Exception as e:
            print(f"Failed to send email to {recipient}: {e}")

def send_email_with_ics(to_email, subject, body, ics_content):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Attach ICS file
    part = MIMEApplication(ics_content, Name="meeting.ics")
    part['Content-Disposition'] = 'attachment; filename="meeting.ics"'
    msg.attach(part)

    # Send
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
    server.quit()

    print(f"✅ Email sent to {to_email}")
