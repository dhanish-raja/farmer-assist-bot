from preprocess import preprocess

INTENT_RULES = {
    "greeting": {
        "keywords": ["hi", "hello", "namaste", "hey"],
        "response": "Hello! How can I help you with farming today?"
    },
    "weather_advice": {
        "keywords": ["weather", "rain", "rainfall", "temperature"],
        "response": "Please tell your location to get the weather forecast."
    },
    "market_price": {
        "keywords": ["price", "rate", "mandi", "market"],
        "response": "Tell me the crop name and mandi location."
    },
    "pest_issue": {
        "keywords": ["pest", "insect", "disease", "spots", "worms"],
        "response": "Please tell the crop name and symptoms."
    },
    "fertilizer_advice": {
        "keywords": ["fertilizer", "urea", "dap", "npk"],
        "response": "Tell me the crop name and growth stage."
    },
    "govt_scheme": {
        "keywords": ["scheme", "subsidy", "loan", "insurance"],
        "response": "Which government scheme information do you need?"
    }
}

def detect_intent(user_tokens, threshold=3):
    best_intent, best_score = None, 0

    for intent, rule in INTENT_RULES.items():
        rule_tokens = set()
        for kw in rule["keywords"]:
            rule_tokens.update(preprocess(kw))

        score = len(user_tokens & rule_tokens)
        if score > best_score:
            best_score, best_intent = score, intent

    if best_score >= threshold:
        return best_intent, best_score
    return None, 0

