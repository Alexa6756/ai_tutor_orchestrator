from typing import Dict, Any, Optional
import threading
import re
from datetime import datetime

class StateManager:
    """
    In-memory state store for demo purposes.
    Supports context tracking, personalization, and adaptive parameters.
    """
    DEFAULT_EMOTIONAL_STATE = "Focused"
    DEFAULT_LEARNING_STYLE = "Direct"
    DEFAULT_MASTERY_LEVEL = 1
    DEFAULT_TEACHING_STYLE = "Direct"

    def __init__(self):
        self._lock = threading.Lock()
        self._store: Dict[str, Dict[str, Any]] = {}

    def upsert_user(self, user_info: Dict[str, Any]):
        if not user_info:
            return
        uid = user_info.get("user_id")
        if not uid:
            return

        with self._lock:
            now = self._store.get(uid, {})
            mastery_level = self._parse_mastery(user_info.get("mastery_level_summary") or user_info.get("mastery_level"))
            now.update({
                "user_id": uid,
                "name": user_info.get("name"),
                "grade_level": user_info.get("grade_level"),
                "learning_style": user_info.get("learning_style_summary") or user_info.get("learning_style") or self.DEFAULT_LEARNING_STYLE,
                "emotional_state": user_info.get("emotional_state_summary") or user_info.get("emotional_state") or self.DEFAULT_EMOTIONAL_STATE,
                "mastery_level": mastery_level or self.DEFAULT_MASTERY_LEVEL,
                "teaching_style": user_info.get("teaching_style") or self.DEFAULT_TEACHING_STYLE,
                "last_interaction": datetime.utcnow(),
                "recent_tools": now.get("recent_tools", []),
                "conversation_history": now.get("conversation_history", [])
            })
            self._store[uid] = now

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self._store.get(user_id)

    def update_emotional_state(self, user_id: str, state: str):
        with self._lock:
            user = self._store.get(user_id)
            if user:
                user["emotional_state"] = state
                user["last_interaction"] = datetime.utcnow()

    def update_mastery_level(self, user_id: str, level: int):
        with self._lock:
            user = self._store.get(user_id)
            if user:
                user["mastery_level"] = level
                user["last_interaction"] = datetime.utcnow()

    def add_tool_usage(self, user_id: str, tool_name: str):
        with self._lock:
            user = self._store.get(user_id)
            if user:
                tools = user.get("recent_tools", [])
                tools.append({"tool": tool_name, "timestamp": datetime.utcnow()})
                
                user["recent_tools"] = tools[-10:]
                user["last_interaction"] = datetime.utcnow()

    def add_conversation(self, user_id: str, role: str, content: str):
        with self._lock:
            user = self._store.get(user_id)
            if user:
                history = user.get("conversation_history", [])
                history.append({"role": role, "content": content, "timestamp": datetime.utcnow()})
               
                user["conversation_history"] = history[-20:]
                user["last_interaction"] = datetime.utcnow()

    def _parse_mastery(self, mastery_str) -> Optional[int]:
        if not mastery_str:
            return None
        if isinstance(mastery_str, int):
            return mastery_str
        m = re.search(r"(\d+)", str(mastery_str))
        if m:
            return int(m.group(1))
        return None
