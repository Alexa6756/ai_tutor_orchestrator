from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ConceptExplainerPayload(BaseModel):
    topic: str
    concept: Optional[str] = None
    difficulty: Optional[str] = "easy"
    user_info: Dict[str, Any] = Field(default_factory=dict)
    chat_history: List[Dict[str, str]] = Field(default_factory=list)
    explanation_style: Optional[str] = "detailed"
