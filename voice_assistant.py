import urllib.parse
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Initialize speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()
reminders = []
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# Initialize microphone recognition
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        speak("I am listening. Please speak.")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=7
            )

            command = recognizer.recognize_google(audio)

            print("You:", command)
            return command.lower()

        except sr.WaitTimeoutError:
            speak("I did not hear anything.")
            return ""

        except sr.UnknownValueError:
            speak("Sorry, I could not understand.")
            return ""

        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return ""
def check_reminders():
    current_time = datetime.datetime.now()

    for reminder in reminders[:]:
        if current_time >= reminder["time"]:
            speak("Reminder: " + reminder["message"])
            reminders.remove(reminder)
def process_command(command):

    if "hello" in command:
        speak("Hello! How can I help you?")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak("The current time is " + current_time)

    elif "date" in command:
        today = datetime.datetime.now().strftime("%d %B %Y")
        speak("Today's date is " + today)
    
    
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    
    elif "search for" in command:
        search_query = command.replace("search for", "", 1).strip()

        if search_query:
            speak("Searching Google for " + search_query)
            search_url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(search_query)
            webbrowser.open(search_url)
        else:
            speak("Please tell me what you want to search for.")
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "take a note" in command:
        note = command.replace("take a note", "", 1).strip()

        if note:
            with open("notes.txt", "a") as file:
                file.write(note + "\n")

            speak("Your note has been saved successfully.")
        else:
            speak("Please tell me what note you want to save.")
    
    elif "read my notes" in command:
        try:
            with open("notes.txt", "r") as file:
                notes = file.read()

            if notes.strip():
                speak("Here are your saved notes.")
                speak(notes)
            else:
                speak("Your notes file is empty.")

        except FileNotFoundError:
            speak("You have not saved any notes yet.")
    elif "remind me" in command:
        try:
            reminder_text, delay_text = command.split(" in ", 1)

            reminder_text = reminder_text.replace("remind me to", "").replace("remind me", "").strip()
            parts = delay_text.strip().split()

            if len(parts) >= 2 and parts[0].isdigit():
                minutes = int(parts[0])

                if minutes > 0 and reminder_text:
                    reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)

                    reminders.append({
                        "message": reminder_text,
                        "time": reminder_time
                    })

                    speak(f"Reminder set for {minutes} minutes.")
                else:
                    speak("Please provide a valid reminder.")
            else:
                speak("Please say the time in minutes.")

        except ValueError:
            speak("Please say: Remind me to drink water in 1 minute.")
    
    elif "bye" in command or "exit" in command:
        speak("Goodbye! Have a nice day.")
        return False

    else:
        speak("I don't know that command yet.")

    return True

# Main program
speak("Welcome to your AI Personal Assistant.")

while True:
    check_reminders()

    user_command = listen()

    check_reminders()

    if user_command:
        if not process_command(user_command):
            break
