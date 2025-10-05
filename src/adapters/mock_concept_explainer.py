from .base_adapter import BaseAdapter
from typing import Dict, Any
import asyncio
from src.utils import check_required

class MockConceptExplainer(BaseAdapter):
    """
    Mock Concept Explainer adapter.
    Expects payload: {"concept_to_explain"/"topic": str, optional "desired_depth"}
    Returns: explanation, examples, practice questions.
    """
    async def call(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0.07)

        
        ok, missing = check_required({"required": ["concept_to_explain"]}, payload)
        if not ok:
            
            payload["concept_to_explain"] = payload.get("topic", "concept")

        concept = payload.get("concept_to_explain") or payload.get("topic") or "concept"
        depth = payload.get("desired_depth", "basic")

        explanation = f"A {depth} explanation of {concept}."
        examples = [f"Example illustrating {concept}"]
        practice = [f"Practice Q: Explain {concept} in your own words."]

        return {
            "tool": "concept_explainer",
            "concept": concept,
            "explanation": explanation,
            "examples": examples,
            "practice_questions": practice
        }
