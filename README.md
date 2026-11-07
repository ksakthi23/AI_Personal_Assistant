
#  AI Personal Assistant Using Python

## 📌 Project Overview
AI Personal Assistant is a Python-based application designed to simplify everyday tasks through voice commands and text-based interaction.

It provides features such as web searching, note management, reminders, date and time information, and voice responses through an interactive Streamlit interface.

##  Features
- Voice input and text-based interaction
- Text-to-speech responses
- Current date and time
- Open Google and YouTube
- Google search
- Random jokes
- Save and read personal notes
- Create and manage reminders
- Automatic reminder checking
- Interactive Streamlit dashboard

## Technologies Used
- Python
- Streamlit
- Speech Recognition
- PyAudio
- pyttsx3
- SQLite
- Requests

## 📂 Project Structure

```text
AI_Personal_Assistant/
├── app.py
├── assistant.py
├── ai_engine.py
├── commands.py
├── voice_assistant.py
├── assistant.db
├── notes.txt
├── requirements.txt
└── data/
```

## Installation

### 1. Clone the repository

```bash
git https://github.com/ksakthi23/projects.git
```

### 2. Open the project folder

```bash
cd AI_Personal_Assistant
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
```

### 4. Activate the environment

Mac/Linux:

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

## Future Enhancements
- AI-powered conversational responses
- Persistent reminder notifications
- Improved speech recognition
- Personalized assistant settings
- Integration with external APIs

## 👨‍💻 Author
Developed as a Python internship project.
