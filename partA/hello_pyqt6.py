import sys

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("PyQt6 Hello - Lungten Choden (14)")
layout = QVBoxLayout(window)
label = QLabel("Hello")
button = QPushButton("Click me")
button.clicked.connect(lambda: label.setText("Hello, button clicked!"))
layout.addWidget(label)
layout.addWidget(button)
window.show()
sys.exit(app.exec())