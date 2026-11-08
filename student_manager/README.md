# Student Record Manager (PyQt6)

Desktop app to add, edit, delete and search student records and marks.

## Requirements
- Python 3.10 or newer

## Install
```
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux
pip install -r requirements.txt
```
After installing, run `pip freeze > requirements.txt` to pin your exact PyQt6 version.

## Run
```
python main.py
```
Run the logic tests (no window needed): `python test_logic.py`

## Files
- `main.py` - starts the app
- `ui_main.py` - UI layer (widgets, layouts, signals/slots, styling)
- `logic.py` - validation and calculations
- `storage.py` - JSON load/save
- `data/students.json` - sample data (saved automatically on every change)

Before submitting: set `ROLL_NO` in `ui_main.py` and list AI-assisted portions in the report's References.