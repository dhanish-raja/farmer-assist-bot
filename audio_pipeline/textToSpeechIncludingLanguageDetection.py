import requests
import pygame
import base64
import tempfile
import os

# ==============================
# 🔐 ADD YOUR SARVAM API KEY
# ==============================
API_KEY = "SARVAM_API_KEY"

HEADERS = {
    "api-subscription-key": API_KEY,
    "Content-Type": "application/json"
}

# ==============================
# 🎙 Supported TTS Languages (Official)
# ==============================

VOICE_MAP = {
    "en-IN": "en-IN-Standard-1",
    "hi-IN": "hi-IN-Standard-1",
    "bn-IN": "bn-IN-Standard-1",
    "gu-IN": "gu-IN-Standard-1",
    "kn-IN": "kn-IN-Standard-1",
    "ml-IN": "ml-IN-Standard-1",
    "mr-IN": "mr-IN-Standard-1",
    "od-IN": "od-IN-Standard-1",
    "pa-IN": "pa-IN-Standard-1",
    "ta-IN": "ta-IN-Standard-1",
    "te-IN": "te-IN-Standard-1"
}

# ==============================
# 🌍 Language Detection
# ==============================

def detect_language(text):
    url = "https://api.sarvam.ai/text-lid"

    payload = {
        "input": text
    }

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code != 200:
        print("Language Detection Error:", response.text)
        return "en-IN"

    result = response.json()

    print("Detection Response:", result)

    return result.get("language_code", "en-IN")


# ==============================
# 🔊 Text to Speech
# ==============================

def speak(text):

    # Step 1: Detect language
    lang_code = detect_language(text)
    print("Detected Language:", lang_code)

    # Step 2: Select voice
    voice = VOICE_MAP.get(lang_code)

    if not voice:
        print("Language not supported for TTS. Falling back to English.")
        voice = "en-IN-Standard-1"

    print("Selected Voice:", voice)

    # Step 3: Call TTS
    url = "https://api.sarvam.ai/text-to-speech"

    payload = {
        "text": text,
        "voice": voice,
        "format": "wav"   # WAV avoids mp3 corruption
    }

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code != 200:
        print("TTS Error:", response.text)
        return

    result = response.json()

    print("TTS Response Keys:", result.keys())

    # Sarvam returns: {"audios": ["base64string"]}
    audio_base64 = result.get("audios", [None])[0]

    if not audio_base64:
        print("Audio not found in response")
        return

    audio_bytes = base64.b64decode(audio_base64)

    # Step 4: Save temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_path = temp_audio.name

    # Step 5: Play audio
    pygame.mixer.init()
    pygame.mixer.music.load(temp_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.quit()

    os.remove(temp_path)


# ==============================
# 🚀 MAIN
# ==============================

if __name__ == "__main__":
    text = input("Enter text: ")
    speak(text)
