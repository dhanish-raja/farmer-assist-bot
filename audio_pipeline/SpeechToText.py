import os
import requests
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import time
import sys

API_KEY = "SARVAM_AI_API_KEY"

if not API_KEY:
    print("Error: SARVAM_AI_API_KEY not set.")
    sys.exit(1)

# ==============================
# 🎤 RECORD AUDIO (Stop after 3s silence)
# ==============================

SAMPLE_RATE = 16000
SILENCE_THRESHOLD = 0.01
SILENCE_DURATION = 3  # seconds


def record_audio(filename="recorded.wav"):
    print("Speak now...")

    audio_buffer = []
    silence_start = None

    def callback(indata, frames, time_info, status):
        nonlocal silence_start

        volume = np.sqrt(np.mean(indata**2))
        audio_buffer.append(indata.copy())

        if volume < SILENCE_THRESHOLD:
            if silence_start is None:
                silence_start = time.time()
            elif time.time() - silence_start > SILENCE_DURATION:
                raise sd.CallbackStop()
        else:
            silence_start = None

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            callback=callback
        ):
            while True:
                time.sleep(0.1)
    except sd.CallbackStop:
        pass

    audio_data = np.concatenate(audio_buffer, axis=0)
    wav.write(filename, SAMPLE_RATE, audio_data)

    print("Recording saved:", filename)


# ==============================
# 🌍 SEND TO SARVAM STT (Translate Mode)
# ==============================

def transcribe_audio(filename="recorded.wav"):
    url = "https://api.sarvam.ai/speech-to-text"

    headers = {
        "api-subscription-key": API_KEY
    }

    files = {
        "file": ("recorded.wav", open(filename, "rb"), "audio/wav")
    }

    data = {
        "model": "saaras:v3",
        "mode": "translate"
    }

    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()

        print("Status Code:", response.status_code)
        result = response.json()
        print("Response:", result)

        transcript = result.get("transcript")

        if transcript:
            print("\nTranscript:")
            print(transcript)
        else:
            print("Transcript not found in response.")

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


# ==============================
# 🚀 MAIN
# ==============================

if __name__ == "__main__":
    record_audio()
    transcribe_audio()
