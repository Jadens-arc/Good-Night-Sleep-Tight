import requests
import time
from TTS.api import TTS
from datetime import datetime
from torch.serialization import add_safe_globals
from TTS.tts.configs.xtts_config import XttsConfig
import os

add_safe_globals([XttsConfig])

STORY_PROMPT = """
Write a 50 word bedtime story.
Make it very original, whimsical, and completely different from every story you've wrote me in the past
Don't include any acknowledgements or suggestions.
Just give me the story by itself.
"""
OLLAMA_URL = "http://192.168.0.111:11434"

def generate_story() -> str:
    r = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": "gemma3:4b",
        "prompt": STORY_PROMPT,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 300
        }
    })
    return r.json().get("response")

def text_to_speech(text: str, file_path: str) -> None:
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
    tts.tts_to_file(text, speaker_wav=f"audio.wav", language="en", file_path=file_path)

if __name__ == "__main__":
    with open("generating_story.txt", "w") as f:
        f.write("Generating story...")
    print("Generating story")
    story = generate_story()
    print(f"Generated\n\n{story}\n")
    print("Converting text to speech")
    date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_path = f"static/outputs/output-{date}.wav"
    text_to_speech(story, file_path)
    print(f"Saved to {file_path}")
    print("Done!")
    print("Sleeping for 1 second to ensure all files are written")
    os.remove("generating_story.txt")
    time.sleep(1)
