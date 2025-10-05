from .base_adapter import BaseAdapter
from typing import Dict, Any
import asyncio
from src.utils import check_required

class MockFlashcard(BaseAdapter):
    """
    Mock Flashcard generator.
    Expects payload: {"topic": str, "count"/"num_questions": int}
    Returns: list of flashcards.
    """
    async def call(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0.06)

       
        ok, missing = check_required({"required": ["topic"]}, payload)
        if not ok:
            return {"error": f"Missing fields for flashcard_generator: {missing}"}

        topic = payload.get("topic", "general")
        count = payload.get("count") or payload.get("num_questions") or 5
        try:
            count = int(count)
        except Exception:
            count = 5
        count = min(count, 20)  

        flashcards = []
        for i in range(count):
            flashcards.append({
                "title": f"{topic} - card {i+1}",
                "question": f"What is {topic} concept {i+1}?",
                "answer": f"Answer for {topic} concept {i+1}.",
                "example": f"Example {i+1}"
            })
        return {"tool":"flashcard_generator","topic":topic,"flashcards":flashcards,"count":len(flashcards)}
