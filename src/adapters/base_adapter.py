from typing import Dict, Any
import asyncio

class BaseAdapter:
    """
    Base adapter interface for all tools.
    Subclasses must implement async `call(payload)` method.
    """
    async def call(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0.05)
        return {"status": "ok", "echo": payload}
