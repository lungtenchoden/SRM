"""Quick tests for logic.py and storage.py. Run: python test_logic.py"""
import tempfile
from pathlib import Path

from logic import StudentManager
from storage import load_students, save_students


def raises_value_error(func, *args):
    try:
        func(*args)
    except ValueError:
        return True
    return False


def run():
    m = StudentManager()
    m.add_student("1", "Tashi", "6A", [78, 85, 64])
    assert len(m.students) == 1, "valid add"
    assert raises_value_error(m.add_student, "2", "  ", "6A", [50, 50, 50]), "blank name"
    assert raises_value_error(m.add_student, "1", "Dup", "6A", [50, 50, 50]), "duplicate roll"
    assert raises_value_error(m.add_student, "3", "A", "6A", [150, 50, 50]), "mark > 100"
    assert raises_value_error(m.add_student, "3", "A", "6A", [-1, 50, 50]), "negative mark"
    assert raises_value_error(m.add_student, "3", "A", "6A", ["x", 50, 50]), "non-number"
    assert raises_value_error(m.add_student, "", "A", "6A", [50, 50, 50]), "blank roll"

    m.add_student("2", "Pema", "6B", [30, 90, 90])
    assert [s["roll_no"] for s in m.search("pem")] == ["2"], "search by name"
    assert m.search("zzz") == [], "search no match"
    assert round(m.average(m.find("1")), 2) == 75.67, "average"
    assert m.passed(m.find("1")) and not m.passed(m.find("2")), "pass/fail"

    m.update_student("1", "Tashi D", "6B", [80, 80, 80])
    assert m.find("1")["name"] == "Tashi D", "update"
    assert raises_value_error(m.update_student, "99", "X", "6A", [1, 1, 1]), "update missing"

    m.delete_student("2")
    assert m.find("2") is None, "delete"
    assert raises_value_error(m.delete_student, "99"), "delete missing"

    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "students.json"
        save_students(m.students, path)
        assert load_students(path) == m.students, "save/load round trip"
        path.write_text("{ not valid json", encoding="utf-8")
        assert load_students(path) == [], "corrupt file does not crash"
        assert load_students(Path(folder) / "missing.json") == [], "missing file"

    print("All tests passed.")


if __name__ == "__main__":
    run()