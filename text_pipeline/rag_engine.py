from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from preprocess import preprocess
from knowledge_base import knowledge_base

rag_model = SentenceTransformer("all-MiniLM-L6-v2")

rag_questions = [" ".join(preprocess(item["question"])) for item in knowledge_base]
rag_answers = [item["answer"] for item in knowledge_base]
rag_embeddings = rag_model.encode(rag_questions)

def rag_chatbot(user_input, threshold=0.55):
    query = " ".join(preprocess(user_input))
    query_vec = rag_model.encode([query])
    scores = cosine_similarity(query_vec, rag_embeddings)[0]
    idx = np.argmax(scores)

    if scores[idx] >= threshold:
        return {
            "intent": "rag_retrieval",
            "crop": "none",
            "answer": rag_answers[idx],
            "confidence": float(scores[idx])
        }
    return None
