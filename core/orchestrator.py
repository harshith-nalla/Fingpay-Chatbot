from core.intent_classifier import IntentClassifier
from core.llm_module import call_llm
from core.static_data import *
from core.disposition_model import predict_disposition
from typing import Dict, Any
import json, inspect
from collections import defaultdict

classifier = IntentClassifier()

# session-aware stores
_conversation_history: Dict[str, list] = defaultdict(list)
_intent_list: Dict[str, list] = defaultdict(list)

def build_system_prompt(intent_name: str, retrieved_data: Dict[str, Any] | None = None,
                        off_domain: bool = False) -> str:
    """Build system prompt for the LLM"""
    if off_domain:
        return """
You are a helpful financial assistant LLM.

Rules for off-domain queries:
1) If the user asks anything outside financial/payment context, answer in ONE factual sentence if possible.
2) After answering, immediately bring the conversation back to loans, EMI, or payments.
3) Keep your response polite, concise, and professional.
4) Do not use any structured data for off-domain queries.

Respond in plain text.
""".strip()
    else:
        return f"""
You are a helpful financial assistant LLM. Follow these rules strictly:

1) Use ONLY the structured information in `retrieved_data` below to answer user queries.
2) If user asks something outside available data, politely say you don't have that info.
3) For chit-chat, gently bring the conversation back to loans/profile.
4) If user requests a human, acknowledge and suggest next steps.

CURRENT_INTENT: {intent_name}
retrieved_data (JSON):
{json.dumps(retrieved_data or {}, indent=2)}
""".strip()

def classify_message(user_input: str) -> Dict[str, Any]:
    classification = classifier.classify(user_input)
    return {
        "text": user_input,
        "intent": classification["chosen_intent"],
        "confidence": classification["confidence"],
        "handler": classification["handler"]
    }

def process_user_query(user_input: str, session_id: str = "default") -> Dict[str, Any]:
    print("Processing user input:", user_input)

    if user_input.strip().lower() in ["end", "finish", "bye", "done", "thankyou", "thank you"]:
        intents_list = [msg["intent"] for msg in _conversation_history[session_id] if "intent" in msg]
        print("Conversation history: ", _conversation_history[session_id])
        final_disp = predict_disposition(intents_list)
        _conversation_history.pop(session_id, None)
        _intent_list.pop(session_id, None)
        return {
            "reply": f"Conversation ended. Final disposition: {final_disp}",
            "intent": "end_conversation",
            "disposition": final_disp
        }

    msg_data = classify_message(user_input)
    _conversation_history[session_id].append(msg_data)
    _intent_list[session_id].append(msg_data["intent"])

    intent = msg_data["intent"]
    handler = msg_data["handler"]

    if intent != "other":
        # safely call handler (with or without user_input)
        try:
            retrieved_data = handler(user_input)
        except TypeError:
            retrieved_data = handler()
        off_domain = False
        system_prompt = build_system_prompt(intent, retrieved_data, off_domain)
    else:
        system_prompt = build_system_prompt(intent_name=intent, off_domain=True)

    llm_reply = call_llm(system_prompt, user_input)

    return {"reply": llm_reply, "intent": intent, "disposition": "in_progress"}
