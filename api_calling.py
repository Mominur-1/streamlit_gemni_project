from google import genai
from gtts import gTTS
from dotenv import load_dotenv
import os, io
import json

# loading the environment variable

load_dotenv()

my_api_key = os.getenv("GEMINI_API_KEY")

# initializing a client
client = genai.Client(api_key=my_api_key)



# note Generator
def note_generator(images):

    prompt = """Sumarize the picture in not format at max 100 words. Make sure to add necessary markdown to differentiate different section"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[images, prompt]
    )
    return response.text


def audio_transcription(text):
    speech = gTTS(text, slow=False)
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    return audio_buffer


def quiz_generator(images, difficulty):
    prompt = f"""Generate 3 quizzes based on the {difficulty}. Make sure to add necessary markdown to differentiate the options. Add correct answer too, after the quiz"""
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[images, prompt]
    )
    return response.text
