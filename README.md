# 📅 SmartChat Scheduler

**SmartChat Scheduler** is an AI-powered meeting scheduling web app that reads chat messages, intelligently extracts user availability, and automatically schedules a meeting when a majority agrees on a time.

Built as part of a technical assessment, this project demonstrates NLP logic, backend API design, real-time availability extraction, and email automation — without relying on pre-trained ML models.

---

## 🔧 Tech Stack

### 💻 Frontend
- **Streamlit** — Python-based web interface for displaying chat, availability, and actions
- **Requests (HTTP)** — API communication with FastAPI backend

### 🧠 Backend
- **FastAPI** — Handles chat APIs, availability extraction, and scheduling logic
- **Uvicorn** — ASGI server to serve FastAPI

### ✉️ Email Integration
- **Python Email (SMTP)** — Sends confirmation emails with `.ics` calendar invites
- **Custom `.ics` generator** — Allows users to "Add to Calendar"

### ⚙️ NLP Logic
- Custom **rule-based NLP** in Python (no external ML/LLM)
- Uses **regular expressions** and **heuristics** to detect:
  - Intent ("I am free...")
  - Day + time availability
  - Clarification needs (e.g., missing time)

---

## 🧠 Scheduling Logic (How It Works)

> Smart, interpretable logic — no black-box ML.

1. **Chat Collection**:
   - Users send chat messages via the UI
   - Messages are tagged with timestamps and usernames

2. **Availability Extraction**:
   - Regex extracts weekdays (`monday`, `tuesday`, etc.)
   - Regex also detects time (`12 PM`, `4:30 pm`, etc.)
   - If user says "everyday", it maps to all 7 days
   - If time is missing, assumes **default 12 PM**
   - Invalid or ambiguous times trigger **clarification flags**

3. **Majority Rule Scheduling**:
   - All extracted availability slots are counted
   - The slot with the most votes is proposed
   - Meeting is scheduled only if **majority (>=50%) agree**

4. **Confidence Calculation**:
   - Confidence = (# of votes for top slot / total users) × 100
   - Shown to user for transparency

5. **Email Notification**:
   - Once scheduled, all users receive:
     - Confirmation email
     - Calendar invite (`.ics`) file to auto-add to calendar apps

---

## 🎯 Features

✅ Multi-user group chat (preloaded or real-time)  
✅ Availability detection from natural language  
✅ Clarification prompt if user input is incomplete  
✅ Vote-based meeting scheduling logic  
✅ Visual display of confidence and slot breakdown  
✅ Confirmation email with `.ics` calendar invite  

---

## 🧪 Sample Use Case

### Chat Messages:
Harshal: I am free on Monday at 12 PM
Komal: I am free on Monday at 12 PM
Jaime: I am free on Monday at 12 PM
Cersei: I am free on Tuesday at 12 PM


### Output:
- 🕓 **Scheduled**: Monday at 12 PM
- ✅ Majority: 3 of 4 users
- 📧 Confirmation email sent to all
- 📎 Includes `.ics` calendar file

---

## 🖥️ Screenshots (Coming Soon)
- Chat UI
- Availability summary
- Vote explanation
- Email sample

---

## 💬 Preloaded Users
- Harshal
- Komal
- Jaime
- Cersei

---

## 🚧 Deployment Plan

This project will be deployed using:
- **Backend**: Render.com (FastAPI)
- **Frontend**: Streamlit Cloud

Live links will be added once deployed.

---

## 📌 Future Enhancements
- Use OpenAI GPT-4o API for deeper NLP parsing
- Connect to Google Calendar API
- Replace in-memory storage with MongoDB or PostgreSQL
- Add user authentication
- Real-time chat support (WebSocket)

---

## 👨‍💻 Built by

**Harshal Soni**  
📧 harshalsoni694@gmail.com  