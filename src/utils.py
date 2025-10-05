from typing import Dict, Any, List, Tuple

def check_required(schema: Dict[str, Any], payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Checks if all required fields from the schema are present in the payload.
    Returns (True, []) if all good, else (False, [missing fields]).
    """
    required_fields = schema.get("required", [])
    missing = [r for r in required_fields if r not in payload or payload[r] in (None, "", [])]
    if missing:
        return False, missing
    return True, []
