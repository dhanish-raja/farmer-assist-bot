from preprocess import preprocess
from knowledge_base import knowledge_base


def preprocess_kb():
    for item in knowledge_base:
        item["processed_tokens"] = set(preprocess(item["question"]))

preprocess_kb()

def search_kb_by_intent(user_tokens, intent, min_score=2):
    best_match, best_score = None, 0

    for item in knowledge_base:
        if item["intent"] != intent:
            continue
        score = len(user_tokens & item["processed_tokens"])
        if score > best_score:
            best_score, best_match = score, item

    if best_match and best_score >= min_score:
        return {
            "intent": best_match["intent"],
            "crop": best_match["crop"],
            "answer": best_match["answer"],
            "confidence": best_score
        }
    return None

def search_kb_globally(user_tokens, min_score=1):
    best_match, best_score = None, 0

    for item in knowledge_base:
        score = len(user_tokens & item["processed_tokens"])
        if score > best_score:
            best_score, best_match = score, item

    if best_match and best_score >= min_score:
        return {
            "intent": best_match["intent"],
            "crop": best_match["crop"],
            "answer": best_match["answer"],
            "confidence": best_score
        }
    return None

