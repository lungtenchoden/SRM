"""Saving and loading students as JSON (no PyQt here)."""
import json
from pathlib import Path

# Relative to this file, never an absolute path.
DATA_FILE = Path(__file__).resolve().parent / "data" / "students.json"


def _is_valid_record(record):
    """Skip damaged records instead of crashing the app."""
    return (
        isinstance(record, dict)
        and all(key in record for key in ("roll_no", "name", "class", "marks"))
        and isinstance(record["marks"], list)
        and len(record["marks"]) == 3
    )


def load_students(path=DATA_FILE):
    """Return the saved students, or an empty list if the file is missing/corrupt."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        students = data.get("students", [])
    except (OSError, json.JSONDecodeError, AttributeError):
        return []
    if not isinstance(students, list):
        return []
    return [s for s in students if _is_valid_record(s)]


def save_students(students, path=DATA_FILE):
    """Write the students to JSON. Raises OSError if the file can't be written."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump({"students": students}, file, indent=2)