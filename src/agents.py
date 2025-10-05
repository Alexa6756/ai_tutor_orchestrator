from dotenv import load_dotenv
import os
from typing import List, Dict, Any


from langchain_openai import OpenAI


load_dotenv()


class TutorAgent:
    """
    The core agent for the AI Tutor orchestrator.
    Handles LLM initialization and tool selection.
    """

    def __init__(self, llm=None):
        """
        Initialize the LLM. If llm is provided, use it; otherwise, create an OpenAI instance.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if llm:
            self.llm = llm
        else:
            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY not set. Please set it in your environment or .env file."
                )
            self.llm = OpenAI(temperature=0.5, openai_api_key=api_key)

    def choose_tools(
        self, chat_history: List[Dict[str, str]], latest_message: str
    ) -> List[str]:
        """
        Decide which tools to use based on chat history and latest message.
        Simple keyword-based selection; can be extended with LangGraph or RAG.
        """
        text = " ".join([m.get("content") or "" for m in chat_history] + [latest_message or ""]).lower()
        tools = []

        if "flashcard" in text:
            tools.append("flashcard_generator")
        if "note" in text or "notes" in text:
            tools.append("note_maker")
        if "explain" in text or "concept" in text:
            tools.append("concept_explainer")

        return tools

    