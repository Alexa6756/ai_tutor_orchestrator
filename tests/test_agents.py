from src.agents import TutorAgent

def test_tool_selection():
    agent = TutorAgent()
    chat_history = [{"role":"user","content":"I want 5 flashcards on photosynthesis"}]
    latest_message = "Easy level please"
    tools = agent.choose_tools(chat_history, latest_message)
    assert "flashcard_generator" in tools
