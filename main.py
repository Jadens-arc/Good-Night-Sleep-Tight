import requests
import pyttsx3
import time
from datetime import datetime

STORY_PROMPT = """
Write a 200 word bedtime story.
Make it very original and random and whimsical
Don't include any acknowledgements or suggestions.
Just give me the story by itself.
"""

OLLAMA_URL = "http://192.168.0.111:11434"

def generate_story() -> str:
    r = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": "georgia:latest",
        "prompt": STORY_PROMPT,
        "stream": False
    })
    return r.json().get("response")

def text_to_speech(text: str, filepath: str, directory: str="outputs") -> None:
    engine = pyttsx3.init()
    engine.save_to_file(text, directory + "/" + filepath)
    try:
        engine.runAndWait()
    except:
        pass

if __name__ == "__main__":
    print("Generating story")
    story = generate_story()
    print(f"Generated\n\n{story}\n")
    print("Converting text to speech")
    date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_path = f"output-{date}.wav"
    text_to_speech(story, file_path)
    print(f"Done! Saved to {file_path}")
    time.sleep(1)
