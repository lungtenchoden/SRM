"""Main window for the Student Record Manager (PyQt6).

UI only: all rules live in logic.py and all file handling in storage.py.
"""
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QAbstractItemView, QCheckBox, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit, QMainWindow, QMessageBox,
    QProgressBar, QPushButton, QSpinBox, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget,
)

from logic import SUBJECTS, StudentManager
from storage import load_students, save_students

STUDENT_NAME = "Lungten Choden"
ROLL_NO = "14"  
CLASSES = ["6A", "6B", "7A", "7B", "8A", "8B"]

STYLESHEET = """
QMainWindow, QWidget { background-color: #f4f6fb; font-size: 13px; }
QGroupBox { font-weight: bold; border: 1px solid #c5cae9;
            border-radius: 6px; margin-top: 10px; padding: 8px; }
QGroupBox::title { subcontrol-origin: margin; left: 10px; }
QPushButton { background-color: #3f51b5; color: white;
              border: none; border-radius: 4px; padding: 6px 14px; }
QPushButton:hover { background-color: #303f9f; }
QPushButton#deleteButton { background-color: #c62828; }
QPushButton#deleteButton:hover { background-color: #8e0000; }
QLineEdit, QSpinBox, QComboBox { padding: 4px; background: white;
                                 border: 1px solid #b0b6d0; border-radius: 3px; }
QLineEdit:read-only { background: #e8eaf6; }
QTableWidget { background: white; alternate-background-color: #eef1fb;
               gridline-color: #d0d4e8; }
QHeaderView::section { background-color: #3f51b5; color: white;
                       padding: 4px; border: none; }
QProgressBar { border: 1px solid #b0b6d0; border-radius: 4px; text-align: center; }
QProgressBar::chunk { background-color: #43a047; }
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = StudentManager(load_students())
        self.selected_roll = None  # roll number of the row being edited

        self.setWindowTitle(f"Student Record Manager - {STUDENT_NAME} ({ROLL_NO})")
        self.resize(900, 650)
        self.setMinimumSize(700, 500)
        self.setStyleSheet(STYLESHEET)

        self._build_menu()
        self._build_ui()
        self._connect_signals()
        self.refresh_table()

    # ---------- building the interface ----------
    def _build_menu(self):
        file_menu = self.menuBar().addMenu("&File")
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = self.menuBar().addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)  # outer layout: stacks everything

        # Search row (QHBoxLayout)
        search_row = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search by name or roll number")
        self.clear_search_btn = QPushButton("Clear")
        self.fail_check = QCheckBox("Show only failing")
        search_row.addWidget(QLabel("Search:"))
        search_row.addWidget(self.search_edit, 1)
        search_row.addWidget(self.clear_search_btn)
        search_row.addWidget(self.fail_check)
        main_layout.addLayout(search_row)

        # Student table
        headers = ["Roll No", "Name", "Class", *SUBJECTS, "Average", "Result"]
        self.table = QTableWidget(0, len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.table, 1)

        # Form (QGridLayout inside a group box)
        form_box = QGroupBox("Student details")
        grid = QGridLayout(form_box)
        self.roll_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.class_combo = QComboBox()
        self.class_combo.addItems(CLASSES)
        grid.addWidget(QLabel("Roll No:"), 0, 0)
        grid.addWidget(self.roll_edit, 0, 1)
        grid.addWidget(QLabel("Name:"), 0, 2)
        grid.addWidget(self.name_edit, 0, 3)
        grid.addWidget(QLabel("Class:"), 1, 0)
        grid.addWidget(self.class_combo, 1, 1)

        self.mark_spins = []
        for i, subject in enumerate(SUBJECTS):
            spin = QSpinBox()
            spin.setRange(0, 100)
            self.mark_spins.append(spin)
            row, col = 2 + i // 2, (i % 2) * 2
            grid.addWidget(QLabel(f"{subject}:"), row, col)
            grid.addWidget(spin, row, col + 1)
        main_layout.addWidget(form_box)

        # Button row (QHBoxLayout)
        button_row = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setObjectName("deleteButton")  # styled red in the QSS
        self.clear_btn = QPushButton("Clear form")
        for button in (self.add_btn, self.update_btn, self.delete_btn, self.clear_btn):
            button_row.addWidget(button)
        main_layout.addLayout(button_row)

        # Class average bar
        self.avg_bar = QProgressBar()
        self.avg_bar.setRange(0, 100)
        self.avg_bar.setFormat("Class average: %p%")
        main_layout.addWidget(self.avg_bar)

    def _connect_signals(self):
        """Signals/slots: every user action is wired here."""
        self.add_btn.clicked.connect(self.on_add)
        self.update_btn.clicked.connect(self.on_update)
        self.delete_btn.clicked.connect(self.on_delete)
        self.clear_btn.clicked.connect(self.clear_form)
        self.clear_search_btn.clicked.connect(self.search_edit.clear)
        self.search_edit.textChanged.connect(self.on_filter_changed)
        self.fail_check.toggled.connect(self.on_filter_changed)
        self.table.itemSelectionChanged.connect(self.on_row_selected)

    # ---------- helpers ----------
    def _read_marks(self):
        return [spin.value() for spin in self.mark_spins]

    def _save(self):
        try:
            save_students(self.manager.students)
        except OSError as error:
            QMessageBox.critical(self, "Save failed", f"Could not save data:\n{error}")

    def refresh_table(self):
        """Rebuild the table from the manager, applying search and filter."""
        students = self.manager.search(self.search_edit.text())
        if self.fail_check.isChecked():
            students = [s for s in students if not self.manager.passed(s)]

        self.table.blockSignals(True)
        self.table.setRowCount(len(students))
        for row, student in enumerate(students):
            values = [
                student["roll_no"], student["name"], student["class"],
                *student["marks"],
                f"{self.manager.average(student):.1f}",
                "Pass" if self.manager.passed(student) else "Fail",
            ]
            for col, value in enumerate(values):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
        self.table.blockSignals(False)

        self.avg_bar.setValue(round(self.manager.class_average()))
        self.statusBar().showMessage(
            f"Showing {len(students)} of {len(self.manager.students)} students"
        )

    # ---------- slots (event handlers) ----------
    def on_add(self):
        if self.selected_roll is not None:
            QMessageBox.warning(
                self, "Form in use",
                "A student is selected. Click 'Clear form' before adding a new one.",
            )
            return
        try:
            self.manager.add_student(
                self.roll_edit.text(), self.name_edit.text(),
                self.class_combo.currentText(), self._read_marks(),
            )
        except ValueError as error:
            QMessageBox.warning(self, "Invalid input", str(error))
            return
        self._save()
        self.refresh_table()
        self.clear_form()

    def on_update(self):
        if self.selected_roll is None:
            QMessageBox.warning(self, "No selection", "Select a student in the table first.")
            return
        try:
            self.manager.update_student(
                self.selected_roll, self.name_edit.text(),
                self.class_combo.currentText(), self._read_marks(),
            )
        except ValueError as error:
            QMessageBox.warning(self, "Invalid input", str(error))
            return
        self._save()
        self.refresh_table()
        self.clear_form()

    def on_delete(self):
        if self.selected_roll is None:
            QMessageBox.warning(self, "No selection", "Select a student in the table first.")
            return
        answer = QMessageBox.question(
            self, "Confirm delete",
            f"Delete student {self.selected_roll}? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        try:
            self.manager.delete_student(self.selected_roll)
        except ValueError as error:
            QMessageBox.warning(self, "Delete failed", str(error))
            return
        self._save()
        self.refresh_table()
        self.clear_form()

    def on_filter_changed(self, *_):
        self.refresh_table()

    def on_row_selected(self):
        """Fill the form with the student chosen in the table."""
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return
        roll_no = self.table.item(rows[0].row(), 0).text()
        student = self.manager.find(roll_no)
        if student is None:
            return
        self.selected_roll = roll_no
        self.roll_edit.setText(student["roll_no"])
        self.roll_edit.setReadOnly(True)  # roll number is the key; don't change it
        self.name_edit.setText(student["name"])
        index = self.class_combo.findText(student["class"])
        if index < 0:
            self.class_combo.addItem(student["class"])
            index = self.class_combo.findText(student["class"])
        self.class_combo.setCurrentIndex(index)
        for spin, mark in zip(self.mark_spins, student["marks"]):
            spin.setValue(mark)

    def clear_form(self):
        self.selected_roll = None
        self.roll_edit.clear()
        self.roll_edit.setReadOnly(False)
        self.name_edit.clear()
        self.class_combo.setCurrentIndex(0)
        for spin in self.mark_spins:
            spin.setValue(0)
        self.table.clearSelection()

    def show_about(self):
        QMessageBox.about(
            self, "About",
            f"Student Record Manager\nBuilt with PyQt6\n\n{STUDENT_NAME}\nRoll No: {ROLL_NO}",
        )