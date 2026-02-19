import os
import requests
from google import genai

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOOGLE_SEARCH_API_KEY or not GOOGLE_CX or not GEMINI_API_KEY:
    raise RuntimeError("Missing API keys. Set environment variables.")

client = genai.Client(api_key=GEMINI_API_KEY)


def google_search(query, top_k=3):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": GOOGLE_CX,
        "q": query,
        "num": top_k
    }

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    return [
        {
            "title": i.get("title", ""),
            "snippet": i.get("snippet", ""),
            "link": i.get("link", "")
        }
        for i in data.get("items", [])
    ]


def summarize_with_gemini(query, search_results):
    if not search_results:
        return "NOT FOUND"

    context = "\n\n".join(
        f"Title: {r['title']}\nContent: {r['snippet']}"
        for r in search_results
    )

    prompt = f"""
You are a factual summarizer.

RULES:
- Use ONLY the information below
- Do NOT add knowledge
- Do NOT infer
- If insufficient info, reply exactly: NOT FOUND

QUESTION:
{query}

INFORMATION:
{context}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception:
        return "NOT FOUND"


def search_and_answer(query):
    results = google_search(query)
    return summarize_with_gemini(query, results)
