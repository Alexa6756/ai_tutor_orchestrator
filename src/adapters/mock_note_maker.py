from .base_adapter import BaseAdapter
from typing import Dict, Any
import asyncio
from src.utils import check_required

class MockNoteMaker(BaseAdapter):
    """
    Mock Note Maker adapter.
    Expects payload: {"topic": str, optional other fields}
    Returns: notes with title, summary, and sections.
    """
    async def call(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0.08)

        
        ok, missing = check_required({"required": ["topic"]}, payload)
        if not ok:
            return {"error": f"Missing fields for note_maker: {missing}"}

        topic = payload.get("topic", "unknown topic")
        title = f"Notes on {topic.title()}"
        summary = f"Short summary for {topic} (auto-generated)."
        note_sections = [
            {"title":"Overview", "content": f"Overview of {topic}", "key_points":["kp1","kp2"], "examples":["ex1"]}
        ]
        return {
            "tool": "note_maker",
            "topic": topic,
            "title": title,
            "summary": summary,
            "note_sections": note_sections
        }
