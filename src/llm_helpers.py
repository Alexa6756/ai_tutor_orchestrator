from typing import Dict, Any

def llm_stub(schema: Dict[str, Any], chat_history: list, latest_message: str, user_info: dict) -> Dict[str, Any]:
    """
    Basic LLM stub to generate payloads.
    """
    payload = {}
    payload['topic'] = latest_message.split()[0] if latest_message else "general"
    payload['user_info'] = user_info
    payload['chat_history'] = chat_history
    return payload
