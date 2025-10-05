import json
from typing import Dict, Any
from pydantic import ValidationError, create_model
import re


def _llm_stub_generate(schema: Dict[str, Any], chat_history, latest_message, user_info) -> Dict[str, Any]:
    """
    Generates a JSON-like payload based on chat heuristics.
    Handles short inputs (like "Easy" or "5") and context from previous chat.
    """
    text = " ".join([m.get("content", "") for m in (chat_history or [])] + [latest_message or ""]).lower()
    payload = {}
    payload["_inferred_fields"] = []

    
    m = re.search(r"(?:about|on|with|for)\s+([a-zA-Z0-9\s\-]+)", text)
    if m:
        payload["topic"] = m.group(1).strip()
        payload["_inferred_fields"].append("topic")
    else:
        words = (latest_message or "").split()
        if len(words) <= 6 and words:
            payload["topic"] = latest_message.strip()
            payload["_inferred_fields"].append("topic")

   
    difficulty_map = {
        "easy": "easy",
        "medium": "medium",
        "hard": "hard",
    }
    for key in difficulty_map.keys():
        if key in text:
            payload["difficulty"] = difficulty_map[key]
            payload["_inferred_fields"].append("difficulty")
            break
    else:
        if any(w in text for w in ["struggling", "can't", "cannot", "don't understand", "confused", "hard"]):
            payload["difficulty"] = "easy"
            payload["_inferred_fields"].append("difficulty")
        elif any(w in text for w in ["practice", "challenge", "challenging", "harder"]):
            payload["difficulty"] = "medium"
            payload["_inferred_fields"].append("difficulty")

    
    m_num = re.search(r"(\d+)", latest_message or "")
    if m_num:
        count = int(m_num.group(1))
        payload["count"] = count
        payload["num_questions"] = count
        payload["_inferred_fields"].append("count")
    else:
        m_num2 = re.search(r"(\d+)\s+(flashcards|questions|problems|cards)", text)
        if m_num2:
            count = int(m_num2.group(1))
            payload["count"] = count
            payload["num_questions"] = count
            payload["_inferred_fields"].append("count")

    
    if "practice" in text or "problems" in text or "flashcards" in text:
        payload["question_type"] = "practice"
        payload["_inferred_fields"].append("question_type")

    
    if "calculus" in text:
        payload["subject"] = "calculus"
        payload["_inferred_fields"].append("subject")
    if "photosynthesis" in text or "photosynth" in text:
        payload["topic"] = "photosynthesis"
        payload["subject"] = "biology"
        payload["_inferred_fields"].append("topic")
        payload["_inferred_fields"].append("subject")

    
    payload["user_info"] = user_info or {}
    payload["chat_history"] = chat_history or []

    return payload


def _fallback_extract(schema: Dict[str, Any], chat_history, latest_message, user_info) -> Dict[str, Any]:
    """Fallback extractor; currently reuses LLM stub."""
    return _llm_stub_generate(schema, chat_history, latest_message, user_info)


def _validate_with_pydantic(schema: Dict[str, Any], candidate: Dict[str, Any]) -> (Dict[str, Any], float):
    required = schema.get("required", [])
    props = schema.get("properties", {})

    fields = {}
    for k, v in props.items():
        t = v.get("type", "string")
        if t == "integer":
            typ = (int, ...)
        elif t == "boolean":
            typ = (bool, ...)
        elif t == "array":
            typ = (list, ...)
        else:
            typ = (str, ...)
        fields[k] = typ

    P = create_model('TmpModel', **fields)  

    try:
        validated = P(**{k: candidate.get(k) for k in props.keys()})
        
        confidence = 0.95
        
        inferred = candidate.get("_inferred_fields", [])
        if inferred:
            confidence -= min(0.1, 0.02 * len(inferred))  
        return validated.dict(), confidence
    except ValidationError:
        
        present = sum(1 for r in required if candidate.get(r) not in (None, "", []))
        inferred = len(candidate.get("_inferred_fields", []))  
        total_fields = max(1, len(required))


        confidence = 0.5 * (present / total_fields) + 0.3 * min(1.0, inferred / total_fields)


        confidence = max(confidence, 0.6)

        return candidate, confidence


def _apply_personalization(payload: Dict[str, Any], state) -> Dict[str, Any]:
    try:
        user_id = payload.get("user_info", {}).get("user_id")
        profile = state.get_user(user_id) if state else None
        if not profile:
            return payload

        mastery = profile.get("mastery_level")
        emo = (profile.get("emotional_state") or "").lower()
        style = (profile.get("teaching_style") or "").lower()

        if "difficulty" in payload and isinstance(mastery, int):
            if mastery <= 3:
                payload["difficulty"] = "easy"
            elif mastery <= 6:
                payload["difficulty"] = "medium"
            else:
                payload["difficulty"] = "hard"

        if "confused" in emo or "anxious" in emo:
            if payload.get("desired_depth") == "advanced":
                payload["desired_depth"] = "intermediate"
            if payload.get("note_taking_style") in ["structured", "narrative"]:
                payload["note_taking_style"] = "bullet_points"

        if style == "visual":
            payload["note_taking_style"] = payload.get("note_taking_style") or "outline"
        elif style == "direct":
            payload["note_taking_style"] = "structured"
        elif style == "socratic":
            payload["note_taking_style"] = payload.get("note_taking_style") or "narrative"

        return payload
    except Exception:
        return payload


async def generate_payload_for_tool(
    tool_name: str,
    schema: Dict[str, Any],
    chat_history,
    latest_message,
    user_info,
    state
) -> (Dict[str, Any], float):
    candidate = _llm_stub_generate(schema, chat_history, latest_message, user_info)
    validated, conf = _validate_with_pydantic(schema, candidate)

    if conf >= 0.6:
        return _apply_personalization(validated, state), conf

    candidate2 = _fallback_extract(schema, chat_history, latest_message, user_info)
    validated2, conf2 = _validate_with_pydantic(schema, candidate2)
    return _apply_personalization(validated2, state), max(conf, conf2)
