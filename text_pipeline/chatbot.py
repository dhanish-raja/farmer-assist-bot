from preprocess import preprocess
from intent_detection import detect_intent, INTENT_RULES
from kb_search import search_kb_by_intent, search_kb_globally
from rag_engine import rag_chatbot
from search_gemini import search_and_answer
from slot_config import INTENT_SLOTS, SLOT_QUESTIONS
from slot_extraction import extract_slots, extract_location
from state_manager import conversation_state, reset_state



def intent_generic_response(intent, confidence):
    return {
        "intent": intent,
        "crop": "none",
        "answer": INTENT_RULES[intent]["response"],
        "confidence": confidence
    }

def get_missing_slots(intent, filled_slots):
    required = INTENT_SLOTS.get(intent, [])
    return [s for s in required if s not in filled_slots]

def stateful_chatbot(user_input):
    global conversation_state

    user_tokens = set(preprocess(user_input))

    # 1. location extraction
    loc = extract_location(user_input)
    if loc:
        conversation_state["slots"]["location"] = loc

    # 2. slot extraction
    conversation_state["slots"].update(extract_slots(user_tokens))

    # 3. intent lock
    if not conversation_state["intent"]:
        intent, _ = detect_intent(user_tokens)
        if not intent:
            return "Sorry, I could not understand."
        conversation_state["intent"] = intent

    intent = conversation_state["intent"]

    # 4. slot gate
    missing = get_missing_slots(intent, conversation_state["slots"])
    if missing:
        return SLOT_QUESTIONS[missing[0]]

    # 5. build slot query
    slot_query = " ".join(conversation_state["slots"].values())
    slot_tokens = set(slot_query.split())

    # 6. KB
    kb_hit = search_kb_by_intent(slot_tokens, intent)
    if kb_hit:
        answer = kb_hit["answer"]
    else:
        generic = intent_generic_response(intent, 0)
        if generic and generic.get("answer"):
            answer = generic["answer"]
        else:
            rag_hit = rag_chatbot(slot_query)
            if rag_hit:
                answer = rag_hit["answer"]
            else:
                answer = search_and_answer(slot_query)

    # 7. reset
    conversation_state = reset_state()
    return answer


# =========================
# CHAT LOOP (STATEFUL → KB → RAG → GEMINI)
# =========================

def start_farmer_chatbot():
    print("Farmer Chatbot Started")
    print("Press 0 to exit\n")

    while True:
        user_input = input("Farmer: ").strip()

        if user_input == "0":
            print("Chatbot: Exiting")
            break

        answer = stateful_chatbot(user_input)
        print("Chatbot:", answer)

        
if __name__ == "__main__":
    start_farmer_chatbot()



