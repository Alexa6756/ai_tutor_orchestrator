import pytest
from src.orchestrator import Orchestrator

@pytest.mark.asyncio
async def test_basic_flow():
    orchestrator = Orchestrator()
    user_info = {
        "user_id": "user123",
        "name": "Alexa",
        "grade_level": "10",
        "learning_style": "visual",
        "emotional_state": "confused",
        "mastery_level": 2
    }
    chat_history = [
        {"role": "user", "content": "I want to learn photosynthesis"},
        {"role": "assistant", "content": "Sure! Do you want notes or flashcards?"},
        {"role": "user", "content": "Can you give me 5 flashcards?"}
    ]
    latest_message = "Easy"

    result = await orchestrator.handle_chat(user_info, chat_history, latest_message)
    
    assert "selected_tools" in result
    assert "payloads" in result
    assert "tool_responses" in result
    assert isinstance(result["selected_tools"], list)

    payload = result["payloads"].get("flashcard_generator", {}).get("payload", {})
    assert payload.get("user_info", {}).get("user_id") == "user123"
    assert "photosynthesis" in payload.get("topic", "").lower()

    if payload.get("difficulty") is None:
        assert "clarify_question" in result


@pytest.mark.asyncio
async def test_state_persistence():
    orchestrator = Orchestrator()
    user_info = {"user_id": "user123", "name": "Alexa", "mastery_level": 2}
    chat_history = [{"role": "user", "content": "I want notes on photosynthesis"}]

    result1 = await orchestrator.handle_chat(user_info, chat_history, "Easy")
    assert "clarify_question" in result1 or result1["tool_responses"]

    result2 = await orchestrator.handle_chat(user_info, chat_history, "Easy")
    assert result2["tool_responses"], "Tools should run without asking again"
