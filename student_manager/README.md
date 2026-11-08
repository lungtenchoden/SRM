# Student Record Manager

## 1. Project Description
The Student Record Manager is a desktop-based application developed using Python and PyQt6. It helps a teacher keep student records and marks. Users can add, edit, delete and search students, and see each student's average and Pass/Fail result through a graphical user interface. Records are saved to a JSON file, so they are still there when the application is closed and reopened.

## 2. Technologies Used

***Python:** Main programming language.
***PyQt6:** Used to develop the graphical user interface.
***JSON:** Used to store the student records in a file (`data/students.json`).
***Qt Style Sheets (QSS):** Used to customise the application's appearance.

## 3. Main Features

**Student Record Management**

*Add new students (roll number, name, class and marks).
*View all student records in a table.
*Search students by name or roll number.
*Update student information.
*Delete student records after a confirmation dialog.

**Marks and Results**

*Enter marks for three subjects (English, Maths and ICT), limited to 0-100.
*Calculate each student's average automatically.
*Show a Pass or Fail result (a student passes only with 40 or more in every subject).
*Filter the list to show only failing students.

**Class Summary**

*Display the class average in a progress bar.
*Display how many students are shown in the status bar.

**Input Validation**

*Reject a blank roll number or name.
*Reject a duplicate roll number.
*Reject marks outside 0-100.
*Show friendly error messages instead of crashing.

**Data Storage**

*Save the records to a JSON file after every change.
*Load the saved records when the application starts.
*Keep the records after closing and reopening the application.

## 4. Project Structure

```
Unit V/
│
├── partA/
│   ├── hello_kivy.py
│   ├── hello_pyqt6.py
│   └── hello_tkinter.py
│
└── student_manager/
    ├── data/
    │   └── students.json
    ├── logic.py
    ├── main.py
    ├── README.md
    ├── requirements.txt
    ├── storage.py
    ├── test_logic.py
    └── ui_main.py
```

*`main.py` starts the application.
*`ui_main.py` is the user interface layer (widgets, layouts, signals and slots, styling).
*`logic.py` is the logic layer (validation, add, update, delete, search and averages).
*`storage.py` is the data layer (loading and saving the JSON file).
*`test_logic.py` contains automated tests for `logic.py` and `storage.py`.
*`data/students.json` stores the student records.
*`partA/` contains the Hello World programs for Tkinter, PyQt6 and Kivy.

## 5. Requirements
Before running the application, ensure that the following are installed:

*Python 3.13 (tested). Python 3.10 or newer is required.
*pip (Python package installer)

Check your Python version with:

```
python --version
```

## 6. Installation and Setup

**Step 1: Open the Project Folder**

Unzip the submitted ZIP file, then open a terminal inside the `student_manager` folder (the folder that contains `main.py`):

```
cd student_manager
```

**Step 2: Create a Virtual Environment**

```
python -m venv venv
```

**Step 3: Activate the Virtual Environment**

For Windows PowerShell:

```
venv\Scripts\Activate.ps1
```

For Windows Command Prompt:

```
venv\Scripts\activate
```

For Mac / Linux:

```
source venv/bin/activate
```

When it is active, `(venv)` appears at the start of the terminal line.

**Step 4: Install Required Dependencies**

```
pip install -r requirements.txt
```

The pinned versions in `requirements.txt` are:

```
PyQt6==6.12.0
PyQt6-Qt6==6.12.0
PyQt6_sip==13.13.0
```

## 7. Running the Application
After completing the installation, run:

```
python main.py
```

The Student Record Manager opens with the sample students already loaded.

**Quick guide**

***Add a student:** click **Clear form**, fill in the form, then click **Add**.
***Edit a student:** click a row, change the details, then click **Update**.
***Delete a student:** click a row, click **Delete**, then confirm with **Yes**.
***Search:** type a name or roll number in the search box. Click **Clear** to show everyone again.
***Failing students:** tick **Show only failing**.
***About:** open **Help > About**.

## 8. Data File and Sample Data
The application stores its records in a JSON file, `data/students.json`. The file is read when the application starts and rewritten after every add, update and delete. Each student has a unique roll number, a name, a class and a list of three marks in the order English, Maths, ICT.

The sample data included with the project is:

```json
{
  "students": [
    {"roll_no": "101", "name": "Tashi Dorji", "class": "6A", "marks": [78, 85, 64]},
    {"roll_no": "102", "name": "Pema Lhamo", "class": "6A", "marks": [92, 88, 95]},
    {"roll_no": "103", "name": "Karma Wangchuk", "class": "6B", "marks": [35, 52, 48]},
    {"roll_no": "104", "name": "Sonam Choden", "class": "7A", "marks": [60, 45, 71]}
  ]
}
```

To reset to the sample data, paste the text above into `data/students.json`. If the file is missing or damaged, the application starts with an empty list and creates a new file the next time it saves.

## 9. Testing

**Automated tests.** The logic and storage layers can be tested without opening a window:


python test_logic.py


The last line should read `All tests passed.`

**Manual tests.** The window itself was tested by hand with 13 test cases, including adding, validation errors, searching, deleting with confirmation, updating, the failing filter and persistence after reopening. The test table is in section 7 of the project report.

## 10. Part A: Framework Hello World Programs
The `partA/` folder contains the Hello World programs developed to explore different Python GUI frameworks:

* Tkinter (`hello_tkinter.py`)
* PyQt6 (`hello_pyqt6.py`)
* Kivy (`hello_kivy.py`)

Each program shows a label and a button that changes the label when clicked. Tkinter needs no installation, and the PyQt6 program uses the packages from Step 4. For the Kivy program, first run `pip install kivy`. Then, from the `partA` folder:

```
python hello_tkinter.py
python hello_pyqt6.py
python hello_kivy.py
```

## 11. Author
Lungten Choden, Roll No. 14, B.Ed ICT, Samtse College of Education, Royal University of Bhutan.

Developed as part of the Unit V assignment, Exploring GUI Frameworks (PyQt, Kivy & Alternatives). Parts of this project were developed with assistance from Claude (Anthropic); the AI-assisted portions are listed in the References section of the project report.