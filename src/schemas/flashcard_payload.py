from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class FlashcardPayload(BaseModel):
    topic: str
    difficulty: Optional[str] = "easy"
    count: int = 5
    num_questions: Optional[int] = None
    question_type: Optional[str] = "practice"
    subject: Optional[str] = None
    user_info: Dict[str, Any] = Field(default_factory=dict)
    chat_history: List[Dict[str, str]] = Field(default_factory=list)
    note_taking_style: Optional[str] = "structured"
