from typing import Dict, Any, List

def check_required(schema: Dict[str, Any], payload: Dict[str, Any]) -> (bool, List[str]):
    """
    Checks required fields in a payload against a schema.
    Returns (all_present: bool, missing_fields: list of str).
    Handles top-level and simple nested fields (dot notation).
    """
    missing = []
    for r in schema.get("required", []):
        
        parts = r.split(".")
        value = payload
        for p in parts:
            if isinstance(value, dict) and p in value:
                value = value[p]
            else:
                value = None
                break
        if value in (None, "", []):
            missing.append(r)

    all_present = len(missing) == 0
    return all_present, missing
