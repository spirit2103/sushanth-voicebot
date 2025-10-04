from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def speech_to_text(audio_file_path):
    """
    audio_file_path: path to uploaded .wav or .mp3 file
    """
    with open(audio_file_path, "rb") as f:
        response = client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=f
        )
    return response.text
