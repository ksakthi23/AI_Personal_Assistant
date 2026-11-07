
import streamlit as st
import datetime
import webbrowser
import random
import urllib.parse
import pyttsx3
import sqlite3
import re

from streamlit_mic_recorder import speech_to_text
from streamlit_autorefresh import st_autorefresh

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Personal Assistant",
    page_icon="🤖",
    layout="wide"
)

# Refresh every 5 seconds
st_autorefresh(interval=5000, key="assistant_refresh")

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "messages": [],
    "voice_enabled": True,
    "voice_widget_id": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------------------------------
# DATABASE
# --------------------------------------------------

DB_NAME = "assistant.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                due_at TEXT NOT NULL,
                notified INTEGER DEFAULT 0
            )
        """)


initialize_database()

# --------------------------------------------------
# DATABASE FUNCTIONS
# --------------------------------------------------

def save_note(note):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO notes (content, created_at) VALUES (?, ?)",
            (note, datetime.datetime.now().isoformat())
        )


def get_notes():
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, content FROM notes ORDER BY id DESC"
        ).fetchall()


def clear_notes():
    with get_connection() as conn:
        conn.execute("DELETE FROM notes")


def save_reminder(message, due_time):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO reminders (message, due_at) VALUES (?, ?)",
            (message, due_time.isoformat())
        )


def get_reminders():
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, message, due_at FROM reminders "
            "WHERE notified = 0 ORDER BY due_at"
        ).fetchall()


def delete_reminder(reminder_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM reminders WHERE id = ?",
            (reminder_id,)
        )


def get_due_reminders():
    now = datetime.datetime.now().isoformat()

    with get_connection() as conn:
        due = conn.execute(
            "SELECT id, message FROM reminders "
            "WHERE due_at <= ? AND notified = 0",
            (now,)
        ).fetchall()

        for reminder_id, message in due:
            conn.execute(
                "UPDATE reminders SET notified = 1 WHERE id = ?",
                (reminder_id,)
            )

    return due


# --------------------------------------------------
# VOICE RESPONSE
# --------------------------------------------------

def speak(text):
    if not st.session_state.voice_enabled:
        return

    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception:
        pass


# --------------------------------------------------
# ASSISTANT COMMAND PROCESSING
# --------------------------------------------------

def assistant_response(command):

    original_command = command.strip()
    command = original_command.lower()

    if command in ["hello", "hi", "hey"] or command.startswith(
        ("hello ", "hi ", "hey ")
    ):
        return "Hello! How can I help you?"

    elif "your name" in command:
        return "I am your AI Personal Assistant."

    elif "time" in command:
        return datetime.datetime.now().strftime(
            "The current time is %I:%M %p"
        )

    elif "date" in command:
        return datetime.datetime.now().strftime(
            "Today's date is %d %B %Y"
        )

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    elif "search for" in command:
        query = original_command.lower().replace(
            "search for", "", 1
        ).strip()

        if query:
            url = (
                "https://www.google.com/search?q="
                + urllib.parse.quote_plus(query)
            )
            webbrowser.open(url)
            return "Searching Google for " + query

        return "Please tell me what to search for."

    elif "joke" in command:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why did the computer go to the doctor? It had a virus!",
            "Why was the computer cold? It left its Windows open!"
        ]
        return random.choice(jokes)

    # SAVE NOTES
    elif command.startswith("take a note"):
        note = original_command[len("take a note"):].strip()

        if note:
            save_note(note)
            return "Your note has been saved successfully."

        return "Please tell me what note to save."

    # READ NOTES
    elif "read my notes" in command:
        notes = get_notes()

        if notes:
            return "Your saved notes:\n" + "\n".join(
                [note[1] for note in notes]
            )

        return "You have not saved any notes yet."

    # CREATE REMINDERS
    elif "remind me to" in command:

        match = re.search(
            r"remind me to (.+) in (\d+) "
            r"(seconds?|minutes?|hours?)",
            command
        )

        if not match:
            return (
                "Please use this format: "
                "Remind me to drink water in 1 minute."
            )

        message = match.group(1).strip()
        amount = int(match.group(2))
        unit = match.group(3)

        if amount <= 0:
            return "Please enter a positive reminder time."

        if unit.startswith("second"):
            delay = datetime.timedelta(seconds=amount)
        elif unit.startswith("minute"):
            delay = datetime.timedelta(minutes=amount)
        else:
            delay = datetime.timedelta(hours=amount)

        due_time = datetime.datetime.now() + delay

        save_reminder(message, due_time)

        return (
            "Reminder saved successfully! "
            "I will remind you to " + message
        )

    elif "help" in command:
        return (
            "I can tell you the time and date, open websites, "
            "search Google, tell jokes, save notes and create reminders."
        )

    else:
        return "Sorry, I don't understand that command yet."


# --------------------------------------------------
# APP HEADER
# --------------------------------------------------

st.title("🤖 AI Personal Assistant")
st.caption("Your personal AI-powered productivity companion")

st.divider()

# --------------------------------------------------
# CHECK DUE REMINDERS
# --------------------------------------------------

due_reminders = get_due_reminders()

for reminder_id, message in due_reminders:
    st.warning("⏰ Reminder: " + message)
    speak("Reminder: " + message)

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

notes = get_notes()
reminders = get_reminders()

st.subheader("📊 Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Chat Messages",
        len(st.session_state.messages)
    )

with col2:
    st.metric("Saved Notes", len(notes))

with col3:
    st.metric("Active Reminders", len(reminders))

st.caption(
    "Current time: "
    + datetime.datetime.now().strftime("%d %B %Y | %I:%M %p")
)

st.divider()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    st.session_state.voice_enabled = st.toggle(
        "Enable voice responses",
        value=st.session_state.voice_enabled
    )

    st.divider()

    st.subheader("📝 Notes Management")

    if st.button("Clear All Notes"):
        clear_notes()
        st.success("All notes deleted.")
        st.rerun()

    st.divider()

    st.subheader("⏰ Reminder Management")

    reminders = get_reminders()

    if reminders:
        for reminder_id, message, due_at in reminders:

            st.write("🔔 " + message)

            due_time = datetime.datetime.fromisoformat(due_at)

            st.caption(
                "Due: " + due_time.strftime("%d %b %Y, %I:%M %p")
            )

            if st.button(
                "Delete",
                key=f"delete_reminder_{reminder_id}"
            ):
                delete_reminder(reminder_id)
                st.rerun()
    else:
        st.info("No active reminders.")

    st.divider()

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.subheader("💡 Available Commands")

    st.write("""
    - Hello
    - What is the time?
    - What is today's date?
    - Open YouTube
    - Open Google
    - Search for Python
    - Tell me a joke
    - Take a note Buy milk
    - Read my notes
    - Remind me to drink water in 1 minute
    - Help
    """)

# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

st.subheader("💬 Assistant Chat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --------------------------------------------------
# VOICE INPUT
# --------------------------------------------------

st.subheader("🎤 Voice Assistant")

voice_input = speech_to_text(
    start_prompt="🎤 Start Speaking",
    stop_prompt="⏹️ Stop Recording",
    language="en",
    use_container_width=True,
    key=f"voice_{st.session_state.voice_widget_id}"
)

# --------------------------------------------------
# TEXT INPUT
# --------------------------------------------------

text_input = st.chat_input("Type your command here...")

user_input = None

if text_input:
    user_input = text_input

elif voice_input:
    user_input = voice_input

# --------------------------------------------------
# PROCESS USER COMMAND
# --------------------------------------------------

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    response = assistant_response(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    speak(response)

    # Reset microphone widget to prevent duplicate commands
    if not text_input:
        st.session_state.voice_widget_id += 1

    st.rerun()
