
import json


def parse_json(json_text):
    try:
        return json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON input: {exc.msg}"
        ) from exc
