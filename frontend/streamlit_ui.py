import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="SmartChat Scheduler", layout="centered")
st.title("📅 SmartChat Scheduler")

# --- Clear Chat Button ---
st.subheader("Preloaded Group Chat")
if st.button("🧼 Clear Chat"):
    res = requests.post(f"{API_URL}/clear")
    if res.status_code == 200:
        st.success("✅ Chat history cleared!")
    else:
        st.error("❌ Failed to clear chat.")

# --- Display Chat Messages ---
response = requests.get(f"{API_URL}/chats")
if response.status_code == 200:
    chats = response.json()
    for chat in chats:
        st.markdown(f"**{chat['user']}** ({chat['timestamp']}): {chat['message']}")
else:
    st.error("❌ Failed to load chats")

# --- Extracted Availability Display ---
st.markdown("---")
st.subheader("🕒 Extracted User Availability")
availability_res = requests.get(f"{API_URL}/availability")
if availability_res.status_code == 200:
    availability = availability_res.json()
    if availability:
        for user, slots in availability.items():
            st.write(f"**{user}**: {', '.join(slots)}")
    else:
        st.info("No availability info extracted yet.")
else:
    st.warning("Failed to fetch availability.")

# --- Show Clarifications ---
clarify_res = requests.get(f"{API_URL}/clarifications")
if clarify_res.status_code == 200 and clarify_res.json():
    st.markdown("---")
    st.subheader("⚠️ Clarifications Needed")
    for user, note in clarify_res.json().items():
        st.warning(f"**{user}**: {note}")

# --- Explanation of Slot Choice ---
st.markdown("---")
st.subheader("🔍 Why This Time?")
why_res = requests.get(f"{API_URL}/why-this-time")
if why_res.status_code == 200:
    data = why_res.json()
    chosen = data["chosen_slot"]
    counts = data["slot_counts"]
    if chosen:
        st.success(f"🕓 Proposed Time: **{chosen}**")
        st.markdown("**Vote breakdown:**")
        for slot, count in counts.items():
            st.write(f"• {slot}: {count} vote(s)")
    else:
        st.info("No time slot has enough agreement yet.")

# --- Confidence Meter ---
conf_res = requests.get(f"{API_URL}/confidence")
if conf_res.status_code == 200:
    conf_data = conf_res.json()
    st.subheader("📈 Scheduling Confidence")
    st.progress(conf_data["confidence_percent"] / 100.0)
    st.write(f"**Confidence:** {conf_data['confidence_percent']}% based on user agreement")

# --- Message Posting ---
st.markdown("---")
st.subheader("Post a New Message")

user_options = ["Harshal", "Komal", "Jaime", "Cersei"]
user = st.selectbox("Select user", user_options)
message = st.text_input("Your message")

if st.button("Send Message"):
    if message.strip():
        res = requests.post(f"{API_URL}/chat", json={"user": user, "message": message})
        if res.status_code == 200:
            st.success("✅ Message sent! Reload to see it above.")
        else:
            st.error("❌ Failed to send message.")
    else:
        st.warning("Message cannot be empty.")

# --- Schedule Meeting ---
st.markdown("---")
st.subheader("📆 Schedule Meeting")

if st.button("🧠 Schedule Now"):
    res = requests.post(f"{API_URL}/schedule")
    if res.status_code == 200:
        data = res.json()
        if "Meeting scheduled" in data["status"]:
            st.success(f"✅ {data['status']}")
            st.info(f"📧 Confirmation emails sent to: {', '.join(data['participants'])}")
        else:
            st.warning(data["status"])
    else:
        st.error("❌ Failed to schedule meeting.")
