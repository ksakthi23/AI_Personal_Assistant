
import datetime
import webbrowser
import random

def assistant_response(command):
    command = command.lower().strip()

    if "hello" in command or "hi" in command:
        return "Hello! I am your personal assistant. How can I help you?"

    elif "your name" in command:
        return "I am your AI Personal Assistant."

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"

    elif "date" in command:
        today = datetime.datetime.now().strftime("%d %B %Y")
        return f"Today's date is {today}"

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    elif "joke" in command:
        jokes = [
            "Why did the computer go to the doctor? Because it had a virus!",
            "Why do programmers prefer dark mode? Because light attracts bugs!"
        ]
        return random.choice(jokes)

    elif "exit" in command or "bye" in command:
        return "Goodbye! Have a great day."

    else:
        return "Sorry, I don't understand that command yet."

print("===================================")
print("       AI PERSONAL ASSISTANT")
print("===================================")
print("Type 'exit' to close the assistant.")

while True:
    user_command = input("\nYou: ")

    response = assistant_response(user_command)

    print("Assistant:", response)

    if "exit" in user_command.lower() or "bye" in user_command.lower():
        break
