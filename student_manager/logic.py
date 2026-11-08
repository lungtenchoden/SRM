"""Business logic for the Student Record Manager.

Plain Python only (no PyQt), so it can be tested without opening a window.
"""

SUBJECTS = ["English", "Maths", "ICT"]
PASS_MARK = 40


class StudentManager:
    """Keeps the list of students and enforces the validation rules."""

    def __init__(self, students=None):
        self.students = students if students is not None else []

    # ---------- helpers ----------
    def find(self, roll_no):
        """Return the student with this roll number, or None."""
        for student in self.students:
            if student["roll_no"] == roll_no:
                return student
        return None

    @staticmethod
    def _clean(roll_no, name, cls, marks):
        """Validate the inputs and return cleaned copies (raises ValueError)."""
        roll_no = str(roll_no).strip()
        name = str(name).strip()
        if not roll_no:
            raise ValueError("Roll number cannot be empty.")
        if not name:
            raise ValueError("Name cannot be empty.")
        if len(marks) != len(SUBJECTS):
            raise ValueError(f"Exactly {len(SUBJECTS)} marks are required.")
        cleaned = []
        for mark in marks:
            try:
                mark = int(mark)
            except (TypeError, ValueError):
                raise ValueError("Marks must be whole numbers.") from None
            if not 0 <= mark <= 100:
                raise ValueError("Marks must be between 0 and 100.")
            cleaned.append(mark)
        return roll_no, name, cls, cleaned

    # ---------- operations ----------
    def add_student(self, roll_no, name, cls, marks):
        roll_no, name, cls, marks = self._clean(roll_no, name, cls, marks)
        if self.find(roll_no) is not None:
            raise ValueError(f"Roll number {roll_no} already exists.")
        self.students.append(
            {"roll_no": roll_no, "name": name, "class": cls, "marks": marks}
        )

    def update_student(self, roll_no, name, cls, marks):
        roll_no, name, cls, marks = self._clean(roll_no, name, cls, marks)
        student = self.find(roll_no)
        if student is None:
            raise ValueError(f"Roll number {roll_no} was not found.")
        student["name"] = name
        student["class"] = cls
        student["marks"] = marks

    def delete_student(self, roll_no):
        student = self.find(roll_no)
        if student is None:
            raise ValueError(f"Roll number {roll_no} was not found.")
        self.students.remove(student)

    def search(self, text):
        """Students whose name or roll number contains the text."""
        text = text.strip().lower()
        if not text:
            return list(self.students)
        return [
            s for s in self.students
            if text in s["name"].lower() or text in s["roll_no"].lower()
        ]

    # ---------- calculations ----------
    @staticmethod
    def total(student):
        return sum(student["marks"])

    def average(self, student):
        return self.total(student) / len(student["marks"])

    @staticmethod
    def passed(student):
        """A student passes only if every subject is at or above PASS_MARK."""
        return all(mark >= PASS_MARK for mark in student["marks"])

    def class_average(self):
        if not self.students:
            return 0.0
        return sum(self.average(s) for s in self.students) / len(self.students)