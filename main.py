import requests
import torch
import time
from TTS.api import TTS
from datetime import datetime
from torch.serialization import add_safe_globals
from TTS.tts.configs.xtts_config import XttsConfig

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
        "model": "georgia:latest",
        "prompt": STORY_PROMPT,
        "stream": False,
        "options": {
            "temperature": 0,
            "top_p": 0,
            "max_tokens": 300
        }
    })
    return r.json().get("response")

def text_to_speech(text: str, file_path: str) -> None:
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
    tts.tts_to_file(text, speaker_wav=f"audio.wav", language="en", file_path=file_path)

if __name__ == "__main__":
    print("Generating story")
    story = generate_story()
    print(f"Generated\n\n{story}\n")
    print("Converting text to speech")
    date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_path = f"outputs/output-{date}.wav"
    text_to_speech(story, file_path)
    print(f"Done! Saved to {file_path}")
    time.sleep(1)
