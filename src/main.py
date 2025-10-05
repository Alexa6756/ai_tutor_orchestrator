from dotenv import load_dotenv
import os
import datetime
import logging
import traceback
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.orchestrator import Orchestrator
from src.state_manager import StateManager

load_dotenv()

#
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_tutor_orchestrator")


app = FastAPI(
    title="AI Tutor Orchestrator (Demo)",
    description="Dynamic multi-tool orchestration for AI Tutor with scalable design and personalization.",
    version="0.2"
)


state = StateManager()
orch = Orchestrator()


class ChatInput(BaseModel):
    user_info: Dict[str, Any]
    chat_history: List[Dict[str, Optional[str]]]
    latest_message: str

class ToolPayload(BaseModel):
    payload: Dict[str, Any]
    confidence: float

class OrchestratorOutput(BaseModel):
    selected_tools: List[str]
    analysis: Dict[str, Any]
    payloads: Dict[str, ToolPayload]
    tool_responses: Dict[str, Any]
    clarify_question: Optional[str] = None


def calculate_confidence(chat_history: List[Dict[str, Optional[str]]], latest_message: str) -> float:
    """
    Example confidence: base 0.5, +0.1 for each keyword matched or message length.
    """
    base_conf = 0.5
    length_factor = min(len(latest_message) / 100, 0.2) if latest_message else 0
    keyword_factor = sum(0.05 for msg in chat_history if msg.get("content") and any(k in msg["content"].lower() for k in ["flashcard","note","explain"]))
    return min(base_conf + length_factor + keyword_factor, 0.95)


@app.post("/orchestrate", response_model=OrchestratorOutput)
async def orchestrate(inp: ChatInput):
    """
    Main endpoint: returns orchestration result including:
      - selected tools
      - extracted payloads
      - tool responses (mocked)
      - clarify_question (optional)
    """
    try:
        logger.info("Received input: %s", inp.dict())

        
        state.upsert_user(inp.user_info)
        logger.info("State updated for user: %s", inp.user_info.get("user_id"))

        
        result = await orch.handle_chat(inp.user_info, inp.chat_history, inp.latest_message)
        logger.info("Orchestration result: %s", result)

        return result

    except Exception as e:
        logger.error("Orchestrator error: %s", str(e))
        logger.debug(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "ORCHESTRATOR_FAILURE",
                "message": str(e),
                "trace": traceback.format_exc()
            }
        )

@app.post("/mock/{tool_name}")
async def mock_tool(tool_name: str, payload: Dict[str, Any]):
    """
    Exposed for manual testing; echoes payload for demonstration.
    """
    try:
        logger.info("🔹 Mock tool called: %s", tool_name)
        return {"tool": tool_name, "status": "ok", "echo": payload}
    except Exception as e:
        logger.error("Mock tool error (%s): %s", tool_name, str(e))
        logger.debug(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "MOCK_TOOL_FAILURE",
                "message": str(e),
                "trace": traceback.format_exc()
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
