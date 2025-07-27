import json
from settings.variables import LICENCE_OUTPUT_FILE

def is_licence_enabled(key: str, path: str = LICENCE_OUTPUT_FILE) -> bool:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get(key, "false").lower() == "true"