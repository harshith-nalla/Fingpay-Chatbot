import httpx, json, os
from typing import List

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("DISPOSITION_MODEL", "disposition-model")

def predict_disposition(intent_list: List[str]) -> str:
    prompt = f"Given these intents, predict final disposition:\n{json.dumps(intent_list, indent=2)}"
    try:
        with httpx.Client(timeout=60) as client:
            resp = client.post(OLLAMA_URL, json={"model": MODEL_NAME, "prompt": prompt, "stream": False})
            resp.raise_for_status()
            data = resp.json()
            return (data.get("response") or "").strip() or "unknown"
    except Exception as e:
        return f"[Error contacting disposition model: {e}]"
