import json
import os
from datetime import datetime, timezone
from pathlib import Path

def write_report(records, rejected, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "summary": {"received": len(records) + len(rejected),
                    "processed": len(records), "rejected": len(rejected)},
        "records": records,
        "rejected_records": rejected,
    }
    temp = path.with_suffix(path.suffix + ".tmp")
    try:
        temp.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()
    return path
