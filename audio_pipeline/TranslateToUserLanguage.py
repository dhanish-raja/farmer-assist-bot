import os
import requests
import sys

API_KEY = "SARVAM_AI_API_KEY"

if not API_KEY:
    print("Error: SARVAM_AI_API_KEY environment variable not set.")
    sys.exit(1)

url = "https://api.sarvam.ai/translate"

headers = {
    "api-subscription-key": API_KEY,
    "Content-Type": "application/json"
}

payload = {
    "input": "Leaf curl is caused by virus spread by whiteflies. Use neem oil spray and control vectors.",
    "source_language_code": "en-IN",
    "target_language_code": "te-IN"
}

try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    print("Status Code:", response.status_code)
    print("Response:", response.json())

except requests.exceptions.RequestException as e:
    print("Request failed:", e)
