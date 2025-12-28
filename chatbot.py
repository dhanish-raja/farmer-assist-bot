from preprocess import preprocess
from intent_detection import detect_intent, INTENT_RULES
from kb_search import search_kb_by_intent, search_kb_globally
from rag_engine import rag_chatbot
from search_gemini import search_and_answer


def intent_generic_response(intent, confidence):
    return {
        "intent": intent,
        "crop": "none",
        "answer": INTENT_RULES[intent]["response"],
        "confidence": confidence
    }


def rule_based_chatbot(user_input):
    user_tokens = set(preprocess(user_input))
    intent, score = detect_intent(user_tokens)

    if intent:
        hit = search_kb_by_intent(user_tokens, intent)
        if hit:
            return hit
        return intent_generic_response(intent, score)

    global_hit = search_kb_globally(user_tokens)
    if global_hit:
        return global_hit

    return {
        "intent": "fallback",
        "crop": "none",
        "answer": "Sorry, I could not understand your question.",
        "confidence": 0
    }


def start_farmer_chatbot():
    print("Farmer Chatbot Started")
    print("Press 0 to exit\n")

    while True:
        user_input = input("Farmer: ").strip()

        if user_input == "0":
            print("Chatbot: Exiting")
            break

        # 1️⃣ Try RULE-BASED chatbot
        response = rule_based_chatbot(user_input)

        if response["intent"] != "fallback":
            print("Chatbot:", response["answer"], "\n")
            print("By rule based chatbot")
            continue

        # 2️⃣ Try RAG chatbot
        rag_response = rag_chatbot(user_input)

        if rag_response:
            print("Chatbot:", rag_response["answer"], "\n")
            print("By RAG chatbot")
            continue

        ans = search_and_answer(user_input)
        if ans != "NOT FOUND":
            print("Chatbot:", ans, "\nBy search+gemini\n")
            continue

        # 3️⃣ Final fallback
        print("Chatbot: Sorry, I could not find an answer. Please give more details.\n")
        
if __name__ == "__main__":
    start_farmer_chatbot()


