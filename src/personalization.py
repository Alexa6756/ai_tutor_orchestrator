from typing import Dict

def adjust_for_mastery(tool_name: str, payload: Dict, mastery_level: int) -> Dict:
    try:
        mastery_level = int(mastery_level)
    except (ValueError, TypeError):
        
        mastery_level = 3
    """
    Dynamically adapts tool parameters based on mastery level.
    - mastery_level: 1 (beginner) to 10 (expert)
    """
    
    if tool_name == "flashcard_generator":
        if mastery_level <= 3:
            payload["difficulty"] = "easy"
            payload["count"] = min(payload.get("count", 5), 5)
        elif mastery_level <= 6:
            payload["difficulty"] = "medium"
            payload["count"] = min(payload.get("count", 10), 10)
        else:
            payload["difficulty"] = "hard"
            payload["count"] = payload.get("count", 15)

    
    elif tool_name == "note_maker":
        if mastery_level <= 3:
            payload["note_taking_style"] = "outline"
        elif mastery_level <= 6:
            payload["note_taking_style"] = "bullet_points"
        else:
            payload["note_taking_style"] = "structured"

    
    elif tool_name == "concept_explainer":
        if mastery_level <= 3:
            payload["desired_depth"] = "basic"
        elif mastery_level <= 6:
            payload["desired_depth"] = "intermediate"
        elif mastery_level <= 9:
            payload["desired_depth"] = "advanced"
        else:
            payload["desired_depth"] = "comprehensive"

    return payload


def adjust_for_emotion(tool_name: str, payload: Dict, emotional_state: str) -> Dict:
    """
    Adapts payload parameters based on emotional state.
    Options: focused, anxious, confused, tired
    """
    state = emotional_state.lower()
    if tool_name == "flashcard_generator":
        if state == "confused":
            payload["count"] = min(payload.get("count", 5), 5)  
            payload["difficulty"] = "easy"
        elif state == "focused":
            payload["count"] = max(payload.get("count", 5), 10)
        elif state == "tired":
            payload["count"] = min(payload.get("count", 5), 3)
            payload["difficulty"] = "easy"

    elif tool_name == "note_maker":
        if state == "confused":
            payload["include_examples"] = True
            payload["include_analogies"] = True
        elif state == "focused":
            payload["include_examples"] = True
        elif state == "tired":
            payload["note_taking_style"] = "outline"

    elif tool_name == "concept_explainer":
        if state == "confused":
            payload["desired_depth"] = "basic"
        elif state == "focused":
            payload["desired_depth"] = payload.get("desired_depth", "intermediate")
        elif state == "tired":
            payload["desired_depth"] = "basic"

    return payload


def adjust_for_learning_style(tool_name: str, payload: Dict, learning_style: str) -> Dict:
    """
    Adjust payload according to preferred learning style.
    Options: visual, auditory, kinesthetic, reading/writing
    """
    style = learning_style.lower()
    if tool_name == "flashcard_generator":
        if style == "visual":
            payload["include_examples"] = True
        elif style == "kinesthetic":
            payload["include_examples"] = True
        elif style == "auditory":
            payload["include_examples"] = False

    elif tool_name == "note_maker":
        if style == "visual":
            payload["include_analogies"] = True
        elif style == "auditory":
            payload["note_taking_style"] = "narrative"
        elif style == "reading/writing":
            payload["note_taking_style"] = "bullet_points"
        elif style == "kinesthetic":
            payload["note_taking_style"] = "structured"

    elif tool_name == "concept_explainer":
        if style == "visual":
            payload["desired_depth"] = payload.get("desired_depth", "intermediate")
        elif style == "auditory":
            payload["desired_depth"] = "basic"
        elif style == "kinesthetic":
            payload["desired_depth"] = "intermediate"

    return payload
