import json
from typing import Dict, Any
from pathlib import Path
from src.adapters.mock_note_maker import MockNoteMaker
from src.adapters.mock_flashcard import MockFlashcard
from src.adapters.mock_concept_explainer import MockConceptExplainer

SCHEMA_DIR = Path(__file__).parent / "schemas"


class ToolOrchestrator:
    def __init__(self):
        
        self.adapters = {
            "note_maker": MockNoteMaker(),
            "flashcard_generator": MockFlashcard(),
            "concept_explainer": MockConceptExplainer(),
        }
       
        self.last_payloads: Dict[str, Dict[str, Any]] = {}

    def register_adapter(self, tool_name: str, adapter_instance):
        """
        Dynamically add a new adapter at runtime.
        """
        self.adapters[tool_name] = adapter_instance

    def load_schema(self, tool_name: str) -> Dict[str, Any]:
        """
        Loads the JSON schema for a tool.
        Returns {} if tool_name is invalid or file not found.
        """
        mapping = {
            "note_maker": "note_maker_schema.json",
            "flashcard_generator": "flashcard_schema.json",
            "concept_explainer": "concept_explainer_schema.json",
        }
        fname = mapping.get(tool_name)
        if not fname:
            print(f" No schema mapping found for tool: {tool_name}")
            return {}

        p = SCHEMA_DIR / fname
        if not p.exists():
            print(f" Schema file missing for {tool_name}: {p}")
            return {}

        try:
            return json.loads(p.read_text())
        except json.JSONDecodeError as e:
            print(f" Failed to parse schema JSON for {tool_name}: {e}")
            return {}

    async def call_tool(self, tool_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calls the tool adapter safely. Returns error dict if anything goes wrong.
        """
        adapter = self.adapters.get(tool_name)
        if not adapter:
            return {"error": f"No adapter found for tool {tool_name}"}

        try:
            result = await adapter.call(payload)
            if not isinstance(result, dict):
                return {"error": f"Adapter returned invalid type for {tool_name}"}
            
            self.last_payloads[tool_name] = payload
            return result
        except Exception as e:
            print(f"Adapter call failed for {tool_name}: {e}")
            return {"error": f"Adapter call failed for {tool_name}: {str(e)}"}

    def make_clarifying_question(self, tool_name: str, payload: Dict[str, Any], schema: Dict[str, Any]) -> str:
        """
        Returns a concise question asking for the most critical missing required field.
        """
        required = schema.get("required", [])
        for r in required:
            if payload.get(r) in (None, "", []):
                return f"Quick question: could you specify `{r}` for the {tool_name.replace('_', ' ')}?"
        return "Could you clarify your request?"

    def check_missing_fields(self, tool_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns a dict of missing required fields.
        """
        schema = self.load_schema(tool_name)
        missing = {}
        for r in schema.get("required", []):
            if payload.get(r) in (None, "", []):
                missing[r] = "required"
        return missing
