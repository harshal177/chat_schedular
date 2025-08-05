from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from chat_nlp import extract_availability, propose_meeting_time
from email_utils import send_confirmation_email

app = FastAPI()

# In-memory DB
chats_db = []
meetings_db = []
clarifications_db = {}
raw_availability_db = {}

class Message(BaseModel):
    user: str
    message: str

@app.post("/chat")
def add_message(msg: Message):
    timestamp = datetime.now().isoformat()
    chats_db.append({"user": msg.user, "message": msg.message, "timestamp": timestamp})
    return {"status": "Message saved"}

@app.get("/chats")
def get_chats():
    return chats_db

@app.post("/clear")
def clear_chat():
    chats_db.clear()
    meetings_db.clear()
    clarifications_db.clear()
    raw_availability_db.clear()
    return {"status": "Chat and meeting data cleared"}

@app.get("/availability")
def get_user_availability():
    user_msgs = {}
    for entry in chats_db:
        user = entry["user"]
        msg = entry["message"]
        user_msgs.setdefault(user, []).append(msg)

    availability, clarifications, raw_slots = extract_availability(user_msgs)
    clarifications_db.update(clarifications)
    raw_availability_db.update(raw_slots)
    return availability

@app.get("/clarifications")
def get_clarifications():
    return clarifications_db

@app.get("/why-this-time")
def explain_time_choice():
    user_msgs = {}
    for entry in chats_db:
        user = entry["user"]
        msg = entry["message"]
        user_msgs.setdefault(user, []).append(msg)

    availability, _, _ = extract_availability(user_msgs)
    final_slot, counts, _ = propose_meeting_time(availability)
    return {
        "chosen_slot": final_slot,
        "slot_counts": counts
    }

@app.get("/confidence")
def get_confidence():
    user_msgs = {}
    for entry in chats_db:
        user = entry["user"]
        msg = entry["message"]
        user_msgs.setdefault(user, []).append(msg)

    availability, _, _ = extract_availability(user_msgs)
    final_slot, _, confidence = propose_meeting_time(availability)
    return {
        "slot": final_slot,
        "confidence_percent": confidence
    }

@app.post("/schedule")
def schedule_meeting():
    user_msgs = {}
    for entry in chats_db:
        user = entry["user"]
        msg = entry["message"]
        user_msgs.setdefault(user, []).append(msg)

    print("\n>>> Incoming messages per user:")
    for u, msgs in user_msgs.items():
        print(f"{u}: {msgs}")

    availability, clarifications, _ = extract_availability(user_msgs)

    print("\n>>> Extracted availability:")
    for u, slots in availability.items():
        print(f"{u}: {slots}")

    final_slot, vote_counts, confidence = propose_meeting_time(availability)

    print(f"\n>>> Final proposed slot: {final_slot}")
    print(f">>> Vote breakdown: {vote_counts}")
    print(f">>> Confidence: {confidence}%")

    if not availability:
        return {"status": "❌ No availability extracted. Please check the chat messages."}

    if not final_slot:
        return {
            "status": "❌ Could not schedule meeting. No slot had majority agreement.",
            "votes": vote_counts,
            "confidence": confidence
        }

    meeting = {
        "datetime": final_slot,
        "participants": [
            "harshalsoni694@gmail.com",
            "komal@example.com",
            "jaime@example.com",
            "cersei@example.com"
        ]
    }

    meetings_db.append(meeting)
    send_confirmation_email(meeting)

    return {
        "status": f"✅ Meeting scheduled on {final_slot}",
        "participants": meeting["participants"],
        "votes": vote_counts,
        "confidence": confidence
    }
