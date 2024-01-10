import json
import os

def get(key):
    value = os.environ.get(key)
    if value:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
        return value
    return None
