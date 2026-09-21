from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel
)

from PySide6.QtCore import Qt

from app.chat import ChatWidget


class IRISWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IRIS")
        self.resize(1000, 700)
        self.setMinimumSize(800, 550)

        central_widget = QWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(8)

        title = QLabel("IRIS")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")

        subtitle = QLabel("Your AI assistant")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("subtitle")

        status = QLabel("● Online")
        status.setAlignment(Qt.AlignCenter)
        status.setObjectName("status")

        chat = ChatWidget()

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(status)
        layout.addSpacing(12)
        layout.addWidget(chat)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #171717;
            }

            QWidget {
                background-color: #171717;
                color: #f5f5f5;
                font-family: Arial;
            }

            QLabel#title {
                font-size: 30px;
                font-weight: bold;
                color: #ffffff;
                padding-top: 4px;
            }

            QLabel#subtitle {
                font-size: 15px;
                color: #a1a1aa;
            }

            QLabel#status {
                font-size: 13px;
                color: #4ade80;
                padding-top: 4px;
            }

            QTextEdit {
                background-color: #111111;
                border: 1px solid #303030;
                border-radius: 14px;
                padding: 16px;
                font-size: 15px;
                color: #f5f5f5;
                selection-background-color: #3f3f46;
            }

            QLineEdit {
                background-color: #111111;
                border: 1px solid #303030;
                border-radius: 12px;
                padding: 13px;
                font-size: 15px;
                color: #ffffff;
            }

            QLineEdit:focus {
                border: 1px solid #666666;
            }

            QPushButton {
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 12px;
                padding: 11px 18px;
                font-size: 14px;
                color: #ffffff;
            }

            QPushButton:hover {
                background-color: #353535;
            }

            QPushButton:pressed {
                background-color: #202020;
            }

            QPushButton:disabled {
                background-color: #202020;
                color: #666666;
            }
        """)