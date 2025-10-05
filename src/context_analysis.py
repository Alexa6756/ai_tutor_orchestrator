from typing import List, Dict, Any
import re


TOOL_KEYWORDS = {
    "note_maker": ["note", "notes", "summarize", "summarise", "summarize notes"],
    "flashcard_generator": ["flashcard", "flashcards", "flash card"],
    "concept_explainer": ["explanation", "explain simply", "what is", "understand", "explain"],
}

HELP_PATTERN = re.compile(
    r"help me with|i'm struggling with|i cant|i can't|i don't understand|i do not understand", 
    re.IGNORECASE
)

def analyze_context(chat_history: List[Dict[str, str]], latest_message: str) -> Dict[str, Any]:
    """
    Returns a dictionary with:
        - 'tools': suggested tools in priority order
        - 'detected_text': concatenated text from chat history + latest message
    """
    tools = set()
    
    
    text = " ".join([m.get("content", "") for m in (chat_history or [])] + [latest_message or ""]).strip().lower()
    
    
    for tool, keywords in TOOL_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                tools.add(tool)

    
    if HELP_PATTERN.search(text):
        tools.add("concept_explainer")

    
    ordered_tools = [t for t in ["concept_explainer", "flashcard_generator", "note_maker"] if t in tools]

    return {"tools": ordered_tools, "detected_text": text}
