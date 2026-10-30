"""JSON persistence helpers."""
import json
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).parent / "data"


def load_records(filename: str) -> list[dict[str, Any]]:
    """Load a JSON list from the data directory, creating it if missing."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / filename
    if not path.exists():
        path.write_text("[]\n", encoding="utf-8")
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{filename} contains invalid JSON.") from exc
    if not isinstance(data, list):
        raise ValueError(f"{filename} must contain a JSON list.")
    return data


def save_records(filename: str, records: list[dict[str, Any]]) -> None:
    """Save records as formatted JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / filename
    path.write_text(json.dumps(records, indent=4, ensure_ascii=False) + "\n",
                    encoding="utf-8")
