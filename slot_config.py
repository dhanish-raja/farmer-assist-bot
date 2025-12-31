INTENT_SLOTS = {
    "fertilizer_advice": ["crop", "stage"],
    "pest_issue": ["crop", "symptom"],
    "market_price": ["crop", "location"],
    "weather_advice": ["location"],
    "govt_scheme": ["scheme_name"]
}

SLOT_QUESTIONS = {
    "crop": "Which crop?",
    "stage": "What is the growth stage?",
    "location": "Which location or mandi?",
    "symptom": "What symptoms are you observing?",
    "scheme_name": "Which scheme do you want information about?"
}
