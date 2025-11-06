import httpx, json
from typing import List, Dict

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "gemma3"

_conversation_history: Dict[str, List[Dict[str, str]]] = {}

def call_llm(system_prompt: str, user_message: str, session_id: str = "default") -> str:
    messages = [{"role": "system", "content": system_prompt}]
    history = _conversation_history.setdefault(session_id, [])
    history.append({"role": "user", "content": user_message})
    messages.extend(history)

    payload = {"model": MODEL_NAME, "messages": messages, "stream": False}

    try:
        with httpx.Client(timeout=60) as client:
            resp = client.post(OLLAMA_URL, json=payload)
            resp.raise_for_status()
            data = resp.json()
            reply = (data.get("message", {}).get("content") or "").strip()
    except Exception as e:
        reply = f"[LLM ERROR] {e}"

    history.append({"role": "assistant", "content": reply})
    return reply
