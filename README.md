# Farmer Advisory Chatbot

A Python-based **hybrid agricultural advisory chatbot** designed to assist farmers with crop-related queries using a combination of **rule-based (intent-driven)** logic and **RAG (Retrieval-Augmented Generation)**–style semantic retrieval.

At present, the chatbot works fully offline using a structured knowledge base and sentence embeddings, making it suitable for low-connectivity environments.

---

## Features

- Rule-based intent detection (deterministic and fast)
- Knowledge-base driven answers for crops, pests, diseases, fertilizers, weather advice, schemes, etc.
- RAG-style semantic fallback using sentence embeddings
- Modular and scalable project structure
- CLI-based interaction (easy to extend to API / UI later)

---

## Architecture Overview

**Response flow:**

1. Rule-based intent detection  
2. Knowledge base search (intent-specific)  
3. Global knowledge base fallback  
4. RAG-based semantic retrieval  
5. Final fallback message  

This ensures high precision for known queries and flexibility for paraphrased or unseen inputs.

---

## Project Structure

