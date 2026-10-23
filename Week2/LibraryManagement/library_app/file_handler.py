
import json
from pathlib import Path

from library_app.validators import DataFileError


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def read_json(filename):
    path = DATA_DIR / filename

    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            write_json(filename, [])
            return []

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise DataFileError(
                f"{filename} must contain a JSON list."
            )

        return data

    except DataFileError:
        raise
    except (OSError, json.JSONDecodeError) as exc:
        raise DataFileError(
            f"Unable to read {filename}: {exc}"
        ) from exc


def write_json(filename, data):
    path = DATA_DIR / filename
    temporary_path = path.with_suffix(path.suffix + ".tmp")

    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        with temporary_path.open(
            "w", encoding="utf-8"
        ) as file:
            json.dump(data, file, indent=4)

        temporary_path.replace(path)

    except (OSError, TypeError, ValueError) as exc:
        try:
            temporary_path.unlink(missing_ok=True)
        except OSError:
            pass

        raise DataFileError(
            f"Unable to write {filename}: {exc}"
        ) from exc
