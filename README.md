# 🎤 VoiceBot

**VoiceBot** is an interactive voice assistant built using **Streamlit**, enabling users to engage in natural conversations through speech. The application captures audio input, processes it to extract text, and generates AI-driven responses, all within a user-friendly interface.

---

## 🛠 Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Speech Recognition:** `speech_recognition` library
- **Text-to-Speech:** `pyttsx3` or `gTTS`
- **Natural Language Processing:** OpenAI GPT-3.5 or Hugging Face Transformers
- **Audio Processing:** `pydub` (optional, for audio file handling)

---

## ✨ Features

- 🎙 **Voice Input:** Capture and process user speech in real-time.
- 🧠 **AI Responses:** Generate context-aware replies using advanced language models.
- 🖥️ **Streamlit Interface:** Intuitive and responsive web interface.
- 🔄 **Real-time Processing:** Immediate feedback after user input.
- 🛠️ **Customizable:** Easily extendable to integrate with various APIs and services.

---

## ⚙️ Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/spirit2103/sushanth-voicebot.git
cd sushanth-voicebot

### 2. Clone the Repository
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3.Install Dependecies
pip install -r requirements.txt

### 4. Run the Application
streamlit run app.py

###. access the app
http://localhost:8501
