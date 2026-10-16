import csv
import json
import os
from pathlib import Path

from employee_app.validators import DataFileError


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def _path(filename):
    # Only allow plain filenames to avoid paths escaping the data folder.
    if Path(filename).name != filename:
        raise DataFileError("Use a filename without directory paths.")
    return DATA_DIR / filename


def read_json(filename):
    path = _path(filename)
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            write_json(filename, [])
            return []
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise DataFileError(f"{filename} must contain a JSON list.")
        return data
    except DataFileError:
        raise
    except (OSError, json.JSONDecodeError) as exc:
        raise DataFileError(f"Unable to read {filename}: {exc}") from exc


def write_json(filename, data):
    path = _path(filename)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        os.replace(temporary_path, path)
    except (OSError, TypeError, ValueError) as exc:
        try:
            temporary_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise DataFileError(f"Unable to write {filename}: {exc}") from exc


def read_csv(filename):
    path = _path(filename)
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            return list(csv.DictReader(file))
    except OSError as exc:
        raise DataFileError(f"Unable to read {filename}: {exc}") from exc


def write_csv(filename, records, fieldnames):
    path = _path(filename)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with temporary_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
        os.replace(temporary_path, path)
    except (OSError, TypeError, ValueError) as exc:
        try:
            temporary_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise DataFileError(f"Unable to write {filename}: {exc}") from exc
